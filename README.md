# NYU DevOps Project - Product Service

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

Products Service - Representation of the products for a catalog where merchants can add updates and display products.


## Overview

This project the code for Orders Service for Product service. The `/service` folder contains the  `models.py` file for Product model and a `routes.py` file for Product service. The `/tests` folder has test case for testing the model and the service separately.

## Running the service locally
Before Run, make sure you have install vscode, Docker Desktop, Remote Containers extension first. Then you could clone the repository and then run the following commands:

- ```cd products```
- ```code .```
- Reopen the folder in Dev Container
- Run ```flask run``` command on the terminal
- The service is available at localhost: ```http://localhost:8000```

To run the all the test cases locally, please run the command nosetests. The test cases have 96% code coverage currently.




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

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
