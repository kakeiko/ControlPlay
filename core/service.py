from datetime import datetime
from .models import Rule, UsageSession
import subprocess
import re
import requests
import os
import socket
from routeros_api import RouterOsApiPool
from .models import Device

# Nomaliza os endereços mac para não ter o mesmo console porém com nomes diferentes
def format_mac(mac):
    mac = mac.lower()
    mac = mac.replace('-', '').replace(':', '').replace('.', '')
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

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

                tabela_arp.append({
                    'ip': ip,
                    'mac': mac,
                    'tipo': tipo,
                    'hostname': hostname
                })
        
    print(tabela_arp)
    return tabela_arp

def conectar_mikrotik():
    api_pool = RouterOsApiPool(
        host=os.getenv('MKT_HOST'),
        username=os.getenv('MKT_USERNAME'),
        password=os.getenv('MKT_PASSWORD'),
        plaintext_login=True
    )
    return api_pool.get_api()

def bloquear_mac(mac): 
    api = conectar_mikrotik()
    firewall_filter = api.get_resource('/ip/firewall/filter')

    firewall_filter.add(
        chain='forward',
        src_mac_address=mac.upper(),
        action='drop',
        comment='Bloqueado pelo ControlPlay'
    )
    device = Device.objects.get(macAddress=mac)
    device.blocked = True
    device.save()

def liberar_mac(mac):
    api = conectar_mikrotik()
    firewall_filter = api.get_resource('/ip/firewall/filter')

    regras = firewall_filter.get()

    for regra in regras:
        if regra.get('src-mac-address') == mac.upper() and \
           regra.get('comment') == 'Bloqueado pelo ControlPlay':
            firewall_filter.remove(id=regra['id'])
