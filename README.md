# 📊 Global Superstore — Interactive Business Dashboard

> ** | Business Intelligence Dashboarding with Streamlit**

---

## 🎯 Task Objective

Develop an interactive dashboard for analysing **sales, profit, and segment-wise performance** using the Global Superstore dataset.  
The project includes:

1. A **Jupyter Notebook** with full EDA, data cleaning, and visualisations.  
2. A **Streamlit Dashboard** with live filters and KPI charts.

---

## 📂 Repository Structure

```
global-superstore-dashboard/
│
├── Global_Superstore_Analysis.ipynb   # EDA notebook (Task 5 deliverable)
├── dashboard.py                       # Streamlit interactive dashboard
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## 🗃️ Dataset

**Global Superstore** — a fictional retail dataset widely used for BI exercises.

| Field | Detail |
|---|---|
| Source | Kaggle / Tableau Sample Superstore |
| Records | ~51,290 orders (synthetic replica: 5,000 in this repo) |
| Columns | Order ID, Date, Customer, Region, Category, Sub-Category, Sales, Profit, Discount, Quantity |
| Time span | 2011 – 2014 |

> **Note:** The code generates a realistic synthetic dataset so the notebook and dashboard run without a Kaggle download. To use the real dataset, replace the `load_data()` function with `pd.read_csv("global_superstore.csv")`.

---

## 🧹 Approach

### 1. Data Cleaning
- Imputed missing **Ship Mode** with the mode value.
- Filled missing **Discount** with `0`.
- Engineered features: `Year`, `Month`, `Profit Margin`, `Ship Days`.
- Clamped extreme margin outliers to `[-100%, +100%]`.

### 2. Exploratory Data Analysis
- **KPI Summary** — Total Sales, Profit, Orders, Average Margin.
- **Category Analysis** — bar charts of sales and profit per category.
- **Segment Pie** — revenue share by Consumer / Corporate / Home Office.
- **Regional breakdown** — grouped bar chart.
- **Monthly trend** — area chart across 2011–2014.
- **Sub-category profit** — colour-coded (green = profit, red = loss).
- **Discount vs Profit** — scatter + OLS trendline, correlation heatmap.
- **Top 5 Customers** — horizontal bar chart.
- **Profit Margin Distribution** — histogram + boxplot by category.

### 3. Interactive Dashboard (Streamlit)
Filters: **Year · Region · Category · Sub-Category · Segment** (sidebar)

KPI Cards:
- 💰 Total Sales
- 📈 Total Profit & Margin
- 🛒 Avg Order Value
- 👥 Unique Customers

Charts:
- Monthly Sales Trend (area)
- Sales by Category (donut)
- Sales & Profit by Region (grouped bar)
- Segment Performance
- **Top 5 Customers by Sales** ✅
- Sub-Category Profit (diverging bar)
- Discount vs Profit Impact (line)
- Orders by Ship Mode (donut)

---

## 🚀 How to Run

### Prerequisites
```bash
pip install -r requirements.txt
```

### Jupyter Notebook
```bash
jupyter notebook Global_Superstore_Analysis.ipynb
```

### Streamlit Dashboard
```bash
streamlit run dashboard.py
```
Then open **http://localhost:8501** in your browser.

---

## 📦 requirements.txt (contents)

```
streamlit>=1.32
pandas>=2.0
numpy>=1.26
plotly>=5.20
matplotlib>=3.8
seaborn>=0.13
```

---

## 📊 Results & Findings

| Finding | Insight |
|---|---|
| 🥇 **Technology leads** | Highest sales AND best profit margin (~18%) |
| 🛒 **Consumer segment dominates** | ~51% of total revenue |
| ⚠️ **Discounts hurt profit** | Discounts ≥ 40% almost always produce negative profit |
| 📅 **Q4 seasonal spike** | Sales peak every November–December |
| 🔴 **Tables sub-category is loss-making** | Needs pricing/cost audit |
| 🌍 **West region is strongest** | Highest sales and profit — a model to replicate |
| 👤 **Top 5 customers = outsized revenue** | High ROI target for retention programmes |

---

## 🛠️ Skills Gained

- ✅ Business Intelligence (BI) dashboarding
- ✅ Data storytelling through visual KPIs
- ✅ User interactivity with Streamlit filters
- ✅ Visual KPI analysis with Plotly

---

## 👤 Author

*Fatima Asif.*

---
