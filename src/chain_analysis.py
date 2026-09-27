"""
Restaurant Chains Analysis Module for Cognifyz Restaurant Data.
Identifies multi-outlet brand chains and evaluates brand-level rating, voting volume, and delivery adoption.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_top_chains(df: pd.DataFrame, min_outlets: int = 4, top_n: int = 15) -> pd.DataFrame:
    """
    Identifies multi-outlet restaurant chains and computes aggregated brand KPIs.
    """
    chain_summary = df.groupby("Restaurant Name").agg(
        Total_Outlets=("Restaurant ID", "count"),
        Cities_Present=("City", "nunique"),
        Avg_Rating=("Aggregate rating", "mean"),
        Avg_Rating_Rated=("Aggregate rating", lambda x: round(x[x > 0].mean(), 2) if (x > 0).any() else 0.0),
        Total_Votes=("Votes", "sum"),
        Avg_Votes=("Votes", "mean"),
        Most_Common_Price_Range=("Price range", lambda x: x.mode()[0] if not x.empty else 1),
        Online_Delivery_Pct=("Has_Online_Delivery_Num", lambda x: round(x.mean() * 100, 2)),
        Table_Booking_Pct=("Has_Table_Booking_Num", lambda x: round(x.mean() * 100, 2)),
    ).reset_index()

    # Filter chains with multiple locations
    chains = chain_summary[chain_summary["Total_Outlets"] >= min_outlets].copy()
    chains["Avg_Rating"] = chains["Avg_Rating"].round(2)
    chains["Avg_Votes"] = chains["Avg_Votes"].round(1)
    return chains.sort_values(by="Total_Outlets", ascending=False).head(top_n)


def plot_top_chains_outlets_bar(chains_df: pd.DataFrame) -> go.Figure:
    """
    Horizontal bar chart showing the largest restaurant chains by outlet count.
    """
    sorted_df = chains_df.sort_values(by="Total_Outlets", ascending=True)
    fig = px.bar(
        sorted_df,
        x="Total_Outlets",
        y="Restaurant Name",
        orientation="h",
        text="Total_Outlets",
        title="Top Restaurant Chains by Outlet Footprint",
        labels={"Total_Outlets": "Number of Outlets", "Restaurant Name": "Brand / Chain Name"},
        color="Total_Outlets",
        color_continuous_scale="Viridis",
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


def plot_chain_ratings_vs_votes(chains_df: pd.DataFrame) -> go.Figure:
    """
    Scatter plot comparing chain average rating vs total votes (bubble size = outlet count).
    """
    fig = px.scatter(
        chains_df,
        x="Avg_Rating_Rated",
        y="Total_Votes",
        size="Total_Outlets",
        color="Online_Delivery_Pct",
        text="Restaurant Name",
        title="Top Chains: Brand Rating vs. Total Votes (Size = Outlets, Color = Delivery %)",
        labels={
            "Avg_Rating_Rated": "Average Customer Rating (Rated > 0)",
            "Total_Votes": "Total Customer Votes",
            "Online_Delivery_Pct": "Delivery %",
        },
        color_continuous_scale="Plasma",
    )
    fig.update_traces(textposition="top center")
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#e2e8f0"),
        yaxis=dict(gridcolor="#e2e8f0"),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_chain_delivery_comparison(chains_df: pd.DataFrame) -> go.Figure:
    """
    Bar chart showing online delivery adoption percentage across top chains.
    """
    sorted_df = chains_df.sort_values(by="Online_Delivery_Pct", ascending=True)
    fig = px.bar(
        sorted_df,
        x="Online_Delivery_Pct",
        y="Restaurant Name",
        orientation="h",
        text="Online_Delivery_Pct",
        title="Online Delivery Adoption Rate (%) Across Top Chains",
        labels={"Online_Delivery_Pct": "Delivery Available (%)", "Restaurant Name": "Chain"},
        color="Online_Delivery_Pct",
        color_continuous_scale="Teal",
    )
    fig.update_traces(
        texttemplate="%{x:.1f}%",
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>Delivery: %{x:.1f}%<extra></extra>",
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
