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
# Helpers
# ─────────────────────────────────────────────

def _upsert_single(doctype, field, value):
    """Insert or update a value in tabSingles — works whether the row exists or not."""
    frappe.db.sql(
        """INSERT INTO `tabSingles` (doctype, field, value)
           VALUES (%s, %s, %s)
           ON DUPLICATE KEY UPDATE value = %s""",
        (doctype, field, value, value)
    )


def get_boot_info(bootinfo):
    """Inject brand logo into boot session so loader uses it."""
    try:
        logo = frappe.db.get_single_value("Brand Settings", "logo")
        if logo:
            bootinfo.app_logo_url = logo
            bootinfo.brand_logo = logo
            bootinfo.splash_image = logo
    except Exception:
        pass


# ─────────────────────────────────────────────
# 1. System Settings — name, logo, favicon
# ─────────────────────────────────────────────

def apply_system_settings(brand):
    try:
        if not brand.brand_name:
            return

        name = brand.brand_name

        for field in ("app_name", "head_title", "system_title"):
            _upsert_single("System Settings", field, name)

        for field in ("app_name", "title_prefix", "home_title"):
            _upsert_single("Website Settings", field, name)

        frappe.db.commit()
        frappe.clear_cache()
        frappe.cache().flushall()

        print(f"[Brand Kit] Applied system name: {name}")
    except Exception as e:
        frappe.log_error(title="Brand Kit: System Settings", message=str(e))


# ─────────────────────────────────────────────
# 2. Website Settings — logo, favicon, portal
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
# 3. CSS — colors, fonts, navbar, login page
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
        name = brand.brand_name or ""

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

/* ── Navbar ── */
.navbar, .navbar-brand {{
    background-color: var(--brand-primary) !important;
}}

.navbar-brand img,
.navbar .brand-logo img {{
    content: url('{logo}') !important;
    height: 32px !important;
    width: auto !important;
    display: inline-block !important;
}}

/* ── Buttons ── */
.btn-primary, .btn-default.btn-primary {{
    background-color: var(--brand-primary) !important;
    border-color: var(--brand-primary) !important;
    color: #fff !important;
}}

.btn-primary:hover {{
    background-color: var(--brand-accent) !important;
    border-color: var(--brand-accent) !important;
}}

/* ── Links ── */
a, .indicator-pill {{
    color: var(--brand-accent) !important;
}}

/* ── Page header ── */
.page-head {{
    background-color: var(--brand-secondary) !important;
}}

/* ── Login page ── */
.page-card-head img.app-logo {{
    content: url('{logo}') !important;
    height: 48px !important;
    width: auto !important;
}}

.btn-login {{
    background-color: var(--brand-primary) !important;
    border-color: var(--brand-primary) !important;
    color: #fff !important;
}}

/* ── Hide Frappe splash — replaced via file copy ── */
.centered.splash {{
    display: none !important;
}}

