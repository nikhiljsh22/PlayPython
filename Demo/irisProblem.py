from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
import mglearn
import matplotlib.pyplot as plt

iris_dataset = load_iris()
print("keys in dataset: \n{}", iris_dataset.keys())
#print(iris_dataset['DESCR'][:100])
#print(iris_dataset["target_names"])
#print("iris data: \n{}", iris_dataset["data"])
print(type(iris_dataset["data"]))
print(iris_dataset["data"].shape)
print(iris_dataset["data"][:5])
print(iris_dataset["target"])
X_train, X_test, Y_train, Y_test = train_test_split(iris_dataset["data"], iris_dataset["target"], random_state=0)
print("x_train shape:", X_train.shape)
print("y_train shape:", Y_train.shape)
print("x_test shape:", X_test.shape)
print("y_test shape:", Y_test.shape)
print(iris_dataset.feature_names)
iris_data_frm = pd.DataFrame(X_train, columns=iris_dataset.feature_names)
pd.plotting.scatter_matrix(iris_data_frm, c=Y_train, figsize=(15, 15),
                           marker='o', hist_kwds={'bins': 20}, s=50,
                           alpha=.8, cmap=mglearn.cm3)
plt.plot()