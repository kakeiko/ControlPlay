from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Rule, UsageSession
from .service import bloquear_mac

@shared_task
def checar_tempo():
    sessions = UsageSession.objects.filter(status='Ativo')
    for s in sessions:
        regra = Rule.objects.get(usuario=s.usuario)
        agora = timezone.now()
        fim_sessao = s.start_time + timedelta(minutes=regra.tempo)
        if agora >= fim_sessao:
            s.end_time = agora
            s.duracao = int((s.end_time - s.start_time).total_seconds() / 60)
            s.status = 'Desativo'
            s.device.status = 'Desativo'
            s.usuario.status = 'Desativo'
            regra.tempo -= s.duracao
            if regra.tempo < 0:
                regra.tempo = 0
            bloquear_mac(s.device.macAddress)
            s.save()
            s.device.save()
            s.usuario.save()
            regra.save()
