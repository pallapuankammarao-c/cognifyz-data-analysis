"""
Online Delivery Analysis Module for Cognifyz Restaurant Data.
Analyzes online ordering penetration, geographic distribution, and performance correlation.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_delivery_overview(df: pd.DataFrame) -> dict:
    """
    Returns counts and percentages of delivery availability.
    """
    total = len(df)
    counts = df["Has Online delivery"].value_counts().to_dict()
    yes_count = counts.get("Yes", 0)
    no_count = counts.get("No", 0)
    yes_pct = round(yes_count / total * 100, 2)
    no_pct = round(no_count / total * 100, 2)

    # Performance comparison
    rated_df = df[df["Aggregate rating"] > 0]
    rating_with_delivery = round(rated_df[rated_df["Has Online delivery"] == "Yes"]["Aggregate rating"].mean(), 2)
    rating_without_delivery = round(rated_df[rated_df["Has Online delivery"] == "No"]["Aggregate rating"].mean(), 2)
    votes_with_delivery = round(df[df["Has Online delivery"] == "Yes"]["Votes"].mean(), 1)
    votes_without_delivery = round(df[df["Has Online delivery"] == "No"]["Votes"].mean(), 1)

    return {
        "total": total,
        "delivery_yes": yes_count,
        "delivery_no": no_count,
        "delivery_pct": yes_pct,
        "no_delivery_pct": no_pct,
        "rating_with_delivery": rating_with_delivery,
        "rating_without_delivery": rating_without_delivery,
        "votes_with_delivery": votes_with_delivery,
        "votes_without_delivery": votes_without_delivery,
    }


def get_delivery_by_city(df: pd.DataFrame, min_restaurants: int = 20) -> pd.DataFrame:
    """
    Computes online delivery adoption rates across major cities.
    """
    city_grouped = df.groupby("City").agg(
        Total_Restaurants=("Restaurant ID", "count"),
        Delivery_Restaurants=("Has_Online_Delivery_Num", "sum"),
        Delivery_Pct=("Has_Online_Delivery_Num", lambda x: round(x.mean() * 100, 2)),
        Avg_Rating_Rated=("Aggregate rating", lambda x: round(x[x > 0].mean(), 2) if (x > 0).any() else 0.0),
    ).reset_index()

    filtered = city_grouped[city_grouped["Total_Restaurants"] >= min_restaurants]
    return filtered.sort_values(by="Delivery_Pct", ascending=False)


def plot_delivery_pie(df: pd.DataFrame) -> go.Figure:
    """
    Pie chart showing the proportion of restaurants offering online delivery.
    """
    delivery_counts = df["Has Online delivery"].value_counts().reset_index()
    delivery_counts.columns = ["Online_Delivery", "Count"]
    delivery_counts["Label"] = delivery_counts["Online_Delivery"].map(
        {"Yes": "Offers Online Delivery", "No": "No Online Delivery"}
    )

    colors = {"Offers Online Delivery": "#10b981", "No Online Delivery": "#ef4444"}

    fig = px.pie(
        delivery_counts,
        values="Count",
        names="Label",
        title="Online Delivery Availability Overview",
        hole=0.4,
        color="Label",
        color_discrete_map=colors,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_delivery_by_city_bar(city_delivery_df: pd.DataFrame, top_n: int = 12) -> go.Figure:
    """
    Bar chart showing online delivery adoption rate by city.
    """
    top_df = city_delivery_df.head(top_n).sort_values(by="Delivery_Pct", ascending=True)
    fig = px.bar(
        top_df,
        x="Delivery_Pct",
        y="City",
        orientation="h",
        text="Delivery_Pct",
        title=f"Online Delivery Adoption Rate (%) in Top Cities (Min {top_df['Total_Restaurants'].min()} Outlets)",
        labels={"Delivery_Pct": "Delivery Penetration (%)", "City": "City"},
        color="Delivery_Pct",
        color_continuous_scale="Mint",
    )
    fig.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Delivery Rate: %{x:.1f}%<extra></extra>",
    )
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis=dict(range=[0, 105], gridcolor="#e2e8f0"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_rating_comparison_by_delivery(df: pd.DataFrame) -> go.Figure:
    """
    Violin/box plot comparing rating distributions between delivery and non-delivery restaurants.
    """
    rated_df = df[df["Aggregate rating"] > 0]
    fig = px.box(
        rated_df,
        x="Has Online delivery",
        y="Aggregate rating",
        color="Has Online delivery",
        title="Customer Rating Comparison: Delivery vs. Non-Delivery Outlets",
        labels={"Has Online delivery": "Offers Online Delivery", "Aggregate rating": "Aggregate Rating"},
        color_discrete_map={"Yes": "#10b981", "No": "#ef4444"},
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(gridcolor="#e2e8f0"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig
