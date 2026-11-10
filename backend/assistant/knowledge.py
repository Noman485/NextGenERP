"""Project-scoped knowledge for the NextGenERP Assistant.

Everything in this module is written for end users of NextGenERP. The assistant
is intentionally limited to this product: inventory, catalog, suppliers, sales
orders, purchase orders, forecasting and day-to-day usage.
"""

PROJECT_OVERVIEW = """
NextGenERP is an inventory and procurement ERP. It includes:
- Dashboard with stock health, low-stock alerts and recent activity.
- Products, categories and suppliers.
- Inventory operations (stock in / stock out) with an audit trail.
- Sales orders: Pending -> Confirmed -> Shipped -> Delivered, with cancellation.
- Purchase orders: Pending -> Approved -> Ordered -> Received, with receiving.
- Demand Forecast: a 7-day outlook and suggested reorders based on live stock,
  lead time, safety stock, recent sales and weather.
- An optional 3D warehouse snapshot and 3D forecast chart.
""".strip()

PROJECT_INTRO = (
    "I am the NextGenERP Assistant. I only help with this workspace: inventory, "
    "products, categories, suppliers, sales orders, purchase orders, demand "
    "forecasting and how to use the app. I can read the live workspace data to "
    "answer questions, but I cannot change records for you."
)

SCOPE_REFUSAL = (
    "I can only help with NextGenERP — inventory, products, categories, "
    "suppliers, sales orders, purchase orders, demand forecasts and how to use "
    "this workspace. I cannot help with general knowledge, news, coding or "
    "other topics.\n\nTry asking:\n"
    "- Show low-stock products\n"
    "- What are the pending sales orders?\n"
    "- How do I add a product?\n"
    "- What should I reorder?"
)

DEFAULT_SUGGESTIONS = [
    "Show low-stock products",
    "What are the pending sales orders?",
    "How do I add a product?",
    "What should I reorder?",
]

DOMAIN_TERMS = {
    "nextgenerp", "erp", "inventory", "stock", "product", "products", "catalog",
    "sku", "category", "categories", "supplier", "suppliers", "vendor",
    "purchase", "purchasing", "sales", "order", "orders", "reorder",
    "forecast", "forecasting", "demand", "warehouse", "dashboard", "login",
    "register", "password", "account", "report", "wape", "xgboost", "3d",
    "shipment", "delivery", "received", "cancelled", "pending", "approved",
    "confirmed", "shipped", "delivered", "low stock", "out of stock",
}

GREETING_TERMS = {
    "hi", "hello", "hey", "namaste", "good morning", "good afternoon",
    "good evening", "thanks", "thank you", "ok", "okay",
}

