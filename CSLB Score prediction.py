import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
import warnings

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

clean = (exp_df["dd_age_years"] < 18) & (exp_df['dd_spayed_or_neutered'] == True)
data = exp_df[clean]

# Excluding the Sample if the Value count of any breed is less than 10

data.replace(np.nan, 0, inplace=True)
value_counts = data['dd_breed_pure'].value_counts()

# Loop through the unique values in the 'FloatColumn' and delete rows where count is 0

for value in value_counts.index:
    if value_counts[value] < 10:
        data = data[data['dd_breed_pure'] != value]

"""#Adding the CSLB Variables from the dap cslb csv to the hles dog owner csv file"""

df2 = pd.read_csv('DAP_2021_CSLB_v1.0.csv')
cslb2 = df2.set_index('dog_id')
cslb = cslb2.loc[:,
       ["cslb_pace","cslb_stare","cslb_stuck","cslb_recognize","cslb_walk_walls","cslb_avoid","cslb_find_food","cslb_pace_6mo","cslb_stare_6mo","cslb_defecate_6mo","cslb_food_6mo","cslb_recognize_6mo","cslb_active_6mo",'cslb_score']]
merged = pd.merge(data, cslb, on='dog_id', how='inner', copy=False)
final = merged.reset_index().drop_duplicates(subset='dog_id',
                                             keep='first').set_index('dog_id')
###Linear regression analysis

Y = final['cslb_score']
X = final[['dd_age_years', 'dd_weight_lbs', 'pa_activity_level', 'hs_health_conditions_eye','hs_health_conditions_ear', 'cslb_pace',"cslb_stare","cslb_stuck","cslb_recognize","cslb_walk_walls","cslb_avoid","cslb_find_food"]]

###Splitting data 80:20

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, Y_train)

# Predicting the Test and Train set result
Y_pred = model.predict(X_test)
model_diff = pd.DataFrame({'Actual value': Y_test, 'Predicted value': Y_pred})

mape = mean_absolute_percentage_error(Y_test, Y_pred)

print("Mean absolute percentage Error:", mape*100)
print(model_diff)

###Taking usr inputs for CSLB score prediction
while True:
    dog_age_ip = int(input("Enter your Dog's age: "))
    dog_weight_ip = int(input("Enter your Dog's weight (in lbs): "))
    pa_activity_level_ip = int(input("Enter your Dog's activity level over the past year(1 = not active >> 3 = very active): "))
    hs_health_conditions_eye_ip = int(input("Has your dog ever been diagnosed with diseases that affect the eyes? (0=no disorder >> 3=both congenital and non congenital): "))
    hs_health_conditions_ear_ip = int(input("Has your dog ever been diagnosed with diseases that affect the ears? (0=no disorder >> 3=both congenital and non congenital): "))
    cslb_pace_ip = int(input("How often does your dog pace up and down, walk in circles and/or wander with no direction or purpose? (1=never>>5=More than once a day):"))
    cslb_stare_ip =int(input("How often does your dog stare blankly at the walls or floor?(1=never>>5=More than once a day): "))
    cslb_stuck_ip = int(input('How often does your dog get stuck behind objects and is unable to get around?(1=never>>5=More than once a day):'))
    cslb_recognize_ip = int(input('How often does your dog fail to recognize familiar people or other pets?(1=never>>5=More than once a day):'))
    cslb_walk_walls_ip = int(input('How often does your dog walk into walls or doors?(1=never>>5=More than once a day):'))
    cslb_avoid_ip = int(input('How often does your dog walk away while, or avoid, being petted?(1=never>>5=More than once a day):'))
    cslb_find_food_ip =int(input('How often does your dog have difficulty finding food dropped on the floor?(1=never>>5=always):'))

    input_dict = {
        'dog_id': 1,
        'dd_age_years': dog_age_ip,
        'dd_weight_lbs': dog_weight_ip,
        'pa_activity_level': pa_activity_level_ip,
        'hs_health_conditions_eye': hs_health_conditions_eye_ip,
        'hs_health_conditions_ear': hs_health_conditions_ear_ip,
        'cslb_pace' : cslb_pace_ip ,
        'cslb_stare' :cslb_stare_ip,
        'cslb_stuck' : cslb_stuck_ip,
        'cslb_recognize' : cslb_recognize_ip,
        'cslb_walk_walls' : cslb_walk_walls_ip,
        'cslb_avoid' : cslb_avoid_ip,
        'cslb_find_food' : cslb_find_food_ip,
    }
    # Wrap scalar values in lists to create columns
    for key in input_dict:
        input_dict[key] = [input_dict[key]]

    input_df = df = pd.DataFrame(input_dict)
    input_df = input_df.set_index('dog_id')
    predicted_value = model.predict(input_df)
    print(f'Predicted CSLB Score = ', predicted_value[0])

    ###Taking decision based on the cslb score

    if predicted_value[0] < 40:
      print('Your dog is safe! No signs of cognitive dysfunction!')
    elif predicted_value[0] >=40 and predicted_value[0] <=60:
      print(f'There is a possibility of your dog having symptomps of cognitive dysfunction! Kindly come back after 6 months and answer these follow up questions:\n')
      cslb_pace_6mo_ip = int(input('Compared with 6 months ago, how much does your dog now pace up and down, walk in circles and/or wander with no direction or purpose? ='))
      cslb_stare_6mo_ip = int(input('Compared with 6 months ago, how much does your dog now stare blankly at the walls or floor?='))
      cslb_defecate_6mo_ip = int(input('Compared with 6 months ago, how much does your dog urinate or defecate in an area it has previously kept clean?='))
      cslb_food_6mo_ip = int(input('Compared with 6 months ago, how much does your dog have difficulty finding food dropped on the floor?='))
      cslb_recognize_6mo_ip =int(input( 'Compared with 6 months ago, how much does your dog fail to recognize familiar people or other pets?='))
      cslb_active_6mo_ip = int(input('Compared with 6 months ago, how much time does your dog spend active?='))
      cslb_score = cslb_pace_ip + cslb_stare_ip + cslb_stuck_ip + cslb_recognize_ip + cslb_walk_walls_ip + cslb_avoid_ip + cslb_find_food_ip + cslb_pace_6mo_ip + cslb_stare_6mo_ip + cslb_defecate_6mo_ip + 2 * cslb_food_6mo_ip + 3 * cslb_recognize_6mo_ip + cslb_active_6mo_ip
      if cslb_score <50:
        print("No need to worry! your dog has no signs of cognitive dysfunction!")
      else:
        print(f"Your dog's CSLB score is =",cslb_score, "He/she has symptoms of cognitive dysfunction! Kindly contact the vet as soon as possible")
    else:
      print("Your dog has symptoms of cognitive dysfunction! Kindly contact the vet as soon as possible")

    user_input = input("Do you want to stop? (yes/no): ")

    if user_input.lower() == "yes":
        break