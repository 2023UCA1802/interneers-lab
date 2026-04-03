# Inventory3 – Product & Category Management API

A Django REST API for managing **products, brands, and categories** using MongoDB, built with a clean **Controller–Service–Repository architecture**.

---

## Features

- CRUD APIs for **Products & Categories**
- Brand-based product validation (product must have a brand)
- Many-to-many mapping (Products ↔ Categories)
- Bulk product upload via CSV
- Advanced filtering (category, brand, name)
- Service Layer (business logic separation)
- Repository Layer (database abstraction)
- Input validation & duplicate checks
- Swagger API documentation
- Unit Tests (mocked repositories)
- Integration Tests (end-to-end with MongoDB)
- Parameterized Tests for edge cases
- Regression test scripts

---

## Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** MongoDB (MongoEngine)  
- **API Docs:** drf-yasg (Swagger)  
- **Testing:** unittest, parameterized  

---

## Project Structure

```bash
inventory3/
│
├── models/ # MongoEngine data models (Product, Brand, Category)
│
├── services/ # Business logic layer
│ ├── product_service.py
│ └── category_service.py
│
├── repositories/ # Database abstraction layer
│ ├── product_repository.py
│ └── category_repository.py
│
├── views.py # API controllers (DRF APIViews)
│
├── utils/ # Helper utilities
│ └── serializers.py
│
├── tests.py # All test cases
│
├── run_tests_script/ # Regression scripts
│ └── run_tests.py
│
├── seed.py # Initial category seed script
├── migrations.py # Data migration for existing products
│
├── apps.py # App configuration
├── urls.py # API route definitions
```