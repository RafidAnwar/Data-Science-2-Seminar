import pandas as pd
import numpy as np
import warnings
import sys
import statsmodels.api as sm

# ignore the simple error warnings in the terminal
warnings.filterwarnings("ignore")
# called from paper_health_regression_part_gui.py to get results from this terminal window
def calculate_result(user_choice_1, user_choice_2):
    result = ""
    return result

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

data.replace(np.nan, 0, inplace=True)

value_counts = data['dd_breed_pure'].value_counts()

# Loop through the unique values in the 'FloatColumn' and delete rows where count is 0
for value in value_counts.index:
    if value_counts[value] < 10:
        data = data[data['dd_breed_pure'] != value]

"""Regression analysis
Cleaning the data in the following four functions:
1. hs_health_conditions_x = 1 and 3 is excluded as they are congenital diseases and we only want to work 
with disease which are not congenital
"""
# mention all selected variables for Diet

an_diet = ['df_diet_consistency', 'df_appetite', 'df_primary_diet_component_organic',
           'df_primary_diet_component_grain_free',
           'df_primary_diet_component_change_recent', 'df_weight_change_last_year', 'df_treats_frequency',
           'df_infrequent_supplements']

# define disease function for Diet
def disease_func_diet(user_choice):
    
    clean = (data[user_choice] != 1) & (data[user_choice] != 3)
    disease= data[clean]
    disease[user_choice] = disease[user_choice].map(lambda x: 0 if x == 0 else 1) #converting the disease data to binary 0 and 1, 0= not affected and 1= affected
    suggestion = [f' Suggestion to minimize the effect of {disease_name} diseases : \n']
    hypotheses = ['\nDetailed result of logistic regression results']

    for variable in an_diet:
        if variable == 'df_diet_consistency':
            disease[variable] = disease[variable].map(lambda x: 0 if x >= 3 else 1) # 1 for very consistent, 0 for Non Consitent diet
            hypo = "dog has a very consistent diet"
            psugg = " >>Make sure your dog follows a very consistent diet!  "
            nsugg = ">>Make sure dog's diet is not consistent!"

        elif variable == 'df_appetite':
            disease[variable] = disease[variable].map(lambda x: 0 if x == 1  else 1) # 0 for poor appetite and 1 for good appetite
            hypo = 'dog shows good appetite'
            psugg = " >>Keep an eye out on your dogs appetite and make sure he has a good appetite "
            nsugg = ">>Keep an eye out on your dogs apetite, its bad if he is always hungry"

        elif variable == 'df_primary_diet_component_organic':
            disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 indicates false to the organic diet and 1 for True Organic Diet
            hypo = "dog's primary diet components is organic"
            psugg = " >>Try to feed organic foods to your dog! "
            nsugg = ">>Try not to feed organic foods to your dog!"

        elif variable == 'df_primary_diet_component_grain_free':
            disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1) # 0 indicates false to the grainfree diet and 1 for True Grainfree Diet
            hypo = "dog's diet is grain free"
            psugg = '>>Try to feed grain free food to your dog!'
            nsugg = ">>try not to feed grain free food to your dog!"
            
        elif variable == 'df_primary_diet_component_change_recent':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True  else 0) # 0 for No and 1 for yes
            hypo ="any recent changes are made in dog diet"
            psugg = ">>Try to change dog's primary diet component frequently! "
            nsugg = ">>Try not to change your dog's primary diet component frequently!"

        elif variable == 'df_weight_change_last_year':
            disease[variable] = disease[variable].map(lambda x: 0 if x == 0  else 1) # 0 incdicates no change in weight in last year and 1 stand for change in weight in last year
            hypo = "dog weight varies from last year (except puppies)"
            psugg = '>>Keep an eye out on your dog weight! Go to vet if it changes over the year!'
            nsugg = ">>Keep an eye out on your dog weight! go to vet if it doesnt change over the year!"
            
        elif variable == 'df_treats_frequency':
            disease[variable] = disease[variable].map(lambda x: 0 if x ==0 or x==4  else 1) # 0 indicates for poor treat frequency to the dogs and 1 stand for moderate treat frequency
            hypo = "owner does not give treat to dog at least once a day other than dog's regular mealtime"
            psugg = '>>Try to give your dog treats moderately! '
            nsugg = ">>Try not to give your dog treats moderately!"
            
        elif variable == 'df_infrequent_supplements':
            disease[variable] = disease[variable].map(lambda x: 0 if x == False  else 1)
            hypo = "any supplements given less often than every day to the dogs"
            psugg = '>>Try to give your dog supplements less often than everyday! '
            nsugg = ">>Try to give your dog supplements everyday!"

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
        result = logit_model.fit(disp=0)

    # Get odds ratio and confidence interval
        odds_ratio = np.exp(result.params[1])
        conf_interval = np.exp(result.conf_int().iloc[1])

    # Print the results
        if result.pvalues.loc['exposure_group'] < 0.05:
            if odds_ratio > 1:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(odds_ratio - 1) * 100:.4f}% more!')
                hypotheses.append(sentence)
                suggestion.append(nsugg)
            else:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(1 - odds_ratio) * 100:.4f}% less!')
                hypotheses.append(sentence)
                suggestion.append(psugg)
        else:
            pass

    for sentence in suggestion:
        print(sentence)

    for line in hypotheses:
        print(line)

