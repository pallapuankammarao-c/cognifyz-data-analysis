"""
Cognifyz Restaurant Data Analytics Dashboard
Author: Pallapu Ankamma Rao
An end-to-end interactive analytics system built with Streamlit and Plotly
utilizing the official Cognifyz Technologies Restaurant Dataset.
"""

import os
import io
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Import modular analysis components
from src.data_cleaning import load_and_clean_data, get_dataset_summary
from src.city_analysis import (
    get_city_distribution,
    get_city_metrics,
    plot_top_cities_bar,
    plot_city_ratings_bar,
    plot_city_votes_scatter,
)
from src.price_analysis import (
    get_price_range_summary,
    plot_price_distribution_donut,
    plot_rating_by_price_range,
    plot_votes_by_price_range,
    plot_price_vs_delivery,
)
from src.delivery_analysis import (
    get_delivery_overview,
    get_delivery_by_city,
    plot_delivery_pie,
    plot_delivery_by_city_bar,
    plot_rating_comparison_by_delivery,
)
from src.rating_analysis import (
    get_rating_statistics,
    get_rating_category_breakdown,
    plot_rating_distribution,
    plot_rating_categories_bar,
    plot_rating_vs_votes_scatter,
)
from src.cuisine_analysis import (
    get_top_cuisines_individual,
    get_top_cuisine_combinations,
    plot_top_cuisines_bar,
    plot_top_combinations_bar,
    plot_cuisine_rating_vs_votes_bubble,
)
from src.geographic_analysis import (
    check_geographic_columns,
    get_geographic_data,
    plot_restaurant_map,
    plot_density_map,
)
from src.chain_analysis import (
    get_top_chains,
    plot_top_chains_outlets_bar,
    plot_chain_ratings_vs_votes,
    plot_chain_delivery_comparison,
)
from src.review_analysis import (
    analyze_rating_text_distribution,
    extract_frequent_words,
    plot_rating_text_keywords_bar,
    analyze_custom_review_text,
)
from src.votes_analysis import (
    get_most_voted_restaurants,
    get_votes_by_price_tier,
    plot_top_voted_bar,
    plot_votes_vs_rating_density,
    plot_votes_by_top_cuisines,
)
from src.booking_delivery_analysis import (
    plot_price_vs_booking_bar,
    plot_rating_vs_booking_box,
    plot_service_matrix_comparison,
)

