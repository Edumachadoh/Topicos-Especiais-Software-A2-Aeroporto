from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class Categoria(db.Model):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(255))

    produtos: Mapped[list["Produto"]] = relationship(
        back_populates="categoria",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Categoria {self.nome}>"
