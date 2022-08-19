import omid_functions as f
import omid_make_graphs as graph
import omid_merge_dataset as m

def main():
    graph.duration_histo(graph.orchestra_dataframe)
    graph.show_top_by_event_frequency(graph.orchestra_dataframe,"ComposerName",10)
    graph.show_top_by_event_frequency(graph.orchestra_dataframe,"Orchestra",3)
    graph.show_top_by_event_frequency(graph.orchestra_dataframe,"ConductorName",7)
    graph.show_top_by_event_frequency(graph.orchestra_dataframe,"Start_Time")
    graph.show_top_by_event_frequency(graph.orchestra_dataframe,"Duration",9)
    graph.mean_duration_per(graph.orchestra_dataframe,"Date")
    graph.mean_duration_per(graph.orchestra_dataframe,"ComposerName")
    graph.mean_duration_per(graph.orchestra_dataframe,"Venue")
    graph.show_top_by_total_duration(graph.orchestra_dataframe,"ConductorName",15)
    graph.show_top_by_total_duration(graph.orchestra_dataframe,"Venue",10)
    graph.show_top_by_total_duration(graph.orchestra_dataframe,"Orchestra",8)
    graph.show_top_by_total_duration(graph.orchestra_dataframe,"ComposerName",7)
    graph.show_top_by_total_duration(graph.orchestra_dataframe,"Event_Type",5)
    graph.daily_durations(graph.orchestra_dataframe)

if __name__ == "__main__":
    main()