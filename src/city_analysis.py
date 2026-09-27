"""
City Analysis Module for Cognifyz Restaurant Data.
Analyzes restaurant distribution, ratings, and votes across cities.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_city_distribution(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Returns counts and percentages of restaurants by city.
    """
    city_counts = df["City"].value_counts().reset_index()
    city_counts.columns = ["City", "Restaurant_Count"]
    total = len(df)
    city_counts["Percentage"] = (city_counts["Restaurant_Count"] / total * 100).round(2)
    return city_counts.head(top_n)


def get_city_metrics(df: pd.DataFrame, min_restaurants: int = 10) -> pd.DataFrame:
    """
    Calculates detailed metrics per city (counts, avg rating, total/avg votes, avg cost).
    """
    grouped = df.groupby("City").agg(
        Restaurant_Count=("Restaurant ID", "count"),
        Avg_Rating=("Aggregate rating", "mean"),
        Avg_Rating_Rated=("Aggregate rating", lambda x: x[x > 0].mean() if (x > 0).any() else 0.0),
        Total_Votes=("Votes", "sum"),
        Avg_Votes=("Votes", "mean"),
        Avg_Cost=("Average Cost for two", "mean"),
        Delivery_Pct=("Has_Online_Delivery_Num", lambda x: round(x.mean() * 100, 2)),
        Booking_Pct=("Has_Table_Booking_Num", lambda x: round(x.mean() * 100, 2)),
    ).reset_index()

    # Filter by minimum restaurant presence for statistical significance
    filtered = grouped[grouped["Restaurant_Count"] >= min_restaurants].copy()
    filtered["Avg_Rating"] = filtered["Avg_Rating"].round(2)
    filtered["Avg_Rating_Rated"] = filtered["Avg_Rating_Rated"].round(2)
    filtered["Avg_Votes"] = filtered["Avg_Votes"].round(1)
    filtered["Avg_Cost"] = filtered["Avg_Cost"].round(1)
    return filtered.sort_values(by="Restaurant_Count", ascending=False)


def plot_top_cities_bar(city_df: pd.DataFrame) -> go.Figure:
    """
    Creates an interactive horizontal bar chart of restaurants by top cities.
    """
    sorted_df = city_df.sort_values(by="Restaurant_Count", ascending=True)
    fig = px.bar(
        sorted_df,
        x="Restaurant_Count",
        y="City",
        orientation="h",
        text="Restaurant_Count",
        title="Top Cities by Restaurant Volume",
        labels={"Restaurant_Count": "Number of Restaurants", "City": "City"},
        color="Restaurant_Count",
        color_continuous_scale="Blues",
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{y}</b><br>Restaurants: %{x:,}<extra></extra>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
        xaxis=dict(gridcolor="#e2e8f0"),
    )
    return fig


def plot_city_ratings_bar(metrics_df: pd.DataFrame, top_n: int = 15) -> go.Figure:
    """
    Plots average rating by city for top cities.
    """
    top_cities = metrics_df.sort_values(by="Avg_Rating_Rated", ascending=False).head(top_n)
    fig = px.bar(
        top_cities,
        x="City",
        y="Avg_Rating_Rated",
        text="Avg_Rating_Rated",
        title=f"Top {top_n} Cities by Average Rating (Rated Restaurants > 0)",
        labels={"Avg_Rating_Rated": "Average Rating (Out of 5.0)", "City": "City"},
        color="Avg_Rating_Rated",
        color_continuous_scale="Viridis",
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{x}</b><br>Avg Rating: %{y:.2f}<extra></extra>")
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(range=[0, 5.2], gridcolor="#e2e8f0"),
        coloraxis_showscale=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_city_votes_scatter(metrics_df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot of City Average Votes vs Average Rating.
    """
    fig = px.scatter(
        metrics_df,
        x="Avg_Votes",
        y="Avg_Rating_Rated",
        size="Restaurant_Count",
        color="Delivery_Pct",
        hover_name="City",
        title="City Engagement: Average Votes vs. Rating (Size = Restaurant Count)",
        labels={
            "Avg_Votes": "Average Votes per Restaurant",
            "Avg_Rating_Rated": "Average Rating",
            "Delivery_Pct": "Delivery %",
        },
        color_continuous_scale="Plasma",
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
