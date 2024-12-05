import plotext as plt
import math

# Class used to display tabs
class TabsDisplayer:
    def __init__(self, measures_per_row, measure_duration):
        self.measures_per_row = measures_per_row
        self.measure_duration = measure_duration

    # Display tabs with 4 measures per row
    def display(self, title, tempo, duration, tabs, tunings):
        
        # compute number of tab rows to display
        num_rows = duration/self.measures_per_row/self.measure_duration
        num_rows_floor = math.floor(num_rows)
        num_rows = int(num_rows if num_rows_floor == num_rows else num_rows_floor + 1)

        print(f"tempo: {tempo}, duration: {duration}")

        num_strings = len(tunings)
        tunings_y_plot = [t.name for t in tunings]

        for row in range(num_rows):
            row_duration = self.measure_duration*self.measures_per_row
            start_time = row*row_duration
            end_time = start_time + row_duration

            print(f"row: {row}, start_time: {start_time}, end_time: {end_time}")
            
            plt.title(title)
            plt.ylim(0.5, num_strings + 1)
            plt.yticks(range(1, num_strings + 1), tunings_y_plot)
            plt.grid(0, 1)

            x_note_start = []
            
            for tuning in tunings:

                tuning_tabs = list(filter(lambda tab: tab.tuning.name == tuning.name and tab.note.start >= start_time and tab.note.start < end_time, tabs))

                print(f"tuning: {tuning.name}, nb notes: {len(tuning_tabs)}")
                for t in tuning_tabs:
                    print(f"note: {str(t.note)}, fret: {t.fret_idx}")

                if (len(tuning_tabs) > 0):
                    x_note_start.extend([t.note.start for t in tuning_tabs])

                    for idx_tab, tab in enumerate(tuning_tabs):
                        plt.scatter([tab.note.start], [tuning.idx], marker=str(tab.fret_idx), color="blue")
                    
            seen = set()
            x_note_start = [x for x in x_note_start if x not in seen and not seen.add(x)]
            x_note_start_sorted = sorted(x_note_start)
            
            plt.xticks(x_note_start_sorted, x_note_start_sorted)
            plt.xlim(-0.1 + min(x_note_start_sorted), row_duration + 0.1)

            plt.show()
            plt.clear_data()
            plt.clear_figure()
        