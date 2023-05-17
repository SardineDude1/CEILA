import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.layers import Input, Embedding, Dense, concatenate
from keras.models import Model,  load_model
import tensorflow as tf
import os

cwd = os.getcwd()

# Set the variable containing the filename of the testing data
filename = ''

# Set the path to the file directory
f1 = cwd + "\\DATA_SETS\\CLEAN\\TRAINING_DATA\\" + filename

# Load data from CSV file
df = pd.read_csv(f1, delimiter='|')

# Remove rows with missing values
df.dropna(inplace=True)

# Separate the features and target variable
text1 = df['GENRE']
text2 = df['PUBLISHER']
int_col = df['NUM LINKING FIELDS']
float_col = df['PRICE']
target = df['VALUE RATING']

# Tokenize text data
tokenizer = Tokenizer(num_words=1298)   # This is usually the culprit an out of bounds error
tokenizer.fit_on_texts(text1)
tokenizer.fit_on_texts(text2)
text1_seq = tokenizer.texts_to_sequences(text1)
text2_seq = tokenizer.texts_to_sequences(text2)

# Pad sequences
text1_seq = pad_sequences(text1_seq, maxlen=100)
text2_seq = pad_sequences(text2_seq, maxlen=100)

# Convert int_col to numeric values and replace non-numeric characters with 0
int_col = pd.to_numeric(int_col, errors='coerce')
int_col.fillna(0, inplace=True)
int_col = int_col.astype(int)

# Assign the testing varaibles
# Split the data into training and testing sets
text1_test, text2_test, int_test, float_test, y_test = text1_seq, text2_seq, int_col, float_col, target

# Load the Model
CEILA_NN = load_model("CEILA_MODELS\\CEILA_NN.h5")

#CEILA_NN.summary()
print(type(float_test))
# Test the Model's accuracy against new data
test_loss, test_acc = CEILA_NN.evaluate([text1_test, text2_test, int_test.to_numpy().reshape(-1, 1), float_test.to_numpy().reshape(-1, 1)], tf.keras.utils.to_categorical(y_test-1, num_classes=3))

# Print the loss and accuracy ratings
print('Test Loss:', test_loss)
print('Test Accuracy:', test_acc)
