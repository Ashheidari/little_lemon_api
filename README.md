online food ordering REST Framework Application
=================================

This application is a REST API built using Django Rest Framework, providing endpoints for managing categories, menu items, user roles (managers and delivery crew), cart, and orders for an online food ordering system.

Table of Contents
-----------------

-   [Installation](#installation)
-   [Usage](#usage)
-   [API Endpoints](#api-endpoints)
-   [Permissions](#permissions)
-   [Throttling](#throttling)
-   [Models](#models)
-   [Serializers](#serializers)
-   [Permissions](#permissions)
-   [Throttling](#throttling)
-   [Contributing](#contributing)
-   [License](#license)

Installation
------------

1.  Clone the repository:

    sh

    Copy code

    `git clone <repository-url>
    cd <repository-directory>`

2.  Install dependencies:

    sh

    Copy code

    `pip install -r requirements.txt`

3.  Run migrations:

    sh

    Copy code

    `python manage.py migrate`

4.  Create a superuser:

    sh

    Copy code

    `python manage.py createsuperuser`

5.  Start the development server:

    sh

    Copy code

    `python manage.py runserver`

Usage
-----

Use a tool like Postman or cURL to interact with the API endpoints. Ensure you have the necessary permissions and authentication tokens when making requests.

API Endpoints
-------------

### Categories

-   **GET /categories/**: List all categories.
-   **POST /categories/**: Create a new category. (Admin or Manager only)

### Menu Items

-   **GET /menu-items/**: List all menu items.
-   **POST /menu-items/**: Create a new menu item. (Admin or Manager only)
-   **PUT /menu-items/{id}/**: Update a menu item. (Admin or Manager only)
-   **DELETE /menu-items/{id}/**: Delete a menu item. (Admin or Manager only)

### Managers

-   **GET /groups/manager/users/**: List all managers.
-   **POST /groups/manager/users/**: Add a user to managers. (Admin or Manager only)
-   **DELETE /groups/manager/users/{userId}/**: Remove a user from managers. (Admin or Manager only)

### Delivery Crew

-   **GET /groups/delivery-crew/users/**: List all delivery crew members.
-   **POST /groups/delivery-crew/users/**: Add a user to delivery crew. (Admin or Manager only)
-   **DELETE /groups/delivery-crew/users/{userId}/**: Remove a user from delivery crew. (Admin or Manager only)

### Cart

-   **GET /cart/menu-item/**: List all items in the cart for the authenticated user.
-   **POST /cart/menu-item/**: Add an item to the cart for the authenticated user.
-   **DELETE /cart/menu-item/**: Clear the cart for the authenticated user.

### Orders

-   **GET /orders/**: List all orders for the authenticated user. Managers and delivery crew can see all orders.
-   **POST /orders/**: Place an order from the authenticated user's cart.
-   **GET /orders/{id}/**: Retrieve a specific order.
-   **PUT /orders/{id}/**: Update a specific order. (Admin, Manager, or assigned delivery crew only)
-   **DELETE /orders/{id}/**: Delete a specific order. (Admin or Manager only)

Permissions
-----------

-   **IsAuthenticated**: Only authenticated users can access the endpoint.
-   **IsAdminUser**: Only admin users can access the endpoint.
-   **IsManager**: Only users in the Managers group can access the endpoint.
-   **IsDeliveryCrew**: Only users in the Delivery Crew group can access the endpoint.

Throttling
----------

The application uses the following throttle classes:

-   **AnonRateThrottle**: Limits the rate of requests for anonymous users.
-   **UserRateThrottle**: Limits the rate of requests for authenticated users.

Models
------

-   **Category**: Represents a category of menu items.
-   **MenuItem**: Represents an item on the menu.
-   **User**: Represents a user of the application.
-   **Cart**: Represents a user's cart.
-   **OrderItem**: Represents an item in an order.
-   **Order**: Represents an order placed by a user.

Serializers
-----------

-   **CategorySerializer**: Serializes the `Category` model.
-   **MenuItemSerializer**: Serializes the `MenuItem` model.
-   **UserSerializer**: Serializes the `User` model.
-   **CartSerializer**: Serializes the `Cart` model.
-   **OrderItemSerializer**: Serializes the `OrderItem` model.
-   **SingleOrderSerilaizer**: Serializes the `Order` model for individual orders.
-   **OrderSerializer**: Serializes the `Order` model.
-   **OrderSerializerForCrew**: Serializes the `Order` model for delivery crew updates.
