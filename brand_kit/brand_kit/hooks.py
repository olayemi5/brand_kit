app_name = "brand_kit"
app_title = "Brand Kit"
app_publisher = "Your Company"
app_description = "Centralized branding configuration for Frappe/ERPNext"
app_version = "1.0.0"

# Auto-apply branding when Brand Settings is saved
doc_events = {
    "Brand Settings": {
        "on_update": "brand_kit.brand_kit.apply.apply_all_branding",
        "after_insert": "brand_kit.brand_kit.apply.apply_all_branding",
    }
}

# Also run every minute to catch any missed saves
scheduler_events = {
    "cron": {
        "*/1 * * * *": [
            "brand_kit.tasks.sync_branding_if_changed"
        ]
    }
}

# Inject custom CSS into every page
website_context = [
    "brand_kit.brand_kit.context.get_brand_context"
]

app_include_css = [
    "/assets/brand_kit/css/brand.css"
]
