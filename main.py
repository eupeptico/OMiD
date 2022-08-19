#!! to make sure the below packages work, install them using: pip install [name of package]
import pandas as pd
import matplotlib.pyplot as plt
from functools import reduce
import re

#the below identifies the text as main, for when it will be imported by other .py
if __name__ == "__main__":
    
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

### end of merging, start of functions ###

orchestra_dataframe = pd.read_csv("./datasets/merged.csv",encoding="utf-8")

#this function prints a synopsis of the event based on the given ID
def get_event_info(df : pd.DataFrame ,event_ID: int):
    #retrieves all event data identified by the same Event_ID
    event = df.loc[df['ID'] == event_ID]
    #if the event had multiple soloists, we have more than one row in the dataframe
    if len(event) > 1:
        print("Event_ID: ", event_ID)
        print("Event_Type: ",event.loc[:,"Event_Type"][0])
        print("Locaton: ",event.loc[:,"Location"][0])
        print("Venue: ",event.loc[:,"Venue"][0])
        print("Date: ",event.loc[:,"Date"][0])
        print("Started : ",event.loc[:,"Start_Time"][0],"Ended: ",event.loc[:,"End_Time"][0],"Duration: ",event.loc[:,"Duration"][0]," minutes")
        print("Playing Orchestra: ",event.loc[:,"Orchestra"][0])
        print("Composer: ",event.loc[:,"ComposerName"][0])
        print("Conductor: ",event.loc[:,"ConductorName"][0])
        soloists=event.loc[:,"Soloist_Name"]
        instruments = event.loc[:,"Soloist_Instrument"]
        ranks=event.loc[:,"Soloist_Rank"]
        print("Soloist(s): ")
        for solo,instr,rank in zip(soloists,instruments,ranks):
            print(f"{solo:<20}{instr:>20}{rank:>30}")
        print("\n\n\n")
        return
    #if there was only one soloist at the event, we'll have only one row in the dataframe
    print("Event_ID: ", event_ID)
    print("Event_Type: ",event.iloc[0]["Event_Type"])
    print("Locaton: ",event.iloc[0]["Location"])
    print("Venue: ",event.iloc[0]["Venue"])
    print("Date: ",event.iloc[0]["Date"])
    print("Started : ",event.iloc[0]["Start_Time"],"Ended: ",event.iloc[0]["End_Time"],"Duration: ",event.iloc[0]["Duration"]," minutes")
    print("Playing Orchestra: ",event.iloc[0]["Orchestra"])
    print("Composer: ",event.iloc[0]["ComposerName"])
    print("Conductor: ",event.iloc[0]["ConductorName"])
    solo=event.iloc[0]["Soloist_Name"]
    instr = event.iloc[0]["Soloist_Instrument"]
    rank=event.iloc[0]["Soloist_Rank"]
    print("Soloist: ")
    print(f"{solo:<20}{instr:>20}{rank:>30}")
    print("\n\n\n")

def best_orchestra( df : pd.DataFrame ):
    # best orchestra is based on the best ranked soloists for each event (means the event ID)

    #get unique Event_IDs from the dataset
    id_set=set(df.loc[:,'ID'])

    #dictionary with key=Event_ID and values = total soloist rank
    ID_to_Rank_Total = dict.fromkeys(id_set,0)
    ID_to_Ranks = dict.fromkeys(id_set,[])
    event_id_by_rank_score = 0
    min_rank_score = 999999999

    #this for cycle populates the two dictionaries created above
    for id,rank in zip(df.loc[:,'ID'],df.loc[:,'Soloist_Rank']):
        ID_to_Rank_Total[id]+=rank
        ID_to_Ranks[id].append(rank)

    #this for cycle scores the soloists on the basis of their rank
    for id in ID_to_Ranks.keys():
        lenght=len(ID_to_Ranks[id])
        rank_score = sum ([ ID_to_Ranks[id][x] / lenght  for x in range(lenght)])
        if rank_score < min_rank_score:
            min_rank_score = rank_score
            event_id_by_rank_score = id
    print("Best event based on the rank_score=sum(rank/n_soloist):\n")
    get_event_info(df,event_id_by_rank_score)
    event_id_by_total_rank = min(ID_to_Rank_Total,key=ID_to_Rank_Total.get)
    print("Best event based on the rank_score=sum(rank):\n")
    get_event_info(df,event_id_by_total_rank)

