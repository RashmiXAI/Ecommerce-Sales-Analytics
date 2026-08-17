import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# CONFIGURATION
# ============================================================

OUTPUT_DIR = "outputs/charts"
PLOTLY_TEMPLATE = "plotly_white"


# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_currency(value):
    """Format numeric values as Indian-style currency."""
    return f"₹{value:,.2f}"


def save_plotly(fig, filename):
    """Save Plotly figure as HTML."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.write_html(filepath)
    return filepath


def clean_chart_data(df):
    """
    Create a safe copy of dataframe for visualization.

    Removes problematic list/array/dict values and converts
    categorical columns to strings.
    """

    data = df.copy()

    # Columns expected to be categorical
    categorical_columns = [
        "Customer_Name",
        "Gender",
        "Product",
        "Category",
        "Payment_Method",
        "City",
        "State",
        "Order_Status"
    ]

    for col in categorical_columns:

        if col not in data.columns:
            continue

        # Convert numpy arrays/lists/tuples/dicts into strings
        data[col] = data[col].apply(
            lambda x:
                x[0] if isinstance(x, (list, tuple)) and len(x) == 1
                else str(x)
                if isinstance(x, (list, tuple, dict))
                else x
        )

        # Handle numpy arrays safely
        data[col] = data[col].apply(
            lambda x:
                x.item()
                if hasattr(x, "ndim") and getattr(x, "ndim", 0) == 0
                else x
        )

        # Convert remaining values to string
        data[col] = data[col].astype(str)

        # Clean string representation
        data[col] = data[col].str.strip()

        # Replace missing representations
        data[col] = data[col].replace(
            ["nan", "None", "NaN", "<NA>"],
            "Unknown"
        )

    return data


# ============================================================
# 1. MONTHLY SALES & PROFIT
# ============================================================

def monthly_sales_profit(df):

    data = clean_chart_data(df)

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"],
        errors="coerce"
    )

    monthly = (
        data
        .dropna(subset=["Order_Date"])
        .groupby(data["Order_Date"].dt.to_period("M"))
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .reset_index()
    )

    monthly["Order_Date"] = monthly["Order_Date"].astype(str)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=monthly["Order_Date"],
            y=monthly["Sales"],
            mode="lines+markers",
            name="Sales"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=monthly["Order_Date"],
            y=monthly["Profit"],
            mode="lines+markers",
            name="Profit"
        )
    )

    fig.update_layout(
        title="Monthly Sales & Profit",
        xaxis_title="Month",
        yaxis_title="Amount",
        template=PLOTLY_TEMPLATE,
        hovermode="x unified"
    )

    return fig


# ============================================================
# 2. CATEGORY PERFORMANCE
# ============================================================

def category_performance(df):

    data = clean_chart_data(df)

    category = (
        data
        .groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values("Sales", ascending=False)
    )

    fig = px.bar(
        category,
        x="Category",
        y="Sales",
        color="Profit",
        title="Category Performance",
        text_auto=".2s",
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales"
    )

    return fig


# ============================================================
# 3. TOP PRODUCTS
# ============================================================

def top_products(df):

    data = clean_chart_data(df)

    products = (
        data
        .groupby("Product", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        products.sort_values("Sales"),
        x="Sales",
        y="Product",
        orientation="h",
        color="Profit",
        title="Top 10 Products by Sales",
        text_auto=".2s",
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        xaxis_title="Sales",
        yaxis_title="Product"
    )

    return fig


# ============================================================
# 4. TOP CITIES
# ============================================================

def top_cities(df):

    data = clean_chart_data(df)

    cities = (
        data
        .groupby("City", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .sort_values("Sales", ascending=False)
        .head(10)
    )

    fig = px.bar(
        cities.sort_values("Sales"),
        x="Sales",
        y="City",
        orientation="h",
        color="Profit",
        title="Top 10 Cities by Sales",
        text_auto=".2s",
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        xaxis_title="Sales",
        yaxis_title="City"
    )

    return fig


# ============================================================
# 5. ORDER STATUS DISTRIBUTION
# ============================================================

def order_status_distribution(df):

    data = clean_chart_data(df)

    status = (
        data["Order_Status"]
        .value_counts()
        .reset_index()
    )

    status.columns = ["Order_Status", "Count"]

    fig = px.pie(
        status,
        names="Order_Status",
        values="Count",
        title="Order Status Distribution",
        hole=0.35,
        template=PLOTLY_TEMPLATE
    )

    return fig


# ============================================================
# 6. PAYMENT METHOD DISTRIBUTION
# ============================================================

def payment_method_distribution(df):

    data = clean_chart_data(df)

    payment = (
        data["Payment_Method"]
        .value_counts()
        .reset_index()
    )

    payment.columns = ["Payment_Method", "Count"]

    fig = px.pie(
        payment,
        names="Payment_Method",
        values="Count",
        title="Payment Method Distribution",
        hole=0.35,
        template=PLOTLY_TEMPLATE
    )

    return fig


# ============================================================
# 7. QUANTITY vs PROFIT
# ============================================================

def quantity_profit_relationship(df):

    data = clean_chart_data(df)

    plot_data = data[
        ["Quantity", "Profit"]
    ].dropna()

    fig = px.scatter(
        plot_data,
        x="Quantity",
        y="Profit",
        title="Quantity vs Profit",
        trendline="ols",
        template=PLOTLY_TEMPLATE,
        opacity=0.6
    )

    fig.update_layout(
        xaxis_title="Quantity",
        yaxis_title="Profit"
    )

    return fig


# ============================================================
# 8. UNIT PRICE vs PROFIT
# ============================================================

def unit_price_profit_relationship(df):

    data = clean_chart_data(df)

    plot_data = data[
        ["Unit_Price", "Profit"]
    ].dropna()

    fig = px.scatter(
        plot_data,
        x="Unit_Price",
        y="Profit",
        title="Unit Price vs Profit",
        trendline="ols",
        template=PLOTLY_TEMPLATE,
        opacity=0.6
    )

    fig.update_layout(
        xaxis_title="Unit Price",
        yaxis_title="Profit"
    )

    return fig


# ============================================================
# 9. DISCOUNT vs PROFIT
# ============================================================

def discount_profit_relationship(df):

    data = clean_chart_data(df)

    plot_data = data[
        ["Discount_Percentage", "Profit"]
    ].dropna()

    fig = px.scatter(
        plot_data,
        x="Discount_Percentage",
        y="Profit",
        title="Discount Percentage vs Profit",
        trendline="ols",
        template=PLOTLY_TEMPLATE,
        opacity=0.6
    )

    fig.update_layout(
        xaxis_title="Discount Percentage",
        yaxis_title="Profit"
    )

    return fig


# ============================================================
# 10. CORRELATION HEATMAP
# ============================================================

def correlation_heatmap(df):

    data = df.copy()

    numeric_columns = [
        "Age",
        "Quantity",
        "Unit_Price",
        "Discount_Percentage",
        "Sales",
        "Profit"
    ]

    numeric_columns = [
        col for col in numeric_columns
        if col in data.columns
    ]

    correlation = data[numeric_columns].corr()

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap",
        template=PLOTLY_TEMPLATE
    )

    return fig


# ============================================================
# 11. PROFIT CORRECTION ANALYSIS
# ============================================================

def profit_correction_analysis(df):

    data = clean_chart_data(df)

    if "Profit" not in data.columns:
        return None

    profit = pd.to_numeric(
        data["Profit"],
        errors="coerce"
    ).dropna()

    fig = px.histogram(
        profit,
        x=profit,
        nbins=50,
        title="Profit Distribution",
        template=PLOTLY_TEMPLATE
    )

    fig.update_layout(
        xaxis_title="Profit",
        yaxis_title="Number of Orders"
    )

    return fig


# ============================================================
# 12. GENERATE ALL INTERACTIVE CHARTS
# ============================================================

def generate_all_interactive_charts(df):

    charts = {

        "monthly_sales_profit":
            monthly_sales_profit(df),

        "category_performance":
            category_performance(df),

        "top_products":
            top_products(df),

        "top_cities":
            top_cities(df),

        "order_status_distribution":
            order_status_distribution(df),

        "payment_method_distribution":
            payment_method_distribution(df),

        "quantity_profit_relationship":
            quantity_profit_relationship(df),

        "unit_price_profit_relationship":
            unit_price_profit_relationship(df),

        "discount_profit_relationship":
            discount_profit_relationship(df),

        "correlation_heatmap":
            correlation_heatmap(df),

        "profit_correction_analysis":
            profit_correction_analysis(df)
    }

    return charts