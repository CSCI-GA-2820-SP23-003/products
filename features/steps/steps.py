######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Product Steps

Steps file for Product.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
import random
from behave import given
from compare import expect


@given('the following products')
def step_impl(context):
    """ Delete all Products and load new ones """
    # List all of the products and delete them one by one
    rest_endpoint = f"{context.BASE_URL}/products"
    context.resp = requests.get(rest_endpoint)
    expect(context.resp.status_code).to_equal(200)
    for product in context.resp.json():
        context.resp = requests.delete(f"{rest_endpoint}/{product['id']}")
        expect(context.resp.status_code).to_equal(204)

    # load the database with new products
    for row in context.table:
        payload = {
            "id": random.randint(0,1000),
            "name": row['name'],
            "desc": row['desc'],
            "price": float(row['price']),
            "category": row['category'],
            "inventory": row['inventory'],
            "discount": row['discount'],
            "like": int(row['like']),
            "created_date": row['created_date'],
            "modified_date": row['modified_date'],
            "deleted_date": row['deleted_date']
        }
        context.resp = requests.post(rest_endpoint, json=payload)
        expect(context.resp.status_code).to_equal(201)
