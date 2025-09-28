import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

try:
    iris = load_iris()
    df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)
    print("First 5 rows of the dataset:")
    display(df.head())
    print("\nDataset info:")
    df.info()
    print("\nMissing values per column:")
    print(df.isnull().sum())
except Exception as e:
    print(f"Error loading dataset: {e}")

print("\nBasic statistics of numerical columns:")
display(df.describe())

species_group = df.groupby('species').mean()
print("\nMean values of features by species:")
display(species_group)

sns.set(style="whitegrid")

plt.figure(figsize=(8,5))
species_group['sepal length (cm)'].plot(kind='line', marker='o')
plt.title("Average Sepal Length per Species")
plt.xlabel("Species")
plt.ylabel("Sepal Length (cm)")
plt.xticks(ticks=range(len(species_group)), labels=species_group.index)
plt.show()

plt.figure(figsize=(8,5))
sns.barplot(x='species', y='petal length (cm)', data=df, ci=None)
plt.title("Average Petal Length per Species")
plt.xlabel("Species")
plt.ylabel("Petal Length (cm)")
plt.show()

plt.figure(figsize=(8,5))
plt.hist(df['sepal width (cm)'], bins=15, color='skyblue', edgecolor='black')
plt.title("Distribution of Sepal Width")
plt.xlabel("Sepal Width (cm)")
plt.ylabel("Frequency")
plt.show()

plt.figure(figsize=(8,5))
sns.scatterplot(x='sepal length (cm)', y='petal length (cm)', hue='species', data=df, s=80)
plt.title("Sepal Length vs Petal Length by Species")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Petal Length (cm)")
plt.legend(title='Species')
plt.show()

print("\nObservations:")
print("- Setosa species tends to have smaller petal and sepal lengths compared to Versicolor and Virginica.")
print("- Petal length and sepal length appear positively correlated, especially in Versicolor and Virginica.")
print("- Sepal width has a roughly normal distribution across all species.")
