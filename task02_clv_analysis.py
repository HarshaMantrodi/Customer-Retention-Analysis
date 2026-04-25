import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. SETUP
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, 'sales_data.xlsx')

def run_clv_analysis():
    try:
        # Step 1: Ingest Excel
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip().str.lower()
        print("✅ Step 1: Customer Data Ingested Successfully.")

        # Step 2: Calculate Monetary Value (LValue)
        # Formula: Average Order Value * Order Frequency
        if 'avgorder' in df.columns and 'ordfreq' in df.columns:
            df['calculated_monetary'] = df['avgorder'] * df['ordfreq']
            print("✅ Step 2: Lifetime Value calculated from avgorder and ordfreq.")
        else:
            print(f"❌ Error: Required columns missing. Found: {df.columns.tolist()}")
            return

        # Step 3: Segment by City or Retention Status
        group_col = 'city' if 'city' in df.columns else df.columns[0]
        
        # Aggregating by City to see where high-value customers live
        clv_report = df.groupby(group_col)['calculated_monetary'].agg(['sum', 'mean', 'count']).reset_index()
        clv_report.columns = [group_col, 'Total_Revenue', 'Avg_CLV', 'Customer_Count']

        # Step 4: VIP Score (Normalization)
        clv_report['VIP_Score'] = (clv_report['Total_Revenue'] / clv_report['Total_Revenue'].max()) * 100

        # Step 5: Visualization
        plt.figure(figsize=(12, 6))
        # Top 10 Cities by Total Revenue
        top_cities = clv_report.sort_values('Total_Revenue', ascending=False).head(10)
        
        sns.barplot(x='Total_Revenue', y=group_col, data=top_cities, palette='viridis')
        plt.title('Capstone Level 6: Market Value by City (CLV)', fontsize=14)
        plt.xlabel('Cumulative Value (Avg Order × Frequency)')
        plt.tight_layout()
        plt.show()

        # Step 6: Summary Print
        print("\n--- TOP MARKET SEGMENTS (CITY) ---")
        print(clv_report.sort_values('VIP_Score', ascending=False).head(5))

    except Exception as e:
        print(f"❌ CLV Pipeline Error: {e}")

if __name__ == "__main__":
    run_clv_analysis()