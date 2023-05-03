Feature: The products service back-end
    As a Products Manager
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name         | desc            | price | category   | inventory | discount | like | created_date | modified_date | deleted_date |
        | orange juice | made in the us  | 3.99  | beverage   | 999       | 1.0      | 642  | 2019-11-18   |               |              |
        | milk         | oat milk        | 5.5   | dairy      | 15        | 1.0      | 56   | 2019-11-18   |               |              |
        | carrot       |                 | 2.5   | fresh food | 0         | 1.0      | 12   | 2019-11-18   |               |              |
        | ice cream    | popular item    | 6.69  | frozen     | 90        | 0.85     | 7574 | 2019-11-18   |               |              |

Scenario: The server is running
    When I visit the "home page"
    Then I should see "Product RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Retrieve products by id
    When I visit the "home page"
    And I set the "Name" to "sangria"
    And I set the "Desc" to "original from Spain"
    And I set the "Price" to "9.9"
    And I set the "Category" to "cocktail"
    And I set the "Inventory" to "5"
    And I set the "Discount" to "0.9"
    And I set the "like" to "0"
    And I set the "Created_date" to "2019-11-30"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "sangria" in the "Name" field
    And I should see "riginal from Spain" in the "Desc" field
    And I should see "9.9" in the "Price" field
    And I should see "cocktail" in the "Category" field
    And I should see "5" in the "Inventory" field
    And I should see "0.9" in the "Discount" field
    And I should see "0" in the "Like" field
    And I should see "2019-11-30" in the "Created_date" field

Scenario: List all products
    When I visit the "Home Page"
    And I press the "List" button
    Then I should see the message "Success"
    And I should see "orange juice" in the results
    And I should see "milk" in the results
    And I should not see "leo" in the results

Scenario: Search for products
    When I visit the "Home Page"
    And I set the "Category" to "dairy"
    And I press the "Search" button
    Then I should see the message "Success"
    And I should see "milk" in the results
    And I should not see "orange juice" in the results

Scenario: Like a Product
    When I visit the "Home Page"
    And I set the "Name" to "airpods"
    And I set the "Desc" to "newest"
    And I set the "Price" to "239.9"
    And I set the "Category" to "3C product"
    And I set the "Inventory" to "5"
    And I set the "Discount" to "1"
    And I set the "like" to "0"
    And I set the "Created_date" to "2019-11-30"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
    When I paste the "Id" field
    And I press the "Like" button
    Then I should see the message "Success like a product"
    And I should not see "1" in the results
    And I should not see "2" in the results

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "macBook Air"
    And I set the "Desc" to "newest"
    And I set the "Price" to "539.9"
    And I set the "Category" to "3C product"
    And I set the "Inventory" to "3"
    And I set the "Discount" to "1"
    And I set the "like" to "0"
    And I set the "Created_date" to "2019-11-30"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "macBook Air" in the "Name" field
    When I change "Name" to "macBook Pro"
    And I change "Price" to "555.5"
    And I change "Category" to "3C"
    And I change "Inventory" to "30"
    And I change "Discount" to "0.9"
    And I change "Like" to "10"
    And I press the "Update" button
    Then I should see the message "Success"
    When I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "macBook Pro" in the "Name" field
    And I should see "555.5" in the "Price" field
    And I should see "3C" in the "Category" field
    And I should see "30" in the "Inventory" field
    And I should see "0.9" in the "Discount" field
    And I should see "10" in the "Like" field

Scenario: Create a product
    When I visit the "home page"
    And I set the "Name" to "sangria"
    And I set the "Desc" to "original from Spain"
    And I set the "Price" to "9.9"
    And I set the "Category" to "cocktail"
    And I set the "Inventory" to "5"
    And I set the "Discount" to "0.9"
    And I set the "like" to "0"
    And I set the "Created_date" to "2019-11-30"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "sangria" in the "Name" field
    And I should see "riginal from Spain" in the "Desc" field
    And I should see "9.9" in the "Price" field
    And I should see "cocktail" in the "Category" field
    And I should see "5" in the "Inventory" field
    And I should see "0.9" in the "Discount" field
    And I should see "0" in the "Like" field
    And I should see "2019-11-30" in the "Created_date" field

Scenario: Delete a product
    When I visit the "home page"
    And I set the "Name" to "sangria"
    And I set the "Desc" to "original from Spain"
    And I set the "Price" to "9.9"
    And I set the "Category" to "cocktail"
    And I set the "Inventory" to "5"
    And I set the "Discount" to "0.9"
    And I set the "like" to "0"
    And I set the "Created_date" to "2019-11-30"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see the message "Success"
    And I should see "sangria" in the "Name" field
    And I should see "riginal from Spain" in the "Desc" field
    And I should see "9.9" in the "Price" field
    And I should see "cocktail" in the "Category" field
    And I should see "5" in the "Inventory" field
    And I should see "0.9" in the "Discount" field
    And I should see "0" in the "Like" field
    And I should see "2019-11-30" in the "Created_date" field
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
    When I paste the "Id" field
    And I press the "Delete" button
    Then I should see the message "Product has been Deleted!"
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should not see "Success"
    And I press the "Clear" button
    And the "Id" field should be empty
    And the "Name" field should be empty
    And the "Desc" field should be empty
    And the "Price" field should be empty
    And the "Category" field should be empty
    And the "Inventory" field should be empty
    And the "Discount" field should be empty
    And the "like" field should be empty
    And the "Created_date" field should be empty
    And the "Modified_date" field should be empty
    And the "Deleted_date" field should be empty
