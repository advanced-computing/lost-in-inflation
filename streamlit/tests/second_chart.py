import pandas as pd
import os

# Relative to root directory
china_path = os.path.join("EIUCOCHNTOT.csv")
pce_path = os.path.join("MoM PCE.csv")

# Load and preview China MXP data
try:
    df_china = pd.read_csv(china_path)
    print("✅ China MXP Data Loaded:")
    print(df_china.head())
    print(df_china.dtypes)
except Exception as e:
    print("❌ Error loading China MXP data:", e)

print("-" * 50)

# Load and preview MoM PCE data
try:
    df_pce = pd.read_csv(pce_path)
    print("✅ MoM PCE Data Loaded:")
    print(df_pce.head())
    print(df_pce.dtypes)
except Exception as e:
    print("❌ Error loading MoM PCE data:", e)
