import plotext as plt

# Main data
x = [1, 2, 3, 4]
y = [1, 4, 9, 16]

# Text labels (as extra data)
text_x = [1, 2, 3, 4]
text_y = [2, 5, 10, 17]  # Slight offset for better readability
labels = ["Point 1", "Point 2", "Point 3", "Point 4"]

# Plot the main data
#plt.scatter(x, y, marker='o', color='cyan')

# Add text "manually" as scatter points with text-like markers
for tx, ty, label in zip(text_x, text_y, labels):
    print(tx)
    print(ty)
    print(label)
    plt.scatter([tx], [ty], marker="a", color="blue")

# Set the limits to make sure annotations are visible
plt.xlim(0, 5)
plt.ylim(0, 20)

# Show the plot
plt.show()