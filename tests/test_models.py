"""
Test cases for Product Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_products.py:TestProductModel

"""
import os
import logging
import unittest
from datetime import date
from werkzeug.exceptions import NotFound
from service.models import Product, DataValidationError, db
from service import app
from tests.factories import ProductFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)

######################################################################
#  P R O D U C T   M O D E L   T E S T   C A S E S
######################################################################


class TestProductModel(unittest.TestCase):
    """ Test Cases for ProductModel Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.session.query(Product).delete()  # clean up the last tests
        db.session.commit()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_a_product(self):
        """It should Create a product and assert that it exists"""
        product = Product(name="Cheese", price=6.5, category="dairy", inventory=5, created_date=date.today())
        self.assertEqual(str(product), "<Product Cheese id=[None]>")
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        self.assertEqual(product.name, "Cheese")
        self.assertEqual(product.price, 6.5)
        self.assertEqual(product.category, "dairy")
        self.assertEqual(product.inventory, 5)
        self.assertEqual(product.created_date, date.today())
        product = Product(name="Cheese", desc="This is more popular", price=7.5,
                          category="dairy", inventory=10, created_date=date.today())
        self.assertEqual(product.desc, "This is more popular")
        self.assertEqual(product.price, 7.5)
        self.assertEqual(product.inventory, 10)

    def test_add_a_product(self):
        """It should Create a product and add it to the database"""
        products = Product.all()
        self.assertEqual(products, [])
        product = Product(name="Cheese", price=6.5, category="dairy", inventory=5, created_date=date.today())
        self.assertTrue(product is not None)
        self.assertEqual(product.id, None)
        product.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertIsNotNone(product.id)
        products = Product.all()
        self.assertEqual(len(products), 1)

    def test_read_a_product(self):
        """It should Read a Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        self.assertIsNotNone(product.id)
        # Fetch it back
        found_product = Product.find(product.id)
        self.assertEqual(found_product.id, product.id)
        self.assertEqual(found_product.name, product.name)
        self.assertEqual(found_product.desc, product.desc)
        self.assertEqual(found_product.price, product.price)
        self.assertEqual(found_product.category, product.category)
        self.assertEqual(found_product.inventory, product.inventory)
        self.assertEqual(found_product.discount, product.discount)
        self.assertEqual(found_product.created_date, product.created_date)

    def test_update_a_product(self):
        """It should Update an existing Product"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        product.create()
        logging.debug(product)
        self.assertIsNotNone(product.id)
        # Change it an save it
        product.price = 8
        original_id = product.id
        product.update()
        self.assertEqual(product.id, original_id)
        self.assertEqual(product.price, 8)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        products = Product.all()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].id, original_id)
        self.assertEqual(products[0].price, 8)

    def test_update_no_id(self):
        """It should not Update a Product with no id"""
        product = ProductFactory()
        logging.debug(product)
        product.id = None
        self.assertRaises(DataValidationError, product.update)

    def test_delete_a_product(self):
        """It should Delete a Product"""
        product = ProductFactory()
        product.create()
        self.assertEqual(len(Product.all()), 1)
        # delete the product and make sure it isn't in the database
        product.delete()
        self.assertEqual(len(Product.all()), 0)

    def test_list_all_products(self):
        """It should List all Products in the database"""
        products = Product.all()
        self.assertEqual(products, [])
        # Create 5 Products
        for _ in range(5):
            product = ProductFactory()
            product.create()
        # See if we get back 5 products
        products = Product.all()
        self.assertEqual(len(products), 5)

    def test_serialize_a_product(self):
        """It should serialize a Product"""
        product = ProductFactory()
        data = product.serialize()
        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], product.id)
        self.assertIn("name", data)
        self.assertEqual(data["name"], product.name)
        self.assertIn("desc", data)
        self.assertEqual(data["desc"], product.desc)
        self.assertIn("price", data)
        self.assertEqual(data["price"], product.price)
        self.assertIn("category", data)
        self.assertEqual(data["category"], product.category)
        self.assertIn("inventory", data)
        self.assertEqual(data["inventory"], product.inventory)
        self.assertIn("discount", data)
        self.assertEqual(data["discount"], product.discount)
        self.assertIn("created_date", data)
        self.assertEqual(date.fromisoformat(data["created_date"]), product.created_date)
        self.assertIn("modified_date", data)
        self.assertEqual(date.fromisoformat(data["modified_date"]), product.modified_date)
        self.assertIn("deleted_date", data)
        self.assertEqual(date.fromisoformat(data["deleted_date"]), product.deleted_date)

    def test_deserialize_a_product(self):
        """It should de-serialize a Product"""
        data = ProductFactory().serialize()
        product = Product()
        product.deserialize(data)
        self.assertNotEqual(product, None)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.desc, data["desc"])
        self.assertEqual(product.price, data["price"])
        self.assertEqual(product.category, data["category"])
        self.assertEqual(product.inventory, data["inventory"])
        self.assertEqual(product.discount, data["discount"])
        self.assertEqual(product.created_date, date.fromisoformat(data["created_date"]))
        self.assertEqual(product.modified_date, date.fromisoformat(data["modified_date"]))
        self.assertEqual(product.deleted_date, date.fromisoformat(data["deleted_date"]))

    def test_deserialize_missing_data(self):
        """It should not deserialize a Product with missing data"""
        data = {"id": 1, "name": "Tea", "category": "cat"}
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_deserialize_bad_data(self):
        """It should not deserialize bad data"""
        data = "this is not a dictionary"
        product = Product()
        self.assertRaises(DataValidationError, product.deserialize, data)

    def test_find_product(self):
        """It should Find a Product by ID"""
        products = ProductFactory.create_batch(5)
        for product in products:
            product.create()
        logging.debug(products)
        # make sure they got saved
        self.assertEqual(len(Product.all()), 5)
        # find the 2nd product in the list
        product = Product.find(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.desc, products[1].desc)
        self.assertEqual(product.price, products[1].price)
        self.assertEqual(product.category, products[1].category)
        self.assertEqual(product.inventory, products[1].inventory)
        self.assertEqual(product.discount, products[1].discount)
        self.assertEqual(product.created_date, products[1].created_date)

    def test_find_by_category(self):
        """It should Find Products by Category"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        category = products[0].category
        count = len([product for product in products if product.category == category])
        found = Product.find_by_category(category)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.category, category)

    def test_find_by_name(self):
        """It should Find a Product by Name"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        name = products[0].name
        count = len([product for product in products if product.name == name])
        found = Product.find_by_name(name)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.name, name)

    def test_find_by_price(self):
        """It should Find Products by Price"""
        products = ProductFactory.create_batch(10)
        for product in products:
            product.create()
        price = products[0].price
        count = len([product for product in products if product.price == price])
        found = Product.find_by_price(price)
        self.assertEqual(found.count(), count)
        for product in found:
            self.assertEqual(product.price, price)

    def _test_find_or_404_found(self):
        """It should Find or return 404 not found"""
        products = ProductFactory.create_batch(3)
        for product in products:
            product.create()

        product = Product.find_or_404(products[1].id)
        self.assertIsNot(product, None)
        self.assertEqual(product.id, products[1].id)
        self.assertEqual(product.name, products[1].name)
        self.assertEqual(product.desc, products[1].desc)
        self.assertEqual(product.price, products[1].price)
        self.assertEqual(product.category, products[1].category)
        self.assertEqual(product.inventory, products[1].inventory)
        self.assertEqual(product.discount, products[1].discount)
        self.assertEqual(product.created_date, products[1].created_date)

    def _test_find_or_404_not_found(self):
        """It should return 404 not found"""
        self.assertRaises(NotFound, Product.find_or_404, 0)

    def test_find_operation(self):
        """It should test all the function related to find 404"""

        self._test_find_or_404_found()
        self._test_find_or_404_not_found()
