"""
Global Superstore — Interactive Business Dashboard
===================================================
Run with:  streamlit run dashboard.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Global Superstore Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .kpi-card {
        background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
        border-radius: 12px;
        padding: 20px 24px;
        color: #fff;
        margin-bottom: 4px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .kpi-label { font-size: 0.78rem; font-weight: 600; opacity: 0.75; letter-spacing: 0.08em; text-transform: uppercase; }
    .kpi-value { font-size: 2rem; font-weight: 700; margin: 4px 0; }
    .kpi-delta { font-size: 0.82rem; opacity: 0.85; }

    .section-header {
        font-size: 1.05rem; font-weight: 700; color: #1e3a5f;
        border-left: 4px solid #2d6a9f; padding-left: 10px;
        margin: 24px 0 12px 0;
    }

    div[data-testid="stSidebar"] { background: #0f2744; }
    div[data-testid="stSidebar"] * { color: #cfe4ff !important; }
    div[data-testid="stSidebar"] .stMultiSelect > div { background: #1a3a62; }
    div[data-testid="stSidebar"] h1 { color: #ffffff !important; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)


# ── Data generation (self-contained — swap for real CSV load in production) ───
@st.cache_data
def load_data() -> pd.DataFrame:
    """Generate a realistic synthetic Global Superstore dataset."""
    np.random.seed(42)
    n = 5_000

    categories = ["Technology", "Furniture", "Office Supplies"]
    sub_cats = {
        "Technology":      ["Phones", "Accessories", "Machines", "Copiers"],
        "Furniture":       ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Binders", "Storage", "Art", "Appliances",
                            "Envelopes", "Fasteners", "Labels", "Paper", "Supplies"],
    }
    regions   = ["West", "East", "Central", "South"]
    segments  = ["Consumer", "Corporate", "Home Office"]
    ship_modes = ["Standard Class", "Second Class", "First Class", "Same Day"]

    first_names = ["Anna","Ben","Carlos","Diana","Ethan","Fiona","George",
                   "Hannah","Ivan","Julia","Kevin","Laura","Mike","Nina","Oscar","Paula"]
    last_names  = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller",
                   "Davis","Wilson","Moore","Taylor","Anderson","Thomas","Jackson"]

    cat_col  = np.random.choice(categories, n)
    sub_cat  = [np.random.choice(sub_cats[c]) for c in cat_col]

    base_sales  = {"Technology": 400, "Furniture": 350, "Office Supplies": 60}
    base_profit = {"Technology": 0.18, "Furniture": 0.05, "Office Supplies": 0.20}

    sales   = np.array([abs(np.random.normal(base_sales[c],  base_sales[c]*0.6))  for c in cat_col])
    margin  = np.array([np.random.normal(base_profit[c], 0.12) for c in cat_col])
    profit  = sales * margin
    discount = np.random.choice([0,.1,.2,.3,.4,.5], n, p=[.4,.25,.15,.10,.07,.03])
    qty      = np.random.randint(1, 15, n)

    order_dates = pd.date_range("2011-01-01", "2014-12-31", periods=n)
    ship_dates  = order_dates + pd.to_timedelta(np.random.randint(1, 8, n), unit="d")

    cust_ids = [f"CUS-{str(i).zfill(5)}" for i in np.random.randint(1, 500, n)]
    names    = [f"{np.random.choice(first_names)} {np.random.choice(last_names)}" for _ in range(n)]

    df = pd.DataFrame({
        "Order ID":      [f"ORD-{str(i).zfill(6)}" for i in range(n)],
        "Order Date":    order_dates,
        "Ship Date":     ship_dates,
        "Ship Mode":     np.random.choice(ship_modes, n),
        "Customer ID":   cust_ids,
        "Customer Name": names,
        "Segment":       np.random.choice(segments, n, p=[.51,.30,.19]),
        "Region":        np.random.choice(regions, n),
        "Category":      cat_col,
        "Sub-Category":  sub_cat,
        "Sales":         sales.round(2),
        "Quantity":      qty,
        "Discount":      discount,
        "Profit":        profit.round(2),
    })

    df["Year"]          = df["Order Date"].dt.year
    df["Month"]         = df["Order Date"].dt.month
    df["Month Name"]    = df["Order Date"].dt.strftime("%b")
    df["Profit Margin"] = (df["Profit"] / df["Sales"] * 100).clip(-100, 100).round(2)
    df["Ship Days"]     = (df["Ship Date"] - df["Order Date"]).dt.days
    return df


df_raw = load_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("🔍 Filters")

years = sorted(df_raw["Year"].unique())
sel_years = st.sidebar.multiselect("Year", years, default=years)

regions = sorted(df_raw["Region"].unique())
sel_regions = st.sidebar.multiselect("Region", regions, default=regions)

categories = sorted(df_raw["Category"].unique())
sel_cats = st.sidebar.multiselect("Category", categories, default=categories)

# Sub-category depends on category selection
available_subs = sorted(df_raw[df_raw["Category"].isin(sel_cats)]["Sub-Category"].unique())
sel_subs = st.sidebar.multiselect("Sub-Category", available_subs, default=available_subs)

segments = sorted(df_raw["Segment"].unique())
sel_segs = st.sidebar.multiselect("Segment", segments, default=segments)

st.sidebar.markdown("---")
st.sidebar.caption("Global Superstore Dashboard · Task 5")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_raw[
    df_raw["Year"].isin(sel_years) &
    df_raw["Region"].isin(sel_regions) &
    df_raw["Category"].isin(sel_cats) &
    df_raw["Sub-Category"].isin(sel_subs) &
    df_raw["Segment"].isin(sel_segs)
].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 📊 Global Superstore — Business Intelligence Dashboard")
st.caption(f"Showing **{len(df):,}** orders · filtered from {len(df_raw):,} total records")

if df.empty:
    st.warning("No data matches the current filters. Please adjust your selection.")
    st.stop()

# ── KPI cards ─────────────────────────────────────────────────────────────────
total_sales   = df["Sales"].sum()
total_profit  = df["Profit"].sum()
total_orders  = df["Order ID"].nunique()
avg_margin    = df["Profit Margin"].mean()
unique_custs  = df["Customer ID"].nunique()

k1, k2, k3, k4, k5 = st.columns(5)
def kpi(col, label, value, delta=""):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta">{delta}</div>
    </div>""", unsafe_allow_html=True)