#this function identifies the most frequest what and will be used in the next functions
def most_frequent(df:pd.DataFrame, what : str):
    #For all of those categories where the best is simply the most frequent one

    #get unique whatever names
    whatever_set=set(df.loc[:,what])

    #dictionary with key=whatever, value = list od Event_IDs
    whatever_to_ID = dict.fromkeys(whatever_set,set())

    best = ""
    most_events=-1

    for key in whatever_set:
        #print(set(df.loc[df["Venue"]==venue]["ID"]))
        whatever_to_ID[key]=set(df.loc[df[what]==key]["ID"])
        #print("DEBUGGING: ",venue, venue_to_ID[conductor])
        events_played=len(whatever_to_ID[key])
        if events_played > most_events:
            most_events=events_played
            best=key
    return best, most_events

#the 3 functions below identify the most recurrent conductor, venue and composer

def most_frequent_conductor( df : pd.DataFrame ):

    bestconductor, most_events_played = most_frequent(df,"ConductorName")

    print(bestconductor, "conducted ", most_events_played," events.")
    print("\n")


def most_frequent_venue(df : pd.DataFrame):

    bestvenue, most_events_played = most_frequent(df, "Venue")

    print(bestvenue, " was used for ", most_events_played," events.")
    print("\n")

def most_frequent_composer(df: pd.DataFrame):

    bestcomposer, most_events_played = most_frequent(df, "ComposerName")

    print(bestcomposer, "'s works were played in ", most_events_played," events.")
    print("\n")

    
#this is the same as most_frequent, but instead of return 1 most frequent whatever, returns the how_many you decide
def ranking_of(df:pd.DataFrame, what:str, how_many : int = 5):
    #displays the top n (default=5) of whateverbased on frequency
    #returns a pair of lists made by slicing the last "how_many" elements from "best" and "n_events"
    whatever_set=set(df.loc[:,what]) 
    #dictionary with key=whatever, value = list od Event_IDs
    whatever_to_ID = dict.fromkeys(whatever_set,set())

    for key in whatever_set:
        whatever_to_ID[key]=len(set(df.loc[df[what]==key]["ID"]))
        #this populates a dictionary where the key are all the entries are the what, while the values are the number of events (based on ID) where the what is present
        #set is needed to display only unique values

    #this creates two lists using the population of the dictionary based on the values (number of events) and the keys (what)
    #the *sorted orders the values in ascending order and the keys accordingly
    a,b = zip(*sorted(zip(whatever_to_ID.values(),whatever_to_ID.keys())))
    #get the last "how_many" elements, which are the most frequently recurring
    best=list(b[-how_many:])
    n_events=list(a[-how_many:])

    #return the reversed list (reversed using the list slice [::-1])
    return best[::-1],n_events[::-1]

#in these three functions the what is defined
def ranking_of_conductors(df:pd.DataFrame):
    top_conductors,events_played = ranking_of(df,"ConductorName")
    print("Conductor:                Events played:")
    for conductor,ep in zip(top_conductors,events_played):
        print(f"{conductor:<30}{ep:>10}")   
    print("\n")

def ranking_of_venues(df:pd.DataFrame):
    top_venues, events_played = ranking_of(df,"Venue")
    print("Venue:                    Events played:")
    for venue,ep in zip (top_venues,events_played):
        print(f"{venue:<30}{ep:>10}")
    print("\n")

def ranking_of_composers(df:pd.DataFrame):
    top_composers, events_played = ranking_of(df,"ComposerName")
    print("Composer:                 Events played:")
    for composer,ep in zip(top_composers,events_played):
        print(f"{composer:<30}{ep:>10}")
    print("\n")

#this function ranks the whatever on the basis of the amount of hours it appears in the dataframe
def most_time_played(df : pd.DataFrame, what : str, how_many : int = 5):
    #displays the top n (default=5) of whatever based on time played (sum of durations) only
    #returns a pair of lists made by slicing the last "how_many" elements from "best" and "time_played"

    whatever_set=set(df.loc[:,what]) 
    #dictionary with key=whatever, value = list o Event_IDs
    whatever_to_ID = dict.fromkeys(whatever_set,set())

    for key in whatever_set:
        whatever_to_ID[key]=sum(df.loc[df[what]==key]["Duration"])

    a,b = zip(*sorted(zip(whatever_to_ID.values(),whatever_to_ID.keys())))
    #get the last "how_many" elements
    best=list(b[-how_many:])
    time_played=list(a[-how_many:])

    #return the reversed list (reversed using the list slice [::-1])
    return best[::-1],time_played[::-1]

