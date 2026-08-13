
import streamlit as st
import sqlite3
from datetime import datetime

st.set_page_config(
    page_title="Sweet Crumbs",
    page_icon="🍰",
    layout="wide"
)

DB = "bakery.db"

# ---------- DATABASE ----------

def db():
    return sqlite3.connect(DB)

def run(sql, data=(), many=False):
    con = db()
    cur = con.cursor()
    if many:
        cur.executemany(sql, data)
    else:
        cur.execute(sql, data)
    con.commit()
    result = cur.fetchall()
    con.close()
    return result

run("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT, category TEXT, price REAL,
stock INTEGER, image TEXT)
""")

run("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
customer TEXT, total REAL,
address TEXT, payment TEXT,
status TEXT, date TEXT)
""")

run("""
CREATE TABLE IF NOT EXISTS offers(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT, code TEXT, discount REAL)
""")

# ---------- DEMO PRODUCTS ----------

if not run("SELECT * FROM products"):

    products = [
        (
            "Chocolate Cake",
            "Cakes",
            650,
            20,
            "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600"
        ),
        (
            "Red Velvet Cake",
            "Cakes",
            700,
            15,
            "https://images.unsplash.com/photo-1586788680434-30d324b2d46f?w=600"
        ),
        (
            "Black Forest Cake",
            "Cakes",
            750,
            12,
            "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=600"
        ),
        (
            "Butterscotch Cake",
            "Cakes",
            680,
            18,
            "https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?w=600"
        ),
        (
            "Red Velvet Pastry",
            "Pastries",
            180,
            30,
            "https://images.unsplash.com/photo-1614707267537-2b7f9a6d6b8d?w=600"
        ),
        (
            "Garlic Bread",
            "Breads",
            120,
            40,
            "https://images.unsplash.com/photo-1619535860434-cf9b902a6e3b?w=600"
        )
    ]

    run("""
    INSERT INTO products
    (name,category,price,stock,image)
    VALUES(?,?,?,?,?)
    """, products, True)

# ---------- SESSION ----------

if "cart" not in st.session_state:
    st.session_state.cart = {}

if "login" not in st.session_state:
    st.session_state.login = False

if "admin" not in st.session_state:
    st.session_state.admin = False

# ---------- STYLE ----------

