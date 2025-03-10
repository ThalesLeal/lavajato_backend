from rest_framework import serializers
from app.models import Lavagem, Veiculo, Funcionario

class VeiculoSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        # Tenta buscar o veículo de forma case-insensitive
        try:
            return self.get_queryset().get(**{self.slug_field + '__iexact': data})
        except self.get_queryset().model.DoesNotExist:
            # Cria uma nova instância com valores default
            # Você pode ajustar os valores default conforme sua necessidade
            new_vehicle = self.get_queryset().model.objects.create(
                placa=data,
                nome=data,         # ou outro valor que faça sentido
                marca="Desconhecido",
                cor="Desconhecido"
            )
            return new_vehicle

class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'

class LavagemSerializer(serializers.ModelSerializer):
    # Usa o campo customizado para veiculo
    veiculo = VeiculoSlugRelatedField(
        slug_field='placa',
        queryset=Veiculo.objects.all(),
        error_messages={'does_not_exist': 'Veículo não encontrado para a placa informada.'}
    )
    funcionarios = serializers.PrimaryKeyRelatedField(
        queryset=Funcionario.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = Lavagem
        fields = '__all__'
