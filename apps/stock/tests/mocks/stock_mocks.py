"""
    Mock factory used during tests to create required gatheros event
    domain objects.
"""
from faker import Faker

from apps.stock.models import Category, Product


class MockStockFactory:
    """ Mock Factory Implementation """

    def __init__(self):
        self.fake_factory = Faker()

    def fake_category_data(self, pk=None, active=True) -> dict:
        data = {
            'name': self.fake_factory.name(),
            'active': active,
        }
        if pk:
            data.update({'pk': pk})
        return data

    def fake_product_data(self, pk=None, active=True) -> dict:
        data = {
            'name': self.fake_factory.name(),
            'active': active,
        }
        if pk:
            data.update({'pk': pk})
        return data

    def fake_category(self, persist=False, **kwargs) -> Category:
        data = self.fake_category_data(pk=kwargs.get('pk'), active=kwargs.get('active', True))
        data.update(**kwargs)
        instance = Category(**data)
        if persist:
            instance.save(ignore_validation=True)
        return instance

    def fake_product(self, persist=False, category: Category = None, **kwargs) -> Product:
        category = category or self.fake_category(**kwargs)

        data = self.fake_category_data(pk=kwargs.get('pk'), active=kwargs.get('active', True))
        data.update(**kwargs)
        instance = Product(category=category, **data)

        if persist:
            category.save(ignore_validation=True)
            instance.save(ignore_validation=True)

        return instance
