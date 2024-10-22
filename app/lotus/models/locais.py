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
        return f"{self.nome} - {self.bloco.nome}"


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
