from django.db import models

from lotus.models.ativos_ti import Computador


class LicencaSoftware(models.Model):
    """Modelo de licença de software."""

    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    quantidade_em_uso = models.IntegerField()
    data_expiracao = models.DateField()
    descricao = models.TextField()
    computador = models.ForeignKey(Computador, on_delete=models.CASCADE)

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Licença de Software"
        verbose_name_plural = "Licenças de Software"

    def __str__(self) -> str:
        """Retorna o nome da licença."""
        return self.nome


class Programa(models.Model):
    """Modelo de programa."""

    nome = models.CharField(max_length=256)
    versao = models.CharField(max_length=100)
    computador = models.ForeignKey(Computador, on_delete=models.CASCADE)

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Programa"
        verbose_name_plural = "Programas"

    def __str__(self) -> str:
        """Retorna o nome do programa."""
        return self.nome
