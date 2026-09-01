from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Passageiro(db.Model):
    __tablename__ = "passageiros"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=True)

    passagens: Mapped[list["Passagem"]] = relationship(
        back_populates="passageiro",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Passageiro {self.nome}>"