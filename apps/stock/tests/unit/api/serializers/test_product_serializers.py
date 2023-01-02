from django.test import TestCase
from uuid import UUID

from apps.stock.api.serializers import ProductSerializer
from apps.stock.models import Product
from ....mocks import MockStockFactory


class ProductSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = MockStockFactory()

    def test_serialized_data(self):
        """ Tests when outcome from model's instance as serialized data. """
        instance = self.factory.fake_product()
        serializer = ProductSerializer(instance=instance)
        data = serializer.data

        for field, value in instance.get_values().items():
            value = str(value) if isinstance(value, UUID) else value
            self.assertIn(field, data)
            self.assertEqual(data[field], value)

        self.assertEqual(str(instance.category_id), data['category']['pk'])

    def test_serialized_collection(self):
        """ Tests when outcome from model's instances as serialized data. """
        instances = [
            self.factory.fake_product(persist=True),
            self.factory.fake_product(persist=True),
            self.factory.fake_product(persist=True),
            self.factory.fake_product(persist=True),
            self.factory.fake_product(persist=True),
        ]

        serializer = ProductSerializer(instance=instances, many=True)
        pks = set([i['pk'] for i in serializer.data])

        for instance in instances:
            self.assertIn(str(instance.pk), pks)

    def test_create(self):
        """ Tests instance creation from serializer """
        data = self.factory.fake_product_data()

        category = self.factory.fake_category(persist=True)
        data.update({'category': str(category.pk)})

        serializer = ProductSerializer(data=data)

        self.assertEqual(serializer.is_valid(), True)

        serializer.save()

        for k, v in serializer.validated_data.items():
            if k == 'category':
                v = str(v.pk)
            self.assertIn(k, data)
            self.assertEqual(data[k], v)

    def test_full_update(self):
        """ Tests instance full update from serializer """
        category = self.factory.fake_category(persist=True)
        instance = self.factory.fake_product(active=True, persist=True)

        data = instance.get_values()
        data.update({'category': str(instance.category_id)})

        serializer = ProductSerializer(instance=instance, data=data)
        self.assertEqual(serializer.is_valid(), True)

        edited_data = {
            'name': f'{instance.name}-updated-123',
            'active': False,
            'category': str(category.pk),
        }
        data.update(edited_data)

        # full edition as data is passed to data and partial is False
        serializer = ProductSerializer(instance=instance, data=data, partial=False)

        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        saved_instance = Product.objects.get(pk=instance.pk)

        self.assertEqual(data['name'], saved_instance.name)
        self.assertEqual(data['active'], saved_instance.active)
        self.assertEqual(data['category'], str(saved_instance.category_id))

    def test_partial_update(self):
        """ Tests instance partial update from serializer """
        instance = self.factory.fake_product(active=True, persist=True)

        data = instance.get_values()
        data.update({'category': str(instance.category_id)})

        serializer = ProductSerializer(instance=instance, data=data)
        self.assertEqual(serializer.is_valid(), True)

        # Edit only partial fields
        partial_edited_data = {
            'name': f'{instance.name}-updated-123',
        }

        # full edition as data is passed to data and partial is None
        serializer = ProductSerializer(instance=instance, data=partial_edited_data, partial=True)

        self.assertEqual(serializer.is_valid(), True)
        serializer.save()

        saved_instance = Product.objects.get(pk=instance.pk)

        self.assertEqual(partial_edited_data['name'], saved_instance.name)
