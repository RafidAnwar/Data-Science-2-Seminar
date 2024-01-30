import customtkinter as ctk
import tkinter as tk
from customtkinter import CTkImage
from tkinter import messagebox
from PIL import Image
from paper_health_regression_part_GUI import PAPER_HEALTH_REGRESSION_PART
from cslb_score_prediction_gui import CSLB_SCORE_PREDICTION_ANALYSIS

class MainApplication(ctk.CTk):
    def __init__(self, *args, **kwargs):
        # Constructor for the MainApplication class
        super().__init__(*args, **kwargs)

        # Set the title, geometry, and icon for the main application window
        self.title("DAP by Analytic Avengers")
        self.geometry("450x550")
        self.iconbitmap('dap.ico')

        # # Creating a frame in the center of the window to organize widgets
        center_frame = ctk.CTkFrame(self)
        center_frame.pack(expand=True)  # This will center the frame

        # Create a label with a welcome message
        label = ctk.CTkLabel(center_frame, text="Welcome to DAP!", font=("Comic Sans MS", 20, "bold"))
        label.pack(pady=10)

        # Create a Label Widget to display Image
        img = CTkImage(light_image=Image.open("dap.PNG"), size=(250, 250))
        label_image = ctk.CTkLabel(center_frame, text=None, image=img)
        label_image.pack()

        # Label to prompt the user to select a task
        label = ctk.CTkLabel(center_frame, text="Please select a task", font=("Arial", 14, "bold"))
        label.pack(pady=10)

        # CSLB Score Prediction Button - - opens a new window for cognitive dysfunction prediction
        btn_cslb = ctk.CTkButton(center_frame, text="Cognitive dysfunction Prediction",
                                 command=self.open_cslb_window)
        btn_cslb.pack(pady=10)

        # Regression Analysis Button - opens a new window for regression analysis of diseases
        btn_regression = ctk.CTkButton(center_frame, text="Regression Analysis of diseases",
                                       command=self.open_regression_window)
        btn_regression.pack(pady=10)

        # Creating a frame at the bottom for theme selection options
        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.pack(side="bottom", fill="x")

        # Dropdown menu for theme selection (Light, Dark, System)
        self.theme_option_variable = tk.StringVar(value="Change Theme")
        self.theme_option = ctk.CTkOptionMenu(bottom_frame,variable=self.theme_option_variable , values=["Light", "Dark", "System"],
                                              command=self.change_appearance_mode)
        self.theme_option.pack(side="right", pady=10)

        # README Button
        btn_readme = ctk.CTkButton(center_frame, text="Read me!", command=self.open_readme_window)
        btn_readme.pack(pady=10)

    # Function to open the regression analysis window
    def open_regression_window(self):
        PAPER_HEALTH_REGRESSION_PART()

    # Function to open the CSLB score prediction window
    def open_cslb_window(self):
        CSLB_SCORE_PREDICTION_ANALYSIS()

    # Function to show the read me window
    def open_readme_window(self):
        # Create a new top-level window
        readme_window = ctk.CTkToplevel(self)
        readme_window.title("README")
        readme_window.geometry("600x400")
        readme_window.attributes('-topmost', True)

        # Add a Text widget to the new window
        text_widget = ctk.CTkTextbox(readme_window, font=("Comic Sans MS", 15), wrap="word")
        text_widget.pack(expand=True, fill="both")

        # Read the contents from readme.txt and insert into the Text widget
        with open("readme.txt", "r", encoding='utf-8') as file:
            readme_text = file.read()
            text_widget.insert("1.0", readme_text)

        # Make the text widget read-only
        text_widget.configure(state="disabled")

    # Function to change the appearance theme of the application
    def change_appearance_mode(self, new_theme):
        ctk.set_appearance_mode(new_theme)

if __name__ == "__main__":
    # Setting the default theme and color and starting the application
    ctk.set_appearance_mode("System")  # Default theme
    ctk.set_default_color_theme("blue")
    window = MainApplication()
    window.mainloop()