"""Reexporta os modelos.

Importar este pacote na factory garante que todas as classes estejam
registradas no metadata antes de o Flask-Migrate comparar com o banco.
"""

from app.models.voo import Voo
from app.models.aeronave import Aeronave
from app.models.passageiro import Passageiro
from app.models.passagem import Passagem

__all__ = ["Voo", "Aeronave", "Passageiro", "Passagem"]
