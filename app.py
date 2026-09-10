import dash
from dash import html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# ------------------------
# 1. Load Data
# ------------------------
df = pd.read_csv("data/cleaned_data.csv")

# ------------------------
# 2. Initialize App
# ------------------------
app = dash.Dash(__name__)

# ------------------------
# 3. Layout
# ------------------------
app.layout = html.Div([

    # Header
    html.Div([
        html.H1("🌍 Global Health & Life Expectancy Dashboard"),
        html.H4("Interactive Data Analysis using Plotly Dash")
    ], style={
        "textAlign": "center",
        "padding": "20px",
        "backgroundColor": "#2c3e50",
        "color": "white"
    }),

    # Dropdown
    html.Div([
        dcc.Dropdown(
            id='region-dropdown',
            options=[{"label": r, "value": r} for r in df["Region"].unique()],
            value=df["Region"].unique()[0],
            clearable=False
        )
    ], style={"width": "50%", "margin": "20px auto"}),

    # Row 1 (WITH BUBBLE CHART)
    html.Div([
        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="scatter-chart"),
        dcc.Graph(id="bubble-chart")   # ✅ Bubble Chart موجود هنا
    ], style={"display": "flex", "gap": "20px", "padding": "20px", "flexWrap": "wrap"}),

    # Row 2
    html.Div([
        dcc.Graph(id="histogram"),
        dcc.Graph(id="box-plot")
    ], style={"display": "flex", "gap": "20px", "padding": "20px", "flexWrap": "wrap"}),

    # Row 3
    html.Div([
        dcc.Graph(id="violin-plot"),
        dcc.Graph(id="line-chart")
    ], style={"display": "flex", "gap": "20px", "padding": "20px", "flexWrap": "wrap"}),

    # Row 4
    html.Div([
        dcc.Graph(id="area-chart"),
        dcc.Graph(id="stacked-chart")
    ], style={"display": "flex", "gap": "20px", "padding": "20px", "flexWrap": "wrap"}),

    # Row 5
    html.Div([
        dcc.Graph(id="clustered-chart")
    ], style={"width": "80%", "margin": "auto"})

])

# ------------------------
# 4. Callback (10 outputs including bubble)
# ------------------------
@app.callback(
    Output("bar-chart", "figure"),
    Output("scatter-chart", "figure"),
    Output("bubble-chart", "figure"),      # ✅ Bubble output
    Output("histogram", "figure"),
    Output("box-plot", "figure"),
    Output("violin-plot", "figure"),
    Output("line-chart", "figure"),
    Output("area-chart", "figure"),
    Output("stacked-chart", "figure"),
    Output("clustered-chart", "figure"),
    Input("region-dropdown", "value")
)
def update_charts(selected_region):

    filtered_df = df[df["Region"] == selected_region]

    # -------- Bar --------
    country_mean = filtered_df.groupby("Country", as_index=False)["Life_expectancy"].mean()
    bar_fig = px.bar(
        country_mean,
        x="Country",
        y="Life_expectancy",
        title=f"Life Expectancy in {selected_region}",
        color="Life_expectancy",
        template="plotly_white"
    )

    # -------- Scatter --------
    scatter_fig = px.scatter(
        filtered_df,
        x="GDP_per_capita",
        y="Life_expectancy",
        size="Population_mln",
        color="Life_expectancy",
        hover_name="Country",
        title=f"GDP vs Life Expectancy in {selected_region}",
        template="plotly_white"
    )

    # -------- BUBBLE CHART (NEW) ✅ --------
    bubble_fig = px.scatter(
        filtered_df,
        x="GDP_per_capita",
        y="Life_expectancy",
        size="Population_mln",
        color="Region",
        hover_name="Country",
        title=f"🔵 Bubble Chart: GDP vs Life Expectancy in {selected_region}",
        template="plotly_white",
        size_max=50
    )

    # -------- Histogram --------
    hist_fig = px.histogram(
        filtered_df,
        x="Life_expectancy",
        nbins=30,
        title=f"Distribution of Life Expectancy in {selected_region}",
        template="plotly_white"
    )

    # -------- Box --------
    box_fig = px.box(
        filtered_df,
        y="Life_expectancy",
        title=f"Box Plot of Life Expectancy in {selected_region}",
        template="plotly_white"
    )

    # -------- Violin --------
    violin_fig = px.violin(
        filtered_df,
        y="Life_expectancy",
        box=True,
        title=f"Violin Plot of Life Expectancy in {selected_region}",
        template="plotly_white"
    )

    # -------- Line --------
    yearly_avg = filtered_df.groupby("Year", as_index=False)["Life_expectancy"].mean()
    line_fig = px.line(
        yearly_avg,
        x="Year",
        y="Life_expectancy",
        title=f"Life Expectancy Over Time in {selected_region}",
        template="plotly_white"
    )

    # -------- Area --------
    area_fig = px.area(
        yearly_avg,
        x="Year",
        y="Life_expectancy",
        title=f"Area Chart of Life Expectancy Over Time in {selected_region}",
        template="plotly_white"
    )

    # -------- Stacked Chart --------
    stacked_df = filtered_df.groupby(["Year", "Country"], as_index=False)["Life_expectancy"].mean()
    stacked_fig = px.bar(
        stacked_df,
        x="Year",
        y="Life_expectancy",
        color="Country",
        title=f"Stacked Life Expectancy by Country in {selected_region}",
        template="plotly_white"
    )

    # -------- Clustered Chart --------
    clustered_fig = px.bar(
        stacked_df,
        x="Year",
        y="Life_expectancy",
        color="Country",
        barmode="group",
        title=f"Clustered Life Expectancy by Country in {selected_region}",
        template="plotly_white"
    )

    # ✅ Return with bubble_fig (10 figures total)
    return (bar_fig, scatter_fig, bubble_fig, hist_fig, box_fig, violin_fig,
            line_fig, area_fig, stacked_fig, clustered_fig)


# ------------------------
# 5. Run App
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)