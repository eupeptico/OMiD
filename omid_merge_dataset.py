from functools import reduce
import pandas as pd
import re

if __name__ == "__main__":

    concerts = pd.read_csv("./datasets/concerts.csv")
    works = pd.read_csv("./datasets//works.csv")
    solo = pd.read_csv("./datasets/soloists.csv")

    #removing phonetical characters (contained in square brackets) from names
    works["ConductorName"] = works["ConductorName"].apply(lambda x : re.sub("[\(\[].*?[\)\]]", "", x))
    works["ComposerName"] = works["ComposerName"].apply(lambda x : re.sub("[\(\[].*?[\)\]]", "", x))
    solo["Soloist_Name"] = solo["Soloist_Name"].apply(lambda x : re.sub("[\(\[].*?[\)\]]", "", x))

    #merging dataframes
    dfs=[concerts,works,solo]
    merged = reduce(lambda left, right: pd.merge(left, right, on='ID'), dfs)

    #dropping duplicates
    merged.drop_duplicates()

    with open("./datasets/merged.csv","w", encoding="utf-8") as file_out:
        merged.to_csv(file_out)