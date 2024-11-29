from lotus.models.ativos_ti import Computador


class ComputadorAllProxy(Computador):
    """Proxy model para todos os computadores."""

    class Meta:
        """Meta opções."""

        proxy = True
        verbose_name = "Computador"
        verbose_name_plural = "Computadores"


class ComputadorValidosProxy(Computador):
    """Proxy model para computadores validos."""

    class Meta:
        """Meta opções."""

        proxy = True
        verbose_name = "Computador Valido"
        verbose_name_plural = "Computadores Validos"
