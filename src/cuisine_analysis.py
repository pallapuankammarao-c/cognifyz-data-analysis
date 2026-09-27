"""
Cuisine Analysis Module for Cognifyz Restaurant Data.
Analyzes individual cuisines, multi-cuisine combinations, and culinary popularity vs. rating.
"""

from collections import Counter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_top_cuisines_individual(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Splits multi-cuisine entries to find individual cuisine frequency, avg rating, and total votes.
    """
    records = []
    for _, row in df.iterrows():
        cuisines_str = str(row["Cuisines"])
        if cuisines_str == "Unknown / Not Specified":
            continue
        cuisines_list = [c.strip() for c in cuisines_str.split(",") if c.strip()]
        for c in cuisines_list:
            records.append({
                "Cuisine": c,
                "Rating": row["Aggregate rating"],
                "Votes": row["Votes"],
                "Cost": row["Average Cost for two"],
            })

    cuisines_df = pd.DataFrame(records)
    grouped = cuisines_df.groupby("Cuisine").agg(
        Count=("Rating", "count"),
        Avg_Rating=("Rating", "mean"),
        Avg_Rating_Rated=("Rating", lambda x: round(x[x > 0].mean(), 2) if (x > 0).any() else 0.0),
        Total_Votes=("Votes", "sum"),
        Avg_Votes=("Votes", "mean"),
    ).reset_index()

    grouped["Avg_Rating"] = grouped["Avg_Rating"].round(2)
    grouped["Avg_Votes"] = grouped["Avg_Votes"].round(1)
    return grouped.sort_values(by="Count", ascending=False).head(top_n)


def get_top_cuisine_combinations(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    """
    Analyzes the most frequent multi-cuisine offerings as served by restaurants.
    """
    combos = df[df["Cuisines"] != "Unknown / Not Specified"]["Cuisines"].value_counts().reset_index()
    combos.columns = ["Cuisine_Combination", "Restaurant_Count"]
    total = len(df)
    combos["Percentage"] = (combos["Restaurant_Count"] / total * 100).round(2)
    return combos.head(top_n)


def plot_top_cuisines_bar(top_cuisines_df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart of most popular cuisines.
    """
    sorted_df = top_cuisines_df.sort_values(by="Count", ascending=True)
    fig = px.bar(
        sorted_df,
        x="Count",
        y="Cuisine",
        orientation="h",
        text="Count",
        title="Top 15 Most Common Cuisines in Dataset",
        labels={"Count": "Total Offerings", "Cuisine": "Cuisine"},
        color="Count",
        color_continuous_scale="Purples",
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{y}</b><br>Outlets: %{x:,}<extra></extra>")
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_top_combinations_bar(combo_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Bar chart showing top cuisine combinations.
    """
    top_df = combo_df.head(top_n).sort_values(by="Restaurant_Count", ascending=True)
    fig = px.bar(
        top_df,
        x="Restaurant_Count",
        y="Cuisine_Combination",
        orientation="h",
        text="Restaurant_Count",
        title=f"Top {top_n} Most Common Multi-Cuisine Combinations",
        labels={"Restaurant_Count": "Restaurant Outlets", "Cuisine_Combination": "Cuisine Pair/Combination"},
        color="Restaurant_Count",
        color_continuous_scale="Sunset",
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{y}</b><br>Outlets: %{x:,}<extra></extra>")
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_cuisine_rating_vs_votes_bubble(top_cuisines_df: pd.DataFrame) -> go.Figure:
    """
    Bubble chart showing Cuisine Popularity vs Rating vs Total Votes.
    """
    fig = px.scatter(
        top_cuisines_df,
        x="Avg_Rating_Rated",
        y="Avg_Votes",
        size="Count",
        color="Cuisine",
        text="Cuisine",
        title="Cuisine Performance Matrix (Avg Rating vs. Avg Votes &bull; Size = Outlets)",
        labels={
            "Avg_Rating_Rated": "Average Customer Rating (Rated > 0)",
            "Avg_Votes": "Average Votes per Outlet",
            "Count": "Total Outlets",
        },
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        yaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig
