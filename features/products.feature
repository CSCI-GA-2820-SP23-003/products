Feature: The products service back-end
    As a Products Manager
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name         | desc            | price | category   | inventory | discount | like | created _date | modified_date | deleted_date |
        | orange juice | made in the us  | 3.99  | beverage   | 999       | 1.0      | 642  | 2019-11-18    | 2019-12-18    |              |
        | milk         | oat milk        | 5.5   | dairy      | 15        | 1.0      | 56   | 2019-11-18    |               |              |
        | carrot       |                 | 2.5   | fresh food | 0         | 1.0      | 12   | 2019-11-18    |               | 2021-04-01   |
        | ice cream    | popular item    | 6.69  | frozen     | 90        | 0.85     | 7574 | 2019-11-18    |               |              |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Search products by id
    When I visit the "home page"
    And I set the "Name" to "sangria"
    And I set the "Desc" to "original from Spain"
    And I set the "Price for create" to "18"
    And I set the "Category" to "cocktail"
    And I press the "Create" button
    Then I should see the message "SUCCESS"
    When I copy the "Id Created" field
    And I press the "Clear" button
    Then the "Id Created" field should be empty
    And the "Name for create" field should be empty
    And the "Category for create" field should be empty
    And the "Description for create" field should be empty
    And the "Price for create" field should be empty
    When I paste the "ID for List" field
    And I press the "List By ID" button
    Then I should see the message "SUCCESS"
    And I should see "Switch" in the results