from random import choice
from typing import Dict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.stock.api.serializers import SimpleCategorySerializer, ProductSerializer
from apps.stock.models import Product
from apps.stock.tests.mocks import MockStockFactory

mock_factory = MockStockFactory()


class ProductAPIEndpointsTestCase(APITestCase):
    def _create_product_data(self) -> dict:
        data = mock_factory.fake_product_data()
        category = mock_factory.fake_category(persist=True)
        data['category'] = SimpleCategorySerializer(instance=category).data
        return data

    def _create_product(self, **kwargs) -> Product:
        return mock_factory.fake_product(**kwargs)

    def _create_collection(self, num: int = 1, **kwargs) -> Dict[str, Product]:
        instances = [self._create_product(**kwargs) for _ in range(num)]
        return {str(i.pk): i for i in instances}

    def test_retrieval_item(self):
        """ Tests retrieval of a record """
        instance = self._create_product(persist=True, active=True)

        endpoint = reverse('stock:product-detail', kwargs={'pk': str(instance.pk)})
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertIsNotNone(result)

        self.assertEqual(instance.name, result.get('name'))
        self.assertEqual(instance.active, result.get('active'))
        self.assertEqual(str(instance.category_id), result.get('category', {}).get('pk'))
        self.assertIsNotNone(result.get('created_at'))
        self.assertIsNotNone(result.get('updated_at'))

    def test_retrieval_collection(self):
        """ Tests retrieval of many records paginated """
        instances = self._create_collection(num=20, persist=True)

        endpoint = reverse('stock:product-list')
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()

        self.assertEqual(resp_data['count'], len(instances.keys()))
        results = resp_data['results']

        for item in results:
            pk = item['pk']
            instance = instances.get(pk)
            print(instance)

            self.assertEqual(str(instance.pk), item['pk'])
            self.assertEqual(instance.name, item['name'])
            self.assertEqual(instance.active, item['active'])
            self.assertEqual(str(instance.category_id), item['category']['pk'])
            self.assertIsNotNone(item['created_at'])
            self.assertIsNotNone(item['updated_at'])

    def test_creation(self):
        """ Tests creation of a record """
        data = self._create_product_data()

        endpoint = reverse('stock:product-list')

        response = self.client.post(endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_data = response.json()

        self.assertIsNotNone(resp_data['pk'])
        self.assertEqual(data['name'], resp_data['name'])
        self.assertEqual(data['active'], resp_data['active'])
        self.assertEqual(data['category']['pk'], resp_data['category']['pk'])
        self.assertIsNotNone(resp_data['created_at'])
        self.assertIsNotNone(resp_data['updated_at'])

    def test_full_update(self):
        """ Tests full update of a record """

        instance = self._create_product(persist=True, active=True)

        data = ProductSerializer(instance=instance).data
        data['name'] = f"{data['name']}-edited"
        data['active'] = False

        endpoint = reverse('stock:product-detail', kwargs={'pk': str(instance.pk)})
        response = self.client.put(endpoint, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertIsNotNone(result)

        self.assertEqual(data['pk'], result['pk'])
        self.assertEqual(data['name'], result['name'])
        self.assertEqual(data['active'], result['active'])
        self.assertEqual(data['category']['pk'], result['category']['pk'])
        self.assertIsNotNone(result['created_at'])
        self.assertIsNotNone(result['updated_at'])

    def test_partial_update(self):
        """ Tests partial update of a record """
        instance = self._create_product(persist=True, active=True)

        data = ProductSerializer(instance=instance).data

        edited_data = {
            'name': f"{data['name']}",
            'active': False
        }

        endpoint = reverse('stock:product-detail', kwargs={'pk': str(instance.pk)})
        response = self.client.patch(endpoint, data=edited_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        self.assertIsNotNone(result)

        self.assertEqual(edited_data['name'], result['name'])
        self.assertEqual(edited_data['active'], result['active'])

    def test_deletion(self):
        """ Tests deletion of a record """
        instances = self._create_collection(num=3, persist=True)
        pks = list(instances.keys())

        pk = choice(pks)
        instance = instances.get(pk)

        endpoint = reverse('stock:product-detail', kwargs={'pk': str(instance.pk)})
        response = self.client.delete(endpoint)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        qs = Product.objects
        self.assertEqual(qs.count(), len(pks) - 1)

        retrieved_pks = [str(i) for i in qs.all()]

        self.assertNotIn(str(instance.pk), retrieved_pks)

    def test_filtering(self):
        """ Tests filtering records by fields """
        instances = list()

        # Create 3 active products with name starting with steve
        category_steve = mock_factory.fake_category(persist=True)
        for i in range(3):
            name = f'Steve {i + 1}'
            instances.append(self._create_product(
                persist=True, category=category_steve, active=True, name=name
            ))

        # Create 2 inactive products
        category_bob = mock_factory.fake_category(persist=True)
        for i in range(2):
            name = f'Bob {i + 1}'
            instances.append(self._create_product(
                persist=True, active=False, name=name, category=category_bob
            ))

        # Create 2 active products with inactive categories
        for i in range(2):
            name = f'Mart {i + 1}'
            instance = self._create_product(persist=True, active=True, name=name)
            instance.category.active = False
            instance.category.save(ignore_validation=True)
            instances.append(instance)

        endpoint = reverse('stock:product-list')

        steve_instances = list(filter(
            lambda x: x.category_id == category_steve.pk, instances
        ))

        active_instances = list(filter(lambda x: x.active is True, instances))
        inactive_instances = list(filter(lambda x: x.active is False, instances))
        with_inactive_cats = list(
            filter(lambda x: x.category.active is False, instances))

        # Filter by active field
        response = self.client.get(f'{endpoint}?active=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data['count'], len(active_instances))

        pks = [str(i.pk) for i in active_instances]
        for item in resp_data['results']:
            self.assertIn(item['pk'], pks)

        response = self.client.get(f'{endpoint}?active=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data['count'], len(inactive_instances))

        pks = [str(i.pk) for i in inactive_instances]
        for item in resp_data['results']:
            self.assertIn(item['pk'], pks)

        # Filter by name
        # @TODO

        # Filter category id
        response = self.client.get(f'{endpoint}?category={category_steve.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data['count'], len(steve_instances))

        pks = [str(i.pk) for i in steve_instances]
        for item in resp_data['results']:
            self.assertIn(item['pk'], pks)

        # Filter by category active field
        response = self.client.get(f'{endpoint}?category__active=false')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()
        self.assertEqual(resp_data['count'], len(with_inactive_cats))

        pks = [str(i.pk) for i in with_inactive_cats]
        for item in resp_data['results']:
            self.assertIn(item['pk'], pks)

    def test_creation_with_category_pk_and_object_support(self):
        """
        Tests tests supports to related category to product using primary key or object
        in payload.
        """
        endpoint = reverse('stock:product-list')
        category = mock_factory.fake_category(persist=True)
        data = self._create_product_data()

        data['category'] = str(category.pk)
        response = self.client.post(endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_data = response.json()
        self.assertEqual(data['category'], resp_data['category']['pk'])

        data['category'] = {
            'pk': str(category.pk)
        }
        response = self.client.post(endpoint, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp_data = response.json()
        self.assertEqual(data['category']['pk'], resp_data['category']['pk'])

    def test_category_output_simple_way(self):
        """ Tests category output as object with main fields (simple way). """
        instance = self._create_product(persist=True, active=True)

        endpoint = reverse('stock:product-detail', kwargs={'pk': str(instance.pk)})
        response = self.client.get(endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()

        category_data = SimpleCategorySerializer(instance=instance.category).data
        self.assertDictEqual(category_data, result['category'])

    def test_fields_query_string_for_payload(self):
        """ Tests whether payload is returning only the fields I want. """
        self._create_collection(num=10, persist=True)

        endpoint = reverse('stock:product-list')

        field_names = ['pk', 'active']
        fields = ','.join(field_names)
        response = self.client.get(f'{endpoint}?fields={fields}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()

        for item in resp_data['results']:
            for f_name in field_names:
                self.assertIn(f_name, item.keys())

        field_names = ['name', 'category']
        fields = ','.join(field_names)
        response = self.client.get(f'{endpoint}?fields={fields}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()

        for item in resp_data['results']:
            for f_name in field_names:
                self.assertIn(f_name, item.keys())

        field_names = ['active']
        fields = ','.join(field_names)
        response = self.client.get(f'{endpoint}?fields={fields}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp_data = response.json()

        for item in resp_data['results']:
            for f_name in field_names:
                self.assertIn(f_name, item.keys())
