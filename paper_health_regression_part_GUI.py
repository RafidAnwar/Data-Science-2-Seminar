import customtkinter as ctk
import subprocess
import threading

def PAPER_HEALTH_REGRESSION_PART():
    def calculate_result():
        start_loading_animation()

        def run_calculation():
            user_choice_1 = user_choice_1_dropdown.get()
            user_choice_2 = user_choice_2_dropdown.get()

            result = subprocess.run(['python', 'paper_health_regression_part.py', user_choice_1, user_choice_2], capture_output=True, text=True, encoding='utf-8')
            display_result(result.stdout.strip(), user_choice_2)
            stop_loading_animation()

            loading_label.configure(text="")

        threading.Thread(target=run_calculation).start()

    def start_loading_animation():
        loading_label.configure(text="Result is loading, please wait")
        animate_loading()

    def stop_loading_animation():
        loading_label.after_cancel(animation_id)
        loading_label.configure(text="")

    def animate_loading():
        global animation_step
        animation_step = 0
        animate_loading_step()

    def animate_loading_step():
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

    def display_result(result_text, choice):
        result_window = ctk.CTkToplevel(root)
        result_window.title(f"Regression Analysis Result - {choice}")
        result_window.geometry("650x450")
        result_window.attributes('-topmost', True)
        result_window.iconbitmap('dap.ico')

        scrollbar = ctk.CTkScrollbar(result_window)
        scrollbar.pack(side="right", fill="y")

        result_text_widget = ctk.CTkTextbox(result_window, height=15, yscrollcommand=scrollbar.set)
        result_text_widget.pack(pady=20, padx=10, fill="both", expand=True)

        result_text_widget.tag_config("center", justify='center')
        result_text_widget.insert("1.0", result_text)
        result_text_widget.tag_add("center", "1.0", "end")

        result_text_widget.configure(state="disabled")
        scrollbar.configure(command=result_text_widget.yview)

    root = ctk.CTk()
    root.title("DAP - Regression Analysis of diseases ")
    root.geometry("750x450")
    root.iconbitmap('dap.ico')

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(2, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(8, weight=1)

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

    frame_2 = ctk.CTkFrame(root)
    frame_2.grid(row=4, column=1, pady=10, padx=10, sticky="ew")
    frame_2.grid_columnconfigure(1, weight=1)

    user_choice_2_label = ctk.CTkLabel(frame_2, text="Select variable")
    user_choice_2_label.grid(row=0, column=0, padx=10, sticky="ns")
    user_choice_2_dropdown = ctk.CTkComboBox(frame_2, width=200, values=["physical_activity", "diet", "environment", "behavior"], state="readonly")
    user_choice_2_dropdown.set("Please select an option...")
    user_choice_2_dropdown.grid(row=0, column=1, padx=10, sticky="ew")

    calculate_button = ctk.CTkButton(root, text="Get data for the desired choices", width=200, command=calculate_result)
    calculate_button.grid(row=5, column=1, pady=20, padx=10)

    loading_label = ctk.CTkLabel(root, text="", anchor="center")
    loading_label.grid(row=6, column=1, pady=10, padx=10, sticky="new")

    root.mainloop()