kpi(k1, "Total Sales",    f"${total_sales/1e6:.2f}M", f"{len(df):,} orders")
kpi(k2, "Total Profit",   f"${total_profit/1e3:.1f}K", f"Margin: {avg_margin:.1f}%")
kpi(k3, "Avg Order Value",f"${total_sales/max(total_orders,1):,.0f}", f"{total_orders:,} orders")
kpi(k4, "Profit Margin",  f"{avg_margin:.1f}%", "avg across orders")
kpi(k5, "Customers",      f"{unique_custs:,}", "unique buyers")

st.markdown("---")

# ── Row 1: Sales trend + Category breakdown ───────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">Monthly Sales Trend</div>', unsafe_allow_html=True)
    monthly = (df.groupby(["Year", "Month"])["Sales"]
                 .sum()
                 .reset_index())
    monthly["Period"] = pd.to_datetime(monthly[["Year","Month"]].assign(day=1))
    monthly = monthly.sort_values("Period")

    fig = px.area(monthly, x="Period", y="Sales",
                  color_discrete_sequence=["#2d6a9f"],
                  labels={"Sales": "Sales ($)", "Period": ""},
                  template="plotly_white")
    fig.update_traces(fill="tozeroy", fillcolor="rgba(45,106,159,0.15)", line_width=2.5)
    fig.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=260)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<div class="section-header">Sales by Category</div>', unsafe_allow_html=True)
    cat_sales = df.groupby("Category")["Sales"].sum().reset_index()
    fig2 = px.pie(cat_sales, values="Sales", names="Category",
                  color_discrete_sequence=["#1565C0","#F57C00","#2E7D32"],
                  hole=0.42, template="plotly_white")
    fig2.update_traces(textinfo="percent+label", textposition="inside")
    fig2.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0), height=260)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Region + Segment ───────────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-header">Sales & Profit by Region</div>', unsafe_allow_html=True)
    reg = df.groupby("Region")[["Sales","Profit"]].sum().reset_index().sort_values("Sales")
    fig3 = go.Figure()
    fig3.add_bar(y=reg["Region"], x=reg["Sales"]/1e3,  name="Sales (K$)",
                 orientation="h", marker_color="#1565C0")
    fig3.add_bar(y=reg["Region"], x=reg["Profit"]/1e3, name="Profit (K$)",
                 orientation="h", marker_color="#43A047")
    fig3.update_layout(barmode="group", template="plotly_white",
                       margin=dict(l=0,r=0,t=10,b=0), height=260,
                       xaxis_title="Amount (K$)", legend=dict(orientation="h",y=1.1))
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<div class="section-header">Segment Performance</div>', unsafe_allow_html=True)
    seg = df.groupby("Segment")[["Sales","Profit"]].sum().reset_index()
    fig4 = px.bar(seg, x="Segment", y=["Sales","Profit"],
                  barmode="group",
                  color_discrete_sequence=["#1565C0","#43A047"],
                  template="plotly_white",
                  labels={"value":"Amount ($)","variable":"Metric"})
    fig4.update_layout(margin=dict(l=0,r=0,t=10,b=0), height=260,
                       legend=dict(orientation="h",y=1.1))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Top 5 Customers + Sub-Category Profit ─────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="section-header">🏆 Top 5 Customers by Sales</div>', unsafe_allow_html=True)
    top5 = (df.groupby("Customer Name")["Sales"]
              .sum()
              .nlargest(5)
              .reset_index()
              .sort_values("Sales"))
    fig5 = px.bar(top5, x="Sales", y="Customer Name",
                  orientation="h", text="Sales",
                  color="Sales",
                  color_continuous_scale="Blues",
                  template="plotly_white")
    fig5.update_traces(texttemplate="$%{text:,.0f}", textposition="outside")
    fig5.update_layout(coloraxis_showscale=False,
                       margin=dict(l=0,r=0,t=10,b=0), height=280,
                       xaxis_title="Total Sales ($)", yaxis_title="")
    st.plotly_chart(fig5, use_container_width=True)

