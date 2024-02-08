from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from polls.models import Address
from polls.viewsAll.v1_AddressViewSet import AddressViewSet

class AddressViewSetTest(TestCase):
    
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AddressViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})
        self.address_data = {'street': '123 Main St', 'street_number': '1', 'region_name': 'Region', 'prefecture_name': 'Prefecture', 'postal_code': '12345'}
    
    # POST METHOD
    def test_create_address(self):
       
        # Simulate POST request to create an address
        request = self.factory.post('/addresses/', self.address_data)
        response = self.view(request)
           
        # Assert response status code and address creation
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Address.objects.last().street, '123 Main St')
        
    # PUT METHOD    
    def test_update_address(self):
        address = Address.objects.create(street='456 Elm St', street_number='2', region_name='Region', prefecture_name='Prefecture', postal_code='54321')
        
        # Simulate PUT request to update the address
        updated_address_data = {'street': '789 O1ak St', 'street_number': '3', 'region_name': 'Updated Region', 'prefecture_name': 'Updated Prefecture', 'postal_code': '67890'}
        request = self.factory.put(f'/addresses/{address.id}/', updated_address_data)
        response = self.view(request, pk=address.id)
        
        # Assert response status code and address update
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        address.refresh_from_db()
        self.assertEqual(address.street, '789 O1ak St')
         
    # DELETE METHOD 
    def test_delete_address(self):
        # Create an address
        address = Address.objects.create(street='456 Elm St', street_number='2', region_name='Region', prefecture_name='Prefecture', postal_code='54321')
        
        # Simulate DELETE request to delete the address
        request = self.factory.delete(f'/addresses/{address.id}/')
        response = self.view(request, pk=address.id)
        
        # Assert response status code and address deletion
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Address.objects.filter(id=address.id).exists())
    
    # GET 1 ADDRESS 
    def test_retrieve_address(self):
        # Create an address
        address = Address.objects.create(street='456 Elm St', street_number='2', region_name='Region', prefecture_name='Prefecture', postal_code='54321')
        
        # Simulate GET request to retrieve the address
        request = self.factory.get(f'/addresses/{address.id}/')
        response = self.view(request, pk=address.id)
        
        # Assert response status code and address retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['street'], '456 Elm St')
    
    # GET ALL ADDRESS     
    def test_retrieve_all_addresses(self):
        # Create some addresses
        Address.objects.create(street='456 Elm St', street_number='2', region_name='Region', prefecture_name='Prefecture', postal_code='54321')
        Address.objects.create(street='789 Oak St', street_number='3', region_name='Region', prefecture_name='Prefecture', postal_code='67890')
        
        # Simulate GET request to retrieve all addresses
        request = self.factory.get('/addresses/')
        response = self.view(request)
        
        # Assert response status code and address retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)     