### end of functions, start of plotting ###

###helper functions
def get_surname(full_name : str):
    #mainly to get cleaner graphs by keeping only the surname to identify people
    #fails with no harm because if the string has no ", " separator, split(", ")[0] returns the full string
    return full_name.split(", ")[0]

def year_of(date : str):
    # returns the last 4 characters of a string.
    # If "date" is formatted as DD/MM/YYYY or MM/DD/YYYY, it returns the year
    # (assuming there is no data before year 1000 and after year 9999)
    return date[-4:]

#this makes the mean of the elements of it, used later
def mean(it): return sum(it)/len(it)

#this makes nice labels for the charts
def label(what:str):
    label_dictionary={
        "Event_Type":"Event Type",
        "Start_Time":"Start Time",
        "End_Time":"End Time",
        "ComposerName":"Composer",
        "ConductorName":"Conductor",
        "Soloist_Rank":"Soloist Rank",
        "Soloist_Name":"Soloist Name",
        "Soloist_Instrument":"Instrument",       
    }
    if what not in label_dictionary.keys(): #for example date...
        return what
    return label_dictionary[what]


###Graphs###

## 1 - shows an histogram of duration in mins per event ID
def duration_histo (df : pd.DataFrame):
    durations = df.loc[:,"Duration"]
    events = df.loc[:,"ID"]
    mean = sum(durations)/len(durations)
    plt.bar(events,durations,label="Data")
    plt.title("Events by duration")
    plt.plot([mean for _ in range(max(events))],label="Mean",linestyle="--",color="red")
    plt.legend(loc="upper left")
    plt.ylabel("Duration in min")
    plt.xlabel("Event IDs")
    plt.show() #this will make the chart pop up
    #plt.savefig("./charts/events_duration") #this will save the .png but has issues

#shows a histogram of the top performing "what", based on the results of "ranking_of()" so the frequency, imported from orchestra.py
def show_top_by_event_frequency (df : pd.DataFrame, what:str, how_many:int=5,):
    #(what = "ConductorName", "ComposerName", "Venue", ...)
    rotate_ticks=False
    top_whatever, events_played = ranking_of(df,what,how_many)
    #the what should not be duration, ID or soloist rank. If it is, we run the get_surname to make sure the what is a string
    if what not in ["Duration", "ID","Soloist_Rank"]:
        top = [get_surname(x) for x in top_whatever]
        if mean([len(x) for x in top]) > 7: rotate_ticks=True #names are tilted of long
    else: top = top_whatever

    plt.bar(top,events_played,label="Data")
    #plt.legend(loc="upper right")
    plt.title(f"Which {label(what)} is the most frequent?")
    plt.ylabel("number of Events")
    #xlabels get mixed up because of the lenght of the names
    #plt.xlabel(what)
    if rotate_ticks:
        plt.xticks(rotation=330)#ugly
    plt.show() #this will make the chart pop up
    #plt.savefig(f"./charts/top_{what}_by_event_frequency") #this will save the .png

#shows a histogram of the top performing "what", based on the results of "most_time_played()" so the duration, imported from orchestra.py
def show_top_by_total_duration (df : pd.DataFrame, what: str, how_many : int = 5,):
    #(what = "ConductorName", "ComposerName", "Venue", ...)
    rotate_ticks=False
    top_whatever, events_played = most_time_played(df,what,how_many)
    if what not in ["Duration", "ID","Soloist_Rank"]:
        top = [get_surname(x) for x in top_whatever]
        if mean([len(x) for x in top]) > 7: rotate_ticks=True
    else: top = top_whatever

    plt.bar(top,events_played,label="Data")
    #plt.legend(loc="upper right")
    plt.title(f"Top {label(what)} by total time played")
    plt.ylabel("Time played in min")
    #xlabels get mixed up because of the lenght of the names
    plt.xlabel(what)
    if rotate_ticks:
        plt.xticks(rotation=330)#ugly
    plt.show() #this will make the chart pop up
    #plt.savefig("./charts/top_{}_by_total_duration".format(what)) #this will save the .png


