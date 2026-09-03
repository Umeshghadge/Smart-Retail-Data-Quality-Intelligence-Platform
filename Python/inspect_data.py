import pandas as pd

file_path = "data/raw/online_retail_II.xlsx"

df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

df = pd.concat([df_2009, df_2010], ignore_index=True)

print("Rows and Columns:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:") 
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nQuantity Range:")
print("Minimum Quantity:", df["Quantity"].min())
print("Maximum Quantity:", df["Quantity"].max())

print("\nNegative Quantity Records:")
print((df["Quantity"] < 0).sum())

print("\nCancelled Invoice Records:")
print(df["Invoice"].astype(str).str.startswith("C").sum())


print("\nPrice Range:")
print("Minimum Price:", df["Price"].min())
print("Maximum Price:", df["Price"].max())

print("\nNegative Price Records:")
print((df["Price"] < 0).sum())

print("\nNegative Price Details:")
print(df[df["Price"] < 0])

print("\nZero Price Records:")
print((df["Price"] == 0).sum())

print("\nZero Price Records:")
print((df["Price"] == 0).sum())

print("\nZero Price Details:")
print(df[df["Price"] == 0].head(10))

print("\nData Types:")
print(df.dtypes)

print("\nDate Range:")
print("Earliest Date:", df["InvoiceDate"].min())
print("Latest Date:", df["InvoiceDate"].max())

print("\nFuture Date Records:")
print((df["InvoiceDate"] > pd.Timestamp.now()).sum())

print("\nUnique Values:")
print("Unique Invoices:", df["Invoice"].nunique())
print("Unique Products:", df["StockCode"].nunique())
print("Unique Customers:", df["Customer ID"].nunique())
print("Unique Countries:", df["Country"].nunique())