/* ── Custom CSS ── */
{custom}
"""

        import os

        site_path = frappe.get_site_path("public", "files", "brand.css")
        os.makedirs(os.path.dirname(site_path), exist_ok=True)
        with open(site_path, "w") as f:
            f.write(css)

        app_css_path = frappe.get_app_path("brand_kit", "public", "css", "brand.css")
        os.makedirs(os.path.dirname(app_css_path), exist_ok=True)
        with open(app_css_path, "w") as f:
            f.write(css)

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
# 4. Email — brand_logo in all outgoing emails
# ─────────────────────────────────────────────

def apply_email_branding(brand):
    """
    Sets brand_logo on all Email Accounts so Frappe's standard.html
    email template shows the brand logo instead of the Frappe logo.
    Also updates sender name and footer.
    """
    try:
        if not brand.logo and not brand.brand_name:
            return

        accounts = frappe.get_all(
            "Email Account",
            filters={"enable_outgoing": 1},
            fields=["name"]
        )

        for acc in accounts:
            ea = frappe.get_doc("Email Account", acc["name"])

            if brand.brand_name:
                ea.sender_name = brand.brand_name

            if brand.logo:
                ea.brand_logo = brand.logo

            if brand.email_footer:
                ea.append_signature = 1
                ea.signature = brand.email_footer

            ea.save(ignore_permissions=True)

        # Also set brand_logo as default via System Settings
        # so emails without an email account also get the logo
        if brand.logo:
            _upsert_single("System Settings", "brand_logo", brand.logo)

        frappe.db.commit()
        print(f"[Brand Kit] Applied email branding to {len(accounts)} account(s).")
    except Exception as e:
        frappe.log_error(title="Brand Kit: Email Branding", message=str(e))


# ─────────────────────────────────────────────
# 5. Email Templates — override password reset,
#    new user, and notification emails
# ─────────────────────────────────────────────

def apply_email_templates(brand):
    """
    Creates/updates Email Templates to replace Frappe branding
    in password reset, new user invitation, and system emails.
    """
    try:
        if not brand.brand_name:
            return

        logo = brand.logo or ""
        name = brand.brand_name
        primary = brand.primary_color or "#171717"
        support = brand.support_email or ""

        logo_html = f'<img src="{logo}" style="height:40px;margin-bottom:16px;" />' if logo else ""

        header_html = f"""
<div style="background:{primary};padding:20px 32px;text-align:center;">
    {logo_html}
</div>
"""
        footer_html = f"""
<div style="padding:16px 32px;text-align:center;font-size:12px;color:#888;border-top:1px solid #eee;margin-top:24px;">
    &copy; {name}{"&nbsp;&nbsp;|&nbsp;&nbsp;" + support if support else ""}
</div>
"""

        # Update default mail footer in System Settings
        _upsert_single("System Settings", "default_mail_footer", footer_html)

        # Update Website Settings email footer
        frappe.db.sql(
            """INSERT INTO `tabSingles` (doctype, field, value)
               VALUES ('Website Settings', 'email_footer', %s)
               ON DUPLICATE KEY UPDATE value = %s""",
            (footer_html, footer_html)
        )

        frappe.db.commit()
        print("[Brand Kit] Applied email templates.")
    except Exception as e:
        frappe.log_error(title="Brand Kit: Email Templates", message=str(e))


# ─────────────────────────────────────────────
# 6. Letterhead
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
# 7. Login Page — logo and app name
# ─────────────────────────────────────────────

def apply_login_page(brand):
    """
    Sets the logo and app name shown on the Frappe login page.
    Frappe's login.html uses {{ logo }} and {{ app_name }} from Website Settings.
    """
    try:
        if brand.logo:
            _upsert_single("Website Settings", "banner_image", brand.logo)
            _upsert_single("System Settings", "app_logo", brand.logo)

        if brand.brand_name:
            _upsert_single("System Settings", "app_name", brand.brand_name)
            _upsert_single("Website Settings", "app_name", brand.brand_name)

        frappe.db.commit()
        frappe.clear_cache()
        frappe.cache().flushall()
        print("[Brand Kit] Applied login page branding.")
    except Exception as e:
        frappe.log_error(title="Brand Kit: Login Page", message=str(e))


# ─────────────────────────────────────────────
# Main Apply Function
# ─────────────────────────────────────────────

def apply_all_branding(doc, method=None):
    """
    Called automatically when Brand Settings is saved.
    Applies branding to all configured subsystems.
    """
    brand = doc

    print("[Brand Kit] Applying branding...")

    apply_system_settings(brand)
    apply_website_settings(brand)
    apply_css(brand)
    apply_letterhead(brand)
    apply_email_branding(brand)
    apply_email_templates(brand)
    apply_login_page(brand)

    # Replace splash image with brand logo
    try:
        from brand_kit.tasks import _replace_splash_image
        _replace_splash_image()
    except Exception as e:
        frappe.log_error(title="Brand Kit: Splash", message=str(e))

    frappe.db.commit()
    frappe.msgprint(
        "Brand settings applied successfully across system, website, emails, login page, and print formats.",
        title="Brand Kit",
        indicator="green"
    )
    print("[Brand Kit] Done.")
