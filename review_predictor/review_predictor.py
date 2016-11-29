from pprint import pprint
import numpy as np
import itertools
from util import utility as u
from sklearn import linear_model
import mord as m
from data_model import user as user_module
from data_model import review as review_module
from data_model import business as business_module

np.set_printoptions(threshold=np.nan)
USER_DATA_SET_FILE_PATH = 'data_set/yelp_academic_dataset_user.json';
BUSINESS_DATA_SET_FILE_PATH = 'data_set/yelp_academic_dataset_business_restaurants_only.json';
# REVIEW_DATA_SET_FILE_PATH = 'data_set/yelp_academic_dataset_review.json';
REVIEW_DATA_SET_FILE_PATH = 'data_set/yelp_academic_dataset_review_test.json';


TRAINING_DATA_SET_SIZE = 4000;
TEST_DATA_SET_SIZE = 4000;
TOTAL_DATA_SET_SIZE = TRAINING_DATA_SET_SIZE + TEST_DATA_SET_SIZE;
FEATURE_SIZE = 45;

print('Started loading business data set. Step 1/6');
business = business_module.Business(BUSINESS_DATA_SET_FILE_PATH);
# business.generateHistogram();
print('Finished loading business data set. Step 1/6');


print('Started loading review data set. Step 2/6');
review = review_module.Review(REVIEW_DATA_SET_FILE_PATH, business.getBusinessDataDict());
# review.generateStarsHistogram();
print('Finished loading review data set. Step 2/6');
print('Total restaurant review count after filtering: ' + str(u.count_iterable(review.getReviewData())));


print('Started loading user data set. Step 3/6');
user = user_module.User(USER_DATA_SET_FILE_PATH, review.getUserIdToBusinessIdMap(), business.getBusinessDataDict());
# user.generateStarsHistogram();
print('Finished loading user data set. Step 3/6');


print('Started constructing X,Y data matrix. Step 4/6');


all_review_data = [];

for i,review_data_entry in enumerate(review.getReviewData()):
	if i < TOTAL_DATA_SET_SIZE:
		all_review_data.append(review_data_entry);
	else:
		break;

print('Total data size: ' + str(u.count_iterable(all_review_data)));

X = np.zeros((len(all_review_data), FEATURE_SIZE));
Y = np.zeros((len(all_review_data), 1));
for i,review_data_entry in enumerate(all_review_data):
	user_id = review_data_entry['user_id'];
	user_matrix = user.populate_user_data(user_id);
	business_id = review_data_entry['business_id'];
	business_matrix = business.populate_business_data(user, user_id, business_id);
	# print(user_matrix.shape);
	# print(business_matrix.shape);
	X[i,:] = np.concatenate((user_matrix, business_matrix), axis=1);
	Y[i] = review_data_entry['stars'];

# X_normed = (X - X.mean(axis=0)) / X.std(axis=0); #If we decided to normalize
X_normed = X; #If we decided not to normalize
X_normed=np.ma.compress_cols(np.ma.masked_invalid(X_normed))
print(X_normed.shape)
X_training = X_normed[1:TRAINING_DATA_SET_SIZE,:]
Y_training = Y[1:TRAINING_DATA_SET_SIZE,:]
X_test = X_normed[TRAINING_DATA_SET_SIZE+1:X_normed.shape[0],:]
Y_test = Y[TRAINING_DATA_SET_SIZE+1:X_normed.shape[0],:]
print(X_training.shape)
print(Y_training.shape)
print(X_test.shape)
print(Y_test.shape)

c = m.OrdinalRidge();
c.fit(X_training, Y_training);

error_count = 0;
for i in range(1,X_test.shape[0]):
	Y_predicted = c.predict(X_test[i,:].reshape(1,-1))
	if Y_predicted != Y_test[i]:
		error_count += 1
		# pprint(str(Y_predicted) + " : " + str(Y_test[i]))
pprint(error_count);

print('Finished constructing X,Y data matrix. Step 4/6');

# print('Started fitting ML model. Step 5/6');
# # Use cross validation to find the appropriate alpha
# model = linear_model.LogisticRegressionCV(
#         Cs=9
#         ,penalty='l2'
#         ,scoring='roc_auc'
#         ,cv=5
#         ,n_jobs=-1
#         ,max_iter=10000
#         ,fit_intercept=True
#         ,tol=10
#     );
# model.fit (X, Y.ravel());
# pprint(model.coef_);
# print('Finished fitting ML model. Step 5/6');

# print('Started predicting using ML model. Step 6/6');
# in_sample_error = 0;
# for i in range(0,TRAINING_DATA_SET_SIZE-1):
# 	predicted_review_result = model.predict(X[i,:].reshape(1, -1));
# 	actual_review_result = Y[i,0];
# 	if i < 50:
# 		print(str(predicted_review_result) + ',' + str(actual_review_result));
# 	in_sample_error += (predicted_review_result - actual_review_result)**2;
# in_sample_error /= TRAINING_DATA_SET_SIZE;
# print('In sample error is: ' + str(in_sample_error));
# print('Mean accuracy: ' + str(model.score(X,Y)));

# out_of_sample_error = 0;
# for i in range(0,TEST_DATA_SET_SIZE-1):
# 	predicted_review_result = model.predict(X_test[i,:].reshape(1, -1));
# 	actual_review_result = Y_test[i,0];
# 	if i < 50:
# 		print(str(predicted_review_result) + ',' + str(actual_review_result));
# 	out_of_sample_error += (predicted_review_result - actual_review_result)**2;
# out_of_sample_error /= TEST_DATA_SET_SIZE;
# print('Out of sample error is: ' + str(out_of_sample_error));
# print('Mean accuracy: ' + str(model.score(X_test,Y_test)));
# print('Finished predicting using ML model. Step 6/6');
