import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import mixins


class Category(mixins.UUIDPkMixin,
               mixins.ActivableMixin,
               mixins.DateTimeManagementMixin,
               mixins.EntityMixin,
               mixins.DomainRuleMixin,
               mixins.DeletableModelMixin,
               models.Model):
    """
    Stock category, for grouping products.
    """

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    name = models.CharField(
        max_length=100,
        verbose_name=_('name'),
        help_text=_('Provide a name for the category'),
    )

    def __str__(self):
        return self.name
