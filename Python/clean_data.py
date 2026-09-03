import pandas as pd


# Load both sheets
file_path = "data/raw/online_retail_II.xlsx"

df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

df = pd.concat([df_2009, df_2010], ignore_index=True)


# Check duplicates
duplicates = df[df.duplicated(keep=False)]

print("Total Duplicate Records:", len(duplicates))
print("\nSample Duplicate Records:")
print(duplicates.head(10))

print("\nDuplicate Count:")
print(df.duplicated().sum())

duplicate_counts = df.value_counts().reset_index(name="Count")

print("\nDuplicate Records with Occurrence Count:")
print(duplicate_counts[duplicate_counts["Count"] > 1].head(10))


# Remove exact duplicates
df_clean = df.drop_duplicates().copy()

print("\nOriginal Records:", len(df))
print("Records After Removing Duplicates:", len(df_clean))
print("Duplicates Removed:", len(df) - len(df_clean))


# Check missing values
print("\nMissing Values After Removing Duplicates:")
print(df_clean.isnull().sum())


# Handle missing descriptions
print("\nMissing Description Sample:")
print(df_clean[df_clean["Description"].isnull()].head(10))

missing_desc_codes = df_clean.loc[
    df_clean["Description"].isnull(), "StockCode"
].unique()

description_mapping = (
    df_clean.dropna(subset=["Description"])
    .groupby("StockCode")["Description"]
    .first()
)

found = sum(code in description_mapping.index for code in missing_desc_codes)

print("\nDescription Mapping Check:")
print("Missing Description StockCodes:", len(missing_desc_codes))
print("StockCodes with Available Description:", found)

df_clean["Description"] = df_clean["Description"].fillna(
    df_clean["StockCode"].map(description_mapping)
)

print("\nMissing Description After Mapping:")
print(df_clean["Description"].isnull().sum())

print("\nRemaining Missing Description Records:")
print(
    df_clean[df_clean["Description"].isnull()][
        ["Invoice", "StockCode", "Quantity", "Price", "Customer ID", "Country"]
    ].head(20)
)

# If no description is available for that StockCode
df_clean["Description"] = df_clean["Description"].fillna("Unknown")

print("\nMissing Description After Final Handling:")
print(df_clean["Description"].isnull().sum())


# Customer ID validation
missing_customer = df_clean[df_clean["Customer ID"].isnull()]

print("\nCustomer ID Missing Analysis:")
print("Missing Customer ID Records:", len(missing_customer))
print("Negative Quantity:", (missing_customer["Quantity"] < 0).sum())
print("Zero Price:", (missing_customer["Price"] == 0).sum())
print("Positive Quantity:", (missing_customer["Quantity"] > 0).sum())
print("Positive Price:", (missing_customer["Price"] > 0).sum())


# Keep missing Customer IDs as a flag
customer_id_missing = df_clean["Customer ID"].isnull()

print("\nCustomer ID Missing Handling:")
print("Missing Customer ID:", customer_id_missing.sum())
print("Records with Customer ID:", df_clean["Customer ID"].notnull().sum())

df_clean["Customer_ID_Missing"] = customer_id_missing

print("\nCustomer ID Missing Flag:")
print(df_clean["Customer_ID_Missing"].value_counts())


# Quantity validation
print("\nQuantity Validation:")
print("Negative Quantity:", (df_clean["Quantity"] < 0).sum())
print("Zero Quantity:", (df_clean["Quantity"] == 0).sum())
print("Positive Quantity:", (df_clean["Quantity"] > 0).sum())

print("\nNegative Quantity Sample:")
print(
    df_clean[df_clean["Quantity"] < 0][
        ["Invoice", "StockCode", "Description", "Quantity", "Price"]
    ].head(10)
)


# Price validation
print("\nPrice Validation:")
print("Negative Price:", (df_clean["Price"] < 0).sum())
print("Zero Price:", (df_clean["Price"] == 0).sum())
print("Positive Price:", (df_clean["Price"] > 0).sum())

print("\nZero Price Sample:")
print(
    df_clean[df_clean["Price"] == 0][
        ["Invoice", "StockCode", "Description", "Quantity", "Price"]
    ].head(10)
)

print("\nNegative Price Sample:")
print(
    df_clean[df_clean["Price"] < 0][
        ["Invoice", "StockCode", "Description", "Quantity",
         "Price", "Customer ID", "Country"]
    ]
)


# Business rules
print("\nBusiness Rule Validation:")

df_clean["Is_Cancellation"] = (
    df_clean["Invoice"].astype(str).str.startswith("C")
)

df_clean["Is_Adjustment"] = (
    df_clean["Invoice"].astype(str).str.startswith("A")
)

df_clean["Is_Return"] = df_clean["Quantity"] < 0
df_clean["Is_Zero_Price"] = df_clean["Price"] == 0
df_clean["Is_Negative_Price"] = df_clean["Price"] < 0

