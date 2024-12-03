from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from lotus.models import Computador, Movimentacao


@receiver(pre_save, sender=Computador)
def handle_ativo_ti_local_change(
    sender: Computador,
    instance: Computador,
    **kwargs: dict,
) -> None:
    """Signal que é ativado quando o AtivoTI está prestes a ser salvo.

    Verifica se o campo 'local' foi alterado e cria uma Movimentacao se
    necessário.
    """
    if instance.pk:
        try:
            old_instance = Computador.objects.get(pk=instance.pk)
            if old_instance.local != instance.local:
                movimentacao = Movimentacao.objects.create(
                    sala_atual=instance.local,
                    movimentacao_anterior=instance.ultima_movimentacao,
                    motivo=get_motivo(instance, old_instance),
                )
                instance.ultima_movimentacao = movimentacao

        except sender.DoesNotExist:
            # caso o objeto tenha pk mas não exista no banco
            cria_primeira_movimentacao(instance)
    else:
        cria_primeira_movimentacao(instance)


def cria_primeira_movimentacao(instance: Computador) -> None:
    """Cria a primeira movimentação de um ativo de TI."""
    primeira_movimentacao = Movimentacao.objects.create(
        sala_atual=instance.local,
        motivo="Cadastro inicial",
    )
    instance.ultima_movimentacao = primeira_movimentacao


def get_motivo(instance: Computador, old_instance: Computador) -> None:
    """Obtém o motivo da movimentação."""
    if instance.local is None:
        motivo = "Remoção de local"
    elif old_instance.local is None:
        motivo = "Atribuição de local"
    else:
        motivo = "Mudança de local"
    return motivo
