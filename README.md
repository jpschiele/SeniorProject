# SeniorProject
# College Basketball Prediction Model
This repository contains a college basketball prediction model that utilizes linear regression to predict scores and logistic regression to predict win probabilities. The models are trained on historical data and can be used to make predictions for future games.

## Features

- Predicts scores for college basketball games using linear regression.
- Estimates win probabilities for each team using logistic regression.
- Utilizes historical game data to train the models.
- Provides an interface to input game information and get predictions.

## Installation

1. Clone the repository to your local machine:

   ```shell
      git clone https://github.com/jpschiele/SeniorProject.git

2. Install the required dependencies:

   ```shell
      pip install -r requirements.txt

## Usage

  1. Run the prediction model script:

      ```shell
         python userInterface.py

  2. Choose a conference and two teams from that conference to simulate a game.

  3. The model will provide predicted scores and win probabilities for the given game.
  
## Dataset

  The prediction model is trained on a comprehensive dataset of college basketball games. The dataset includes game statistics, offensive and defensive ratings,
  team information, and other relevant features. The dataset is not included in this repository, but can be found at 
  https://console.firebase.google.com/project/schieleproject/overview

## Model Training

  The linear regression and logistic regression models are trained using the scikit-learn library in Python. The training process involves feature selection, data
  preprocessing, and model fitting. Details of the model training can be found in Model.py.
