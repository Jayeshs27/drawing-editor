import tkinter as tk

def on_button_click():
    print("Button clicked")

def on_color_selected(color):
    print("Color selected:", color)

root = tk.Tk()
root.geometry("800x600")

# Create frames for toolbar and canvas
toolbar_frame = tk.Frame(root, width=100, bg="light gray")
canvas_frame = tk.Frame(root, bg="white")

toolbar_frame.pack(side=tk.LEFT, fill=tk.Y)
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

buttons_frame = tk.Frame(toolbar_frame, width=100, bg='light gray')
buttons_frame.grid(row=0,column=0)

colors_frame = tk.Frame(toolbar_frame, width=100, bg='white')
colors_frame.grid(row=1,column=0)

# Create buttons in the toolbar
for i in range(5):
    for j in range(2):
        btn = tk.Button(buttons_frame, text=f"Button {i}{j}", width=10, height=2, command=on_button_click)
        btn.grid(row=i, column=j, padx=5, pady=5)

# Create a color palette in the toolbar
colors = ["red", "blue", "green", "yellow", "orange", "purple", "black", "white"]
for i, color in enumerate(colors):
    color_btn = tk.Button(colors_frame, bg=color, width=2, height=1, command=lambda c=color: on_color_selected(c))
    color_btn.grid(row=6 + i//2, column=i % 2, padx=5, pady=5)

# Create a canvas
canvas = tk.Canvas(canvas_frame, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

root.mainloop()
