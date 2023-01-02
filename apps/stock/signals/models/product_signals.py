from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.stock.models import Product


@receiver(pre_save, sender=Product)
def pre_save_handler(instance: Product, raw: bool, **kwargs) -> None:
    if raw is True:
        print(f'Pre save signal for {instance.__class__.__name__} - ignored in fixtures entries')
        return

    print(f'This is a signal for pre-save dispatch for {instance.__class__.__name__}')


@receiver(post_save, sender=Product)
def post_save_handler(instance: Product, raw: bool, **kwargs) -> None:
    if raw is True:
        print(f'Post save signal for {instance.__class__.__name__} - ignored in fixtures entries')
        return

    print(f'This is a signal for post-save dispatch for {instance.__class__.__name__}')
