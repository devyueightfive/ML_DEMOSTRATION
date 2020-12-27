# scientific libs
import numpy as np
import pandas as pd

# file workers
import pickle
import os

# transformers
from sklearn.base import TransformerMixin
from sklearn.preprocessing import StandardScaler, OneHotEncoder, QuantileTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import FunctionTransformer
# classifier
from sklearn.ensemble import RandomForestClassifier



class CategoryTransformer(TransformerMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def fit(self, X):
        return self

    def transform(self, X):
        if (X is not None):
            return [str(x) for x in X]
        else:
            return None

    def fit_transform(self, X, y=None):
        return self.fit(X).transform(X)