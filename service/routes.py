"""
Products Service

Paths:
------
GET / - Displays a UI for Selenium testing
GET /products - Returns a list all of the Products
GET /products/{product_id} - Returns the Product with a given id number
POST /products - Creates a new Product record in the database
PUT /products/{product_id} - Updates a Product record in the database
DELETE /products/{product_id} - Deletes a Product record in the database
PUT /products/{product_id}/like - Likes a Product with a given id number
"""

from flask import jsonify
from flask_restx import Resource, fields, reqparse
from service.common import status  # HTTP Status Codes
from service.models import Product

# Import Flask application
from . import app, api


######################################################################
# Configure the Root route before OpenAPI
######################################################################
# Define the model so that the docs reflect what can be sent
create_model = api.model('Product', {
    'name': fields.String(required=True,
                          description='The name of the Product'),
    'desc': fields.String(required=False,
                          description='The description of the Product'),
    'price': fields.Float(required=True,
                          description='The price of the Product'),
    'category': fields.String(required=True,
                              description='The category of Product (e.g., beverage, dairy, fresh food, frozen.)'),
    'inventory': fields.Integer(required=True,
                                description='The inventory of the Product'),
    'discount': fields.Float(required=True,
                             description='The discount of the Product'),
    'like': fields.Integer(required=True,
                           description='The number of like of the Product'),
    'created_date': fields.Date(required=True,
                                  description='The day the Product was created'),
    'modified_date': fields.Date(required=False,
                                 description='The day the Product detail was modified'),
    'deleted_date': fields.Date(required=False,
                                description='The day the Product was deleted')
})

product_model = api.inherit(
    'ProductModel',
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
product_args = reqparse.RequestParser()
product_args.add_argument('name', type=str, location='args', required=False, help='List Products by name')
product_args.add_argument('category', type=str, location='args', required=False, help='List Products by category')
product_args.add_argument('price', type=str, location='args', required=False, help='List Products by Price')


######################################################################
# HEALTH ENDPOINT
######################################################################
@app.route("/health")
def health():
    """Endpoint to check health status of the app."""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Index page"""
    return app.send_static_file("index.html")


######################################################################
#  PATH: /products/{product_id}
######################################################################
@api.route('/products/<product_id>')
@api.param('product_id', 'The Product identifier')
class ProductResource(Resource):
    """
    ProductResource class

    Allows the manipulation of a single Product
    GET /product{id} - Returns a Product with the id
    PUT /product{id} - Update a Product with the id
    DELETE /product{id} -  Deletes a Product with the id
    """
    # ------------------------------------------------------------------
    # RETRIEVE A PRODUCT
    # ------------------------------------------------------------------
    @api.response(404, 'Product not found')
    @api.marshal_with(product_model)
    def get(self, product_id):
        """
        Retrieve a single Product

        This endpoint will return a Product based on it's id
        """
        app.logger.info("Request for product with id: %s", product_id)
        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
        app.logger.info("Returning product: %s", product.name)
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # UPDATE AN EXISTING PRODUCT
    # ------------------------------------------------------------------
    @api.response(404, 'Product not found')
    @api.response(400, 'The posted Product data was not valid')
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        """
        Update a Product

        This endpoint will update a Product based the body that is posted
        """
        app.logger.info("Request to update product with id: %s", product_id)
        product = Product.find(product_id)

        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
        app.logger.debug('Payload = %s', api.payload)

        data = api.payload
        product.deserialize(data)
        product.id = product_id
        product.update()

        app.logger.info("Product with id [%s] updated.", product.id)
        return product.serialize(), status.HTTP_200_OK

    # ------------------------------------------------------------------
    # DELETE A PRODUCT
    # ------------------------------------------------------------------
    @api.response(204, 'Product deleted')
    def delete(self, product_id):
        """
        Delete a Product

        This endpoint will delete a Product based the id specified in the path
        """
        app.logger.info("Request to delete product with id: %s", product_id)
        product = Product.find(product_id)

        if product:
            product.delete()
            app.logger.info('Product with id [%s] was deleted', product_id)

        return '', status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /products
######################################################################
@api.route('/products', strict_slashes=False)
class ProductCollection(Resource):
    """ Handles all interactions with collections of Products """

    # ------------------------------------------------------------------
    # LIST ALL PRODUCTS
    # ------------------------------------------------------------------
    @api.expect(product_args, validate=True)
    @api.marshal_list_with(product_model)
    def get(self):
        """ Returns all of the Products """
        app.logger.info("Request to list Products...")

        products = []
        args = product_args.parse_args()
        if args['category']:
            app.logger.info('Filtering by category: %s', args['category'])
            products = Product.find_by_category(args['category'])
        elif args['name']:
            app.logger.info('Filtering by name: %s', args['name'])
            products = Product.find_by_name(args['name'])
        elif args['price']:
            app.logger.info('Filtering by price: %s', args['price'])
            products = Product.find_by_price(args['price'])
        else:
            app.logger.info('Returning unfiltered list.')
            products = Product.all()

        # app.logger.info('[%s] Prodcuts returned', len(products))
        results = [product.serialize() for product in products]
        return results, status.HTTP_200_OK

    # ------------------------------------------------------------------
    # ADD A NEW PET
    # ------------------------------------------------------------------
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        """
        Creates a Product
        This endpoint will create a Product based the data in the body that is posted
        """
        app.logger.info("Request to Create a Product")

        product = Product()
        app.logger.debug('Payload = %s', api.payload)
        product.deserialize(api.payload)
        product.create()

        app.logger.info("Product with ID [%s] created.", product.id)
        location_url = api.url_for(ProductResource, product_id=product.id, _external=True)

        return product.serialize(), status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /products/{product_id}/like
######################################################################
@api.route('/products/<product_id>/like')
@api.param('product_id', 'The Product identifier')
class LikeResource(Resource):
    """ Like actions on a Product """
    @api.response(404, 'Product not found')
    def put(self, product_id):
        """
        Like a Product

        This endpoint will like a Product
        """
        app.logger.info("Request to like product with id: %s", product_id)

        product = Product.find(product_id)
        if not product:
            abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")

        app.logger.info("Product with id [%s] like count before update: %s", product.like)
        product.like += 1
        product.update()
        app.logger.info("Product with id [%s] updated.", product.id)
        app.logger.info("Product with id [%s] like count after update: %s", product.like)
        return product.serialize(), status.HTTP_200_OK


######################################################################
# QUERY PRODUCTS
######################################################################
# @app.route("/products/query", methods=["GET"])
# def query_products():
#     """
#     Query products by name, category, price.
#     """
#     app.logger.info("Request to query products.")
#     name = request.args.get("name")
#     category = request.args.get("category")
#     price = request.args.get("price")

#     print(request.args)

#     if name:
#         name_products = Product.find_by_name(name)
#     else:
#         name_products = Product.all()
#     if category:
#         category_products = Product.find_by_category(category)
#     else:
#         category_products = Product.all()
#     if price:
#         price_products = Product.find_by_price(price)
#     else:
#         price_products = Product.all()
#     products = list(set(name_products).intersection(category_products, price_products))
#     results = [product.serialize() for product in products]
#     app.logger.info(f"Returning {len(results)} products.")
#     response = jsonify(results), status.HTTP_200_OK
#     return response


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def abort(error_code: int, message: str):
    """Logs errors before aborting"""
    app.logger.error(message)
    api.abort(error_code, message)
