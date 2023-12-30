import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import statsmodels.api as sm

# dog owner csv
df = pd.read_csv('DAP_2021_HLES_dog_owner_v1.0.csv')


df = pd.read_csv('DAP_2021_HLES_dog_owner_v1.0.csv')

exp_df = df.set_index('dog_id')


"""#unwanted variables exclusion

Reason for exclusion:
1. age selected between 1 to 18. As below 1 year, puppies do not have fixed feeding frequency compared to adults and 
   above 18 years older dogs there are outliers
2. only neutered dogs are considered as almost 95% were spayed.
"""

clean = (exp_df["dd_age_years"] >= 1) & (exp_df["dd_age_years"] < 18) & (exp_df['dd_spayed_or_neutered'] == True)
data = exp_df[clean]

# print(data.head())

# print(data.shape)

# Excluding the Sample if the Value count of any breed is less than 10

data.replace(np.nan, 0, inplace=True)

value_counts = data['dd_breed_pure'].value_counts()

# Loop through the unique values in the 'FloatColumn' and delete rows where count is 0
for value in value_counts.index:
    if value_counts[value] < 10:
        data = data[data['dd_breed_pure'] != value]

disease_column = ['hs_health_conditions_gastrointestinal', 'hs_health_conditions_oral',
                  'hs_health_conditions_orthopedic', 'hs_health_conditions_kidney', 'hs_health_conditions_liver',
                  'hs_health_conditions_cardiac', 'hs_health_conditions_skin', 'hs_health_conditions_neurological',
                  'hs_health_conditions_cancer']

"""#Regression analysis
1. All disease

Cleaning the data:
1. hs_health_conditions_x = 1 and 3 is excluded as they are congenital diseases and we only want to work 
   with disease which are not congenital
"""
#Diet Variable List

an_diet = ['df_diet_consistency','df_appetite', 'df_primary_diet_component_organic','df_primary_diet_component_grain_free',    
           'df_primary_diet_component_change_recent', 'df_weight_change_last_year', 'df_treats_frequency', 'df_infrequent_supplements']



def disease_func_diet(user_choice):
  clean = (data[user_choice] != 1) & (data[user_choice] != 3)
  disease= data[clean]
  disease[user_choice] = disease[user_choice].map(lambda x: 0 if x == 0 else 1) #converting the disease data to binary 0 and 1, 0= not affected and 1= affected

  for variable in an_diet:
    if variable == 'df_diet_consistency':
      disease[variable] = disease[variable].map(lambda x: 0 if x >= 3 else 1) # 1 for very consistent, 0 for Non Consitent diet
      
    elif variable == 'df_appetite':
      disease[variable] = disease[variable].map(lambda x: 0 if x == 1  else 1) # 0 for poor appetite and 1 for good appetite
      
    elif variable == 'df_primary_diet_component_organic':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 indicates false to the organic diet and 1 for True Organic Diet
      
    elif variable == 'df_primary_diet_component_grain_free':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 indicates false to the grainfree diet and 1 for True Grainfree Diet
      
    elif variable == 'df_primary_diet_component_change_recent':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 for No and 1 for yes
      
    elif variable == 'df_weight_change_last_year':
      disease[variable] = disease[variable].map(lambda x: 0 if x == 0  else 1) # 0 incdicates no change in weight in last year and 1 stand for change in weight in last year
      
    elif variable == 'df_treats_frequency':
      disease[variable] = disease[variable].map(lambda x: 0 if x ==1 or x==4  else 1) # 0 indicates for poor treat frequency to the dogs and 1 stand for moderate treat frequency
      
    elif variable == 'df_infrequent_supplements':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1)

    import statsmodels.api as sm

    array1 = disease[variable].values
    array2 = disease[user_choice].values

    data_reg = pd.DataFrame({
      'exposure_group': array1,
      'outcome': array2
    })

    # Create a contingency table
    contingency_table = pd.crosstab(data_reg['exposure_group'], data_reg['outcome'])
    
    # Perform logistic regression
    exog = sm.add_constant(data_reg['exposure_group'])
    logit_model = sm.Logit(data_reg['outcome'], exog)
    result = logit_model.fit()

    # Get odds ratio and confidence interval
    odds_ratio = np.exp(result.params[1])
    conf_interval = np.exp(result.conf_int().iloc[1])

    # Print the results
    print(f'Odds Ratio for {user_choice} w.r.t {variable}: {odds_ratio:.4f}')
    print(f'Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}]')
    print(f'p-value:', result.pvalues.loc['exposure_group'])
    
