from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from lotus.views import (
    AgenteApiView,
    BlocosViewSet,
    ComputadoresViewSet,
    DashboardViewSet,
    ImpressorasViewSet,
    MonitorViewSet,
    SalaViewSet,
)

router = DefaultRouter()
router.register(r"computadores", ComputadoresViewSet, basename="computadores")
router.register(r"impressoras", ImpressorasViewSet, basename="impressoras")
router.register(r"monitores", MonitorViewSet, basename="monitores")
router.register(r"salas", SalaViewSet, basename="salas")
router.register(r"blocos", BlocosViewSet, basename="blocos")
router.register(r"dashboard", DashboardViewSet, basename="dashboard")

urlpatterns = [
    path("", include(router.urls)),
    path(
        r"blocos/<int:bloco_id>/salas/",
        SalaViewSet.as_view({"get": "salas_in_bloco"}),
    ),
    path(
        r"blocos/<int:_bloco_id>/salas/<int:sala_id>/computadores/",
        ComputadoresViewSet.as_view({"get": "computadores_in_sala"}),
    ),
    path(r"agente/<str:tipo>/", AgenteApiView.as_view(), name="agente"),
    path(
        r"computadores/<int:computador_id>/ativos-relacionados/",
        ComputadoresViewSet.as_view({"get": "ativos_relacionados"}),
    ),
]
