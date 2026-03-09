# Brand Kit for Frappe/ERPNext

A Frappe app that gives you complete white-label control over your Frappe/ERPNext system. Configure your brand once and it applies everywhere — no coding, no terminal commands, just fill in a form and save.

---

## What It Does

Brand Kit replaces all Frappe default branding with your own across:

| Area | What Changes |
|------|-------------|
| Navbar | Your logo and brand colors |
| Login Page | Your logo and app name |
| Browser Tab | Your favicon and page title |
| Splash Screen | Your logo on page load |
| Buttons & Links | Your primary and accent colors |
| Emails | Your sender name, logo, and footer |
| Letterhead | Your logo, colors, and address |
| Print Formats | Your brand colors and letterhead |

---

## Installation

```bash
# Get the app
bench get-app brand_kit https://github.com/olayemi5/brand_kit.git

# Install on your site
bench --site your-site.com install-app brand_kit

# Run migrations
bench --site your-site.com migrate

# Restart
bench restart
```

---

## Setup

1. Go to **Brand Settings** in your Frappe desk
2. Fill in your brand details:
   - Brand Name
   - Logo
   - Favicon
   - Colors
   - Email Footer
   - Company Address
3. Click **Save**

That's it. Everything applies automatically.

---

## Brand Settings Fields

### Brand Identity
- **Brand Name** — Used as system name, email sender name, and page titles
- **Logo** — Shown in navbar, login page, emails, and print formats
- **Favicon** — Browser tab icon (.ico or .png, 32x32)
- **Tagline** — Short tagline shown on portal and emails

### Brand Colors
- **Primary Color** — Navbar, buttons, email header
- **Secondary Color** — Page header background
- **Accent Color** — Links, badges, hover states
- **Text Color** — Body text color

### Typography
- **Font Family** — Choose from Inter, Roboto, Poppins, Lato, Montserrat, Open Sans, Nunito, Raleway
- **Base Font Size** — 13px, 14px, 15px, or 16px

### Email Branding
- **Email Footer Text** — Appended to all outgoing emails
- **Support Email** — Shown in footer and website settings
- **Email Header Color** — Background color of email header banner
- **Email Logo** — Separate logo for emails (optional)

### Website & Portal
- **Portal Headline** — Shown on the portal home page
- **Portal Description** — Meta description for the portal
- **Footer Links** — JSON array of footer navigation links
- **Custom CSS** — Any additional CSS injected into every page

### Print & Letterhead
- **Letterhead Top HTML** — Custom HTML for top of printed documents
- **Letterhead Bottom HTML** — Custom HTML for bottom of printed documents
- **Print Primary Color** — Color used in print format headers
- **Company Address** — Shown on letterheads and print formats

---

## How It Works

Every time you save Brand Settings, the app automatically:

1. Updates **System Settings** and **Website Settings** with your brand name
2. Sets your **logo** in Navbar Settings and Website Settings
3. Sets your **favicon** in all the right places
4. Injects **custom CSS** with your colors and fonts into every page
5. Updates all **outgoing email accounts** with your sender name and logo
6. Sets the **email footer** on all outgoing emails
7. Creates or updates your **letterhead** for print formats
8. Replaces the **splash screen** image with your logo
9. Updates the **login page** with your logo and app name
10. Flushes all caches so changes are instant for all users

---

## Manual Commands

```bash
# Initial setup (creates Brand Settings DocType)
bench --site your-site.com execute brand_kit.tasks.setup_brand_kit

# Re-apply all branding (useful after Frappe updates)
bench --site your-site.com execute brand_kit.tasks.reapply_branding
```

---

## Requirements

- Frappe v14 or v15
- ERPNext (optional)
- Python 3.10+

---

## License

MIT
