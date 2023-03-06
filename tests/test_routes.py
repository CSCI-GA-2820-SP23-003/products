"""
Test Products API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from datetime import date, datetime, timedelta
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, init_db, Product
from service.common import status  # HTTP Status Codes
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)
BASE_URL = "/products"


######################################################################
#  T E S T   C A S E S
######################################################################


class TestProductsServer(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code, status.HTTP_201_CREATED, "Could not create test product"
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products
        
    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_product(self):
        """It should Get a single Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_get_product_not_found(self):
        """It should not Get a Product thats not found"""
        response = self.client.get(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_update_product(self):
        """It should Update a Product"""
        # get the id of a product
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Update the product
        test_product = response.get_json()
        test_product_price = test_product["price"]
        logging.debug(test_product)
        new_price = test_product_price * 2
        test_product["name"] = "Tomato"
        test_product["category"] = "Vegetable"
        test_product["price"] = new_price
        response = self.client.put(f"{BASE_URL}/{test_product['id']}", json=test_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        
        self.assertEqual(updated_product["id"], test_product["id"])
        self.assertEqual(updated_product["name"], "Tomato")
        self.assertEqual(updated_product["desc"], test_product["desc"])
        self.assertEqual(updated_product["price"], new_price)
        self.assertEqual(updated_product["category"], "Vegetable")
        self.assertEqual(updated_product["inventory"], test_product["inventory"])
        self.assertEqual(updated_product["discount"], test_product["discount"])
        self.assertEqual(updated_product["created_date"], test_product["created_date"])
        self.assertEqual(updated_product["modified_date"], test_product["modified_date"])
        self.assertEqual(updated_product["deleted_date"], test_product["deleted_date"])
    
    def test_update_product_not_found(self):
        """It should not Update a Product thats not found"""
        test_product = ProductFactory()
        response = self.client.put(f"{BASE_URL}/{test_product.id}", json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])
        # self.assertEqual(data["message"], "Product with id %s was not found", test_product.id)
                        
    def test_create_product(self):
        """It should Create a new Product"""
        test_product = ProductFactory()
        logging.debug("Test Product: %s", test_product.serialize())
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Make sure location header is set
        location = response.headers.get("Location", None)
        self.assertIsNotNone(location)

        # Check the data is correct
        new_product = response.get_json()
        self.assertNotEqual(new_product["id"], None)
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["desc"], test_product.desc)
        self.assertEqual(new_product["price"], test_product.price)
        self.assertEqual(new_product["category"], test_product.category)
        self.assertEqual(new_product["inventory"], test_product.inventory)
        self.assertEqual(new_product["discount"], test_product.discount)

        # Check that the location header was correct
        response = self.client.get(location)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        new_product = response.get_json()
        self.assertNotEqual(new_product["id"], None)
        self.assertEqual(new_product["name"], test_product.name)
        self.assertEqual(new_product["desc"], test_product.desc)
        self.assertEqual(new_product["price"], test_product.price)
        self.assertEqual(new_product["category"], test_product.category)
        self.assertEqual(new_product["inventory"], test_product.inventory)
        self.assertEqual(new_product["discount"], test_product.discount)

    def test_create_product_negative_price(self):
        """ It should identify the price is invalid if price is negative """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = float(-5)
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_type_int(self):
        """ It should identify the price is invalid if price is not type float """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = 19
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_price_type_string(self):
        """ It should identify the price is invalid if price is not digit """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = "s"
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_product_date(self):
        """ It should identify the created_date/ deleted_date is invalid if created_date is greater than deleted_date """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.created_date = test_product.deleted_date + timedelta(days=4)
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_data(self):
        """ It should not Create a Product with missing data """
        response = self.client.post(BASE_URL, json = {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """ It should not Create a Product with no content type """
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

