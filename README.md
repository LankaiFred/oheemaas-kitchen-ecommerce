# Ohemaa's Kitchen - E-Commerce Website

A modern e-commerce platform for Ohemaa's Kitchen Restaurant and Bar, built with Django backend, HTML/CSS/JavaScript frontend, and MySQL database.

## Features

- 🏠 **Home Page** - Welcome and featured items
- 📋 **Menu Display** - Browse food and drink items with descriptions and prices
- 🛒 **Shopping Cart** - Add/remove items, manage quantities
- 👤 **User Authentication** - Sign up, login, user profiles
- 📦 **Order Management** - View order history and track orders
- 🚚 **Delivery/Pickup** - Choose delivery or pickup options
- ⏰ **Restaurant Hours** - Display operating hours
- 📍 **Location Info** - Restaurant location and directions
- 📞 **Contact & Reservations** - Contact form and reservation system
- 💳 **Payment Options** - MTN MOMO, Vodafone Cash, GCB Bank, Cash on Delivery
- 👨‍💼 **Admin Dashboard** - Manage menu items, orders, and restaurant info
- ℹ️ **About Us** - Restaurant information and story

## Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Python, Django
- **Database**: MySQL
- **Payment Gateway**: MTN MOMO, Vodafone Cash, GCB Bank API Integration

## Project Structure

```
oheemaas-kitchen-ecommerce/
├── frontend/                 # Frontend files
│   ├── index.html           # Home page
│   ├── menu.html            # Menu page
│   ├── cart.html            # Shopping cart
│   ├── login.html           # Login page
│   ├── register.html        # Registration page
│   ├── profile.html         # User profile
│   ├── orders.html          # Order history
│   ├── reservation.html     # Reservation form
│   ├── contact.html         # Contact page
│   ├── about.html           # About us page
│   ├── checkout.html        # Checkout page
│   ├── css/
│   │   ├── styles.css       # Main styles
│   │   └── responsive.css   # Responsive design
│   └── js/
│       ├── main.js          # Main JavaScript
│       ├── cart.js          # Cart functionality
│       ├── auth.js          # Authentication
│       ├── payment.js       # Payment processing
│       └── api.js           # API calls

├── backend/                  # Django backend
│   ├── manage.py
│   ├── requirements.txt
│   ├── oheemaas/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── restaurant/
│   │   ├── models.py        # Database models
│   │   ├── views.py         # Views and logic
│   │   ├── urls.py          # URL routing
│   │   ├── serializers.py   # DRF serializers
│   │   ├── permissions.py   # Custom permissions
│   │   └── admin.py         # Admin configuration
│   └── api/
│       ├── views.py         # API endpoints
│       ├── urls.py
│       └── authentication.py

├── db/
│   └── schema.sql           # MySQL database schema

├── .env.example             # Environment variables template
├── .gitignore
└── README.md
```

## Installation

### Prerequisites
- Python 3.9+
- MySQL 8.0+
- Node.js (optional, for frontend build tools)

### Backend Setup

1. Clone the repository
```bash
git clone https://github.com/LankaiFred/oheemaas-kitchen-ecommerce.git
cd oheemaas-kitchen-ecommerce/backend
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Run migrations
```bash
python manage.py migrate
```

6. Create superuser
```bash
python manage.py createsuperuser
```

7. Start development server
```bash
python manage.py runserver
```

## Usage

1. **Frontend**: Open `frontend/index.html` in a web browser
2. **Backend API**: Available at `http://localhost:8000/api/`
3. **Admin Panel**: Access at `http://localhost:8000/admin/`

## Payment Integration

The platform supports multiple payment methods:
- **MTN MOMO**: Mobile money payments
- **Vodafone Cash**: Mobile wallet payments
- **GCB Bank**: Bank transfer integration
- **Cash**: Cash on delivery option

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see LICENSE.md for details.

## Support

For support, email support@oheemaaskitchen.com or create an issue in the repository.

---

**Ohemaa's Kitchen - Where Tradition Meets Taste** 🍽️
