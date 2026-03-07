import frappe
import json


def get_brand():
    """Fetch Brand Settings values safely."""
    try:
        return frappe.get_single("Brand Settings")
    except Exception as e:
        print(f"[Brand Kit] Could not load Brand Settings: {e}")
        return None


# ─────────────────────────────────────────────
# 1. System Settings — name, logo, favicon
# ─────────────────────────────────────────────

def _upsert_single(doctype, field, value):
    """Insert or update a value in tabSingles — works whether the row exists or not."""
    frappe.db.sql(
        """INSERT INTO `tabSingles` (doctype, field, value)
           VALUES (%s, %s, %s)
           ON DUPLICATE KEY UPDATE value = %s""",
        (doctype, field, value, value)
    )


def apply_system_settings(brand):
    try:
        if not brand.brand_name:
            return

        name = brand.brand_name

        # Upsert all known title fields across Frappe versions
        for field in ("app_name", "head_title", "system_title"):
            _upsert_single("System Settings", field, name)

        for field in ("app_name", "title_prefix", "home_title"):
            _upsert_single("Website Settings", field, name)

        frappe.db.commit()

        # Clear all caches so change takes effect immediately for all users
        frappe.clear_cache()
        frappe.cache().flushall()

        print(f"[Brand Kit] Applied system name: {name}")
    except Exception as e:
        frappe.log_error(title="Brand Kit: System Settings", message=str(e))


# ─────────────────────────────────────────────
# 2. Website Settings — logo, favicon, footer, portal text
# ─────────────────────────────────────────────

def apply_website_settings(brand):
    try:
        ws = frappe.get_single("Website Settings")
        if brand.logo:
            ws.brand_html = f'<img src="{brand.logo}" alt="{brand.brand_name}" style="height:40px;">'
        if brand.favicon:
            ws.favicon = brand.favicon
            for dt in ("Website Settings", "System Settings"):
                frappe.db.sql(
                    """INSERT INTO `tabSingles` (doctype, field, value)
                       VALUES (%s, 'favicon', %s)
                       ON DUPLICATE KEY UPDATE value = %s""",
                    (dt, brand.favicon, brand.favicon)
                )
        if brand.brand_name:
            ws.title_prefix = brand.brand_name
        if brand.website_headline:
            ws.home_page = ws.home_page
        if brand.website_description:
            ws.description = brand.website_description
        if brand.support_email:
            ws.email = brand.support_email
        ws.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.clear_cache()
        frappe.cache().flushall()
        print("[Brand Kit] Applied website settings.")
    except Exception as e:
        frappe.log_error(title="Brand Kit: Website Settings", message=str(e))


# ─────────────────────────────────────────────
# 3. CSS File — inject brand colors, fonts
# ─────────────────────────────────────────────

def apply_css(brand):
    try:
        font = brand.font_family or "Inter"
        font_size = brand.font_size or "14px"
        primary = brand.primary_color or "#171717"
        secondary = brand.secondary_color or "#F5F5F5"
        accent = brand.accent_color or "#4F46E5"
        text = brand.text_color or "#1A1A1A"
        custom = brand.custom_css or ""
        logo = brand.logo or ""

        css = f"""
/* ── Brand Kit Auto-generated CSS ── */
@import url('https://fonts.googleapis.com/css2?family={font.replace(' ', '+')}:wght@300;400;500;600;700&display=swap');

:root {{
    --brand-primary: {primary};
    --brand-secondary: {secondary};
    --brand-accent: {accent};
    --brand-text: {text};
    --brand-font: '{font}', sans-serif;
    --brand-font-size: {font_size};
}}

body, .frappe-app {{
    font-family: var(--brand-font) !important;
    font-size: var(--brand-font-size) !important;
    color: var(--brand-text) !important;
}}

.navbar, .navbar-brand {{
    background-color: var(--brand-primary) !important;
}}

/* ── Brand Logo in Navbar ── */
.navbar-brand img,
.navbar .brand-logo img {{
    content: url('{logo}') !important;
    height: 32px !important;
    width: auto !important;
    display: inline-block !important;
}}



.btn-primary, .btn-default.btn-primary {{
    background-color: var(--brand-primary) !important;
    border-color: var(--brand-primary) !important;
    color: #fff !important;
}}

.btn-primary:hover {{
    background-color: var(--brand-accent) !important;
    border-color: var(--brand-accent) !important;
}}

a, .indicator-pill {{
    color: var(--brand-accent) !important;
}}

.page-head {{
    background-color: var(--brand-secondary) !important;
}}

/* ── Custom CSS ── */
{custom}
"""

        import os

        # Write to site's public folder — persists without bench build
        site_path = frappe.get_site_path("public", "files", "brand.css")
        os.makedirs(os.path.dirname(site_path), exist_ok=True)
        with open(site_path, "w") as f:
            f.write(css)

        # Also write to app public folder as fallback
        app_css_path = frappe.get_app_path("brand_kit", "public", "css", "brand.css")
        os.makedirs(os.path.dirname(app_css_path), exist_ok=True)
        with open(app_css_path, "w") as f:
            f.write(css)

        # Inject CSS directly into Website Settings head_html so it always loads
        frappe.db.sql(
            """INSERT INTO `tabSingles` (doctype, field, value)
               VALUES ('Website Settings', 'head_html', %s)
               ON DUPLICATE KEY UPDATE value = %s""",
            (f"<style>{css}</style>", f"<style>{css}</style>")
        )
        frappe.db.commit()
        frappe.clear_cache()
        frappe.cache().flushall()

        print("[Brand Kit] Applied CSS theme.")
    except Exception as e:
        frappe.log_error(title="Brand Kit: CSS", message=str(e))


