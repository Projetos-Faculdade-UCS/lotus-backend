from lotus.serializers.agente import (
    AgenteCoreSerializer,
    AgenteHardwareSerializer,
    AgenteProgramasSerializer,
)
from lotus.serializers.ativos_ti import (
    AtivoTIBaseSerializer,
    ComputadorDetailSerializer,
    ComputadorListSerializer,
    ImpressoraListSerializer,
    MonitorListSerializer,
)
from lotus.serializers.computador_relations import (
    LicencaSoftwareSerializer,
    ProgramaSerializer,
)
from lotus.serializers.locais import BlocoSerializer, SalaSerializer

__all__ = [
    "AgenteCoreSerializer",
    "AgenteHardwareSerializer",
    "AgenteProgramasSerializer",
    "AgenteSoftwareSerializer",
    "AtivoTIBaseSerializer",
    "BlocoSerializer",
    "ComputadorDetailSerializer",
    "ComputadorListSerializer",
    "ImpressoraDetailSerializer",
    "ImpressoraListSerializer",
    "LicencaSoftwareSerializer",
    "MonitorListSerializer",
    "ProgramaSerializer",
    "SalaSerializer",
]
