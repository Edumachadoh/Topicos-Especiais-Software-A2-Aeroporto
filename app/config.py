import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Config:
    """Configuração comum a todos os ambientes."""

    SECRET_KEY = os.getenv("SECRET_KEY", "chave-insegura-apenas-para-aula")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'catalogo.db'}"
    )
    # Desligado por padrão desde o Flask-SQLAlchemy 3.x; mantido explícito
    # porque a turma vai ver esse nome em tutoriais antigos.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def init_app(cls, app) -> None:
        """Gancho de validação, chamado pela factory após `from_object`.

        Existe porque `app.config.from_object()` recebe a *classe* e nunca a
        instancia — validação escrita em `__init__` jamais seria executada.
        """


class DevelopmentConfig(Config):
    DEBUG = True
    # Ecoa o SQL gerado no console: útil para mostrar o N+1 e o cascade em aula.
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "0") == "1"


class TestingConfig(Config):
    TESTING = True
    # Banco em memória: cada execução da suíte começa do zero.
    SQLALCHEMY_DATABASE_URI = "sqlite+pysqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False

    @classmethod
    def init_app(cls, app) -> None:
        if cls.SECRET_KEY == Config.SECRET_KEY:
            raise RuntimeError(
                "SECRET_KEY não definida. Em produção ela é obrigatória. "
                "Falhar na inicialização é melhor que subir com chave conhecida."
            )


CONFIG_POR_NOME: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(nome: str | None = None) -> type[Config]:
    """Devolve a classe de configuração do ambiente pedido.

    A precedência é: argumento explícito > variável APP_ENV > development.
    """
    nome = nome or os.getenv("APP_ENV", "development")
    try:
        return CONFIG_POR_NOME[nome]
    except KeyError:
        validos = ", ".join(sorted(CONFIG_POR_NOME))
        raise ValueError(
            f"Ambiente '{nome}' desconhecido. Use um destes: {validos}."
        ) from None
