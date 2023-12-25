import pandas as pd
import numpy as np

# dog owner csv

df = pd.read_csv('DAP_2021_HLES_dog_owner_v1.0.csv')

print(df.shape)

exp_df = df.set_index('dog_id')


"""#unwanted variables exclusion

Reason for exclusion:
1. age selected between 1 to 18. As below 1 year, puppies do not have fixed feeding frequency compared to adults and 
   above 18 years older dogs there are outliers
2. only neutered dogs are considered as almost 95% were spayed.
"""

clean = (exp_df["dd_age_years"] >= 1) & (exp_df["dd_age_years"] < 18) & (exp_df['dd_spayed_or_neutered'] == True)
data = exp_df[clean]
print(data.head())

print(data.shape)

"""# Excluding the Sample if the Value count of any breed is less than 10

"""

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

for col in disease_column:
  clean = (data[col] != 1) & (data[col] != 3)
  disease= data[clean]
  disease[col] = disease[col].map(lambda x: 0 if x == 0 else 1) #converting the disease data to binary 0 and 1, 0= not affected and 1= affected

  disease['df_appetite'] = disease['df_appetite'].map(lambda x: 1 if x >= 2 else 0) #converting the predicting variable data to binary 0 and 1, 1 = predicted outcome and 0 = opposite prediction

  import statsmodels.api as sm
  array1 =disease['df_appetite'].values
  array2 =disease[col].values

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
  if odds_ratio <= 0.95:
  # Print the results
    print(f'Odds Ratio for {col}: {odds_ratio:.4f}')
    print(f'Confidence Interval: [{conf_interval[0]:.4f}, {conf_interval[1]:.4f}]')
    print(f'p-value:', result.pvalues.loc['exposure_group'])

