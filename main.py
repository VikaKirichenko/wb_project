import pandas as pd
from transform.transform_data import tokenize_lemmatize_text

df = pd.read_csv("data/products.csv")

# возьмем первые 20 элементов для быстроты экспериментов и простой проверки
df = df.drop(columns = ["Unnamed: 0"])
df_part = df.iloc[:20]
print(df_part[["Наименование","category"]])

