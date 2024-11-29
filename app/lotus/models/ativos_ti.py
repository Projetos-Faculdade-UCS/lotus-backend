from django.db import models

from lotus.models.locais import Sala

# Create your models here.
CHOICES_TIPO_ATIVO = (
    ("computador", "Computador"),
    ("impressora", "Impressora"),
    ("monitor", "Monitor"),
)

CHOICES_CRITICIDADE_DADOS = (
    ("alta", "Alta Prioridade"),
    ("media", "Média Prioridade"),
    ("baixa", "Baixa Prioridade"),
)


class ComputadorQuerySet(models.QuerySet):
    """QuerySet customizado para o modelo Computador."""

    def validos(self) -> models.QuerySet:
        """Retorna os computadores com todos os campos preenchidos."""
        return self.filter(
            valido=True,
        )


class AllComputadoresManager(models.Manager):
    """Manager customizado para o modelo Computador."""

    def get_queryset(self) -> models.QuerySet:
        """Retorna o queryset customizado."""
        return ComputadorQuerySet(self.model, using=self._db)


class ComputadoresValidosManager(models.Manager):
    """Manager customizado para o modelo Computador."""

    def get_queryset(self) -> models.QuerySet:
        """Retorna o queryset customizado."""
        return ComputadorQuerySet(self.model, using=self._db).validos()


class AtivoTI(models.Model):
    """Modelo genérico de ativo de TI."""

    tipo = models.CharField(
        max_length=50,
        choices=CHOICES_TIPO_ATIVO,
        default="computador",
    )
    patrimonio = models.IntegerField(unique=True)
    nome = models.CharField(max_length=100, blank=True)
    fabricante = models.CharField(max_length=100, blank=True)
    numero_serie = models.CharField(max_length=50, blank=True)
    em_uso = models.BooleanField(default=False)
    descricao = models.TextField(blank=True)
    automatico = models.BooleanField(default=True)
    local = models.ForeignKey(Sala, on_delete=models.SET_NULL, blank=True, null=True)
    ativos_relacionados = models.ManyToManyField("self", blank=True)
    responsavel = models.CharField(max_length=100, blank=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta informações do modelo."""

        abstract = True

    def __str__(self) -> str:
        """Retorna o nome do ativo."""
        return f"{self.nome} - {self.patrimonio}"


class Computador(AtivoTI):
    """Modelo de computador."""

    tamanho_ram = models.CharField(max_length=100, blank=True)
    tamanho_hd = models.CharField(max_length=100, blank=True)
    modelo_cpu = models.CharField(max_length=100, blank=True)
    ultimo_usuario_logado = models.CharField(max_length=100, blank=True)
    valido = models.BooleanField(default=False)
    sistema_operacional = models.CharField(max_length=100, blank=True)
    placa_mae = models.CharField(max_length=100, blank=True)
    criticidade_dados = models.CharField(
        max_length=50,
        choices=CHOICES_CRITICIDADE_DADOS,
        default="baixa",
    )

    objects = AllComputadoresManager()
    validos = ComputadoresValidosManager()

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Computador"
        verbose_name_plural = "Computadores"

    def __str__(self) -> str:
        """Retorna o nome do computador."""
        return f"{self.nome} - {self.patrimonio}"


class Impressora(AtivoTI):
    """Modelo de impressora."""

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Impressora"
        verbose_name_plural = "Impressoras"

    def __str__(self) -> str:
        """Retorna o nome da impressora."""
        return f"{self.nome} - {self.patrimonio}"


class Monitor(AtivoTI):
    """Modelo de monitor."""

    resolucao = models.CharField(max_length=100)

    class Meta:
        """Meta informações do modelo."""

        verbose_name = "Monitor"
        verbose_name_plural = "Monitores"

    def __str__(self) -> str:
        """Retorna o nome do monitor."""
        return f"{self.nome} - {self.patrimonio}"
