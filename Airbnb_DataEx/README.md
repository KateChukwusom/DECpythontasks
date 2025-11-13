## Airbnb Listings Analysis (Japan)

# Overview

This project analyzes Airbnb listings data for Japan to understand pricing, availability, room types, hosts, and neighborhoods. The goal is to uncover key insights that can help hosts, travelers, or market analysts make informed decisions.

# Dataset

The dataset includes columns like: price, minimum_nights, availability_365, room_type, host_name, neighbourhood_cleansed, and number_of_reviews.

Data cleaning and enrichment were performed to make it ready for analysis.

# Data Cleaning Steps

- Converted price columns from string (like $2,100.00) to numeric floats.

- Handled missing values in critical columns:

- reviews_per_month - filled with 0

- host_name - filled with "Unknown Host"

- neighbourhood_group_cleansed - filled with "Unknown"

- Removed irrelevant listings:

- price == 0

- availability_365 == 0

- Checked for duplicates and unusual data types.

# Data Enrichment

- Created price_per_booking:

- Formula: price_per_booking = price * minimum_nights

- Provides a realistic total cost for a booking.

- Categorized availability into:

- Full-time - availability_365 > 300

- Part-time - 100 ≤ availability_365 ≤ 300

- Rare - availability_365 < 100

# Analysis Conducted

- Top 10 Most Expensive Neighborhoods: Identified neighborhoods with the highest average prices.

- Average Availability and Price by Room Type: Compared Entire home, Private room, and Shared room.

- Host with the Most Listings: Determined which hosts manage multiple listings.

- Price Variation Across Neighborhoods: Explored location-based pricing trends.

- Listings Never Reviewed: Counted listings with number_of_reviews == 0, including  active listings.

# Key Insights

- Some neighborhoods consistently show higher prices, pointing to more premium or in-demand areas.

- Entire homes tend to cost more and are often available for longer periods compared to private or shared rooms.

- A few hosts manage several listings, which likely reflects professional or business-level hosting.

- Many listings have no reviews, suggesting they’re either new or not frequently booked.

- Prices differ noticeably across locations, showing how geography influences value and demand.

# Conclusion

This analysis gives a solid overview of Airbnb listings in Japan, revealing how pricing, availability, and host activity vary across neighborhoods. 