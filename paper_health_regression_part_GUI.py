import customtkinter as ctk
import subprocess
import threading

def PAPER_HEALTH_REGRESSION_PART():
    # This is the main function to launch the regression analysis part of the application.
    def calculate_result():
        # Function to initiate the calculation process.
        # Starts a loading animation and triggers calculations for each selected option.
        start_loading_animation()
        for option in options:
            if options[option].get():
                # For each option checked by the user, start a separate thread to handle the calculation.
                threading.Thread(target=run_calculation, args=(option,)).start()

    def run_calculation(user_choice_2):
        # Function to run the actual calculation process.
        # Takes user's second choice as an argument to run specific analysis.
        user_choice_1 = user_choice_1_dropdown.get()

        # Runs a subprocess to execute the calculation script with the provided arguments.
        result = subprocess.run(["pythonw.exe", 'paper_health_regression_part.py', user_choice_1, user_choice_2],
                                capture_output=True, text=True, encoding='utf-8')
        # Once the subprocess completes, display the result and stop the loading animation.
        display_result(result.stdout.strip(), user_choice_2)
        stop_loading_animation()
        loading_label.configure(text="")

    def start_loading_animation():
        # Function to initiate a loading animation on the GUI.
        # Updates the loading label to inform the user that the result is being processed.
        loading_label.configure(text="Result is loading, please wait")
        animate_loading()

    def stop_loading_animation():
        # Function to stop the loading animation.
        # Cancels the after method used for animation and resets the loading label text.
        loading_label.after_cancel(animation_id)
        loading_label.configure(text="")

    def animate_loading():
        # Function to control the steps of the loading animation.
        # Resets and starts the animation steps.
        global animation_step
        animation_step = 0
        animate_loading_step()

    def animate_loading_step():
        # Recursive function to animate loading text.
        # Adds dots to the loading label and cycles through animation steps.
        global animation_step, animation_id
        if animation_step < 4:
            loading_label.configure(text=loading_label.cget("text") + ".")
            animation_step += 1
            animation_id = loading_label.after(500, animate_loading_step)
        else:
            # After 4 dots, reset the animation
            loading_label.configure(text="Result is loading, please wait")
            animation_step = 0
            animate_loading_step()

    def parse_result_text(result_text):
        # Function to parse the result text into a readable format for display.
        # Splits the result text into two parts: suggestions and regression details.
        lines = result_text.split("\n")
        index = lines.index("Detailed result of logistic regression results")
        suggestions = [line.replace(">>", "• ") for line in lines[:index]]
        regression_details = [line.replace(">>", "• ") for line in lines[index:]]
        return suggestions, regression_details

    def display_result(result_text, choice):
        # Function to display the parsed results in a new window.
        # Splits the results into suggestions and regression details and displays them.
        suggestions, regression_details = parse_result_text(result_text)

        # Create a new window to display the results.
        result_window = ctk.CTkToplevel(root)
        result_window.title(f"Regression Analysis Result - {choice}")
        result_window.geometry("1200x800")
        result_window.iconbitmap('dap.ico')
        result_window.attributes('-topmost', True)

        # Define a larger font for displaying results.
        result_font = ("Comic Sans MS", 15)

        # Create and configure a frame to hold the result labels.
        table_frame = ctk.CTkFrame(result_window)
        table_frame.pack(pady=20, padx=10, fill="both", expand=True)
        table_frame.grid_columnconfigure(0, weight=1)
        table_frame.grid_columnconfigure(1, weight=1)

        # Populate the frame with suggestion and detail labels.
        for i, (suggestion, detail) in enumerate(zip(suggestions, regression_details), start=1):
            suggestion_label = ctk.CTkLabel(table_frame, text=suggestion, font=result_font, wraplength=600, anchor="w",
                                            justify="left")
            suggestion_label.grid(row=i * 2 - 1, column=0, sticky="ew")
            detail_label = ctk.CTkLabel(table_frame, text=detail, font=result_font, wraplength=600, anchor="w",
                                        justify="left")
            detail_label.grid(row=i * 2 - 1, column=1, sticky="ew")
            # Add blank labels as spacers between rows.
            spacer_label_1 = ctk.CTkLabel(table_frame, text="", font=result_font)
            spacer_label_1.grid(row=i * 2, column=0, sticky="ew")
            spacer_label_2 = ctk.CTkLabel(table_frame, text="", font=result_font)
            spacer_label_2.grid(row=i * 2, column=1, sticky="ew")

    # Initialize variables and setup the main GUI window.
    options = {"physical_activity": ctk.StringVar(), "diet": ctk.StringVar(), "environment": ctk.StringVar(), "behavior": ctk.StringVar()}

    root = ctk.CTk()
    root.title("DAP - Regression Analysis of diseases ")
    root.geometry("650x450")
    root.iconbitmap('dap.ico')

    # Configure grid layout for the main window.
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(8, weight=1)

    # Setup the main label and dropdown menu for disease selection.
    label_1 = ctk.CTkLabel(root, text="Get suggestions on how to reduce the effects of a disease based on selected variables", anchor="center", font=("Arial", 14, "bold"))
    label_1.grid(row=1, column=1, pady=10, padx=10, sticky="new")

    frame_1 = ctk.CTkFrame(root)
    frame_1.grid(row=3, column=1, pady=10, padx=10, sticky="ew")
    frame_1.grid_columnconfigure(1, weight=1)

    user_choice_1_label = ctk.CTkLabel(frame_1, text="Select the Name of Disease")
    user_choice_1_label.grid(row=0, column=0, padx=10, sticky="ns")
    user_choice_1_dropdown = ctk.CTkComboBox(frame_1, width=200, values=["gastrointestinal", "oral", "orthopedic", "kidney", "liver", "cardiac", "skin", "neurological", "cancer"], state="readonly")
    user_choice_1_dropdown.set("Please select an option...")
    user_choice_1_dropdown.grid(row=0, column=1, padx=10, sticky="ew")

    # Setup the frame for variable selection checkboxes.
    frame_2 = ctk.CTkFrame(root)
    frame_2.grid(row=4, column=1, pady=10, padx=10, sticky="ew")
    frame_2.grid_columnconfigure(0, weight=1)
    frame_2.grid_columnconfigure(1, weight=1)

    # Create checkboxes for each option in the 'options' dictionary.
    row = 1
    for option in options:
        ctk.CTkCheckBox(frame_2, text=option, variable=options[option], onvalue=option, offvalue="").grid(row=row, column=1, sticky="new")  # Adjust the column to 1
        row += 1

    # Center-align the "Select Variable(s)" label between the options.
    select_variables_label = ctk.CTkLabel(frame_2, text="Select Variable(s):")
    select_variables_label.grid(row=0, column=0, padx=10, columnspan=2, sticky="ew")

    # Button to trigger data calculation based on user selections.
    calculate_button = ctk.CTkButton(root, text="Get data for the desired choices", width=200, command=calculate_result)
    calculate_button.grid(row=5, column=1, pady=20, padx=10)

    # Label for displaying the loading animation text.
    loading_label = ctk.CTkLabel(root, text="", anchor="center")
    loading_label.grid(row=6, column=1, pady=10, padx=10, sticky="new")

    # Start the main GUI loop.
    root.mainloop()