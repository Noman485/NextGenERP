"""Localized copy and language metadata for the NextGenERP Assistant.

The assistant supports English, Hindi and Bengali. This module keeps every
user-facing string and language-specific keyword in one place so the engine and
the optional LLM bridge can stay language-agnostic.
"""

DEFAULT_LANGUAGE = "en"

LANGUAGES = {
    "en": {
        "label": "English",
        "native_label": "English",
        "speech_locale": "en-IN",
        "llm_name": "English",
    },
    "hi": {
        "label": "Hindi",
        "native_label": "हिन्दी",
        "speech_locale": "hi-IN",
        "llm_name": "Hindi using Devanagari script",
    },
    "bn": {
        "label": "Bengali",
        "native_label": "বাংলা",
        "speech_locale": "bn-IN",
        "llm_name": "Bengali using Bengali script",
    },
}


def normalize_language(value) -> str:
    code = str(value or "").strip().lower()
    return code if code in LANGUAGES else DEFAULT_LANGUAGE


def language_metadata(language) -> dict:
    return LANGUAGES[normalize_language(language)]


# ---------------------------------------------------------------------------
# Greetings, scope and suggestions
# ---------------------------------------------------------------------------
PROJECT_INTRO = {
    "en": (
        "I am the NextGenERP Assistant. I only help with this workspace: "
        "inventory, products, categories, suppliers, sales orders, purchase "
        "orders, demand forecasting and how to use the app. I can read the live "
        "workspace data to answer questions, but I cannot change records for "
        "you.\n\nAsk me about live stock, low-stock items, orders, suppliers or "
        "how to use any page."
    ),
    "hi": (
        "मैं NextGenERP सहायक हूँ। मैं केवल इस वर्कस्पेस में मदद करता हूँ: "
        "इन्वेंटरी, उत्पाद, श्रेणियाँ, आपूर्तिकर्ता, बिक्री ऑर्डर, खरीद ऑर्डर, "
        "मांग पूर्वानुमान और ऐप का उपयोग कैसे करें। मैं उत्तर देने के लिए लाइव "
        "वर्कस्पेस डेटा पढ़ सकता हूँ, लेकिन आपके लिए रिकॉर्ड नहीं बदल सकता।\n\n"
        "मुझसे लाइव स्टॉक, कम-स्टॉक वस्तुओं, ऑर्डर, आपूर्तिकर्ताओं या किसी भी "
        "पेज के उपयोग के बारे में पूछें।"
    ),
    "bn": (
        "আমি NextGenERP সহায়ক। আমি শুধু এই ওয়ার্কস্পেসে সাহায্য করি: "
        "ইনভেন্টরি, পণ্য, বিভাগ, সরবরাহকারী, বিক্রয় অর্ডার, ক্রয় অর্ডার, "
        "চাহিদা পূর্বাভাস এবং অ্যাপটি কীভাবে ব্যবহার করবেন। উত্তর দিতে আমি লাইভ "
        "ওয়ার্কস্পেস ডেটা পড়তে পারি, কিন্তু আপনার জন্য রেকর্ড বদলাতে পারি না।\n\n"
        "আমাকে লাইভ স্টক, কম-স্টক পণ্য, অর্ডার, সরবরাহকারী বা যেকোনো পেজ "
        "ব্যবহারের বিষয়ে জিজ্ঞাসা করুন।"
    ),
}

SCOPE_REFUSAL = {
    "en": (
        "I can only help with NextGenERP — inventory, products, categories, "
        "suppliers, sales orders, purchase orders, demand forecasts and how to "
        "use this workspace. I cannot help with general knowledge, news, coding "
        "or other topics.\n\nTry asking:\n"
        "- Show low-stock products\n"
        "- What are the pending sales orders?\n"
        "- How do I add a product?\n"
        "- What should I reorder?"
    ),
    "hi": (
        "मैं केवल NextGenERP में मदद कर सकता हूँ — इन्वेंटरी, उत्पाद, श्रेणियाँ, "
        "आपूर्तिकर्ता, बिक्री ऑर्डर, खरीद ऑर्डर, मांग पूर्वानुमान और इस "
        "वर्कस्पेस का उपयोग। मैं सामान्य ज्ञान, समाचार, कोडिंग या अन्य "
        "विषयों में मदद नहीं कर सकता।\n\nऐसे पूछें:\n"
        "- कम स्टॉक वाले उत्पाद दिखाएँ\n"
        "- लंबित बिक्री ऑर्डर कौन से हैं?\n"
        "- उत्पाद कैसे जोड़ें?\n"
        "- मुझे क्या रीऑर्डर करना चाहिए?"
    ),
    "bn": (
        "আমি শুধু NextGenERP-এ সাহায্য করতে পারি — ইনভেন্টরি, পণ্য, বিভাগ, "
        "সরবরাহকারী, বিক্রয় অর্ডার, ক্রয় অর্ডার, চাহিদা পূর্বাভাস এবং এই "
        "ওয়ার্কস্পেসের ব্যবহার। আমি সাধারণ জ্ঞান, সংবাদ, কোডিং বা অন্যান্য "
        "বিষয়ে সাহায্য করতে পারি না।\n\nএভাবে জিজ্ঞাসা করুন:\n"
        "- কম স্টকের পণ্য দেখান\n"
        "- কোন বিক্রয় অর্ডারগুলি মুলতুবি আছে?\n"
        "- কীভাবে একটি পণ্য যোগ করব?\n"
        "- আমার কী পুনরায় অর্ডার করা উচিত?"
    ),
}

FALLBACK = {
    "en": (
        "I could not find that in the current workspace data. I can help with "
        "live stock levels, low-stock items, pending orders, suppliers, product "
        "prices and reorder needs.\n\nTry:\n"
        "- Show low-stock products\n"
        "- What are the pending purchase orders?\n"
        "- What is the stock of a product?\n"
        "- How do I record a stock movement?"
    ),
    "hi": (
        "मुझे वर्तमान वर्कस्पेस डेटा में यह नहीं मिला। मैं लाइव स्टॉक स्तर, "
        "कम-स्टॉक वस्तुओं, लंबित ऑर्डर, आपूर्तिकर्ताओं, उत्पाद कीमतों और "
        "रीऑर्डर आवश्यकताओं में मदद कर सकता हूँ।\n\nप्रयास करें:\n"
        "- कम स्टॉक वाले उत्पाद दिखाएँ\n"
        "- लंबित खरीद ऑर्डर कौन से हैं?\n"
        "- किसी उत्पाद का स्टॉक क्या है?\n"
        "- स्टॉक मूवमेंट कैसे दर्ज करें?"
    ),
    "bn": (
        "বর্তমান ওয়ার্কস্পেস ডেটায় এটি পাইনি। আমি লাইভ স্টক স্তর, কম-স্টক "
        "পণ্য, মুলতুবি অর্ডার, সরবরাহকারী, পণ্যের মূল্য এবং পুনরায় অর্ডারের "
        "প্রয়োজন সম্পর্কে সাহায্য করতে পারি।\n\nচেষ্টা করুন:\n"
        "- কম স্টকের পণ্য দেখান\n"
        "- কোন ক্রয় অর্ডারগুলি মুলতুবি আছে?\n"
        "- একটি পণ্যের স্টক কত?\n"
        "- কীভাবে স্টক মুভমেন্ট লিখব?"
    ),
}

DEFAULT_SUGGESTIONS = {
    "en": [
        "Show low-stock products",
        "What are the pending sales orders?",
        "How do I add a product?",
        "What should I reorder?",
    ],
    "hi": [
        "कम स्टॉक वाले उत्पाद दिखाएँ",
        "लंबित बिक्री ऑर्डर कौन से हैं?",
        "उत्पाद कैसे जोड़ें?",
        "मुझे क्या रीऑर्डर करना चाहिए?",
    ],
    "bn": [
        "কম স্টকের পণ্য দেখান",
        "কোন বিক্রয় অর্ডারগুলি মুলতুবি আছে?",
        "কীভাবে একটি পণ্য যোগ করব?",
        "আমার কী পুনরায় অর্ডার করা উচিত?",
    ],
}


def intro_text(language) -> str:
    return PROJECT_INTRO[normalize_language(language)]


def refusal_text(language) -> str:
    return SCOPE_REFUSAL[normalize_language(language)]


def fallback_text(language) -> str:
    return FALLBACK[normalize_language(language)]


def suggestions_for(language) -> list[str]:
    return list(DEFAULT_SUGGESTIONS[normalize_language(language)])


