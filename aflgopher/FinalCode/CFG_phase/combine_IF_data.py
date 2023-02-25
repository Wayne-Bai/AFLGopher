import pandas as pd

first_part = pd.read_csv('if_data.csv')
second_part = pd.read_csv('if_cos.csv')

first_part['max_cos_similarity'] = second_part.max_cos_similarity
first_part['max_similarity_corresponding_ID'] = second_part.max_similarity_corresponding_ID

first_part.to_csv('whole_if_data.csv', index=False)