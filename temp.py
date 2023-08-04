import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

final = pd.read_csv('Good-Books.csv')
final.drop_duplicates('Book-Title',inplace=True)
final.to_csv('Good-Books.csv')