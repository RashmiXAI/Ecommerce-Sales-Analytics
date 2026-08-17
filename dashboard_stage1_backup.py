import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 45%,
            #172554 100%
        );
        color: white;
    }

    /* Header */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        color: #ffffff;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #cbd5e1;
        margin-bottom: 30px;
    }

    /* KPI cards */
    .kpi-card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.25);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-5px);
    }

    .kpi-title {
        color: #cbd5e1;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: white;
        font-size: 28px;
        font-weight: 800;
        margin-top: 8px;
    }

    /* Section headings */
    .section-title {
        font-size: 25px;
        font-weight: 750;
        color: white;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #020617;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = (
        "Data/cleaned/"
        "ecommerce_sales_cleaned_final.csv"
    )

    data = pd.read_csv(file_path)

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"],
        errors="coerce"
    )

    return data


df = load_data()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to interact with the dashboard."
)

# Category filter
categories = sorted(
    df["Category"].dropna().unique()
)

selected_categories = st.sidebar.multiselect(
    "📦 Category",
    categories,
    default=categories
)

# City filter
cities = sorted(
    df["City"].dropna().unique()
)

selected_cities = st.sidebar.multiselect(
    "🏙️ City",
    cities,
    default=cities
)

# Payment method filter
payment_methods = sorted(
    df["Payment_Method"].dropna().unique()
)

selected_payment = st.sidebar.multiselect(
    "💳 Payment Method",
    payment_methods,
    default=payment_methods
)

# Order status filter
statuses = sorted(
    df["Order_Status"].dropna().unique()
)

selected_status = st.sidebar.multiselect(
    "📋 Order Status",
    statuses,
    default=statuses
)


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["Category"].isin(selected_categories)
    & df["City"].isin(selected_cities)
    & df["Payment_Method"].isin(selected_payment)
    & df["Order_Status"].isin(selected_status)
].copy()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🛒 E-Commerce Sales Analytics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Interactive Business Intelligence Dashboard'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = filtered_df["Order_ID"].nunique()

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_quantity = filtered_df["Quantity"].sum()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

average_discount = filtered_df[
    "Discount_Percentage"
].mean()


# ============================================================
# KPI CARDS
# ============================================================

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📦 TOTAL ORDERS</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi2:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💰 TOTAL SALES</div>
            <div class="kpi-value">₹{total_sales:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi3:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">📈 TOTAL PROFIT</div>
            <div class="kpi-value">₹{total_profit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi4:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🛍️ QUANTITY</div>
            <div class="kpi-value">{total_quantity:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi5:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">💵 AVG ORDER VALUE</div>
            <div class="kpi-value">₹{average_order_value:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with kpi6:
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">🏷️ AVG DISCOUNT</div>
            <div class="kpi-value">{average_discount:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MONTHLY SALES & PROFIT
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 Sales & Profit Trend'
    '</div>',
    unsafe_allow_html=True
)

monthly = (
    filtered_df
    .assign(
        Month=filtered_df["Order_Date"].dt.to_period("M")
    )
    .groupby("Month", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )
)

monthly["Month"] = monthly["Month"].astype(str)

fig_monthly = go.Figure()

fig_monthly.add_trace(
    go.Scatter(
        x=monthly["Month"],
        y=monthly["Sales"],
        mode="lines+markers",
        name="Sales",
        line=dict(width=4),
        marker=dict(size=8)
    )
)

fig_monthly.add_trace(
    go.Scatter(
        x=monthly["Month"],
        y=monthly["Profit"],
        mode="lines+markers",
        name="Profit",
        line=dict(width=4),
        marker=dict(size=8)
    )
)

fig_monthly.update_layout(
    template="plotly_dark",
    height=450,
    hovermode="x unified",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Month",
    yaxis_title="Amount (₹)"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# ============================================================
# CATEGORY + PAYMENT
# ============================================================

col1, col2 = st.columns(2)


# ---------------- CATEGORY ----------------

with col1:

    st.markdown(
        '<div class="section-title">'
        '📦 Category Performance'
        '</div>',
        unsafe_allow_html=True
    )

    category = (
        filtered_df
        .groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
    )

    fig_category = px.bar(
        category,
        x="Category",
        y="Sales",
        color="Profit",
        title="Sales by Category",
        hover_data=["Profit"]
    )

    fig_category.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


# ---------------- PAYMENT ----------------

with col2:

    st.markdown(
        '<div class="section-title">'
        '💳 Payment Methods'
        '</div>',
        unsafe_allow_html=True
    )

    payment = (
        filtered_df
        .groupby("Payment_Method", as_index=False)
        .agg(
            Orders=("Order_ID", "nunique"),
            Sales=("Sales", "sum")
        )
    )

    fig_payment = px.pie(
        payment,
        names="Payment_Method",
        values="Orders",
        hole=0.55,
        title="Orders by Payment Method"
    )

    fig_payment.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_payment,
        use_container_width=True
    )


# ============================================================
# TOP PRODUCTS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🏆 Top Products'
    '</div>',
    unsafe_allow_html=True
)

products = (
    filtered_df
    .groupby("Product", as_index=False)
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    products.sort_values("Sales"),
    x="Sales",
    y="Product",
    orientation="h",
    color="Profit",
    title="Top 10 Products by Sales",
    hover_data=["Profit", "Quantity"]
)

fig_products.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=500
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)


# ============================================================
# CITY ANALYSIS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        '<div class="section-title">'
        '🏙️ Top Cities'
        '</div>',
        unsafe_allow_html=True
    )

    city = (
        filtered_df
        .groupby("City", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig_city = px.bar(
        city.sort_values("Sales"),
        x="Sales",
        y="City",
        orientation="h",
        color="Profit",
        title="Top 10 Cities"
    )

    fig_city.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True
    )


# ============================================================
# ORDER STATUS
# ============================================================

with col2:

    st.markdown(
        '<div class="section-title">'
        '📋 Order Status'
        '</div>',
        unsafe_allow_html=True
    )

    status = (
        filtered_df
        .groupby("Order_Status", as_index=False)
        .agg(
            Orders=("Order_ID", "nunique")
        )
    )

    fig_status = px.pie(
        status,
        names="Order_Status",
        values="Orders",
        hole=0.5,
        title="Order Status Distribution"
    )

    fig_status.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )


# ============================================================
# PROFIT RELATIONSHIPS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📈 Profit Relationships'
    '</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)


with col1:

    fig_discount = px.scatter(
        filtered_df,
        x="Discount_Percentage",
        y="Profit",
        size="Sales",
        color="Category",
        hover_data=[
            "Product",
            "Sales",
            "Quantity"
        ],
        title="Discount vs Profit"
    )

    fig_discount.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_discount,
        use_container_width=True
    )


with col2:

    fig_price = px.scatter(
        filtered_df,
        x="Unit_Price",
        y="Profit",
        size="Sales",
        color="Category",
        hover_data=[
            "Product",
            "Sales",
            "Quantity"
        ],
        title="Unit Price vs Profit"
    )

    fig_price.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )


# ============================================================
# DATA TABLE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔎 Filtered Sales Data'
    '</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=400
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <br>
    <center>
        <p style="color:#94a3b8;">
            🛒 E-Commerce Sales Analytics |
            Built with Python • Pandas • Plotly • Streamlit
        </p>
    </center>
    """,
    unsafe_allow_html=True
)