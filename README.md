
# Django E-commerce Project

This is a Django-based e-commerce platform with features like product management, order management, and user authentication. The project also includes APIs for login, registration, order management, and more.

## Features

- User authentication (Registration and Login)
- Product management (CRUD operations)
- Order management (view, update order status)
- Reviews and ratings for products
- Admin dashboard to manage products and orders
- RESTful API endpoints using Django REST Framework
- Product Display: Users can view all products, view product details, and add them to the cart.
- Shopping Cart: Users can add products to the cart and proceed to checkout.
- Order Management: Users can place orders, and admins can view and update order statuses.

## Technologies Used

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- Postgres (or any other database, configurable in settings)
- Token-based Authentication for APIs
- Bootstrap 4/5 for frontend styling
- jQuery for interactivity

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/muhammedshabeen/E-commerce
   cd E-commerce
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   setup a database connection using postgres
   ```

4. Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Navigate to `http://127.0.0.1:8000` to access the application.

## API Endpoints

### Authentication

- **POST /api/register/**: Register a new user.
    - Request: `username`, `email`, `password`
    - Response: `token`

- **POST /api/login/**: Login and receive a token.
    - Request: `username`, `password`
    - Response: `token`

### Products

- **GET /api/product-view-api**: List all products.


### Orders
- Authentication needed for listing user orders
- **GET /api/order-view-api**: List all orders.

## Frontend

The frontend is where customers can view and interact with products, manage their cart, and place orders. To access the frontend of the web app, use the following URL:

- URL: `http://127.0.0.1:8000/`
  
### Features Available for Customers:
- **View all products**: Browse through the products available in the store.
- **Add to Cart**: Customers can add multiple items to their cart.
- **Place Orders**: Customers can place orders and create an address module for future use.
- **View Order Status**: Track the status of previous orders (Pending, Approved, Shipped, Delivered).
- **Rate Products**: Customers can rate products they've purchased.


###  Backend Admin Panel
To manage products, orders, and users, log in to the Backend admin panel:

- URL: `http://127.0.0.1:8000/super-admin/`
- Use the superuser credentials you created during setup.
  
  **Login Details**:
  - Username: `<your_superuser_username>`
  - Password: `<your_superuser_password>`

Once logged in, you can:
- **Manage Products**: Add, edit, or delete products.
- **View and Update Orders**: Manage order statuses (Pending, Approved, Shipped, Delivered).
- **View Customers**: Access the list of customers and their details.



## Main Admin Panel

- URL: `http://127.0.0.1:8000/admin/`
- Use the superuser credentials you created during setup.

