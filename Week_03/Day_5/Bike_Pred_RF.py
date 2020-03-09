import pandas as pd
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import probplot
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.preprocessing import PolynomialFeatures, MinMaxScaler
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sys import argv
import warnings


warnings.filterwarnings('ignore')
#Name of train or test files
namelist = argv[1:]
########################################################

#--------------------------- LOAD THE DATA----------------------------
print('Loading the data...')
df_train = pd.read_csv(namelist[0], index_col = 0)


####------------------- FEATURE ENGINEERING --------------##################
print('Performing Feature Engineering...')

#Hour Binning
hour_range = range(0,24)
bins = ['Night']*5 + ['Morning']*5 + ['Day']*6 + ['Evening']*8
hour_new = dict(zip(hour_range, bins))
df_train['Hour_binned'] = df_train['Hour'].map(hour_new)

#Hour_Dict_Factorization_Low Level
factor_hour = {'Night': 0, 'Morning':1, 'Day': 2, 'Evening': 3}
df_train['Hour_Reconvert'] = df_train['Hour_binned'].map(factor_hour)

# Month and Season Polynomial Degree = 2 ENCODING
df_train['Month_Poly2'] = df_train['Month']**2
df_train['season_Poly2'] = df_train['season']**2

#--------------------------------------------------------------------

#Separate Categorical and Numerical Columns

num_list = ['count', 'atemp', 'humidity', 'temp', 'windspeed'] # Numeric All
num_nows = ['count', 'atemp', 'humidity', 'temp'] # Numeric No windspeed
cat_list = df_train.columns.drop(num_list).tolist() # Categorical but in fact has flattened numerics inside

#--------------------------------------------------------------------

#TRAINING SUBSET selection
Xtrain_nonscaled = df_train[['Year', 'atemp', 'Hour']]
ytrain_nonscaled = df_train['count']
#--------------------------------------------------------------------

#----------------------Scale the Numerical Variables--------------------
sc = MinMaxScaler()
Xtrain_sc= sc.fit_transform(Xtrain_nonscaled)
Xtrain_sc = pd.DataFrame(Xtrain_sc, columns = Xtrain_nonscaled.columns)
#Take log1p of the target var
ytrain_sc = np.log1p(ytrain_nonscaled)

#----------------------GRID SEARCH CV and RF FIT----------------------------
print('Grid Search Cross-Validation Optimization')
#Random Forest
rf = RandomForestRegressor()
rf_param = { 'max_depth': [1, 5, 8, 32],#, 8, 32, 128, None],
    'n_estimators': [10, 100]}#, 100, 1000, 1000]}

grid_rf= GridSearchCV(rf,rf_param,scoring = 'neg_mean_squared_error',cv=5)
grid_rf.fit( Xtrain_sc, ytrain_sc )
ypred = grid_rf.predict(Xtrain_sc)

best_score = (grid_rf.best_score_)*-1
print('MSE is:', best_score)
print('Random Forest Regressor is running...')
#----------------------------------------RF Fit with GSCV params -------------
rf = RandomForestRegressor(max_depth = grid_rf.best_params_['max_depth'],
                            n_estimators = grid_rf.best_params_['n_estimators'])
rf.fit(Xtrain_sc, ytrain_sc)
feature_label = Xtrain_sc.columns
feature_importance =rf.feature_importances_

plt.title('Feature Importance')
plt.bar(feature_label,feature_importance)
plt.xticks(rotation=45)
plt.show()


#-------------------ASSUMPTION CHECK ------------------------ #

#Check the assumptions
#Mean residual is around zero
residuals = ypred - ytrain_sc

#Q-Q plot
#probplot(residuals, plot=plt)
plt.figure(figsize = (12,5))
plt.subplot(1,2,1) # r, c, fignum
plt.title('Mean Residual:' f'{residuals.mean()}')
residuals.hist()
plt.subplot(1,2,2) # r, c, fignum
probplot(residuals, plot=plt)
plt.show()


#Residuals uncorrelated with x and must be equally on and under 0
fig = plt.figure(figsize = (12,5))

for column,i in zip(Xtrain_sc.columns, range(1,len(Xtrain_sc.columns)+1)):
    ax = fig.add_subplot(1,3,i)
    ax.scatter(Xtrain_sc[column], residuals)
    ax.set_title(f'{column}''Residuals')
    ax.set_xlabel(f'{column}')
    ax.set_ylabel('Residuals')
plt.show()

#-------------------------DATA v. PREDICTION ----------------------------#
a = pd.DataFrame(ytrain_nonscaled)
ypred_back = np.expm1(ypred)
a['datetime'] = ytrain_nonscaled.index
ypred_back = ypred_back.astype(int)
a['Prediction'] = ypred_back[:]

#Plot predicted vs real values
plt.scatter(a['count'], a['Prediction'])
plt.xlabel('Real_Counts')
plt.ylabel('Predicted_Counts')
plt.title('Prediction vs. Reality')
plt.show()

#-------------------------RMSLE----------------------------#

ms = (np.log1p(a['Prediction'])-np.log1p(a['count']))**2
s = np.sum(ms)
msle = s/len(a['Prediction'])
rmsle = np.sqrt(msle)
print('RMSLE is:', rmsle)

#-----------------------SAVE------------------------------#
a.to_csv(f'{namelist[0]}_Predictions.csv', index_label = 'datetime')
