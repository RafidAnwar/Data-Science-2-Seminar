import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
import warnings
import sys

# called from CSLB_score_prediction_gui.py to get results from this terminal window
def submit_data(predicted_value):
    result = ""
    return result

# ignore basic warnings in the terminal window
warnings.filterwarnings("ignore")

# dog owner csv
df = pd.read_csv('DAP_2021_HLES_dog_owner_v1.0.csv')
exp_df = df.set_index('dog_id')

"""#unwanted variables exclusion

Reason for exclusion:
1. age selected under 18 years. Above 18 years older dogs there are outliers
2. only neutered dogs are considered as almost 95% were spayed.
3. only considering breeds which have at least 10 samples in the csv
"""

clean = (exp_df["dd_age_years"] <= 18) & (exp_df['dd_spayed_or_neutered'] == True)
data = exp_df[clean]

data.replace(np.nan, 0, inplace=True)
value_counts = data['dd_breed_pure'].value_counts()

# Loop through the unique values in the 'FloatColumn' and delete rows where count is 0

for value in value_counts.index:
    if value_counts[value] < 10:
        data = data[data['dd_breed_pure'] != value]

# Adding the CSLB Variables from the dap cslb csv to the hles dog owner csv file

df2 = pd.read_csv('DAP_2021_CSLB_v1.0.csv')
cslb2 = df2.set_index('dog_id')
cslb = cslb2.loc[:,
       ["cslb_pace","cslb_stare","cslb_stuck","cslb_recognize","cslb_walk_walls","cslb_avoid","cslb_find_food","cslb_pace_6mo","cslb_stare_6mo","cslb_defecate_6mo","cslb_food_6mo","cslb_recognize_6mo","cslb_active_6mo",'cslb_score']]
merged = pd.merge(data, cslb, on='dog_id', how='inner', copy=False)
final = merged.reset_index().drop_duplicates(subset='dog_id',
                                             keep='first').set_index('dog_id')
# Linear regression analysis

Y = final['cslb_score']
X = final[['dd_age_years', 'dd_weight_lbs', 'pa_activity_level', 'hs_health_conditions_eye','hs_health_conditions_ear', 'cslb_pace',"cslb_stare","cslb_stuck","cslb_recognize","cslb_walk_walls","cslb_avoid","cslb_find_food"]]

# Splitting data 80:20

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, Y_train)

# Assigning the command line arguments from frontend gui to variables
dog_age_ip = int(sys.argv[1])
dog_weight_ip = float(sys.argv[2])
pa_activity_level_ip = int(sys.argv[3])
hs_health_conditions_eye_ip = int(sys.argv[4])
hs_health_conditions_ear_ip = int(sys.argv[5])
cslb_pace_ip = int(sys.argv[6])
cslb_stare_ip = int(sys.argv[7])
cslb_stuck_ip = int(sys.argv[8])
cslb_recognize_ip = int(sys.argv[9])
cslb_walk_walls_ip = int(sys.argv[10])
cslb_avoid_ip = int(sys.argv[11])
cslb_find_food_ip = int(sys.argv[12])

# create a input dictionary based on the data input from user in the gui

input_dict = {
    'dog_id': 1,
    'dd_age_years': dog_age_ip,
    'dd_weight_lbs': dog_weight_ip,
    'pa_activity_level': pa_activity_level_ip,
    'hs_health_conditions_eye': hs_health_conditions_eye_ip,
    'hs_health_conditions_ear': hs_health_conditions_ear_ip,
    'cslb_pace': cslb_pace_ip ,
    'cslb_stare':cslb_stare_ip,
    'cslb_stuck': cslb_stuck_ip,
    'cslb_recognize': cslb_recognize_ip,
    'cslb_walk_walls': cslb_walk_walls_ip,
    'cslb_avoid': cslb_avoid_ip,
    'cslb_find_food': cslb_find_food_ip,
}
# Wrap scalar values in lists to create columns
for key in input_dict:
    input_dict[key] = [input_dict[key]]
input_df = df = pd.DataFrame(input_dict)
input_df = input_df.set_index('dog_id')
predicted_value = model.predict(input_df)
print(f'Predicted CSLB Score = ', predicted_value[0])

# Taking decision based on the cslb score
if predicted_value[0] < 40:
  print('\nYour dog is safe! No signs of cognitive dysfunction!')
elif predicted_value[0] >=40 and predicted_value[0] <=60:
  print(f'\nThere is a possibility of your dog having symptoms of cognitive dysfunction! Kindly come back after 6 months and answer some follow up questions:\n')

# Assign the data of Follow up questions after 6 months from the gui to variables

  cslb_pace_6mo_ip = int(sys.argv[13])
  cslb_stare_6mo_ip = int(sys.argv[14])
  cslb_defecate_6mo_ip = int(sys.argv[15])
  cslb_food_6mo_ip = int(sys.argv[16])
  cslb_recognize_6mo_ip = int(sys.argv[17])
  cslb_active_6mo_ip = int(sys.argv[18])

# Calculate the actual CSLB score based on DR. Hannah assessment tool
  cslb_score = cslb_pace_ip + cslb_stare_ip + cslb_stuck_ip + cslb_recognize_ip + cslb_walk_walls_ip + cslb_avoid_ip + cslb_find_food_ip + cslb_pace_6mo_ip + cslb_stare_6mo_ip + cslb_defecate_6mo_ip + 2 * cslb_food_6mo_ip + 3 * cslb_recognize_6mo_ip + cslb_active_6mo_ip
  predicted_value = cslb_score

# show the final cognitive dysfunction result
  if predicted_value <50:
    print("\n NEW UPDATE : \nNo need to worry! Your dog's actual CSLB score is =",predicted_value," your dog has no signs of cognitive dysfunction!")
  else:
    print(f"\n NEW UPDATE : \nYour dog's actual CSLB score is =",predicted_value, "He/she has symptoms of cognitive dysfunction! Kindly contact the vet as soon as possible")
else:
  print("\nYour dog has symptoms of cognitive dysfunction! Kindly contact the vet as soon as possible")
