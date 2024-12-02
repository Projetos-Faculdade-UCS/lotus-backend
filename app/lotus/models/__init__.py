from lotus.models.ativos_ti import AtivoTI, Computador, Impressora, Monitor
from lotus.models.computador_relations import LicencaSoftware, Programa
from lotus.models.locais import Bloco, Sala, Movimentacao
from lotus.models.proxys import ComputadorAllProxy, ComputadorValidosProxy

__all__ = [
    "AtivoTI",
    "Bloco",
    "Computador",
    "ComputadorAllProxy",
    "ComputadorValidosProxy",
    "Impressora",
    "LicencaSoftware",
    "Monitor",
    "Programa",
    "Sala",
    "Movimentacao",
]
