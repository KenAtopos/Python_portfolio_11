from PIL import Image
from collections import Counter
import tkinter as tk
import tkinter.filedialog as filedialog

# Define the font styles used in the GUI
LARGE_FONT = ("Arial", 16)
MEDIUM_FONT = ("Arial", 12)


class ColorPaletteGenerator(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Set the window title and icon
        self.title("Color Palette Generator")
        self.iconbitmap("palette.ico")

        # Set the window size and position
        window_width = 640
        window_height = 480
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Create a container to hold the main content
        container = tk.Frame(self)
        container.pack(fill=tk.BOTH, expand=True)

        # Create a label and entry box for the image path
        image_frame = tk.Frame(container)
        image_frame.pack(pady=10)

        image_label = tk.Label(image_frame, text="Select an image file:", font=MEDIUM_FONT)
        image_label.pack(side="left")

        image_path = tk.Entry(image_frame, width=50, font=MEDIUM_FONT)
        image_path.pack(side="left", padx=10, ipady=5, expand=True)

        image_button = tk.Button(image_frame, text="Browse", font=MEDIUM_FONT, command=self.open_image)
        image_button.pack(side="left")

        # Create a label and text box to display the color palette
        output_frame = tk.Frame(container)
        output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        output_label = tk.Label(output_frame, text="Color Palette:", font=LARGE_FONT)
        output_label.pack(side="top", anchor="w", pady=10)

        output_box = tk.Text(output_frame, width=50, height=10, font=MEDIUM_FONT, wrap="word")
        output_box.pack(side="left", padx=10, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the output box
        output_scroll = tk.Scrollbar(output_frame, command=output_box.yview)
        output_scroll.pack(side="left", fill="y")

        output_box.config(yscrollcommand=output_scroll.set)

        # Add a button to generate the color palette
        generate_button = tk.Button(container, text="Generate Palette", font=LARGE_FONT, command=self.generate_color_palette)
        generate_button.pack(pady=10)

        # Save references to the image path entry and output box for later use
        self.image_path = image_path
        self.output_box = output_box

    def open_image(self):
        # Open a file dialog to select an image
        file_path = filedialog.askopenfilename()
        if file_path:
            # Update the image path in the entry box
            self.image_path.delete(0, tk.END)
            self.image_path.insert(0, file_path)
            # Generate the color palette for the selected image
            self.generate_color_palette()

    def generate_color_palette(self):
        # Load the image
        img = Image.open(self.image_path.get())

        # Resize the image to reduce memory usage and improve performance
        img = img.resize((256, 256))

        # Get a list of RGB values from the image
        rgb_values = list(img.getdata())

        # Count the frequency of each RGB value
        color_count = Counter(rgb_values)

        # Sort the colors by frequency (from most common to least common)
        most_common = color_count.most_common()

        # Clear the existing text in the output box
        self.output_box.delete("1.0", tk.END)

        # Print the RGB values of the top 10 colors in the output box
        for i, (color, count) in enumerate(most_common[:10], 1):
            # Add a colored box to the output box to represent each color
            color_box = tk.Text(self.output_box, width=5, height=1, font=MEDIUM_FONT, padx=5, pady=5, wrap="none")
            color_box.insert("1.0", "     ")
            color_box.tag_configure("center", justify="center")
            color_box.tag_add("center", "1.0", "end")
            color_box.tag_add(f"color{i}", "1.0", "end")
            # Get the RGB values of the current color
            r, g, b = color
            # Set the background color of the color box using the RGB values
            color_box.tag_config(f"color{i}", background=f"#{r:02x}{g:02x}{b:02x}",
                                 foreground="#ffffff")
            self.output_box.window_create("end", window=color_box)
            self.output_box.insert(tk.END, f" {count} pixels\n")
            self.output_box.tag_add(f"text{i}", tk.END, tk.END)
            self.output_box.tag_config(f"text{i}", font=MEDIUM_FONT)

        # Clear the existing text in the output box
        self.output_box.delete("1.0", tk.END)

        # Print the RGB values of the top 10 colors in the output box
        for i, (color, count) in enumerate(most_common[:10], 1):
            # Add a colored box to the output box to represent each color
            color_box = tk.Text(self.output_box, width=5, height=1, font=MEDIUM_FONT, padx=5, pady=5, wrap="none")
            color_box.insert("1.0", "     ")
            color_box.tag_configure("center", justify="center")
            color_box.tag_add("center", "1.0", "end")
            color_box.tag_add(f"color{i}", "1.0", "end")
            color_box.tag_config(f"color{i}", background=f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}",
                                 foreground="#ffffff")
            self.output_box.window_create("end", window=color_box)
            self.output_box.insert(tk.END, f" {count} pixels\n")
            self.output_box.tag_add(f"text{i}", tk.END, tk.END)
            self.output_box.tag_config(f"text{i}", font=MEDIUM_FONT)


# Create and run the main application
app = ColorPaletteGenerator()
app.mainloop()