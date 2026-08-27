from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# ============================================================
# FILE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "sales_data.csv"


# ============================================================
# CREATE DATASET AUTOMATICALLY
# ============================================================

data = [
    ["2026-01-05", "Laptop", "Electronics", "North", 85000, 12000, 5, "Corporate"],
    ["2026-01-08", "Mobile", "Electronics", "South", 55000, 9000, 10, "Consumer"],
    ["2026-01-12", "Chair", "Furniture", "East", 18000, 4000, 8, "Consumer"],
    ["2026-01-15", "Table", "Furniture", "West", 32000, 7000, 6, "Corporate"],
    ["2026-01-20", "Headphones", "Electronics", "North", 15000, 3500, 15, "Consumer"],
    ["2026-01-25", "Monitor", "Electronics", "South", 42000, 8000, 7, "Corporate"],

    ["2026-02-03", "Laptop", "Electronics", "East", 92000, 15000, 6, "Corporate"],
    ["2026-02-07", "Mobile", "Electronics", "West", 61000, 10000, 12, "Consumer"],
    ["2026-02-11", "Chair", "Furniture", "North", 21000, 5000, 10, "Consumer"],
    ["2026-02-16", "Table", "Furniture", "South", 35000, 8000, 7, "Corporate"],
    ["2026-02-21", "Headphones", "Electronics", "East", 17000, 4000, 18, "Consumer"],
    ["2026-02-27", "Monitor", "Electronics", "West", 46000, 9000, 8, "Corporate"],

    ["2026-03-04", "Laptop", "Electronics", "South", 98000, 17000, 7, "Corporate"],
    ["2026-03-09", "Mobile", "Electronics", "North", 59000, 9500, 11, "Consumer"],
    ["2026-03-13", "Chair", "Furniture", "West", 24000, 5500, 11, "Consumer"],
    ["2026-03-18", "Table", "Furniture", "East", 38000, 9000, 8, "Corporate"],
    ["2026-03-23", "Headphones", "Electronics", "South", 19000, 4500, 20, "Consumer"],
    ["2026-03-28", "Monitor", "Electronics", "North", 51000, 10500, 9, "Corporate"],

    ["2026-04-05", "Laptop", "Electronics", "West", 105000, 19000, 8, "Corporate"],
    ["2026-04-10", "Mobile", "Electronics", "East", 64000, 11000, 13, "Consumer"],
    ["2026-04-14", "Chair", "Furniture", "South", 26000, 6000, 12, "Consumer"],
    ["2026-04-19", "Table", "Furniture", "North", 41000, 10000, 9, "Corporate"],
    ["2026-04-24", "Headphones", "Electronics", "West", 22000, 5500, 22, "Consumer"],
    ["2026-04-29", "Monitor", "Electronics", "East", 55000, 11500, 10, "Corporate"],

    ["2026-05-03", "Laptop", "Electronics", "North", 112000, 21000, 9, "Corporate"],
    ["2026-05-08", "Mobile", "Electronics", "South", 68000, 12000, 14, "Consumer"],
    ["2026-05-13", "Chair", "Furniture", "East", 28000, 6500, 13, "Consumer"],
    ["2026-05-18", "Table", "Furniture", "West", 45000, 11000, 10, "Corporate"],
    ["2026-05-23", "Headphones", "Electronics", "North", 25000, 6000, 25, "Consumer"],
    ["2026-05-28", "Monitor", "Electronics", "South", 59000, 12500, 11, "Corporate"],

    ["2026-06-04", "Laptop", "Electronics", "East", 118000, 23000, 10, "Corporate"],
    ["2026-06-09", "Mobile", "Electronics", "West", 72000, 13000, 15, "Consumer"],
    ["2026-06-14", "Chair", "Furniture", "North", 30000, 7000, 14, "Consumer"],
    ["2026-06-19", "Table", "Furniture", "South", 48000, 12000, 11, "Corporate"],
    ["2026-06-24", "Headphones", "Electronics", "East", 27000, 6500, 27, "Consumer"],
    ["2026-06-29", "Monitor", "Electronics", "West", 63000, 13500, 12, "Corporate"],
]


columns = [
    "Date",
    "Product",
    "Category",
    "Region",
    "Sales",
    "Profit",
    "Quantity",
    "Customer_Segment"
]


