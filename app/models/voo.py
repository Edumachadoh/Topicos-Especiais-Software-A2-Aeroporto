from __future__ import annotations

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Voo(db.Model):
    __tablename__ = "voos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    # Chave estrangeira explícita (Relacionamento N:1 com Aeronave)
    aeronave_id: Mapped[str] = mapped_column(ForeignKey("aeronaves.id"), nullable=False)

    aeronave: Mapped["Aeronave"] = relationship(back_populates="voos")

    passagens: Mapped[list["Passagem"]] = relationship(
        back_populates="voo",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Voo {self.id}>"
