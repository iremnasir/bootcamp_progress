#Import necessary modules
import numpy as np
from sys import argv
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix, roc_auc_score, roc_curve

#Name of train or test files
namelist = argv[1:]

#-----------------------------------------#
#          FEATURE ENGINEERING            #
#-----------------------------------------#

#Read-in split data
X_train = pd.read_csv(namelist[0], index_col = 0)
ytrain = pd.read_csv(namelist[1], header = None, index_col = 0)

#Check the sizes

if len(X_train) != len(ytrain):
    print("DataFrames aren't of equal length")

#Merge the training data back together
df_p = pd.concat([X_train, ytrain], axis = 1)

#Rename the merged target group column name
df_p.rename(columns = {1:'status_group'}, inplace = True)

#Replace "functional needs repair" by "non functional"
#The rationale behind it is simply we don't want a bad shape pump go under the radar

df_p['status_group'] = df_p['status_group'].str.replace('functional needs repair', 'non functional')
print ('Fraction of functional pipes is:',df_p['status_group'].value_counts(1)[0], '\n',
       'Fraction of non-functional pipes is:',df_p['status_group'].value_counts(1)[1])

#Remove scheme_name and date_recorded because
#scheme_name is mostly empty and date_recorded is something that cant be correlated
print ('Removing scheme_name and date_recorded from the data frame ...')
df_p = df_p.drop(['scheme_name', 'date_recorded'], axis=1)

#Divide df into numeric and categorical
#Get rid of num_private
print('Slicing out numerical and categorical columns...')
df_num = df_p[['amount_tsh', 'gps_height', 'longitude', 'latitude', 'region_code', 'district_code', 'population', 'construction_year']]

#Categorical df

df_cat = df_p[['funder', 'installer', 'wpt_name', 'basin', 'subvillage', 'region', 'lga', 'ward', 'public_meeting', 'recorded_by', 'scheme_management', 'permit', 'extraction_type', 'extraction_type_group', 'extraction_type_class', 'management', 'management_group', 'payment', 'payment_type', 'water_quality', 'quality_group', 'quantity', 'quantity_group', 'source', 'source_type', 'source_class', 'waterpoint_type', 'waterpoint_type_group', 'status_group']]

#Imputation with mean, median and most frequent
print ('Imputing construction_year with the most frequent value after 0...\n\n\n')
#Construction_Year
year_to_replace_with = df_num['construction_year'].value_counts()
year_to_replace_with.index[1]
df_num['construction_year'].replace(0, year_to_replace_with.index[1], inplace = True)

#Fill all NaNs with 'no data'
print('\n\n\n')
print ('Filling NaNs with a "not available" statement...')
df_cat_fillna = df_cat.fillna('not available')

#Dummify the target
print ('Dummifying the status_group (a.k.a target variable)')
dummy_target_var = pd.get_dummies(df_cat_fillna['status_group'])

#Concat original cat df and dummified target
print('Concatenating the categorical and target columns')
df_cat_fillna_dummy_target = pd.concat([df_cat_fillna, dummy_target_var], axis = 1)
#-----------------------------------------------------------
#Target Encoding a Subset of columns

#Subset of large var list
column_list_to_target_encode = ['extraction_type', 'payment', 'quantity', 'waterpoint_type']

print ('Target encoding a subset of categorical columns', f'{column_list_to_target_encode}')


for column in column_list_to_target_encode:
    target_means = df_cat_fillna_dummy_target.groupby(column).mean()
    df_cat_fillna_dummy_target[f'{column}_func'] = df_cat_fillna_dummy_target[column].replace(target_means['functional'])
#---------------------------------------------------------------

# merge with numerical df
print('Concatenating with numerical column construction_year')
num_dumm_cat = pd.concat([df_cat_fillna_dummy_target,df_num], axis = 1)

# List Extension and Comprehension
#for functionals
s_func = '_func'
func_list = [x + s_func for x in column_list_to_target_encode]

num_list = []
num_list =['construction_year']
func_list.extend(num_list)

#-----------------------TARGET ENCODING ENDS-------------------------------#
#------------------------MODEL TRAINING--------------------------#
#Define data and train sets
X_func = num_dumm_cat.loc[:, func_list]
y_func = num_dumm_cat.loc[:, 'functional']

print('Performing Random Forest...')
rf = RandomForestClassifier(n_estimators=100, max_depth=5)
m_rf=rf.fit(X_func,y_func)
y_pred_rf=m_rf.predict(X_func)

print('Accuracy for functional pump prediction is', accuracy_score(y_func,y_pred_rf))
 # calculates the accuracy (% of correct points) for func
 #----------------------------CROSS_VALIDATION-----------------------#

print ('Performing 5-fold cross-validation')
accuracy_func = cross_val_score(m_rf, X_func, y_func, cv=5, scoring='accuracy')
mean_func = np.mean(accuracy_func)
std_func = np.std(accuracy_func)
print(
"Mean cross-validation score for functional-pumps:", mean_func, '\n',
"St.dev of cross-validation score for functional-pumps:", std_func)

#--------------------------FEATURE IMPORTANCE -------------------------#
feature_label = X_func.columns
feature_importance =m_rf.feature_importances_
plt.bar(feature_label, feature_importance)
plt.xticks(rotation=45)
plt.show()
