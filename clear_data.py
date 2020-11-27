import glob
import pandas as pd


# discentes
all_files = glob.glob(r'./data/discentes/*.csv')

li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, error_bad_lines=False, sep=";")
    li.append(df)

df_discentes = pd.concat(li, axis=0, ignore_index=True)
df_discentes = df_discentes[df_discentes['sexo'].isin(['M', 'F'])]
df_discentes.to_csv('./data/discentes.csv', sep=';', index=False)