# ---------------------------------------------------------------------------
# Scope detection and intent keywords
# ---------------------------------------------------------------------------
DOMAIN_TERMS_BY_LANGUAGE = {
    "en": {
        "nextgenerp", "erp", "inventory", "stock", "product", "products",
        "catalog", "sku", "category", "categories", "supplier", "suppliers",
        "vendor", "purchase", "purchasing", "sales", "order", "orders",
        "reorder", "forecast", "forecasting", "demand", "warehouse",
        "dashboard", "login", "register", "password", "account", "report",
        "wape", "xgboost", "3d", "shipment", "delivery", "received",
        "cancelled", "pending", "approved", "confirmed", "shipped",
        "delivered", "low stock", "out of stock",
    },
    "hi": {
        "इन्वेंटरी", "स्टॉक", "उत्पाद", "प्रोडक्ट", "कैटलॉग", "श्रेणी",
        "श्रेणियाँ", "कैटेगरी", "आपूर्तिकर्ता", "सप्लायर", "विक्रेता", "खरीद",
        "बिक्री", "ऑर्डर", "पूर्वानुमान", "मांग", "डैशबोर्ड", "गोदाम",
        "खाता", "लॉगिन", "पासवर्ड", "रिपोर्ट", "डिलीवरी", "शिपमेंट",
        "रीऑर्डर", "कम स्टॉक", "स्टॉक खत्म", "लंबित", "स्वीकृत", "रद्द",
    },
    "bn": {
        "ইনভেন্টরি", "স্টক", "পণ্য", "প্রোডাক্ট", "ক্যাটালগ", "বিভাগ",
        "শ্রেণি", "ক্যাটাগরি", "সরবরাহকারী", "সাপ্লায়ার", "বিক্রেতা", "ক্রয়",
        "বিক্রয়", "অর্ডার", "পূর্বাভাস", "চাহিদা", "ড্যাশবোর্ড", "গুদাম",
        "অ্যাকাউন্ট", "লগইন", "পাসওয়ার্ড", "রিপোর্ট", "ডেলিভারি",
        "শিপমেন্ট", "পুনরায় অর্ডার", "কম স্টক", "স্টক শেষ", "মুলতুবি",
        "অনুমোদিত", "বাতিল",
    },
}

GREETING_TERMS_BY_LANGUAGE = {
    "en": {
        "hi", "hello", "hey", "namaste", "good morning", "good afternoon",
        "good evening", "thanks", "thank you", "ok", "okay",
    },
    "hi": {
        "नमस्ते", "नमस्कार", "हैलो", "हाय", "सुप्रभात", "शुभ संध्या",
        "धन्यवाद", "शुक्रिया", "ठीक है",
    },
    "bn": {
        "নমস্কার", "হ্যালো", "হাই", "সুপ্রভাত", "শুভ সন্ধ্যা", "ধন্যবাদ",
        "ঠিক আছে",
    },
}

GREETING_FIRST_WORDS = {
    "en": {"hi", "hello", "hey", "namaste", "thanks"},
    "hi": {"नमस्ते", "नमस्कार", "हैलो", "हाय", "धन्यवाद", "शुक्रिया"},
    "bn": {"নমস্কার", "হ্যালো", "হাই", "ধন্যবাদ"},
}


def domain_terms(language) -> set[str]:
    code = normalize_language(language)
    terms = set(DOMAIN_TERMS_BY_LANGUAGE["en"])
    if code != "en":
        terms |= DOMAIN_TERMS_BY_LANGUAGE[code]
    return terms


def greeting_terms(language) -> set[str]:
    code = normalize_language(language)
    terms = set(GREETING_TERMS_BY_LANGUAGE["en"])
    if code != "en":
        terms |= GREETING_TERMS_BY_LANGUAGE[code]
    return terms


def greeting_first_words(language) -> set[str]:
    code = normalize_language(language)
    words = set(GREETING_FIRST_WORDS["en"])
    if code != "en":
        words |= GREETING_FIRST_WORDS[code]
    return words


INTENT_TERMS = {
    "low_stock": {
        "en": [
            "low stock", "low on stock", "low-stock", "running low", "reorder",
            "restock", "minimum stock", "stock kam", "kam stock",
            "need to order", "should i order",
        ],
        "hi": [
            "कम स्टॉक", "स्टॉक कम", "स्टॉक खत्म होने", "रीऑर्डर",
            "दोबारा ऑर्डर", "न्यूनतम स्टॉक", "ऑर्डर करना चाहिए",
            "स्टॉक कम है",
        ],
        "bn": [
            "কম স্টক", "স্টক কম", "স্টক শেষের পথে", "পুনরায় অর্ডার",
            "সর্বনিম্ন স্টক", "অর্ডার করা উচিত", "স্টক কম আছে",
        ],
    },
    "out_of_stock": {
        "en": ["out of stock", "no stock", "zero stock", "khatam"],
        "hi": [
            "स्टॉक खत्म", "स्टॉक में नहीं", "शून्य स्टॉक",
            "कोई स्टॉक नहीं", "खत्म हो गया",
        ],
        "bn": [
            "স্টক শেষ", "স্টকে নেই", "শূন্য স্টক", "কোনো স্টক নেই",
            "শেষ হয়ে গেছে",
        ],
    },
    "pending_sales": {
        "en": [
            "pending sales", "pending order", "open sales", "sales pending",
        ],
        "hi": [
            "लंबित बिक्री", "बिक्री ऑर्डर लंबित", "खुली बिक्री",
            "बिक्री लंबित",
        ],
        "bn": [
            "মুলতুবি বিক্রয়", "বিক্রয় অর্ডার মুলতুবি", "খোলা বিক্রয়",
            "বিক্রয় মুলতুবি",
        ],
    },
    "pending_purchase": {
        "en": [
            "pending purchase", "open purchase", "purchase pending",
            "awaiting delivery",
        ],
        "hi": [
            "लंबित खरीद", "खरीद ऑर्डर लंबित", "खुली खरीद", "खरीद लंबित",
            "डिलीवरी प्रतीक्षित",
        ],
        "bn": [
            "মুলতুবি ক্রয়", "ক্রয় অর্ডার মুলতুবি", "খোলা ক্রয়",
            "ক্রয় মুলতুবি", "ডেলিভারি অপেক্ষমাণ",
        ],
    },
    "count": {
        "en": ["how many", "count", "total", "kitne"],
        "hi": ["कितने", "कितनी", "संख्या", "कुल"],
        "bn": ["কতটি", "কত", "সংখ্যা", "মোট"],
    },
    "supplier_for": {
        "en": ["who supplies", "which supplier", "supplier for", "vendor for"],
        "hi": [
            "कौन आपूर्ति", "कौन सप्लाई", "आपूर्तिकर्ता कौन", "विक्रेता कौन",
            "किस आपूर्तिकर्ता", "कौन सप्लायर",
        ],
        "bn": [
            "কে সরবরাহ", "সরবরাহকারী কে", "কোন সরবরাহকারী", "বিক্রেতা কে",
            "কোন সাপ্লায়ার",
        ],
    },
    "product_detail": {
        "en": [
            "stock", "price", "quantity", "sku", "detail", "about", "status",
        ],
        "hi": [
            "स्टॉक", "कीमत", "मूल्य", "मात्रा", "विवरण", "स्थिति",
            "के बारे में", "जानकारी",
        ],
        "bn": [
            "স্টক", "মূল্য", "পরিমাণ", "বিস্তারিত", "অবস্থা", "সম্পর্কে",
            "তথ্য",
        ],
    },
    "supplier_detail": {
        "en": [
            "supplier", "vendor", "lead time", "rating", "contact",
        ],
        "hi": [
            "आपूर्तिकर्ता", "विक्रेता", "सप्लायर", "लीड समय", "रेटिंग",
            "संपर्क",
        ],
        "bn": [
            "সরবরাহকারী", "বিক্রেতা", "সাপ্লায়ার", "লিড টাইম", "রেটিং",
            "যোগাযোগ",
        ],
    },
    "supplier_list": {
        "en": ["supplier", "vendor"],
        "hi": ["आपूर्तिकर्ता", "विक्रेता", "सप्लायर"],
        "bn": ["সরবরাহকারী", "বিক্রেতা", "সাপ্লায়ার"],
    },
    "sales_summary": {
        "en": ["sales", "orders", "order summary"],
        "hi": ["बिक्री", "ऑर्डर", "ऑर्डर सारांश"],
        "bn": ["বিক্রয়", "অর্ডার", "অর্ডার সারাংশ"],
    },
}

