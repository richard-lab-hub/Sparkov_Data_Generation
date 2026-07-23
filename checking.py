import pandas as pd 

df = pd.read_csv("./Sparkov_Data_Generation/output_data/transactions.csv", sep='|')
fraud_percentage = df["is_fraud"].mean() * 100 
print(f"Fraud Percentage: {fraud_percentage:.4f}%")

