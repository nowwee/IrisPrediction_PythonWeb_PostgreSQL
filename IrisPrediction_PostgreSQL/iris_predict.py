from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression


def load_data():
    iris = load_iris()
    X = iris.data
    y = iris.target
    return X, y


def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    return model    


def predict_iris(features):
    X, y = load_data()
    model = train_model(X, y)
    predicted_iris_type = model.predict([features])[0]
    return 'setosa' if predicted_iris_type == 0 else ('versicolor' if predicted_iris_type == 1 else 'virginica')