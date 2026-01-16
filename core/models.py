from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
OPCOES_STATUS = [
    ("Ativo","Ativo"),
    ("Desativo","Desativo")
]

OPCOES_TIPO = [
    ("LimiteTempo", "LimiteTempo")
]

class Profile(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    status = models.CharField(max_length=100, blank=False, null=False, choices=OPCOES_STATUS, default="Desativo")
    dono = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=False, related_name="dono")

class Device(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False)
    macAddress = models.CharField(max_length=100, blank=False, null=False, unique=True)
    status = models.CharField(max_length=100, blank=False, null=False, choices=OPCOES_STATUS,default="Desativo")
    blocked = models.BooleanField(default=False)

class Rule(models.Model):
    tipo = models.CharField(max_length=100, blank=False, null=False, choices=OPCOES_TIPO, default="LimiteTempo")
    tempo = models.IntegerField(blank=False, null=False)
    usuario = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True, blank=False, related_name="usuario_regra")

class UsageSession(models.Model):
    device = models.ForeignKey(to=Device, on_delete=models.CASCADE, null=True, blank=False, related_name="console")
    usuario = models.ForeignKey(to=Profile, on_delete=models.CASCADE, null=True, blank=False, related_name="usuario_sessao")
    start_time = models.DateTimeField(blank=False, null=False, default=datetime.now())
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=100, blank=False, null=False, choices=OPCOES_STATUS, default="Ativo")
    duracao = models.IntegerField(blank=True, null=True)