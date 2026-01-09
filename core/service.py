from datetime import datetime
from .models import Rule
import subprocess
import re
import requests
import socket

# Nomaliza os endereços mac para não ter o mesmo console porém com nomes diferentes
def format_mac(mac):
    mac = mac.lower()
    mac = mac.replace('-', '').replace(':', '').replace('.', '')
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

def usage_service(session, finalizada):
    regra = Rule.objects.get(usuario=session.profile)
    agora = datetime.now()
    usado = agora - session.start_time
    restante = regra.tempo - int(usado)
    if finalizada:
        session.end_time = datetime.now()
        session.duracao = session.end_time - session.start_time
        session.status = 'Desativo'
        session.device.status = 'Desativo'
        session.profile.status = 'Desativo'
        regra.tempo -= session.duracao
        # Aplicar lógica de bloquear acesso a internet
    return int(usado), restante

def get_device_type(mac, hostname):
    try:
        response = requests.get(f"https://api.macvendors.com/{mac}", timeout=2)
        print(response.status_code)
        if response.status_code == 200:
            fabricante = response.text.lower()
            if any(x in fabricante for x in ['sony']):
                return 'Playstation'
            if any(x in fabricante for x in ['microsoft']):
                return 'Xbox'
            if any(x in fabricante for x in ['nintendo']):
                return 'Nintendo'
            if 'desktop' in hostname or 'notebook' in hostname:
                return 'Computador'
            return 'N/A'
        return "Desconhecido"
    except:
        return "Erro na consulta"

def NetworkdiscoveryService():
    resultado = subprocess.check_output(["arp", "-a"]).decode('cp1252')
    padrao = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F-]+)\s+(\w+)')

    tabela_arp = []

    for linha in resultado.split('\n'):
        match = padrao.search(linha)
        if match:
            ip = match.group(1)
            mac = match.group(2)
            if not mac.startswith(('ff', '01-00-5e', '---')):
                try:
                    hostname = socket.gethostbyaddr(ip)[0]
                except:
                    hostname = 'N/A'
                
                tipo = get_device_type(mac,hostname)
                if any(x in tipo for x in ['Playstation','Xbox','Nintendo','Computador']):
                    tabela_arp.append({
                        'ip': ip,
                        'mac': mac,
                        'tipo': tipo,
                        'hostname': hostname
                    })
        
    print(tabela_arp)
    return tabela_arp