print("Cancellation Records:", df_clean["Is_Cancellation"].sum())
print("Adjustment Records:", df_clean["Is_Adjustment"].sum())
print("Return / Negative Quantity Records:", df_clean["Is_Return"].sum())
print("Zero Price Records:", df_clean["Is_Zero_Price"].sum())
print("Negative Price Records:", df_clean["Is_Negative_Price"].sum())


# Calculate revenue
print("\nRevenue Calculation:")

df_clean["Revenue"] = df_clean["Quantity"] * df_clean["Price"]

print(
    df_clean[
        ["Invoice", "StockCode", "Quantity", "Price", "Revenue"]
    ].head(10)
)


# Revenue validation
print("\nRevenue Validation:")
print("Negative Revenue:", (df_clean["Revenue"] < 0).sum())
print("Zero Revenue:", (df_clean["Revenue"] == 0).sum())
print("Positive Revenue:", (df_clean["Revenue"] > 0).sum())


# Final quality summary
print("\nData Quality Summary:")
print("Original Records:", len(df))
print("Final Records:", len(df_clean))
print("Duplicates Removed:", len(df) - len(df_clean))
print("Missing Description:", df_clean["Description"].isnull().sum())
print("Missing Customer ID:", df_clean["Customer ID"].isnull().sum())
print("Negative Quantity:", (df_clean["Quantity"] < 0).sum())
print("Zero Quantity:", (df_clean["Quantity"] == 0).sum())
print("Negative Price:", (df_clean["Price"] < 0).sum())
print("Zero Price:", (df_clean["Price"] == 0).sum())
print("Cancellation Records:", df_clean["Is_Cancellation"].sum())
print("Adjustment Records:", df_clean["Is_Adjustment"].sum())
print("Return Records:", df_clean["Is_Return"].sum())
print("Negative Revenue:", (df_clean["Revenue"] < 0).sum())
print("Zero Revenue:", (df_clean["Revenue"] == 0).sum())
print("Positive Revenue:", (df_clean["Revenue"] > 0).sum())




print("\nDate Transformation:")

# Convert InvoiceDate into datetime format
df_clean["InvoiceDate"] = pd.to_datetime(df_clean["InvoiceDate"])

# Create useful date columns
df_clean["Invoice_Date"] = df_clean["InvoiceDate"].dt.date
df_clean["Year"] = df_clean["InvoiceDate"].dt.year
df_clean["Month"] = df_clean["InvoiceDate"].dt.month
df_clean["Month_Name"] = df_clean["InvoiceDate"].dt.month_name()

print(
    df_clean[
        ["InvoiceDate", "Invoice_Date", "Year", "Month", "Month_Name"]
    ].head(10)
)




print("\nTransaction Type:")

df_clean["Transaction_Type"] = "Sale"

df_clean.loc[df_clean["Is_Return"], "Transaction_Type"] = "Return"

df_clean.loc[
    df_clean["Is_Cancellation"],
    "Transaction_Type"
] = "Cancellation"

df_clean.loc[
    df_clean["Is_Adjustment"],
    "Transaction_Type"
] = "Adjustment"

print(
    df_clean["Transaction_Type"].value_counts()
)

print("\nCustomer Type:")

df_clean["Customer_Type"] = "Registered"

df_clean.loc[
    df_clean["Customer ID"].isnull(),
    "Customer_Type"
] = "Guest"

print(df_clean["Customer_Type"].value_counts())


print("\nRevenue Category:")

df_clean["Revenue_Category"] = "Positive"

df_clean.loc[
    df_clean["Revenue"] == 0,
    "Revenue_Category"
] = "Zero"

df_clean.loc[
    df_clean["Revenue"] < 0,
    "Revenue_Category"
] = "Negative"

print(df_clean["Revenue_Category"].value_counts())



print("\nQuantity Category:")

df_clean["Quantity_Category"] = "Positive"

df_clean.loc[
    df_clean["Quantity"] < 0,
    "Quantity_Category"
] = "Negative"

print(df_clean["Quantity_Category"].value_counts())



print("\nStock Code Type:")

df_clean["StockCode_Type"] = "Numeric"

df_clean.loc[
    df_clean["StockCode"].astype(str).str.contains(
        r"[A-Za-z]",
        regex=True
    ),
    "StockCode_Type"
] = "Alphanumeric"

print(df_clean["StockCode_Type"].value_counts())

print("\nSaving Cleaned Dataset:")

output_path = "data/processed/retail_cleaned.csv"

df_clean.to_csv(output_path, index=False)

print("Cleaned dataset saved successfully.")
print("File:", output_path)
print("Final Records:", len(df_clean))
print("Final Columns:", len(df_clean.columns))