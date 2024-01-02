import pandas as pd
import numpy as np
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

"""#Regression analysis
Cleaning the data:
1. hs_health_conditions_x = 1 and 3 is excluded as they are congenital diseases and we only want to work 
   with disease which are not congenital
"""
# define disease function for Diet

an_diet = ['df_diet_consistency', 'df_appetite', 'df_primary_diet_component_organic',
           'df_primary_diet_component_grain_free',
           'df_primary_diet_component_change_recent', 'df_weight_change_last_year', 'df_treats_frequency',
           'df_infrequent_supplements']
def disease_func_diet(user_choice):
  clean = (data[user_choice] != 1) & (data[user_choice] != 3)
  disease= data[clean]
  disease[user_choice] = disease[user_choice].map(lambda x: 0 if x == 0 else 1) #converting the disease data to binary 0 and 1, 0= not affected and 1= affected

  for variable in an_diet:
    if variable == 'df_diet_consistency':
      disease[variable] = disease[variable].map(lambda x: 0 if x >= 3 else 1) # 1 for very consistent, 0 for Non Consitent diet
      #hypo =
      
    elif variable == 'df_appetite':
      disease[variable] = disease[variable].map(lambda x: 0 if x == 1  else 1) # 0 for poor appetite and 1 for good appetite
      #hypo =
      
    elif variable == 'df_primary_diet_component_organic':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 indicates false to the organic diet and 1 for True Organic Diet
      #hypo =
      
    elif variable == 'df_primary_diet_component_grain_free':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 indicates false to the grainfree diet and 1 for True Grainfree Diet
      #hypo =
      
    elif variable == 'df_primary_diet_component_change_recent':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 for No and 1 for yes
      #hypo =
      
    elif variable == 'df_weight_change_last_year':
      disease[variable] = disease[variable].map(lambda x: 0 if x == 0  else 1) # 0 incdicates no change in weight in last year and 1 stand for change in weight in last year
      #hypo =
      
    elif variable == 'df_treats_frequency':
      disease[variable] = disease[variable].map(lambda x: 0 if x ==1 or x==4  else 1) # 0 indicates for poor treat frequency to the dogs and 1 stand for moderate treat frequency
      #hypo =
      
    elif variable == 'df_infrequent_supplements':
      disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1)
      #hypo =

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
    print(f'If {hypo} the odds of having {disease_name} diseases is: {(1 - odds_ratio) * 100:.4f}% less!')
    print(f'Odds Ratio for {user_choice} w.r.t {variable}: {odds_ratio:.4f}')
    print(f'Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}]')
    print(f'p-value:', result.pvalues.loc['exposure_group'])
    
#define disease_funtion Physical activities

variable_column_pa = ['pa_activity_level', 'pa_avg_activity_intensity', 'pa_swim', 'pa_physical_games_frequency',
                      'pa_moderate_weather_sun_exposure_level', 'pa_on_leash_walk_frequency',
                      'pa_other_aerobic_activity_frequency']
def disease_func_pa(user_choice):
    clean = (data[user_choice] != 1) & (data[user_choice] != 3)
    disease = data[clean]
    disease[user_choice] = disease[user_choice].map(
        lambda x: 0 if x == 0 else 1)  # converting the disease data to binary 0 and 1, 0= not affected and 1= affected

    for row in variable_column_pa:
        if row == 'pa_swim':
            disease[row] = disease[row].map(lambda x: 1 if x == True else 0)
            hypo = 'dogs go to swimming'

        elif row == 'pa_physical_games_frequency':
            disease[row] = disease[row].map(lambda x: 1 if x <= 3 else 0)
            hypo = "Dogs fetch items or play other games (such as Frisbee) that involve physical activity"

        elif row == 'pa_avg_activity_intensity':
            disease[row] = disease[row].map(lambda x: 0 if x == 1 else 1)
            hypo = "over the year the average intensity level of activity included jogging and sprinting "

        elif row == 'pa_activity_level':
            disease[row] = disease[row].map(lambda x: 0 if x == 1 else 1)
            hypo = "dog’s lifestyle over the past year has been active"

        elif row == 'pa_moderate_weather_sun_exposure_level':
            disease[row] = disease[row].map(lambda x: 1 if x <= 2 else 0)
            hypo = "dog’s have good sun exposure on moderate days (40‐85 degrees Fahrenheit)"

        elif row == 'pa_other_aerobic_activity_frequency':
            disease[row] = disease[row].map(lambda x: 1 if x >= 3 else 0)
            hypo = 'dog gets other aerobic (elevated heart rate) activity more than once a week'

        elif row == 'pa_on_leash_walk_frequency':
            disease[row] = disease[row].map(lambda x: 1 if x >= 3 else 0)
            hypo = 'average frequency that your dog is active on a lead/leash is more than once a week'

        import statsmodels.api as sm

        array1 = disease[row].values
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
        print(f'If {hypo} the likelihood of having {disease_name} diseases is: {(1 - odds_ratio) * 100:.4f} % less!')
        print(f'Odds Ratio for {user_choice} w.r.t {row}: {odds_ratio:.4f}')
        print(f'Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}]')
        print(f'p-value:', result.pvalues.loc['exposure_group'])

