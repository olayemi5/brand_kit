import frappe
from brand_kit.brand_kit.fields import ensure_brand_settings_doctype
from brand_kit.brand_kit.apply import apply_all_branding


def _replace_splash_image():
    """Replace Frappe default splash with brand logo after every migrate."""
    try:
        import os, shutil
        logo = frappe.db.get_single_value("Brand Settings", "logo")
        if not logo:
            return

        site_path = frappe.get_site_path("public", logo.lstrip("/"))
        frappe_splash = frappe.get_app_path("frappe", "public", "images", "frappe-framework-logo.png")

        if os.path.exists(site_path) and os.path.exists(os.path.dirname(frappe_splash)):
            shutil.copy(site_path, frappe_splash)
            print("[Brand Kit] Replaced Frappe splash image with brand logo.")
        else:
            print(f"[Brand Kit] Splash image not found at {site_path}")
    except Exception as e:
        frappe.log_error(title="Brand Kit: Splash Image", message=str(e))


def after_install():
    """
    Runs automatically after bench install-app brand_kit.
    Zero manual setup needed.
    """
    ensure_brand_settings_doctype()
    print("[Brand Kit] Installation complete. Go to Brand Settings to configure your brand.")


def after_migrate():
    """Runs automatically after every bench migrate."""
    ensure_brand_settings_doctype()

    # Replace Frappe splash image with brand logo
    _replace_splash_image()

    # Reapply branding in case anything was reset
    try:
        brand = frappe.get_single("Brand Settings")
        if brand.brand_name:
            apply_all_branding(brand)
    except Exception:
        pass


def setup_brand_kit():
    """
    Run once to set up Brand Kit manually if needed.
    Usage:
        bench --site your-site execute brand_kit.tasks.setup_brand_kit
    """
    ensure_brand_settings_doctype()
    print("[Brand Kit] Setup complete. Go to Brand Settings to configure.")


def reapply_branding():
    """
    Manually re-trigger branding application.
    Usage:
        bench --site your-site execute brand_kit.tasks.reapply_branding
    """
    ensure_brand_settings_doctype()
    brand = frappe.get_single("Brand Settings")
    apply_all_branding(brand)
    _replace_splash_image()


def sync_branding_if_changed():
    """
    Runs every minute via scheduler.
    Ensures branding is always applied even if doc_events hook misses.
    """
    try:
        result = frappe.db.sql(
            """SELECT modified FROM `tabBrand Settings`
               WHERE TIMESTAMPDIFF(SECOND, modified, NOW()) < 120
               LIMIT 1"""
        )
        if result:
            brand = frappe.get_single("Brand Settings")
            apply_all_branding(brand)
            print("[Brand Kit] Synced branding from scheduler.")
    except Exception:
        pass
