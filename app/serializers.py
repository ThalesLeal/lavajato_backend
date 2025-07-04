from rest_framework import serializers
from app.models import Lavagem, Funcionario  # Certifique-se de importar os modelos corretamente

# Serializer para a Lavagem
class LavagemSerializer(serializers.ModelSerializer):
    hora_inicio = serializers.SerializerMethodField()
    hora_fim = serializers.SerializerMethodField()

    class Meta:
        model = Lavagem
        fields = '__all__'  # Ou defina explicitamente os campos que deseja

    def get_hora_inicio(self, obj):
        """
        Retorna hora_inicio no formato HH:MM
        """
        if obj.hora_inicio:
            return obj.hora_inicio.strftime("%H:%M")
        return None

    def get_hora_fim(self, obj):
        """
        Retorna hora_fim no formato HH:MM
        """
        if obj.hora_fim:
            return obj.hora_fim.strftime("%H:%M")
        return None


# Serializer para o Funcionario
class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = '__all__'  # Ou defina explicitamente os campos que deseja