# define disease_funtion for behavior

behavior = ['db_aggression_level_food_taken_away', 'db_fear_level_bathed_at_home',
            'db_fear_level_nails_clipped_at_home', 'db_left_alone_restlessness_frequency',
            'db_urinates_alone_frequency', 'db_urinates_in_home_frequency',
            'db_aggression_level_unknown_aggressive_dog']
def disease_func_behavior(user_choice):
    clean = (data[user_choice] != 1) & (data[user_choice] != 3)
    disease = data[clean]
    disease[user_choice] = disease[user_choice].map(
        lambda x: 0 if x == 0 else 1)  # converting the disease data to binary 0 and 1, 0= not affected and 1= affected

    for variable in behavior:
        if variable == 'db_aggression_level_food_taken_away':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # No/Rarely aggression of dogs when food taken away by a family member results in less diseases
            hypo = 'dogs show No/Rarely aggression when food taken away by a family member'
        elif variable == 'db_fear_level_bathed_at_home':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # No fear while bathed at home results less diseases
            hypo = 'dogs show No fear while bathed at home'
        elif variable == 'db_fear_level_nails_clipped_at_home':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 3 else 1)  # No/Rare fear/anxiety results in less diseases
            hypo = 'dogs show No/Rare fear/anxiety while getting nails clipped at home'
        elif variable == 'db_left_alone_restlessness_frequency':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 3 else 1)  # Less/zero restlessness or agitation results in less diseases
            hypo = 'dogs show Less/zero restlessness or agitation when left alone at home'
        elif variable == 'db_urinates_alone_frequency':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # Not urinating when left alone results in less diseases
            hypo = 'dogs Not urinating when left alone'
        elif variable == 'db_urinates_in_home_frequency':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # Not urinating in home against objects results in less diseases
            hypo = 'dogs Not urinating in home against objects'
        elif variable == 'db_aggression_level_unknown_aggressive_dog':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # Less or no aggression results in less diseases
            hypo = 'dogs show Less or no aggression when approached by an unfamiliar dog'

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
        print(f'If {hypo} the likelihood of having {disease_name} diseases is: {(1 - odds_ratio) *100:.4f}% less!')
        print(f'Odds Ratio for {user_choice} w.r.t {variable}: {odds_ratio:.4f}')
        print(f'Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}]')
        print(f'p-value:', result.pvalues.loc['exposure_group'])

########### Define disease Function for Environment######################

environment = ['de_lifetime_residence_count','de_room_or_window_air_conditioning_present','de_drinking_water_is_filtered', 'de_asbestos_present', 'de_floor_types_wood',  
               'de_routine_toys', 'de_neighborhood_has_sidewalks', 'de_neighborhood_has_parks', 'de_dogpark', 'de_recreational_spaces', 'de_sitter_or_daycare', 'de_traffic_noise_in_home_frequency']

