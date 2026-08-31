from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Passagem(db.Model):
    __tablename__ = "passagens"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    assento: Mapped[str] = mapped_column(String(10), nullable=False)
    valor: Mapped[double] = mapped_column(nullable=False)

    voo: Mapped["Voo"] = mapped_column(ForeignKey("voos.id"), nullable=False)
    passageiro_id: Mapped["Passageiro"] = mapped_column(ForeignKey("passageiros.id"), nullable=False)

    def __repr__(self) -> str:
        return f"<Passagem {self.assento} {self.voo}>"