import frappe
from brand_kit.brand_kit.fields import ensure_brand_settings_doctype
from brand_kit.brand_kit.apply import apply_all_branding


def setup_brand_kit():
    """
    Run once to set up Brand Kit.
    Creates the Brand Settings DocType if missing.
    Also fixes existing installs where is_single was not set correctly.

    Usage:
        bench --site your-site execute brand_kit.tasks.setup_brand_kit
    """
    ensure_brand_settings_doctype()
    print("[Brand Kit] Setup complete. Go to Brand Settings in your site to configure.")


def reapply_branding():
    """
    Manually re-trigger branding application without saving the form.

    Usage:
        bench --site your-site execute brand_kit.tasks.reapply_branding
    """
    ensure_brand_settings_doctype()  # also fixes is_single if needed
    brand = frappe.get_single("Brand Settings")
    apply_all_branding(brand)
