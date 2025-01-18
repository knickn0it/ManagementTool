import database
from gui import EmployeeManagementApp
import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os

def main():
    # Create the database and table if not already created
    database.create_table()

    # Set up the GUI
    root = ctk.CTk()

    # Correct path to the icon file in the 'assets' folder (now PNG format)
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'icon.png')

    # Print the icon path for debugging
    print(f"Icon Path: {icon_path}")
    
    # Check if the icon file exists
    if os.path.exists(icon_path):
        # Open the image with Pillow
        img = Image.open(icon_path)
        img = img.resize((32, 32))  # Optional: Resize the icon (taskbar icons usually need to be small)
        icon = ImageTk.PhotoImage(img)  # Convert the image to a format Tkinter can use

        # Set the window and taskbar icon using iconphoto()
        root.iconphoto(True, icon)
        print("Icon set successfully.")
    else:
        print("Icon file not found. Please check the file path.")

    # Create the application window
    app = EmployeeManagementApp(root)
    
    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    main()
