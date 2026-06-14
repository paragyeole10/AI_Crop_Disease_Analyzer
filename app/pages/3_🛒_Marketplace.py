import sys
import os
# Add project root to sys.path dynamically
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import base64
import random
import streamlit as st
from src.config import load_config, get_absolute_path
from src.marketplace import PRODUCTS, get_recommended_products, DISEASE_PRODUCT_MAPPING

def get_base64_image(image_path):
    """Convert a local product image to base64 string to embed in HTML."""
    try:
        abs_path = get_absolute_path(image_path)
        if abs_path and os.path.exists(abs_path):
            with open(abs_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception:
        pass
    return ""

# Helper to render stepper
def render_tracking_stepper(status_index):
    steps = [
        {"name": "Order Placed", "icon": "📝"},
        {"name": "Dispatched", "icon": "📦"},
        {"name": "In Transit", "icon": "🚚"},
        {"name": "Delivered", "icon": "🏡"}
    ]
    
    html = '<div class="stepper-wrapper">'
    for idx, step in enumerate(steps):
        status_class = ""
        if idx < status_index:
            status_class = "completed"
        elif idx == status_index:
            status_class = "active"
            
        html += f"""<div class="stepper-item {status_class}">
<div class="step-counter">{step['icon']}</div>
<div class="step-name">{step['name']}</div>
</div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

st.markdown("## 🛒 AgriVision Crop Care Marketplace")
st.markdown("Browse high-quality fertilizer, pest control, and soil restoration products customized for your crops.")

# 2. Personalized Recommendations Banner
if st.session_state.last_diagnosis:
    diag = st.session_state.last_diagnosis
    st.markdown(f"""<div class="recommendation-banner">
<span style="font-size: 2.2rem;">💡</span>
<div class="recommendation-banner-content">
<div class="recommendation-banner-title">Personalized Treatment Available</div>
<div class="recommendation-banner-text">Based on your recent scan showing <b>{diag['disease_name']}</b>, we recommend specific treatments below (marked with ⭐).</div>
</div>
</div>""", unsafe_allow_html=True)

# 3. Determine Step View
if st.session_state.checkout_step == "tracking":
    # Find current order
    order = None
    for o in st.session_state.orders:
        if o['order_id'] == st.session_state.current_order_id:
            order = o
            break
            
    if not order:
        st.error("No active order found.")
        if st.button("Return to Marketplace"):
            st.session_state.checkout_step = "cart"
            st.rerun()
    else:
        st.success(f"🎉 Order {order['order_id']} placed successfully! Estimated delivery in 2-3 business days.")
        
        st.markdown("### 🚚 Live Delivery Tracker")
        st.markdown("Use the slider below to simulate the dispatch and delivery steps:")
        
        simulated_step = st.select_slider(
            "Simulation Stage",
            options=["Order Placed 📝", "Dispatched from Depot 📦", "In Transit 🚚", "Delivered 🏡"],
            value=["Order Placed 📝", "Dispatched from Depot 📦", "In Transit 🚚", "Delivered 🏡"][order['status_index']]
        )
        
        step_mapping = {
            "Order Placed 📝": 0,
            "Dispatched from Depot 📦": 1,
            "In Transit 🚚": 2,
            "Delivered 🏡": 3
        }
        order['status_index'] = step_mapping[simulated_step]
        order['status'] = simulated_step
        
        # Render stepper
        render_tracking_stepper(order['status_index'])
        
        # Display detailed delivery receipt
        st.markdown("### 📄 Order Receipt")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown(f"""**Customer Details**:
- **Name**: {order['name']}
- **Phone**: {order['phone']}
- **Address**: {order['address']}
- **Payment Method**: {order['payment_method']}""")
        with col_r2:
            st.markdown(f"**Order Reference**: `{order['order_id']}`")
            for pid, qty in order['items'].items():
                prod = PRODUCTS[pid]
                st.markdown(f"- {prod['image']} {prod['name']} (x{qty}): **${prod['price']*qty:.2f}**")
                
            st.markdown(f"""<div style="background: #F8FAF8; padding: 1rem; border-radius: 8px; margin-top: 0.5rem; font-size: 0.9rem;">
<div style="display: flex; justify-content: space-between;"><span>Subtotal:</span><span>${order['subtotal']:.2f}</span></div>
{f'<div style="display: flex; justify-content: space-between; color: #C62828;"><span>Discount:</span><span>-${order["discount"]:.2f}</span></div>' if order['discount'] > 0 else ''}
<div style="display: flex; justify-content: space-between;"><span>Shipping:</span><span>{"FREE" if order['shipping'] == 0 else f"${order['shipping']:.2f}"}</span></div>
<div style="display: flex; justify-content: space-between;"><span>Tax (8%):</span><span>${order['tax']:.2f}</span></div>
<hr style="margin: 0.3rem 0;">
<div style="display: flex; justify-content: space-between; font-weight: 700; color: #2E7D32;"><span>Grand Total:</span><span>${order['total']:.2f}</span></div>
</div>""", unsafe_allow_html=True)
            
        st.markdown("---")
        
        if st.button("Continue Shopping 🛒", use_container_width=True):
            st.session_state.checkout_step = "cart"
            st.rerun()

else:
    # Two-column layout: Products / Checkout Form on Left, Cart on Right
    col_catalog, col_cart = st.columns([2.0, 1.1])
    
    with col_catalog:
        if st.session_state.checkout_step == "checkout":
            st.markdown("### 💳 Secure Checkout")
            st.markdown("Please fill out your delivery details to complete the fertilizer recommendation order.")
            
            with st.form("checkout_form"):
                name = st.text_input("Full Name", placeholder="e.g. John Doe")
                address = st.text_area("Delivery Address", placeholder="e.g. 123 Farm Road, Green County")
                phone = st.text_input("Phone Number", placeholder="e.g. +1 555-0199")
                
                pay_method = st.selectbox(
                    "Payment Method", 
                    ["Cash on Delivery (COD)", "UPI / Instant FarmPay", "Credit/Debit Card", "Agricultural Subsidy Credits"]
                )
                
                terms = st.checkbox("I agree to the Agricultural Direct Delivery Terms & Conditions")
                
                col_back, col_submit = st.columns([1, 1])
                with col_back:
                    back_click = st.form_submit_button("Back to Cart")
                with col_submit:
                    submit_click = st.form_submit_button("Place Order 🚀")
                    
            if back_click:
                st.session_state.checkout_step = "cart"
                st.rerun()
                
            if submit_click:
                if not name or not address or not phone:
                    st.error("Please fill in all the required delivery details.")
                elif not terms:
                    st.error("Please accept the terms and conditions to proceed.")
                else:
                    # Successful order placement!
                    order_id = f"AV-{random.randint(100000, 999999)}"
                    st.session_state.current_order_id = order_id
                    
                    subtotal = sum(PRODUCTS[pid]['price'] * qty for pid, qty in st.session_state.cart.items())
                    coupon_code = st.session_state.get("coupon", None)
                    discount_pct = 0.50 if coupon_code == "GROW50" else (0.20 if coupon_code == "AGRISMART" else 0.0)
                    discount = subtotal * discount_pct
                    shipping = 5.0 if subtotal < 50 else 0.0
                    tax = (subtotal - discount) * 0.08
                    grand_total = subtotal - discount + shipping + tax
                    
                    order_detail = {
                        "order_id": order_id,
                        "name": name,
                        "address": address,
                        "phone": phone,
                        "payment_method": pay_method,
                        "items": {pid: qty for pid, qty in st.session_state.cart.items()},
                        "subtotal": subtotal,
                        "discount": discount,
                        "shipping": shipping,
                        "tax": tax,
                        "total": grand_total,
                        "status": "Order Placed",
                        "status_index": 0
                    }
                    
                    st.session_state.orders.append(order_detail)
                    st.session_state.cart = {}
                    st.session_state.coupon = None
                    st.session_state.checkout_step = "tracking"
                    st.rerun()
        else:
            # Browse mode
            st.markdown("### Browse Products")
            
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            with col_f1:
                cat_filter = st.selectbox("Category Filter", ["All", "Fertilizer", "Fungicide", "Pest Control", "Soil & Nutrient Care"])
            with col_f2:
                search_query = st.text_input("🔍 Search Products", placeholder="Search products...")
            with col_f3:
                sort_option = st.selectbox("Sort By", ["Popularity", "Price: Low to High", "Price: High to Low", "Rating"])
            
            # Filter logic
            filtered_prods = list(PRODUCTS.values())
            
            recs_ids = []
            if st.session_state.last_diagnosis:
                recs_ids = DISEASE_PRODUCT_MAPPING.get(st.session_state.last_diagnosis['class_name'], [])
            
            if cat_filter != "All":
                filtered_prods = [p for p in filtered_prods if p['category'] == cat_filter]
                
            if search_query:
                q = search_query.lower()
                filtered_prods = [p for p in filtered_prods if q in p['name'].lower() or q in p['description'].lower() or q in p['suitability'].lower()]
                
            if sort_option == "Price: Low to High":
                filtered_prods.sort(key=lambda x: x['price'])
            elif sort_option == "Price: High to Low":
                filtered_prods.sort(key=lambda x: x['price'], reverse=True)
            elif sort_option == "Rating":
                filtered_prods.sort(key=lambda x: x['rating'], reverse=True)
            
            # Render Catalog Grid
            gcols = st.columns(2)
            for idx, prod in enumerate(filtered_prods):
                gcol = gcols[idx % 2]
                with gcol:
                    is_rec = prod['id'] in recs_ids
                    rec_badge = '<div style="position: absolute; top: 10px; right: 10px; background: #E8F5E9; color: #2E7D32; padding: 0.2rem 0.5rem; border-radius: 20px; font-size: 0.7rem; font-weight: 700; border: 1px solid #2E7D32;">⭐ RECOMMENDED</div>' if is_rec else ''
                    
                    img_base64 = get_base64_image(prod.get('image_path', ''))
                    if img_base64:
                        img_html = f'<img src="data:image/png;base64,{img_base64}" style="width: 80px; height: 80px; border-radius: 8px; object-fit: cover; margin-bottom: 0.5rem; display: block;" />'
                    else:
                        img_html = f'<span style="font-size: 2.5rem; display: block; margin-bottom: 0.5rem;">{prod["image"]}</span>'
                    
                    st.markdown(f"""<div style="background: white; border: 1px solid {'#2E7D32' if is_rec else '#E2E8F0'}; border-radius: 12px; padding: 1.25rem; margin-bottom: 1rem; position: relative; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); min-height: 330px; display: flex; flex-direction: column; justify-content: space-between;">
{rec_badge}
<div>
{img_html}
<span style="font-size: 0.8rem; background: #E2E8F0; color: #475569; padding: 0.15rem 0.5rem; border-radius: 12px; font-weight: 600;">{prod['category']}</span>
<h4 style="margin: 0.5rem 0 0.25rem 0; color: #1E293B; font-size: 1.05rem;">{prod['name']}</h4>
<p style="font-size: 0.85rem; color: #64748B; line-height: 1.3; min-height: 3.5rem;">{prod['description']}</p>
<div style="font-size: 0.8rem; color: #475569; margin-bottom: 0.5rem;"><b>Suitable for:</b> {prod['suitability']}</div>
</div>
<div>
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
<span style="font-size: 1.25rem; font-weight: 800; color: #2E7D32;">${prod['price']:.2f}</span>
<span style="font-size: 0.85rem; color: #F59E0B; font-weight: 600;">⭐ {prod['rating']}</span>
</div>
</div>
</div>""", unsafe_allow_html=True)
                    
                    ac_col1, ac_col2 = st.columns(2)
                    with ac_col1:
                        if st.button("Add to Cart", key=f"catalog_add_{prod['id']}"):
                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                            st.toast(f"Added {prod['name']}!")
                            st.rerun()
                    with ac_col2:
                        if st.button("Buy Now", key=f"catalog_buy_{prod['id']}"):
                            st.session_state.cart[prod['id']] = st.session_state.cart.get(prod['id'], 0) + 1
                            st.session_state.checkout_step = "checkout"
                            st.rerun()

    # Shopping Cart Column
    with col_cart:
        st.markdown("### 🛒 Shopping Cart")
        if not st.session_state.cart:
            st.markdown("Your cart is empty. Add recommended fertilizers to get started!")
        else:
            subtotal = 0.0
            for pid, qty in list(st.session_state.cart.items()):
                if qty <= 0:
                    del st.session_state.cart[pid]
                    continue
                prod = PRODUCTS[pid]
                item_total = prod['price'] * qty
                subtotal += item_total
                
                st.markdown(f"**{prod['image']} {prod['name']}**")
                item_col1, item_col2 = st.columns([2, 1])
                with item_col1:
                    st.write(f"${prod['price']:.2f} x {qty} = **${item_total:.2f}**")
                with item_col2:
                    q_col1, q_col2 = st.columns(2)
                    with q_col1:
                        if st.button("➕", key=f"cart_inc_{pid}"):
                            st.session_state.cart[pid] = qty + 1
                            st.rerun()
                    with q_col2:
                        if st.button("➖", key=f"cart_dec_{pid}"):
                            st.session_state.cart[pid] = max(0, qty - 1)
                            if st.session_state.cart[pid] == 0:
                                del st.session_state.cart[pid]
                            st.rerun()
                st.markdown("<hr style='margin: 0.4rem 0;'>", unsafe_allow_html=True)
            
            # Coupon Input
            if "coupon" not in st.session_state:
                st.session_state.coupon = None
                
            coupon_input = st.text_input("Promo Code", value=st.session_state.coupon or "", placeholder="Try GROW50 or AGRISMART")
            
            discount_pct = 0.0
            if coupon_input.upper() == "GROW50":
                st.success("Grower's Special: 50% discount applied!")
                discount_pct = 0.50
                st.session_state.coupon = "GROW50"
            elif coupon_input.upper() == "AGRISMART":
                st.success("AgriSmart: 20% discount applied!")
                discount_pct = 0.20
                st.session_state.coupon = "AGRISMART"
            elif coupon_input:
                st.error("Invalid coupon code.")
                st.session_state.coupon = None
                
            discount = subtotal * discount_pct
            shipping = 5.0 if subtotal < 50 else 0.0
            tax = (subtotal - discount) * 0.08
            grand_total = subtotal - discount + shipping + tax
            
            st.markdown(f"""<div style="background: #F8FAF8; padding: 1rem; border-radius: 8px; margin-top: 1rem; font-size: 0.9rem;">
<div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
<span>Subtotal:</span>
<span>${subtotal:.2f}</span>
</div>
{f'<div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem; color: #C62828;"><span>Discount ({discount_pct*100:.0f}%):</span><span>-${discount:.2f}</span></div>' if discount > 0 else ''}
<div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
<span>Shipping:</span>
<span>{"FREE" if shipping == 0 else f"${shipping:.2f}"}</span>
</div>
<div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
<span>Tax (8%):</span>
<span>${tax:.2f}</span>
</div>
<hr style="margin: 0.5rem 0;">
<div style="display: flex; justify-content: space-between; font-weight: 800; font-size: 1.1rem; color: #2E7D32;">
<span>Total:</span>
<span>${grand_total:.2f}</span>
</div>
</div>""", unsafe_allow_html=True)
            
            if st.session_state.checkout_step == "cart":
                if st.button("Proceed to Checkout 💳", use_container_width=True):
                    st.session_state.checkout_step = "checkout"
                    st.rerun()
