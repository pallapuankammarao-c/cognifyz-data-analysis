"""
Geographic Analysis Module for Cognifyz Restaurant Data.
Maps restaurant locations, density concentrations, and geographic ratings using Plotly.
Includes graceful error handling and fallback checks for missing coordinate attributes.
Compatible with Plotly v5, v6, and v7+.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def check_geographic_columns(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Validates whether required spatial coordinates are available in the DataFrame.
    """
    required_cols = ["Latitude", "Longitude"]
    for col in required_cols:
        if col not in df.columns:
            return False, f"Missing required spatial column '{col}' in dataset."

    valid_count = df["Valid_Coords"].sum() if "Valid_Coords" in df.columns else (
        (df["Latitude"] != 0) & (df["Longitude"] != 0)
    ).sum()

    if valid_count == 0:
        return False, "No valid non-zero latitude/longitude coordinates found in the dataset."

    return True, f"Found {valid_count:,} restaurants with valid geographical coordinates."


def get_geographic_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filters dataset for valid latitude and longitude coordinates.
    """
    if "Valid_Coords" in df.columns:
        valid_df = df[df["Valid_Coords"]].copy()
    else:
        valid_df = df[
            (df["Latitude"] != 0.0)
            & (df["Longitude"] != 0.0)
            & (df["Latitude"].between(-90, 90))
            & (df["Longitude"].between(-180, 180))
        ].copy()
    return valid_df


def plot_restaurant_map(
    geo_df: pd.DataFrame,
    color_col: str = "Aggregate rating",
    sample_size: int = 2500,
    selected_city: str = "All",
) -> go.Figure:
    """
    Creates an interactive scatter geo map of restaurant locations.
    Automatically supports Plotly v7+ (scatter_map) and legacy Plotly (scatter_mapbox).
    """
    data = geo_df.copy()
    if selected_city != "All":
        data = data[data["City"] == selected_city]

    if len(data) > sample_size:
        data = data.sample(sample_size, random_state=42)

    center_lat = float(data["Latitude"].mean()) if len(data) > 0 else 20.0
    center_lon = float(data["Longitude"].mean()) if len(data) > 0 else 77.0
    zoom_level = 10 if selected_city != "All" else 3

    # Ensure hover_data only includes columns present in the dataframe
    possible_hover = [
        ("City", True),
        ("Cuisines", True),
        ("Price_Range_Label", True),
        ("Aggregate rating", ":.1f"),
        ("Votes", ":,"),
        ("Latitude", False),
        ("Longitude", False),
    ]
    safe_hover_data = {col: fmt for col, fmt in possible_hover if col in data.columns}

    common_kwargs = dict(
        lat="Latitude",
        lon="Longitude",
        color=color_col if color_col in data.columns else None,
        size="Votes" if "Votes" in data.columns and (data["Votes"] > 0).any() else None,
        size_max=18,
        hover_name="Restaurant Name" if "Restaurant Name" in data.columns else None,
        hover_data=safe_hover_data,
        title=f"Geographic Distribution of Restaurants (Color: {color_col} - Sample: {len(data):,})",
        color_continuous_scale="Plasma",
        zoom=zoom_level,
        center=dict(lat=center_lat, lon=center_lon),
    )

    try:
        # Plotly v6/v7+
        if hasattr(px, "scatter_map"):
            fig = px.scatter_map(data, map_style="open-street-map", **common_kwargs)
        # Legacy Plotly v5
        elif hasattr(px, "scatter_mapbox"):
            fig = px.scatter_mapbox(data, mapbox_style="open-street-map", **common_kwargs)
        else:
            fig = px.scatter_geo(data, lat="Latitude", lon="Longitude", color=color_col, title="Geographic Distribution of Restaurants")
    except Exception:
        # Fallback to scatter_geo if tile service is blocked
        fig = px.scatter_geo(
            data,
            lat="Latitude",
            lon="Longitude",
            color=color_col if color_col in data.columns else None,
            hover_name="Restaurant Name" if "Restaurant Name" in data.columns else None,
            title="Geographic Distribution of Restaurants (Global Geo View)"
        )

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig


def plot_density_map(geo_df: pd.DataFrame, selected_city: str = "All") -> go.Figure:
    """
    Creates a density heatmap map to identify restaurant cluster concentration.
    Automatically supports Plotly v7+ (density_map) and legacy Plotly (density_mapbox).
    """
    data = geo_df.copy()
    if selected_city != "All":
        data = data[data["City"] == selected_city]

    center_lat = float(data["Latitude"].mean()) if len(data) > 0 else 28.6
    center_lon = float(data["Longitude"].mean()) if len(data) > 0 else 77.2
    zoom_level = 10 if selected_city != "All" else 3

    common_density_kwargs = dict(
        lat="Latitude",
        lon="Longitude",
        z="Votes" if "Votes" in data.columns else None,
        radius=12,
        center=dict(lat=center_lat, lon=center_lon),
        zoom=zoom_level,
        title="Restaurant Density and Customer Engagement Heatmap (Weighted by Votes)",
    )

    try:
        # Plotly v6/v7+
        if hasattr(px, "density_map"):
            fig = px.density_map(data, map_style="open-street-map", **common_density_kwargs)
        # Legacy Plotly v5
        elif hasattr(px, "density_mapbox"):
            fig = px.density_mapbox(data, mapbox_style="open-street-map", **common_density_kwargs)
        else:
            fig = px.density_heatmap(data, x="Longitude", y="Latitude", z="Votes", title="Restaurant Density Heatmap")
    except Exception:
        fig = px.density_heatmap(data, x="Longitude", y="Latitude", z="Votes" if "Votes" in data.columns else None, title="Restaurant Density Heatmap")

    fig.update_layout(
        margin=dict(l=10, r=10, t=50, b=10),
        font=dict(family="Arial, sans-serif", size=12),
    )
    return fig
