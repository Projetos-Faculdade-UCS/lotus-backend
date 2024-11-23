from lotus.models.ativos_ti import Computador


class ComputadorAllProxy(Computador):
    """Proxy model para todos os computadores."""

    class Meta:
        """Meta opções."""

        proxy = True
        verbose_name = "Computador"
        verbose_name_plural = "Computadores"


class ComputadorCompletosProxy(Computador):
    """Proxy model para computadores completos."""

    class Meta:
        """Meta opções."""

        proxy = True
        verbose_name = "Computador Completo"
        verbose_name_plural = "Computadores Completos"