# Always create/repair CSV if it is missing or empty
if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
    dataset = pd.DataFrame(data, columns=columns)
    dataset.to_csv(DATA_FILE, index=False)
else:
    try:
        dataset = pd.read_csv(DATA_FILE)

        # If CSV exists but has no columns, recreate it
        if dataset.empty or len(dataset.columns) == 0:
            dataset = pd.DataFrame(data, columns=columns)
            dataset.to_csv(DATA_FILE, index=False)

    except pd.errors.EmptyDataError:
        dataset = pd.DataFrame(data, columns=columns)
        dataset.to_csv(DATA_FILE, index=False)


# ============================================================
# PREPARE DATA
# ============================================================

df = dataset.copy()

df["Date"] = pd.to_datetime(df["Date"])

df["Month"] = df["Date"].dt.strftime("%b")

df["Month_Number"] = df["Date"].dt.month


# ============================================================
# DASH APP
# ============================================================

app = Dash(__name__)

app.title = "Sales & Revenue Dashboard"


# ============================================================
# APP LAYOUT
# ============================================================

app.layout = html.Div(
    style={
        "backgroundColor": "#f4f6f8",
        "minHeight": "100vh",
        "padding": "20px",
        "fontFamily": "Arial"
    },

    children=[

        html.Div(
            style={
                "backgroundColor": "#1f2937",
                "padding": "25px",
                "borderRadius": "12px",
                "marginBottom": "20px",
                "textAlign": "center"
            },

            children=[

                html.H1(
                    "Sales & Revenue Data Visualization Dashboard",
                    style={"color": "white"}
                ),

                html.P(
                    "Interactive analysis of sales, profit, products and regions",
                    style={
                        "color": "#d1d5db",
                        "fontSize": "16px"
                    }
                )
            ]
        ),


        # FILTERS
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "12px",
                "marginBottom": "20px"
            },

            children=[

                html.H3("Dashboard Filters"),

                html.Div(
                    style={
                        "display": "flex",
                        "gap": "20px"
                    },

                    children=[

                        html.Div(
                            style={"flex": "1"},

                            children=[

                                html.Label("Category"),

                                dcc.Dropdown(
                                    id="category-filter",

                                    options=[
                                        {
                                            "label": "All",
                                            "value": "All"
                                        }
                                    ] +
                                    [
                                        {
                                            "label": category,
                                            "value": category
                                        }

                                        for category
                                        in sorted(df["Category"].unique())
                                    ],

                                    value="All",
                                    clearable=False
                                )
                            ]
                        ),


                        html.Div(
                            style={"flex": "1"},

                            children=[

                                html.Label("Region"),

                                dcc.Dropdown(
                                    id="region-filter",

                                    options=[
                                        {
                                            "label": "All",
                                            "value": "All"
                                        }
                                    ] +
                                    [
                                        {
                                            "label": region,
                                            "value": region
                                        }

                                        for region
                                        in sorted(df["Region"].unique())
                                    ],

                                    value="All",
                                    clearable=False
                                )
                            ]
                        )
                    ]
                )
            ]
        ),


        # KPI CARDS
        html.Div(
            style={
                "display": "flex",
                "flexWrap": "wrap"
            },

            children=[

                html.Div(
                    [
                        html.H4("Total Sales"),
                        html.H2(id="total-sales")
                    ],

                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "textAlign": "center",
                        "flex": "1",
                        "margin": "8px"
                    }
                ),


                html.Div(
                    [
                        html.H4("Total Profit"),
                        html.H2(id="total-profit")
                    ],

                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "textAlign": "center",
                        "flex": "1",
                        "margin": "8px"
                    }
                ),


                html.Div(
                    [
                        html.H4("Total Quantity"),
                        html.H2(id="total-quantity")
                    ],

                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "textAlign": "center",
                        "flex": "1",
                        "margin": "8px"
                    }
                ),


                html.Div(
                    [
                        html.H4("Average Sale"),
                        html.H2(id="average-sale")
                    ],

                    style={
                        "backgroundColor": "white",
                        "padding": "20px",
                        "borderRadius": "12px",
                        "textAlign": "center",
                        "flex": "1",
                        "margin": "8px"
                    }
                )
            ]
        ),


        # BAR
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "12px",
                "marginTop": "20px"
            },

            children=[
                dcc.Graph(id="bar-chart")
            ]
        ),


        # LINE
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "12px",
                "marginTop": "20px"
            },

            children=[
                dcc.Graph(id="line-chart")
            ]
        ),


        # PIE + SCATTER
        html.Div(
            style={
                "display": "flex",
                "gap": "20px",
                "flexWrap": "wrap",
                "marginTop": "20px"
            },

            children=[

                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "15px",
                        "borderRadius": "12px",
                        "flex": "1",
                        "minWidth": "400px"
                    },

                    children=[
                        dcc.Graph(id="pie-chart")
                    ]
                ),


                html.Div(
                    style={
                        "backgroundColor": "white",
                        "padding": "15px",
                        "borderRadius": "12px",
                        "flex": "1",
                        "minWidth": "400px"
                    },

                    children=[
                        dcc.Graph(id="scatter-chart")
                    ]
                )
            ]
        ),


        # HEATMAP
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "15px",
                "borderRadius": "12px",
                "marginTop": "20px"
            },

            children=[
                dcc.Graph(id="heatmap")
            ]
        ),


        # FOOTER
        html.Div(
            style={
                "textAlign": "center",
                "padding": "20px"
            },

            children=[
                html.P(
                    "Task 3 | Data Visualization Dashboard | Python + Pandas + Plotly + Dash"
                )
            ]
        )
    ]
)


