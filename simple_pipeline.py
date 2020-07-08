# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute


# %%
# load feature matrix
X_min = pd.read_hdf('trial_data/0_0315_4_electrodes_min.h5')
X_eff = pd.read_hdf('trial_data/0_0315_4_electrodes_eff.h5')

# load target dataframe
y = pd.read_hdf('trial_data/0_0315_4_electrodes_y.h5')
y = y.drop_duplicates()
y = y.set_index('window_id')
y = y.T.squeeze()
y = y.sort_index(0)


# %%
impute(X_min)
impute(X_eff)
X_min_filt = select_features(X_min, y)
X_eff_filt = select_features(X_eff, y)


# %%
X_eff_train, X_eff_test, y_train, y_test = train_test_split(X_eff_filt, y, test_size=.4)
X_min_train, X_min_test, y_train, y_test = train_test_split(X_min_filt, y, test_size=.4)


# %%
tree_eff = DecisionTreeClassifier()
tree_eff.fit(X_eff_train, y_train)
print(classification_report(y_test, tree_eff.predict(X_eff_test)))


# %%
tree_min = DecisionTreeClassifier()
tree_min.fit(X_min_train, y_train)
print(classification_report(y_test, tree_min.predict(X_min_test)))


# %%
X_min_filt.head()