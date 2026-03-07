app_name = "brand_kit"
app_title = "Brand Kit"
app_publisher = "Stephen Olayemi"
app_description = "Centralized branding for Frappe/ERPNext"
app_email = "olayemistephen007@gmail.com"
app_license = "mit"

doc_events = {
    "Brand Settings": {
        "on_update": "brand_kit.brand_kit.apply.apply_all_branding",
        "after_insert": "brand_kit.brand_kit.apply.apply_all_branding",
    }
}

scheduler_events = {
    "cron": {
        "*/1 * * * *": [
            "brand_kit.tasks.sync_branding_if_changed"
        ]
    }
}

app_include_css = [
    "/assets/brand_kit/css/brand.css"
]
