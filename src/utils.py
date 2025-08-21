import numpy as np
import pandas as pd

def get_summary(df):
    if 'category' in df.columns:
        summary = df.groupby('category').mean(numeric_only=True).reset_index()
    else:
        print ('not applicable')
    return summary