def disease_func_environment(user_choice):
    clean = (data[user_choice] != 1) & (data[user_choice] != 3)
    disease= data[clean]
    disease[user_choice] = disease[user_choice].map(lambda x: 0 if x == 0 else 1) #converting the disease data to binary 0 and 1, 0= not affected and 1= affected
    
    for variable in environment:
        if variable == 'de_lifetime_residence_count':
            disease[variable] = disease[variable].map(lambda x: 1 if x <=3  else 0) #x =0 when additonal residences are more than 3, x= 1 for lesser number of additional residence
      
        elif variable == 'de_room_or_window_air_conditioning_present':
            disease[variable] = disease[variable].map(lambda x: 0 if x == 0  else 1) #x =0 for no room or window air condition are x= 1 for included the room or air condition
      
        elif variable == 'de_drinking_water_is_filtered':
            disease[variable] = disease[variable].map(lambda x: 1 if x == 0  else 0) #x =0 for  filtered, x = 1 for non filtered
      
        elif variable == 'de_asbestos_present':
            disease[variable] = disease[variable].map(lambda x: 1 if x == 0  else 0) # x =0 for  asbestos(1,99 ), x = 1 for non asbestos(0 )
      
        elif variable == 'de_floor_types_wood':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 for  non wooded, x = 1 for wooden
      
        elif variable == 'de_routine_toys':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 No, x = 1 yes dog regularly lick, chew, or play with toys
            
        elif variable == 'de_neighborhood_has_sidewalks':
            disease[variable] = disease[variable].map(lambda x: 1 if x != 0 else 0) # x =0 No, x = 1 yes de_neighborhood_has_sidewalks
            
        elif variable == 'de_neighborhood_has_parks':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 No, x = 1 yes de_neighborhood_has_parks
    
        elif variable == 'de_dogpark':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 No, x = 1 yes de_dogpark
        
        elif variable == 'de_recreational_spaces':
            disease[variable] = disease[variable].map(lambda x: 0 if x == False else 1) # x =0 No, x = 1 yes de_recreational_spaces
            
        elif variable == 'de_sitter_or_daycare':
            disease[variable] = disease[variable].map(lambda x: 0 if x == False else 1) # x =0 No, x = 1 yes de_sitter_or_daycare
        
        elif variable == 'de_traffic_noise_in_home_frequency':
            disease[variable] = disease[variable].map(lambda x: 1 if x > 1 else 0) # x =0 No, x = 1 yes de_traffic_noise_in_home_frequency
        
        import statsmodels.api as sm

        array1 =disease[variable].values
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
        print(f'Odds Ratio for {user_choice} w.r.t {variable}: {odds_ratio:.4f}')
        print(f'Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}]')
        print(f'p-value:', result.pvalues.loc['exposure_group'])
      
while True:
    # taking user Input
    print('This is a list of available diseases = gastrointestinal, oral, orthopedic, kidney, liver, cardiac, skin, '
          'neurological, cancer')
    user_choice_1 = input('The disease you want to know about: ')
    disease_name = user_choice_1

    print('These are the available variables section = Physical_activity(pa), diet, environment, behavior')
    user_choice_2 = input('The variable You want to know about: ')

    ################# Diet ##########################

    if user_choice_1 == 'cancer' and user_choice_2 == 'diet':
        disease_func_diet('hs_health_conditions_cancer')

    elif user_choice_1 == 'gastrointestinal' and user_choice_2 == 'diet':
        disease_func_diet('hs_health_conditions_gastrointestinal')

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

    ############## physical activity ##################
    elif user_choice_1 == 'cancer' and user_choice_2 == 'pa':
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
            
        ################----Environment--------#################
        
    elif user_choice_1 == 'cancer' and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_cancer')

    elif 'gastro' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_gastrointestinal')
    
    elif 'skin' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_skin')

    elif 'oral' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_oral')

    elif 'neuro' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_neurological')

    elif 'kidney' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_kidney')

    elif 'liver' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_liver')

    elif 'cardiac' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_cardiac')

    elif 'orthopedic' in user_choice_1 and user_choice_2 == 'environment':
        disease_func_environment('hs_health_conditions_orthopedic')

    ############## Behavior ##################
    elif user_choice_1 == 'cancer' and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_cancer')

    elif user_choice_1 == 'gastrointestinal' and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_gastrointestinal')

    elif 'skin' in user_choice_1 and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_skin')

    elif 'oral' in user_choice_1 and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_oral')

    elif 'neuro' in user_choice_1 and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_neurological')

    elif 'kidney' in user_choice_1 and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_kidney')

    elif 'liver' in user_choice_1 and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_liver')

    elif 'cardiac' in user_choice_1 and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_cardiac')

    elif 'orthopedic' in user_choice_1 and user_choice_2 == 'behavior':
        disease_func_behavior('hs_health_conditions_orthopedic')

    else:
        print('Please check your inputs again')

    user_input = input("Do you want to stop? (yes/no): ")

    if user_input.lower() == "yes":
        break