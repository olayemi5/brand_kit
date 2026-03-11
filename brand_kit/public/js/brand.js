// Brand Kit — inject CSS from boot session into desk
frappe.after_ajax(function() {
    if (frappe.boot && frappe.boot.brand_css) {
        const style = document.createElement('style');
        style.id = 'brand-kit-css';
        style.innerHTML = frappe.boot.brand_css;
        // Remove old style if exists
        const old = document.getElementById('brand-kit-css');
        if (old) old.remove();
        document.head.appendChild(style);
    }
});
