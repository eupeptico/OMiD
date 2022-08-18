import pandas as pd
import matplotlib.pyplot as plt
#the below imports from the other code the two functions requested
from omid_functions import ranking_of, most_time_played

orchestra_dataframe = pd.read_csv("./datasets/merged.csv",encoding="utf-8")
#helper functions
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


###Graphs

#takes all event IDs and builds an histogram of duration in mins/event ID
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
    plt.show()

#shows a histogram of the top performing "what", based on the results of "ranking_of()" so the frequency, imported from orchestra.py
def show_top_by_event_frequency (df : pd.DataFrame, what: str, how_many : int = 5,):
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
    plt.xlabel(what)
    if rotate_ticks:
        plt.xticks(rotation=330)#ugly
    plt.show()

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
    plt.show()


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
    plt.show()

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
    
    plt.plot(tuple(plt_dates),tuple(plt_durations))
    plt.title("How many mins of music were played that day?")
    plt.ylabel("Duration")
    plt.xlabel("Date")
    plt.xticks([plt_dates[0], plt_dates[-1]], visible=True, rotation="horizontal")
    
    plt.show()


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