from pymongo import MongoClient
from datetime import datetime

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
customers_collection = db["customers"]
orders_collection = db["orders"]

# Clear existing data (optional, to avoid duplicates)
customers_collection.delete_many({})
orders_collection.delete_many({})

# Sample Customers Data
customers = [
    {"customerId": "C001", "name": "John Doe", "email": "johndoe@example.com"},
    {"customerId": "C002", "name": "Jane Smith", "email": "janesmith@example.com"},
    {"customerId": "C003", "name": "Alice Brown", "email": "alicebrown@example.com"},
    {"customerId": "C004", "name": "Bob Johnson", "email": "bobjohnson@example.com"},
    {"customerId": "C005", "name": "Charlie White", "email": "charliewhite@example.com"},
    {"customerId": "C006", "name": "David Black", "email": "davidblack@example.com"},
    {"customerId": "C007", "name": "Emma Wilson", "email": "emmawilson@example.com"},
    {"customerId": "C008", "name": "Frank Lee", "email": "franklee@example.com"}
]

# Insert Customers Data
customers_collection.insert_many(customers)

# Sample Orders Data
orders = [
    {
        "customerId": "C001",
        "orderId": "O1001",
        "totalAmount": 450,
        "products": [
            {"category": "Electronics", "price": 200},
            {"category": "Clothing", "price": 150},
            {"category": "Clothing", "price": 100}
        ],
        "orderDate": datetime(2024, 1, 10)
    },
    {
        "customerId": "C001",
        "orderId": "O1002",
        "totalAmount": 900,
        "products": [{"category": "Electronics", "price": 900}],
        "orderDate": datetime(2024, 2, 15)
    },
    {
        "customerId": "C002",
        "orderId": "O2001",
        "totalAmount": 1200,
        "products": [{"category": "Home", "price": 1200}],
        "orderDate": datetime(2023, 7, 25)
    },
    {
        "customerId": "C003",
        "orderId": "O3001",
        "totalAmount": 3500,
        "products": [{"category": "Furniture", "price": 3500}],
        "orderDate": datetime(2024, 3, 1)
    },
    {
        "customerId": "C004",
        "orderId": "O4001",
        "totalAmount": 300,
        "products": [{"category": "Books", "price": 300}],
        "orderDate": datetime(2024, 2, 20)
    },
    {
        "customerId": "C005",
        "orderId": "O5001",
        "totalAmount": 1500,
        "products": [
            {"category": "Gaming", "price": 800},
            {"category": "Gaming", "price": 700}
        ],
        "orderDate": datetime(2023, 12, 5)
    },
    {
        "customerId": "C006",
        "orderId": "O6001",
        "totalAmount": 400,
        "products": [{"category": "Sports", "price": 400}],
        "orderDate": datetime(2024, 1, 30)
    },
    {
        "customerId": "C007",
        "orderId": "O7001",
        "totalAmount": 4200,
        "products": [
            {"category": "Jewelry", "price": 2500},
            {"category": "Clothing", "price": 1700}
        ],
        "orderDate": datetime(2024, 2, 8)
    },
    {
        "customerId": "C008",
        "orderId": "O8001",
        "totalAmount": 2100,
        "products": [
            {"category": "Electronics", "price": 1000},
            {"category": "Clothing", "price": 1100}
        ],
        "orderDate": datetime(2024, 1, 15)
    }
]

# Insert Orders Data
orders_collection.insert_many(orders)

print("Dummy data inserted successfully!")
