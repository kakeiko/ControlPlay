# 🎮 ControlPlay

Sistema de **controle e gerenciamento de tempo por dispositivo** desenvolvido em Python com Django, PostgreSQL e frontend simples em HTML.

O projeto permite registrar dispositivos, perfis, regras e sessões de uso, oferecendo controle centralizado e histórico de atividades.

---

## 🧠 Motivação

A ideia do ControlPlay surgiu após observar o controle manual de tempo em uma game house, onde os horários eram anotados em papel.  
Esse método gerava erros e falta de controle. O objetivo do projeto é automatizar esse processo, tornando-o mais confiável, escalável e fácil de gerenciar.

---

## 🚀 Funcionalidades

- CRUD completo para:
  - Perfis
  - Dispositivos
  - Regras
  - Sessões de uso

- Controle de tempo por sessão:
  - Backend informa início e término da sessão
  - Frontend monta e executa o cronômetro
  - Evita processamento contínuo no backend

- Histórico de atividades:
  - Sessão iniciada
  - Perfil criado
  - Eventos relevantes do sistema

- Frontend simples:
  - HTML básico
  - Sem CSS (utilizado apenas para testar funcionalidades)

---

## 🛠 Tecnologias Utilizadas até o momento

- Python  
- Django  
- HTML  
- PostgreSQL

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

## 📦 Instalação e Execução

1. Clone o repositório:
 ```bash
    git clone https://github.com/kakeiko/ControlPlay.git
```
Acesse a pasta do projeto:

```bash
    cd ControlPlay
    Crie um ambiente virtual:
```
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

Acesse no navegador:

```cpp
    http://127.0.0.1:8000/
```

⚔️ Desafios e Aprendizados
Estudo de conceitos de redes, como IP, tabela ARP e estrutura de MAC Address

Implementação do cronômetro:

Tentativa inicial no backend

Avaliação de async

Solução final no frontend, garantindo melhor desempenho e usabilidade

📌 Próximos Passos
Interface com CSS e layout responsivo

Identificação automática de dispositivos via rede

Dashboard visual de uso e sessões


🤝 Contribuição
Contribuições são bem-vindas!
Sinta-se à vontade para abrir issues ou pull requests.

📜 Licença
Projeto de código aberto, livre para uso e estudo.