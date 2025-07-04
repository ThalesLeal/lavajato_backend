from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from datetime import datetime, time
from django.db import transaction
from app.models import Lavagem, Funcionario, Veiculo
from app.serializers import LavagemSerializer, FuncionarioSerializer
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework.views import APIView

# Definição do horário de expediente
WORK_START = time(8, 0)
WORK_END = time(18, 0)


def normalizar_hora(hora_str):
    """
    Converte uma string de hora para o formato HH:MM (remove segundos se existirem).
    Aceita entradas como '08:30' ou '08:30:00'
    """
    try:
        hora = datetime.strptime(hora_str, "%H:%M:%S").time()
    except ValueError:
        hora = datetime.strptime(hora_str, "%H:%M").time()
    return hora.strftime("%H:%M")


class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all()
    serializer_class = FuncionarioSerializer


class LavagemViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Lavagem.objects.all().order_by("data", "hora_inicio")
    serializer_class = LavagemSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["veiculo__placa", "tipo_lavagem", "data"]
    ordering_fields = ["data", "hora_inicio", "hora_fim"]
    ordering = ["data", "hora_inicio"]

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering_param = self.request.query_params.get('ordering')

        if not ordering_param:
            queryset = queryset.order_by(*self.ordering)
        else:
            queryset = queryset.order_by(*ordering_param.split(','), 'id')

        return queryset

    def filter_queryset(self, queryset):
        veiculo = self.request.query_params.get("veiculo")
        tipo_lavagem = self.request.query_params.get("tipo_lavagem")

        if veiculo and tipo_lavagem:
            queryset = queryset.filter(veiculo__placa=veiculo, tipo_lavagem=tipo_lavagem)

        queryset = super().filter_queryset(queryset)
        return queryset

    def create(self, request, *args, **kwargs):
        # Torna request.data mutável
        if hasattr(request.data, "_mutable"):
            request.data._mutable = True

        placa = request.data.get("veiculo")
        data_str = request.data.get("data")  # "DD/MM/YYYY"
        hora_inicio_str = request.data.get("hora_inicio")
        hora_fim_str = request.data.get("hora_fim")

        if not placa or not data_str or not hora_inicio_str or not hora_fim_str:
            return Response(
                {"non_field_errors": ["Campos obrigatórios: veiculo, data, hora_inicio e hora_fim."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificação de formato de data
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
        except ValueError:
            return Response(
                {"non_field_errors": ["Formato inválido para data. Use DD/MM/YYYY."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Normaliza hora para HH:MM
        try:
            hora_inicio_str = normalizar_hora(hora_inicio_str)
            hora_fim_str = normalizar_hora(hora_fim_str)
            hora_inicio_obj = datetime.strptime(hora_inicio_str, "%H:%M").time()
            hora_fim_obj = datetime.strptime(hora_fim_str, "%H:%M").time()
        except ValueError:
            return Response(
                {"non_field_errors": ["Formato inválido para hora. Use HH:MM ou HH:MM:SS."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Atualiza request.data com horas normalizadas
        request.data["hora_inicio"] = hora_inicio_str
        request.data["hora_fim"] = hora_fim_str

        # Verifica se o horário de início é anterior ao de término
        if hora_inicio_obj >= hora_fim_obj:
            return Response(
                {"non_field_errors": ["O horário de início deve ser anterior ao de término."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se o horário está dentro do expediente
        if hora_inicio_obj < WORK_START or hora_fim_obj > WORK_END:
            return Response(
                {"non_field_errors": ["Agendamentos devem ser realizados entre 08:00 e 18:00."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se já existe agendamento para o mesmo veículo e data
        existing_agendamentos = self.get_queryset().filter(
            veiculo__placa__iexact=placa,
            data=data_obj
        )

        # Verifica conflito de horários
        def overlaps(new_start, new_end, existing_start, existing_end):
            return not (new_end <= existing_start or new_start >= existing_end)

        conflict_found = any(
            overlaps(hora_inicio_obj, hora_fim_obj, ag.hora_inicio, ag.hora_fim)
            for ag in existing_agendamentos
        )

        if conflict_found:
            return Response(
                {"non_field_errors": ["Horário ocupado."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Chama a criação padrão do DRF após validações
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Torna request.data mutável
        if hasattr(request.data, "_mutable"):
            request.data._mutable = True

        placa = request.data.get("veiculo")
        data_str = request.data.get("data")  # "DD/MM/YYYY"
        hora_inicio_str = request.data.get("hora_inicio")
        hora_fim_str = request.data.get("hora_fim")

        if not placa or not data_str or not hora_inicio_str or not hora_fim_str:
            return Response(
                {"non_field_errors": ["Campos obrigatórios: veiculo, data, hora_inicio e hora_fim."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Normaliza hora para HH:MM
        try:
            hora_inicio_str = normalizar_hora(hora_inicio_str)
            hora_fim_str = normalizar_hora(hora_fim_str)
            hora_inicio_obj = datetime.strptime(hora_inicio_str, "%H:%M").time()
            hora_fim_obj = datetime.strptime(hora_fim_str, "%H:%M").time()
        except ValueError:
            return Response(
                {"non_field_errors": ["Formato inválido para hora. Use HH:MM ou HH:MM:SS."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Atualiza request.data com horas normalizadas
        request.data["hora_inicio"] = hora_inicio_str
        request.data["hora_fim"] = hora_fim_str

        # Verifica se o horário de início é anterior ao de término
        if hora_inicio_obj >= hora_fim_obj:
            return Response(
                {"non_field_errors": ["O horário de início deve ser anterior ao de término."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verifica se o horário está dentro do expediente
        if hora_inicio_obj < WORK_START or hora_fim_obj > WORK_END:
            return Response(
                {"non_field_errors": ["Agendamentos devem ser realizados entre 08:00 e 18:00."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().update(request, *args, **kwargs)

    def destroy(self, request, pk, *args, **kwargs):
        lavagem = self.get_object()
        if lavagem:
            lavagem.delete()
            return Response({"message": "Agendamento de lavagem excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "Agendamento não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    def perform_create(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def perform_update(self, serializer, **kwargs):
        serializer.save(**kwargs)
