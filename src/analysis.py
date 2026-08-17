import pandas as pd
import numpy as np


# ============================================================
# HELPER FUNCTION
# ============================================================

def clean_group_column(df, column):
    """
    Make sure grouping columns contain hashable scalar values.

    This prevents:
    TypeError: unhashable type: 'numpy.ndarray'
    """

    data = df.copy()

    def convert_value(value):

        # Missing value
        if pd.isna(value) if not isinstance(value, (list, tuple, np.ndarray)) else False:
            return value

        # NumPy array
        if isinstance(value, np.ndarray):

            if value.size == 0:
                return np.nan

            if value.size == 1:
                return value.flatten()[0]

            return ", ".join(map(str, value.flatten()))

        # List or tuple
        if isinstance(value, (list, tuple)):

            if len(value) == 0:
                return np.nan

            if len(value) == 1:
                return value[0]

            return ", ".join(map(str, value))

        return value

    data[column] = data[column].apply(convert_value)

    return data


# ============================================================
# BASIC KPIs
# ============================================================

def calculate_basic_kpis(df):
    """
    Calculate the main business KPIs.
    """

    total_orders = df["Order_ID"].nunique()

    total_sales = df["Sales"].sum()

    total_profit = df["Profit"].sum()

    total_quantity = df["Quantity"].sum()

    average_order_value = (
        total_sales / total_orders
        if total_orders > 0
        else 0
    )

    average_profit_per_order = (
        total_profit / total_orders
        if total_orders > 0
        else 0
    )

    average_discount = df["Discount_Percentage"].mean()

    return {
        "total_orders": total_orders,
        "total_sales": total_sales,
        "total_profit": total_profit,
        "total_quantity": total_quantity,
        "average_order_value": average_order_value,
        "average_profit_per_order": average_profit_per_order,
        "average_discount": average_discount
    }


# ============================================================
# CATEGORY ANALYSIS
# ============================================================

def category_analysis(df):
    """
    Analyze sales, profit and quantity by category.
    """

    data = clean_group_column(df, "Category")

    result = (
        data.groupby("Category", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .sort_values("Sales", ascending=False)
    )

    return result


# ============================================================
# PRODUCT ANALYSIS
# ============================================================

def product_analysis(df):
    """
    Analyze sales, profit and quantity by product.
    """

    data = clean_group_column(df, "Product")

    result = (
        data.groupby("Product", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Quantity=("Quantity", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .sort_values("Sales", ascending=False)
    )

    return result


# ============================================================
# CITY ANALYSIS
# ============================================================

def city_analysis(df):
    """
    Analyze sales, profit and orders by city.
    """

    data = clean_group_column(df, "City")

    result = (
        data.groupby("City", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique")
        )
        .sort_values("Sales", ascending=False)
    )

    return result


# ============================================================
# PAYMENT METHOD ANALYSIS
# ============================================================

def payment_method_analysis(df):
    """
    Analyze customer payment-method preferences.
    """

    data = clean_group_column(df, "Payment_Method")

    result = (
        data.groupby("Payment_Method", as_index=False)
        .agg(
            Orders=("Order_ID", "nunique"),
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .sort_values("Orders", ascending=False)
    )

    return result


# ============================================================
# ORDER STATUS ANALYSIS
# ============================================================

def order_status_analysis(df):
    """
    Analyze order status distribution.
    """

    data = clean_group_column(df, "Order_Status")

    result = (
        data.groupby("Order_Status", as_index=False)
        .agg(
            Orders=("Order_ID", "nunique"),
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum")
        )
        .sort_values("Orders", ascending=False)
    )

    return result


# ============================================================
# MONTHLY ANALYSIS
# ============================================================

def monthly_analysis(df):
    """
    Calculate monthly sales, profit and orders.
    """

    data = df.copy()

    data["Order_Date"] = pd.to_datetime(
        data["Order_Date"],
        errors="coerce"
    )

    data["Month"] = data["Order_Date"].dt.to_period("M")

    result = (
        data.groupby("Month", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Orders=("Order_ID", "nunique"),
            Quantity=("Quantity", "sum")
        )
    )

    result["Month"] = result["Month"].astype(str)

    return result


# ============================================================
# TOP PERFORMERS
# ============================================================

def get_top_performers(df):
    """
    Identify the best-performing category, product and city.
    """

    category = category_analysis(df)
    product = product_analysis(df)
    city = city_analysis(df)

    best_category_sales = category.iloc[0]["Category"]

    best_category_profit = category.loc[
        category["Profit"].idxmax(),
        "Category"
    ]

    best_product_sales = product.iloc[0]["Product"]

    best_product_profit = product.loc[
        product["Profit"].idxmax(),
        "Product"
    ]

    best_city_sales = city.iloc[0]["City"]

    best_city_profit = city.loc[
        city["Profit"].idxmax(),
        "City"
    ]

    return {
        "best_category_by_sales": best_category_sales,
        "best_category_by_profit": best_category_profit,
        "best_product_by_sales": best_product_sales,
        "best_product_by_profit": best_product_profit,
        "best_city_by_sales": best_city_sales,
        "best_city_by_profit": best_city_profit
    }


# ============================================================
# GENERATE COMPLETE BUSINESS ANALYSIS
# ============================================================

def generate_business_analysis(df):
    """
    Generate all business analysis results.
    """

    results = {

        "basic_kpis":
            calculate_basic_kpis(df),

        "category_analysis":
            category_analysis(df),

        "product_analysis":
            product_analysis(df),

        "city_analysis":
            city_analysis(df),

        "payment_method_analysis":
            payment_method_analysis(df),

        "order_status_analysis":
            order_status_analysis(df),

        "monthly_analysis":
            monthly_analysis(df),

        "top_performers":
            get_top_performers(df)
    }

    return results