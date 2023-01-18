import math
import numpy as np
import pandas as pd
import seaborn as sns
from seaborn import countplot
from warnings import simplefilter
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure, show
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def TitanicPrediction():
    # Step 1 : Load Data

    simplefilter(action='ignore', category=FutureWarning)
    titanic_data = pd.read_csv('MarvellousTitanicDataset.csv')

    print("First 5 entries from loaded dataset")
    print(titanic_data.head())

    print("Number of passengers are "+str(len(titanic_data)))

    # Step 2 : Analyze data
    print("Visualization : Survived and non survived passengers")
    figure()
    target = "Survived"

    countplot(data = titanic_data, x =target).set_title("Survived and non survived passengers")
    show()

    print("Visualization : Survived and non survived passengers based on gender")
    figure()
    target = "Survived"

    countplot(data = titanic_data, x = target, hue = "Sex").set_title("Survived and non survived passengers based on gender")
    show()

    print("Visualization : Survived and non survived passengers based on passenger class")
    figure()
    target = "Survived"

    countplot(data=titanic_data, x=target, hue="Pclass").set_title("Survived and non survived passengers based on passenger class")
    show()

    print("Visualization : Survived and non survived passengers based on Age")
    figure()
    target = "Survived"

    titanic_data["Age"].plot.hist().set_title("Survived and non survived passengers based on Age")
    show()

    print("Visualization : Survived and non survived passengers based on Fare")
    figure()
    target = "Survived"

    titanic_data["Fare"].plot.hist().set_title("Survived and non survived passengers based on Fare")
    show()

    # Step 3 : Data Cleaning
    titanic_data.drop("zero", axis = 1, inplace = True)

    print("First 5 entries from loaded dataset after removing zero column")
    print(titanic_data.head(5))

    print("Values of Sex Column")
    print(pd.get_dummies(titanic_data["Sex"]))

    print("Values of Sex column after removing one field")
    Sex = pd.get_dummies(titanic_data["Sex"],drop_first = True)
    print(Sex.head(5))

    print("Values of Pass column after removing one field")
    Pclass = pd.get_dummies(titanic_data["Pclass"], drop_first = True)
    print(Pclass.head(5))

    print("Values of data set after concatenating new columns")
    titanic_data = pd.concat([titanic_data, Sex, Pclass], axis = 1)
    print(titanic_data.head(5))

    print("Values of data set after removing irrelevant columns")
    titanic_data.drop(["Sex","sibsp","Parch","Embarked"], axis = 1, inplace = True)
    print(titanic_data.head(5))

    x = titanic_data.drop("Survived", axis = 1)
    y = titanic_data["Survived"]

    # Step 4 : Data Training
    xtrain, xtest, ytrain, ytest = train_test_split(x,y,random_state = 42,test_size = 0.85)

    logmodel = LogisticRegression(max_iter = 1000)
    logmodel.fit(xtrain,ytrain)

    # Step 5 : Data Testing
    prediction = logmodel.predict(xtest)

    # Step 6 : Calculate Accuracy
    print("Classification report of Logistic Regression is :")
    print(classification_report(ytest, prediction))

    print("Confusion Matrix of Logistic Regression is :")
    print(confusion_matrix(ytest, prediction))

    print("Accuracy of Logistic Regression is :")
    print(accuracy_score(ytest, prediction))

    # Create classifier object for Ensemble learning technique
    #log_clf = LogisticRegression(max_iter=1000)
    rnd_clf = RandomForestClassifier()
    knn_clf = KNeighborsClassifier()

    vot_clf = VotingClassifier(estimators=[('rnd', rnd_clf), ('knn', knn_clf)], voting='hard')

    vot_clf.fit(xtrain, ytrain)

    pred = vot_clf.predict(xtest)

    print("Accuracy Score using Ensemble learning techniques")

    print("Accuracy : ", accuracy_score(ytest, pred) * 100)

def main():
    print("Supervised Machine Learning")
    print("Logistic Regression on Titanic Data Set")
    TitanicPrediction()

if __name__ == "__main__":
    main()