st.markdown("""
<style>

.stApp {
    background:#fffaf4;
}

.title {
    background:#3b1d1d;
    padding:30px;
    border-radius:20px;
    color:white;
    margin-bottom:25px;
}

.title h1 {
    color:white;
}

.card {
    background:white;
    padding:20px;
    border-radius:18px;
    border:1px solid #eaded5;
    margin-bottom:15px;
}

.price {
    color:#642e25;
    font-size:20px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOGIN
# =========================================================

def login():

    st.markdown("""
    <div class="title">
    <h1>🍰 Sweet Crumbs</h1>
    <p>Happiness in Every Bite ♥</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Welcome Back")

    email = st.text_input("Email")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button(
        "Login",
        type="primary"
    ):

        if email == "admin@sweetcrumbs.com" \
                and password == "admin123":

            st.session_state.login = True
            st.session_state.admin = True
            st.rerun()

        elif email == "customer@sweetcrumbs.com" \
                and password == "customer123":

            st.session_state.login = True
            st.session_state.admin = False
            st.rerun()

        else:

            st.error(
                "Invalid login details"
            )

    st.info("""
Demo accounts:

Admin:
admin@sweetcrumbs.com
admin123

Customer:
customer@sweetcrumbs.com
customer123
""")


# =========================================================
# CUSTOMER
# =========================================================

def customer():

    st.markdown("""
    <div class="title">
    <h1>🍰 Sweet Crumbs</h1>
    <p>Freshly baked. Lovingly made.</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        [
            "Home",
            "Products",
            "Cart",
            "Offers",
            "My Orders",
            "Profile"
        ],
        horizontal=True
    )

    # ---------- HOME ----------

    if page == "Home":

        st.header(
            "What are you craving today?"
        )

        st.write(
            "Fresh cakes, pastries, breads and more."
        )

        products = run("""
        SELECT * FROM products
        ORDER BY id DESC
        """)

        cols = st.columns(4)

        for i, p in enumerate(products[:4]):

            with cols[i % 4]:

                st.image(
                    p[5],
                    use_container_width=True
                )

                st.subheader(p[1])

                st.write(
                    f"₹{p[3]:,.0f}"
                )

                if st.button(
                    "Add to Cart",
                    key=f"home{i}"
                ):

                    st.session_state.cart[p[0]] = \
                        st.session_state.cart.get(
                            p[0], 0
                        ) + 1

                    st.toast(
                        "Added to cart!"
                    )

    # ---------- PRODUCTS ----------

    elif page == "Products":

        st.header(
            "🍰 All Products"
        )

        category = st.selectbox(
            "Category",
            [
                "All",
                "Cakes",
                "Pastries",
                "Breads"
            ]
        )

        if category == "All":

            products = run(
                "SELECT * FROM products"
            )

        else:

            products = run(
                "SELECT * FROM products WHERE category=?",
                (category,)
            )

        cols = st.columns(3)

        for i, p in enumerate(products):

            with cols[i % 3]:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.image(
                    p[5],
                    use_container_width=True
                )

                st.subheader(p[1])

                st.caption(p[2])

                st.markdown(
                    f'<div class="price">₹{p[3]:,.0f}</div>',
                    unsafe_allow_html=True
                )

                st.write(
                    f"Stock: {p[4]}"
                )

                if st.button(
                    "🛒 Add to Cart",
                    key=f"product{i}"
                ):

                    st.session_state.cart[p[0]] = \
                        st.session_state.cart.get(
                            p[0], 0
                        ) + 1

                    st.success(
                        "Added!"
                    )

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

    # ---------- CART ----------

    elif page == "Cart":

        st.header(
            "🛒 My Cart"
        )

        if not st.session_state.cart:

            st.info(
                "Your cart is empty."
            )

        total = 0

        for pid, qty in list(
            st.session_state.cart.items()
        ):

            p = run(
                "SELECT * FROM products WHERE id=?",
                (pid,)
            )[0]

            subtotal = p[3] * qty
            total += subtotal

            col1, col2, col3 = \
                st.columns(3)

            col1.write(
                f"**{p[1]}**"
            )

            col2.write(
                f"Qty: {qty}"
            )

            col3.write(
                f"₹{subtotal:,.0f}"
            )

        if total > 0:

            delivery = 0 if total >= 999 else 40

            st.markdown(
                f"""
                <div class="card">
                <h3>Subtotal: ₹{total:,.0f}</h3>
                <p>Delivery: ₹{delivery}</p>
                <h2>Total: ₹{total+delivery:,.0f}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )

            address = st.text_area(
                "Delivery Address"
            )

            payment = st.selectbox(
                "Payment Method",
                [
                    "UPI",
                    "Credit / Debit Card",
                    "Cash on Delivery"
                ]
            )

            if st.button(
                "Place Order",
                type="primary"
            ):

                if not address:

                    st.error(
                        "Enter delivery address"
                    )

                else:

                    run("""
                    INSERT INTO orders
                    (customer,total,address,
                    payment,status,date)
                    VALUES(?,?,?,?,?,?)
                    """, (
                        "Customer",
                        total + delivery,
                        address,
                        payment,
                        "Pending",
                        str(datetime.now())[:16]
                    ))

                    st.session_state.cart = {}

                    st.success(
                        "🎉 Order placed successfully!"
                    )

    # ---------- OFFERS ----------

    elif page == "Offers":

        st.header(
            "🎁 Special Offers"
        )

        st.markdown("""
        <div class="card">
        <h2>FLAT 20% OFF</h2>
        <p>20% off selected cakes</p>
        <b>Code: CAKE20</b>
        </div>

        <div class="card">
        <h2>FREE DELIVERY</h2>
        <p>Free delivery above ₹999</p>
        <b>Code: FREESHIP</b>
        </div>
        """, unsafe_allow_html=True)

    # ---------- ORDERS ----------

    elif page == "My Orders":

        st.header(
            "📦 Track Orders"
        )

        orders = run("""
        SELECT * FROM orders
        ORDER BY id DESC
        """)

        for o in orders:

            st.markdown(
                f"""
                <div class="card">

                <h3>
                Order #SC{o[0]:04d}
                </h3>

                <b>
                ₹{o[2]:,.0f}
                </b>

                <p>
                Status: {o[5]}
                </p>

                <p>
                {o[3]}
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    # ---------- PROFILE ----------

    elif page == "Profile":

        st.header(
            "👤 My Profile"
        )

        st.markdown("""
        <div class="card">

        <h2>Customer</h2>

        <p>
        customer@sweetcrumbs.com
        </p>

        <p>📦 My Orders</p>
        <p>📍 My Addresses</p>
        <p>💳 Payment Methods</p>
        <p>🎁 Offers & Coupons</p>

        </div>
        """, unsafe_allow_html=True)

    if st.button("Logout"):

        st.session_state.login = False
        st.session_state.admin = False
        st.rerun()


# =========================================================
# ADMIN
# =========================================================

def admin():

    st.markdown("""
    <div class="title">
    <h1>Sweet Crumbs Admin</h1>
    <p>Bakery Management Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    page = st.sidebar.radio(
        "ADMIN MENU",
        [
            "Dashboard",
            "Products",
            "Add Product",
            "Orders",
            "Offers",
            "Delivery"
        ]
    )

    # ---------- DASHBOARD ----------

    if page == "Dashboard":

        st.header(
            "📊 Dashboard"
        )

        orders = run(
            "SELECT * FROM orders"
        )

        products = run(
            "SELECT * FROM products"
        )

        revenue = sum(
            o[2] for o in orders
        )

        a, b, c, d = \
            st.columns(4)

        a.metric(
            "Total Orders",
            len(orders)
        )

        b.metric(
            "Revenue",
            f"₹{revenue:,.0f}"
        )

        c.metric(
            "Products",
            len(products)
        )

        d.metric(
            "Pending Orders",
            len([
                o for o in orders
                if o[5] == "Pending"
            ])
        )

        st.subheader(
            "Recent Orders"
        )

        for o in orders[-10:]:

            st.write(
                f"#{o[0]} | "
                f"{o[1]} | "
                f"₹{o[2]:,.0f} | "
                f"{o[5]}"
            )

    # ---------- PRODUCTS ----------

    elif page == "Products":

        st.header(
            "📦 Manage Products"
        )

        products = run(
            "SELECT * FROM products"
        )

        for p in products:

            col1, col2, col3 = \
                st.columns([3, 2, 1])

            col1.write(
                f"**{p[1]}**"
            )

            col2.write(
                f"₹{p[3]:,.0f} | Stock {p[4]}"
            )

            if col3.button(
                "Delete",
                key=f"delete{p[0]}"
            ):

                run(
                    "DELETE FROM products WHERE id=?",
                    (p[0],)
                )

                st.rerun()

    # ---------- ADD PRODUCT ----------

    elif page == "Add Product":

        st.header(
            "➕ Add Product"
        )

        name = st.text_input(
            "Product Name"
        )

        category = st.selectbox(
            "Category",
            [
                "Cakes",
                "Pastries",
                "Breads"
            ]
        )

        price = st.number_input(
            "Price",
            min_value=0.0
        )

        stock = st.number_input(
            "Stock",
            min_value=0
        )

        image = st.text_input(
            "Image URL"
        )

        if st.button(
            "Add Product",
            type="primary"
        ):

            run("""
            INSERT INTO products
            (name,category,price,stock,image)
            VALUES(?,?,?,?,?)
            """, (
                name,
                category,
                price,
                stock,
                image
            ))

            st.success(
                "Product added!"
            )

    # ---------- ORDERS ----------

    elif page == "Orders":

        st.header(
            "📦 Manage Orders"
        )

        orders = run("""
        SELECT * FROM orders
        ORDER BY id DESC
        """)

        statuses = [
            "Pending",
            "Confirmed",
            "Preparing",
            "Out for Delivery",
            "Delivered",
            "Cancelled"
        ]

        for o in orders:

            st.markdown(
                f"""
                <div class="card">
                <h3>Order #{o[0]}</h3>
                <p>Customer: {o[1]}</p>
                <p>Total: ₹{o[2]:,.0f}</p>
                <p>Address: {o[3]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            status = st.selectbox(
                "Order Status",
                statuses,
                index=statuses.index(o[5])
                if o[5] in statuses else 0,
                key=f"order{o[0]}"
            )

            if st.button(
                "Update",
                key=f"update{o[0]}"
            ):

                run("""
                UPDATE orders
                SET status=?
                WHERE id=?
                """, (
                    status,
                    o[0]
                ))

                st.rerun()

    # ---------- OFFERS ----------

    elif page == "Offers":

        st.header(
            "🎁 Launch Offer"
        )

        title = st.text_input(
            "Offer Name"
        )

        code = st.text_input(
            "Coupon Code"
        )

        discount = st.number_input(
            "Discount %",
            min_value=0.0,
            max_value=100.0
        )

        if st.button(
            "Launch Offer"
        ):

            run("""
            INSERT INTO offers
            (title,code,discount)
            VALUES(?,?,?)
            """, (
                title,
                code,
                discount
            ))

            st.success(
                "Offer launched!"
            )

    # ---------- DELIVERY ----------

    elif page == "Delivery":

        st.header(
            "🚚 Delivery Options"
        )

        st.info(
            "Standard Delivery — 30–45 mins — ₹40"
        )

        st.info(
            "Express Delivery — 15–20 mins — ₹80"
        )

    if st.sidebar.button(
        "Logout"
    ):

        st.session_state.login = False
        st.session_state.admin = False
        st.rerun()


# =========================================================
# RUN
# =========================================================

if not st.session_state.login:

    login()

elif st.session_state.admin:

    admin()

else:

    customer()
