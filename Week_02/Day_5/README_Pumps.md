For the Pumps project:

Please look at the things in such order:

1- load_test_train_split.py
2- RandomForest.py
3- P_TT_Target_RF-CN_HyperparamOpt.ipynb - which consists of the combination
      of both .py files to see it as a story.

load_test_train_split.py takes the csv files, combines them and splits
train/test
RandomForest.py performs feature engineering, uses RF as fitter, hyperparam.
optimization, CV and plots feature importance. It also gives an output of final
desired csv that has pump id index, output variable and predicted outcome.


To run the program:

1- Run load_test_train_split.py by arguments of two datasets to be loaded
(in this case pumps.csv, pumps_y.csv)

2- Run RandomForest.py by Xtrain, ytrain or Xtest, ytest
