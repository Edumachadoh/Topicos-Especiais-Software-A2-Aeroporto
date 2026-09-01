from __future__ import annotations

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Passagem(db.Model):
    __tablename__ = "passagens"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    assento: Mapped[str] = mapped_column(String(10), nullable=False)
    valor: Mapped[float] = mapped_column(nullable=False)

    voo_id: Mapped[str] = mapped_column(ForeignKey("voos.id"), nullable=False)
    passageiro_id: Mapped[str] = mapped_column(ForeignKey("passageiros.id"), nullable=False)

    voo: Mapped["Voo"] = relationship(back_populates="passagens")
    passageiro: Mapped["Passageiro"] = relationship(back_populates="passagens")

    def __repr__(self) -> str:
        return f"<Passagem {self.assento} {self.voo}>"