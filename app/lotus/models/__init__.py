from lotus.models.ativos_ti import AtivoTI, Computador, Impressora, Monitor
from lotus.models.computador_relations import LicencaSoftware, Programa
from lotus.models.locais import Bloco, Sala
from lotus.models.proxys import ComputadorAllProxy, ComputadorCompletosProxy

__all__ = [
    "AtivoTI",
    "Bloco",
    "Computador",
    "ComputadorAllProxy",
    "ComputadorCompletosProxy",
    "Impressora",
    "LicencaSoftware",
    "Monitor",
    "Programa",
    "Sala",
]
