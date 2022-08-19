import pandas as pd
orchestra_dataframe = pd.read_csv("./datasets/merged.csv")

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
    
#this executes the functions and prints the results
if __name__ == "__main__":
    print("ranking of conductors:\n")
    ranking_of_conductors(orchestra_dataframe)
    print("ranking of composers:\n")
    ranking_of_composers(orchestra_dataframe)
    print("ranking of venues:\n")
    ranking_of_venues(orchestra_dataframe)
    print("best orchestra:\n")
    best_orchestra(orchestra_dataframe)
    print("best conductor\n")
    most_frequent_conductor(orchestra_dataframe)
    print("best venue\n")
    most_frequent_venue(orchestra_dataframe)
    print("best composer\n")
    most_frequent_composer(orchestra_dataframe)