#shows the average duration of events per whatever (year, composer, etc)
def mean_duration_per(df: pd.DataFrame, what:str):

    whatever = df.loc[:,what]
    durations = df.loc[:,"Duration"]

    #choosing which function to apply 
    #see helper function "year_of" and "get_surname"
    if what == "Date":
        whatever_set = set(whatever.apply(year_of))
    else:
        whatever_set = set(whatever.apply(get_surname))

    #dictionaries to keep track of durations and average duration
    whatever_to_durations=dict.fromkeys(whatever_set,[])
    whatever_to_durations_mean = dict.fromkeys(whatever_set,int)

    #populate the durations dictionary
    for x,duration in zip(whatever,durations):
        if what == "Date":
            whatever_to_durations[year_of(x)].append(duration)
            whatever_to_durations_mean[year_of(x)]=mean(whatever_to_durations[year_of(x)])
        else:
            whatever_to_durations[get_surname(x)].append(duration)
            whatever_to_durations_mean[get_surname(x)]=mean(whatever_to_durations[get_surname(x)])
    
    plt_whatever,plt_duration_mean = zip(*sorted(zip(whatever_to_durations_mean.keys(),whatever_to_durations_mean.values())))

    #plotting part
    plt.plot(tuple(plt_whatever),tuple(plt_duration_mean))

    if len(plt_whatever) >= 20:
        plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=True,       # ticks along the bottom edge are on
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off

    plt.title(f"Event's mean duration per {label(what)}")
    plt.ylabel("Mean duration in min")
    plt.xlabel(f"{label(what)}")
    plt.show() #this will make the chart pop up
    #plt.savefig(f"./charts/mean_duration_per_{what}") #this will save the .png

#makes chart of durations of event in given dates (how many hours of music was played that day?)
def daily_durations(df : pd.DataFrame):
    dates = df.loc[:,"Date"]
    durations = df.loc[:,"Duration"]
    x_ticks=[]
    unique_dates = []
    unique_durations = []

    for date,duration in zip(dates,durations):
        if date not in unique_dates:
            unique_dates.append(date)
            unique_durations.append(duration)
            if duration > 300 :
                x_ticks.append(date)

    plt_dates,plt_durations = zip(*sorted(zip(unique_dates,unique_durations)))
    
    # x_ticks.append(plt_dates[-1])
    # x_ticks.insert(0,plt_dates[0])    
    
    plt.plot(tuple(plt_dates),tuple(plt_durations))#matplotlyb wants an unmodifiable object for this, so the tuple
    plt.title("How many mins of music were played that day?")
    plt.ylabel("Duration")
    plt.xlabel("Date")
    plt.xticks([plt_dates[0], plt_dates[-1]], visible=True, rotation="horizontal")
    plt.show() #this will make the chart pop up
    #plt.savefig(f"./charts/daily_durations") #this will save the .png

#this calls the functions and makes the charts
if __name__ == "__main__":

    duration_histo(orchestra_dataframe)
    show_top_by_event_frequency(orchestra_dataframe,"ComposerName",10)
    show_top_by_event_frequency(orchestra_dataframe,"Orchestra",3)
    show_top_by_event_frequency(orchestra_dataframe,"ConductorName",7)
    show_top_by_event_frequency(orchestra_dataframe,"Start_Time")
    show_top_by_event_frequency(orchestra_dataframe,"Duration",9)
    mean_duration_per(orchestra_dataframe,"Date")
    mean_duration_per(orchestra_dataframe,"ComposerName")
    mean_duration_per(orchestra_dataframe,"Venue")
    show_top_by_total_duration(orchestra_dataframe,"ConductorName",15)
    show_top_by_total_duration(orchestra_dataframe,"Venue",10)
    show_top_by_total_duration(orchestra_dataframe,"Orchestra",8)
    show_top_by_total_duration(orchestra_dataframe,"ComposerName",7)
    show_top_by_total_duration(orchestra_dataframe,"Event_Type",5)
    daily_durations(orchestra_dataframe)