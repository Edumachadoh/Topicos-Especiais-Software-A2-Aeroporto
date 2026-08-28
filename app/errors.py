from flask import Flask, jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.extensions import db


class AppError(Exception):
    """Raiz de todos os erros previstos da aplicação."""

    status_code = 400

    def __init__(self, mensagem: str, status_code: int | None = None) -> None:
        super().__init__(mensagem)
        self.mensagem = mensagem
        if status_code is not None:
            self.status_code = status_code


class RecursoNaoEncontrado(AppError):
    status_code = 404


class RegraDeNegocio(AppError):
    """Conflito com o estado atual dos dados (ex.: nome duplicado)."""

    status_code = 409


class ReferenciaInvalida(AppError):
    """Payload sintaticamente válido apontando para um recurso inexistente."""

    status_code = 422


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def tratar_erro_de_dominio(erro: AppError):
        db.session.rollback()
        return (
            jsonify(
                {
                    "code": erro.status_code,
                    "name": type(erro).__name__,
                    "description": erro.mensagem,
                }
            ),
            erro.status_code,
        )

    @app.errorhandler(ValidationError)
    def tratar_erro_de_validacao(erro: ValidationError):
        """Centraliza o 422 do Marshmallow.

        Sem este handler, cada rota precisaria do seu próprio try/except em
        volta do `schema.load()` — cinco blocos idênticos por recurso.
        """
        return (
            jsonify(
                {
                    "code": 422,
                    "name": "Unprocessable Entity",
                    "description": "Falha na validação do payload.",
                    "errors": erro.messages,
                }
            ),
            422,
        )

    @app.errorhandler(HTTPException)
    def tratar_http_exception(erro: HTTPException):
        """Converte os erros do próprio Werkzeug (404, 405, 400) para JSON."""
        return (
            jsonify(
                {
                    "code": erro.code,
                    "name": erro.name,
                    "description": erro.description,
                }
            ),
            erro.code,
        )

    @app.errorhandler(Exception)
    def tratar_excecao_generica(erro: Exception):
        """Rede de segurança para o que não foi previsto.

        Atenção ao `raise`: um handler registrado para `Exception` é chamado
        pelo Flask mesmo em modo debug. Sem re-levantar, o traceback some e
        você fica olhando para um 500 genérico sem pista nenhuma — exatamente
        o pior cenário durante uma aula ao vivo.
        """
        db.session.rollback()
        app.logger.exception("Erro não tratado")
        if app.debug or app.testing:
            raise erro
        return (
            jsonify(
                {
                    "code": 500,
                    "name": "Internal Server Error",
                    "description": "Ocorreu um erro interno inesperado no servidor.",
                }
            ),
            500,
        )
