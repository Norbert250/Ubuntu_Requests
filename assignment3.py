import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from collections import Counter
import re

try:
    df = pd.read_csv("metadata.csv")
    print("Dataset loaded successfully")
except FileNotFoundError:
    print("Error: metadata.csv not found")

print(df.shape)
df.info()
print(df.isnull().sum())

df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
df['year'] = df['publish_time'].dt.year
df['abstract'] = df['abstract'].fillna("")
df['abstract_word_count'] = df['abstract'].apply(lambda x: len(x.split()))

year_counts = df['year'].value_counts().sort_index()
plt.figure(figsize=(8,5))
plt.bar(year_counts.index, year_counts.values, color='skyblue')
plt.title("Number of Publications per Year")
plt.xlabel("Year")
plt.ylabel("Number of Papers")
plt.show()

top_journals = df['journal'].value_counts().head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis")
plt.title("Top 10 Journals Publishing COVID-19 Research")
plt.xlabel("Number of Papers")
plt.ylabel("Journal")
plt.show()

titles = df['title'].dropna().str.lower().str.cat(sep=' ')
words = re.findall(r'\b\w+\b', titles)
common_words = Counter(words).most_common(15)
words_df = pd.DataFrame(common_words, columns=['word','count'])
plt.figure(figsize=(8,5))
sns.barplot(x='count', y='word', data=words_df, palette='magma')
plt.title("Most Frequent Words in Paper Titles")
plt.show()

source_counts = df['source_x'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=source_counts.values, y=source_counts.index, palette='cool')
plt.title("Top Sources of Papers")
plt.xlabel("Number of Papers")
plt.ylabel("Source")
plt.show()

st.title("CORD-19 Data Explorer")
st.write("Interactive exploration of COVID-19 research papers")

year_min = int(df['year'].min())
year_max = int(df['year'].max())
year_range = st.slider("Select year range", year_min, year_max, (year_min, year_max))

filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
st.subheader(f"Papers from {year_range[0]} to {year_range[1]}")
st.dataframe(filtered_df[['title', 'journal', 'publish_time']].head(20))

st.subheader("Publications per Year")
year_counts_filtered = filtered_df['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts_filtered.index, year_counts_filtered.values, color='skyblue')
ax.set_xlabel("Year")
ax.set_ylabel("Number of Papers")
st.pyplot(fig)

st.subheader("Top Journals")
top_journals_filtered = filtered_df['journal'].value_counts().head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x=top_journals_filtered.values, y=top_journals_filtered.index, ax=ax2, palette="viridis")
st.pyplot(fig2)
