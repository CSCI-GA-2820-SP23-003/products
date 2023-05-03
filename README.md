# NYU DevOps Project - Product Service

[![Build Status](https://github.com/CSCI-GA-2820-SP23-003/products/actions/workflows/tdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-003/products/actions)
[![Build Status](https://github.com/CSCI-GA-2820-SP23-003/products/actions/workflows/bdd.yml/badge.svg)](https://github.com/CSCI-GA-2820-SP23-003/products/actions)
[![codecov](https://codecov.io/gh/CSCI-GA-2820-SP23-003/products/branch/master/graph/badge.svg?token=UWLJEWXJFB)](https://codecov.io/gh/CSCI-GA-2820-SP23-003/products)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

Products Service - Representation of the products for a catalog where merchants can add updates and display products.


## Overview

This project the code for Product service. The `/service` folder contains the  `models.py` file for Product model and a `routes.py` file for Product service. The `/tests` folder has test case for testing the model 
and the service separately.

## Our Service End Point
The service is currently hosted on a Kubernetes Cluster on IBM Cloud.

- Dev End Point:  http://169.51.207.249:31001/
- Prod End Point: http://169.51.207.249:31006/
- Our Pipeline: https://cloud.ibm.com/devops/pipelines/562cb654-4cd4-43ba-9a03-ab1c4351c784?env_id=ibm:yp:us-south

## Running the service locally
Before Run, make sure you have install [Docker Desktop](https://www.docker.com/products/docker-desktop), [Visual Studio Code](https://code.visualstudio.com), [Remote Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) first. Then you could clone the repository and then run the following commands:

- ```cd products```
- ```code .```
- Reopen the folder in Dev Container
- Run ```flask run``` command on the terminal
- The service is available at localhost: ```http://localhost:8000```

To run the all the test cases locally, please run the command ```nosetests```. The test cases have 99% code coverage currently.

To run the BDD tests, first start the service in a terminal by running ```honcho start``` and then run ```behave``` in another terminal.


## Products Service APIs

### Index

GET `/`

### Products Operations


| Endpoint        | Methods | Rule
| --------------- | ------- | --------------------------
| create_products | POST    | ```/products```
| delete_products | DELETE  | ```/products/{int:product_id}```
| get_products    | GET     | ```/products/{int:product_id}```
| list_products   | GET     | ```/products```
| search_products | GET     | ```/products?<query_field>=<query_value>```
| update_products | PUT     | ```/products/{int:product_id}```
| like_products   | PUT     | ```/prouducts/{int:product_id}/like```


## Product Service APIs - Usage

### Create a Product

URL : `http://127.0.0.1:8000/products`

Method : POST

Auth required : No

Permissions required : None

Create a product with json file which included product name, description, price, category, inventory, discount and created date.

Example:

Request Body (JSON)
```
{
  "price": 0.5,
  "name": "Cheese",
  "category": "dairy",
  "created_date": "2023-03-07",
  "inventory": 5,
  "desc": "This is more popular",
  "discount": 1,
  "like": 0
}
```

Success Response : `HTTP_201_CREATED`
```
{
  "category": "dairy",
  "created_date": "2023-03-07",
  "deleted_date": null,
  "desc": "This is more popular",
  "discount": 1.0,
  "id": 956,
  "inventory": 5,
  "modified_date": null,
  "name": "Cheese",
  "price": 0.5,
  "like": 0
}
```

### Read/Get a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : GET

Auth required : No

Permissions required : None

Gets/Reads a product with id provided in the URL

Example:

Success Response : `HTTP_200_OK`
```
{
  "category": "dairy",
  "created_date": "2023-03-07",
  "deleted_date": null,
  "desc": "This is more popular",
  "discount": 1.0,
  "id": 956,
  "inventory": 5,
  "modified_date": null,
  "name": "Cheese",
  "price": 0.5,
  "like": 0
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Product with id '1' could not be found.",
  "status": 404
}
```

### Update a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : PUT

Auth required : No

Permissions required : None

Updates a product with id provided in the URL according to the updated fields provided in the body

Example:

Request Body (JSON)
```
{
  "price": 0.5,
  "name": "Cheese",
  "category": "dairy",
  "created_date": "2023-03-07",
  "inventory": 50,
  "desc": "This is more popular",
  "discount": 1,
  "like": 0
}
```


Success Response : `HTTP_200_OK`
```
{
  "category": "dairy",
  "created_date": "2023-03-07",
  "deleted_date": null,
  "desc": "This is more popular",
  "discount": 1.0,
  "id": 955,
  "inventory": 50,
  "modified_date": null,
  "name": "Cheese",
  "price": 0.5,
  "like": 0
}
```

Failure Response : `HTTP_404_NOT_FOUND`
```
{
  "error": "Not Found",
  "message": "404 Not Found: Product with id '1' could not be found.",
  "status": 404
}
```

### Delete a Product

URL : `http://127.0.0.1:8000/products/{int:product_id}`

Method : DELETE

Auth required : No

Permissions required : None

Deletes a Product with id

Example:

Success Response : `204 NO CONTENT`

### List Products

URL : `http://127.0.0.1:8000/products`

Method : GET

Auth required : No

Permissions required : None

Lists all the Products

Example:

Success Response : `HTTP_200_OK`
```
[
  {
    "category": "dairy",
    "created_date": "2023-03-07",
    "deleted_date": null,
    "desc": "This is more popular",
    "discount": 1.0,
    "id": 954,
    "inventory": 5,
    "modified_date": null,
    "name": "Cheese",
    "price": 0.5,
    "like": 0
  }
]
```

### Like a Products

URL : `http://127.0.0.1:8000/products/{int:product_id}/like`

Method : PUT

Auth required : No

Permissions required : None

Like a Product with given id

Example:

Success Response : `HTTP_200_OK`
```
[
  {
    "category": "dairy",
    "created_date": "2023-03-07",
    "deleted_date": null,
    "desc": "This is more popular",
    "discount": 1.0,
    "id": 954,
    "inventory": 5,
    "modified_date": null,
    "name": "Cheese",
    "price": 0.5,
    "like": 1
  }
]
```

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants
└── static                 - code for UI of the homepage

tests/                - test cases package
├── __init__.py       - package initializer
├── factories.py      - factory to generate instances of model
├── test_cli_commands - tests custom flask cli commands
├── test_models.py    - test suite for business models
└── test_routes.py    - test suite for service routes

features/             - bdd test cases package
├── products.feature  - products test scenarios
├── environment.py    - environment for bdd tests
└── steps             - code for describing bdd steps
    ├── steps.py      - steps for products.feature
    ├── web_steps.py  - steps for web interaction with selenium

deploy/               - yaml files for kubernetes deployment
├── deployment.yaml   - Deployment for products api
├── postgresql.yaml   - StatefulSet, Service, Secret for postgres db 
├── service.yaml      - Service for products api
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
