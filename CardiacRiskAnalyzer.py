import tkinter as tk # Importing library for GUI
from tkinter import messagebox # For GUI

dataset = [
    # LOW RISK GROUP
    {"name": "P1-A", "age": 25, "chol": 180, "risk": "No"},
    {"name": "P1-B", "age": 35, "chol": 200, "risk": "No"},
    {"name": "P1-C", "age": 40, "chol": 185, "risk": "No"},
    {"name": "P1-D", "age": 30, "chol": 190, "risk": "No"},
    {"name": "P1-E", "age": 28, "chol": 175, "risk": "No"},
    {"name": "P1-F", "age": 32, "chol": 205, "risk": "No"},
    {"name": "P1-G", "age": 38, "chol": 195, "risk": "No"},
    
    # HIGH RISK GROUP 
    {"name": "P2-A", "age": 45, "chol": 210, "risk": "Yes"},
    {"name": "P2-B", "age": 50, "chol": 230, "risk": "Yes"},
    {"name": "P2-C", "age": 60, "chol": 250, "risk": "Yes"},
    {"name": "P2-D", "age": 55, "chol": 240, "risk": "Yes"},
    {"name": "P2-E", "age": 62, "chol": 260, "risk": "Yes"},
    {"name": "P2-F", "age": 48, "chol": 225, "risk": "Yes"},
    
    # EDGE CASES
    {"name": "P3-A", "age": 42, "chol": 208, "risk": "No"},
    {"name": "P3-B", "age": 44, "chol": 215, "risk": "Yes"},
    {"name": "P3-C", "age": 37, "chol": 220, "risk": "Yes"}, 
    {"name": "P3-D", "age": 52, "chol": 205, "risk": "No"},  
]

# RECURSION:
def power(base, exp):
    # recursion used for squaring differences (ahead in code)
    if exp == 0:
        return 1
    else:
        return base * power(base, exp - 1)
    
# Calculating max and min for both age and chol
def calculate_min_max_ranges(data):

    # assigning the variables value of the very first patient to compare
    min_age = data[0]["age"]
    max_age = data[0]["age"]
    min_chol = data[0]["chol"]
    max_chol = data[0]["chol"]

    for patient in data:
        age = patient["age"]
        chol = patient["chol"]

        # finding max age value and min age value
        if age < min_age:
            min_age = age
        if age > max_age:
            max_age = age
        
        # finding min chol value and max chol value
        if chol < min_chol:
            min_chol = chol
        if chol > max_chol:
            max_chol = chol

    return min_age, max_age, min_chol, max_chol

# EUCLIDEAN DISTANCE:
def FindEuclideanDistance(row1, row2):
    
    # Getting Euclidean Distance
    min_age, max_age, min_chol, max_chol = calculate_min_max_ranges(dataset)
    age_range = max_age - min_age
    chol_range = max_chol - min_chol

    # Calculating the diff in age and chol and dividing by range of ages/chols to NORMALIZE data 
    diff_age = (row1["age"] - row2["age"])/age_range
    diff_chol = (row1["chol"] - row2["chol"]) / chol_range

    age_sq = power(diff_age, 2)
    chol_sq = power(diff_chol, 2)
    # Formula: Sqrt( (x2-x1)^2 + (y2-y1)^2 )
    distance = (age_sq + chol_sq) ** 0.5
    return distance

# BUBBLE SORT:
def bubble_sort_neighbors(distances):
    # Sorts the list of neighbors by distance (ascending way) using Bubble Sort
    n = len(distances)
    for i in range(n):
        # The inner loop compares adjacent elements and swaps them
        for j in range(0, n - i - 1): 
            if distances[j][0] > distances[j + 1][0]:
                distances[j], distances[j + 1] = distances[j + 1], distances[j]
    return distances

# MAIN CORE LOGIC FUNCTION:
def predict_risk(user_age, user_chol, k=5):
    user_data = {"age": user_age, "chol": user_chol}
    all_distances = []

    print(f"\nCalculations for Age:{user_age}, Chol:{user_chol}, Nearest neighbors:{k}")
    
    # Calculate distance and weight to every patient in the dataset
    for patient in dataset:
        dist = FindEuclideanDistance(patient, user_data)
        
        # Calculate Weighted score
        if dist == 0:
            weight = float('inf') 
        else:
            weight = 1 / power(dist, 2) 

        all_distances.append([
            dist,
            patient["risk"],
            patient["name"],
            patient["age"],
            patient["chol"],
            weight
        ])

        print(f"Distance to {patient['name']} (Age={patient['age']}, Chol={patient['chol']}) is {dist:.2f} (Weight: {weight:.2f})")

    # Sort all patients by distance
    sorted_neighbors = bubble_sort_neighbors(all_distances) 
    print("\nAll sorted distances:")

    for dist, risk, name, age, p_chol, weight in sorted_neighbors:
        print(f" {name}: Distance={dist:.2f}, Risk={risk}, Weight={weight:.2f}")

    # K-Nearest Neighbors
    nearest_neighbors = sorted_neighbors[:k]
    print(f"\nK={k} Nearest Neighbors (Selected for Voting):")

    for dist, risk, name, p_age, p_chol, weight in nearest_neighbors:
        print(f" >>{name}: Distance={dist:.2f}, Risk={risk}, Weight={weight:.2f}")
    
    # weighted voting logic
    yes_score = 0.0
    no_score = 0.0

    for neighbor in nearest_neighbors:
        label = neighbor[1] 
        weight = neighbor[5] 
        
        if label == "Yes":
            yes_score += weight
        else:
            no_score += weight

    # Getting final prediction
    if yes_score > no_score:
        result_text = "HIGH RISK (Predicted: Heart Disease)"
    elif no_score > yes_score:
        result_text = "LOW RISK (Predicted: No Heart Disease)"
    else:
        # no_score = yes_score return to low.
        result_text = "LOW RISK (Predicted: No Heart Disease)"

    print(f"\nFinal result: Yes Score: {yes_score:.2f}, No Score: {no_score:.2f}")
    print(f"Prediction: {result_text}")
    return result_text

