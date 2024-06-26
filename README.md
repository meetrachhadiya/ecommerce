# Django Ecommerce Website

This Django Ecommerce Website is a project designed to serve as a foundation for building an online store. It comes equipped with essential features such as user authentication, product management, cart functionality, and integration with Razorpay for payments.

https://github.com/meetrachhadiya/ecommerce/assets/77917050/5beda269-6860-4127-91f4-ad3c116f608f

## Prerequisites
- Python 3.x installed on your system
- Basic understanding of Django framework

## Installation and Setup

1. **Download Project**: Clone this repository to your local machine:
    ```
    git clone <repository_url>
    ```

2. **Install Requirements**: Navigate to the project directory and install the required dependencies using pip:
    ```
    cd django-ecommerce-website
    pip install -r requirements.txt
    ```

3. **Database Setup**: Make migrations and migrate to set up the database schema:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

4. **Create Superuser**: Create a superuser account to access the Django admin panel:
    ```
    python manage.py createsuperuser
    ```

    Follow the prompts to enter a username, email, and password for the superuser.

5. **Add Products to Dashboard**: Log in to the Django admin panel using the superuser credentials created in the previous step. Navigate to the Product section to add products to your store.

6. **Configure Environment Variables**: Create a `.env` file in the project root directory and add the following environment variables:
    ```
    RAZORPAY_KEY_ID=<your_razorpay_key_id>
    RAZORPAY_KEY_SECRET=<your_razorpay_key_secret>
    EMAIL_HOST_USER=<your_email_address>
    EMAIL_HOST_PASSWORD=<your_email_password>
    ```

    Replace `<your_razorpay_key_id>`, `<your_razorpay_key_secret>`, `<your_email_address>`, and `<your_email_password>` with your actual Razorpay API keys and email credentials.

7. **Run the Development Server**: Start the Django development server:
    ```
    python manage.py runserver
    ```

    Visit `http://localhost:8000` in your web browser to access the website.

## Usage
- Users can browse products, add them to the cart, and proceed to checkout.
- Admins can manage products, orders, and user accounts through the Django admin panel.
