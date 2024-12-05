from django.db import models


class Sala(models.Model):
    """Modelo de sala."""

    nome = models.CharField(max_length=100)
    bloco = models.ForeignKey("Bloco", on_delete=models.CASCADE)

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Sala"
        verbose_name_plural = "Salas"

    def __str__(self) -> str:
        """Retorna o nome da sala."""
        return f"Sala {self.nome} - Bloco {self.bloco.nome}"


class Bloco(models.Model):
    """Modelo de bloco."""

    nome = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    campus = models.CharField(max_length=100)

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Bloco"
        verbose_name_plural = "Blocos"

    def __str__(self) -> str:
        """Retorna o nome do bloco."""
        return self.nome


class Movimentacao(models.Model):
    """Representa uma movimentação de local de um ativo de TI qualquer.

    A movimentação é registrada toda vez que a FK local em um objeto ativo_ti é
    alterada. (Processo ocorre em signals.py)
    """

    sala_atual = models.ForeignKey(
        Sala,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    movimentacao_anterior = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    data = models.DateTimeField(
        auto_now_add=True,
    )
    motivo = models.CharField(
        max_length=100,
    )

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Movimentação"
        verbose_name_plural = "Movimentações"

    def __str__(self) -> str:
        """Retorna a representação da movimentação."""
        return f"Mov para {self.sala_atual} em {self.data_formatada}"

    @property
    def data_formatada(self) -> str:
        """Retorna a data formatada."""
        return self.data.strftime("%d/%m/%Y")

    @classmethod
    def get_movimentacoes(cls, movimentacao: models.Model) -> models.QuerySet:
        """Retorna uma lista de movimentações de um ativo.

        Retorna do mais recente para o mais antigo.
        """
        if not movimentacao:
            return []

        if movimentacao.movimentacao_anterior:
            return [
                movimentacao,
                *cls.get_movimentacoes(movimentacao.movimentacao_anterior),
            ]

        return [movimentacao]
