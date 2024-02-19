# LittleLemon REST API

## Overview

Welcome to the LittleLemon REST API! This API serves as the backend for a sophisticated food delivery platform. It provides functionalities for managing menu items, categories, user roles, shopping carts, and orders. Users can seamlessly browse through available menu items, add items to their carts, place orders, and track their order status.

## Installation

To run the LittleLemon REST API on your local machine, follow these steps:

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Mu5alaf/littlelemon-api.git
    ```

2. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

3. **Apply migrations**:

    ```bash
    python manage.py migrate
    ```

4. **Run the development server**:

    ```bash
    python manage.py runserver
    ```

## Features

- **Menu Items Management**: CRUD operations on menu items with search and ordering capabilities.
- **User Role Management**: Assign roles such as admin, manager, and delivery crew to users.
- **Shopping Cart Functionality**: Users can add, remove, and manage items in their shopping carts.
- **Order Placement and Tracking**: Seamless order placement with real-time order tracking.
- **Robust Authentication**: Token-based authentication using JWT for secure access to API endpoints.

## LittleLemon REST API Endpoints

## Authentication  

- `/auth/`: Authentication endpoints provided by Djoser.
- `/auth/token/`: Obtain JWT token for authentication.

## Menu Items

- `/menu-items/`: List and create menu items.
- `/menu-items/category/`: List and create categories for menu items.
- `/menu-items/<int:pk>/`: Retrieve, update, or delete a specific menu item.

## User Groups Management

- `/groups/managers/users/`: Add users to the manager group.
- `/groups/managers/users/<int:pk>/`: Remove a user from the manager group.
- `/groups/delivery-crew/users/`: Add users to the delivery crew group.
- `/groups/delivery-crew/users/<int:pk>/`: Remove a user from the delivery crew group.

## Shopping Cart

- `/cart/menu-items/`: Manage items in the user's shopping cart.

## Orders

- `/menu-items/orders/`: List and create orders.
- `/menu-items/orders/<int:pk>/`: Retrieve and update a specific order.

## Authentications

To authenticate requests, obtain a JWT token by sending a POST request to `/api/token/`. Include the token in the Authorization header of subsequent requests:
    ```
    Authorization: Bearer <token>
    ```

## Permissions

- **Managers**: Full access to all features and functionalities.
- **Delivery Crew**: Limited access to view and update assigned orders.
- **Regular Users**: Limited access to menu items, shopping cart, and order placement.



