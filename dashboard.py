import streamlit as st
import pandas as pd
import plotly.express as px


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)


# ============================================================
# SIMPLE CUSTOM STYLE
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #777777;
        font-size: 17px;
        margin-bottom: 25px;
    }

    .kpi {
        padding: 18px;
        border-radius: 12px;
        text-align: center;
        background-color: #f5f7fa;
        border: 1px solid #e5e7eb;
    }

    .kpi-title {
        font-size: 14px;
        color: #666666;
        font-weight: bold;
    }

    .kpi-value {
        font-size: 25px;
        font-weight: bold;
        margin-top: 5px;
    }

    .section-title {
        font-size: 25px;
        font-weight: bold;
        margin-top: 25px;
        margin-bottom: 5px;
    }

    .section-text {
        color: #666666;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    file_path = "Data/cleaned/ecommerce_sales_cleaned_final.csv"

    data = pd.read_csv(file_path)

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"],
        errors="coerce"
    )

    return data


df = load_data()


# ============================================================
# CHECK DATA
# ============================================================

required_columns = [
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Product",
    "Category",
    "Quantity",
    "Sales",
    "Profit",
    "Payment_Method",
    "City",
    "State",
    "Order_Status",
    "Discount_Percentage"
]


missing_columns = [
    col for col in required_columns
    if col not in df.columns
]


if missing_columns:

    st.error("Some required columns are missing.")

    st.write(missing_columns)

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛒 E-Commerce Sales Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore sales, profit, customers, products and business performance'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("🎛️ Filters")

st.sidebar.write(
    "Use these filters to explore the business."
)

st.sidebar.markdown("---")


# ------------------------------------------------------------
# CATEGORY
# ------------------------------------------------------------

category_list = sorted(
    df["Category"].dropna().unique()
)

selected_category = st.sidebar.multiselect(
    "📦 Category",
    category_list,
    default=category_list
)


# ------------------------------------------------------------
# CITY
# ------------------------------------------------------------

city_list = sorted(
    df["City"].dropna().unique()
)

selected_city = st.sidebar.multiselect(
    "🏙️ City",
    city_list,
    default=city_list
)


# ------------------------------------------------------------
# STATE
# ------------------------------------------------------------

state_list = sorted(
    df["State"].dropna().unique()
)

selected_state = st.sidebar.multiselect(
    "🗺️ State",
    state_list,
    default=state_list
)


# ------------------------------------------------------------
# PAYMENT
# ------------------------------------------------------------

payment_list = sorted(
    df["Payment_Method"].dropna().unique()
)

selected_payment = st.sidebar.multiselect(
    "💳 Payment Method",
    payment_list,
    default=payment_list
)


# ------------------------------------------------------------
# ORDER STATUS
# ------------------------------------------------------------

status_list = sorted(
    df["Order_Status"].dropna().unique()
)

selected_status = st.sidebar.multiselect(
    "📋 Order Status",
    status_list,
    default=status_list
)


# ------------------------------------------------------------
# DATE
# ------------------------------------------------------------

valid_dates = df["Order_Date"].dropna()

