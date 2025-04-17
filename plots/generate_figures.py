import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Check working directory and path
print("Current Working Directory:", os.getcwd())

# Load result CSV (adjust path depending on where you run this from)
try:
    df = pd.read_csv("results/prewarming_simulation.csv")  # Run from root of project
except FileNotFoundError:
    df = pd.read_csv("../results/prewarming_simulation.csv")  # Run from plots/ folder

# Ensure figures folder exists
os.makedirs("figures", exist_ok=True)

# ------------------ 1. Confusion Matrix ------------------
print("[1/5] Confusion Matrix...")
y_true = df["Cold_Start"]
y_pred = df["cold_start_proba"] > 0.6

cm = confusion_matrix(y_true, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Warm", "Cold"])
disp.plot(cmap="Blues_r", values_format=".0f")
plt.title("Confusion Matrix: Cold Start Prediction")
plt.tight_layout()
plt.savefig("figures/confusion_matrix.png", dpi=300)
plt.close()

# ------------------ 2. Cost Comparison ------------------
print("[2/5] Cost Comparison...")
cold_cost = df["cold_start_cost"].sum()
prewarm_cost = df["prewarm_cost"].sum()
net_savings = cold_cost - prewarm_cost

labels = ["Cold Start Cost", "Prewarming Cost", "Net Savings"]
values = [cold_cost, prewarm_cost, net_savings]
colors = ["#77B5FE", "#D3D3D3", "#90EE90"]

plt.figure(figsize=(8, 5))
ax = sns.barplot(x=labels, y=values, palette=colors)
for i, v in enumerate(values):
    ax.text(i, v + 10, f"${v:,.2f}", ha='center', fontweight='bold')
plt.title("Cost Comparison: Cold Starts vs Smart Prewarming")
plt.ylabel("Cost (USD)")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("figures/cost_comparison.png", dpi=300)
plt.close()

# ------------------ 3. Delay Distribution ------------------
print("[3/5] Delay Distribution...")
plt.figure(figsize=(10, 4))
sns.histplot(df["Delay (s)"], bins=100, kde=True, color="skyblue")
plt.title("Delay Distribution")
plt.xlabel("Delay (seconds)")
plt.xlim(0, 3000)  # Zoom in on main range
plt.axvline(df["Delay (s)"].mean(), color='red', linestyle='--', label='Mean')
plt.legend()
plt.tight_layout()
plt.savefig("figures/delay_distribution.png", dpi=300)
plt.close()

# ------------------ 4. Probability Distribution ------------------
print("[4/5] Probability Distribution...")
plt.figure(figsize=(10, 4))
sns.histplot(df["cold_start_proba"], bins=50, kde=True, color="salmon")
plt.title("Cold Start Probability Distribution")
plt.xlabel("Probability")
plt.axvline(0.6, color='red', linestyle='--', label='Prediction Threshold (0.6)')
plt.legend()
plt.tight_layout()
plt.savefig("figures/probability_distribution.png", dpi=300)
plt.close()

# ------------------ 5. Cluster Scatter Plot ------------------
print("[5/5] Cluster Scatter Plot...")
if "cluster" in df.columns:
    print("✅ Cluster data found. Generating plot.")
    agg_df = df.groupby(["hour", "dayofweek", "cluster"]).agg({
        "Cold_Start": "mean",
        "Delay (s)": "mean"
    }).reset_index().rename(columns={"Cold_Start": "cold_start_ratio", "Delay (s)": "avg_delay"})

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=agg_df, x="cold_start_ratio", y="avg_delay", hue="cluster",
                    palette="Set2", s=100, alpha=0.8, edgecolor="black")
    plt.title("Clusters of Time Periods Based on Cold Start Behavior")
    plt.xlabel("Cold Start Ratio")
    plt.ylabel("Average Delay (s)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/cluster_scatter.png", dpi=300)
    plt.close()
else:
    print("⚠️ Skipping cluster plot — 'cluster' column not found.")

print("✅ All plots saved in the 'figures/' folder.")