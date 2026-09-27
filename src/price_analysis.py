"""
Price Analysis Module for Cognifyz Restaurant Data.
Analyzes price tier distribution, rating differentials, and delivery availability.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_price_range_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes distribution and performance indicators across price ranges.
    """
    summary = df.groupby("Price_Range_Label").agg(
        Restaurant_Count=("Restaurant ID", "count"),
        Avg_Rating=("Aggregate rating", "mean"),
        Avg_Rating_Rated=("Aggregate rating", lambda x: x[x > 0].mean() if (x > 0).any() else 0.0),
        Avg_Votes=("Votes", "mean"),
        Avg_Cost=("Average Cost for two", "mean"),
        Online_Delivery_Pct=("Has_Online_Delivery_Num", lambda x: round(x.mean() * 100, 2)),
        Table_Booking_Pct=("Has_Table_Booking_Num", lambda x: round(x.mean() * 100, 2)),
    ).reset_index()

    total = len(df)
    summary["Percentage"] = (summary["Restaurant_Count"] / total * 100).round(2)
    summary["Avg_Rating"] = summary["Avg_Rating"].round(2)
    summary["Avg_Rating_Rated"] = summary["Avg_Rating_Rated"].round(2)
    summary["Avg_Votes"] = summary["Avg_Votes"].round(1)
    summary["Avg_Cost"] = summary["Avg_Cost"].round(1)

    # Sort in ascending order of price range
    summary["Sort_Key"] = summary["Price_Range_Label"].apply(lambda x: int(x.split(" - ")[0]) if " - " in x else 0)
    summary = summary.sort_values(by="Sort_Key").drop(columns=["Sort_Key"])
    return summary


def plot_price_distribution_donut(summary_df: pd.DataFrame) -> go.Figure:
    """
    Donut chart of price range distribution.
    """
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"]
    fig = px.pie(
        summary_df,
        values="Restaurant_Count",
        names="Price_Range_Label",
        title="Distribution of Restaurants by Price Tier",
        hole=0.45,
        color_discrete_sequence=colors,
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_rating_by_price_range(df: pd.DataFrame) -> go.Figure:
    """
    Boxplot showing distribution of aggregate ratings across price tiers.
    """
    rated_df = df[df["Aggregate rating"] > 0]
    fig = px.box(
        rated_df,
        x="Price_Range_Label",
        y="Aggregate rating",
        color="Price_Range_Label",
        title="Customer Rating Distribution by Price Tier (Rated Restaurants)",
        labels={"Price_Range_Label": "Price Tier", "Aggregate rating": "Aggregate Rating (0 - 5)"},
        category_orders={"Price_Range_Label": ["1 - Budget", "2 - Mid-Range", "3 - Premium", "4 - Fine Dining"]},
        color_discrete_sequence=["#3b82f6", "#10b981", "#f59e0b", "#ef4444"],
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


def plot_votes_by_price_range(summary_df: pd.DataFrame) -> go.Figure:
    """
    Bar chart showing average votes per restaurant across price tiers.
    """
    fig = px.bar(
        summary_df,
        x="Price_Range_Label",
        y="Avg_Votes",
        text="Avg_Votes",
        title="Average Customer Engagement (Votes) by Price Tier",
        labels={"Price_Range_Label": "Price Tier", "Avg_Votes": "Average Votes per Restaurant"},
        color="Avg_Votes",
        color_continuous_scale="Teal",
    )
    fig.update_traces(textposition="outside", hovertemplate="<b>%{x}</b><br>Avg Votes: %{y:.1f}<extra></extra>")
    fig.update_layout(
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_price_vs_delivery(df: pd.DataFrame) -> go.Figure:
    """
    Grouped bar chart showing online delivery proportion across price ranges.
    """
    cross_tab = pd.crosstab(
        df["Price_Range_Label"],
        df["Has Online delivery"],
        normalize="index"
    ) * 100
    cross_tab = cross_tab.reset_index()

    fig = go.Figure()
    if "Yes" in cross_tab.columns:
        fig.add_trace(go.Bar(
            x=cross_tab["Price_Range_Label"],
            y=cross_tab["Yes"].round(2),
            name="Offers Online Delivery",
            marker_color="#10b981",
            text=cross_tab["Yes"].round(1).astype(str) + "%",
            textposition="auto"
        ))
    if "No" in cross_tab.columns:
        fig.add_trace(go.Bar(
            x=cross_tab["Price_Range_Label"],
            y=cross_tab["No"].round(2),
            name="No Online Delivery",
            marker_color="#ef4444",
            text=cross_tab["No"].round(1).astype(str) + "%",
            textposition="auto"
        ))

    fig.update_layout(
        barmode="stack",
        title="Online Delivery Availability Across Price Tiers (% Breakdown)",
        xaxis_title="Price Tier",
        yaxis_title="Percentage (%)",
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        yaxis=dict(gridcolor="#e2e8f0", range=[0, 105]),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig
