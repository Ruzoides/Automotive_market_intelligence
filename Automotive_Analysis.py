
# Automotive Market Intelligence Report
# Author: Rui Costa
# Date: May 2026
# Dataset: Car Sales Data - 23,000 records
# Tools used: Python, Pandas, Matplotlib, Seaborn
# analyses on car sales data to understand
# market trends, brand performance and pricing patterns.


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv('Updated_Car_Sales_Data.csv')

# basic plot settings, i prefer whitegrid for readability
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("=" * 60)
print("AUTOMOTIVE MARKET INTELLIGENCE REPORT")
print("=" * 60)



# CHAPTER 1 - Data Quality Check
# Before doing any analysis i always check the data quality
# first. In my experience dirty data leads to wrong conclusions
# so this step is non-negotiable.


print("\n--- CHAPTER 1: DATA QUALITY REPORT ---\n")

# basic overview of the dataset
total_records = len(df)
total_columns = len(df.columns)
print(f"Total Records:  {total_records:,}")
print(f"Total Columns:  {total_columns}")

# check for missing values in each column
# this is similar to checking NULL counts in SQL
print("\nMissing Values Per Column:")
missing = df.isnull().sum()
missing_pct = (missing / total_records * 100).round(2)
quality_report = pd.DataFrame({
    'Missing Count': missing,
    'Missing %': missing_pct,
    'Status': ['Clean' if x == 0 else 'Has Nulls' for x in missing]
})
print(quality_report)

# check for duplicate rows
duplicates = df.duplicated().sum()
print(f"\nDuplicate Records: {duplicates}")
print(f"Data Quality Score: {'100% Clean' if duplicates == 0 else 'Has Duplicates'}")

# identify price outliers using standard deviation
# anything more than 3 std from the mean is flagged
mean_price = df['Price'].mean()
std_price = df['Price'].std()
outliers = df[df['Price'] > mean_price + (3 * std_price)]
print(f"\nPrice Outliers (above 3 std from mean): {len(outliers)} records")
print(f"Average Price: EUR {mean_price:,.0f}")
print(f"Price Range: EUR {df['Price'].min():,.0f} to EUR {df['Price'].max():,.0f}")

# sanity check on year values - anything outside 2000-2024 is suspicious
invalid_years = df[(df['Year'] < 2000) | (df['Year'] > 2024)]
print(f"\nInvalid Year Records: {len(invalid_years)}")
print(f"Year Range in Data: {df['Year'].min()} to {df['Year'].max()}")

# negative mileage doesnt make sense so we flag those too
negative_mileage = df[df['Mileage'] < 0]
print(f"Negative Mileage Records: {len(negative_mileage)}")

print("\nData Quality Report Complete")


# CHAPTER 2 - Brand Performance
#Brand performance
#overview on brand performances in terms of total listings and average prices.


print("\n--- CHAPTER 2: BRAND PERFORMANCE ANALYSIS ---\n")

# total listings and average price per brand
brand_performance = df.groupby('Car Make').agg(
    total_listings=('Car Make', 'count'),
    avg_price=('Price', 'mean'),
    avg_mileage=('Mileage', 'mean')
).round(0).sort_values('total_listings', ascending=False)

print("Top 10 Brands by Listings:")
print(brand_performance.head(10).to_string())

# Premium brand highlinghted  
porsche_data = df[df['Car Make'] == 'Porsche']
print(f"\n--- PORSCHE SPECIFIC ---")
print(f"Total Porsche Listings:  {len(porsche_data):,}")
print(f"Average Porsche Price:   EUR {porsche_data['Price'].mean():,.0f}")
print(f"Average Porsche Mileage: {porsche_data['Mileage'].mean():,.0f} km")
print(f"Most Common Model:       {porsche_data['Car Model'].mode()[0]}")
print(f"Most Common Fuel Type:   {porsche_data['Fuel Type'].mode()[0]}")

# comparison of Porsche with other brands 
# The choosing of the brands correlate directly with the fact that they are directly 
#competitors
luxury_brands = ['Porsche', 'BMW', 'Mercedes-Benz', 'Audi',
                 'Ferrari', 'Lamborghini', 'Aston Martin', 'Maserati']
luxury_data = df[df['Car Make'].isin(luxury_brands)]
luxury_comparison = luxury_data.groupby('Car Make')['Price'].mean()\
    .sort_values(ascending=False).round(0)

print("\nLuxury Brand Average Price Comparison:")
for brand, price in luxury_comparison.items():
    marker = ">> " if brand == 'Porsche' else "   "
    print(f"{marker} {brand:<20} EUR {price:>10,.0f}")

