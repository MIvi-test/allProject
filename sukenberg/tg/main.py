from data.db import Database
import pandas as pd

dtb = Database()
resumes = dtb.get_full()

df = pd.DataFrame(data = open('History_1250880296.csv', 'r'))
print(df)