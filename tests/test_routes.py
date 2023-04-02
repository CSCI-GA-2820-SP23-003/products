"""
Test Products API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from datetime import timedelta
from unittest import TestCase

# from unittest.mock import MagicMock, patch
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
    """REST API Server Tests"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        self.client = app.test_client()
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()

    def _create_products(self, count):
        """Factory method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                "Could not create test product",
            )
            new_product = response.get_json()
            test_product.id = new_product["id"]
            products.append(test_product)
        return products

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """It should call the home page"""
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

    def test_create_customer_valid_id(self):
        """It should check if a Product has been created with a valid ID"""

        test_product = ProductFactory.create_batch(5)
        for prod in test_product:
            logging.debug(prod)
            prod_post_req = self.client.post(BASE_URL, json=prod.serialize())

            # Assert that the product has been created successfully
            self.assertEqual(
                prod_post_req.status_code,
                status.HTTP_201_CREATED,
                "Product did not get created",
            )

            created_product = prod_post_req.get_json()
            self.assertIsNotNone(created_product["id"], "IDs haven't been created")

    def test_create_product_negative_price(self):
        """It should identify the price is invalid if price is negative"""
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = float(-5)
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_type_int(self):
        """It should identify the price is invalid if price is not type float"""
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = 19
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_price_type_string(self):
        """It should identify the price is invalid if price is not digit"""
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.price = "s"
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_date(self):
        """It should identify the created_date/ deleted_date is invalid if created_date is greater than deleted_date"""
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.created_date = test_product.deleted_date + timedelta(days=4)
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_data(self):
        """It should not Create a Product with missing data"""
        response = self.client.post(BASE_URL, json={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_no_content_type(self):
        """It should not Create a Product with no content type"""
        response = self.client.post(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_update_product(self):
        """It should Update an existing Product"""
        # Create a product to update
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update the product
        new_product = response.get_json()
        logging.debug(new_product)
        new_product["name"] = "Tomato"
        new_product["category"] = "vegetable"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["id"], new_product["id"])
        self.assertEqual(updated_product["name"], "Tomato")
        self.assertEqual(updated_product["desc"], new_product["desc"])
        self.assertEqual(updated_product["price"], new_product["price"])
        self.assertEqual(updated_product["category"], "vegetable")

    def test_update_product_not_found(self):
        """It should not Update a Product thats not found"""
        test_product = ProductFactory()
        response = self.client.put(
            f"{BASE_URL}/{test_product.id}", json=test_product.serialize()
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_delete_product_not_found(self):
        """It should delete a Product thats not found"""
        response = self.client.delete(f"{BASE_URL}/0")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product(self):
        """It should delete a Product thats found"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_product_repeatedly(self):
        """It should delete a Product thats already deleted"""
        test_product = self._create_products(1)[0]
        N = 5
        for _ in range(N):
            response = self.client.delete(f"{BASE_URL}/{test_product.id}")
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_products(self):
        """This should list all products"""
        products = self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.get_json()), len(products))

    def test_list_products_with_name(self):
        """List all the products with a particular name"""
        products = self._create_products(5)
        name = products[0].name
        count = len([product for product in products if product.name == name])
        response = self.client.get(f"{BASE_URL}?name={name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.get_json()
        self.assertEqual(len(response_data), count)
        for product in response_data:
            self.assertEqual(product["name"], name)

    def test_list_products_with_category(self):
        """List all the products with a particular category"""
        products = self._create_products(5)
        category = products[0].category
        count = len([product for product in products if product.category == category])
        response = self.client.get(f"{BASE_URL}?category={category}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.get_json()
        self.assertEqual(len(response_data), count)
        for product in response_data:
            self.assertEqual(product["category"], category)

    def test_list_products_with_price(self):
        """List all the products with a particular price"""
        products = self._create_products(5)
        price = products[0].price
        count = len([product for product in products if product.price == price])
        response = self.client.get(f"{BASE_URL}?price={price}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.get_json()
        self.assertEqual(len(response_data), count)
        for product in response_data:
            self.assertEqual(product["price"], price)

    def test_method_not_allowed(self):
        """It should not allow an illegal method call"""
        test_product = ProductFactory()
        response = self.client.post(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        data = response.get_json()
        logging.debug("Response data = %s", data)


    ######################################################################
    #  LIKE ACTION TEST CASES
    ######################################################################


    def test_like_product(self):
        """ It should like product """
        # Create product with default value like = FALSE
        test_product = ProductFactory.create_batch(1)[0]
        prev_like_count = test_product.like
        
        # API call to like the product with given id
        response = self.client.put(f"{BASE_URL}/{test_product.id}/like")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertEqual(data["like"], prev_like_count + 1)

        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertEqual(data["like"], prev_like_count + 2)

    def test_like_product_not_found(self):
        """It should not Like a Product thats not found"""
        test_product = ProductFactory()
        response = self.client.put(
            f"{BASE_URL}/{test_product.id}/like", json=test_product.serialize()
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        data = response.get_json()
        logging.debug("Response data = %s", data)
        self.assertIn("was not found", data["message"])

    def test_create_product_string_like(self):
        """ It should identify the like is invalid if like count is a string """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.like = 'a'
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_like_negative(self):
        """ It should identify the like is invalid if like count is negative """
        test_product = ProductFactory()
        logging.debug(test_product)

        test_product.like = -5
        response = self.client.post(BASE_URL, json = test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)