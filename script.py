
# Create a comprehensive analysis of Bitcoin monthly seasonality data
import pandas as pd
import numpy as np

# Bitcoin Monthly Returns Data (Average from 2009-2025 based on research)
btc_monthly_data = {
    'Month': ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December'],
    'Average_Return_%': [9.74, 12.52, 9.19, 33.79, 17.82, 7.76, 
                         7.36, -0.07, -4.67, 25.0, 35.51, 10.45],
    'Total_Return_2009_2023_%': [146, 187, 137, 506, 267, 116, 
                                  110, -0.99, -70, 375, 532, 156],
    'Performance': ['Positive', 'Positive', 'Positive', 'Strong Positive', 
                   'Positive', 'Positive', 'Positive', 'Weak/Neutral', 
                   'Negative', 'Strong Positive', 'Strong Positive', 'Positive']
}

df_btc = pd.DataFrame(btc_monthly_data)

# Add trading recommendations
df_btc['Trading_Strategy'] = df_btc['Average_Return_%'].apply(
    lambda x: 'Strong Buy Period' if x > 25 else ('Buy Period' if x > 10 else ('Hold/Caution' if x > 0 else 'Sell/Avoid'))
)

# Best and worst months
print("=" * 80)
print("BITCOIN MONTHLY SEASONALITY ANALYSIS (2009-2025)")
print("=" * 80)
print("\nComplete Monthly Performance:")
print(df_btc.to_string(index=False))

print("\n" + "=" * 80)
print("KEY INSIGHTS FOR TRADING BOT ALGORITHM")
print("=" * 80)

best_months = df_btc.nlargest(3, 'Average_Return_%')
worst_months = df_btc.nsmallest(3, 'Average_Return_%')

print("\n🔥 BEST MONTHS TO TRADE (Highest Returns):")
for idx, row in best_months.iterrows():
    print(f"   {row['Month']}: {row['Average_Return_%']}% average return")

print("\n⚠️  WORST MONTHS TO AVOID/SHORT (Lowest Returns):")
for idx, row in worst_months.iterrows():
    print(f"   {row['Month']}: {row['Average_Return_%']}% average return")

print("\n📊 SEASONAL PATTERNS:")
print("   Q1 (Jan-Mar): Average Return = {:.2f}%".format(df_btc.iloc[0:3]['Average_Return_%'].mean()))
print("   Q2 (Apr-Jun): Average Return = {:.2f}%".format(df_btc.iloc[3:6]['Average_Return_%'].mean()))
print("   Q3 (Jul-Sep): Average Return = {:.2f}%".format(df_btc.iloc[6:9]['Average_Return_%'].mean()))
print("   Q4 (Oct-Dec): Average Return = {:.2f}%".format(df_btc.iloc[9:12]['Average_Return_%'].mean()))

# Save to CSV for bot integration
df_btc.to_csv('bitcoin_monthly_seasonality.csv', index=False)
print("\n✅ Data saved to 'bitcoin_monthly_seasonality.csv'")