# Add all selected variables for physical activity
variable_column_pa = ['pa_activity_level', 'pa_physical_games_frequency','pa_avg_activity_intensity','pa_swim',
                      'pa_moderate_weather_sun_exposure_level', 'pa_moderate_weather_daily_hours_outside',
                      'pa_other_aerobic_activity_frequency', 'pa_on_leash_walk_frequency']

#define disease_funtion Physical activities
def disease_func_pa(user_choice):
    clean = (data[user_choice] != 1) & (data[user_choice] != 3)
    disease = data[clean]
    disease[user_choice] = disease[user_choice].map(
        lambda x: 0 if x == 0 else 1)  # converting the disease data to binary 0 and 1, 0= not affected and 1= affected
    suggestion = [f' Suggestion to minimize the effect of {disease_name} diseases : \n']
    hypotheses = ['\nDetailed result of logistic regression results']

    for row in variable_column_pa:
        if row == 'pa_activity_level':
            disease[row] = disease[row].map(lambda x: 0 if x == 1 else 1) # 0 =not active and 1= moderately or very active
            hypo = "dog's lifestyle over the past year has been active"
            psugg = ">>Try to make sure your dog has an active lifestyle!"
            nsugg = ">>Try to make sure that your dog doesnt have an active lifestyle"

        elif row == 'pa_physical_games_frequency':
            disease[row] = disease[row].map(lambda x: 1 if x <= 3 else 0) #1= atleast monthly physical games, 0 =rarely or never physical games
            hypo = "Dog fetches items or play other games (such as Frisbee) that involve physical activity"
            psugg = ">>Play games such as Frisbee with you dog or ask yor dog to fetch items more"
            nsugg = ">>Dont play games such as Frisbee with you dog or ask yor dog to fetch items more"

        elif row == 'pa_avg_activity_intensity':
            disease[row] = disease[row].map(lambda x: 0 if x == 1 else 1) # 0 = only walking 1 = jogging and sprinting
            hypo = "over the year the average intensity level of activity of dog included jogging and sprinting "
            psugg = ">>Try to make sure that your dog does good amount of jogging and sprinting! "
            nsugg = ">>Try to make sure that your dog does not do much jogging and sprinting!"

        elif row == 'pa_swim':
            disease[row] = disease[row].map(lambda x: 1 if x == True else 0) # 0 = no swimming
            hypo = 'dog goes to swimming'
            psugg = ">>Take your dog to swimming more often!"
            nsugg = ">>Dont Take your dog to swimming that much!"

        elif row == 'pa_moderate_weather_sun_exposure_level':
            disease[row] = disease[row].map(lambda x: 1 if x <= 2 else 0) # 1 = full sun or access to shade or sun, 0 = full shade
            hypo = "dog has good sun exposure on moderate days (40‐85 degrees Fahrenheit)"
            psugg = ">>On moderate days (40-85 degrees Fahrenheit) try to make sure your dog has exposure to sun"
            nsugg = ">>On moderate days (40-85 degrees Fahrenheit) try to make sure your dog is under a shade"

        elif row == 'pa_moderate_weather_daily_hours_outside':
            disease[row] = disease[row].map(lambda x: 0 if x in [1, 5] else 1) # 0 =less than 3 hours, 1 = more than 3hr
            hypo = 'during moderate weather dog spends less than 3 hours on average outdoors'
            psugg = ">>On moderate days (40-85 degrees Fahrenheit) try to make sure your dog spends less than 3 hours on average outdoors"
            nsugg = ">>On moderate days (40-85 degrees Fahrenheit) try to make sure your dog spends more than 3 hours on average outdoors"

        elif row == 'pa_other_aerobic_activity_frequency':
            disease[row] = disease[row].map(lambda x: 1 if x >= 3 else 0) #0 = less than once a week 1= more than once a week
            hypo = 'dog gets other aerobic (elevated heart rate) activity more than once a week'
            psugg = ">>Do more aerobic activities that Elevate heart rate more than once a week"
            nsugg = ">>Do more aerobic activities that Elevate heart rate less than once a week"

        elif row == 'pa_on_leash_walk_frequency':
            disease[row] = disease[row].map(lambda x: 1 if x >= 3 else 0) # 0 = less than once a week 1= more than once a week
            hypo = 'average frequency that your dog is active on a lead/leash is more than once a week'
            psugg = ">>your dog should be active on a lead/leash more than once a week"
            nsugg = ">>your dog should be active on a lead/leash less than once a week"

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
        result = logit_model.fit(disp=0)

        # Get odds ratio and confidence interval
        odds_ratio = np.exp(result.params[1])
        conf_interval = np.exp(result.conf_int().iloc[1])

        # Print the results
        if result.pvalues.loc['exposure_group'] < 0.05:
            if odds_ratio > 1:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(odds_ratio - 1) * 100:.4f}% more!')
                hypotheses.append(sentence)
                suggestion.append(nsugg)
            else:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(1 - odds_ratio) * 100:.4f}% less!')
                hypotheses.append(sentence)
                suggestion.append(psugg)
        else:
            pass

    for sentence in suggestion:
        print(sentence)

    for line in hypotheses:
        print(line)
        
