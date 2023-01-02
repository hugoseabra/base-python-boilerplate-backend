import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins


class Product(mixins.UUIDPkMixin,
              mixins.ActivableMixin,
              mixins.DateTimeManagementMixin,
              mixins.EntityMixin,
              mixins.DomainRuleMixin,
              mixins.DeletableModelMixin,
              models.Model):
    """
    Product to be stored in stock
    """

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        ordering = ['category_id', 'name']

    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
        help_text=_('Provide a name for the product'),
        null=False,
        blank=False,
    )

    category = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        verbose_name=_('Category'),
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name
