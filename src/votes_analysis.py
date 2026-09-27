"""
Votes Analysis Module for Cognifyz Restaurant Data.
Analyzes customer voting patterns, high-engagement restaurants, and correlation with price and cuisines.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_most_voted_restaurants(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Returns the top most-voted restaurants in the dataset.
    """
    columns = [
        "Restaurant Name",
        "City",
        "Cuisines",
        "Price_Range_Label",
        "Aggregate rating",
        "Votes",
        "Has Online delivery",
    ]
    top_voted = df.sort_values(by="Votes", ascending=False).head(top_n)[columns].copy()
    return top_voted


def get_votes_by_price_tier(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes voting statistics by price range.
    """
    grouped = df.groupby("Price_Range_Label").agg(
        Total_Votes=("Votes", "sum"),
        Avg_Votes=("Votes", "mean"),
        Median_Votes=("Votes", "median"),
        Max_Votes=("Votes", "max"),
        Outlets=("Restaurant ID", "count"),
    ).reset_index()

    grouped["Avg_Votes"] = grouped["Avg_Votes"].round(1)
    return grouped


def plot_top_voted_bar(top_voted_df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart showing the highest voted restaurants.
    """
    sorted_df = top_voted_df.sort_values(by="Votes", ascending=True)
    fig = px.bar(
        sorted_df,
        x="Votes",
        y="Restaurant Name",
        orientation="h",
        text="Votes",
        hover_data=["City", "Aggregate rating", "Price_Range_Label"],
        title="Top Most-Voted Restaurants (Customer Engagement Volume)",
        labels={"Votes": "Total Customer Votes", "Restaurant Name": "Restaurant Name"},
        color="Aggregate rating",
        color_continuous_scale="Viridis",
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{y}</b><br>Votes: %{x:,}<extra></extra>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_votes_vs_rating_density(df: pd.DataFrame) -> go.Figure:
    """
    2D density / contour scatter plot of Votes vs Aggregate Rating.
    """
    rated_df = df[df["Aggregate rating"] > 0]
    fig = px.density_heatmap(
        rated_df,
        x="Aggregate rating",
        y="Votes",
        nbinsx=20,
        nbinsy=20,
        title="Customer Density: Aggregate Rating vs. Vote Volume",
        labels={"Aggregate rating": "Aggregate Rating", "Votes": "Customer Votes"},
        color_continuous_scale="Viridis",
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        yaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_votes_by_top_cuisines(df: pd.DataFrame, top_n: int = 12) -> go.Figure:
    """
    Computes total votes received by top cuisines.
    """
    records = []
    for _, row in df.iterrows():
        cuisines_str = str(row["Cuisines"])
        if cuisines_str == "Unknown / Not Specified":
            continue
        for c in cuisines_str.split(","):
            c = c.strip()
            if c:
                records.append({"Cuisine": c, "Votes": row["Votes"]})

    cdf = pd.DataFrame(records)
    grouped = cdf.groupby("Cuisine")["Votes"].sum().reset_index()
    top_cuisines = grouped.sort_values(by="Votes", ascending=False).head(top_n)
    sorted_df = top_cuisines.sort_values(by="Votes", ascending=True)

    fig = px.bar(
        sorted_df,
        x="Votes",
        y="Cuisine",
        orientation="h",
        text="Votes",
        title=f"Total Customer Votes Accumulated by Top {top_n} Cuisines",
        labels={"Votes": "Total Votes", "Cuisine": "Cuisine"},
        color="Votes",
        color_continuous_scale="Purples",
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{y}</b><br>Votes: %{x:,}<extra></extra>")
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig
