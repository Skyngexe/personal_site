import pandas as pd
import matplotlib.pyplot as plt

csv_path = r"c:\Users\Sky\Downloads\diabetes_data.csv"
output_image = "diabetes_europe_male_60_64.png"

# Read CSV
df = pd.read_csv(csv_path)

# Filter for European Region, Male, age 60-64, prevalence of diabetes
mask = (
    (df['location_name'] == 'European Region') &
    (df['sex_name'] == 'Male') &
    (df['age_name'] == '60-64 years') &
    (df['measure_name'] == 'Prevalence') &
    (df['cause_name'] == 'Diabetes mellitus') &
    (df['year'] >= 2015) & (df['year'] <= 2023)
)

df2 = df.loc[mask, ['year', 'val']].drop_duplicates().sort_values('year')

if df2.empty:
    print('No matching rows found for the specified filters.')
else:
    # Plot
    plt.figure(figsize=(8,4))
    plt.plot(df2['year'], df2['val'], marker='o', linewidth=2)
    plt.title('Diabetes prevalence rate (Male, 60-64) — European Region (2015–2023)')
    plt.xlabel('Year')
    plt.ylabel('Prevalence rate (val)')
    plt.xticks(df2['year'])
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_image, dpi=150)
    print(df2.to_string(index=False))
    print(f"Saved plot to {output_image}")