ENTITY_TERMS = {
    "product": {
        "en": ["product"],
        "hi": ["उत्पाद", "प्रोडक्ट"],
        "bn": ["পণ্য", "প্রোডাক্ট"],
    },
    "supplier": {
        "en": ["supplier", "vendor"],
        "hi": ["आपूर्तिकर्ता", "विक्रेता", "सप्लायर"],
        "bn": ["সরবরাহকারী", "বিক্রেতা", "সাপ্লায়ার"],
    },
    "purchase": {
        "en": ["purchase"],
        "hi": ["खरीद"],
        "bn": ["ক্রয়"],
    },
    "order": {
        "en": ["order", "sale"],
        "hi": ["ऑर्डर", "बिक्री"],
        "bn": ["অর্ডার", "বিক্রয়"],
    },
    "category": {
        "en": ["categor"],
        "hi": ["श्रेणी", "श्रेणियाँ", "कैटेगरी"],
        "bn": ["বিভাগ", "শ্রেণি", "ক্যাটাগরি"],
    },
}

PURCHASE_TERMS = {
    "en": ["purchase", "po "],
    "hi": ["खरीद", "पर्चेज"],
    "bn": ["ক্রয়", "পারচেজ"],
}


def _merged_terms(table: dict, language) -> list[str]:
    code = normalize_language(language)
    values = list(table["en"])
    if code != "en":
        values.extend(table[code])
    return values


def terms_for(intent: str, language) -> list[str]:
    return _merged_terms(INTENT_TERMS[intent], language)


def entity_terms(entity: str, language) -> list[str]:
    return _merged_terms(ENTITY_TERMS[entity], language)


def purchase_terms(language) -> list[str]:
    return _merged_terms(PURCHASE_TERMS, language)


# ---------------------------------------------------------------------------
# Status labels
# ---------------------------------------------------------------------------
STATUS_LABELS = {
    "en": {
        "Pending": "Pending",
        "Confirmed": "Confirmed",
        "Shipped": "Shipped",
        "Delivered": "Delivered",
        "Cancelled": "Cancelled",
        "Approved": "Approved",
        "Ordered": "Ordered",
        "Received": "Received",
    },
    "hi": {
        "Pending": "लंबित",
        "Confirmed": "पुष्ट",
        "Shipped": "भेजा गया",
        "Delivered": "डिलीवर किया गया",
        "Cancelled": "रद्द",
        "Approved": "स्वीकृत",
        "Ordered": "ऑर्डर किया गया",
        "Received": "प्राप्त",
    },
    "bn": {
        "Pending": "মুলতুবি",
        "Confirmed": "নিশ্চিত",
        "Shipped": "পাঠানো হয়েছে",
        "Delivered": "বিতরণ করা হয়েছে",
        "Cancelled": "বাতিল",
        "Approved": "অনুমোদিত",
        "Ordered": "অর্ডার করা হয়েছে",
        "Received": "গৃহীত",
    },
}

PRODUCT_STATUS_LABELS = {
    "en": {
        "out of stock": "out of stock",
        "low stock": "low stock",
        "in stock": "in stock",
    },
    "hi": {
        "out of stock": "स्टॉक खत्म",
        "low stock": "कम स्टॉक",
        "in stock": "स्टॉक में है",
    },
    "bn": {
        "out of stock": "স্টক শেষ",
        "low stock": "কম স্টক",
        "in stock": "স্টকে আছে",
    },
}


def status_label(value: str, language) -> str:
    code = normalize_language(language)
    return STATUS_LABELS[code].get(value, value)


def product_status_label(value: str, language) -> str:
    code = normalize_language(language)
    return PRODUCT_STATUS_LABELS[code].get(value, value)


