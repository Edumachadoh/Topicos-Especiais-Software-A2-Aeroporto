from __future__ import annotations

from sqlalchemy import String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db

voo_passageiro = db.Table('voo_passageiro',
    db.Column('voo_id', db.String(36), db.ForeignKey('voos.id'), primary_key=True),
    db.Column('passageiro_id', db.String(36), db.ForeignKey('passageiros.id'), primary_key=True)
)

class Voo(db.Model):
    __tablename__ = "voos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    
    # Chave estrangeira explícita (Relacionamento N:1 com Aeronave)
    aeronave_id: Mapped[str] = mapped_column(ForeignKey("aeronaves.id"), nullable=False)

    aeronave: Mapped["Aeronave"] = relationship(back_populates="voos")
    
    passageiros: Mapped[list["Passageiro"]] = relationship(
        secondary=voo_passageiro,
        back_populates="voos",
    )

    def __repr__(self) -> str:
        return f"<Voo {self.id}>"