from flask import Flask

from app.config import get_config
from app.errors import register_error_handlers
from app.extensions import db, ma, migrate


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__)

    config_cls = get_config(config_name)
    app.config.from_object(config_cls)
    config_cls.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from app import models  # noqa: F401
    
    # Importando os blueprints das novas entidades do sistema
    from app.routes.aeronave_routes import aeronave_bp
    from app.routes.passageiro_routes import passageiro_bp
    from app.routes.voo_routes import voo_bp

    # Registrando as rotas
    app.register_blueprint(aeronave_bp, url_prefix="/api/aeronaves")
    app.register_blueprint(passageiro_bp, url_prefix="/api/passageiros")
    app.register_blueprint(voo_bp, url_prefix="/api/voos")

    register_error_handlers(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app