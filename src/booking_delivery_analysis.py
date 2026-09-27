"""
Comparative Analysis: Price Range vs. Online Delivery & Table Booking.
Cross-analyzes service availability across price tiers and rating correlations.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_service_cross_tab(df: pd.DataFrame, feature: str = "Has Table booking") -> pd.DataFrame:
    """
    Computes cross-tabulation percentages between Price Tier and selected service.
    """
    ct = pd.crosstab(df["Price_Range_Label"], df[feature], normalize="index") * 100
    ct = ct.round(2).reset_index()
    return ct


def plot_price_vs_booking_bar(df: pd.DataFrame) -> go.Figure:
    """
    Grouped stacked bar chart showing Table Booking availability across price ranges.
    """
    ct = get_service_cross_tab(df, "Has Table booking")
    fig = go.Figure()

    if "Yes" in ct.columns:
        fig.add_trace(go.Bar(
            x=ct["Price_Range_Label"],
            y=ct["Yes"],
            name="Table Booking Available",
            marker_color="#3b82f6",
            text=ct["Yes"].astype(str) + "%",
            textposition="auto",
        ))
    if "No" in ct.columns:
        fig.add_trace(go.Bar(
            x=ct["Price_Range_Label"],
            y=ct["No"],
            name="No Table Booking",
            marker_color="#94a3b8",
            text=ct["No"].astype(str) + "%",
            textposition="auto",
        ))

    fig.update_layout(
        barmode="stack",
        title="Table Booking Availability Across Price Tiers (% Proportion)",
        xaxis_title="Price Tier",
        yaxis_title="Percentage (%)",
        yaxis=dict(range=[0, 105], gridcolor="#e2e8f0"),
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_rating_vs_booking_box(df: pd.DataFrame) -> go.Figure:
    """
    Boxplot showing rating distribution for restaurants with vs without table booking.
    """
    rated_df = df[df["Aggregate rating"] > 0]
    fig = px.box(
        rated_df,
        x="Has Table booking",
        y="Aggregate rating",
        color="Has Table booking",
        title="Customer Rating Comparison: Table Booking vs. Walk-In Outlets",
        labels={"Has Table booking": "Table Booking Available", "Aggregate rating": "Aggregate Rating"},
        color_discrete_map={"Yes": "#3b82f6", "No": "#94a3b8"},
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_service_matrix_comparison(df: pd.DataFrame) -> go.Figure:
    """
    Compares average rating across 4 quadrants:
    (Online Delivery Yes/No) x (Table Booking Yes/No)
    """
    rated_df = df[df["Aggregate rating"] > 0]
    quad = rated_df.groupby(["Has Online delivery", "Has Table booking"]).agg(
        Avg_Rating=("Aggregate rating", "mean"),
        Avg_Votes=("Votes", "mean"),
        Count=("Restaurant ID", "count"),
    ).reset_index()

    quad["Quadrant"] = quad.apply(
        lambda r: f"Delivery: {r['Has Online delivery']} | Booking: {r['Has Table booking']}", axis=1
    )
    quad["Avg_Rating"] = quad["Avg_Rating"].round(2)
    quad["Avg_Votes"] = quad["Avg_Votes"].round(1)

    fig = px.bar(
        quad,
        x="Quadrant",
        y="Avg_Rating",
        text="Avg_Rating",
        color="Quadrant",
        title="Omnichannel Premium: Average Rating by Service Combination",
        labels={"Avg_Rating": "Average Rating (Rated > 0)", "Quadrant": "Service Combination"},
        color_discrete_sequence=["#94a3b8", "#10b981", "#3b82f6", "#8b5cf6"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
        yaxis=dict(range=[0, 5.2], gridcolor="#e2e8f0"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig
