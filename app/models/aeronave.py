from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Aeronave(db.Model):
    __tablename__ = "aeronaves"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    capacidade_assentos: Mapped[int] = mapped_column(nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)

    voos: Mapped[list["Voo"]] = relationship(
        back_populates="aeronave",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Aeronave {self.modelo}>"