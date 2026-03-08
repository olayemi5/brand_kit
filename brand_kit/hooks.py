app_name = "brand_kit"
app_title = "Brand Kit"
app_publisher = "Stephen Olayemi"
app_description = "Centralized branding for Frappe/ERPNext"
app_email = "olayemistephen007@gmail.com"
app_license = "mit"

after_install = "brand_kit.tasks.after_install"
after_migrate = "brand_kit.tasks.after_migrate"

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

boot_session = "brand_kit.brand_kit.apply.get_boot_info"

# Override ERPNext default mail footer
default_mail_footer = ""

# Expose brand logo method to all Jinja/email templates
jinja = {
    "methods": [
        "brand_kit.brand_kit.apply.get_brand_logo_for_email",
        "brand_kit.brand_kit.apply.get_brand_footer"
    ]
}
