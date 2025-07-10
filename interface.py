import tkinter as tk
from tkinter import messagebox, font as tkfont
from GA import genetic_algorithm

class RectangleInputApp:
    def __init__(self, master):
        self.master = master
        self.master.title("2D Cutting Problem")
        self.master.geometry("600x600")
        self.master.resizable(False, False)
        self.master.configure(bg="#F9EDE1")

        self.rectangles = []
        self.custom_font = tkfont.Font(family="Segoe UI", size=10)
        self.list_font = tkfont.Font(family="Segoe UI", size=11, weight="normal")


        # Material Dimensions 
        material_frame = tk.LabelFrame(master, text="Material Dimensions", padx=10, pady=10, bg="#F9EDE1", font=self.custom_font)
        material_frame.pack(padx=20, pady=10, fill="x")

        self._add_centered_entry_row(material_frame, "Material width:", 0)
        self.material_width_entry = self._create_entry(material_frame)
        self.material_width_entry.grid(row=0, column=1, pady=5)

        self._add_centered_entry_row(material_frame, "Material height:", 1)
        self.material_height_entry = self._create_entry(material_frame)
        self.material_height_entry.grid(row=1, column=1, pady=5)

        # Rectangle Input
        rectangle_frame = tk.LabelFrame(master, text="Rectangle Input", padx=10, pady=10, bg="#F9EDE1", font=self.custom_font)
        rectangle_frame.pack(padx=20, pady=10, fill="x")

        self._add_centered_entry_row(rectangle_frame, "Rectangle width:", 0)
        self.rect_width_entry = self._create_entry(rectangle_frame)
        self.rect_width_entry.grid(row=0, column=1, pady=5)

        self._add_centered_entry_row(rectangle_frame, "Rectangle height:", 1)
        self.rect_height_entry = self._create_entry(rectangle_frame)
        self.rect_height_entry.grid(row=1, column=1, pady=5)

        self._add_centered_entry_row(rectangle_frame, "Quantity:", 2)
        self.rect_count_entry = self._create_entry(rectangle_frame)
        self.rect_count_entry.grid(row=2, column=1, pady=5)

        self.add_button = tk.Button(rectangle_frame, text="Add Rectangle", font=self.custom_font,
                                    command=self.add_rectangle, bg="#e3c8b7", activebackground="#d8b5a3")
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # List Frame
        list_frame = tk.LabelFrame(master, text="Added Rectangles", padx=10, pady=10, bg="#F9EDE1", font=self.custom_font)
        list_frame.pack(padx=20, pady=5, fill="x")

        self.rect_listbox = tk.Listbox(list_frame, width=50, height=6, font=self.list_font, bg="#fff5ef", relief=tk.GROOVE, justify="center")
        self.rect_listbox.pack(padx=5, pady=5)

        # Button Row: Remove & Reset & Done
        button_frame = tk.Frame(master, bg="#F9EDE1")
        button_frame.pack(pady=15)

        self.remove_button = tk.Button(button_frame, text="Remove", font=self.custom_font,
                                       command=self.remove_selected_rectangle, bg="#d89c9c", activebackground="#c87b7b")
        self.remove_button.grid(row=0, column=0, padx=15, pady=5)

        self.reset_button = tk.Button(button_frame, text="Reset", font=self.custom_font,
                              command=self.reset_all, bg="#e4c2c2", activebackground="#dba7a7")
        self.reset_button.grid(row=0, column=2, padx=15, pady=5)

        self.done_button = tk.Button(button_frame, text="Done", font=self.custom_font,
                                     command=self.done_clicked, bg="#a7d7c5", activebackground="#8fcab5")
        self.done_button.grid(row=0, column=1, padx=15, pady=5)

    def _add_centered_entry_row(self, frame, label_text, row):
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        label = tk.Label(frame, text=label_text, bg="#F9EDE1", font=self.custom_font)
        label.grid(row=row, column=0, sticky="e", padx=5, pady=5)

    def _create_entry(self, parent):
        return tk.Entry(parent, justify='center', font=self.custom_font, width=20)

    def add_rectangle(self):
        """Add rectangle entry to the internal list and listbox."""
        try:
            width = int(self.rect_width_entry.get())
            height = int(self.rect_height_entry.get())
            number = int(self.rect_count_entry.get())

            self.rectangles.append({"width": width, "height": height, "number": number})
            self.rect_listbox.insert(tk.END, f"{number} x {width}x{height}")

            # Clear inputs
            self.rect_width_entry.delete(0, tk.END)
            self.rect_height_entry.delete(0, tk.END)
            self.rect_count_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Input Error", "All inputs must be integers.")

    def remove_selected_rectangle(self):
        """Remove selected rectangle from list and internal data."""
        selection = self.rect_listbox.curselection()
        if selection:
            index = selection[0]
            del self.rectangles[index]
            self.rect_listbox.delete(index)
        else:
            messagebox.showinfo("Selection Required", "Please select a rectangle to remove.")

    def done_clicked(self):
        """Validates inputs and simulates project execution (future implementation)."""
        try:
            mat_width = int(self.material_width_entry.get())
            mat_height = int(self.material_height_entry.get())
        except ValueError:
            messagebox.showerror("Validation Error", "Material dimensions must be valid integers.")
            return

        if len(self.rectangles) < 1:
            messagebox.showwarning("Validation Error", "Please add at least 1 rectangle before proceeding.")
            return

        # Simulate final action
        self.material_dimensions = (mat_width, mat_height)
        self.given_rectangles = self.rectangles
        print("Material dimensions:", self.material_dimensions)
        print("Rectangles to cut:", self.given_rectangles)
        genetic_algorithm(
            population_size=100,
            dimensions=self.given_rectangles,
            paper_width=mat_width,
            paper_height=mat_height,
            generations=200
        )
    
    def reset_all(self):
        """Resetuje sve unose i listu pravougaonika."""
        self.material_width_entry.delete(0, tk.END)
        self.material_height_entry.delete(0, tk.END)
        self.rect_width_entry.delete(0, tk.END)
        self.rect_height_entry.delete(0, tk.END)
        self.rect_count_entry.delete(0, tk.END)

        self.rectangles.clear()
        self.rect_listbox.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = RectangleInputApp(root)
    root.mainloop()

    try:
        print("\nFinal collected data:")
        print("Material:", app.material_dimensions)
        print("Rectangles:", app.given_rectangles)
    except AttributeError:
        print("Input was not completed.")
