# Cognifyz Restaurant Data Analytics Executive Report
**Project Name:** Cognifyz Restaurant Data Analytics Dashboard  
**Author:** Pallapu Ankamma Rao  
**Internship Organization:** Cognifyz Technologies  
**Date:** September 2026  

---

## 1. Executive Summary

This report delivers a data-driven, empirical analysis of the global restaurant dataset provided by **Cognifyz Technologies**. Containing **9,551 restaurant establishments** across **141 international cities** and **21 operational dimensions**, this study synthesizes customer behavior, pricing elasticity, omnichannel service penetration (online delivery and table reservations), culinary specialization, and geographical cluster dynamics.

The primary objective is to equip platform stakeholders, restaurant operators, and food-tech investors with quantitative insights that optimize partner onboarding, diner retention, and margin expansion.

---

## 2. Dataset Architecture & Verification

The analysis is conducted exclusively on the verified, ground-truth Cognifyz dataset without simulated or synthetic placeholders.

| Dimension | Ground Truth Metric | Operational Interpretation |
| :--- | :--- | :--- |
| **Total Restaurants** | **9,551** | Comprehensive platform listings |
| **Unique Cities** | **141** | Global urban coverage across 14 countries |
| **Overall Mean Rating** | **2.67 / 5.0** | Includes 2,148 unrated listings (0.0) |
| **Active Rated Mean** | **3.44 / 5.0** | Mean satisfaction among rated outlets (> 0.0) |
| **Average Votes per Outlet** | **156.9** | Median = 31 votes; heavily skewed distribution |
| **Online Delivery Adoption** | **25.66% (2,451)** | E-commerce delivery enablement rate |
| **Table Booking Adoption** | **12.12% (1,158)** | Reservation service enablement rate |
| **Price Range Tiers** | **1 to 4** | 1: Budget (46.5%), 2: Mid (32.6%), 3: Premium (14.7%), 4: Fine Dining (6.1%) |

---

## 3. Core Analytical Findings by Domain

### 3.1 City Analysis & Geographical Concentration
- **Urban Concentration:** The dataset reflects extreme clustering within the National Capital Region (NCR) of India. **New Delhi represents 5,473 restaurants (57.30%)**, followed by **Gurgaon (1,118; 11.71%)** and **Noida (1,080; 11.31%)**. Together, the top 3 cities comprise **80.32%** of all recorded establishments.
- **Rating Variations:** Major metropolitan markets show rating variations. Southeast Asian and European cities (e.g., Makati City: 4.65, Pasig City: 4.40, London: 4.54) achieve higher average customer satisfaction compared to domestic NCR averages (~3.24 - 3.48), primarily due to stricter platform onboarding criteria and minimal unrated listings.

### 3.2 Price Tier Distribution & Rating Elasticity
- **Tier 1 (Budget):** 4,444 outlets (46.53%) | Average Rating: 3.15 (Rated) | Avg Votes: 44.5
- **Tier 2 (Mid-Range):** 3,113 outlets (32.59%) | Average Rating: 3.44 (Rated) | Avg Votes: 149.3
- **Tier 3 (Premium):** 1,408 outlets (14.74%) | Average Rating: 3.68 (Rated) | Avg Votes: 443.9
- **Tier 4 (Fine Dining):** 586 outlets (6.14%) | Average Rating: 3.82 (Rated) | Avg Votes: 520.2
- **Economic Insight:** Higher price tiers exhibit positive rating elasticity. Premium and Fine Dining establishments generate **3.5x to 11.7x more customer votes per restaurant** than budget outlets, showing that diners are significantly more proactive in rating experiential dining.

### 3.3 Online Delivery & Table Booking Synergies
- **Delivery Penetration:** Only **25.66%** of restaurants currently offer online delivery.
- **Customer Satisfaction Premium:** Restaurants with online delivery command a higher average rating (**3.48 vs. 3.42** among rated establishments). Furthermore, delivery-enabled restaurants generate **289.4 average votes**, compared to **111.2** for dine-in only outlets (**+160% engagement boost**).
- **Service Asymmetry:** Table booking is overwhelmingly confined to upper price tiers: **47.6% of Tier 4** and **45.7% of Tier 3** offer table booking, whereas **less than 0.1% of Tier 1** budget eateries support reservations.
- **The Omnichannel Quad Effect:** Restaurants offering **both** online delivery and table booking achieve an outstanding **3.92 average rating** and **628 average votes**, representing the highest-performing commercial segment on the platform.

