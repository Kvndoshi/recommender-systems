import pandas.core.indexes.base
import sys

sys.modules['pandas.core.indexes.numeric'] = pandas.core.indexes.base
import pickle

with open("popular_df.pkl", "rb") as f:
    try:
        data = pickle.load(f)
        print(data)
    except Exception as e:
        print(f"Error: {e}")
