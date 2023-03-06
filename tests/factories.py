"""
Test Factory to make fake objects for testing
"""
from datetime import date

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyFloat, FuzzyInteger
from service.models import Product


class ProductFactory(factory.Factory):
    """Creates fake products that you don't have to feed"""

    class Meta:  # pylint: disable=too-few-public-methods
        """Maps factory to data model"""

        model = Product

    id = factory.Sequence(lambda n: n)
    name = FuzzyChoice(choices=["Orange Juice", "Milk", "Carrot", "Ice Cream"])
    desc = factory.Faker("word")
    price = FuzzyFloat(10, 60)
    category = FuzzyChoice(choices=["beverage", "dairy", "fresh food", "frozen"])
    inventory = FuzzyInteger(0, 40)
    discount = FuzzyChoice(choices=[0.3, 0.75, 0.9])
    created_date = date(2008, 1, 1)
    modified_date = date(2008, 1, 2)
    deleted_date = date(2008, 1, 3)