if not valid_dates.empty:

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()

    selected_date = st.sidebar.date_input(
        "📅 Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

else:

    selected_date = None


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df[
    df["Category"].isin(selected_category)
    & df["City"].isin(selected_city)
    & df["State"].isin(selected_state)
    & df["Payment_Method"].isin(selected_payment)
    & df["Order_Status"].isin(selected_status)
].copy()


if selected_date is not None and len(selected_date) == 2:

    start_date = selected_date[0]
    end_date = selected_date[1]

    filtered_df = filtered_df[
        (
            filtered_df["Order_Date"].dt.date
            >= start_date
        )
        &
        (
            filtered_df["Order_Date"].dt.date
            <= end_date
        )
    ]


# ============================================================
# EMPTY DATA
# ============================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data found for the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_orders = filtered_df["Order_ID"].nunique()

total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_quantity = filtered_df["Quantity"].sum()

total_customers = filtered_df["Customer_ID"].nunique()

profit_margin = (
    total_profit / total_sales * 100
    if total_sales != 0
    else 0
)


# ============================================================
# KPI SECTION
# ============================================================

st.markdown(
    '<div class="section-title">📊 Business Summary</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4, k5, k6 = st.columns(6)


with k1:

    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-title">📦 TOTAL ORDERS</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-title">💰 TOTAL SALES</div>
            <div class="kpi-value">₹{total_sales:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-title">📈 TOTAL PROFIT</div>
            <div class="kpi-value">₹{total_profit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-title">🛍️ ITEMS SOLD</div>
            <div class="kpi-value">{total_quantity:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k5:

    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-title">👥 CUSTOMERS</div>
            <div class="kpi-value">{total_customers:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with k6:

    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-title">🎯 PROFIT MARGIN</div>
            <div class="kpi-value">{profit_margin:.1f}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# BUSINESS HIGHLIGHTS
# ============================================================

st.markdown(
    '<div class="section-title">💡 Business Highlights</div>',
    unsafe_allow_html=True
)

category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

product_sales = (
    filtered_df
    .groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

city_sales = (
    filtered_df
    .groupby("City")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

state_sales = (
    filtered_df
    .groupby("State")["Sales"]
    .sum()
    .sort_values(ascending=False)
)


best_category = category_sales.index[0]

best_product = product_sales.index[0]

best_city = city_sales.index[0]

best_state = state_sales.index[0]


h1, h2, h3, h4 = st.columns(4)


with h1:

    st.info(
        f"🏆 **Best Category**\n\n"
        f"### {best_category}"
    )


with h2:

    st.success(
        f"🥇 **Best Product**\n\n"
        f"### {best_product}"
    )


with h3:

    st.warning(
        f"🏙️ **Top City**\n\n"
        f"### {best_city}"
    )


with h4:

    st.info(
        f"🗺️ **Top State**\n\n"
        f"### {best_state}"
    )


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "🏠 Overview",
        "📈 Sales",
        "📦 Products",
        "👥 Customers",
        "🌍 Location",
        "🔎 Data"
    ]
)


# ============================================================
# TAB 1 - OVERVIEW
# ============================================================

with tab1:

    st.markdown(
        '<div class="section-title">'
        '📈 Overall Business Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "See how sales, profit and orders change over time."
    )


    # --------------------------------------------------------
    # MONTHLY TREND
    # --------------------------------------------------------

    monthly = (
        filtered_df
        .assign(
            Month=filtered_df["Order_Date"].dt.to_period("M")
        )
        .groupby("Month")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .reset_index()
    )

    monthly["Month"] = monthly["Month"].astype(str)


    fig = px.line(
        monthly,
        x="Month",
        y=["Sales", "Profit"],
        markers=True,
        title="Monthly Sales and Profit",
        labels={
            "value": "Amount (₹)",
            "Month": "Month",
            "variable": "Metric"
        }
    )

    fig.update_layout(
        hovermode="x unified",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # --------------------------------------------------------
    # SIMPLE EXPLANATION
    # --------------------------------------------------------

    if len(monthly) >= 2:

        first_sales = monthly.iloc[0]["Sales"]

        last_sales = monthly.iloc[-1]["Sales"]

        if first_sales != 0:

            growth = (
                (last_sales - first_sales)
                / abs(first_sales)
            ) * 100

        else:

            growth = 0


        if growth > 5:

            st.success(
                f"📈 Sales increased by approximately "
                f"{growth:.1f}% from the first period "
                f"to the latest period."
            )

        elif growth < -5:

            st.error(
                f"📉 Sales decreased by approximately "
                f"{abs(growth):.1f}% from the first period "
                f"to the latest period."
            )

        else:

            st.info(
                "➡️ Sales remained relatively stable."
            )


# ============================================================
# TAB 2 - SALES
# ============================================================

with tab2:

    st.markdown(
        '<div class="section-title">'
        '📈 Sales Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # CATEGORY SALES
    # --------------------------------------------------------

    with col1:

        category_chart = (
            filtered_df
            .groupby("Category", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum")
            )
            .sort_values(
                "Sales",
                ascending=False
            )
        )


        fig_category = px.bar(
            category_chart,
            x="Category",
            y="Sales",
            color="Category",
            text_auto=".2s",
            title="💰 Sales by Category",
            hover_data=["Profit"]
        )


        fig_category.update_layout(
            height=450,
            showlegend=False
        )


        st.plotly_chart(
            fig_category,
            use_container_width=True
        )


    # --------------------------------------------------------
    # PROFIT BY CATEGORY
    # --------------------------------------------------------

    with col2:

        fig_profit_category = px.bar(
            category_chart,
            x="Category",
            y="Profit",
            color="Category",
            text_auto=".2s",
            title="📈 Profit by Category"
        )


        fig_profit_category.update_layout(
            height=450,
            showlegend=False
        )


        st.plotly_chart(
            fig_profit_category,
            use_container_width=True
        )


    # --------------------------------------------------------
    # PAYMENT METHOD
    # --------------------------------------------------------

    payment_chart = (
        filtered_df
        .groupby("Payment_Method", as_index=False)
        .agg(
            Orders=("Order_ID", "nunique"),
            Sales=("Sales", "sum")
        )
    )


    col3, col4 = st.columns(2)


    with col3:

        fig_payment = px.pie(
            payment_chart,
            names="Payment_Method",
            values="Orders",
            hole=0.45,
            title="💳 Payment Methods"
        )

        fig_payment.update_layout(
            height=450
        )

        st.plotly_chart(
            fig_payment,
            use_container_width=True
        )


    # --------------------------------------------------------
    # ORDER STATUS
    # --------------------------------------------------------

    with col4:

        status_chart = (
            filtered_df
            .groupby("Order_Status", as_index=False)
            .agg(
                Orders=("Order_ID", "nunique")
            )
        )


        fig_status = px.pie(
            status_chart,
            names="Order_Status",
            values="Orders",
            hole=0.45,
            title="📋 Order Status"
        )


        fig_status.update_layout(
            height=450
        )


        st.plotly_chart(
            fig_status,
            use_container_width=True
        )


    # --------------------------------------------------------
    # DISCOUNT VS PROFIT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🏷️ Discount vs Profit'
        '</div>',
        unsafe_allow_html=True
    )


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
        title="Does Discount Affect Profit?"
    )


    fig_discount.update_layout(
        height=500
    )


    st.plotly_chart(
        fig_discount,
        use_container_width=True
    )


# ============================================================
# TAB 3 - PRODUCTS
# ============================================================

with tab3:

    st.markdown(
        '<div class="section-title">'
        '📦 Product Performance'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TOP 10 PRODUCTS
    # --------------------------------------------------------

    top_products = (
        filtered_df
        .groupby("Product", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )


    fig_products = px.bar(
        top_products.sort_values("Sales"),
        x="Sales",
        y="Product",
        orientation="h",
        color="Profit",
        text_auto=".2s",
        hover_data=[
            "Profit",
            "Quantity"
        ],
        title="🏆 Top 10 Products by Sales"
    )


    fig_products.update_layout(
        height=550
    )


    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


    # --------------------------------------------------------
    # PRODUCT TABLE
    # --------------------------------------------------------

    product_table = (
        filtered_df
        .groupby("Product", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values(
            "Sales",
            ascending=False
        )
    )


    product_table["Profit_Margin"] = (
        product_table["Profit"]
        / product_table["Sales"]
        * 100
    ).round(2)


    st.subheader("📋 Product Details")


    st.dataframe(
        product_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 4 - CUSTOMERS
# ============================================================

with tab4:

    st.markdown(
        '<div class="section-title">'
        '👥 Customer Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # TOP CUSTOMERS
    # --------------------------------------------------------

    customers = (
        filtered_df
        .groupby(
            "Customer_ID",
            as_index=False
        )
        .agg(
            Orders=("Order_ID", "nunique"),
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .sort_values(
            "Sales",
            ascending=False
        )
        .head(10)
    )


    fig_customers = px.bar(
        customers.sort_values("Sales"),
        x="Sales",
        y="Customer_ID",
        orientation="h",
        color="Profit",
        text_auto=".2s",
        hover_data=[
            "Orders",
            "Profit"
        ],
        title="🏆 Top 10 Customers by Sales"
    )


    fig_customers.update_layout(
        height=500
    )


    st.plotly_chart(
        fig_customers,
        use_container_width=True
    )


    # --------------------------------------------------------
    # AGE DISTRIBUTION
    # --------------------------------------------------------

    fig_age = px.histogram(
        filtered_df,
        x="Age",
        nbins=20,
        color="Gender",
        title="👤 Customer Age Distribution"
    )


    fig_age.update_layout(
        height=450
    )


    st.plotly_chart(
        fig_age,
        use_container_width=True
    )


    # --------------------------------------------------------
    # GENDER
    # --------------------------------------------------------

    gender_data = (
        filtered_df
        .groupby("Gender", as_index=False)
        .agg(
            Customers=("Customer_ID", "nunique")
        )
    )


    fig_gender = px.pie(
        gender_data,
        names="Gender",
        values="Customers",
        hole=0.45,
        title="👥 Customers by Gender"
    )


    fig_gender.update_layout(
        height=450
    )


    st.plotly_chart(
        fig_gender,
        use_container_width=True
    )


# ============================================================
# TAB 5 - LOCATION
# ============================================================

with tab5:

    st.markdown(
        '<div class="section-title">'
        '🌍 Location Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # CITY
    # --------------------------------------------------------

    with col1:

        city_chart = (
            filtered_df
            .groupby("City", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Orders=("Order_ID", "nunique")
            )
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(10)
        )


        fig_city = px.bar(
            city_chart.sort_values("Sales"),
            x="Sales",
            y="City",
            orientation="h",
            color="Profit",
            text_auto=".2s",
            hover_data=[
                "Profit",
                "Orders"
            ],
            title="🏙️ Top 10 Cities by Sales"
        )


        fig_city.update_layout(
            height=550
        )


        st.plotly_chart(
            fig_city,
            use_container_width=True
        )


    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    with col2:

        state_chart = (
            filtered_df
            .groupby("State", as_index=False)
            .agg(
                Sales=("Sales", "sum"),
                Profit=("Profit", "sum"),
                Orders=("Order_ID", "nunique")
            )
            .sort_values(
                "Sales",
                ascending=False
            )
            .head(10)
        )


        fig_state = px.bar(
            state_chart.sort_values("Sales"),
            x="Sales",
            y="State",
            orientation="h",
            color="Profit",
            text_auto=".2s",
            hover_data=[
                "Profit",
                "Orders"
            ],
            title="🗺️ Top 10 States by Sales"
        )


        fig_state.update_layout(
            height=550
        )


        st.plotly_chart(
            fig_state,
            use_container_width=True
        )


    # --------------------------------------------------------
    # CITY TABLE
    # --------------------------------------------------------

    st.subheader("📍 City Performance")


    city_table = (
        filtered_df
        .groupby("City", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .sort_values(
            "Sales",
            ascending=False
        )
    )


    st.dataframe(
        city_table,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# TAB 6 - DATA
# ============================================================

with tab6:

    st.markdown(
        '<div class="section-title">'
        '🔎 Detailed Data'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        f"Showing **{len(filtered_df):,} records**"
    )


    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=550,
        hide_index=True
    )


    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")


    st.download_button(
        label="📥 Download Filtered Data",
        data=csv_data,
        file_name="filtered_ecommerce_sales.csv",
        mime="text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🛒 E-Commerce Sales Dashboard | "
    "Built with Python • Pandas • Plotly • Streamlit"
)