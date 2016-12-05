from sklearn import linear_model
from util import utility as u
import mord as m

class OrdinalRegression:
    def __init__(self):
        self.c = m.OrdinalRidge()

    def fit(self, X, Y):
        self.c.fit(X, Y)

    def accuracy_and_error(self, X, Y):
        error_val = 0
        prediction_match_count = 0
        for i in range(0,X.shape[0]-1):
          predicted_review_result = self.c.predict(X[i,:].reshape(1, -1));
          actual_review_result = Y[i,0];
          if u.convert_y_to_discrete_output(predicted_review_result) == actual_review_result:
            prediction_match_count += 1
          error_val += (predicted_review_result - actual_review_result)**2;
        error_val /= X.shape[0];
        accuracy = prediction_match_count/X.shape[0]
        return (error_val, accuracy)