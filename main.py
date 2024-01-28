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
        self.theme_option = ctk.CTkOptionMenu(bottom_frame, values=["Light", "Dark", "System"],
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
        readme_text = (
            "DAP provides tools for Cognitive Dysfunction Prediction model which predicts the dogs current state of cognitive dysfunction and Regression Analysis of diseases which gives suggestions on how to reduce the affects of a disease based on selected variables.\n"
            "\nFollow the on-screen instructions to use each tool.\n\n"
            "For Cognitive Dysfunction Prediction:\n"
            "- Fill up the given questionnaire using the drop down menus.\n"
            "- The dog weight is taken as input, kindly put your dogs weight in lbs in the box.\n"
            "- Click submit button to get the current condition of your dogs health.\n"
            "- You maybe asked to answer some followup questions based on our score prediction. For that kindly come back after 6 months and fill up the rest of questionnaires and click submit again to get the actual cognitive dysfunction score of your dog.\n \n"
            "For Regression Analysis:\n"
            "- Select a disease and a variable from the drop down menus.\n"
            "- Click 'Get data for the desired choices'\n"
            "- View the suggestion and detailed regression results in the results window\n\n"
            "\nFor any assistance, contact Analytic Avengers."
        )
        messagebox.showinfo("README", readme_text)

    # Function to change the appearance theme of the application
    def change_appearance_mode(self, new_theme):
        ctk.set_appearance_mode(new_theme)

if __name__ == "__main__":
    # Setting the default theme and color and starting the application
    ctk.set_appearance_mode("System")  # Default theme
    ctk.set_default_color_theme("blue")
    window = MainApplication()
    window.mainloop()

