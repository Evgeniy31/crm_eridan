# CRM Eridan

A comprehensive Customer Relationship Management (CRM) system built with Django for managing client requests, production orders, repairs, and user roles.

## Features

- **User Management**: Role-based access control with multiple user types (Admin, Manager, Production Chief, Design Chief, Chief, Quality Manager, Executor)
- **Client Requests**: Create, manage, and track client requests with approval workflows
- **Production Management**: Handle production orders and product management
- **Repair Management**: Track and manage repair requests
- **Notifications**: In-app notification system
- **Analytics**: Dashboard with key metrics and reports
- **Kanban Board**: Visual task management
- **Chat System**: Internal messaging between users

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd crm_eridan
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with:
   ```
   DJANGO_SECRET_KEY=your-secure-secret-key-here
   DEBUG=False
   DJANGO_ALLOWED_HOSTS=your-domain.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com
   ```

5. Run migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Docker Setup

Alternatively, use Docker Compose:

1. Build and run the containers:
   ```bash
   docker-compose up --build
   ```

2. Set environment variables in docker-compose.yml or create a .env file

## Usage

- Access the application at `http://localhost:8000`
- Admin interface at `http://localhost:8000/admin/`
- Default admin credentials: admin / Adaptive

## Testing

Run the test suite:
```bash
python manage.py test
```

## Project Structure

- `crm_eridan/`: Main Django project settings
- `users/`: User management and authentication
- `requests/`: Client request management
- `clients/`: Client and address management
- `production/`: Production orders and products
- `repairs/`: Repair request management
- `notifications/`: Notification system
- `analytics/`: Analytics and reporting

## Security Notes

- Change the default SECRET_KEY before deploying to production
- Set DEBUG=False in production
- Use HTTPS in production
- Regularly update dependencies

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

This project is proprietary software.