# add all selected variables for behavior

behavior = ['db_aggression_level_food_taken_away', 'db_fear_level_bathed_at_home',
            'db_fear_level_nails_clipped_at_home', 'db_left_alone_restlessness_frequency',
            'db_urinates_alone_frequency', 'db_urinates_in_home_frequency',
            'db_aggression_level_unknown_aggressive_dog', 'db_hyperactive_frequency']
# define disease_funtion for behavior
def disease_func_behavior(user_choice):
    clean = (data[user_choice] != 1) & (data[user_choice] != 3)
    disease = data[clean]
    disease[user_choice] = disease[user_choice].map(
        lambda x: 0 if x == 0 else 1)  # converting the disease data to binary 0 and 1, 0= not affected and 1= affected
    suggestion = [f' Suggestion to minimize the effect of {disease_name} diseases : \n']
    hypotheses = ['\nDetailed result of logistic regression results']

    for variable in behavior:
        if variable == 'db_aggression_level_food_taken_away':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # No/Rarely aggression of dogs when food taken away by a family member results in less diseases
            hypo = 'dogs show No/Rarely aggression when food taken away by a family member'
            psugg = ">> Your dog has lesser chance of having gastronominal disease, If your dog become rarely aggressive when food taken away,"
            nsugg = ">> Your dog has chance of having gastronominal disease, If your dog become aggressive when food taken away,"
            
        elif variable == 'db_fear_level_bathed_at_home':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # No fear while bathed at home results less diseases
            hypo = 'dogs show No fear while bathed at home'
            psugg = ">>Try to Be very friendly and gentle to your pet while bathing so that he/she does not become afraid"
            nsugg = ">>Try not to Be very friendly and gentle to your pet while bathing so that he/she becomes afraid"
                
        elif variable == 'db_fear_level_nails_clipped_at_home':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 3 else 1)  # No/Rare fear/anxiety results in less diseases
            hypo = 'dogs show No/Rare fear/anxiety while getting nails clipped at home'
            psugg = ">> Try to Be very friendly and gentle to your pet while getting nails clipped at home so that it shows no fear/anxiety"
            nsugg = ">> It is not so important to Be very friendly and gentle to your pet while getting nails clipped at home so that it shows fear/anxiety"
                        
        elif variable == 'db_left_alone_restlessness_frequency':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 3 else 1)  # Less/zero restlessness or agitation results in less diseases
            hypo = 'dogs show Less/zero restlessness or agitation when left alone at home'
            psugg = ">>Try to get help and take care of your dog if he/she shows any signs of fear or agitation when left alone at home "
            nsugg = ">>There is nothing to fear if your dog shows fear/agitation when left alone at home"
            
        elif variable == 'db_urinates_alone_frequency':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # Not urinating when left alone results in less diseases
            hypo = 'dogs Not urinating when left alone'
            psugg = ">>Try to get help and take care of your dog if he/she urinating when left alone"
            nsugg = ">>There is nothing to fear if your dog urinates while left alone"
            
        elif variable == 'db_urinates_in_home_frequency':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # Not urinating in home against objects results in less diseases
            hypo = 'dogs Not urinating in home against objects'
            psugg = ">> Try to consult vet if your dog is urinating in home against objects "
            nsugg = ">> There is nothing to worry if your dog is urinating in home against objects"
            
        elif variable == 'db_aggression_level_unknown_aggressive_dog':
            disease[variable] = disease[variable].map(
                lambda x: 0 if x >= 2 else 1)  # Less or no aggression results in less diseases
            hypo = 'dogs show Less or no aggression when approached by an unfamiliar dog'
            psugg = ">> Teach your dog to be calm when approached by an unfamiliar dog"
            nsugg = ">> There is no risk if your dog shows aggression when approached by an unfamiliar dog"
            
        elif variable == 'db_hyperactive_frequency':
            disease[variable] = disease[variable].map(
                lambda x: 1 if x <= 2 else 0)  # less restlessness results in less diseases
            hypo = 'dogs are less Hyperactive,restless or has trouble settling down'
            psugg = ">>Make sure your dog is not hyperactive,restless or has any trouble settling down."
            nsugg = ">>Make sure your dog is hyperactive,restless or has trouble settling down."

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
        result = logit_model.fit(disp=0)

        # Get odds ratio and confidence interval
        odds_ratio = np.exp(result.params[1])
        conf_interval = np.exp(result.conf_int().iloc[1])

        # Print the results
        if result.pvalues.loc['exposure_group'] < 0.05:
            if odds_ratio > 1:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(odds_ratio - 1) * 100:.4f}% more!')
                hypotheses.append(sentence)
                suggestion.append(nsugg)
            else:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(1 - odds_ratio) * 100:.4f}% less!')
                hypotheses.append(sentence)
                suggestion.append(psugg)
        else:
            pass

    for sentence in suggestion:
        print(sentence)

    for line in hypotheses:
        print(line)

