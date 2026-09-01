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
```

## Arquitetura do Sistema

O projeto adota uma **Arquitetura em Camadas (Layered Architecture)** adaptada para o ecossistema Flask. Embora possua forte equivalência com o padrão tradicional de mercado (`Controllers`, `Services`, `Repository`, `Models`), a organização das responsabilidades difere em pontos estruturais específicos:

* **Routes (Controllers):** Camada de apresentação. Interceptam as requisições HTTP, extraem parâmetros das URLs e devolvem as respostas padronizadas com os respectivos *Status Codes*.
* **Services:** Cérebro da aplicação. Centralizam as lógicas de negócio, validações operacionais e a orquestração do sistema.
* **Models:** Camada de dados. Mapeiam fisicamente as tabelas e restrições do banco de dados relacional através do ORM (SQLAlchemy).
* **Schemas vs Repositories (Divergência Arquitetural):**
  * **Schemas:** Atuam como **DTOs (Data Transfer Objects)**. Eles validam a tipagem e integridade dos dados de entrada (JSON) na fronteira da API e serializam os objetos para a saída.
  * **Repositories:** Em arquiteturas tradicionais (como Java/Spring), isolariam as *queries* do banco. Neste projeto com Flask/SQLAlchemy, a responsabilidade do acesso a dados foi absorvida diretamente pela camada **Services** (via `db.session`), mantendo a base de código mais enxuta e eliminando a necessidade de diretórios adicionais para repositórios.



# Modelagem de Dados e Relacionamentos

A arquitetura de dados reflete as operações reais da aviação. A associação genérica (N:N) entre voos e passageiros foi substituída por uma entidade transacional dedicada (`Passagem`).

### Aeronave e Voo (1:N)
* Uma **Aeronave** pode realizar múltiplos **Voos** em sua vida útil.
* Um **Voo** está vinculado a apenas uma **Aeronave** específica.
* Fisicamente, a chave estrangeira (`aeronave_id`) reside na tabela `voos`. 

### Voo e Passagem (1:N)
* Um **Voo** contém múltiplas **Passagens** (representando os assentos alocados).
* Fisicamente, o banco de dados armazena a chave estrangeira (`voo_id`) dentro de cada linha da tabela `passagens`. 
* Lógica e estruturalmente, a classe `Voo` controla sua ocupação através de uma lista interna de passagens mapeada pelo ORM.

### Passageiro e Passagem (1:N)
* Um **Passageiro** pode ser titular de múltiplas **Passagens** (seu histórico de compras/viagens).
* Cada **Passagem** é nominal e pertence a apenas um **Passageiro**. 
* Fisicamente, a chave estrangeira (`passageiro_id`) fica na tabela `passagens`, garantindo o vínculo nominal do bilhete.

# 🧪 Testes Automatizados

A garantia de qualidade da API é realizada através de testes automatizados utilizando a biblioteca **Pytest**. A suíte de testes valida o funcionamento das rotas HTTP, esquemas de validação e regras de persistência de forma segura e isolada.

### 📂 Estrutura de Testes

Todos os arquivos responsáveis pela validação do sistema estão localizados no diretório `tests/`.

* **`conftest.py`:** É o arquivo de configuração global do Pytest. Ele intercepta a inicialização da aplicação e injeta **Fixtures** (recursos compartilhados). Sua principal função é gerar o *Test Client* do Flask e substituir a conexão do MySQL por um **banco de dados SQLite em memória** (`sqlite+pysqlite:///:memory:`). Isso garante que cada execução de teste comece com um banco vazio e não afete os dados reais do seu servidor MySQL.
* **Arquivos `test_*.py` (ex: `test_aeronave.py`, `test_voo.py`):** Contêm as suítes de teste individuais para cada domínio. Eles enviam requisições simuladas (POST, GET, PUT, DELETE) para a API e utilizam instruções `assert` para verificar se os *Status Codes* (200, 201, 404, 422) e os payloads JSON de resposta estão perfeitamente de acordo com as regras de negócio esperadas.

### 🚀 Como Executar os Testes

Certifique-se de que o seu ambiente virtual (`.venv`) está ativado no terminal antes de executar os comandos.

**1. Executar a suíte completa de testes:**
Roda todos os testes de todos os arquivos dentro da pasta `tests/`.
```bash
pytest