# ─────────────────────────────────────────────
# 4. Letterhead — create or update default letterhead
# ─────────────────────────────────────────────

def apply_letterhead(brand):
    try:
        logo = brand.email_logo or brand.logo or ""
        name = brand.brand_name or "Company"
        primary = brand.print_primary_color or brand.primary_color or "#171717"
        address = brand.company_address or ""
        top_html = brand.letterhead_top or f"""
<div style="background:{primary};padding:16px 24px;color:#fff;display:flex;align-items:center;gap:16px;">
    {"<img src='" + logo + "' style='height:40px;'>" if logo else ""}
    <span style="font-size:20px;font-weight:600;">{name}</span>
</div>
<div style="font-size:12px;color:#555;padding:6px 24px;">{address}</div>
"""
        bottom_html = brand.letterhead_bottom or f"""
<div style="border-top:2px solid {primary};margin-top:20px;padding:10px 24px;font-size:11px;color:#888;text-align:center;">
    {name} &mdash; {address}
</div>
"""

        letterhead_name = f"{name} Letterhead"
        if frappe.db.exists("Letter Head", letterhead_name):
            lh = frappe.get_doc("Letter Head", letterhead_name)
        else:
            lh = frappe.new_doc("Letter Head")
            lh.letter_head_name = letterhead_name
            lh.is_default = 1

        lh.content = top_html
        lh.footer = bottom_html
        lh.save(ignore_permissions=True)
        print("[Brand Kit] Applied letterhead.")
    except Exception as e:
        frappe.log_error(title="Brand Kit: Letterhead", message=str(e))


# ─────────────────────────────────────────────
# 5. Email Account — sender name, footer
# ─────────────────────────────────────────────

def apply_email_settings(brand):
    try:
        # Update all outgoing email accounts with brand sender name
        accounts = frappe.get_all(
            "Email Account",
            filters={"enable_outgoing": 1},
            fields=["name"]
        )
        for acc in accounts:
            ea = frappe.get_doc("Email Account", acc["name"])
            if brand.brand_name:
                ea.sender_name = brand.brand_name
            if brand.email_footer:
                ea.append_signature = 1
                ea.signature = brand.email_footer
            ea.save(ignore_permissions=True)

        print(f"[Brand Kit] Applied email branding to {len(accounts)} account(s).")
    except Exception as e:
        frappe.log_error(title="Brand Kit: Email Settings", message=str(e))


# ─────────────────────────────────────────────
# Main Apply Function
# ─────────────────────────────────────────────

def apply_all_branding(doc, method=None):
    """
    Called automatically when Brand Settings is saved.
    Applies branding to all configured subsystems.
    """
    brand = doc  # doc is passed directly from doc_events hook

    print("[Brand Kit] Applying branding...")

    apply_system_settings(brand)
    apply_website_settings(brand)
    apply_css(brand)
    apply_letterhead(brand)
    apply_email_settings(brand)

    frappe.db.commit()
    frappe.msgprint(
        "Brand settings applied successfully across system, website, emails, and print formats.",
        title="Brand Kit",
        indicator="green"
    )
    print("[Brand Kit] Done.")
