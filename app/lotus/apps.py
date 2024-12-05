from django.apps import AppConfig


class LotusConfig(AppConfig):
    """Configuração da aplicação lotus."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "lotus"

    def ready(self) -> None:
        """Importa signals."""
        import lotus.signals

        return super().ready()
