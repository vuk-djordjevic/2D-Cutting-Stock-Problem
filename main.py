import tkinter as tk
from interface import RectangleInputApp

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