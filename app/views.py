from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import DjangoModelPermissions
from rest_framework_tracking.mixins import LoggingMixin
from datetime import datetime, time
from app.models import Lavagem, Funcionario
from app.serializers import LavagemSerializer, FuncionarioSerializer

class FuncionarioViewSet(viewsets.ModelViewSet):
    queryset = Funcionario.objects.all().order_by('nome')
    serializer_class = FuncionarioSerializer
    permission_classes = [DjangoModelPermissions]

class LavagemViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Lavagem.objects.all().order_by("data", "hora_inicio")
    serializer_class = LavagemSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["veiculo__placa", "tipo_lavagem", "data"]
    ordering_fields = ["data", "hora_inicio", "hora_fim"]
    ordering = ["data", "hora_inicio"]

    def create(self, request, *args, **kwargs):
        placa = request.data.get("veiculo")
        data_str = request.data.get("data")         # "DD/MM/YYYY"
        hora_inicio_str = request.data.get("hora_inicio")
        hora_fim_str = request.data.get("hora_fim")

        if not placa or not data_str or not hora_inicio_str or not hora_fim_str:
            return Response(
                {"non_field_errors": ["Campos obrigatórios: veiculo, data, hora_inicio e hora_fim."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
        except ValueError:
            return Response(
                {"non_field_errors": ["Formato inválido para data. Use DD/MM/YYYY."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            hora_inicio_obj = datetime.strptime(hora_inicio_str, "%H:%M").time()
            hora_fim_obj = datetime.strptime(hora_fim_str, "%H:%M").time()
        except ValueError:
            return Response(
                {"non_field_errors": ["Formato inválido para hora. Use HH:MM."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        if hora_inicio_obj >= hora_fim_obj:
            return Response(
                {"non_field_errors": ["O horário de início deve ser anterior ao de término."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        work_start = time(8, 0)
        work_end = time(18, 0)
        if hora_inicio_obj < work_start or hora_fim_obj > work_end:
            return Response(
                {"non_field_errors": ["Agendamentos devem ser realizados entre 08:00 e 18:00."]},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing_agendamentos = self.get_queryset().filter(
            veiculo__placa__iexact=placa,
            data=data_obj
        )

        def overlaps(new_start, new_end, existing_start, existing_end):
            return not (new_end <= existing_start or new_start >= existing_end)

        conflict_found = False
        for ag in existing_agendamentos:
            if overlaps(hora_inicio_obj, hora_fim_obj, ag.hora_inicio, ag.hora_fim):
                conflict_found = True
                break

        if conflict_found:
            intervals = []
            for ag in existing_agendamentos:
                intervals.append((ag.hora_inicio, ag.hora_fim))
            intervals.sort(key=lambda x: x[0])
            free_intervals = []
            current = work_start
            for start, end in intervals:
                if current < start:
                    free_intervals.append((current, start))
                if end > current:
                    current = end
            if current < work_end:
                free_intervals.append((current, work_end))
            free_slots = [f"{slot[0].strftime('%H:%M')} - {slot[1].strftime('%H:%M')}" for slot in free_intervals]
            return Response(
                {
                    "non_field_errors": [
                        "Horário ocupado.",
                        "Horários disponíveis: " + ", ".join(free_slots)
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().create(request, *args, **kwargs)
