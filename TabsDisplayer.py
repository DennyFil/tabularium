import matplotlib.pyplot as plt

# Class used to display tabs
class TabsDisplayer:

    def display(self, title, tabs, tunings):
        
        num_strings = len(tunings)
        tunings_y_plot = [t.name for t in tunings]

        fig, ax = plt.subplots(figsize=(10, num_strings))
        ax.set_title(title)
        ax.set_yticks(range(1, num_strings + 1))
        ax.set_yticklabels(tunings_y_plot)

        x_note_start = []
        
        for tuning in tunings:
            tuning_tabs = list(filter(lambda tab: tab.tuning.name == tuning.name, tabs))

            print(f"tuning: {tuning.name}, nb notes: {len(tuning_tabs)}")
            if (len(tuning_tabs) > 0):
                x_note_start.extend([t.note.start for t in tuning_tabs])

                for idx_tab, tab in enumerate(tuning_tabs):
                    ax.text(idx_tab, tuning.idx, tab.fret_idx, color="blue", ha="center", va="center", fontsize=14)
                
        seen = set()
        x_note_start = [x for x in x_note_start if x not in seen and not seen.add(x)]
        x_note_start_sorted = sorted(x_note_start)
        
        ax.set_xticks(x_note_start_sorted)
        ax.set_ylim(0.5, num_strings + 0.5)
        ax.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.7)
        plt.show()
        