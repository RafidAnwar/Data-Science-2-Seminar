import customtkinter as ctk
import subprocess
import threading

# This function launches the Cognitive Dysfunction Prediction Model for dogs.
def CSLB_SCORE_PREDICTION_ANALYSIS():
    # Variable to keep track of the result window
    result_window = None

    def submit_data():
        # Initiates the data processing in a new thread when the submit button is clicked.
        threading.Thread(target=process_data, daemon=True).start()
    def process_data():
        # Handles the data processing logic.
        try:
            data = (
                int(dog_age_ip.get()),
                float(dog_weight_ip.get()),
                # Maps user input to corresponding values.
                activity_level_map[pa_activity_level_ip.get()],
                health_conditions_map[hs_health_conditions_eye_ip.get()],
                health_conditions_map[hs_health_conditions_ear_ip.get()],
                frequency_map[cslb_pace_ip.get()],
                frequency_map[cslb_stare_ip.get()],
                frequency_map[cslb_stuck_ip.get()],
                frequency_map[cslb_recognize_ip.get()],
                frequency_map[cslb_walk_walls_ip.get()],
                frequency_map[cslb_avoid_ip.get()],
                frequency_map[cslb_find_food_ip.get()]
            )
            start_loading_animation() # Starts the loading animation.

            # Runs a subprocess to execute the prediction model script with the collected data.
            result = subprocess.run(["pythonw.exe", 'CSLB score prediction.py', *map(str, data)], capture_output=True, text=True)
            predicted_value = result.stdout.strip()
            stop_loading_animation() # Stops the loading animation.

            # Update the GUI with the result using a callback
            app.after(0, lambda: update_result_label(predicted_value))

            # Conditions are met in the prediction, show a follow-up window.
            if "There is a possibility of your dog having symptoms of cognitive dysfunction! Kindly come back after 6 months and answer some follow up questions:" in predicted_value:
                app.after(0, show_follow_up_window)

        except ValueError:
            # Error handling for incorrect follow-up data inputs.
            app.after(0, lambda: result_label.configure(text="Error: Please ensure all fields are filled correctly."))

    def start_loading_animation():
        # Function to initiate a loading animation on the GUI.
        loading_label.configure(text="Result is loading, please wait")
        animate_loading()

    def stop_loading_animation():
        # Function to stop the loading animation.
        loading_label.after_cancel(animation_id)
        loading_label.configure(text="")

    def animate_loading():
        # Initializes the loading animation steps.
        global animation_step
        animation_step = 0
        animate_loading_step()

    def animate_loading_step():
        # Recursive function to animate loading text.
        global animation_step, animation_id
        if animation_step < 4:
            loading_label.configure(text=loading_label.cget("text") + ".")
            animation_step += 1
            # Schedule the next animation step.
            animation_id = loading_label.after(500, animate_loading_step)
        else:
            # After 3 dots, reset the animation
            loading_label.configure(text="Result is loading, please wait")
            animation_step = 0
            animate_loading_step()

    def update_result_label(predicted_value):
        # Updates the result label with the prediction result.
        nonlocal result_window
        show_result_window(f" {predicted_value}", result_font=("Comic Sans MS", 15, "bold"), reference_font=("Arial", 12))

    def show_result_window(result_text, result_font, reference_font):
        # Displays the prediction result in a new window.
        nonlocal result_window
        # Close the existing result window if it's open
        if result_window is not None:
            result_window.destroy()

        result_window = ctk.CTkToplevel(app)
        result_window.title("Model predictions")
        result_window.geometry("1200x300")
        result_window.attributes('-topmost', True)
        result_window.iconbitmap('dap.ico')

        # Layout and setup for the result window.
        result_frame = ctk.CTkFrame(result_window)
        result_frame.grid(row=0, column=0, sticky="nsew")

        # Configure the result window grid
        result_window.grid_rowconfigure(0, weight=1)
        result_window.grid_columnconfigure(0, weight=1)

        # Configure the result frame grid
        result_frame.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)

        # Label to display the result with specified font
        result_label = ctk.CTkLabel(result_frame, text=result_text, font=result_font)
        result_label.grid(row=0, column=0, sticky="nsew")

        # Reference text label with specified font
        label_1 = ctk.CTkLabel(result_frame, text="Reference:", anchor="center", font=reference_font)
        label_1.grid(row=1, column=0, sticky="nsew")

        # Reference text for the result window
        reference_text = """
            The assessment tool via CSLB Score was developed and validated by Dr. Hannah Salvin:
            Hannah E. Salvin, Paul D. McGreevy, Perminder S. Sachdev, Michael J. Valenzuela,
            The canine cognitive dysfunction rating scale (CCDR): A data-driven and ecologically relevant assessment tool,
            The Veterinary Journal, Volume 188, Issue 3,2011,Pages 331-336,ISSN 1090-0233,
            https://doi.org/10.1016/j.tvjl.2010.05.014.
            """
        reference_label = ctk.CTkLabel(result_frame, text=reference_text, font=reference_font)
        reference_label.grid(row=2, column=0, sticky="nsew")


    def submit_follow_up_data(follow_up_window):
        # Function to handle follow-up data submission
        nonlocal result_window
        try:
            # Collects follow-up data.
            follow_up_data = (
                int(dog_age_ip.get()),  # Dog's age as an integer.
                float(dog_weight_ip.get()),  # Dog's weight as a float.
                activity_level_map[pa_activity_level_ip.get()],  # Dog's activity level mapped to a numerical value.
                health_conditions_map[hs_health_conditions_eye_ip.get()],  # Dog's eye health condition mapped to a numerical value.
                health_conditions_map[hs_health_conditions_ear_ip.get()],  # Dog's ear health condition mapped to a numerical value.
                frequency_map[cslb_pace_ip.get()],  # Frequency of dog pacing mapped to a numerical value.
                frequency_map[cslb_stare_ip.get()],  # Frequency of dog staring mapped to a numerical value.
                frequency_map[cslb_stuck_ip.get()],  # Frequency of dog getting stuck mapped to a numerical value.
                frequency_map[cslb_recognize_ip.get()],  # Frequency of dog's recognition failure mapped to a numerical value.
                frequency_map[cslb_walk_walls_ip.get()],  # Frequency of dog walking into walls mapped to a numerical value.
                frequency_map[cslb_avoid_ip.get()],  # Frequency of dog avoiding being petted mapped to a numerical value.
                frequency_map[cslb_find_food_ip.get()],  # Frequency of dog's difficulty in finding food mapped to a numerical value.
                # Additional fields for follow-up data (6 months later).
                frequency_6mo_map[cslb_pace_6mo_ip.get()],  # Change of dog's pace changing after 6 months to a numerical value.
                frequency_6mo_map[cslb_stare_6mo_ip.get()],  # Change of dog's staring at the door after 6 months to a numerical value.
                frequency_6mo_map[cslb_defecate_6mo_ip.get()],  # Change of dog's defecation rate after 6 months to a numerical value.
                frequency_6mo_map[cslb_food_6mo_ip.get()],  # Change of dog's finding food after 6 months to a numerical value.
                frequency_6mo_map[cslb_recognize_6mo_ip.get()],  # Change of dog's recognization cabability after 6 months to a numerical value.
                activity_6mo_map[cslb_active_6mo_ip.get()]  # Frequency of dog's active level changing after 6 months to a numerical value.
            )

            # Executes the Python script for follow-up data analysis using subprocess.
            # Passes the collected follow-up data to the script.
            result_new = subprocess.run(['pythonw.exe', 'CSLB score prediction.py', *map(str, follow_up_data)], capture_output=True, text=True)
            new_predicted_value = result_new.stdout.strip()

            # If an existing result window is open, it is closed to display new results.
            if result_window is not None:
                result_window.destroy()

            # Call the same function used for the original result
            app.after(0, lambda: update_result_label(new_predicted_value))
        except ValueError:
            # Error handling for incorrect follow-up data inputs.
            app.after(0, lambda: result_label.configure(text="Error: Please ensure all fields are filled correctly."))
    
        follow_up_window.destroy()

    
    # Function to display the follow-up window
    def show_follow_up_window():
        # Displays the follow-up window if certain conditions in the prediction result are met.
        # Contains additional input fields for follow-up data.
        follow_up_window = ctk.CTkToplevel(app)
        follow_up_window.title("6-Month Follow-Up Questions")
        follow_up_window.geometry("+300+800") # Set the position of the window on the screen.
        follow_up_window.attributes('-topmost', True)  # Ensure the window is on top of others.
        follow_up_window.iconbitmap('dap.ico')

        # Declaring global variables for the follow-up input fields to access them outside this function.
        global cslb_pace_6mo_ip, cslb_stare_6mo_ip, cslb_defecate_6mo_ip, cslb_food_6mo_ip, cslb_recognize_6mo_ip, cslb_active_6mo_ip
        # Creating Dropdown options for follow up questions
        # Each combo box corresponds to a specific behavior or condition being monitored over the past 6 months.
        # Users can select from predefined frequency levels to indicate changes in the dog's condition or behavior.
        cslb_pace_6mo_ip = ctk.CTkComboBox(follow_up_window, values=list(frequency_6mo_map.keys()), state="readonly", width=240)
        cslb_pace_6mo_ip.set("Please select an option")
        cslb_stare_6mo_ip = ctk.CTkComboBox(follow_up_window, values=list(frequency_6mo_map.keys()), state="readonly", width=240)
        cslb_stare_6mo_ip.set("Please select an option")
        cslb_defecate_6mo_ip = ctk.CTkComboBox(follow_up_window, values=list(frequency_6mo_map.keys()), state="readonly", width=240)
        cslb_defecate_6mo_ip.set("Please select an option")
        cslb_food_6mo_ip = ctk.CTkComboBox(follow_up_window, values=list(frequency_6mo_map.keys()), state="readonly", width=240)
        cslb_food_6mo_ip.set("Please select an option")
        cslb_recognize_6mo_ip = ctk.CTkComboBox(follow_up_window, values=list(frequency_6mo_map.keys()), state="readonly", width=240)
        cslb_recognize_6mo_ip.set("Please select an option")
        cslb_active_6mo_ip = ctk.CTkComboBox(follow_up_window, values=list(activity_6mo_map.keys()), state="readonly", width=240)
        cslb_active_6mo_ip.set("Please select an option")

        # Organizing follow-up fields into a list of tuples.
        # Each tuple contains the input field and its corresponding label text.
        follow_up_fields = [
            (cslb_pace_6mo_ip, "Compared with 6 months ago, whats your Dog's pacing frequency now?"),
            (cslb_stare_6mo_ip, "Compared with 6 months ago, whats your Dog's staring frequency now?"),
            (cslb_defecate_6mo_ip, "Compared with 6 months ago, how much does your dog urinate or defecate now?"),
            (cslb_food_6mo_ip, "Compared with 6 months ago, whats your dog's difficulty in finding food now?"),
            (cslb_recognize_6mo_ip, "Compared with 6 months ago, whats your Dog's recognition failure now?"),
            (cslb_active_6mo_ip, "Compared with 6 months ago, whats your Dog's activity level now?")
        ]
        # Looping through each field to create and position labels and input fields in the follow-up window.
        for i, (field, label) in enumerate(follow_up_fields):
            row = i
            ctk.CTkLabel(follow_up_window, text=label).grid(row=row, column=0, sticky='w', padx=10, pady=2)
            field.grid(row=row, column=1, pady=2, padx=10)

        # Creating and placing the submit button for the follow-up data.
        submit_follow_up_button = ctk.CTkButton(
            follow_up_window, 
            text="Submit Follow-up", 
            command=lambda: submit_follow_up_data(follow_up_window)
        )
        submit_follow_up_button.grid(row=len(follow_up_fields), column=0, columnspan=2, pady=10)
    
    app = ctk.CTk()
    app.title("DAP - Cognitive dysfunction prediction model")
    app.columnconfigure(0, weight=1)
    app.iconbitmap('dap.ico')
    
    # Maps for dropdown selections for the follow up window
    # These maps are used to convert the user's textual selection into a numeric value for analysis.
    # Maping is done according to the CSLB questionnaire pdf
    activity_level_map = {"not active": 1, "Moderately active": 2, "very active": 3}
    health_conditions_map = {"no disorder": 0, "Only congenital disorder": 1, "Only non congenital disorder": 2, "both congenital and non congenital": 3}
    frequency_map = {"never": 1, "once a month": 2, "once a week": 3, "once a day": 4, "More than once a day": 5}
    frequency_6mo_map = {"Much less": 1, "Slightly less": 2, "The same": 3, "Slightly more": 4, "Much more": 5}
    activity_6mo_map = {"Much more": 1, "Slightly more": 2, "The same": 3, "Slightly less": 4, "Much less": 5}
    
    # Initialize the initial input fields
    dog_age_ip = ctk.CTkComboBox(app, values=[str(n) for n in range(1, 19)])
    dog_weight_ip = ctk.CTkEntry(app, width=240)
    pa_activity_level_ip = ctk.CTkComboBox(app, values=list(activity_level_map.keys()))
    hs_health_conditions_eye_ip = ctk.CTkComboBox(app, values=list(health_conditions_map.keys()))
    hs_health_conditions_ear_ip = ctk.CTkComboBox(app, values=list(health_conditions_map.keys()))
    cslb_pace_ip = ctk.CTkComboBox(app, values=list(frequency_map.keys()))
    cslb_stare_ip = ctk.CTkComboBox(app, values=list(frequency_map.keys()))
    cslb_stuck_ip = ctk.CTkComboBox(app, values=list(frequency_map.keys()))
    cslb_recognize_ip = ctk.CTkComboBox(app, values=list(frequency_map.keys()))
    cslb_walk_walls_ip = ctk.CTkComboBox(app, values=list(frequency_map.keys()))
    cslb_avoid_ip = ctk.CTkComboBox(app, values=list(frequency_map.keys()))
    cslb_find_food_ip = ctk.CTkComboBox(app, values=list(frequency_map.keys()))
    
    # Layout the initial input fields for the user to answer
    input_fields = [
        (dog_age_ip, "Enter your Dog's age"),
        (dog_weight_ip, "Enter your Dog's weight in lbs"),
        (pa_activity_level_ip, "Enter your Dog's activity level over the past year"),
        (hs_health_conditions_eye_ip, "Has your dog ever been diagnosed with diseases that affect the eyes?"),
        (hs_health_conditions_ear_ip, "Has your dog ever been diagnosed with diseases that affect the ears?"),
        (cslb_pace_ip, "How often does your dog pace up and down, walk in circles and/or wander with no direction or purpose?"),
        (cslb_stare_ip, "How often does your dog stare blankly at the walls or floor?"),
        (cslb_stuck_ip, "How often does your dog get stuck behind objects and is unable to get around?"),
        (cslb_recognize_ip, "How often does your dog fail to recognize familiar people or other pets?"),
        (cslb_walk_walls_ip, "How often does your dog walk into walls or doors?:"),
        (cslb_avoid_ip, "How often does your dog walk away while, or avoid, being petted?"),
        (cslb_find_food_ip, "How often does your dog have difficulty finding food dropped on the floor?")
    ]

    # Label for text
    checkout_label = ctk.CTkLabel(app, text="Please answer the following questions to get predictions on the dogs current state of cognitive dysfunction", anchor="center", font=("Arial", 16, "bold"))
    checkout_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

    # Frame and input field for Dog's Age
    frame_dog_age = ctk.CTkFrame(app)
    frame_dog_age.grid(row=1, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_dog_age, text="Enter your Dog's age").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    dog_age_ip = ctk.CTkComboBox(frame_dog_age, values=[str(n) for n in range(1, 19)], state="readonly", width=240)
    dog_age_ip.set("Please select an option")
    dog_age_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_dog_age.columnconfigure((0, 1), weight=1)

    # Frame and input field for Dog's Weight
    frame_dog_weight = ctk.CTkFrame(app)
    frame_dog_weight.grid(row=2, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_dog_weight, text="Enter your Dog's weight in lbs").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    dog_weight_ip = ctk.CTkEntry(frame_dog_weight, width=240)
    dog_weight_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_dog_weight.columnconfigure((0, 1), weight=1)

    # Frame and input field for Dog's Activity Level
    frame_dog_activity = ctk.CTkFrame(app)
    frame_dog_activity.grid(row=3, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_dog_activity, text="Enter your Dog's activity level over the past year").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    pa_activity_level_ip = ctk.CTkComboBox(frame_dog_activity, values=list(activity_level_map.keys()), state="readonly", width=240)
    pa_activity_level_ip.set("Please select an option")
    pa_activity_level_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_dog_activity.columnconfigure((0, 1), weight=1)

    # Frame and input field for Dog's Eye Health Condition
    frame_eye_health = ctk.CTkFrame(app)
    frame_eye_health.grid(row=4, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_eye_health, text="Has your dog ever been diagnosed with diseases that affect the eyes?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    hs_health_conditions_eye_ip = ctk.CTkComboBox(frame_eye_health, values=list(health_conditions_map.keys()), state="readonly", width=240)
    hs_health_conditions_eye_ip.set("Please select an option")
    hs_health_conditions_eye_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_eye_health.columnconfigure((0, 1), weight=1)

    # Frame and input field for Dog's Ear Health Condition
    frame_ear_health = ctk.CTkFrame(app)
    frame_ear_health.grid(row=5, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_ear_health, text="Has your dog ever been diagnosed with diseases that affect the ears?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    hs_health_conditions_ear_ip = ctk.CTkComboBox(frame_ear_health, values=list(health_conditions_map.keys()), state="readonly", width=240)
    hs_health_conditions_ear_ip.set("Please select an option")
    hs_health_conditions_ear_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_ear_health.columnconfigure((0, 1), weight=1)

    # Frame for Dog's Pacing Behavior
    frame_pacing = ctk.CTkFrame(app, width=100, height=500)
    frame_pacing.grid(row=6, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_pacing, text="How often does your dog pace up and down, walk in circles and/or wander with no direction or purpose?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    cslb_pace_ip = ctk.CTkComboBox(frame_pacing, values=list(frequency_map.keys()), state="readonly", width=240)
    cslb_pace_ip.set("Please select an option")
    cslb_pace_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_pacing.columnconfigure((0, 1), weight=1)

    # Frame for Dog's Staring Behavior
    frame_staring = ctk.CTkFrame(app)
    frame_staring.grid(row=7, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_staring, text="How often does your dog stare blankly at the walls or floor?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    cslb_stare_ip = ctk.CTkComboBox(frame_staring, values=list(frequency_map.keys()), state="readonly", width=240)
    cslb_stare_ip.set("Please select an option")
    cslb_stare_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_staring.columnconfigure((0, 1), weight=1)

    # Frame for Dog Getting Stuck
    frame_stuck = ctk.CTkFrame(app)
    frame_stuck.grid(row=8, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_stuck, text="How often does your dog get stuck behind objects and is unable to get around?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    cslb_stuck_ip = ctk.CTkComboBox(frame_stuck, values=list(frequency_map.keys()), state="readonly", width=240)
    cslb_stuck_ip.set("Please select an option")
    cslb_stuck_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_stuck.columnconfigure((0, 1), weight=1)

    # Frame for Dog's Recognition Failure
    frame_recognition = ctk.CTkFrame(app)
    frame_recognition.grid(row=9, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_recognition, text="How often does your dog fail to recognize familiar people or other pets?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    cslb_recognize_ip = ctk.CTkComboBox(frame_recognition, values=list(frequency_map.keys()), state="readonly", width=240)
    cslb_recognize_ip.set("Please select an option")
    cslb_recognize_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_recognition.columnconfigure((0, 1), weight=1)

    # Frame for Dog Walking into Walls
    frame_walk_walls = ctk.CTkFrame(app)
    frame_walk_walls.grid(row=10, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_walk_walls, text="How often does your dog walk into walls or doors?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    cslb_walk_walls_ip = ctk.CTkComboBox(frame_walk_walls, values=list(frequency_map.keys()), state="readonly", width=240)
    cslb_walk_walls_ip.set("Please select an option")
    cslb_walk_walls_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_walk_walls.columnconfigure((0, 1), weight=1)

    # Frame for Dog Avoiding Being Petted
    frame_avoid = ctk.CTkFrame(app)
    frame_avoid.grid(row=11, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_avoid, text="How often does your dog walk away while, or avoid, being petted?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    cslb_avoid_ip = ctk.CTkComboBox(frame_avoid, values=list(frequency_map.keys()), state="readonly", width=240)
    cslb_avoid_ip.set("Please select an option")
    cslb_avoid_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_avoid.columnconfigure((0, 1), weight=1)

    # Frame for Dog's Difficulty Finding Food
    frame_find_food = ctk.CTkFrame(app)
    frame_find_food.grid(row=12, column=0, columnspan=2, padx=10, pady=2, sticky="ew")
    ctk.CTkLabel(frame_find_food, text="How often does your dog have difficulty finding food dropped on the floor?").grid(row=0, column=0, sticky="w", padx=10, pady=2)
    cslb_find_food_ip = ctk.CTkComboBox(frame_find_food, values=list(frequency_map.keys()), state="readonly", width=240)
    cslb_find_food_ip.set("Please select an option")
    cslb_find_food_ip.grid(row=0, column=1, sticky="e", pady=2, padx=10)
    frame_find_food.columnconfigure((0, 1), weight=1)

    # submit button and result label
    submit_button = ctk.CTkButton(app, text="Submit", command=submit_data)
    submit_button.grid(row=13, column=0, columnspan=2, pady=10) 

    result_label = ctk.CTkLabel(app, text="", font=("Arial", 20, "bold"))
    result_label.grid(row=14, column=0, columnspan=2)

    loading_label = ctk.CTkLabel(app, text="", anchor="center")
    loading_label.grid(row=14, column=0, columnspan=2)

    # Start the main GUI loop.
    app.mainloop()