# ---------------------------------------------------------------------------
# Reply templates
# ---------------------------------------------------------------------------
TEXT = {
    "en": {
        "product_detail": (
            "{name} ({sku})\n"
            "- Stock: {stock} units\n"
            "- Reorder level: {reorder_level}\n"
            "- Price: {price}\n"
            "- Status: {status}\n\n"
            "Open Products to edit it, or Inventory Operations to record a "
            "stock movement."
        ),
        "supplier_detail_head": (
            "{name}\n"
            "- Lead time: {lead_time} days\n"
            "- Performance rating: {rating}"
        ),
        "supplier_contact": "- Contact: {contact}",
        "supplier_hint": (
            "Open Suppliers to view or update the supplier. Lead time is used "
            "in reorder planning."
        ),
        "low_stock_header": "Products at or below their reorder level:",
        "low_stock_line": (
            "- {name} ({sku}): {stock} units left, reorder level "
            "{reorder_level}"
        ),
        "low_stock_none": (
            "No products are at or below their reorder level right now."
        ),
        "more_line": "...and {count} more.",
        "out_of_stock_extra": "Also out of stock ({count}): {names}",
        "forecast_hint": (
            "Open Demand Forecast for suggested reorder quantities based on "
            "demand, lead time and safety stock."
        ),
        "out_of_stock_none": "No products are out of stock right now.",
        "out_of_stock_header": "{count} product(s) are out of stock:",
        "out_of_stock_line": (
            "- {name} ({sku}): reorder level {reorder_level}"
        ),
        "out_of_stock_hint": (
            "Use Inventory Operations for a stock-in movement or create a "
            "purchase order."
        ),
        "no_pending_sales": "There are no pending sales orders right now.",
        "pending_sales_header": "{count} pending sales order(s).",
        "showing_latest": " Showing the latest {count}.",
        "pending_sales_line": (
            "- Order #{id}: {customer} — {product} × {quantity}"
        ),
        "sales_hint": (
            "Open Sales Orders to confirm, ship or cancel an order."
        ),
        "no_open_purchases": "There are no open purchase orders right now.",
        "open_purchases_header": (
            "{count} open purchase order(s) (Pending, Approved or Ordered)."
        ),
        "open_purchases_line": (
            "- PO #{id}: {supplier} — {product} × {quantity} ({status})"
        ),
        "purchases_hint": (
            "Open Purchase Orders to approve, order or receive stock."
        ),
        "count_products": "The catalog has {count} product(s).",
        "count_suppliers": "There are {count} supplier(s).",
        "count_purchase_orders": "There are {count} purchase order(s).",
        "count_sales_orders": "There are {count} sales order(s).",
        "count_categories": "There are {count} categor(y/ies).",
        "sales_summary_header": "Sales orders: {count} total",
        "sales_summary_line": "- {status}: {count}",
        "sales_summary_hint": (
            "Open Sales Orders for the full list and status controls."
        ),
        "no_suppliers": (
            "No suppliers are registered yet. Open Suppliers to add one."
        ),
        "supplier_list_header": "{count} supplier(s):",
        "supplier_list_line": (
            "- {name}: lead time {lead_time} days, rating {rating}"
        ),
        "not_found_purchase": (
            "I could not find purchase order #{id} in the recent records."
        ),
        "not_found_sales": (
            "I could not find sales order #{id} in the recent records."
        ),
        "purchase_order_title": "Purchase order #{id}",
        "sales_order_title": "Sales order #{id}",
        "label_supplier": "- Supplier: {value}",
        "label_product": "- Product: {value}",
        "label_quantity": "- Quantity: {value}",
        "label_unit_price": "- Unit price: {value}",
        "label_total": "- Total: {value}",
        "label_status": "- Status: {value}",
        "label_customer": "- Customer: {value}",
        "generic_product": "product",
        "generic_supplier": "supplier",
        "supplier_for_none": (
            "No recent purchase orders link {product} to a supplier. Open "
            "Purchase Orders or Suppliers to check the full record."
        ),
        "supplier_for_header": (
            "Supplier(s) linked to {product} in recent purchase orders: "
            "{suppliers}."
        ),
        "doc_from": "From {source} — {title}:",
        "not_rated": "not rated",
    },
    "hi": {
        "product_detail": (
            "{name} ({sku})\n"
            "- स्टॉक: {stock} इकाइयाँ\n"
            "- रीऑर्डर स्तर: {reorder_level}\n"
            "- कीमत: {price}\n"
            "- स्थिति: {status}\n\n"
            "इसे संपादित करने के लिए Products खोलें, या स्टॉक मूवमेंट दर्ज "
            "करने के लिए Inventory Operations खोलें।"
        ),
        "supplier_detail_head": (
            "{name}\n"
            "- लीड समय: {lead_time} दिन\n"
            "- प्रदर्शन रेटिंग: {rating}"
        ),
        "supplier_contact": "- संपर्क: {contact}",
        "supplier_hint": (
            "आपूर्तिकर्ता देखने या अपडेट करने के लिए Suppliers खोलें। "
            "रीऑर्डर योजना में लीड समय का उपयोग होता है।"
        ),
        "low_stock_header": "रीऑर्डर स्तर पर या उससे नीचे वाले उत्पाद:",
        "low_stock_line": (
            "- {name} ({sku}): {stock} इकाइयाँ शेष, रीऑर्डर स्तर "
            "{reorder_level}"
        ),
        "low_stock_none": (
            "अभी कोई उत्पाद रीऑर्डर स्तर पर या उससे नीचे नहीं है।"
        ),
        "more_line": "...और {count} अधिक।",
        "out_of_stock_extra": "स्टॉक खत्म ({count}): {names}",
        "forecast_hint": (
            "मांग, लीड समय और सुरक्षा स्टॉक के आधार पर सुझाई गई रीऑर्डर "
            "मात्रा के लिए Demand Forecast खोलें।"
        ),
        "out_of_stock_none": "अभी कोई उत्पाद स्टॉक खत्म नहीं है।",
        "out_of_stock_header": "{count} उत्पाद स्टॉक खत्म हैं:",
        "out_of_stock_line": (
            "- {name} ({sku}): रीऑर्डर स्तर {reorder_level}"
        ),
        "out_of_stock_hint": (
            "स्टॉक-इन मूवमेंट के लिए Inventory Operations उपयोग करें या खरीद "
            "ऑर्डर बनाएं।"
        ),
        "no_pending_sales": "अभी कोई लंबित बिक्री ऑर्डर नहीं है।",
        "pending_sales_header": "{count} लंबित बिक्री ऑर्डर।",
        "showing_latest": " नवीनतम {count} दिखाए जा रहे हैं।",
        "pending_sales_line": (
            "- ऑर्डर #{id}: {customer} — {product} × {quantity}"
        ),
        "sales_hint": (
            "ऑर्डर पुष्टि, भेजने या रद्द करने के लिए Sales Orders खोलें।"
        ),
        "no_open_purchases": "अभी कोई खुला खरीद ऑर्डर नहीं है।",
        "open_purchases_header": (
            "{count} खुले खरीद ऑर्डर (Pending, Approved या Ordered)।"
        ),
        "open_purchases_line": (
            "- PO #{id}: {supplier} — {product} × {quantity} ({status})"
        ),
        "purchases_hint": (
            "खरीद ऑर्डर स्वीकृत, ऑर्डर या प्राप्त करने के लिए Purchase "
            "Orders खोलें।"
        ),
        "count_products": "कैटलॉग में {count} उत्पाद हैं।",
        "count_suppliers": "{count} आपूर्तिकर्ता हैं।",
        "count_purchase_orders": "{count} खरीद ऑर्डर हैं।",
        "count_sales_orders": "{count} बिक्री ऑर्डर हैं।",
        "count_categories": "{count} श्रेणियाँ हैं।",
        "sales_summary_header": "बिक्री ऑर्डर: कुल {count}",
        "sales_summary_line": "- {status}: {count}",
        "sales_summary_hint": (
            "पूरी सूची और स्थिति नियंत्रण के लिए Sales Orders खोलें।"
        ),
        "no_suppliers": (
            "अभी कोई आपूर्तिकर्ता पंजीकृत नहीं है। जोड़ने के लिए Suppliers "
            "खोलें।"
        ),
        "supplier_list_header": "{count} आपूर्तिकर्ता:",
        "supplier_list_line": (
            "- {name}: लीड समय {lead_time} दिन, रेटिंग {rating}"
        ),
        "not_found_purchase": (
            "हाल के रिकॉर्ड में खरीद ऑर्डर #{id} नहीं मिला।"
        ),
        "not_found_sales": (
            "हाल के रिकॉर्ड में बिक्री ऑर्डर #{id} नहीं मिला।"
        ),
        "purchase_order_title": "खरीद ऑर्डर #{id}",
        "sales_order_title": "बिक्री ऑर्डर #{id}",
        "label_supplier": "- आपूर्तिकर्ता: {value}",
        "label_product": "- उत्पाद: {value}",
        "label_quantity": "- मात्रा: {value}",
        "label_unit_price": "- इकाई मूल्य: {value}",
        "label_total": "- कुल: {value}",
        "label_status": "- स्थिति: {value}",
        "label_customer": "- ग्राहक: {value}",
        "generic_product": "उत्पाद",
        "generic_supplier": "आपूर्तिकर्ता",
        "supplier_for_none": (
            "{product} को हाल के खरीद ऑर्डर में किसी आपूर्तिकर्ता से नहीं "
            "जोड़ा गया। पूरा रिकॉर्ड देखने के लिए Purchase Orders या "
            "Suppliers खोलें।"
        ),
        "supplier_for_header": (
            "हाल के खरीद ऑर्डर में {product} से जुड़े आपूर्तिकर्ता: "
            "{suppliers}।"
        ),
        "doc_from": "{source} — {title} से:",
        "not_rated": "रेटिंग नहीं",
    },
    "bn": {
        "product_detail": (
            "{name} ({sku})\n"
            "- স্টক: {stock} একক\n"
            "- পুনরায় অর্ডার স্তর: {reorder_level}\n"
            "- মূল্য: {price}\n"
            "- অবস্থা: {status}\n\n"
            "সম্পাদনা করতে Products খুলুন, বা স্টক মুভমেন্ট লিখতে Inventory "
            "Operations খুলুন।"
        ),
        "supplier_detail_head": (
            "{name}\n"
            "- লিড টাইম: {lead_time} দিন\n"
            "- পারফরম্যান্স রেটিং: {rating}"
        ),
        "supplier_contact": "- যোগাযোগ: {contact}",
        "supplier_hint": (
            "সরবরাহকারী দেখতে বা আপডেট করতে Suppliers খুলুন। পুনরায় অর্ডার "
            "পরিকল্পনায় লিড টাইম ব্যবহৃত হয়।"
        ),
        "low_stock_header": "পুনরায় অর্ডার স্তরে বা তার নিচে থাকা পণ্য:",
        "low_stock_line": (
            "- {name} ({sku}): {stock} একক বাকি, পুনরায় অর্ডার স্তর "
            "{reorder_level}"
        ),
        "low_stock_none": (
            "এই মুহূর্তে কোনো পণ্য পুনরায় অর্ডার স্তরে বা তার নিচে নেই।"
        ),
        "more_line": "...আরও {count}টি।",
        "out_of_stock_extra": "স্টক শেষ ({count}): {names}",
        "forecast_hint": (
            "চাহিদা, লিড টাইম ও নিরাপত্তা স্টকের ভিত্তিতে প্রস্তাবিত পুনরায় "
            "অর্ডার পরিমাণের জন্য Demand Forecast খুলুন।"
        ),
        "out_of_stock_none": "এই মুহূর্তে কোনো পণ্যের স্টক শেষ নেই।",
        "out_of_stock_header": "{count}টি পণ্যের স্টক শেষ:",
        "out_of_stock_line": (
            "- {name} ({sku}): পুনরায় অর্ডার স্তর {reorder_level}"
        ),
        "out_of_stock_hint": (
            "স্টক-ইন মুভমেন্টের জন্য Inventory Operations ব্যবহার করুন বা ক্রয় "
            "অর্ডার তৈরি করুন।"
        ),
        "no_pending_sales": "এই মুহূর্তে কোনো মুলতুবি বিক্রয় অর্ডার নেই।",
        "pending_sales_header": "{count}টি মুলতুবি বিক্রয় অর্ডার।",
        "showing_latest": " সর্বশেষ {count}টি দেখানো হচ্ছে।",
        "pending_sales_line": (
            "- অর্ডার #{id}: {customer} — {product} × {quantity}"
        ),
        "sales_hint": (
            "অর্ডার নিশ্চিত, পাঠাতে বা বাতিল করতে Sales Orders খুলুন।"
        ),
        "no_open_purchases": "এই মুহূর্তে কোনো খোলা ক্রয় অর্ডার নেই।",
        "open_purchases_header": (
            "{count}টি খোলা ক্রয় অর্ডার (Pending, Approved বা Ordered)।"
        ),
        "open_purchases_line": (
            "- PO #{id}: {supplier} — {product} × {quantity} ({status})"
        ),
        "purchases_hint": (
            "ক্রয় অর্ডার অনুমোদন, অর্ডার বা গ্রহণ করতে Purchase Orders খুলুন।"
        ),
        "count_products": "ক্যাটালগে {count}টি পণ্য আছে।",
        "count_suppliers": "{count}জন সরবরাহকারী আছে।",
        "count_purchase_orders": "{count}টি ক্রয় অর্ডার আছে।",
        "count_sales_orders": "{count}টি বিক্রয় অর্ডার আছে।",
        "count_categories": "{count}টি বিভাগ আছে।",
        "sales_summary_header": "বিক্রয় অর্ডার: মোট {count}",
        "sales_summary_line": "- {status}: {count}",
        "sales_summary_hint": (
            "সম্পূর্ণ তালিকা ও স্ট্যাটাস নিয়ন্ত্রণের জন্য Sales Orders খুলুন।"
        ),
        "no_suppliers": (
            "এখনও কোনো সরবরাহকারী নিবন্ধিত নেই। যোগ করতে Suppliers খুলুন।"
        ),
        "supplier_list_header": "{count}জন সরবরাহকারী:",
        "supplier_list_line": (
            "- {name}: লিড টাইম {lead_time} দিন, রেটিং {rating}"
        ),
        "not_found_purchase": (
            "সাম্প্রতিক রেকর্ডে ক্রয় অর্ডার #{id} পাওয়া যায়নি।"
        ),
        "not_found_sales": (
            "সাম্প্রতিক রেকর্ডে বিক্রয় অর্ডার #{id} পাওয়া যায়নি।"
        ),
        "purchase_order_title": "ক্রয় অর্ডার #{id}",
        "sales_order_title": "বিক্রয় অর্ডার #{id}",
        "label_supplier": "- সরবরাহকারী: {value}",
        "label_product": "- পণ্য: {value}",
        "label_quantity": "- পরিমাণ: {value}",
        "label_unit_price": "- একক মূল্য: {value}",
        "label_total": "- মোট: {value}",
        "label_status": "- অবস্থা: {value}",
        "label_customer": "- গ্রাহক: {value}",
        "generic_product": "পণ্য",
        "generic_supplier": "সরবরাহকারী",
        "supplier_for_none": (
            "সাম্প্রতিক ক্রয় অর্ডারে {product}-কে কোনো সরবরাহকারীর সাথে "
            "সংযুক্ত করা নেই। সম্পূর্ণ রেকর্ড দেখতে Purchase Orders বা "
            "Suppliers খুলুন।"
        ),
        "supplier_for_header": (
            "সাম্প্রতিক ক্রয় অর্ডারে {product}-এর সাথে সংযুক্ত সরবরাহকারী: "
            "{suppliers}।"
        ),
        "doc_from": "{source} — {title} থেকে:",
        "not_rated": "রেটিং নেই",
    },
}