# add all selected variables for environment
environment = ['de_lifetime_residence_count','de_room_or_window_air_conditioning_present','de_drinking_water_is_filtered', 'de_asbestos_present', 'de_floor_types_wood',  
               'de_routine_toys', 'de_neighborhood_has_sidewalks', 'de_neighborhood_has_parks', 'de_dogpark', 'de_recreational_spaces', 'de_sitter_or_daycare', 'de_traffic_noise_in_home_frequency']

########### Define disease Function for Environment######################
def disease_func_environment(user_choice):
    clean = (data[user_choice] != 1) & (data[user_choice] != 3)
    disease= data[clean]
    disease[user_choice] = disease[user_choice].map(lambda x: 0 if x == 0 else 1) #converting the disease data to binary 0 and 1, 0= not affected and 1= affected
    suggestion = [f' Suggestion to minimize the effect of {disease_name} diseases : \n']
    hypotheses = ['\nDetailed result of logistic regression results']

    for variable in environment:
        if variable == 'de_lifetime_residence_count':
            disease[variable] = disease[variable].map(lambda x: 1 if x <=3  else 0) #x =0 when additonal residences are more than 3, x= 1 for lesser number of additional residence
            hypo = "Dogs whose Owner has less than three additional addresses in dog's lifetime "
            psugg = ">>Try not to change residence very frequently in dog's lifetime"
            nsugg = ">>Try to move in more than three residences"

        elif variable == 'de_room_or_window_air_conditioning_present':
            disease[variable] = disease[variable].map(lambda x: 0 if x == 0  else 1) #x =0 for no room or window air condition are x= 1 for included the room or air condition
            hypo = "Dog Owner's residence has sufficient air conditioning"
            psugg = ">>Try to ensure that your residence where you will live with dog has good air conditioning"
            nsugg = ">>Good air conditioning system is not a must to ensure dogs' health"

        elif variable == 'de_drinking_water_is_filtered':
            disease[variable] = disease[variable].map(lambda x: 0 if x == 0  else 1) #x =0 for  filtered, x = 1 for non filtered
            hypo = "drinking water on owner'residence is not filtered"
            nsugg = '>>Try to ensure that your residence where you will live with dog has filtered drinking water for the dog'
            psugg = ">>Filtered is not a must to ensure dogs' health"

        elif variable == 'de_asbestos_present':
            disease[variable] = disease[variable].map(lambda x: 0 if x == 0  else 1) # x =0 for  asbestos(1,99 ), x = 1 for non asbestos(0 )
            hypo = "asbestos is present in owner's residence floor"
            nsugg = ">>Please try to make sure that your residence floor is asbestos free"
            psugg = ">>Try to make sure that there are asbestos in your residence floor"
            
        elif variable == 'de_floor_types_wood':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 for  non wooded, x = 1 for wooden
            hypo = "Dog Owner's residence has wooden floor"
            nsugg = ">>Try not to consider wooden floor floor your residence"
            psugg = ">>Try to consider wooden floor floor your residence"
            
        elif variable == 'de_routine_toys':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 No, x = 1 yes dog regularly lick, chew, or play with toys
            hypo = "dog regularly lick, chew, or play with toys"
            psugg = ">>Try to ensure that your dog is regularly licking, chewing and playing with toys"
            nsugg = ">>Try not to provide your pet with chewing or licking ingredients or toy regularly"

        elif variable == 'de_neighborhood_has_sidewalks':
            disease[variable] = disease[variable].map(lambda x: 0 if x > 0 else 1) # x =0 No, x = 1 yes de_neighborhood_has_sidewalks
            hypo = 'neighbourhood does not have many sidewalks'
            nsugg = ">>Having too many sidewalks in neighbourhood is not a problem"
            psugg = ">>Try to make sure that your neighbourhood does not have many sidewalks"
            
        elif variable == 'de_neighborhood_has_parks':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 No, x = 1 yes de_neighborhood_has_parks
            hypo = "there parks or green spaces within half a mile of dog owner's home"
            nsugg = ">>It is not important to consider such neighbourhood that has parks or green space with half a mile"
            psugg = ">>Try to consider such neighbourhood that has parks or green space within half a mile"
            
        elif variable == 'de_dogpark':
            disease[variable] = disease[variable].map(lambda x: 1 if x == True else 0) # x =0 No, x = 1 yes de_dogpark
            hypo = 'neighbourhood has dog parks'
            nsugg = ">>It is not necessary to have Dog parks in neighbourhood"
            psugg = ">>Try to live in such neighbourhoods that have Dog parks"
            
        elif variable == 'de_recreational_spaces':
            disease[variable] = disease[variable].map(lambda x: 0 if x == False else 1) # x =0 No, x = 1 yes de_recreational_spaces
            hypo = "there are recreational space in the neighbourhood"
            psugg= ">>Try to choose such neighbourhood that have recreational spaces"
            nsugg = ">>Try not to choose such neighbourhood that have recreational spaces"
            
            
        elif variable == 'de_sitter_or_daycare':
            disease[variable] = disease[variable].map(lambda x: 0 if x == False else 1) # x =0 No, x = 1 yes de_sitter_or_daycare
            hypo = "the dog's been taken to the daycare center by the owner"
            psugg = ">>Try to take your pet to the daycare centre "
            nsugg = ">>It is not necessary to take your pet to the daycare centre"
            
        elif variable == 'de_traffic_noise_in_home_frequency':
            disease[variable] = disease[variable].map(lambda x: 1 if x > 1 else 0) # x =0 No, x = 1 yes de_traffic_noise_in_home_frequency
            hypo = "the occurrence of traffic noice is more frequent"
            psugg = ">>It is not a issue if there is frequent traffic noise in the  neighbourhood"
            nsugg = ">>Try to avoid such neighbourhood where traffic noise is more frequent"

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
        result = logit_model.fit(disp=0)

        # Get odds ratio and confidence interval
        odds_ratio = np.exp(result.params[1])
        conf_interval = np.exp(result.conf_int().iloc[1])
        
            # Print the results
        if result.pvalues.loc['exposure_group'] < 0.05:
            if odds_ratio > 1:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(odds_ratio - 1) * 100:.4f}% more!')
                hypotheses.append(sentence)
                suggestion.append(nsugg)
            else:
                sentence = (f'\n>>If {hypo} the odds of having {disease_name} diseases is: {(1 - odds_ratio) * 100:.4f}% less!')
                hypotheses.append(sentence)
                suggestion.append(psugg)
        else:
            pass

    for sentence in suggestion:
        print(sentence)

    for line in hypotheses:
        print(line)

# Assign the inputs given in the front end by the user
user_choice_1 = sys.argv[1]
disease_name = user_choice_1
user_choice_2 = sys.argv[2]

# call the disease diet function for all choices of diseases and diet

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

# call the disease physical activity function for all choices of diseases and physical activity
elif user_choice_1 == 'cancer' and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_cancer')

elif 'gastro' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_gastrointestinal')

elif 'skin' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_skin')

elif 'oral' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_oral')

elif 'neuro' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_neurological')

elif 'liver' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_liver')

elif 'cardiac' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_cardiac')

elif 'orthopedic' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_orthopedic')

elif 'kidney' in user_choice_1 and user_choice_2 == 'physical_activity':
    disease_func_pa('hs_health_conditions_kidney')

# call the disease environment function for all choices of diseases and environment

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

# call the disease behavior function for all choices of diseases and behavior
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
