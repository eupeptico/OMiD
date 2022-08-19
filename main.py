import omid_functions as of
import omid_make_graphs as og
import omid_merge_dataset as om


def main():

    #merging datesets
    om.merge()
    #dataframe
    orchestra_dataframe = of.pd.read_csv("./datasets/merged.csv",encoding="utf-8")

    #Show results in command line PART
    # print("ranking of conductors:\n")
    # of.ranking_of_conductors(orchestra_dataframe)
    # print("ranking of composers:\n")
    # of.ranking_of_composers(orchestra_dataframe)
    # print("ranking of venues:\n")
    # of.ranking_of_venues(orchestra_dataframe)
    # print("best orchestra:\n")
    # of.best_orchestra(orchestra_dataframe)
    # print("best conductor\n")
    # of.most_frequent_conductor(orchestra_dataframe)
    # print("best venue\n")
    # of.most_frequent_venue(orchestra_dataframe)
    # print("best composer\n")
    # of.most_frequent_composer(orchestra_dataframe)


    #GRAPH PART
    og.duration_histo(orchestra_dataframe)
    og.show_top_by_event_frequency(orchestra_dataframe,"ComposerName",10)
    og.show_top_by_event_frequency(orchestra_dataframe,"Orchestra",3)
    og.show_top_by_event_frequency(orchestra_dataframe,"ConductorName",7)
    og.show_top_by_event_frequency(orchestra_dataframe,"Start_Time")
    og.show_top_by_event_frequency(orchestra_dataframe,"Duration",9)
    og.mean_duration_per(orchestra_dataframe,"Date")
    og.mean_duration_per(orchestra_dataframe,"ComposerName")
    og.mean_duration_per(orchestra_dataframe,"Venue")
    og.show_top_by_total_duration(orchestra_dataframe,"ConductorName",15)
    og.show_top_by_total_duration(orchestra_dataframe,"Venue",10)
    og.show_top_by_total_duration(orchestra_dataframe,"Orchestra",8)
    og.show_top_by_total_duration(orchestra_dataframe,"ComposerName",7)
    og.show_top_by_total_duration(orchestra_dataframe,"Event_Type",5)
    og.daily_durations(orchestra_dataframe)
    og.events_per_month(orchestra_dataframe)

if __name__ == "__main__":
    main()