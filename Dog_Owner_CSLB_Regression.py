import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.compose import make_column_transformer

#Loading HLES_dog_owner csv
df = pd.read_csv('E:/Data_Science2_Seminar/Data-Science-2-Seminar/DAP_2021_HLES_dog_owner_v1.0.csv', low_memory=False)

# print(df.shape)

###-------Loading DAP_2021_CSLB_v1.0 csv---###
df2= pd.read_csv('E:/Data_Science2_Seminar/Data-Science-2-Seminar/DAP_2021_CSLB_v1.0.csv',low_memory=False)

#Set dog_id column as the Dataframe Index Column

cslb2 =df2.set_index('dog_id')

# generate a new dataframe name cslb only consiting of the cslb_score column

cslb= cslb2.loc[:,['cslb_score']]

#assign the dog_id column as Index for df dataframe and store it in a new variable named 'index_df'

index_df =df.set_index('dog_id')
# index_df.head(5)

#A new dataframe [exp_df] is created with some specific columns / varibales
#exp df consists of some specified columns from the actual Dataframe df

exp_df = index_df.loc[:,["dd_age_years",'dd_sex', 'dd_weight_lbs','dd_breed_pure_or_mixed','dd_breed_pure', 'dd_spayed_or_neutered',
                         'df_diet_consistency', 'df_feedings_per_day', 'df_daily_supplements_omega3', 'df_primary_diet_component' ]]
# print(exp_df.head())

######################---unwanted variables exclusion---#########################

#Dataframe filtered on dd_age_years Criteria and df_diet_consistency and Stored in a new df named 'data'

clean = (exp_df["dd_age_years"]>1) & (exp_df["dd_age_years"]<18) & (exp_df['dd_spayed_or_neutered'] == True) & (exp_df['df_diet_consistency'] != 3)
data = exp_df[clean]
# print(data.head())

#merging cslb score variable from cslb csv file

#datafrma 'data' and 'cslb' merged and Stored in a New variable named "final"
final = pd.merge(data, cslb, on='dog_id', how='inner', copy = False)
print(final.head())

# if we have duplicates in the column Dog_id we drop the entire row and the new dataframe generated is stored as df1 (# Final data frame to work with)

df1 = final.reset_index().drop_duplicates(subset='dog_id', keep='first').set_index('dog_id')

# Replacing NaN value in df1 dataframe with 0

df1.replace(np.nan, 0, inplace=True)

#Excluding the Breed Sample if Value_count_dd_pure_breed is less than 10

value_counts = df1['dd_breed_pure'].value_counts()

# Loop through the unique values in the 'dd_breed_pure' and delete rows where count is 0
for value in value_counts.index:
    if value_counts[value] < 10:
        df1 = df1[df1['dd_breed_pure'] != value]


print(df1.head())