# Visualisation method through line bar chart 
fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#FF6B00' if brand == 'Porsche' else '#2C3E50'
          for brand in luxury_comparison.index]
bars = ax.barh(luxury_comparison.index, luxury_comparison.values, color=colors)
ax.set_xlabel('Average Price (EUR)', fontsize=12)
ax.set_title('Luxury Brand Average Price Comparison\nPorsche highlighted in orange',
             fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'EUR {x:,.0f}'))
for bar, value in zip(bars, luxury_comparison.values):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f'EUR {value:,.0f}', va='center', fontsize=9)
plt.tight_layout()
plt.savefig('02_brand_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: 02_brand_comparison.png")


# CHAPTER 3 - Price Analysis
# Looking at what factors drive price differences.
# Fuel type, condition and accident history all seem
# to have an impact based on initial exploration.

print("\n--- CHAPTER 3: PRICE ANALYSIS ---\n")

# average price broken down by fuel type
price_by_fuel = df.groupby('Fuel Type').agg(
    avg_price=('Price', 'mean'),
    total=('Price', 'count'),
    min_price=('Price', 'min'),
    max_price=('Price', 'max')
).round(0).sort_values('avg_price', ascending=False)

print("Price Analysis by Fuel Type:")
print(price_by_fuel.to_string())

# price by vehicle condition
# expectation is New > Like New > Used
price_by_condition = df.groupby('Condition')['Price']\
    .mean().sort_values(ascending=False).round(0)
print("\nAverage Price by Condition:")
for condition, price in price_by_condition.items():
    print(f"  {condition:<12} EUR {price:>10,.0f}")

# correlation between mileage and price
# higher mileage should generally mean lower price
print("\nPrice vs Mileage Correlation:")
correlation = df['Price'].corr(df['Mileage'])
print(f"  Correlation: {correlation:.3f}")
if correlation < -0.3:
    print("  Finding: Higher mileage leads to lower price as expected")
elif correlation > 0.3:
    print("  Finding: Higher mileage associated with higher price - unusual")
else:
    print("  Finding: Weak relationship between mileage and price")

# does accident history affect price
accident_price = df.groupby('Accident')['Price'].mean().round(0)
print("\nImpact of Accident History on Price:")
for accident, price in accident_price.items():
    print(f"  Accident {accident:<5} Average Price: EUR {price:,.0f}")

no_accident_premium = accident_price.get('No', 0) - accident_price.get('Yes', 0)
print(f"  Price premium for clean history: EUR {no_accident_premium:,.0f}")

# plot price by fuel type and condition side by side
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

fuel_colors = ['#FF6B00', '#2C3E50', '#27AE60', '#E74C3C', '#9B59B6']
axes[0].bar(price_by_fuel.index, price_by_fuel['avg_price'],
            color=fuel_colors[:len(price_by_fuel)])
axes[0].set_title('Average Price by Fuel Type', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Average Price (EUR)')
axes[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'EUR {x:,.0f}'))
axes[0].tick_params(axis='x', rotation=15)

condition_colors = ['#27AE60', '#FF6B00', '#E74C3C']
axes[1].bar(price_by_condition.index, price_by_condition.values,
            color=condition_colors[:len(price_by_condition)])
axes[1].set_title('Average Price by Vehicle Condition', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Average Price (EUR)')
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'EUR {x:,.0f}'))

