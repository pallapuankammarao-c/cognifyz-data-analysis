"""
Restaurant Rating Analysis Module for Cognifyz Restaurant Data.
Analyzes aggregate rating distributions, rating text sentiment categories, and vote correlations.
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go


def get_rating_statistics(df: pd.DataFrame) -> dict:
    """
    Computes distribution statistics for restaurant ratings.
    """
    all_ratings = df["Aggregate rating"]
    rated_ratings = df[df["Aggregate rating"] > 0]["Aggregate rating"]

    return {
        "mean_all": round(all_ratings.mean(), 2),
        "median_all": round(all_ratings.median(), 2),
        "std_all": round(all_ratings.std(), 2),
        "mean_rated": round(rated_ratings.mean(), 2) if len(rated_ratings) > 0 else 0.0,
        "median_rated": round(rated_ratings.median(), 2) if len(rated_ratings) > 0 else 0.0,
        "unrated_count": int((all_ratings == 0).sum()),
        "unrated_pct": round((all_ratings == 0).mean() * 100, 2),
        "top_rated_count": int((all_ratings >= 4.5).sum()),
        "top_rated_pct": round((all_ratings >= 4.5).mean() * 100, 2),
    }


def get_rating_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns breakdown of rating text categories (Excellent, Very Good, Good, Average, Poor, Not rated).
    """
    breakdown = df.groupby("Rating text").agg(
        Count=("Restaurant ID", "count"),
        Avg_Rating=("Aggregate rating", "mean"),
        Avg_Votes=("Votes", "mean"),
        Avg_Cost=("Average Cost for two", "mean"),
    ).reset_index()

    order = ["Excellent", "Very Good", "Good", "Average", "Poor", "Not rated"]
    breakdown["Sort_Order"] = breakdown["Rating text"].apply(lambda x: order.index(x) if x in order else 99)
    breakdown = breakdown.sort_values(by="Sort_Order").drop(columns=["Sort_Order"])
    total = len(df)
    breakdown["Percentage"] = (breakdown["Count"] / total * 100).round(2)
    breakdown["Avg_Rating"] = breakdown["Avg_Rating"].round(2)
    breakdown["Avg_Votes"] = breakdown["Avg_Votes"].round(1)
    return breakdown


def plot_rating_distribution(df: pd.DataFrame, include_unrated: bool = False) -> go.Figure:
    """
    Histogram of aggregate rating distribution.
    """
    plot_data = df if include_unrated else df[df["Aggregate rating"] > 0]
    title_suffix = "Including Unrated (0.0)" if include_unrated else "Rated Outlets (> 0.0)"

    fig = px.histogram(
        plot_data,
        x="Aggregate rating",
        nbins=25,
        title=f"Aggregate Rating Distribution ({title_suffix})",
        labels={"Aggregate rating": "Aggregate Rating (0 - 5)", "count": "Frequency"},
        color_discrete_sequence=["#3b82f6"],
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


def plot_rating_categories_bar(breakdown_df: pd.DataFrame) -> go.Figure:
    """
    Bar chart of rating categories with standard Cognifyz coloring.
    """
    color_map = {
        "Excellent": "#22c55e",
        "Very Good": "#84cc16",
        "Good": "#eab308",
        "Average": "#f97316",
        "Poor": "#ef4444",
        "Not rated": "#94a3b8",
    }
    fig = px.bar(
        breakdown_df,
        x="Rating text",
        y="Count",
        text="Count",
        title="Restaurant Count by Rating Category (Cognifyz Classification)",
        labels={"Rating text": "Rating Tier", "Count": "Number of Restaurants"},
        color="Rating text",
        color_discrete_map=color_map,
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{x}</b><br>Outlets: %{y:,}<extra></extra>")
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_rating_vs_votes_scatter(df: pd.DataFrame, sample_size: int = 1500) -> go.Figure:
    """
    Scatter plot analyzing correlation between aggregate rating and customer votes.
    """
    rated_df = df[df["Aggregate rating"] > 0]
    sample_df = rated_df.sample(min(sample_size, len(rated_df)), random_state=42)

    corr = round(rated_df["Aggregate rating"].corr(rated_df["Votes"]), 2)

    fig = px.scatter(
        sample_df,
        x="Aggregate rating",
        y="Votes",
        color="Price_Range_Label",
        hover_name="Restaurant Name",
        hover_data=["City", "Cuisines", "Price_Range_Label"],
        title=f"Customer Votes vs. Aggregate Rating (Sampled {len(sample_df):,} Outlets &bull; Pearson r = {corr})",
        labels={"Aggregate rating": "Aggregate Rating (0 - 5)", "Votes": "Customer Votes"},
        color_discrete_sequence=["#3b82f6", "#10b981", "#f59e0b", "#ef4444"],
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