def text(language, key: str, **values) -> str:
    code = normalize_language(language)
    template = TEXT[code].get(key) or TEXT["en"][key]
    return template.format(**values) if values else template


# ---------------------------------------------------------------------------
# Localized knowledge keywords and answers
# ---------------------------------------------------------------------------
KNOWLEDGE_KEYWORDS = {
    "hi": {
        "add-product": [
            "उत्पाद जोड़ें", "नया उत्पाद", "उत्पाद कैसे जोड़ें",
            "प्रोडक्ट जोड़ें", "उत्पाद बनाएं",
        ],
        "edit-product": [
            "उत्पाद संपादित", "उत्पाद अपडेट", "उत्पाद हटाएं",
            "उत्पाद बदलें", "प्रोडक्ट हटाएं",
        ],
        "add-category": ["श्रेणी जोड़ें", "नई श्रेणी", "कैटेगरी जोड़ें"],
        "add-supplier": [
            "आपूर्तिकर्ता जोड़ें", "नया आपूर्तिकर्ता", "विक्रेता जोड़ें",
            "सप्लायर जोड़ें",
        ],
        "stock-movement": [
            "स्टॉक इन", "स्टॉक आउट", "स्टॉक जोड़ें", "स्टॉक घटाएं",
            "इन्वेंटरी ऑपरेशन", "स्टॉक मूवमेंट",
        ],
        "create-sales-order": [
            "बिक्री ऑर्डर बनाएं", "नया बिक्री ऑर्डर", "सेल ऑर्डर",
            "बिक्री ऑर्डर कैसे",
        ],
        "sales-status": [
            "बिक्री ऑर्डर स्थिति", "ऑर्डर पुष्टि", "ऑर्डर भेजें",
            "ऑर्डर रद्द", "ऑर्डर स्थिति",
        ],
        "create-purchase-order": [
            "खरीद ऑर्डर बनाएं", "नया खरीद ऑर्डर", "पर्चेज ऑर्डर",
            "खरीद ऑर्डर कैसे",
        ],
        "purchase-status": [
            "खरीद ऑर्डर स्थिति", "ऑर्डर स्वीकृत", "स्टॉक प्राप्त",
            "खरीद ऑर्डर प्राप्त", "मार्क रिसीव्ड",
        ],
        "forecast": [
            "पूर्वानुमान", "मांग पूर्वानुमान", "डिमांड फोरकास्ट",
            "रीऑर्डर सुझाव", "रीऑर्डर मात्रा",
        ],
        "dashboard": [
            "डैशबोर्ड", "स्टॉक अलर्ट", "कम स्टॉक अलर्ट", "अवलोकन",
        ],
        "login": [
            "लॉगिन", "साइन इन", "पंजीकरण", "खाता बनाएं", "पासवर्ड",
            "सत्र समाप्त",
        ],
        "permissions": ["भूमिका", "अनुमति", "एडमिन", "पहुँच", "अधिकार"],
        "navigation": [
            "नेविगेशन", "साइडबार", "पेज खोजें", "मेनू", "कहाँ है",
        ],
        "delete-rules": [
            "हटा नहीं सकते", "डिलीट ब्लॉक", "संदर्भित", "उपयोग में",
        ],
        "errors": [
            "त्रुटि", "काम नहीं कर रहा", "विफल", "लोड नहीं", "समस्या",
            "401", "422", "500",
        ],
        "assistant": [
            "तुम कौन हो", "आप क्या कर सकते हैं", "सहायक", "आपकी सीमा",
            "चैटजीपीटी",
        ],
    },
    "bn": {
        "add-product": [
            "পণ্য যোগ করুন", "নতুন পণ্য", "পণ্য কীভাবে যোগ", "পণ্য যোগ",
            "প্রোডাক্ট যোগ", "কীভাবে পণ্য যোগ",
        ],
        "edit-product": [
            "পণ্য সম্পাদনা", "পণ্য আপডেট", "পণ্য মুছুন", "পণ্য পরিবর্তন",
        ],
        "add-category": ["বিভাগ যোগ করুন", "নতুন বিভাগ", "ক্যাটাগরি যোগ"],
        "add-supplier": [
            "সরবরাহকারী যোগ করুন", "নতুন সরবরাহকারী", "বিক্রেতা যোগ",
            "সাপ্লায়ার যোগ",
        ],
        "stock-movement": [
            "স্টক ইন", "স্টক আউট", "স্টক যোগ", "স্টক কমান",
            "ইনভেন্টরি অপারেশন", "স্টক মুভমেন্ট",
        ],
        "create-sales-order": [
            "বিক্রয় অর্ডার তৈরি", "নতুন বিক্রয় অর্ডার", "সেল অর্ডার",
            "বিক্রয় অর্ডার কীভাবে",
        ],
        "sales-status": [
            "বিক্রয় অর্ডার স্ট্যাটাস", "অর্ডার নিশ্চিত", "অর্ডার পাঠান",
            "অর্ডার বাতিল", "অর্ডার স্ট্যাটাস",
        ],
        "create-purchase-order": [
            "ক্রয় অর্ডার তৈরি", "নতুন ক্রয় অর্ডার", "পারচেজ অর্ডার",
            "ক্রয় অর্ডার কীভাবে",
        ],
        "purchase-status": [
            "ক্রয় অর্ডার স্ট্যাটাস", "অর্ডার অনুমোদন", "স্টক গ্রহণ",
            "ক্রয় অর্ডার গ্রহণ", "রিসিভড করুন",
        ],
        "forecast": [
            "পূর্বাভাস", "চাহিদা পূর্বাভাস", "ডিমান্ড ফোরকাস্ট",
            "পুনরায় অর্ডার পরামর্শ", "পুনরায় অর্ডার পরিমাণ",
        ],
        "dashboard": [
            "ড্যাশবোর্ড", "স্টক সতর্কতা", "কম স্টক সতর্কতা", "ওভারভিউ",
        ],
        "login": [
            "লগইন", "সাইন ইন", "নিবন্ধন", "অ্যাকাউন্ট তৈরি", "পাসওয়ার্ড",
            "সেশন শেষ",
        ],
        "permissions": ["ভূমিকা", "অনুমতি", "অ্যাডমিন", "অ্যাক্সেস", "অধিকার"],
        "navigation": [
            "নেভিগেশন", "সাইডবার", "পেজ খুঁজুন", "মেনু", "কোথায়",
        ],
        "delete-rules": [
            "মুছে ফেলা যাবে না", "ডিলিট ব্লক", "উল্লেখিত", "ব্যবহারে",
        ],
        "errors": [
            "ত্রুটি", "কাজ করছে না", "ব্যর্থ", "লোড হচ্ছে না", "সমস্যা",
            "401", "422", "500",
        ],
        "assistant": [
            "তুমি কে", "আপনি কী করতে পারেন", "সহায়ক", "আপনার সীমা",
            "চ্যাটজিপিটি",
        ],
    },
}

