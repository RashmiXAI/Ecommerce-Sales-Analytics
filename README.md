# 🛒 E-Commerce Sales Analytics

An interactive E-Commerce Sales Analytics project built with **Python, Pandas, Plotly, Matplotlib, Seaborn, and Streamlit** to analyze sales, profit, products, customers, locations, payment methods, and overall business performance.

The project transforms raw e-commerce data into meaningful insights through **data cleaning, exploratory data analysis, visualization, feature engineering, and an interactive dashboard**.

---

## 📊 Project Overview

The goal of this project is to understand the performance of an e-commerce business using data-driven analysis.

The project answers questions such as:

* 💰 How much revenue is being generated?
* 📈 How much profit is the business making?
* 📦 Which products sell the most?
* 🏆 Which category performs best?
* 🏙️ Which cities generate the highest sales?
* 🌍 Which states contribute the most revenue?
* 💳 Which payment methods are most popular?
* 📋 What percentage of orders are completed, cancelled, or returned?
* 🏷️ How do discounts affect profit?
* 📅 How do sales and profit change over time?

---

## 🎯 Key Features

### 📊 Business Performance

* Total Orders
* Total Sales
* Total Profit
* Items Sold
* Total Customers
* Average Order Value
* Profit Margin

### 📦 Product Analysis

* Top-selling products
* Product-wise sales
* Product-wise profit
* Quantity sold
* Product profit margin

### 🏷️ Category Analysis

* Category-wise sales
* Category-wise profit
* Category performance comparison

### 🏙️ Customer & Location Analysis

* City-wise sales
* City-wise profit
* State-wise performance
* Top-performing locations

### 💳 Payment Analysis

* Payment method distribution
* Orders by payment method
* Sales by payment method

### 📋 Order Analysis

* Order status distribution
* Completed orders
* Cancelled orders
* Returned orders

### 📅 Time-Based Analysis

* Monthly sales trends
* Monthly profit trends
* Order trends
* Business growth/decline analysis

### 🎛️ Interactive Dashboard

The Streamlit dashboard allows users to interact with the data using filters such as:

* Product Category
* City
* Payment Method
* Order Status
* Date Range

Charts update automatically according to the selected filters.

---

## 🧹 Data Cleaning

The dataset was cleaned before analysis.

Major preprocessing steps included:

* Handling missing values
* Removing duplicate records
* Standardizing categorical values
* Cleaning text fields
* Converting date columns
* Detecting outliers
* Handling numerical anomalies
* Validating categorical values
* Creating consistent city/state relationships
* Validating the final dataset

After cleaning, the dataset was checked to ensure that the required columns contained valid and usable data.

---

## 📈 Exploratory Data Analysis

The project uses Python libraries to perform exploratory analysis.

### Libraries Used

* **Pandas** — Data manipulation and analysis
* **NumPy** — Numerical operations
* **Matplotlib** — Data visualization
* **Seaborn** — Statistical visualization
* **Plotly** — Interactive visualizations
* **Streamlit** — Interactive dashboard

---

## 📊 Dashboard Visualizations

The dashboard contains interactive visualizations for:

| Visualization           | Purpose                                 |
| ----------------------- | --------------------------------------- |
| 📈 Sales Trend          | Understand sales changes over time      |
| 💰 Profit Trend         | Track profitability                     |
| 📦 Category Sales       | Compare product categories              |
| 🥇 Top Products         | Identify best-selling products          |
| 🏙️ City Sales          | Find high-performing cities             |
| 🌍 State Performance    | Compare states                          |
| 💳 Payment Distribution | Understand customer payment preferences |
| 📋 Order Status         | Analyze order outcomes                  |
| 🏷️ Discount vs Profit  | Understand discount impact              |
| 📊 Product Performance  | Compare sales, profit and quantity      |

---

## 💡 Business Insights

Some of the major insights obtained from the analysis include:

* Identifying the highest-performing product category
* Finding the best-selling product
* Identifying cities with the highest sales
* Comparing sales and profit across categories
* Understanding customer payment preferences
* Monitoring order completion and cancellation patterns
* Studying the relationship between discounts and profit
* Tracking business performance over time

The exact results change depending on the filters selected in the dashboard.

---

## 🗂️ Project Structure

```text
Ecommerce-Sales-Analytics/
│
├── Data/
│   └── cleaned/
│       └── ecommerce_sales_cleaned_final.csv
│
├── notebooks/
│   ├── ecommerce_analysis.ipynb
│   └── ecommerce_analysis_backup.ipynb
│
├── outputs/
│
├── src/
│   ├── __init__.py
│   ├── analysis.py
│   ├── data_cleaning.py
│   ├── data_loader.py
│   ├── feature_engineering.py
│   └── validation.py
│
├── visualizations/
│   ├── __init__.py
│   └── charts.py
│
├── dashboard.py
├── dashboard_stage1_backup.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Technologies Used

### Programming

* Python

### Data Analysis

* Pandas
* NumPy

### Data Visualization

* Matplotlib
* Seaborn
* Plotly

### Dashboard

* Streamlit

### Development Tools

* Jupyter Notebook
* VS Code
* Git
* GitHub

---

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/RashmiXAI/Ecommerce-Sales-Analytics.git
```

### 2. Move into the project directory

```bash
cd Ecommerce-Sales-Analytics
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open in your browser.

---

## 🎛️ Dashboard Filters

Users can interact with the dashboard using filters such as:

```text
📦 Product Category
🏙️ City
💳 Payment Method
📋 Order Status
📅 Date Range
```

Changing the filters updates the dashboard visualizations dynamically.

---

## 📌 Skills Demonstrated

This project demonstrates practical knowledge of:

* Python
* Pandas
* NumPy
* Data Cleaning
* Data Preprocessing
* Exploratory Data Analysis
* Data Visualization
* Statistical Analysis
* Feature Engineering
* Business Analysis
* Streamlit
* Plotly
* Matplotlib
* Seaborn
* SQL
* Git
* GitHub

---

## 📷 Dashboard Preview

Dashboard screenshots can be added here to provide a visual preview of the project.

Example:

```text
Dashboard Overview
Sales Analysis
Product Analysis
Customer & Location Analysis
```

---

## 📈 Future Improvements

Possible future enhancements include:

* Adding advanced customer segmentation
* Adding sales forecasting
* Adding machine learning models
* Adding RFM analysis
* Adding automated business recommendations
* Adding deployment using Streamlit Cloud
* Adding advanced geographic visualizations
* Adding real-time data integration

---

## 👨‍💻 Author

**Rashmi Ranjan Panda**

B.Tech — Computer Science & Engineering

Aspiring Data Analyst

### Skills

Python • Pandas • NumPy • SQL • MySQL • Excel • Power BI • Streamlit • Data Visualization

---

## ⭐ Project

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.