#def disease_funtion Physical activities

variable_column_pa = ['pa_activity_level', 'pa_avg_activity_intensity', 'pa_swim', 'pa_physical_games_frequency',
                      'pa_moderate_weather_sun_exposure_level', 'pa_on_leash_walk_frequency',
                      'pa_other_aerobic_activity_frequency']

def disease_func_pa(user_choice):
  clean = (data[user_choice] != 1) & (data[user_choice] != 3)
  disease= data[clean]
  disease[user_choice] = disease[user_choice].map(lambda x: 0 if x == 0 else 1) #converting the disease data to binary 0 and 1, 0= not affected and 1= affected

  for row in variable_column_pa:
    if row == 'pa_swim':
      disease[row] = disease[row].map(lambda x: 1 if x == True else 0)
      
    elif row == 'pa_physical_games_frequency':
      disease[row] = disease[row].map(lambda x: 1 if x <= 3 else 0)
      
    elif row == 'pa_moderate_weather_sun_exposure_level':
      disease[row] = disease[row].map(lambda x: 1 if x <= 2 else 0)
      
    elif row == 'pa_other_aerobic_activity_frequency' or 'pa_on_leash_walk_frequency':
      disease[row] = disease[row].map(lambda x: 1 if x >= 2 else 0)
      
    else:
      disease[row] = disease[row].map(lambda x: 0 if x == 1 else 1)

    import statsmodels.api as sm

    array1 =disease[row].values
    array2 =disease[user_choice].values

    data_reg = pd.DataFrame({
      'exposure_group': array1,
      'outcome': array2
    })

    # Create a contingency table
    contingency_table = pd.crosstab(data_reg['exposure_group'], data_reg['outcome'])
    
        # Perform logistic regression
    exog = sm.add_constant(data_reg['exposure_group'])
    logit_model = sm.Logit(data_reg['outcome'], exog)
    result = logit_model.fit()

    # Get odds ratio and confidence interval
    odds_ratio = np.exp(result.params[1])
    conf_interval = np.exp(result.conf_int().iloc[1])

    # Print the results
    print(f'Odds Ratio for {user_choice} w.r.t {row}: {odds_ratio:.4f}')
    print(f'Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}]')
    print(f'p-value:', result.pvalues.loc['exposure_group'])


while True:

  #taking user Input

  print('This is a list of Nine Disease = gastrointestinal, oral, orthopedic, kidney, liver, cardiac, skin, neurological, cancer')
  user_choice_1 = input('What Disease You want to know about:  ')

  print('This is a four area you could know about = Physical_activity(pa), diet, Environment,')
  user_choice_2 = input('What area You want to know about: ')

  ################# Diet ##########################

  if user_choice_1 == 'cancer' and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_cancer')

  elif 'gastro' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_gastrointestinal')
  
  elif 'skin' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_skin')

  elif 'oral' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_oral')

  elif 'neuro' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_neurological')

  elif 'kidney' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_kidney')

  elif 'liver' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_liver')

  elif 'cardiac' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_cardiac')

  elif 'orthopedic' in user_choice_1 and user_choice_2 == 'diet':
    disease_func_diet('hs_health_conditions_orthopedic')

  else:
    print('Please check your inputs again')

  ############## physical activity ##################


  if user_choice_1 == 'cancer' and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_cancer')
    
  elif 'gastro' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_gastrointestinal')

  elif 'skin' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_skin')

  elif 'oral' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_oral')

  elif 'neuro' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_neurological')

  elif 'kidney' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_kidney')

  elif 'liver' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_liver')

  elif 'cardiac' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_cardiac')

  elif 'orthopedic' in user_choice_1 and user_choice_2 == 'pa':
    disease_func_pa('hs_health_conditions_orthopedic')

  else:
    print('Please check your inputs again')

  user_input = input("Do you want to stop? (yes/no): ")

  if user_input.lower() == "yes":
    break

