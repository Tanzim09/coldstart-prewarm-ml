import pandas as pd

# Load the two CSVs
inv_df = pd.read_csv("invocation_log.csv")
cold_df = pd.read_csv("cold_start_data.csv")

# Convert timestamps to datetime
inv_df["Timestamp (UTC)"] = pd.to_datetime(inv_df["Timestamp (UTC)"])
cold_df["Timestamp (UTC)"] = pd.to_datetime(cold_df["Timestamp (UTC)"])

# Initialize Cold_Start = 0
inv_df["Cold_Start"] = 0

# Mark rows with cold starts
inv_df.loc[
    inv_df["Timestamp (UTC)"].isin(cold_df["Timestamp (UTC)"]),
    "Cold_Start"
] = 1

# Add Hour of day feature
inv_df["Hour"] = inv_df["Timestamp (UTC)"].dt.hour

# Rearrange columns
final_df = inv_df[["Timestamp (UTC)", "Hour", "Delay (s)", "Cold_Start"]]

# Save the final dataset
final_df.to_csv("ml_training_data.csv", index=False)
print(f"✅ ML training dataset saved to 'ml_training_data.csv' | Rows: {len(final_df)}")
