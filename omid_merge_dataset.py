from functools import reduce
import pandas as pd
import re

#the below identifies the text as main, for when it will be imported by other .py
def merge():
    
    #make sure to identify the right datasets in .csv format
    concerts = pd.read_csv("./datasets_original/concerts.csv", encoding="utf-8")
    works = pd.read_csv("./datasets_original/works.csv", encoding="utf-8")
    solo = pd.read_csv("./datasets_original/soloists.csv", encoding="utf-8")

    #removing phonetical characters (contained in square brackets) from names
    works["ConductorName"] = works["ConductorName"].apply(lambda x : re.sub("[\(\[].*?[\)\]]", "", x))
    #pd.DataFrame.apply() applies the function passed as argument to all elements in the dataframe
    #the function in this case is a lambda function 
    #(a lambda function is just like any normal python function, except that it has no name when defining it,
    #A lambda function evaluates an expression for a given argument.)
    #This lambda function takes x as input (x is an element of the dataframe) and returns re.sub("[\(\[].*?[\)\]]", "", x),
    # which means: "substitute everything between square brackets with a null character"
    works["ComposerName"] = works["ComposerName"].apply(lambda x : re.sub("[\(\[].*?[\)\]]", "", x))
    solo["Soloist_Name"] = solo["Soloist_Name"].apply(lambda x : re.sub("[\(\[].*?[\)\]]", "", x))
    
    #note that null strings("") get interpreted as np.nan (Not a Number) by pandas
    #which is of type <class 'float'>, while other "Instruments" are clearly of <class 'str'>
    
    i=1
    while type(solo["Soloist_Instrument"].iloc[-i]) == float:
        solo["Soloist_Instrument"].iloc[-i] = "Unknown Instrument"
        i+=1

    #if we want to eliminate rows with missing values 
    #solo.dropna(subset=["Soloist_Instrument"], inplace=True)
    
    #merging dataframes
    dfs=[concerts,works,solo]
    merged = reduce(lambda left, right: pd.merge(left, right, on='ID'), dfs)
    #reduce(func,seq) applies a function "func" on all elements of a sequence, in this case a list of pd.DataFrame
    #"func" is a lambda function having 2 inputs and returning pd.merge (left,right,on="ID") a pandas function
    #that unites two dataframes having a common header ( in this case "ID")

    #dropping duplicates with a pandas function designed to do so.
    merged.drop_duplicates()

    with open("./datasets/merged.csv","w",encoding="utf-8") as file_out:
        merged.to_csv(file_out, encoding="utf-8")