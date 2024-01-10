import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error , r2_score
from sklearn.model_selection import train_test_split, cross_val_score
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
       ['cslb_score']]
merged = pd.merge(data, cslb, on='dog_id', how='inner', copy=False)
final = merged.reset_index().drop_duplicates(subset='dog_id',
                                             keep='first').set_index('dog_id')
###Linear regression analysis

Y = final['cslb_score']
X = final[['dd_age_years', 'dd_sex', 'dd_weight_lbs', 'dd_breed_pure_or_mixed']]

###Splitting data 80:20

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, Y_train)

# Predicting the Test and Train set result
Y_pred = model.predict(X_test)
model_diff = pd.DataFrame({'Actual value': Y_test, 'Predicted value': Y_pred})

mse = mean_squared_error(Y_test, Y_pred)
mae = mean_absolute_error(Y_test, Y_pred)
r2 = r2_score(Y_test, Y_pred)

print("Mean Squared Error:", mse)
print("Mean absolute Error:", mae)
print("R-squared:", r2)
print(model_diff)

###Taking usr inputs for CSLB score prediction
dog_sex_ip = int(input("Select 1 for male and 2 for Female: "))
dog_age_ip = int(input("Enter your Dog's age: "))
dog_breed_pure_or_mixed_ip = int(input("Enter your Dog's breed: "))
dog_weight_ip = int(input("Enter your Dog's weight: "))

input_dict = {
    'dog_id': 1,
    'dd_age_years': dog_age_ip,
    'dd_sex': dog_sex_ip,
    'dd_weight_lbs': dog_weight_ip,
    'dd_breed_pure_or_mixed': dog_breed_pure_or_mixed_ip,

}
# Wrap scalar values in lists to create columns
for key in input_dict:
    input_dict[key] = [input_dict[key]]

input_df = df = pd.DataFrame(input_dict)
input_df = input_df.set_index('dog_id')
predicted_value = model.predict(input_df)
print(f'Predicted CSLB Score = ', predicted_value[0])