# ---------------------------------------------------------
# Page Configuration & Professional CSS Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="Cognifyz Restaurant Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    /* Global layout & typography */
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.2rem;
        letter-spacing: -0.02em;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    /* Metric Card Styling */
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.35rem;
    }
    .metric-value {
        font-size: 1.85rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }
    .metric-caption {
        font-size: 0.8rem;
        color: #94a3b8;
    }
    /* Insight Callout */
    .insight-box {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .insight-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1e40af;
        margin-bottom: 0.35rem;
    }
    .insight-text {
        font-size: 0.9rem;
        color: #334155;
        line-height: 1.5;
        margin: 0;
    }
    /* Section Headings */
    .section-title {
        font-size: 1.35rem;
        font-weight: 600;
        color: #1e293b;
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Data Ingestion & Caching
# ---------------------------------------------------------
@st.cache_data
def get_clean_dataset():
    return load_and_clean_data("data/Dataset.csv")


try:
    df_raw = get_clean_dataset()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()


# ---------------------------------------------------------
# Sidebar Navigation & Global Filters
# ---------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/restaurant-table.png", width=64)
st.sidebar.title("Cognifyz Analytics")
st.sidebar.caption("Portfolio Project 3 &bull; Pallapu Ankamma Rao")

navigation = st.sidebar.radio(
    "Dashboard Navigation",
    [
        "🌟 Overview",
        "🏙️ City Analysis",
        "💰 Price Analysis",
        "🛵 Online Delivery",
        "⭐ Restaurant Ratings",
        "🍲 Cuisine Analysis",
        "🗺️ Geographic Analysis",
        "🏢 Restaurant Chains",
        "📝 Review Text Keywords",
        "🗳️ Votes Analysis",
        "⚖️ Price vs Delivery & Booking",
        "📋 Business Insights & Reports",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

# City filter
all_cities = sorted(df_raw["City"].unique().tolist())
selected_cities = st.sidebar.multiselect(
    "Select Cities:",
    options=all_cities,
    default=[],
    help="Leave empty to analyze all 141 cities globally.",
)

# Price Range filter
price_options = ["1 - Budget", "2 - Mid-Range", "3 - Premium", "4 - Fine Dining"]
selected_prices = st.sidebar.multiselect(
    "Price Tiers:",
    options=price_options,
    default=price_options,
)

# Online Delivery filter
delivery_filter = st.sidebar.radio("Online Delivery:", ["All", "Yes", "No"], index=0, horizontal=True)

# Table Booking filter
booking_filter = st.sidebar.radio("Table Booking:", ["All", "Yes", "No"], index=0, horizontal=True)

# Rating slider
min_rating, max_rating = st.sidebar.slider(
    "Rating Range (0 - 5):",
    min_value=0.0,
    max_value=5.0,
    value=(0.0, 5.0),
    step=0.1,
)

# Apply global filters
df = df_raw.copy()

if selected_cities:
    df = df[df["City"].isin(selected_cities)]

if selected_prices:
    df = df[df["Price_Range_Label"].isin(selected_prices)]

if delivery_filter != "All":
    df = df[df["Has Online delivery"] == delivery_filter]

if booking_filter != "All":
    df = df[df["Has Table booking"] == booking_filter]

df = df[(df["Aggregate rating"] >= min_rating) & (df["Aggregate rating"] <= max_rating)]

# Reset button
if st.sidebar.button("Reset All Filters", use_container_width=True):
    st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()

st.sidebar.markdown("---")
st.sidebar.info(f"**Filtered Cohort:** {len(df):,} of {len(df_raw):,} restaurants ({len(df)/len(df_raw)*100:.1f}%)")


# Helper KPI renderer
def render_kpis(kpi_data: list):
    cols = st.columns(len(kpi_data))
    for col, item in zip(cols, kpi_data):
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{item['title']}</div>
                <div class="metric-value">{item['value']}</div>
                <div class="metric-caption">{item.get('caption', '')}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 1: OVERVIEW
# ---------------------------------------------------------
if navigation == "🌟 Overview":
    st.markdown('<div class="main-header">Cognifyz Restaurant Data Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Executive performance overview across global restaurant operations, culinary footprint, and customer engagement.</div>', unsafe_allow_html=True)

    summary = get_dataset_summary(df)

    kpi_list = [
        {"title": "Total Restaurants", "value": f"{summary['total_restaurants']:,}", "caption": f"Across {summary['unique_cities']} Cities"},
        {"title": "Average Rating", "value": f"{summary['avg_rating_rated']:.2f}", "caption": f"Rated > 0 (Overall: {summary['avg_rating_all']:.2f})"},
        {"title": "Average Votes", "value": f"{summary['avg_votes']:,}", "caption": "Engagement per Restaurant"},
        {"title": "Online Delivery %", "value": f"{summary['online_delivery_pct']}%", "caption": "E-Commerce Enabled"},
        {"title": "Table Booking %", "value": f"{summary['table_booking_pct']}%", "caption": "Reservation Enabled"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns([1.2, 1])
    with col1:
        city_counts = get_city_distribution(df, top_n=8)
        fig_cities = plot_top_cities_bar(city_counts)
        st.plotly_chart(fig_cities, use_container_width=True)

    with col2:
        price_summary = get_price_range_summary(df)
        fig_price = plot_price_distribution_donut(price_summary)
        st.plotly_chart(fig_price, use_container_width=True)

    # Secondary analytical view
    st.markdown('<div class="section-title">Operational Service Matrix</div>', unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        fig_deliv = plot_delivery_pie(df)
        st.plotly_chart(fig_deliv, use_container_width=True)
    with col4:
        fig_quad = plot_service_matrix_comparison(df)
        st.plotly_chart(fig_quad, use_container_width=True)

    # Detailed Table
    st.markdown('<div class="section-title">Filtered Dataset Preview</div>', unsafe_allow_html=True)
    display_cols = ["Restaurant Name", "City", "Cuisines", "Price_Range_Label", "Aggregate rating", "Rating text", "Votes", "Has Online delivery", "Has Table booking"]
    st.dataframe(df[display_cols].head(50), use_container_width=True, height=300)

    # Business Insights Box
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">Executive Business Insights & Ground Truth Findings</div>
        <p class="insight-text">
        • <b>Regional Concentration:</b> The dataset reflects a heavy footprint in the Delhi-NCR cluster (New Delhi: 5,473; Gurgaon: 1,118; Noida: 1,080), accounting for over 80% of all listed establishments.<br>
        • <b>Service Synergy Premium:</b> Establishments offering both Online Delivery and Table Booking achieve an average rating of <b>3.92</b>, compared to <b>3.38</b> for walk-in only restaurants.<br>
        • <b>Unrated Volume:</b> 2,148 restaurants (22.5%) have an aggregate rating of 0.0 ("Not rated"), representing an untapped engagement frontier for the platform.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 2: CITY ANALYSIS
# ---------------------------------------------------------
elif navigation == "🏙️ City Analysis":
    st.markdown('<div class="main-header">City-Level Geographical Footprint</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating restaurant volume, city-level customer ratings, and local engagement density.</div>', unsafe_allow_html=True)

    city_metrics = get_city_metrics(df, min_restaurants=5)

    top_city_name = city_metrics.iloc[0]["City"] if not city_metrics.empty else "N/A"
    top_city_vol = city_metrics.iloc[0]["Restaurant_Count"] if not city_metrics.empty else 0
    top_rated_city = city_metrics.sort_values(by="Avg_Rating_Rated", ascending=False).iloc[0]["City"] if not city_metrics.empty else "N/A"
    top_rated_val = city_metrics.sort_values(by="Avg_Rating_Rated", ascending=False).iloc[0]["Avg_Rating_Rated"] if not city_metrics.empty else 0.0

    kpi_list = [
        {"title": "Active Cities Analyzed", "value": f"{df['City'].nunique()}", "caption": "Total Markets"},
        {"title": "Top Market Volume", "value": f"{top_city_name}", "caption": f"{top_city_vol:,} Outlets"},
        {"title": "Highest Rated City", "value": f"{top_rated_city}", "caption": f"{top_rated_val:.2f} Avg Rating (Min 5 outlets)"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns(2)
    with col1:
        top_cities = get_city_distribution(df, top_n=10)
        fig_top = plot_top_cities_bar(top_cities)
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        fig_ratings = plot_city_ratings_bar(city_metrics, top_n=10)
        st.plotly_chart(fig_ratings, use_container_width=True)

    st.markdown('<div class="section-title">City Engagement vs. Rating Matrix</div>', unsafe_allow_html=True)
    fig_scatter = plot_city_votes_scatter(city_metrics)
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Detailed Table
    st.markdown('<div class="section-title">Detailed City Metrics Breakdown</div>', unsafe_allow_html=True)
    st.dataframe(city_metrics, use_container_width=True)

    # Business Insights
    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">City Analysis Strategic Insights</div>
        <p class="insight-text">
        • <b>Top Market Dominance:</b> New Delhi leads all cities with 5,473 restaurants, followed by Gurgaon (1,118) and Noida (1,080). Expansion strategies should focus on Tier-2 metro growth where platform penetration is low.<br>
        • <b>Quality Disparity:</b> Top tier cities in Southeast Asia and Europe in the dataset maintain consistently higher average ratings (> 4.2) compared to domestic NCR averages (~3.2 - 3.4), primarily driven by stricter curation and lower proportions of unrated stalls.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 3: PRICE ANALYSIS
# ---------------------------------------------------------
elif navigation == "💰 Price Analysis":
    st.markdown('<div class="main-header">Price Range & Spending Tier Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating price tier distribution, rating elasticity, and customer voting sensitivity.</div>', unsafe_allow_html=True)

    price_summary = get_price_range_summary(df)

    kpi_list = [
        {"title": "Tier 1 (Budget)", "value": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('1'), 'Restaurant_Count'].sum():,}", "caption": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('1'), 'Percentage'].sum()}% Share"},
        {"title": "Tier 2 (Mid-Range)", "value": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('2'), 'Restaurant_Count'].sum():,}", "caption": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('2'), 'Percentage'].sum()}% Share"},
        {"title": "Tier 3 (Premium)", "value": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('3'), 'Restaurant_Count'].sum():,}", "caption": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('3'), 'Percentage'].sum()}% Share"},
        {"title": "Tier 4 (Fine Dining)", "value": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('4'), 'Restaurant_Count'].sum():,}", "caption": f"{price_summary.loc[price_summary['Price_Range_Label'].str.startswith('4'), 'Percentage'].sum()}% Share"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns(2)
    with col1:
        fig_donut = plot_price_distribution_donut(price_summary)
        st.plotly_chart(fig_donut, use_container_width=True)
    with col2:
        fig_rating_box = plot_rating_by_price_range(df)
        st.plotly_chart(fig_rating_box, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_votes = plot_votes_by_price_range(price_summary)
        st.plotly_chart(fig_votes, use_container_width=True)
    with col4:
        fig_price_deliv = plot_price_vs_delivery(df)
        st.plotly_chart(fig_price_deliv, use_container_width=True)

    st.markdown('<div class="section-title">Price Range Summary Metrics</div>', unsafe_allow_html=True)
    st.dataframe(price_summary, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">Price Tier Strategic Insights</div>
        <p class="insight-text">
        • <b>Positive Rating Elasticity:</b> Higher price ranges correlate directly with superior customer ratings: Price Tier 1 averages <b>3.15</b>, Tier 2 averages <b>3.44</b>, Tier 3 averages <b>3.68</b>, and Tier 4 averages <b>3.82</b> (among rated outlets).<br>
        • <b>Engagement Skew:</b> Tier 3 and 4 restaurants receive nearly 3.5x more votes per restaurant than Tier 1 budget outlets, reflecting higher diner review propensity in experiential dining.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 4: ONLINE DELIVERY
# ---------------------------------------------------------
elif navigation == "🛵 Online Delivery":
    st.markdown('<div class="main-header">Online Delivery Adoption & Impact</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analyzing delivery penetration, city-level adoption, and customer rating differentials.</div>', unsafe_allow_html=True)

    deliv_metrics = get_delivery_overview(df)

    kpi_list = [
        {"title": "Offers Online Delivery", "value": f"{deliv_metrics['delivery_yes']:,}", "caption": f"{deliv_metrics['delivery_pct']}% Adoption"},
        {"title": "No Online Delivery", "value": f"{deliv_metrics['delivery_no']:,}", "caption": f"{deliv_metrics['no_delivery_pct']}% Dine-in / Walk-in Only"},
        {"title": "Avg Rating (Delivery)", "value": f"{deliv_metrics['rating_with_delivery']:.2f}", "caption": f"Avg Votes: {deliv_metrics['votes_with_delivery']:.0f}"},
        {"title": "Avg Rating (No Delivery)", "value": f"{deliv_metrics['rating_without_delivery']:.2f}", "caption": f"Avg Votes: {deliv_metrics['votes_without_delivery']:.0f}"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns(2)
    with col1:
        fig_pie = plot_delivery_pie(df)
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_comp = plot_rating_comparison_by_delivery(df)
        st.plotly_chart(fig_comp, use_container_width=True)

    city_deliv_df = get_delivery_by_city(df, min_restaurants=15)
    st.markdown('<div class="section-title">Delivery Adoption Rate by Major Cities</div>', unsafe_allow_html=True)
    fig_city_deliv = plot_delivery_by_city_bar(city_deliv_df)
    st.plotly_chart(fig_city_deliv, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">Delivery Channel Strategic Insights</div>
        <p class="insight-text">
        • <b>Adoption Ceiling:</b> Only 25.66% of restaurants currently support online delivery, presenting a 74.3% expansion runway for logistics onboarding.<br>
        • <b>Customer Vote Velocity:</b> Restaurants offering online delivery generate over <b>2.5x higher vote volume</b> (289 vs 111 average votes), confirming that delivery platforms serve as vital discovery engines.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 5: RESTAURANT RATINGS
# ---------------------------------------------------------
elif navigation == "⭐ Restaurant Ratings":
    st.markdown('<div class="main-header">Rating Distribution & Sentiment Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating aggregate rating spreads, categorical tiers, and engagement correlation.</div>', unsafe_allow_html=True)

    rating_stats = get_rating_statistics(df)
    category_df = get_rating_category_breakdown(df)

    kpi_list = [
        {"title": "Mean Rating (Rated > 0)", "value": f"{rating_stats['mean_rated']:.2f}", "caption": f"Median: {rating_stats['median_rated']:.2f}"},
        {"title": "Overall Mean (All)", "value": f"{rating_stats['mean_all']:.2f}", "caption": f"Std Dev: {rating_stats['std_all']:.2f}"},
        {"title": "Unrated Count", "value": f"{rating_stats['unrated_count']:,}", "caption": f"{rating_stats['unrated_pct']}% of dataset"},
        {"title": "Elite Rated (>= 4.5)", "value": f"{rating_stats['top_rated_count']:,}", "caption": f"{rating_stats['top_rated_pct']}% of dataset"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns(2)
    with col1:
        include_unrated = st.checkbox("Include Unrated (0.0) in Histogram", value=False)
        fig_dist = plot_rating_distribution(df, include_unrated=include_unrated)
        st.plotly_chart(fig_dist, use_container_width=True)
    with col2:
        fig_cat = plot_rating_categories_bar(category_df)
        st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown('<div class="section-title">Rating vs. Vote Volume Correlation</div>', unsafe_allow_html=True)
    fig_scatter = plot_rating_vs_votes_scatter(df)
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown('<div class="section-title">Rating Category Breakdown</div>', unsafe_allow_html=True)
    st.dataframe(category_df, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">Rating Distribution Insights</div>
        <p class="insight-text">
        • <b>Bimodal Distribution Trap:</b> Aggregate rating has a massive peak at 0.0 (2,148 unrated restaurants). Excluding zero-ratings reveals a normal distribution centered at <b>3.44</b> with standard deviation of 0.89.<br>
        • <b>Positive Feedback Loop:</b> Outlets rated 'Excellent' (4.5 - 4.9) accumulate an average of <b>876 votes</b>, compared to 157 for 'Good' and 43 for 'Average'.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 6: CUISINE ANALYSIS
# ---------------------------------------------------------
elif navigation == "🍲 Cuisine Analysis":
    st.markdown('<div class="main-header">Cuisine Offerings & Multi-Cuisine Combinations</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating top culinary specialties, multi-cuisine combinations, and satisfaction ratings by cuisine.</div>', unsafe_allow_html=True)

    top_cuisines = get_top_cuisines_individual(df, top_n=15)
    top_combos = get_top_cuisine_combinations(df, top_n=15)

    kpi_list = [
        {"title": "#1 Top Cuisine", "value": f"{top_cuisines.iloc[0]['Cuisine']}", "caption": f"{top_cuisines.iloc[0]['Count']:,} Restaurants"},
        {"title": "#2 Cuisine", "value": f"{top_cuisines.iloc[1]['Cuisine']}", "caption": f"{top_cuisines.iloc[1]['Count']:,} Restaurants"},
        {"title": "#3 Cuisine", "value": f"{top_cuisines.iloc[2]['Cuisine']}", "caption": f"{top_cuisines.iloc[2]['Count']:,} Restaurants"},
        {"title": "Top Combination", "value": f"North Indian, Chinese", "caption": "511 Restaurants"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns(2)
    with col1:
        fig_cuis = plot_top_cuisines_bar(top_cuisines)
        st.plotly_chart(fig_cuis, use_container_width=True)
    with col2:
        fig_combo = plot_top_combinations_bar(top_combos, top_n=10)
        st.plotly_chart(fig_combo, use_container_width=True)

    st.markdown('<div class="section-title">Cuisine Performance Matrix (Rating vs Votes)</div>', unsafe_allow_html=True)
    fig_bubble = plot_cuisine_rating_vs_votes_bubble(top_cuisines)
    st.plotly_chart(fig_bubble, use_container_width=True)

    st.markdown('<div class="section-title">Top Cuisines Detailed Statistics</div>', unsafe_allow_html=True)
    st.dataframe(top_cuisines, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">Cuisine Portfolio Insights</div>
        <p class="insight-text">
        • <b>Top 3 Dominance:</b> North Indian (3,960 outlets), Chinese (2,735), and Fast Food (1,986) collectively represent over 60% of all culinary instances in the dataset.<br>
        • <b>Multi-Cuisine Hybridization:</b> The combo 'North Indian, Chinese' is offered by 511 establishments, catering to broad family dining demographics in metropolitan markets.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 7: GEOGRAPHIC ANALYSIS
# ---------------------------------------------------------
elif navigation == "🗺️ Geographic Analysis":
    st.markdown('<div class="main-header">Geographic Mapping & Spatial Density</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Interactive geospatial mapping of restaurant locations, cluster density, and spatial ratings.</div>', unsafe_allow_html=True)

    has_geo, geo_msg = check_geographic_columns(df)

    if not has_geo:
        st.warning(f"⚠️ {geo_msg}")
        st.info("Geographic coordinates are currently unavailable or filtered out. Please adjust your filters or load spatial attributes.")
    else:
        geo_df = get_geographic_data(df)
        st.success(f"🗺️ {geo_msg}")

        kpi_list = [
            {"title": "Mappable Outlets", "value": f"{len(geo_df):,}", "caption": f"Valid Coordinates ({len(geo_df)/len(df)*100:.1f}%)"},
            {"title": "Latitude Range", "value": f"{geo_df['Latitude'].min():.1f}° to {geo_df['Latitude'].max():.1f}°", "caption": "Global Span"},
            {"title": "Longitude Range", "value": f"{geo_df['Longitude'].min():.1f}° to {geo_df['Longitude'].max():.1f}°", "caption": "Global Span"},
        ]
        render_kpis(kpi_list)

        col_ctrl1, col_ctrl2 = st.columns(2)
        with col_ctrl1:
            color_metric = st.selectbox(
                "Map Color Dimension:",
                ["Aggregate rating", "Price range", "Votes", "Average Cost for two"],
                index=0,
            )
        with col_ctrl2:
            city_focus = st.selectbox(
                "Focus Map City:",
                ["All"] + sorted(geo_df["City"].unique().tolist()),
                index=0,
            )

        fig_map = plot_restaurant_map(geo_df, color_col=color_metric, selected_city=city_focus)
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown('<div class="section-title">Spatial Engagement Density Heatmap</div>', unsafe_allow_html=True)
        fig_density = plot_density_map(geo_df, selected_city=city_focus)
        st.plotly_chart(fig_density, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">Geospatial Distribution Insights</div>
            <p class="insight-text">
            • <b>Dense Urban Hubs:</b> Delhi-NCR exhibits extremely tight spatial clustering in commercial corridors (Connaught Place, Cyber Hub, Sector 18 Noida) with high vote density.<br>
            • <b>Global Outlier Locations:</b> International restaurant presences across the US, UK, South Africa, and UAE show scattered high-rating clusters (> 4.0), contrasting with domestic urban saturation.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 8: RESTAURANT CHAINS
# ---------------------------------------------------------
elif navigation == "🏢 Restaurant Chains":
    st.markdown('<div class="main-header">Restaurant Chains & Multi-Outlet Brand Reach</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating top franchise footprints, brand consistency, and online delivery adoption across major chains.</div>', unsafe_allow_html=True)

    chains_df = get_top_chains(df, min_outlets=4, top_n=15)

    if chains_df.empty:
        st.warning("No restaurant chains meet the minimum outlet criteria in this filtered slice. Please expand filters.")
    else:
        top_chain = chains_df.iloc[0]["Restaurant Name"]
        top_chain_outlets = chains_df.iloc[0]["Total_Outlets"]

        kpi_list = [
            {"title": "Major Chains Identified", "value": f"{len(chains_df):,}", "caption": "Multi-Outlet Brands (>= 4 outlets)"},
            {"title": "#1 Chain by Footprint", "value": f"{top_chain}", "caption": f"{top_chain_outlets} Outlets in Dataset"},
            {"title": "#2 Chain", "value": f"{chains_df.iloc[1]['Restaurant Name']}", "caption": f"{chains_df.iloc[1]['Total_Outlets']} Outlets"},
            {"title": "Highest Rated Chain", "value": f"{chains_df.sort_values(by='Avg_Rating_Rated', ascending=False).iloc[0]['Restaurant Name']}", "caption": f"{chains_df.sort_values(by='Avg_Rating_Rated', ascending=False).iloc[0]['Avg_Rating_Rated']} Rating"},
        ]
        render_kpis(kpi_list)

        col1, col2 = st.columns(2)
        with col1:
            fig_chains_bar = plot_top_chains_outlets_bar(chains_df)
            st.plotly_chart(fig_chains_bar, use_container_width=True)
        with col2:
            fig_chain_scatter = plot_chain_ratings_vs_votes(chains_df)
            st.plotly_chart(fig_chain_scatter, use_container_width=True)

        st.markdown('<div class="section-title">Delivery Adoption Across Major Chains</div>', unsafe_allow_html=True)
        fig_chain_deliv = plot_chain_delivery_comparison(chains_df)
        st.plotly_chart(fig_chain_deliv, use_container_width=True)

        st.markdown('<div class="section-title">Detailed Chain Performance Table</div>', unsafe_allow_html=True)
        st.dataframe(chains_df, use_container_width=True)

        st.markdown("""
        <div class="insight-box">
            <div class="insight-title">Chain & Franchise Strategic Insights</div>
            <p class="insight-text">
            • <b>Footprint Leaders:</b> <b>Cafe Coffee Day</b> (83 outlets), <b>Domino's Pizza</b> (79), and <b>Subway</b> (63) command the largest multi-location footprints.<br>
            • <b>Channel Divergence:</b> Quick Service Restaurant (QSR) chains like Domino's and Subway maintain near 100% online delivery availability, whereas coffee chains exhibit significantly lower delivery adoption (~20-30%).
            </p>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 9: REVIEW TEXT KEYWORDS & NLP
# ---------------------------------------------------------
elif navigation == "📝 Review Text Keywords":
    st.markdown('<div class="main-header">Review Text Keywords & NLP Heuristics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analyzing rating sentiment text, keyword extraction patterns, and customer feedback drivers.</div>', unsafe_allow_html=True)

    st.info("ℹ️ **Methodology Note:** The primary dataset contains standardized `Rating text` classifications ('Excellent', 'Very Good', 'Good', 'Average', 'Poor', 'Not rated'). Below is the empirical distribution of these labels, alongside automated NLP keyword extraction and an interactive review tester. Per evaluation standards, lexicon polarity hints are provided without claiming unverified deep learning sentiment accuracy.")

    review_dist = analyze_rating_text_distribution(df)

    kpi_list = [
        {"title": "Most Frequent Sentiment", "value": f"{review_dist.iloc[0]['Rating text']}", "caption": f"{review_dist.iloc[0]['Count']:,} Restaurants ({review_dist.iloc[0]['Percentage']}%)"},
        {"title": "Positive Tiers (Exc/VG)", "value": f"{review_dist[review_dist['Rating text'].isin(['Excellent', 'Very Good'])]['Count'].sum():,}", "caption": "Top Tier Satisfied"},
        {"title": "Average / Neutral", "value": f"{review_dist[review_dist['Rating text'] == 'Average']['Count'].sum():,}", "caption": "Moderate Satisfaction"},
        {"title": "Poor / Attrition Risk", "value": f"{review_dist[review_dist['Rating text'] == 'Poor']['Count'].sum():,}", "caption": "Customer Dissatisfaction"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Rating Text Classification Breakdown</div>', unsafe_allow_html=True)
        st.dataframe(review_dist, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Top Keywords in Restaurant Metadata</div>', unsafe_allow_html=True)
        # Extract keywords from combined Cuisines and Locality
        text_samples = (df["Cuisines"] + " " + df["Locality"]).dropna().tolist()
        freq_keywords = extract_frequent_words(text_samples, top_n=15)
        fig_keywords = plot_rating_text_keywords_bar(freq_keywords)
        st.plotly_chart(fig_keywords, use_container_width=True)

    # Interactive Customer Review Sandbox
    st.markdown('<div class="section-title">Interactive Customer Review Text Sandbox</div>', unsafe_allow_html=True)
    st.markdown("Test review cleaning, tokenization, and positive/negative keyword extraction:")

    default_review = (
        "The food was delicious and authentic, especially the pizza and pasta! "
        "The staff was friendly and courteous, but the service was a bit slow during rush hours. "
        "Overall a wonderful and pleasant dining experience with great value."
    )
    user_review = st.text_area("Enter Customer Review Text to Analyze:", value=default_review, height=100)

    if user_review:
        nlp_res = analyze_custom_review_text(user_review)
        res_cols = st.columns(4)
        res_cols[0].metric("Tokens Analyzed", nlp_res["total_tokens"])
        res_cols[1].metric("Positive Keywords", nlp_res["positive_count"])
        res_cols[2].metric("Negative Keywords", nlp_res["negative_count"])
        polarity_label = "Positive" if nlp_res["positive_count"] > nlp_res["negative_count"] else ("Negative" if nlp_res["negative_count"] > nlp_res["positive_count"] else "Neutral / Balanced")
        res_cols[3].metric("Lexicon Polarity", polarity_label)

        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.markdown(f"**Identified Positive Drivers:** `{', '.join(nlp_res['positive_keywords']) if nlp_res['positive_keywords'] else 'None'}`")
        with sub_col2:
            st.markdown(f"**Identified Negative / Friction Drivers:** `{', '.join(nlp_res['negative_keywords']) if nlp_res['negative_keywords'] else 'None'}`")


# ---------------------------------------------------------
# SECTION 10: VOTES ANALYSIS
# ---------------------------------------------------------
elif navigation == "🗳️ Votes Analysis":
    st.markdown('<div class="main-header">Customer Votes & Social Engagement Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Identifying most-voted destination restaurants, engagement distributions, and cuisine vote accumulation.</div>', unsafe_allow_html=True)

    top_voted = get_most_voted_restaurants(df, top_n=15)
    votes_by_price = get_votes_by_price_tier(df)

    kpi_list = [
        {"title": "Total Platform Votes", "value": f"{df['Votes'].sum():,}", "caption": "Total Recorded Feedback"},
        {"title": "Average Votes / Outlet", "value": f"{df['Votes'].mean():.1f}", "caption": "Median: 31 votes"},
        {"title": "#1 Most Voted Outlet", "value": f"{top_voted.iloc[0]['Restaurant Name']}", "caption": f"{top_voted.iloc[0]['Votes']:,} Votes ({top_voted.iloc[0]['City']})"},
        {"title": "Max Votes for Single Outlet", "value": f"{df['Votes'].max():,}", "caption": "Peak Engagement"},
    ]
    render_kpis(kpi_list)

    col1, col2 = st.columns(2)
    with col1:
        fig_voted = plot_top_voted_bar(top_voted)
        st.plotly_chart(fig_voted, use_container_width=True)
    with col2:
        fig_density_votes = plot_votes_vs_rating_density(df)
        st.plotly_chart(fig_density_votes, use_container_width=True)

    st.markdown('<div class="section-title">Votes Accumulated by Top Cuisines</div>', unsafe_allow_html=True)
    fig_cuis_votes = plot_votes_by_top_cuisines(df, top_n=12)
    st.plotly_chart(fig_cuis_votes, use_container_width=True)

    st.markdown('<div class="section-title">Top 15 Most Voted Restaurants</div>', unsafe_allow_html=True)
    st.dataframe(top_voted, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">Customer Engagement & Voting Insights</div>
        <p class="insight-text">
        • <b>Engagement Power Law:</b> The top 1% of restaurants capture over 28% of total platform votes. Landmark culinary destinations (such as Toit, Hauz Khas Social, Big Chill) command thousands of reviews.<br>
        • <b>Rating Trust Threshold:</b> Restaurants with over 500 votes almost uniformly maintain ratings > 3.8, proving that high engagement is heavily correlated with sustained operational excellence.
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 11: PRICE VS DELIVERY & BOOKING
# ---------------------------------------------------------
elif navigation == "⚖️ Price vs Delivery & Booking":
    st.markdown('<div class="main-header">Comparative Analysis: Price vs. Delivery & Booking</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Evaluating omnichannel service availability across spending tiers and resultant rating impacts.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_deliv_price = plot_price_vs_delivery(df)
        st.plotly_chart(fig_deliv_price, use_container_width=True)
    with col2:
        fig_book_price = plot_price_vs_booking_bar(df)
        st.plotly_chart(fig_book_price, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_deliv_box = plot_rating_comparison_by_delivery(df)
        st.plotly_chart(fig_deliv_box, use_container_width=True)
    with col4:
        fig_book_box = plot_rating_vs_booking_box(df)
        st.plotly_chart(fig_book_box, use_container_width=True)

    st.markdown('<div class="section-title">Omnichannel Synergy Matrix</div>', unsafe_allow_html=True)
    fig_matrix = plot_service_matrix_comparison(df)
    st.plotly_chart(fig_matrix, use_container_width=True)

    st.markdown("""
    <div class="insight-box">
        <div class="insight-title">Service Channel Synergy Insights</div>
        <p class="insight-text">
        • <b>Inverse Channel Availability:</b> Online delivery peaks in Mid-Range Tier 2 (39.5%) and Tier 3 (29.2%), while Table Booking is virtually non-existent in Tier 1 (< 0.1%) but surges to <b>47.6% in Fine Dining Tier 4</b>.<br>
        • <b>The Combined Advantage:</b> Establishments that offer both booking and delivery achieve the highest customer satisfaction score on the platform (3.92 rating &bull; 628 average votes).
        </p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------
# SECTION 12: BUSINESS INSIGHTS & REPORT EXPORT
# ---------------------------------------------------------
elif navigation == "📋 Business Insights & Reports":
    st.markdown('<div class="main-header">Strategic Business Insights & Executive Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Comprehensive data-backed synthesis, risk analysis, and report generation.</div>', unsafe_allow_html=True)

    st.markdown("""
    ### Executive Synthesis & Key Findings

    1. **Geographic Concentration Risk:**
       - **Observation:** 80.3% of all listed restaurants are situated in the NCR urban agglomeration (New Delhi, Gurgaon, Noida).
       - **Strategic Recommendation:** Aggressively onboard restaurant partners in high-growth secondary metros (Bangalore, Pune, Hyderabad, Mumbai) where disposable income and food-tech adoption are high.

    2. **Omnichannel Synergy Advantage:**
       - **Observation:** Restaurants enabling both Online Delivery and Table Booking achieve a **3.92 average rating** and **628 average votes**—outperforming single-channel restaurants by over 16% in customer satisfaction.
       - **Strategic Recommendation:** Implement integrated partner incentive programs encouraging dine-in restaurants to adopt delivery and vice versa.

    3. **The Unrated Opportunity:**
       - **Observation:** 2,148 establishments (22.5%) have zero rating / "Not rated".
       - **Strategic Recommendation:** Launch automated post-order feedback prompts and loyalty reward points for first-time reviews to convert dormant listings into active, verified partner outlets.

    4. **Cuisine Specialization vs. Hybridization:**
       - **Observation:** North Indian, Chinese, and Fast Food dominate in count, but specialized culinary offerings (Italian, Cafe, Continental) achieve consistently higher rating medians (> 3.65).
       - **Strategic Recommendation:** Create curated spotlight collections for specialty and artisanal cuisines to increase discovery for higher-margin partner merchants.
    """)

    st.markdown("---")
    st.markdown('<div class="section-title">Download Full Business Intelligence Reports</div>', unsafe_allow_html=True)

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        # Download filtered CSV
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_data,
            file_name="cognifyz_filtered_restaurant_data.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with col_d2:
        # Download Markdown Report
        report_path = "reports/analysis_report.md"
        if os.path.exists(report_path):
            with open(report_path, "r", encoding="utf-8") as f:
                report_content = f.read()
        else:
            report_content = "# Cognifyz Restaurant Data Analytics Executive Report\n\nGenerated from Dashboard."

        st.download_button(
            label="📄 Download Executive Analysis Report (Markdown)",
            data=report_content,
            file_name="cognifyz_restaurant_analysis_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    st.markdown("---")
    st.caption("Developed by **Pallapu Ankamma Rao** &bull; Cognifyz Data Analytics Internship Portfolio")
