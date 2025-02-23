from flask import Flask, jsonify
from pymongo import MongoClient
from datetime import datetime, timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["ecommerce"]
customers_collection = db["customers"]
orders_collection = db["orders"]

@app.route('/high-value-customers', methods=['GET',"POST"])
def get_high_value_customers():
    six_months_ago = datetime.utcnow() - timedelta(days=180)

    pipeline = [
        {"$lookup": {
            "from": "orders",
            "localField": "customerId",
            "foreignField": "customerId",
            "as": "orders"
        }},
        {"$set": {
            "totalSpent": {"$sum": "$orders.totalAmount"},
            "averageOrderValue": {
                "$cond": {
                    "if": {"$gt": [{"$size": "$orders"}, 0]},
                    "then": {"$divide": [{"$sum": "$orders.totalAmount"}, {"$size": "$orders"}]},
                    "else": 0
                }
            },
            "lastPurchaseDate": {"$max": "$orders.orderDate"}
        }},
        {"$match": {"totalSpent": {"$gte": 500}}},  # Exclude customers with less than 500 spent
        {"$set": {
            "isActive": {"$gte": ["$lastPurchaseDate", six_months_ago]},
            "loyaltyTier": {
                "$switch": {
                    "branches": [
                        {"case": {"$lt": ["$totalSpent", 1000]}, "then": "Bronze"},
                        {"case": {"$and": [{"$gte": ["$totalSpent", 1000]}, {"$lte": ["$totalSpent", 3000]}]}, "then": "Silver"},
                        {"case": {"$gt": ["$totalSpent", 3000]}, "then": "Gold"}
                    ],
                    "default": "Bronze"
                }
            }
        }},
        {"$unwind": "$orders"},
        {"$unwind": "$orders.products"},
        {"$group": {
            "_id": {"customerId": "$customerId", "category": "$orders.products.category"},
            "customerDetails": {"$first": {
                "name": "$name", "email": "$email", "totalSpent": "$totalSpent",
                "averageOrderValue": "$averageOrderValue", "lastPurchaseDate": "$lastPurchaseDate",
                "isActive": "$isActive", "loyaltyTier": "$loyaltyTier"
            }},
            "categorySpend": {"$sum": "$orders.products.price"},
            "categoryPurchaseCount": {"$sum": 1}
        }},
        {"$group": {
            "_id": "$_id.customerId",
            "customerDetails": {"$first": "$customerDetails"},
            "categoryWiseSpend": {"$push": {"category": "$_id.category", "spend": "$categorySpend"}},
            "favoriteCategory": {"$push": {"category": "$_id.category", "count": "$categoryPurchaseCount"}}
        }},
        {"$set": {
            "favoriteCategory": {
                "$arrayElemAt": [
                    {"$sortArray": {"input": "$favoriteCategory", "sortBy": {"count": -1, "category": 1}}}, 0
                ]
            }
        }},
        {"$project": {
            "_id": 0,
            "customerId": "$_id",
            "name": "$customerDetails.name",
            "email": "$customerDetails.email",
            "totalSpent": "$customerDetails.totalSpent",
            "averageOrderValue": "$customerDetails.averageOrderValue",
            "loyaltyTier": "$customerDetails.loyaltyTier",
            "lastPurchaseDate": "$customerDetails.lastPurchaseDate",
            "isActive": "$customerDetails.isActive",
            "favoriteCategory": "$favoriteCategory.category",
            "categoryWiseSpend": 1
        }}
    ]

    result = list(customers_collection.aggregate(pipeline))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
