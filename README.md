# BRAND NEW STORE 0.2

Production-ready Flask + PostgreSQL e-commerce starter for a Bangladeshi clothing store.

## Features

- Premium black/white/gold responsive storefront
- Uploaded official logo used unchanged
- Categories, search and filters
- Product cards with stock, sizes, colors, old/current price and discount
- Product detail pages with multiple images
- Server-side session cart
- Guest checkout (no customer account)
- Cash on Delivery + configurable bKash/Nagad/manual payment instructions
- Unique order IDs and persistent PostgreSQL order records
- Order status workflow: New, Confirmed, Processing, Packed, Shipped, Delivered, Cancelled
- Secure admin login with hashed passwords and session protection
- Admin product/category/order/settings management
- Multiple product image uploads with file validation
- CSRF protection
- Login rate limiting
- Configurable delivery charges/free-delivery threshold
- Configurable WhatsApp button
- Configurable generic SMS JSON API
- Environment-based secrets
- Gunicorn production server configuration
- Docker/PostgreSQL deployment option

## 1. Local setup

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Create a PostgreSQL database, then set `DATABASE_URL` in `.env`.

Example:

```text
postgresql+psycopg://brandnew:strong-password@localhost:5432/brandnewstore
```

Run:

```bash
python app.py init-db
python app.py seed
python app.py create-admin
python app.py
```

Open:

- Store: http://127.0.0.1:5000/
- Admin: http://127.0.0.1:5000/admin/login

## 2. Admin login

The first admin is created with:

```bash
python app.py create-admin
```

The command asks for a username and password if the environment values are not supplied. Passwords are hashed with Werkzeug and are never stored in HTML or JavaScript.

After login, change the password from **Admin > Settings**.

## 3. Logo

The supplied logo is stored at:

`app/static/images/logo.png`

The website references that exact file and does not recolor or redesign it.

## 4. Product images

Admin can upload JPG, JPEG, PNG or WEBP images. The server checks file type with Pillow, limits image dimensions and stores generated safe filenames.

## 5. SMS

The project supports a generic JSON SMS provider. Set:

```text
SMS_ENABLED=true
SMS_API_URL=https://provider.example/send
SMS_API_KEY=...
SMS_SENDER_ID=...
SMS_ADMIN_NUMBER=01...
```

The app sends a JSON body containing:

```json
{
  "to": "admin-number",
  "message": "New order received - Order ID: BNS-..., Customer Name: ..., Phone Number: ..., Total Amount: ৳..."
}
```

Because SMS providers use different API contracts, the provider endpoint must accept this JSON format or the `send_admin_sms()` function in `app/services.py` can be adapted to the provider's documented schema. No API key is hard-coded.

## 6. Payments

bKash and Nagad are implemented as configurable manual payment methods. Admin enters the receiving numbers in Settings. The checkout displays the selected number and asks the customer to provide the transaction/reference note.

For a real automated bKash/Nagad gateway, obtain merchant credentials from the provider and replace the manual payment adapter with the provider's official server-to-server API. Secrets must remain in environment variables.

## 7. Production

Use HTTPS behind Nginx/Cloudflare and Gunicorn:

```bash
gunicorn -w 3 -b 127.0.0.1:8000 app:app
```

Set:

```text
FLASK_ENV=production
SESSION_COOKIE_SECURE=true
SECRET_KEY=<long-random-secret>
DATABASE_URL=<production-postgresql-url>
```

Do not commit `.env`.

Recommended production architecture:

Nginx/Cloudflare -> Gunicorn -> Flask -> PostgreSQL

Use a persistent volume for `app/static/uploads/` or move uploads to an object-storage service.

## 8. Docker

Build:

```bash
docker compose up --build
```

Then initialize:

```bash
docker compose exec web python app.py init-db
docker compose exec web python app.py seed
docker compose exec web python app.py create-admin
```

## 9. Security notes

- Admin authentication is server-side.
- Passwords are hashed.
- CSRF protection is enabled for forms.
- Admin routes require authentication.
- Login attempts are rate-limited.
- Uploaded images are type-checked with Pillow.
- Filenames are generated server-side.
- Prices and stock are re-read from the database during checkout.
- Order totals are calculated server-side.
- Secrets are environment variables.
- Use HTTPS in production.

## 10. Editing

Main areas:

- `app/models.py` - database models
- `app/routes.py` - storefront/admin routes
- `app/services.py` - SMS and image validation
- `app/templates/` - pages
- `app/static/css/style.css` - design
- `app/static/js/store.js` - cart/filter UX
- `.env` - store settings/secrets
