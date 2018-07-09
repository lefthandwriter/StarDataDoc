"""
Trains a feed-forward neural network using extracted state-action pair information.

"""


from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras import optimizers, losses, activations
from keras.layers import Dense, Input
from keras import regularizers
from keras.models import Sequential
from keras.utils.np_utils import to_categorical

import numpy as np
import matplotlib.pyplot as plt

id2unit = [ 
	("Terran_Marine", "0", "120", "50", "0", "1", "0", "32", "64"),
	("Terran_Ghost", "1", "250", "50", "25", "1", "1", "33", "65"),
	("Terran_Vulture", "2", "150", "75", "0", "2", "2", "34", "66"),
	("Terran_Goliath", "3", "200", "100", "50", "2", "3", "35", "67"),
	("Terran_Siege_Tank_Tank_Mode", "5", "250", "150", "100", "2", "4", "36", "68"),
	("Terran_SCV", "7", "100", "50", "0", "1", "5", "37", "69"),
	("Terran_Wraith", "8", "300", "150", "100", "2", "6", "38", "70"),
	("Terran_Science_Vessel", "9", "400", "100", "225", "2", "7", "39", "71"),
	("Terran_Dropship", "11", "250", "100", "100", "2", "8", "40", "72"),
	("Terran_Battlecruiser", "12", "665", "400", "300", "6", "9", "41", "73"),
	("Terran_Nuclear_Missile", "14", "300", "200", "200", "8", "10", "42", "74"),					
	("Terran_Firebat", "32", "120", "50", "25", "1", "11", "43", "75"),
	("Terran_Medic", "34", "150", "50", "25", "1", "12", "44", "76"),
	("Terran_Valkyrie", "58", "250", "250", "125", "3", "13", "45", "77"),
	("Terran_Command_Center", "106", "600", "400", "0", "0", "14", "46", "78"),
	("Terran_Comsat_Station", "107", "200", "50", "50", "0", "15", "47", "79"),
	("Terran_Nuclear_Silo", "108", "400", "100", "100", "0", "16", "48", "80"),
	("Terran_Supply_Depot", "109", "200", "100", "0", "0", "17", "49", "81"),
	("Terran_Refinery", "110", "200", "100", "0", "0", "18", "50", "82"),
	("Terran_Barracks", "111", "400", "150", "0", "0", "19", "51", "83"),
	("Terran_Academy", "112", "400", "150", "0", "0", "20", "52", "84"),
	("Terran_Factory", "113", "400", "200", "100", "0", "21", "53", "85"),
	("Terran_Starport", "114", "350", "150", "100", "0", "22", "54", "86"),
	("Terran_Control_Tower", "115", "200", "50", "50", "0", "23", "55", "87"),
	("Terran_Science_Facility", "116", "300", "100", "150", "0", "24", "56", "88"),
	("Terran_Covert_Ops", "117", "200", "50", "50", "0", "25", "57", "89"),
	("Terran_Physics_Lab", "118", "200", "50", "50", "0", "26", "58", "90"),
	("Terran_Machine_Shop", "120", "200", "50", "50", "0", "27", "59", "91"),
	("Terran_Engineering_Bay", "122", "300", "125", "0", "0", "28", "60", "92"),
	("Terran_Armory", "123", "400", "100", "50", "0", "29", "61", "93"),
	("Terran_Missile_Turret", "124", "150", "75", "0", "0", "30", "62", "94"),
	("Terran_Bunker", "125", "150", "100", "0", "0", "31", "63", "95")
]

## Current lowest error: 57.4% train and 61.3% hold with 7 hidden layers, standardization. Num epochs: 82 at 0.4064 acc
def deep_model_1():
	model = Sequential()
	model.add(Dense(32, bias_initializer='zeros', kernel_initializer='glorot_normal',
	activity_regularizer=regularizers.l2(0.0001), input_dim=input_shape))
	model.add(Dense(32, activation=activations.relu))
	model.add(Dense(32, activation=activations.relu))
	model.add(Dense(32, activation=activations.relu))
	model.add(Dense(32, activation=activations.relu))
	model.add(Dense(32, activation=activations.relu))
	model.add(Dense(32, activation=activations.relu))
	model.add(Dense(32, activation=activations.relu))
	model.add(Dense(nclass, activation=activations.softmax))
	opt = optimizers.Adam(lr=0.0001)
	model.compile(optimizer=opt, loss=losses.categorical_crossentropy, metrics=['acc'])
	model.summary()
	return model

## Load States and Actions ##
print("Reading data..")
data = np.loadtxt("StateData/Terran678911.txt")

print("Training model..")
States = data[:,0:102] # with frame number
Actions = data[:,102]
Actions = to_categorical(Actions, num_classes=33) # make actions one-hot vectors

