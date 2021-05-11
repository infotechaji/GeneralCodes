import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv_path  = "G:\Ajith\Others\Ajith-self-emp\Image-classification\med_Training_set.csv"
brain_df = pd.read_csv(csv_path)
brain_df.head()
brain_df.tail()
