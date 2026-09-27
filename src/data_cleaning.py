"""
Data Cleaning and Preprocessing Module for Cognifyz Restaurant Dataset.
Handles missing values, data type standardization, and derived feature engineering.
"""

import os
import pandas as pd
import numpy as np


def load_and_clean_data(filepath="data/Dataset.csv") -> pd.DataFrame:
    """
    Loads and cleans the Cognifyz restaurant dataset.
    
    Args:
        filepath (str): Path to Dataset.csv
        
    Returns:
        pd.DataFrame: Cleaned and feature-engineered DataFrame.
    """
    if not os.path.exists(filepath):
        # Fallback search if current working directory varies
        alt_paths = [
            os.path.join(os.path.dirname(__file__), "..", filepath),
            os.path.join(os.path.dirname(__file__), "..", "data", "Dataset.csv"),
            filepath,
        ]
        for p in alt_paths:
            if os.path.exists(p):
                filepath = p
                break
        else:
            raise FileNotFoundError(f"Dataset not found at {filepath}")

    # Load with UTF-8 encoding, fallback to latin-1 if needed
    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(filepath, encoding="latin-1")

    # Clean whitespace in column headers
    df.columns = df.columns.str.strip()

    # Handle missing values in Cuisines (9 missing rows in official dataset)
    df["Cuisines"] = df["Cuisines"].fillna("Unknown / Not Specified").str.strip()

    # Ensure correct data types
    df["Restaurant ID"] = df["Restaurant ID"].astype(str)
    df["Restaurant Name"] = df["Restaurant Name"].astype(str).str.strip()
    df["City"] = df["City"].astype(str).str.strip()
    df["Address"] = df["Address"].astype(str).str.strip()
    df["Locality"] = df["Locality"].astype(str).str.strip()
    df["Locality Verbose"] = df["Locality Verbose"].astype(str).str.strip()
    df["Price range"] = pd.to_numeric(df["Price range"], errors="coerce").fillna(1).astype(int)
    df["Aggregate rating"] = pd.to_numeric(df["Aggregate rating"], errors="coerce").fillna(0.0)
    df["Votes"] = pd.to_numeric(df["Votes"], errors="coerce").fillna(0).astype(int)
    df["Average Cost for two"] = pd.to_numeric(df["Average Cost for two"], errors="coerce").fillna(0.0)
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce").fillna(0.0)
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce").fillna(0.0)

    # Boolean and standardized categorical columns
    df["Has Table booking"] = df["Has Table booking"].astype(str).str.strip().str.capitalize()
    df["Has Online delivery"] = df["Has Online delivery"].astype(str).str.strip().str.capitalize()
    df["Is delivering now"] = df["Is delivering now"].astype(str).str.strip().str.capitalize()

    # Derived Feature Engineering
    df["Has_Online_Delivery_Num"] = (df["Has Online delivery"] == "Yes").astype(int)
    df["Has_Table_Booking_Num"] = (df["Has Table booking"] == "Yes").astype(int)
    df["Is_Delivering_Now_Num"] = (df["Is delivering now"] == "Yes").astype(int)
    df["Has_Rating"] = df["Aggregate rating"] > 0

    # Price Range Text Labels
    price_labels = {
        1: "1 - Budget",
        2: "2 - Mid-Range",
        3: "3 - Premium",
        4: "4 - Fine Dining",
    }
    df["Price_Range_Label"] = df["Price range"].map(price_labels).fillna("Unknown")

    # Clean Rating Text
    df["Rating text"] = df["Rating text"].astype(str).str.strip()

    # Valid geographic coordinate flag
    # Filter out 0.0 lat/long which are missing in 497 rows
    df["Valid_Coords"] = (
        (df["Latitude"] != 0.0)
        & (df["Longitude"] != 0.0)
        & (df["Latitude"].between(-90, 90))
        & (df["Longitude"].between(-180, 180))
    )

    # Number of cuisines offered
    df["Cuisine_Count"] = df["Cuisines"].apply(
        lambda x: len([c.strip() for c in x.split(",") if c.strip()]) if x != "Unknown / Not Specified" else 0
    )

    return df


def get_dataset_summary(df: pd.DataFrame) -> dict:
    """
    Computes key summary statistics for the dataset.
    """
    total_restaurants = len(df)
    unique_cities = df["City"].nunique()
    avg_rating_all = round(df["Aggregate rating"].mean(), 2)
    rated_df = df[df["Aggregate rating"] > 0]
    avg_rating_rated = round(rated_df["Aggregate rating"].mean(), 2) if len(rated_df) > 0 else 0.0
    avg_votes = round(df["Votes"].mean(), 1)
    avg_cost = round(df["Average Cost for two"].mean(), 2)
    online_delivery_pct = round((df["Has Online delivery"] == "Yes").mean() * 100, 2)
    table_booking_pct = round((df["Has Table booking"] == "Yes").mean() * 100, 2)
    unrated_count = int((df["Aggregate rating"] == 0).sum())

    return {
        "total_restaurants": total_restaurants,
        "unique_cities": unique_cities,
        "avg_rating_all": avg_rating_all,
        "avg_rating_rated": avg_rating_rated,
        "avg_votes": avg_votes,
        "avg_cost": avg_cost,
        "online_delivery_pct": online_delivery_pct,
        "table_booking_pct": table_booking_pct,
        "unrated_count": unrated_count,
    }