KNOWLEDGE = [
    {
        "id": "add-product",
        "title": "Add a product",
        "keywords": [
            "add product", "new product", "create product", "product add",
            "add a product", "how do i add product", "product kaise",
        ],
        "answer": (
            "To add a product:\n"
            "1. Open Products from the sidebar.\n"
            "2. Select Add Product.\n"
            "3. Enter the product name, SKU and price.\n"
            "4. Optionally set opening stock, reorder level and category.\n"
            "5. Save the product.\n\n"
            "SKU must be unique. Stock and reorder level cannot be negative."
        ),
    },
    {
        "id": "edit-product",
        "title": "Edit or delete a product",
        "keywords": [
            "edit product", "update product", "delete product", "remove product",
            "change product price", "product delete",
        ],
        "answer": (
            "Open Products, find the product in the table and use Edit or Delete. "
            "Deleting a product is blocked when sales orders or purchase orders "
            "reference it, so historical records stay intact. To stop selling an "
            "item without losing history, keep the product and set its stock to "
            "zero instead."
        ),
    },
    {
        "id": "add-category",
        "title": "Add a category",
        "keywords": [
            "add category", "new category", "create category", "category add",
        ],
        "answer": (
            "Open Categories and select Add Category. Enter a unique name and an "
            "optional description, then save. A category cannot be deleted while "
            "products are assigned to it."
        ),
    },
    {
        "id": "add-supplier",
        "title": "Add a supplier",
        "keywords": [
            "add supplier", "new supplier", "create supplier", "supplier add",
            "vendor add",
        ],
        "answer": (
            "Open Suppliers and select Add Supplier. Enter the supplier name, "
            "then optionally add email, phone, address, lead time in days and a "
            "performance rating from 0 to 5. Save the supplier.\n\n"
            "Lead time is used by the demand forecast when it calculates suggested "
            "reorders."
        ),
    },
    {
        "id": "stock-movement",
        "title": "Record stock in or stock out",
        "keywords": [
            "stock in", "stock out", "add stock", "remove stock", "stock adjust",
            "inventory operation", "record stock", "stock movement", "adjust stock",
        ],
        "answer": (
            "Open Inventory Operations from the sidebar.\n"
            "1. Choose Stock In or Stock Out.\n"
            "2. Select the product.\n"
            "3. Enter a whole quantity greater than zero.\n"
            "4. Add a short reason, for example 'New shipment' or 'Damaged goods'.\n"
            "5. Select Record Stock Movement.\n\n"
            "Stock Out is rejected if the quantity is higher than available stock. "
            "Every successful movement is written to the stock history."
        ),
    },
    {
        "id": "create-sales-order",
        "title": "Create a sales order",
        "keywords": [
            "create sales order", "new sales order", "add sales order",
            "place order", "sell product", "sales order kaise", "new sale",
        ],
        "answer": (
            "Open Sales Orders and use the create-order form. Choose a product, "
            "enter the customer name and a whole quantity, then submit.\n\n"
            "Stock is reduced immediately when the order is created. The order "
            "starts as Pending. If stock is insufficient, the order is rejected."
        ),
    },
    {
        "id": "sales-status",
        "title": "Sales order statuses and cancellation",
        "keywords": [
            "sales order status", "confirm order", "ship order", "deliver order",
            "cancel sales order", "cancel order", "order status", "sales lifecycle",
        ],
        "answer": (
            "Sales order flow: Pending -> Confirmed -> Shipped -> Delivered.\n"
            "- Pending or Confirmed orders can be cancelled.\n"
            "- Cancelling restores the reserved stock exactly once.\n"
            "- Delivered and Cancelled are final states.\n"
            "- Sales order history cannot be deleted.\n\n"
            "Use the status control on the Sales Orders page to move an order "
            "forward."
        ),
    },
    {
        "id": "create-purchase-order",
        "title": "Create a purchase order",
        "keywords": [
            "create purchase order", "new purchase order", "add purchase order",
            "purchase order kaise", "order from supplier", "buy stock",
        ],
        "answer": (
            "Open Purchase Orders and use the create-order form. Choose a supplier "
            "and product, enter the quantity and unit price, then submit.\n\n"
            "A purchase order starts as Pending and does not change stock yet. "
            "Stock is added only when the order is marked Received."
        ),
    },
    {
        "id": "purchase-status",
        "title": "Purchase order statuses and receiving",
        "keywords": [
            "purchase order status", "approve order", "receive order", "receive stock",
            "receive purchase order", "receive a purchase order", "purchase lifecycle",
            "mark received", "purchase order cancel",
        ],
        "answer": (
            "Purchase order flow: Pending -> Approved -> Ordered -> Received.\n"
            "- An Approved order can also be marked Received directly.\n"
            "- Pending, Approved or Ordered orders can be cancelled.\n"
            "- Receiving adds the ordered quantity to stock exactly once.\n"
            "- Received and Cancelled are final states.\n\n"
            "If receiving is repeated, stock is not added twice."
        ),
    },
    {
        "id": "forecast",
        "title": "Demand forecast and suggested reorders",
        "keywords": [
            "forecast", "demand forecast", "demand planning", "prediction",
            "suggested reorder", "reorder suggestion", "reorder quantity",
            "forecast kaise", "demand kaise",
        ],
        "answer": (
            "Open Demand Forecast from the sidebar to see:\n"
            "- A 7-day demand outlook for trained products.\n"
            "- Suggested reorder quantities based on forecasted demand, lead time, "
            "safety stock and current inventory.\n"
            "- Urgent items that should be ordered before lead time runs out.\n\n"
            "Use the All / Needs reorder filter to focus the table, and Refresh "
            "forecast to reload it. The forecast is a planning aid; review supplier "
            "and stock details before ordering."
        ),
    },
    {
        "id": "dashboard",
        "title": "Dashboard and low-stock alerts",
        "keywords": [
            "dashboard", "low stock alert", "stock alert", "kpi", "overview",
            "home page", "attention required",
        ],
        "answer": (
            "The Dashboard shows total products, units on hand, low-stock and "
            "out-of-stock counts, sales and purchase order summaries, recent "
            "activity and a 3D stock snapshot.\n\n"
            "A product is low stock when its quantity is above zero but at or "
            "below its reorder level. Out of stock means the quantity is zero. "
            "The 3D view is optional; the rest of the dashboard still works if it "
            "cannot load."
        ),
    },
    {
        "id": "login",
        "title": "Sign in and registration",
        "keywords": [
            "login", "sign in", "register", "create account", "sign up",
            "forgot password", "reset password", "password", "session expired",
        ],
        "answer": (
            "Sign in with your username and password. New accounts can be created "
            "from the Create an account link.\n\n"
            "- Usernames are case-insensitive and may use letters, numbers, dot, "
            "underscore and hyphen.\n"
            "- Registration passwords must be at least 12 characters.\n"
            "- A session lasts 30 minutes. If it expires, sign in again.\n\n"
            "This build does not include self-service password reset. If you cannot "
            "sign in, contact the person who manages your deployment. Never share "
            "your password in chat."
        ),
    },
    {
        "id": "permissions",
        "title": "Roles and permissions",
        "keywords": [
            "role", "permission", "admin", "access", "who can", "authorization",
        ],
        "answer": (
            "All registered accounts currently have the same permissions. There is "
            "no separate administrator role or role-based access control in this "
            "build. Every protected page requires a valid signed-in session."
        ),
    },
    {
        "id": "navigation",
        "title": "Navigation and search",
        "keywords": [
            "navigate", "navigation", "sidebar", "find page", "search module",
            "jump to", "menu", "where is",
        ],
        "answer": (
            "Use the sidebar to open Dashboard, Demand Forecast, Products, "
            "Inventory Operations, Categories, Suppliers, Sales Orders and "
            "Purchase Orders.\n\n"
            "On desktop, the Jump to module search in the header also finds pages "
            "by name or keyword, for example 'stock', 'orders' or 'vendors'. On "
            "mobile, open the menu button to reach the same pages."
        ),
    },
    {
        "id": "delete-rules",
        "title": "Why a record cannot be deleted",
        "keywords": [
            "cannot delete", "can't delete", "delete blocked", "409", "conflict",
            "referenced", "in use",
        ],
        "answer": (
            "NextGenERP protects history and relationships:\n"
            "- A product cannot be deleted while orders or purchase orders use it.\n"
            "- A category cannot be deleted while products are assigned to it.\n"
            "- A supplier cannot be deleted while purchase orders reference it.\n"
            "- Sales order history cannot be deleted at all.\n\n"
            "These rules keep inventory and order records consistent."
        ),
    },
    {
        "id": "errors",
        "title": "Common errors and troubleshooting",
        "keywords": [
            "error", "not working", "failed", "cannot connect", "backend",
            "401", "422", "500", "loading", "blank page", "troubleshoot",
        ],
        "answer": (
            "Quick checks:\n"
            "- If data does not load, confirm the backend is running and open "
            "/health on the API; it should return status ok.\n"
            "- If you are signed out unexpectedly, the 30-minute session expired. "
            "Sign in again.\n"
            "- A 422 message usually means a required field is missing or invalid.\n"
            "- A 409 message means the action conflicts with existing records, "
            "such as deleting a supplier that has purchase orders.\n"
            "- If one dashboard section fails, the other sections still load; use "
            "Try again to refresh."
        ),
    },
    {
        "id": "assistant",
        "title": "What the assistant can do",
        "keywords": [
            "who are you", "what can you do", "assistant help", "your scope",
            "are you chatgpt", "what do you know",
        ],
        "answer": (
            "I am the NextGenERP Assistant. I can explain how the app works and "
            "answer questions from live workspace data: stock levels, low-stock "
            "items, pending orders, suppliers, product prices and reorder needs.\n\n"
            "I am read-only: I cannot create, edit, cancel or delete records. Use "
            "the relevant page for changes. I only answer NextGenERP questions."
        ),
    },
]


def _normalize(value: str) -> str:
    return " ".join(str(value or "").lower().split())


def find_knowledge(message: str):
    """Return the best matching help entry for a message, or None."""
    text = _normalize(message)
    best_entry = None
    best_score = 0

    for entry in KNOWLEDGE:
        score = 0
        for keyword in entry["keywords"]:
            if keyword in text:
                score += len(keyword.split()) * 2 + 1
        title_words = [word for word in _normalize(entry["title"]).split() if len(word) > 3]
        score += sum(1 for word in title_words if word in text)

        if score > best_score:
            best_score = score
            best_entry = entry

    return best_entry if best_score >= 3 else None
