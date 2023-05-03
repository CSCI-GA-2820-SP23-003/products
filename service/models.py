"""
Models for Products

All of the models are stored in this module

Models
------
Product - A Product in a catalog

Attributes:
-----------
name (string) - the name of the product
desc (string) - the description of the product
price (float) - the price of the product
category (string) - the category the product belongs to (i.e., tops, shirts)
inventory (int) - the quantity of the product
discount (float) - the discount percent of the product (i.e., from 1.0 to 0.1)
like (int) - the total number of the product is liked
created_date (timestamp) - the timestamp when the product is created
modified_date (timestamp) - the timestamp when the product is modified
deleted_date (timestamp) - the timestamp when the product is deleted

"""
import logging

# from enum import Enum
from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


# Function to initialize the database
def init_db(app):
    """Initializes the SQLAlchemy app"""
    Product.init_db(app)


class DataValidationError(Exception):
    """Used for an data validation errors when deserializing"""


# pylint: disable=too-many-instance-attributes
class Product(db.Model):
    """
    Class that represents a Product
    """

    app = None

    ##################################################
    # Table Schema
    ##################################################

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(63), nullable=False)
    desc = db.Column(db.String(256))
    price = db.Column(db.Float(), nullable=False)
    category = db.Column(db.String(63), nullable=False)
    inventory = db.Column(db.Integer(), nullable=False)
    discount = db.Column(db.Float(), nullable=False, default=1)
    like = db.Column(db.Integer(), nullable=False, default=0)
    created_date = db.Column(db.Date(), nullable=False, default=date.today())
    modified_date = db.Column(db.Date())
    deleted_date = db.Column(db.Date())

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return f"<Product {self.name} id=[{self.id}]>"

    def create(self):
        """
        Creates a Product to the database
        """
        logger.info("Creating product %s", self.name)
        self.id = None  # pylint: disable=invalid-name
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Product to the database
        """
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        # if self.inventory < 0:
        #     raise DataValidationError("Update called with invalid Inventory field")
        db.session.commit()

    def delete(self):
        """Removes a Product from the data store"""
        logger.info("Deleting product %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """Serializes a Product into a dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "desc": self.desc if self.desc is not None else None,
            "price": self.price,
            "category": self.category,
            "inventory": self.inventory,
            "discount": self.discount,
            "like": self.like,
            "created_date": self.created_date.isoformat(),
            "modified_date": self.modified_date.isoformat()
            if self.modified_date is not None
            else None,
            "deleted_date": self.deleted_date.isoformat()
            if self.deleted_date is not None
            else None,
        }

    def deserialize(self, data):
        """
        Deserializes a Product from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # self.id = data["id"]
            self.name = data["name"]
            # if "desc" in data:
            self.desc = data["desc"]

            if not isinstance(data["price"], (float, int)):
                raise DataValidationError(
                    "Invalid type for number [price]: " + str(type(data["price"]))
                )
            if data["price"] < 0:
                raise DataValidationError(
                    "Invalid value for price. Price should be a non-negative value"
                )
            self.price = data["price"]

            self.category = data["category"]
            self.inventory = data["inventory"]
            self.discount = data["discount"]

            if not isinstance(data["like"], int):
                raise DataValidationError(
                    "Invalid type for int [like]: " + str(type(data["like"]))
                )
            if data["like"] < 0:
                raise DataValidationError(
                    "Invalid value for like. Like should be a non-negative value"
                )
            self.like = data["like"]

            self.created_date = date.fromisoformat(data["created_date"])
            if data["modified_date"]:
                self.modified_date = date.fromisoformat(data["modified_date"])
            if data["deleted_date"]:
                self.deleted_date = date.fromisoformat(data["deleted_date"])
        except KeyError as error:
            raise DataValidationError(
                "Invalid product: missing " + error.args[0]
            ) from error
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data - "
                "Error message: " + str(error)
            ) from error
        return self

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app: Flask):
        """Initializes the database session

        :param app: the Flask app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls) -> list:
        """Returns all of the Product in the database"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """Finds a Product by it's ID

        :param product_id: the id of the Product to find
        :type product_id: int

        :return: an instance with the product_id, or None if not found
        :rtype: Product

        """
        logger.info("Processing lookup for product id %s ...", product_id)
        return cls.query.get(product_id)

    @classmethod
    def find_or_404(cls, product_id: int):
        """Find a Product by it's id

        :param product_id: the id of the Product to find
        :type product_id: int

        :return: an instance with the product_id, or 404_NOT_FOUND if not found
        :rtype: Product

        """
        logger.info("Processing lookup or 404 for product id %s ...", product_id)
        return cls.query.get_or_404(product_id)

    @classmethod
    def find_by_name(cls, name: str) -> list:
        """Returns all Products with the given name

        :param name: the name of the Product you want to match
        :type name: str

        :return: a collection of Products with that name
        :rtype: list

        """
        logger.info("Processing product name query for %s ...", name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category: str) -> list:
        """Returns all of the Products in a category

        :param category: the category of the Products you want to match
        :type category: str

        :return: a collection of Products in that category
        :rtype: list

        """
        logger.info("Processing product category query for %s ...", category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_price(cls, price: float) -> list:
        """Returns all of the Products with a given price

        :param category: the price of the Products you want to match
        :type category: float

        :return: a collection of Products with that price
        :rtype: list

        """
        logger.info("Processing product price query for %s ...", price)
        return cls.query.filter(cls.price == price)
