from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StockConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.stock'
    verbose_name = _('Stock')

    # noinspection PyUnresolvedReferences
    def ready(self):
        import apps.stock.signals
