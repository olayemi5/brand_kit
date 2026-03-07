import frappe


BRAND_SETTINGS_FIELDS = [
    # ── Identity ──────────────────────────────────────────
    {
        "fieldname": "section_identity",
        "label": "Brand Identity",
        "fieldtype": "Section Break",
    },
    {
        "fieldname": "brand_name",
        "label": "Brand Name",
        "fieldtype": "Data",
        "reqd": 1,
        "description": "Used as system name, email sender name, and page titles",
    },
    {
        "fieldname": "tagline",
        "label": "Tagline",
        "fieldtype": "Data",
        "description": "Short brand tagline shown on portal and emails",
    },
    {
        "fieldname": "col_break_1",
        "fieldtype": "Column Break",
    },
    {
        "fieldname": "logo",
        "label": "Logo",
        "fieldtype": "Attach Image",
        "description": "Used in system header, emails, and print formats",
    },
    {
        "fieldname": "favicon",
        "label": "Favicon",
        "fieldtype": "Attach Image",
        "description": "Browser tab icon (.ico or .png, 32x32)",
    },

    # ── Colors ────────────────────────────────────────────
    {
        "fieldname": "section_colors",
        "label": "Brand Colors",
        "fieldtype": "Section Break",
    },
    {
        "fieldname": "primary_color",
        "label": "Primary Color",
        "fieldtype": "Color",
        "default": "#171717",
        "description": "Main brand color — buttons, links, highlights",
    },
    {
        "fieldname": "secondary_color",
        "label": "Secondary Color",
        "fieldtype": "Color",
        "default": "#F5F5F5",
    },
    {
        "fieldname": "col_break_2",
        "fieldtype": "Column Break",
    },
    {
        "fieldname": "accent_color",
        "label": "Accent Color",
        "fieldtype": "Color",
        "default": "#4F46E5",
        "description": "Used for badges, highlights, and hover states",
    },
    {
        "fieldname": "text_color",
        "label": "Text Color",
        "fieldtype": "Color",
        "default": "#1A1A1A",
    },

    # ── Typography ────────────────────────────────────────
    {
        "fieldname": "section_fonts",
        "label": "Typography",
        "fieldtype": "Section Break",
    },
    {
        "fieldname": "font_family",
        "label": "Font Family",
        "fieldtype": "Select",
        "options": "Inter\nRoboto\nPoppins\nLato\nMontserrat\nOpen Sans\nNunito\nRaleway",
        "default": "Inter",
    },
    {
        "fieldname": "font_size",
        "label": "Base Font Size",
        "fieldtype": "Select",
        "options": "13px\n14px\n15px\n16px",
        "default": "14px",
    },

    # ── Email ─────────────────────────────────────────────
    {
        "fieldname": "section_email",
        "label": "Email Branding",
        "fieldtype": "Section Break",
    },
    {
        "fieldname": "email_footer",
        "label": "Email Footer Text",
        "fieldtype": "Small Text",
        "description": "Appended to all outgoing emails",
    },
    {
        "fieldname": "support_email",
        "label": "Support Email",
        "fieldtype": "Data",
        "options": "Email",
    },
    {
        "fieldname": "col_break_3",
        "fieldtype": "Column Break",
    },
    {
        "fieldname": "email_header_color",
        "label": "Email Header Color",
        "fieldtype": "Color",
        "default": "#171717",
        "description": "Background color of email header banner",
    },
    {
        "fieldname": "email_logo",
        "label": "Email Logo (optional)",
        "fieldtype": "Attach Image",
        "description": "Separate logo for emails if different from main logo",
    },

    # ── Website/Portal ─────────────────────────────────────
    {
        "fieldname": "section_website",
        "label": "Website & Portal",
        "fieldtype": "Section Break",
    },
    {
        "fieldname": "website_headline",
        "label": "Portal Headline",
        "fieldtype": "Data",
    },
    {
        "fieldname": "website_description",
        "label": "Portal Description",
        "fieldtype": "Small Text",
    },
    {
        "fieldname": "col_break_4",
        "fieldtype": "Column Break",
    },
    {
        "fieldname": "footer_links",
        "label": "Footer Links (JSON)",
        "fieldtype": "Code",
        "options": "JSON",
        "description": 'Example: [{"label": "Privacy Policy", "url": "/privacy"}]',
    },
    {
        "fieldname": "custom_css",
        "label": "Custom CSS",
        "fieldtype": "Code",
        "options": "CSS",
        "description": "Extra CSS injected into every page",
    },

    # ── Print & Letterhead ─────────────────────────────────
    {
        "fieldname": "section_print",
        "label": "Print & Letterhead",
        "fieldtype": "Section Break",
    },
    {
        "fieldname": "letterhead_top",
        "label": "Letterhead Top HTML",
        "fieldtype": "Code",
        "options": "HTML",
        "description": "HTML shown at top of every printed document",
    },
    {
        "fieldname": "letterhead_bottom",
        "label": "Letterhead Bottom HTML",
        "fieldtype": "Code",
        "options": "HTML",
        "description": "HTML shown at bottom of every printed document",
    },
    {
        "fieldname": "col_break_5",
        "fieldtype": "Column Break",
    },
    {
        "fieldname": "print_primary_color",
        "label": "Print Primary Color",
        "fieldtype": "Color",
        "default": "#171717",
        "description": "Color used in print format headers and borders",
    },
    {
        "fieldname": "company_address",
        "label": "Company Address",
        "fieldtype": "Small Text",
        "description": "Shown on letterheads and print formats",
    },
]


def ensure_brand_settings_doctype():
    """Create Brand Settings Single DocType if it does not exist."""
    if frappe.db.exists("DocType", "Brand Settings"):
        print("[Brand Kit] Brand Settings DocType already exists.")
        return

    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": "Brand Settings",
        "module": "Brand Kit",
        "is_single": 1,
        "custom": 1,
        "fields": BRAND_SETTINGS_FIELDS,
        "permissions": [
            {"role": "System Manager", "read": 1, "write": 1}
        ],
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    print("[Brand Kit] Created Brand Settings DocType.")
