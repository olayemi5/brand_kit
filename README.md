# Brand Kit

A Frappe app for centralized branding. Set your brand once — it applies everywhere.

## What it does

| Area | What gets updated |
|---|---|
| System | System title / app name |
| Website | Logo, favicon, tagline, portal description |
| UI Theme | Primary color, accent, font, custom CSS |
| Email | Sender name, email footer/signature |
| Letterhead | Auto-generated header/footer for print formats |

---

## Installation (Fresh Server)

### Step 1 — Create the app
```bash
cd ~/frappe-bench
bench new-app brand_kit
```
When prompted:
- **App Title** → `Brand Kit`
- **App Description** → `Centralized branding for Frappe/ERPNext`
- **App Publisher** → Your name or company
- **App Email** → Your email
- **App License** → `MIT`

### Step 2 — Copy files into the app
Copy all provided files into:
```
~/frappe-bench/apps/brand_kit/brand_kit/
```
File structure should look like:
```
apps/brand_kit/
├── requirements.txt
├── setup.py
├── README.md
└── brand_kit/
    ├── __init__.py
    ├── tasks.py
    └── brand_kit/
        ├── __init__.py
        ├── hooks.py
        ├── fields.py
        ├── apply.py
        └── context.py
```

### Step 3 — Install dependencies
```bash
cd ~/frappe-bench
./env/bin/pip install -r apps/brand_kit/requirements.txt
```

### Step 4 — Install app on your site
```bash
bench --site your-site install-app brand_kit
```

### Step 5 — Run migrate
```bash
bench --site your-site migrate
```

### Step 6 — Restart bench
```bash
bench restart
```

### Step 7 — Create the Brand Settings DocType
```bash
bench --site your-site console
```
Then in the console:
```python
from brand_kit.brand_kit.fields import ensure_brand_settings_doctype
ensure_brand_settings_doctype()
```

---

## Usage

1. Go to your site and search for **Brand Settings** in the search bar
2. Fill in your brand name, colors, logo, fonts etc.
3. Click **Save** — branding is applied automatically to all areas

---

## If something goes wrong — Reinstall from scratch

```bash
# Step 1 — Uninstall from site
bench --site your-site uninstall-app brand_kit

# Step 2 — Remove the app
bench remove-app brand_kit

# Step 3 — Start fresh from Step 1 above
```

If the app directory was deleted before uninstalling:
```bash
# Remove from database manually
bench --site your-site console
```
```python
frappe.db.delete("Installed Applications", {"app_name": "brand_kit"})
frappe.db.commit()
```
```bash
# Remove from apps list
sed -i '/brand_kit/d' ~/frappe-bench/sites/apps.txt
sed -i '/brand_kit/d' ~/frappe-bench/sites/your-site/site_config.json
bench restart
```

---

## Manual reapply

To reapply branding without opening the form:
```bash
bench --site your-site execute brand_kit.tasks.reapply_branding
```

---

## Fields Reference

### Brand Identity
- Brand Name, Tagline, Logo, Favicon

### Colors
- Primary Color, Secondary Color, Accent Color, Text Color

### Typography
- Font Family (Inter, Roboto, Poppins, Lato, etc.), Base Font Size

### Email Branding
- Email Header Color, Email Logo, Support Email, Email Footer Text

### Website & Portal
- Portal Headline, Portal Description, Footer Links, Custom CSS

### Print & Letterhead
- Letterhead Top/Bottom HTML, Print Primary Color, Company Address
