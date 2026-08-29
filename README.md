# Sistema de Gestão Aeroportuária - API RESTful

API RESTful desenvolvida em Python utilizando o microframework Flask. Este projeto visa gerenciar as operações fundamentais de um aeroporto, controlando o cadastro de Aeronaves, Passageiros e a alocação de Voos. 

O sistema foi arquitetado visando a separação de responsabilidades (Clean Architecture), conformidade estrita com o protocolo HTTP (regras REST) e persistência de dados em banco relacional.

## 🛠️ Tecnologias Utilizadas

* **Framework Web:** Flask
* **Linguagem:** Python 3.12+
* **Banco de Dados:** MySQL
* **ORM:** Flask-SQLAlchemy
* **Migrações:** Flask-Migrate (Alembic)
* **Serialização e Validação (DTOs):** Marshmallow
* **Testes:** Pytest

## 📂 Estrutura de Diretórios e Arquitetura

O projeto adota uma arquitetura em camadas para isolar regras de negócio, rotas e acesso a dados.

```text
📦 projeto-aeroporto
 ┣ 📂 app
 ┃ ┣ 📂 models      # Camada de Dados: Classes ORM mapeadas para o banco (Aeronave, Passageiro, Voo)
 ┃ ┣ 📂 routes      # Camada de Apresentação: Controladores HTTP (Blueprints)
 ┃ ┣ 📂 schemas     # Camada de Validação/DTO: Serialização e validação de payloads JSON
 ┃ ┣ 📂 services    # Camada de Negócio: Regras, integrações e transações com o banco
 ┃ ┣ 📜 __init__.py # Application Factory (Inicialização do Flask)
 ┃ ┣ 📜 config.py   # Configurações de ambiente (Dev, Test, Prod)
 ┃ ┣ 📜 errors.py   # Interceptador global de exceções
 ┃ ┗ 📜 extensions.py # Instanciação centralizada de plugins (evita importação circular)
 ┣ 📂 migrations    # Histórico de versionamento do banco de dados (Alembic)
 ┣ 📂 tests         # Suíte de testes automatizados (Pytest)
 ┣ 📜 .env          # Variáveis de ambiente e credenciais (Não versionado)
 ┣ 📜 requirements.txt # Dependências do projeto
 ┗ 📜 run.py        # Ponto de entrada (Entry point) do servidor web