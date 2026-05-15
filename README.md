### Analysing 23,000 vehicle records to uncover pricing trends, brand performance and market shifts
# Automotive Market Intelligence

## Overview

This project evaluate a dataset of 23,000 car sales records
using Python and Pandas. The goal was to build a complete
analytical pipeline from raw data through 
executive report similar to the kind of
reporting workflows used in automotive and digital businesses.

The analysis covers five areas: data quality, brand performance,
pricing patterns, market trends and automated reporting.



## Key Findings

- Porsche is the most listed brand in the dataset with 1,268 records
  and commands a 43% price premium over the market average
- Electric vehicles represent 24.6% of all listings
  with consistent growth year on year since 2015
- Vehicles with no accident history command a meaningful
  price premium over those with reported incidents
- Newer vehicles from 2020 onwards are priced significantly
  higher than pre 2020 models across all fuel types
- The dataset passed all quality checks with zero missing values
  and zero duplicate records across 23,000 rows



## Analysis Chapters

**Chapter 1  Data Quality Report**
Validation of the dataset before any analysis begins.
Checking for missing values, duplicates, price outliers,
invalid year ranges and negative mileage values.
Produces a column-level quality summary with status flags.

**Chapter 2  Brand Performance**
Aggregation of listings and average prices by brand.
I Isolated Porsche specific metrics and compares against
direct luxury competitors including Ferrari, Lamborghini,
Aston Martin, Maserati, Mercedes-Benz, BMW and Audi.
Production of a highlighted bar chart for visual comparison.

**Chapter 3  Price Analysis**
Examination what drives price differences in the market.
Analyses the impact of fuel type, vehicle condition
and accident history on average selling price.
Calculates the correlation between mileage and price.

**Chapter 4  Market Trends**
Tracking how the market has evolved from 2010 to 2023.
Shows total listings per year and the shift in fuel type
mix over time, with a focus on electric vehicle growth.

**Chapter 5  Automated Executive Report**
Generation of a complete market summary automatically from raw data.
All metrics update dynamically when new data is loaded.
Output is printed to terminal and exported to CSV,
making it easy to schedule or integrate into a reporting pipeline.


## The Technical Skills Demonstrated

- Python Pandas, Matplotlib, Seaborn
- Data quality validation and outlier detection
- Aggregation and grouping (equivalent to SQL GROUP BY)
- Automated report generation
- Data visualisation with professional styling
- Clean, well commented code with business context


## The Tools Used

- Python 3.13
- Pandas 2.3
- Matplotlib
- Seaborn
- VS Code

## The Dataset

Source: Kaggle  Car Sales Dataset
Records: 23,000
Fields: Car Make, Car Model, Year, Mileage, Price,
        Fuel Type, Color, Transmission, Condition, Accident