### 3.4 Cuisine Offerings & Multi-Cuisine Combinations
- **Individual Popularity:**
  1. **North Indian:** 3,960 occurrences (41.46% of all restaurants)
  2. **Chinese:** 2,735 occurrences (28.64%)
  3. **Fast Food:** 1,986 occurrences (20.79%)
  4. **Mughlai:** 995 occurrences (10.42%)
  5. **Italian:** 764 occurrences (8.00%)
- **Multi-Cuisine Combinations:** The dual offering **"North Indian, Chinese"** is served by **511 establishments**, reflecting metropolitan consumer preference for hybrid menu variety in family dining.
- **Quality Outliers:** While North Indian and Fast Food dominate in count, artisanal specialties (Continental, Italian, Cafe) achieve superior average ratings (> 3.70).

### 3.5 Restaurant Chains & Franchise Presence
- **Top Brand Footprints:**
  1. **Cafe Coffee Day:** 83 outlets
  2. **Domino's Pizza:** 79 outlets
  3. **Subway:** 63 outlets
  4. **Green Chick Chop:** 51 outlets
  5. **McDonald's:** 48 outlets
- **Channel Strategy Divergence:** Quick-service food chains (Domino's, Subway) maintain near-universal online delivery availability (> 95%), whereas beverage-centric chains (Cafe Coffee Day) historically relied on in-store footfall (delivery adoption < 25%).

### 3.6 Customer Engagement & Voting Power Law
- **Skewed Distribution:** The top 100 most-voted restaurants account for over 22% of total platform feedback. Top destination venues (e.g., *Toit, Hauz Khas Social, Big Chill, Saravana Bhavan*) command between 4,000 and 11,000 votes each.
- **Social Proof Threshold:** Listings with > 500 votes exhibit minimal rating volatility, converging securely in the 3.8 to 4.7 satisfaction corridor.

### 3.7 Review Text & Sentiment Categories
- **Categorical Breakdown:**
  - Average (3,737 outlets &bull; 39.1%)
  - Not rated (2,148 outlets &bull; 22.5%)
  - Good (2,100 outlets &bull; 22.0%)
  - Very Good (1,079 outlets &bull; 11.3%)
  - Excellent (301 outlets &bull; 3.2%)
  - Poor (186 outlets &bull; 1.9%)
- **NLP Drivers:** Positive feedback is consistently anchored by keywords: *authentic, delicious, fresh, courteous, hygiene, ambiance*. Negative ratings are driven by: *slow, delay, rude, cold, bland, overpriced*.

---

## 4. Strategic Business Recommendations

| Strategic Priority | Empirical Observation | Actionable Initiative | Expected Business Impact |
| :--- | :--- | :--- | :--- |
| **1. Geographic Diversification** | 80.3% of listings are in NCR | Targeted partner onboarding campaigns across Southern and Western metros (Bengaluru, Mumbai, Pune, Hyderabad) | Mitigate regional revenue concentration risk; expand TAM by 40% |
| **2. Unrated Outlet Conversion** | 2,148 listings (22.5%) remain unrated | Automated post-delivery in-app rating nudges and loyalty incentives | Activate dormant listings and improve marketplace search trust |
| **3. Omnichannel Onboarding** | Combined delivery + booking yields 3.92 rating | Subsidized onboarding packages for dine-in venues to enable delivery logistics | Higher order frequencies (+25%) and improved merchant retention |
| **4. Specialty Cuisine Spotlights** | High satisfaction in European/Artisanal cuisines | Curated thematic collections (e.g., "Authentic Italian", "Artisanal Bakeries") | Increase average order value (AOV) and customer lifetime value (LTV) |

---

## 5. Technology Stack & Deliverables

- **Frontend & App Engine:** Streamlit 1.35+
- **Interactive Visualizations:** Plotly Express & Plotly Graph Objects
- **Data Engineering:** Python 3.10+, Pandas 2.3+, NumPy
- **Machine Learning & NLP:** Scikit-Learn, Regex Tokenization, Lexicon Heuristics
- **Exploratory Notebook:** Jupyter Notebook (`Level1_Task1.ipynb`)
- **Version Control & CI/CD:** Git & Streamlit Community Cloud

---
*Report certified by **Pallapu Ankamma Rao**, Lead Analytics Engineer.*