# ============================================================
# CALLBACK
# ============================================================

@app.callback(

    Output("total-sales", "children"),
    Output("total-profit", "children"),
    Output("total-quantity", "children"),
    Output("average-sale", "children"),

    Output("bar-chart", "figure"),
    Output("line-chart", "figure"),
    Output("pie-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("heatmap", "figure"),

    Input("category-filter", "value"),
    Input("region-filter", "value")
)


def update_dashboard(category, region):

    filtered = df.copy()


    # Category filter
    if category != "All":
        filtered = filtered[
            filtered["Category"] == category
        ]


    # Region filter
    if region != "All":
        filtered = filtered[
            filtered["Region"] == region
        ]


    # ========================================================
    # KPIs
    # ========================================================

    total_sales = filtered["Sales"].sum()

    total_profit = filtered["Profit"].sum()

    total_quantity = filtered["Quantity"].sum()

    average_sale = filtered["Sales"].mean()


    # ========================================================
    # BAR CHART
    # ========================================================

    product_sales = (
        filtered
        .groupby("Product", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=False)
    )


    bar_fig = px.bar(
        product_sales,
        x="Product",
        y="Sales",
        title="Sales by Product",
        text_auto=True
    )


    bar_fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    # ========================================================
    # LINE CHART
    # ========================================================

    monthly_sales = (
        filtered
        .groupby(
            ["Month_Number", "Month"],
            as_index=False
        )["Sales"]
        .sum()
        .sort_values("Month_Number")
    )


    line_fig = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )


    line_fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    # ========================================================
    # PIE CHART
    # ========================================================

    category_sales = (
        filtered
        .groupby("Category", as_index=False)["Sales"]
        .sum()
    )


    pie_fig = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="Sales Distribution by Category",
        hole=0.3
    )


    pie_fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    # ========================================================
    # SCATTER PLOT
    # ========================================================

    scatter_fig = px.scatter(
        filtered,
        x="Sales",
        y="Profit",
        size="Quantity",
        color="Category",
        hover_data=[
            "Product",
            "Region",
            "Customer_Segment"
        ],
        title="Sales vs Profit"
    )


    scatter_fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    # ========================================================
    # HEATMAP
    # ========================================================

    correlation = filtered[
        ["Sales", "Profit", "Quantity"]
    ].corr()


    heatmap_fig = px.imshow(
        correlation,
        text_auto=True,
        aspect="auto",
        title="Correlation Heatmap"
    )


    heatmap_fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )


    # ========================================================
    # RETURN
    # ========================================================

    return (

        f"₹{total_sales:,.0f}",

        f"₹{total_profit:,.0f}",

        f"{total_quantity:,}",

        f"₹{average_sale:,.0f}",

        bar_fig,

        line_fig,

        pie_fig,

        scatter_fig,

        heatmap_fig
    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)