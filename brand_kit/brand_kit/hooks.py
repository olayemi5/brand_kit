app_name = "Brand Kit"
app_title = "Brand Kit"
app_publisher = "Stephen Olayemi"
app_description = "Centralized branding configuration for Frappe/ERPNext"
app_version = "1.0.0"

# Auto-apply branding when Brand Settings is saved
doc_events = {
    "Brand Settings": {
        "on_update": "brand_kit.brand_kit.apply.apply_all_branding"
    }
}

# Inject custom CSS into every page
website_context = [
    "brand_kit.brand_kit.context.get_brand_context"
]

app_include_css = [
    "/assets/brand_kit/css/brand.css"
]