def on_predict_click():
    # Get the raw string input
    age_raw = age_entry.get().strip() # .strip() removes accidental spaces
    chol_raw = chol_entry.get().strip()

    # Check for empty fields
    if not age_raw or not chol_raw:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    try:
        age_val = int(age_raw)
        chol_val = int(chol_raw)

        # Range Validations
        if age_val > 100 or age_val < 19:
            messagebox.showwarning("Invalid Age", "Age must be between 19 and 100.")
            return

        if chol_val < 100 or chol_val > 400:
            messagebox.showwarning("Invalid Cholesterol Level", "Cholesterol Level must be between 100 and 400.")
            return 

        # Run Prediction
        result = predict_risk(age_val, chol_val)
        
        # Color for result based on prediction
        if "HIGH RISK" in result:
            result_color = "red"
        else:
            result_color = "green"
            
        label_result.config(text=f"Prediction: {result}", fg=result_color)
        
    except ValueError:
        # This catches cases where input is not empty but contains letters/symbols
        messagebox.showerror("Input Error", "Please enter valid numbers only.")

# GUI Logic
root = tk.Tk()
root.title("Cardiac Risk Analyzer (KNN)")
root.geometry("500x450") 
root.configure(bg="#f0f0f0") 

# TITLE
heading = tk.Label(root, text="❤️ Cardiac Risk Analyzer", 
                   font=("Segoe UI", 20, "bold"), 
                   fg="#333333", bg="#f0f0f0")
heading.pack(pady=(30, 20))

# FRAMES
frame_inputs = tk.Frame(root, bg="#ffffff", padx=20, pady=20, bd=1, relief=tk.RAISED)
frame_inputs.pack(pady=10)

# Taking age input
tklabelage = tk.Label(frame_inputs, text="Patient Age:", font=("Segoe UI", 12), bg="#ffffff", fg="#555555")
tklabelage.grid(row=0, column=0, padx=10, pady=10, sticky="w")
age_entry = tk.Entry(frame_inputs, font=("Consolas", 14), width=10, bd=2, relief=tk.SUNKEN)
age_entry.grid(row=0, column=1, padx=10, pady=10)

# Taking cholesterol input
tklabelchol = tk.Label(frame_inputs, text="Cholesterol Level (mg/dL):", font=("Segoe UI", 12), bg="#ffffff", fg="#555555")
tklabelchol.grid(row=1, column=0, padx=10, pady=10, sticky="w") 
chol_entry = tk.Entry(frame_inputs, font=("Consolas", 14), width=10, bd=2, relief=tk.SUNKEN)
chol_entry.grid(row=1, column=1, padx=10, pady=10)

# Buttons
btn_predict = tk.Button(root, text="🔬 Analyze Risk", 
                        font=("Segoe UI", 14, "bold"), 
                        bg="#4CAF50", fg="white", 
                        activebackground="#66BB6A", activeforeground="white",
                        relief=tk.RAISED, bd=3,
                        command=on_predict_click)
btn_predict.pack(pady=30, ipadx=10, ipady=5)

# Labels
label_result = tk.Label(root, text="Prediction: ...", 
                         font=("Segoe UI", 16, "bold"), 
                         fg="#333333", bg="#f0f0f0",
                         wraplength=400)
label_result.pack(pady=10)
label_result.pack(pady=10)

hint = tk.Label(root, text="(Detailed KNN steps are printed on the console)", 
                font=("Segoe UI", 9, "italic"), 
                fg="gray", bg="#f0f0f0")
hint.pack(pady=5)

# Calling Function
root.mainloop()

"""
    What this model indicates overall:
    - At Cholestrol_level <= 100, at all ages there is low risk of heart disease.
    - As a person ages, even if the cholestrol level remains same, the heart disease risk increases.
    - As Cholestrol level increases, even at the same age, the heart disease risk increases.
"""