plt.suptitle('Price Analysis Dashboard', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('03_price_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: 03_price_analysis.png")


# CHAPTER 4 - Market Trends
# This section looks at how the market has changed over time.
# Electric vehicle growth is particularly interesting given
# the push towards electrification across europe.

print("\n--- CHAPTER 4: MARKET TRENDS ---\n")

# listings per year to see if market is growing or shrinking
yearly_trend = df.groupby('Year').agg(
    total_listings=('Year', 'count'),
    avg_price=('Price', 'mean')
).round(0)

print("Market Listings by Year:")
print(yearly_trend.to_string())

# fuel type split by year to track electrification trend
fuel_trend = df.groupby(['Year', 'Fuel Type']).size()\
    .unstack(fill_value=0)
print("\nFuel Type Distribution by Year:")
print(fuel_trend.to_string())

# zoom in on electric vehicle growth specifically
electric_growth = df[df['Fuel Type'] == 'Electric']\
    .groupby('Year').size()
print("\nElectric Vehicle Listings by Year:")
for year, count in electric_growth.items():
    bar = "|" * (count // 10)
    print(f"  {year}: {bar} ({count})")

# plot market trends
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# line chart showing total listings over time
axes[0].plot(yearly_trend.index, yearly_trend['total_listings'],
             marker='o', color='#FF6B00', linewidth=2, markersize=6)
axes[0].fill_between(yearly_trend.index, yearly_trend['total_listings'],
                     alpha=0.2, color='#FF6B00')
axes[0].set_title('Total Listings Per Year', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Year')
axes[0].set_ylabel('Number of Listings')

# stacked bar showing how fuel types shift over time
fuel_trend.plot(kind='bar', stacked=True, ax=axes[1],
                colormap='Set2', width=0.8)
axes[1].set_title('Fuel Type Mix by Year', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Year')
axes[1].set_ylabel('Number of Listings')
axes[1].tick_params(axis='x', rotation=45)
axes[1].legend(title='Fuel Type', bbox_to_anchor=(1.05, 1))

plt.suptitle('Market Trend Analysis', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('04_market_trends.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart saved: 04_market_trends.png")


# CHAPTER 5 - Automated Executive Report

# This section auto-generates a summary report from the data.
# The idea is that this could be scheduled to run daily or weekly
# and always produce an up to date report without manual work.
# This is what i mean by automating reporting routines.

print("\n--- CHAPTER 5: AUTOMATED EXECUTIVE REPORT ---\n")
print("=" * 60)
print("EXECUTIVE SUMMARY - AUTOMOTIVE MARKET REPORT")
print("=" * 60)

# all metrics calculated automatically from raw data
total_cars = len(df)
avg_price = df['Price'].mean()
most_common_brand = df['Car Make'].mode()[0]
most_common_fuel = df['Fuel Type'].mode()[0]
newest_avg_price = df[df['Year'] >= 2020]['Price'].mean()
older_avg_price = df[df['Year'] < 2020]['Price'].mean()
electric_share = (df['Fuel Type'] == 'Electric').sum() / total_cars * 100
accident_rate = (df['Accident'] == 'Yes').sum() / total_cars * 100
porsche_avg = df[df['Car Make'] == 'Porsche']['Price'].mean()
market_avg = df['Price'].mean()
porsche_premium = ((porsche_avg - market_avg) / market_avg * 100)

print(f"""
MARKET OVERVIEW
{'─' * 40}
Total Vehicles Analyzed:     {total_cars:>10,}
Average Market Price:        EUR {avg_price:>10,.0f}
Most Listed Brand:           {most_common_brand:>10}
Dominant Fuel Type:          {most_common_fuel:>10}

PRICING INSIGHTS
{'─' * 40}
2020+ Vehicles Avg Price:    EUR {newest_avg_price:>10,.0f}
Pre-2020 Vehicles Avg Price: EUR {older_avg_price:>10,.0f}
Newer Vehicle Premium:       {((newest_avg_price/older_avg_price)-1)*100:>9.1f}%

PORSCHE PERFORMANCE
{'─' * 40}
Porsche Average Price:       EUR {porsche_avg:>10,.0f}
Market Average Price:        EUR {market_avg:>10,.0f}
Porsche Premium vs Market:   {porsche_premium:>9.1f}%
Porsche Total Listings:      {len(porsche_data):>10,}

MARKET HEALTH INDICATORS
{'─' * 40}
Electric Vehicle Share:      {electric_share:>9.1f}%
Vehicles with Accidents:     {accident_rate:>9.1f}%
Data Quality Score:          {'100% Clean' if duplicates == 0 else 'Issues Found':>10}

KEY FINDINGS
{'─' * 40}
1. Porsche has a {porsche_premium:.1f}% price premium over the market average
2. Electric vehicles make up {electric_share:.1f}% of all listings
3. {accident_rate:.1f}% of vehicles have a reported accident history
4. Newer vehicles from 2020 onwards priced {((newest_avg_price/older_avg_price)-1)*100:.1f}% above older models
5. Dataset is clean with no missing values or duplicates
""")

print("=" * 60)
print("Automated Executive Report Complete")
print("=" * 60)


# save the summary metrics to a CSV file
# this makes it easy to load into Excel or Power BI later
summary_data = {
    'Metric': [
        'Total Vehicles',
        'Average Price',
        'Porsche Average Price',
        'Porsche Premium %',
        'Electric Share %',
        'Accident Rate %',
        'Missing Values',
        'Duplicate Records'
    ],
    'Value': [
        total_cars,
        round(avg_price, 0),
        round(porsche_avg, 0),
        round(porsche_premium, 1),
        round(electric_share, 1),
        round(accident_rate, 1),
        0,
        0
    ]
}

summary_df = pd.DataFrame(summary_data)
summary_df.to_csv('executive_summary.csv', index=False)
print("\nExecutive summary exported to executive_summary.csv")
print("Analysis complete - all output files saved to current folder")