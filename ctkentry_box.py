import tkinter as tk
import ttkbootstrap as ttbk
from tkinter import ttk, messagebox
import subprocess

from tkinter import scrolledtext
def calculate_result():
    user_choice_1 = user_choice_1_var.get()
    user_choice_2 = user_choice_2_var.get()

    # Use subprocess.run() to capture the output of paper_health_regression_part.py
    result = subprocess.run(['python', 'paper_health_regression_part.py', user_choice_1, user_choice_2], capture_output=True, text=True, encoding='utf-8')

    result_text = f"{result.stdout.strip()}"
    result_window = tk.Toplevel(root)
    result_window.title("Health Regression Analysis Result")
    result_window.iconbitmap('icon.ico')
    # Create a scrolled text widget
    text_widget = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, width=130, height=40)
    text_widget.insert(tk.END, result_text)
    # Configure a custom font
    font = ("Arial", 12)
    text_widget.tag_configure("custom_font", font=font)

    # Apply the custom font to the entire text
    text_widget.tag_add("custom_font", 1.0, tk.END)
    text_widget.pack(expand=True, fill="both")

# Create main tkinter window
root = tk.Tk()
root.title("Dog Aging Project")
root.iconbitmap('icon.ico')
root.geometry("400x400")
style = ttbk.Style(theme="darkly")


# Add lebel
label_1 = tk.Label(root, text="Dog Aging Project")
label_1.pack(pady=10)
label_2 = tk.Label(root, text="Analytic Avengers")
label_2.pack()

# Create and set options for user_choice_1 dropdown
user_choice_1_var = tk.StringVar(value='Please select an option...')
user_choice_1_label = tk.Label(root, text="Select the Name of Disease")
user_choice_1_label.pack(pady=15)
user_choice_1_dropdown = ttk.Combobox(root, state="readonly", textvariable=user_choice_1_var, values=[
    "gastrointestinal", "oral", "orthopedic", "kidney", "liver", "cardiac", "skin", "neurological", "cancer"
])
user_choice_1_dropdown.pack()

# Create and set options for user_choice_2 dropdown
user_choice_2_var = tk.StringVar(value='Please select an option...')
user_choice_2_label = tk.Label(root, text="Select variable")
user_choice_2_label.pack(pady=15)
user_choice_2_dropdown = ttk.Combobox(root, state="readonly", textvariable=user_choice_2_var, values=["physical_activity", "diet", "environment", "behavior"])
user_choice_2_dropdown.pack()

# Button to calculate and display result
calculate_button = tk.Button(root, text="Get data for the desired choices", command=calculate_result)
calculate_button.pack(pady=25)

# Run the main tkinter loop
root.mainloop()


