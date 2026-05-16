import pandas as pd
import numpy as np
import plotly.express as px

np.random.seed(42)

n = 1000

date_range = pd.date_range("2023-01-01", "2026-05-31", freq="D")

df = pd.DataFrame({
    "Order Date": np.random.choice(date_range, n),
    "Ship Date": np.random.choice(date_range, n),
    "Category": np.random.choice(["Furniture", "Office Supplies", "Technology"], n),
    "Sub-Category": np.random.choice(["Phones", "Tables", "Paper", "Accessories"], n),
    "Sales": np.random.uniform(50, 2000, n),
    "Profit": np.random.uniform(-200, 800, n),
    "Region": np.random.choice(["Nord", "Sud", "Est", "Ovest"], n),
    "State": np.random.choice(["Italy", "Germany", "France", "Spain"], n),
    "Quantity": np.random.randint(1, 10, n)
})


df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df = df.dropna()
df = df.drop_duplicates()


df["Year"] = df["Order Date"].dt.year

print("\nDATASET PULITO")
print(df.head())


yearly = df.groupby("Year")[["Sales", "Profit"]].sum().reset_index()

fig1 = px.bar(
    yearly,
    x="Year",
    y=["Sales", "Profit"],
    barmode="group",
    title="Vendite e Profitti per Anno"
)
fig1.show()


top5 = df.groupby("Sub-Category")["Sales"].sum().nlargest(5).reset_index()

fig2 = px.bar(
    top5,
    x="Sub-Category",
    y="Sales",
    title="Top 5 Sottocategorie"
)
fig2.show()


map_data = df.groupby("State")["Sales"].sum().reset_index()

fig3 = px.choropleth(
    map_data,
    locations="State",
    locationmode="country names",
    color="Sales",
    title="Mappa Vendite Europa"
)

fig3.show()