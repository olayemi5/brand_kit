import frappe
from brand_kit.brand_kit.fields import ensure_brand_settings_doctype
from brand_kit.brand_kit.apply import apply_all_branding


def after_migrate():
    """Runs automatically after every bench migrate."""
    from brand_kit.brand_kit.fields import ensure_brand_settings_doctype
    ensure_brand_settings_doctype()
    
    # Also reapply branding in case anything was reset
    try:
        brand = frappe.get_single("Brand Settings")
        if brand.brand_name:
            from brand_kit.brand_kit.apply import apply_all_branding
            apply_all_branding(brand)
    except Exception:
        pass



def setup_brand_kit():
    """
    Run once to set up Brand Kit.
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


def sync_branding_if_changed():
    """
    Runs every minute via scheduler.
    Checks if Brand Settings has been modified recently and applies if so.
    This ensures branding is always applied even if doc_events hook misses.
    """
    try:
        # Check if Brand Settings was modified in the last 2 minutes
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
        # tabBrand Settings won't exist on first run — silently ignore
        pass
