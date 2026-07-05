import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("data/merged_clean.csv", low_memory=False)
numeric_df = df.select_dtypes(include="number")
corr = numeric_df.corr()

plt.figure(figsize=(20, 16))
sns.heatmap(corr, cmap="coolwarm", center=0)
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
print("Saved correlation_heatmap.png")