KNOWLEDGE_ANSWERS = {
    "hi": {
        "add-product": (
            "उत्पाद जोड़ने के लिए:\n"
            "1. साइडबार से Products खोलें।\n"
            "2. Add Product चुनें।\n"
            "3. उत्पाद का नाम, SKU और कीमत दर्ज करें।\n"
            "4. वैकल्पिक रूप से प्रारंभिक स्टॉक, रीऑर्डर स्तर और श्रेणी सेट करें।\n"
            "5. उत्पाद सहेजें।\n\n"
            "SKU अद्वितीय होना चाहिए। स्टॉक और रीऑर्डर स्तर ऋणात्मक नहीं हो "
            "सकते।"
        ),
        "edit-product": (
            "Products खोलें, तालिका में उत्पाद खोजें और Edit या Delete का उपयोग "
            "करें। यदि बिक्री या खरीद ऑर्डर उत्पाद का संदर्भ देते हैं तो हटाना "
            "रोका जाता है, ताकि इतिहास सुरक्षित रहे। इतिहास खोए बिना बिक्री "
            "रोकने के लिए उत्पाद रखें और उसका स्टॉक शून्य कर दें।"
        ),
        "add-category": (
            "Categories खोलें और Add Category चुनें। अद्वितीय नाम और वैकल्पिक "
            "विवरण दर्ज करें, फिर सहेजें। जब तक उत्पाद किसी श्रेणी से जुड़े हैं, "
            "उसे हटाया नहीं जा सकता।"
        ),
        "add-supplier": (
            "Suppliers खोलें और Add Supplier चुनें। आपूर्तिकर्ता का नाम दर्ज "
            "करें, फिर वैकल्पिक रूप से ईमेल, फ़ोन, पता, लीड समय (दिनों में) और "
            "0 से 5 तक प्रदर्शन रेटिंग जोड़ें। सहेजें।\n\n"
            "मांग पूर्वानुमान सुझाए गए रीऑर्डर की गणना में लीड समय का उपयोग "
            "करता है।"
        ),
        "stock-movement": (
            "साइडबार से Inventory Operations खोलें।\n"
            "1. Stock In या Stock Out चुनें।\n"
            "2. उत्पाद चुनें।\n"
            "3. शून्य से बड़ी पूर्ण संख्या दर्ज करें।\n"
            "4. छोटा कारण जोड़ें, जैसे 'New shipment' या 'Damaged goods'।\n"
            "5. Record Stock Movement चुनें।\n\n"
            "यदि मात्रा उपलब्ध स्टॉक से अधिक है तो Stock Out अस्वीकार होता है। "
            "हर सफल मूवमेंट स्टॉक इतिहास में दर्ज होता है।"
        ),
        "create-sales-order": (
            "Sales Orders खोलें और ऑर्डर फ़ॉर्म का उपयोग करें। उत्पाद चुनें, "
            "ग्राहक का नाम और पूर्ण मात्रा दर्ज करें, फिर सबमिट करें।\n\n"
            "ऑर्डर बनते ही स्टॉक घट जाता है। ऑर्डर Pending से शुरू होता है। "
            "स्टॉक अपर्याप्त होने पर ऑर्डर अस्वीकार होता है।"
        ),
        "sales-status": (
            "बिक्री ऑर्डर प्रवाह: Pending -> Confirmed -> Shipped -> "
            "Delivered.\n"
            "- Pending या Confirmed ऑर्डर रद्द किए जा सकते हैं।\n"
            "- रद्द करने पर आरक्षित स्टॉक ठीक एक बार बहाल होता है।\n"
            "- Delivered और Cancelled अंतिम स्थितियाँ हैं।\n"
            "- बिक्री ऑर्डर इतिहास हटाया नहीं जा सकता।\n\n"
            "ऑर्डर आगे बढ़ाने के लिए Sales Orders पेज का स्थिति नियंत्रण उपयोग "
            "करें।"
        ),
        "create-purchase-order": (
            "Purchase Orders खोलें और ऑर्डर फ़ॉर्म का उपयोग करें। आपूर्तिकर्ता "
            "और उत्पाद चुनें, मात्रा और इकाई मूल्य दर्ज करें, फिर सबमिट करें।\n\n"
            "खरीद ऑर्डर Pending से शुरू होता है और अभी स्टॉक नहीं बदलता। स्टॉक "
            "तभी जुड़ता है जब ऑर्डर Received होता है।"
        ),
        "purchase-status": (
            "खरीद ऑर्डर प्रवाह: Pending -> Approved -> Ordered -> Received.\n"
            "- Approved ऑर्डर सीधे Received भी किया जा सकता है।\n"
            "- Pending, Approved या Ordered ऑर्डर रद्द किए जा सकते हैं।\n"
            "- Receive करने पर ऑर्डर की मात्रा ठीक एक बार स्टॉक में जुड़ती है।\n"
            "- Received और Cancelled अंतिम स्थितियाँ हैं।\n\n"
            "Receive दोहराने पर स्टॉक दोबारा नहीं जुड़ता।"
        ),
        "forecast": (
            "साइडबार से Demand Forecast खोलें:\n"
            "- प्रशिक्षित उत्पादों के लिए 7-दिन की मांग दृष्टि।\n"
            "- पूर्वानुमानित मांग, लीड समय, सुरक्षा स्टॉक और वर्तमान इन्वेंटरी "
            "के आधार पर सुझाई गई रीऑर्डर मात्रा।\n"
            "- लीड समय समाप्त होने से पहले ऑर्डर करने योग्य तत्काल वस्तुएँ।\n\n"
            "तालिका केंद्रित करने के लिए All / Needs reorder फ़िल्टर उपयोग करें, "
            "और Refresh forecast से पुनः लोड करें। पूर्वानुमान केवल योजना सहायता "
            "है; ऑर्डर से पहले आपूर्तिकर्ता और स्टॉक विवरण जाँचें।"
        ),
        "dashboard": (
            "Dashboard कुल उत्पाद, उपलब्ध इकाइयाँ, कम-स्टॉक और स्टॉक-खत्म "
            "संख्या, बिक्री और खरीद ऑर्डर सारांश, हाल की गतिविधि और 3D स्टॉक "
            "स्नैपशॉट दिखाता है।\n\n"
            "कोई उत्पाद कम स्टॉक तब होता है जब मात्रा शून्य से अधिक लेकिन "
            "रीऑर्डर स्तर पर या उससे कम हो। स्टॉक खत्म का अर्थ मात्रा शून्य है। "
            "3D दृश्य वैकल्पिक है; लोड न होने पर भी बाकी डैशबोर्ड काम करता है।"
        ),
        "login": (
            "अपने उपयोगकर्ता नाम और पासवर्ड से साइन इन करें। Create an account "
            "लिंक से नया खाता बनाया जा सकता है।\n\n"
            "- उपयोगकर्ता नाम केस-असंवेदनशील हैं और अक्षर, संख्या, बिंदु, "
            "अंडरस्कोर और हाइफ़न ले सकते हैं।\n"
            "- पंजीकरण पासवर्ड कम से कम 12 अक्षरों का होना चाहिए।\n"
            "- सत्र 30 मिनट तक चलता है। समाप्त होने पर दोबारा साइन इन करें।\n\n"
            "इस बिल्ड में स्वयं पासवर्ड रीसेट नहीं है। साइन इन न कर पाने पर "
            "अपने डिप्लॉयमेंट प्रबंधक से संपर्क करें। चैट में अपना पासवर्ड साझा "
            "न करें।"
        ),
        "permissions": (
            "सभी पंजीकृत खातों के पास वर्तमान में समान अनुमतियाँ हैं। इस बिल्ड "
            "में अलग प्रशासक भूमिका या भूमिका-आधारित पहुँच नियंत्रण नहीं है। हर "
            "संरक्षित पेज के लिए वैध साइन-इन सत्र आवश्यक है।"
        ),
        "navigation": (
            "साइडबार से Dashboard, Demand Forecast, Products, Inventory "
            "Operations, Categories, Suppliers, Sales Orders और Purchase Orders "
            "खोलें।\n\n"
            "डेस्कटॉप पर हेडर में Jump to module खोज पेजों को नाम या कीवर्ड से "
            "ढूँढती है, जैसे 'stock', 'orders' या 'vendors'। मोबाइल पर वही पेज "
            "खोलने के लिए मेनू बटन दबाएँ।"
        ),
        "delete-rules": (
            "NextGenERP इतिहास और संबंधों की रक्षा करता है:\n"
            "- जब तक ऑर्डर या खरीद ऑर्डर उत्पाद का उपयोग करते हैं, उत्पाद हटाया "
            "नहीं जा सकता।\n"
            "- जब तक उत्पाद किसी श्रेणी में हैं, श्रेणी हटाई नहीं जा सकती।\n"
            "- जब तक खरीद ऑर्डर आपूर्तिकर्ता का संदर्भ देते हैं, आपूर्तिकर्ता "
            "हटाया नहीं जा सकता।\n"
            "- बिक्री ऑर्डर इतिहास बिल्कुल हटाया नहीं जा सकता।\n\n"
            "ये नियम इन्वेंटरी और ऑर्डर रिकॉर्ड सुसंगत रखते हैं।"
        ),
        "errors": (
            "त्वरित जाँच:\n"
            "- यदि डेटा लोड नहीं होता, तो पुष्टि करें कि बैकएंड चल रहा है और "
            "API पर /health खोलें; उसे status ok लौटाना चाहिए।\n"
            "- यदि अचानक साइन आउट हो गए, तो 30 मिनट का सत्र समाप्त हुआ। दोबारा "
            "साइन इन करें।\n"
            "- 422 आमतौर पर बताता है कि कोई आवश्यक फ़ील्ड गायब या अमान्य है।\n"
            "- 409 का अर्थ है कि क्रिया मौजूदा रिकॉर्ड से टकराती है, जैसे खरीद "
            "ऑर्डर वाले आपूर्तिकर्ता को हटाना।\n"
            "- यदि डैशबोर्ड का एक भाग विफल हो, तो बाकी भाग लोड रहते हैं; "
            "रीफ़्रेश के लिए Try again दबाएँ।"
        ),
        "assistant": (
            "मैं NextGenERP सहायक हूँ। मैं ऐप कैसे काम करता है यह समझा सकता हूँ "
            "और लाइव वर्कस्पेस डेटा से उत्तर दे सकता हूँ: स्टॉक स्तर, कम-स्टॉक "
            "वस्तुएँ, लंबित ऑर्डर, आपूर्तिकर्ता, उत्पाद कीमतें और रीऑर्डर "
            "आवश्यकताएँ।\n\n"
            "मैं केवल पढ़ सकता हूँ: रिकॉर्ड बना, बदल, रद्द या हटा नहीं सकता। "
            "बदलाव के लिए संबंधित पेज उपयोग करें। मैं केवल NextGenERP प्रश्नों "
            "का उत्तर देता हूँ।"
        ),
    },
    "bn": {
        "add-product": (
            "একটি পণ্য যোগ করতে:\n"
            "1. সাইডবার থেকে Products খুলুন।\n"
            "2. Add Product নির্বাচন করুন।\n"
            "3. পণ্যের নাম, SKU এবং মূল্য লিখুন।\n"
            "4. ঐচ্ছিকভাবে প্রারম্ভিক স্টক, পুনরায় অর্ডার স্তর এবং বিভাগ সেট "
            "করুন।\n"
            "5. পণ্য সংরক্ষণ করুন।\n\n"
            "SKU অবশ্যই অনন্য হতে হবে। স্টক এবং পুনরায় অর্ডার স্তর ঋণাত্মক হতে "
            "পারবে না।"
        ),
        "edit-product": (
            "Products খুলুন, টেবিলে পণ্যটি খুঁজুন এবং Edit বা Delete ব্যবহার "
            "করুন। বিক্রয় বা ক্রয় অর্ডার পণ্যটি উল্লেখ করলে মুছে ফেলা বন্ধ "
            "থাকে, যাতে ইতিহাস অক্ষত থাকে। ইতিহাস না হারিয়ে বিক্রয় বন্ধ করতে "
            "পণ্যটি রেখে স্টক শূন্য করুন।"
        ),
        "add-category": (
            "Categories খুলুন এবং Add Category নির্বাচন করুন। অনন্য নাম এবং "
            "ঐচ্ছিক বিবরণ লিখে সংরক্ষণ করুন। কোনো বিভাগে পণ্য থাকা পর্যন্ত তা "
            "মুছে ফেলা যাবে না।"
        ),
        "add-supplier": (
            "Suppliers খুলুন এবং Add Supplier নির্বাচন করুন। সরবরাহকারীর নাম "
            "লিখুন, তারপর ঐচ্ছিকভাবে ইমেল, ফোন, ঠিকানা, লিড টাইম (দিনে) এবং 0 "
            "থেকে 5 পর্যন্ত পারফরম্যান্স রেটিং যোগ করুন। সংরক্ষণ করুন।\n\n"
            "চাহিদা পূর্বাভাস প্রস্তাবিত পুনরায় অর্ডার গণনায় লিড টাইম ব্যবহার "
            "করে।"
        ),
        "stock-movement": (
            "সাইডবার থেকে Inventory Operations খুলুন।\n"
            "1. Stock In বা Stock Out নির্বাচন করুন।\n"
            "2. পণ্য নির্বাচন করুন।\n"
            "3. শূন্যের চেয়ে বড় পূর্ণ সংখ্যা লিখুন।\n"
            "4. সংক্ষিপ্ত কারণ যোগ করুন, যেমন 'New shipment' বা 'Damaged goods'।\n"
            "5. Record Stock Movement নির্বাচন করুন।\n\n"
            "পরিমাণ উপলব্ধ স্টকের বেশি হলে Stock Out প্রত্যাখ্যাত হয়। প্রতিটি "
            "সফল মুভমেন্ট স্টক ইতিহাসে লেখা হয়।"
        ),
        "create-sales-order": (
            "Sales Orders খুলুন এবং অর্ডার ফর্ম ব্যবহার করুন। পণ্য নির্বাচন করুন, "
            "গ্রাহকের নাম ও পূর্ণ পরিমাণ লিখে সাবমিট করুন।\n\n"
            "অর্ডার তৈরি হলে স্টক সঙ্গে সঙ্গে কমে। অর্ডার Pending হিসেবে শুরু "
            "হয়। স্টক অপর্যাপ্ত হলে অর্ডার প্রত্যাখ্যাত হয়।"
        ),
        "sales-status": (
            "বিক্রয় অর্ডার প্রবাহ: Pending -> Confirmed -> Shipped -> "
            "Delivered।\n"
            "- Pending বা Confirmed অর্ডার বাতিল করা যায়।\n"
            "- বাতিল করলে সংরক্ষিত স্টক ঠিক একবার ফিরে আসে।\n"
            "- Delivered এবং Cancelled চূড়ান্ত অবস্থা।\n"
            "- বিক্রয় অর্ডার ইতিহাস মুছে ফেলা যায় না।\n\n"
            "অর্ডার এগিয়ে নিতে Sales Orders পেজের স্ট্যাটাস নিয়ন্ত্রণ ব্যবহার "
            "করুন।"
        ),
        "create-purchase-order": (
            "Purchase Orders খুলুন এবং অর্ডার ফর্ম ব্যবহার করুন। সরবরাহকারী ও "
            "পণ্য নির্বাচন করুন, পরিমাণ ও একক মূল্য লিখে সাবমিট করুন।\n\n"
            "ক্রয় অর্ডার Pending হিসেবে শুরু হয় এবং এখনই স্টক বদলায় না। অর্ডার "
            "Received হলে তবেই স্টক যোগ হয়।"
        ),
        "purchase-status": (
            "ক্রয় অর্ডার প্রবাহ: Pending -> Approved -> Ordered -> Received।\n"
            "- Approved অর্ডার সরাসরি Received-ও করা যায়।\n"
            "- Pending, Approved বা Ordered অর্ডার বাতিল করা যায়।\n"
            "- Receive করলে অর্ডারের পরিমাণ ঠিক একবার স্টকে যোগ হয়।\n"
            "- Received এবং Cancelled চূড়ান্ত অবস্থা।\n\n"
            "Receive পুনরাবৃত্তি করলে স্টক দ্বিতীয়বার যোগ হয় না।"
        ),
        "forecast": (
            "সাইডবার থেকে Demand Forecast খুলুন:\n"
            "- প্রশিক্ষিত পণ্যের জন্য ৭ দিনের চাহিদা পূর্বাভাস।\n"
            "- পূর্বাভাসিত চাহিদা, লিড টাইম, নিরাপত্তা স্টক এবং বর্তমান "
            "ইনভেন্টরির ভিত্তিতে প্রস্তাবিত পুনরায় অর্ডার পরিমাণ।\n"
            "- লিড টাইম শেষ হওয়ার আগে অর্ডার করা উচিত এমন জরুরি পণ্য।\n\n"
            "টেবিল ফোকাস করতে All / Needs reorder ফিল্টার ব্যবহার করুন এবং "
            "Refresh forecast দিয়ে পুনরায় লোড করুন। পূর্বাভাস শুধু পরিকল্পনা "
            "সহায়ক; অর্ডারের আগে সরবরাহকারী ও স্টকের বিবরণ যাচাই করুন।"
        ),
        "dashboard": (
            "Dashboard মোট পণ্য, হাতে থাকা একক, কম-স্টক ও স্টক-শেষ সংখ্যা, "
            "বিক্রয় ও ক্রয় অর্ডার সারাংশ, সাম্প্রতিক কার্যকলাপ এবং 3D স্টক "
            "স্ন্যাপশট দেখায়।\n\n"
            "কোনো পণ্যের পরিমাণ শূন্যের বেশি কিন্তু পুনরায় অর্ডার স্তরে বা তার "
            "নিচে হলে সেটি কম স্টক। স্টক শেষ মানে পরিমাণ শূন্য। 3D দৃশ্য "
            "ঐচ্ছিক; লোড না হলেও বাকি ড্যাশবোর্ড কাজ করে।"
        ),
        "login": (
            "আপনার ব্যবহারকারীর নাম ও পাসওয়ার্ড দিয়ে সাইন ইন করুন। Create an "
            "account লিংক থেকে নতুন অ্যাকাউন্ট তৈরি করা যায়।\n\n"
            "- ব্যবহারকারীর নাম কেস-সংবেদনশীল নয় এবং অক্ষর, সংখ্যা, ডট, "
            "আন্ডারস্কোর ও হাইফেন ব্যবহার করতে পারে।\n"
            "- নিবন্ধন পাসওয়ার্ড অন্তত ১২ অক্ষরের হতে হবে।\n"
            "- সেশন ৩০ মিনিট স্থায়ী হয়। মেয়াদ শেষ হলে আবার সাইন ইন করুন।\n\n"
            "এই বিল্ডে স্ব-পরিষেবা পাসওয়ার্ড রিসেট নেই। সাইন ইন করতে না পারলে "
            "আপনার ডিপ্লয়মেন্ট পরিচালকের সাথে যোগাযোগ করুন। চ্যাটে পাসওয়ার্ড "
            "শেয়ার করবেন না।"
        ),
        "permissions": (
            "বর্তমানে সব নিবন্ধিত অ্যাকাউন্টের সমান অনুমতি রয়েছে। এই বিল্ডে "
            "আলাদা প্রশাসক ভূমিকা বা ভূমিকা-ভিত্তিক অ্যাক্সেস নিয়ন্ত্রণ নেই। "
            "প্রতিটি সুরক্ষিত পেজের জন্য বৈধ সাইন-ইন সেশন প্রয়োজন।"
        ),
        "navigation": (
            "সাইডবার থেকে Dashboard, Demand Forecast, Products, Inventory "
            "Operations, Categories, Suppliers, Sales Orders এবং Purchase Orders "
            "খুলুন।\n\n"
            "ডেস্কটপে হেডারের Jump to module অনুসন্ধান নাম বা কীওয়ার্ড দিয়ে পেজ "
            "খুঁজে দেয়, যেমন 'stock', 'orders' বা 'vendors'। মোবাইলে একই পেজ "
            "খুলতে মেনু বোতাম চাপুন।"
        ),
        "delete-rules": (
            "NextGenERP ইতিহাস ও সম্পর্ক রক্ষা করে:\n"
            "- অর্ডার বা ক্রয় অর্ডার পণ্যটি ব্যবহার করলে পণ্য মুছে ফেলা যায় না।\n"
            "- কোনো বিভাগে পণ্য থাকলে বিভাগ মুছে ফেলা যায় না।\n"
            "- ক্রয় অর্ডার সরবরাহকারীকে উল্লেখ করলে সরবরাহকারী মুছে ফেলা যায় "
            "না।\n"
            "- বিক্রয় অর্ডার ইতিহাস একেবারেই মুছে ফেলা যায় না।\n\n"
            "এই নিয়মগুলি ইনভেন্টরি ও অর্ডার রেকর্ড সামঞ্জস্যপূর্ণ রাখে।"
        ),
        "errors": (
            "দ্রুত পরীক্ষা:\n"
            "- ডেটা লোড না হলে নিশ্চিত করুন ব্যাকএন্ড চলছে এবং API-তে /health "
            "খুলুন; এটি status ok ফেরত দেবে।\n"
            "- হঠাৎ সাইন আউট হলে ৩০ মিনিটের সেশন শেষ হয়েছে। আবার সাইন ইন করুন।\n"
            "- 422 সাধারণত বোঝায় কোনো প্রয়োজনীয় ফিল্ড অনুপস্থিত বা অবৈধ।\n"
            "- 409 মানে কাজটি বিদ্যমান রেকর্ডের সাথে সংঘর্ষ করছে, যেমন ক্রয় "
            "অর্ডার থাকা সরবরাহকারী মুছে ফেলা।\n"
            "- ড্যাশবোর্ডের একটি অংশ ব্যর্থ হলেও বাকি অংশ লোড থাকে; রিফ্রেশ করতে "
            "Try again চাপুন।"
        ),
        "assistant": (
            "আমি NextGenERP সহায়ক। আমি অ্যাপটি কীভাবে কাজ করে তা ব্যাখ্যা করতে "
            "পারি এবং লাইভ ওয়ার্কস্পেস ডেটা থেকে উত্তর দিতে পারি: স্টক স্তর, "
            "কম-স্টক পণ্য, মুলতুবি অর্ডার, সরবরাহকারী, পণ্যের মূল্য এবং পুনরায় "
            "অর্ডারের প্রয়োজন।\n\n"
            "আমি শুধু পড়তে পারি: রেকর্ড তৈরি, সম্পাদনা, বাতিল বা মুছে ফেলতে পারি "
            "না। পরিবর্তনের জন্য সংশ্লিষ্ট পেজ ব্যবহার করুন। আমি শুধু NextGenERP "
            "প্রশ্নের উত্তর দিই।"
        ),
    },
}


def localized_keywords(entry_id: str, language) -> list[str]:
    code = normalize_language(language)
    if code == "en":
        return []
    return list(KNOWLEDGE_KEYWORDS.get(code, {}).get(entry_id, []))


def knowledge_answer(entry: dict, language) -> str:
    code = normalize_language(language)
    if code == "en":
        return entry["answer"]
    return KNOWLEDGE_ANSWERS.get(code, {}).get(entry["id"], entry["answer"])


# ---------------------------------------------------------------------------
# LLM instruction
# ---------------------------------------------------------------------------
def llm_language_instruction(language) -> str:
    code = normalize_language(language)
    if code == "en":
        return "Respond in English."
    meta = LANGUAGES[code]
    return (
        f"Respond only in {meta['llm_name']}. Keep product names, SKUs, order "
        "numbers and status values exactly as they appear in the workspace "
        "data. Do not answer in English unless the user explicitly asks for a "
        "translation."
    )
