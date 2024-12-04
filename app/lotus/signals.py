from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from lotus.models import AtivoTI, Computador, Impressora, Monitor, Movimentacao


@receiver(pre_save, sender=Computador)
def handle_computador_local_change(
    sender: Computador,
    instance: Computador,
    **_: dict,
) -> None:
    """Signal que é ativado quando o AtivoTI está prestes a ser salvo.

    Verifica se o campo 'local' foi alterado e cria uma Movimentacao se
    necessário.
    """
    if instance.pk:
        try:
            old_instance = Computador.objects.get(pk=instance.pk)
            if old_instance.local != instance.local:
                cria_movimentacao(instance, old_instance)
        except sender.DoesNotExist:
            # caso o objeto tenha pk mas não exista no banco
            cria_primeira_movimentacao(instance)
    else:
        cria_primeira_movimentacao(instance)


@receiver(pre_save, sender=Monitor)
def handle_monitor_local_change(
    sender: Monitor,
    instance: Monitor,
    **_: dict,
) -> None:
    """Signal que é ativado quando o AtivoTI está prestes a ser salvo.

    Verifica se o campo 'local' foi alterado e cria uma Movimentacao se
    necessário.
    """
    if instance.pk:
        try:
            old_instance = Monitor.objects.get(pk=instance.pk)
            if old_instance.local != instance.local:
                cria_movimentacao(instance, old_instance)
        except sender.DoesNotExist:
            # caso o objeto tenha pk mas não exista no banco
            cria_primeira_movimentacao(instance)
    else:
        cria_primeira_movimentacao(instance)


@receiver(pre_save, sender=Impressora)
def handle_impressora_local_change(
    sender: Impressora,
    instance: Impressora,
    **_: dict,
) -> None:
    """Signal que é ativado quando o AtivoTI está prestes a ser salvo.

    Verifica se o campo 'local' foi alterado e cria uma Movimentacao se
    necessário.
    """
    if instance.pk:
        try:
            old_instance = Impressora.objects.get(pk=instance.pk)
            if old_instance.local != instance.local:
                cria_movimentacao(instance, old_instance)
        except sender.DoesNotExist:
            # caso o objeto tenha pk mas não exista no banco
            cria_primeira_movimentacao(instance)
    else:
        cria_primeira_movimentacao(instance)


def cria_movimentacao(instance: AtivoTI, old_instance: AtivoTI) -> None:
    """Cria a movimentação seguinte."""
    movimentacao = Movimentacao.objects.create(
        sala_atual=instance.local,
        movimentacao_anterior=instance.ultima_movimentacao,
        motivo=get_motivo(instance, old_instance),
    )
    instance.ultima_movimentacao = movimentacao


def cria_primeira_movimentacao(instance: AtivoTI) -> None:
    """Cria a primeira movimentação de um ativo de TI."""
    primeira_movimentacao = Movimentacao.objects.create(
        sala_atual=instance.local,
        motivo="Cadastro inicial",
    )
    instance.ultima_movimentacao = primeira_movimentacao


def get_motivo(instance: AtivoTI, old_instance: AtivoTI) -> None:
    """Obtém o motivo da movimentação."""
    if instance.local is None:
        motivo = "Remoção de local"
    elif old_instance.local is None:
        motivo = "Atribuição de local"
    else:
        motivo = "Mudança de local"
    return motivo
