from django.db import models
from django.contrib.auth.models import User

# Modelo para Veículo
class Veiculo(models.Model):
    nome = models.CharField(max_length=255)
    marca = models.CharField(max_length=255)
    placa = models.CharField(max_length=10, unique=True)
    cor = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.marca} {self.nome} - {self.placa}"

# Modelo para Funcionário (quem realiza a lavagem)
class Funcionario(models.Model):
    nome = models.CharField(max_length=255)
    # Adicione outros campos se necessário (telefone, e-mail, etc.)

    def __str__(self):
        return self.nome

# Opções para o tipo de lavagem
TIPO_LAVAGEM_CHOICES = [
    ("simples", "Simples"),
    ("completa", "Completa"),
    ("especial", "Especial"),
]

# Modelo para Lavagem (agendamento)
class Lavagem(models.Model):
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    tipo_lavagem = models.CharField(max_length=20, choices=TIPO_LAVAGEM_CHOICES)
    data = models.DateField()             # Data do agendamento
    hora_inicio = models.TimeField()      # Hora de início
    hora_fim = models.TimeField()         # Hora de término
    observacao = models.TextField(null=True, blank=True)
    funcionarios = models.ManyToManyField(Funcionario, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.veiculo.placa} - {self.data} ({self.hora_inicio} - {self.hora_fim})"
