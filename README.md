# 🎮 ControlPlay

ControlPlay é um **sistema web para controle e gerenciamento de tempo de uso por dispositivo**, desenvolvido em Python com Django, utilizando PostgreSQL, Celery, Redis e um frontend simples em HTML + CSS.

O sistema foi pensado para ambientes como game houses, lan houses ou laboratórios, oferecendo controle centralizado de sessões, usuários, dispositivos e histórico de atividades.

---

## 🧠 Motivação

O projeto surgiu a partir da observação de um problema real:
o controle manual de tempo em game houses, feito por anotações em papel, gera erros, retrabalho e falta de histórico confiável.

O ControlPlay automatiza esse processo, permitindo:

    - Controle preciso do tempo
    - Histórico de sessões
    - Redução de erros humanos
    - Base sólida para automações futuras (ex: bloqueio real de rede)

---

## 🚀 Funcionalidades

📋 Gerenciamento (CRUD)

    - Perfis de usuários
    - Dispositivos (consoles / PCs)
    - Regras de uso
    - Sessões de utilização

⏱ Controle de Sessões

    - Registro de início e fim da sessão no backend
    - Cronômetro executado no frontend
    - Evita processamento contínuo no servidor
    - Finalização automática da sessão ao término do tempo

🌐 Controle de Rede (Base)

    - Identificação de dispositivos por:
        - IP
        - MAC Address
    - Estrutura preparada para futuras integrações com bloqueio real de rede (ex: Mikrotik)

📜 Logs do Sistema

    - Registro de ações realizadas
    - Responsável pela ação
    - Data e horário
    - Histórico completo para auditoria
---

## 🛠 Tecnologias Utilizadas até o momento

- Python  
- Django  
- HTML
- CSS
- PostgreSQL
- Docker
- Redis
- Celery
- Celery Beat

---

## 📁 Estrutura do Projeto

ControlPlay/

├── core/ # Aplicação principal (models, views, lógica)

├── templates/ # Templates HTML

├── manage.py # Comandos Django

├── requirements.txt # Dependências

├── setup/ # Configurações do projeto

└── .gitignore

---

## 🔐 Variáveis de Ambiente

Este projeto utiliza variáveis de ambiente para configurações sensíveis.

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```env
    SECRET_KEY=your-secret-key-here

    ENGINE=django.db.backends.postgresql_psycopg2
    NAME=controlplay
    USER=postgres
    PASSWORD=postgres
    HOST=localhost
    PORT=5432
    MKT_HOST=IP_MIKROTIK
    MKT_USERNAME=SEU_USUARIO
    MKT_PASSWORD=SUA_PASSWORD
```
⚠️ Nunca versionar o arquivo .env

🐘 Configurando o PostgreSQL
Crie um banco de dados:

```sql
    CREATE DATABASE controlplay;
```

Certifique-se de que as credenciais informadas no .env estão corretas.

---

## 📦 Instalação e Execução

1. Clone o repositório:
 ```bash
git clone https://github.com/kakeiko/ControlPlay.git
```
Acesse a pasta do projeto:

```bash
cd ControlPlay
```
Crie um ambiente virtual:

```bash
python -m venv venv
```
Ative o ambiente virtual:

Windows

```bash
venv\Scripts\activate
```
Linux / MacOS

```bash
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```
Execute as migrations:

```bash
python manage.py migrate
```
Inicie o servidor:

```bash
python manage.py runserver
```
Suba o Redis com Docker:

```bash
docker run -d --name redis -p 6379:6379 redis
```

Inicie o worker do Celery:

```bash
celery -A setup  worker -l info --pool=solo
```

Inicie o Celery Beat:

```bash
celery -A setup beat -l info
```

Acesse no navegador:

```cpp
http://127.0.0.1:8000/
```

# ⚔️ Desafios e Aprendizados

- Estudo de conceitos de redes, como IP, tabela ARP e estrutura de MAC Address
- Implementação do cronômetro:
    - Tentativa inicial no backend
    - Avaliação de async
    - Solução final no frontend, garantindo melhor desempenho e usabilidade

# 📌 Possíveis Evoluções

    - Dashboard visual de uso e estatísticas
    - Gráficos de sessões e tempo consumido
    - Bloqueio automático de rede por dispositivo
    - Integração direta com equipamentos de rede


# 🤝 Contribuição

Contribuições são bem-vindas!
Sinta-se à vontade para abrir issues ou pull requests.

# 📜 Licença

Projeto de código aberto, livre para uso e estudo.