## Plot action distribution
# sum_classes = np.sum(Actions, axis=0)
# plt.bar(range(33), sum_classes); plt.show()

len_train = int(len(States)*0.8)
X_train = States[0:len_train,:]
y_train = Actions[0:len_train,:] # one hot vector
X_test = States[len_train:,:]

y_labels_train = data[0:len_train,102] # single vector
y_labels_test = data[len_train:,102] # single vector


## Standardize features according to training set
## IF we standardize here, need to standardize in the test script too
Xmean = np.mean(X_train, axis=0)
Xstd  = np.std(X_train, axis=0)

# Apply standardization to XTrain
print ('XTrain mean before standardization: ', np.mean(X_train))
for obs in range(len(X_train)):
	for feature in range(X_train.shape[1]-1): ## don't take mean / std of bias term
		X_train[obs][feature] = (X_train[obs][feature] - Xmean[feature]) / Xstd[feature]
print ('XTrain mean after standardization: ', np.mean(X_train))

print ('XTest mean before standardization: ', np.mean(X_test))
# Apply standardization to XTest
for obs in range(len(X_test)):
	for feature in range(X_test.shape[1]-1): ## don't take mean / std of bias term
		X_test[obs][feature]  = (X_test[obs][feature]  - Xmean[feature]) / Xstd[feature]
print ('XTest mean after standardization: ', np.mean(X_test))


# input_shape = (X_train.shape[1], 1) ## change this shape according to the number of input features we have
input_shape = X_train.shape[1]
nclass = 33 ## total number of possible Terran units/buildings 


## Train Model ##
model = deep_model_1()
file_path_weights = "weights.best.hdf5"
checkpoint = ModelCheckpoint(file_path_weights, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
early = EarlyStopping(monitor="val_acc", mode="max", patience=10)
callbacks_list = [checkpoint, early]
history = model.fit(X_train, y_train, validation_split=0.2, epochs=200, shuffle=True, batch_size=100, verbose=2, callbacks=callbacks_list)
model.load_weights(file_path_weights)

## Predict on train set
predicts_train = model.predict(X_train) # gives a one-hot vector
predicts_train = np.argmax(predicts_train, axis=1) # gives the index for the max
# predicts_train = [id2unit[p][0] for p in predicts_train]

## Predict on test set
predicts_test = model.predict(X_test) # gives a one-hot vector
predicts_test = np.argmax(predicts_test, axis=1) # gives the index for the max

# for pred in predicts_train:
# 	if pred == 0.0:
# 		print "Nothing"
# 	else:
# 		print id2unit[int(pred)-1][0]

# for pred in predicts_test:
# 	if pred == 0.0:
# 		print "Nothing"
# 	else:
# 		print id2unit[int(pred)-1][0]


## Check accuracy - train set
count_missclassified = sum(1 for a, b in zip(predicts_train, y_labels_train) if a != b)
per_error = float(count_missclassified) / len(predicts_train) * 100
print("Training Error: %f"%per_error)


## Check accuracy - test set
count_missclassified = sum(1 for a, b in zip(predicts_test, y_labels_test) if a != b)
per_error = float(count_missclassified) / len(predicts_test) * 100
print("Test Error: %f"%per_error)


## Run on one game
datatest = np.loadtxt("StateData/OneGame.txt")
States = datatest[:,0:102]
Actions = datatest[:,102]
X_test = States
y_labels_test = Actions  # single vector
input_shape = X_train.shape[1]

# Apply standardization to XTest based on XTrain mean and std
for obs in range(len(X_test)):
	for feature in range(X_test.shape[1]-1): ## don't take mean / std of bias term
		X_test[obs][feature]  = (X_test[obs][feature]  - Xmean[feature]) / Xstd[feature]
print ('XTest mean after standardization: ', np.mean(X_test))

## Test Model on a new Replay ##
model = deep_model_1()
file_path_weights = "weights.best.hdf5"
model.load_weights(file_path_weights)

## Predict on test set
predicts_test = model.predict(X_test) # gives a one-hot vector
predicts_test = np.argmax(predicts_test, axis=1) # gives the index for the max

# for pred in predicts_test:
# 	if pred == 0.0:
# 		print "Nothing"
# 	else:
# 		print id2unit[int(pred)-1][0]

# for pred in y_labels_test:
# 	if pred == 0.0:
# 		print "Nothing"
# 	else:
# 		print id2unit[int(pred)-1][0]

## Check accuracy - test set
count_missclassified = sum(1 for a, b in zip(predicts_test, y_labels_test) if a != b)
per_error = float(count_missclassified) / len(predicts_test) * 100
print("Test Error: %f"%per_error)

np.savetxt("netpreds.txt", predicts_test)
np.savetxt("nettrues.txt", y_labels_test)

## to do: save the predicts and true for this test game






