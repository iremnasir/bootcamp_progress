from sklearn.linear_model import LinearRegression
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


#pop = pd.read_excel('gapminder_population.xlsx', index_col=0)
pop = pop.sum()
#logpop = np.log(pop)
#logpop.dropna(inplace=True)





pop.index = pop.index.astype(int)
#y = logpop.values

for year, forecast in zip(xfuture, yfuture):
    X = logpop.index.values.reshape(-1, 1)
    y = logpop.values
    xfuture = [[2020], [2030]]
    yfuture = m.predict(xfuture)
    yfuture = np.exp(yfuture) / 1000_000_000
    m = LinearRegression()
    





m.fit(X, y)
ypred = m.predict(X)



plt.show()
plt.plot(X, ypred)
plt.plot(X, y)

#X = logpop.index.values.reshape(-1, 1)

print("R-squared: ", m.score(X, y))
print(f"population forecast for {year}: {forecast:5.1f} bln")
print("intercept: ", m.intercept_)
print("slope    : ", m.coef_[0])
