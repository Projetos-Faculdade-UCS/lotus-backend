from django.urls import include, path
from rest_framework.routers import DefaultRouter

from lotus.views import ComputadoresViewSet, ImpressorasViewSet

router = DefaultRouter()
router.register(r"computadores", ComputadoresViewSet, basename="computadores")
router.register(r"impressoras", ImpressorasViewSet, basename="impressoras")

urlpatterns = [
    path("", include(router.urls)),
]