with col6:
    st.markdown('<div class="section-header">Sub-Category Profit</div>', unsafe_allow_html=True)
    sub = (df.groupby("Sub-Category")["Profit"]
             .sum()
             .sort_values(ascending=True)
             .reset_index())
    sub["Color"] = sub["Profit"].apply(lambda x: "#2E7D32" if x >= 0 else "#C62828")
    fig6 = go.Figure(go.Bar(
        y=sub["Sub-Category"], x=sub["Profit"]/1e3,
        orientation="h", marker_color=sub["Color"],
        text=(sub["Profit"]/1e3).round(1),
        texttemplate="%{text}K", textposition="outside"
    ))
    fig6.update_layout(template="plotly_white",
                       margin=dict(l=0,r=0,t=10,b=0), height=280,
                       xaxis_title="Profit (K$)", yaxis_title="")
    st.plotly_chart(fig6, use_container_width=True)

# ── Row 4: Discount analysis + Ship mode ─────────────────────────────────────
col7, col8 = st.columns(2)

with col7:
    st.markdown('<div class="section-header">Discount vs Profit Impact</div>', unsafe_allow_html=True)
    disc_grp = df.groupby("Discount")[["Sales","Profit"]].mean().reset_index()
    fig7 = go.Figure()
    fig7.add_scatter(x=disc_grp["Discount"], y=disc_grp["Profit"],
                     mode="lines+markers", name="Avg Profit",
                     line=dict(color="#C62828", width=2.5))
    fig7.add_scatter(x=disc_grp["Discount"], y=disc_grp["Sales"],
                     mode="lines+markers", name="Avg Sales",
                     line=dict(color="#1565C0", width=2.5))
    fig7.update_layout(template="plotly_white",
                       margin=dict(l=0,r=0,t=10,b=0), height=240,
                       xaxis_title="Discount Rate", yaxis_title="Average ($)",
                       legend=dict(orientation="h", y=1.1),
                       xaxis=dict(tickformat=".0%"))
    st.plotly_chart(fig7, use_container_width=True)

with col8:
    st.markdown('<div class="section-header">Orders by Ship Mode</div>', unsafe_allow_html=True)
    ship = df["Ship Mode"].value_counts().reset_index()
    ship.columns = ["Ship Mode", "Orders"]
    fig8 = px.pie(ship, values="Orders", names="Ship Mode",
                  color_discrete_sequence=px.colors.qualitative.Set2,
                  hole=0.4, template="plotly_white")
    fig8.update_traces(textinfo="percent+label")
    fig8.update_layout(showlegend=False, margin=dict(l=0,r=0,t=10,b=0), height=240)
    st.plotly_chart(fig8, use_container_width=True)

# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("📋 View Raw Data"):
    show_cols = ["Order Date","Customer Name","Segment","Region","Category",
                 "Sub-Category","Sales","Profit","Discount","Quantity","Profit Margin"]
    st.dataframe(
        df[show_cols].sort_values("Sales", ascending=False).head(500),
        use_container_width=True
    )
    st.caption(f"Showing top 500 rows by Sales (filtered set: {len(df):,} rows)")

st.markdown("---")
st.caption("🛒 Global Superstore Dashboard · Built with Streamlit & Plotly · Task 5")
