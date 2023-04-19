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