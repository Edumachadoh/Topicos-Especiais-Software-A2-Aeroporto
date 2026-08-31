from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Passageiro(db.Model):
    __tablename__ = "passageiros"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, nullable=True)

    voos: Mapped[list["Voo"]] = relationship(
        secondary="voo_passageiro",
        back_populates="passageiros",
    )

    def __repr__(self) -> str:
        return f"<Passageiro {self.nome}>"