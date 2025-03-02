# Order Processing Backend

This project is a backend system for managing and processing orders in an e-commerce platform. It is built using FastAPI and integrates with PostgreSQL for data storage and Redis for caching.

## Project Structure

```
order-processing-backend
├── app
│   ├── api
│   │   ├── __init__.py
│   │   ├── orders.py
│   ├── core
│   │   ├── __init__.py
│   │   ├── config.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── session.py
│   ├── main.py
│   └── schemas
│       ├── __init__.py
│       ├── order.py
├── docker-compose.yaml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd order-processing-backend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   Ensure you have PostgreSQL installed and running. Create a database for the application and update the database connection settings in `app/core/config.py`.

5. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Orders

- **Create Order**
  - **Endpoint:** `POST /orders`
  - **Description:** Create a new order.
  - **Request Body:** Order details (user_id, item_ids, total_amount).
  - **Response:** Order confirmation with order_id.

- **Check Order Status**
  - **Endpoint:** `GET /orders/{order_id}`
  - **Description:** Retrieve the status of an existing order.
  - **Response:** Order details including status.

- **Fetch Metrics**
  - **Endpoint:** `GET /orders/metrics`
  - **Description:** Get metrics related to orders (e.g., total orders, revenue).
  - **Response:** Metrics data.

## Design Decisions

- **FastAPI** was chosen for its performance and ease of use in building RESTful APIs.
- **PostgreSQL** is used for its robustness and support for complex queries.
- **Redis** is implemented for caching frequently accessed data to improve performance.

## Assumptions

- The application assumes that the PostgreSQL database is properly configured and accessible.
- Redis is assumed to be running for caching purposes.

## License

This project is licensed under the MIT License.