import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


data = pd.read_csv("C:/Users/jpsch/OneDrive/Documents/SeniorProject/sampleCode.csv")


X = data[['team1_avg_points', 'team2_avg_points']]
X = X.values
y = data[['team1_points', 'team2_points']]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)


reg = LinearRegression().fit(X_train, y_train)


y_pred = reg.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
print("Mean Squared Error:", mse)


new_game = np.array([[75, 70]])
predicted_score = reg.predict(new_game)
print("Predicted Score:", predicted_score[0])


#%%
