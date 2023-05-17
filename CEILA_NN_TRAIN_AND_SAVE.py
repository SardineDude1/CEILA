import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.layers import Input, Embedding, Dense, concatenate
from keras.models import Model
import tensorflow as tf
import os

cwd = os.getcwd()

# Set the variable containing the filename of the training data
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
tokenizer = Tokenizer(num_words=5000)
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

# Split the data into training and testing sets
text1_train, text1_test, text2_train, text2_test, int_train, int_test, float_train, float_test, y_train, y_test = train_test_split(text1_seq, text2_seq, int_col, float_col, target, test_size=0.2)

# Define the input layers
input1 = Input(shape=(100,))
input2 = Input(shape=(100,))
input3 = Input(shape=(1,))
input4 = Input(shape=(1,))

# Define the embedding layer for text input
embedding_layer = Embedding(len(tokenizer.word_index) + 1,
                            100,
                            input_length=100)

# Define the text input layers
embedded_input1 = embedding_layer(input1)
embedded_input2 = embedding_layer(input2)

# Merge the text input layers
merged_layer = concatenate([embedded_input1, embedded_input2])

# Flatten the merged layer
flatten_layer = tf.keras.layers.Flatten()(merged_layer)

# Merge the flattened text input with the numeric input
merged_layer = concatenate([flatten_layer, input3, input4])

# Define the output layer
output = Dense(3, activation='softmax')(merged_layer)

# Define the model with four inputs and one output
model = Model(inputs=[input1, input2, input3, input4], outputs=output)

# Define the optimizer for the nerual network
opitmizer = tf.keras.optimizers.Adam(learning_rate=0.0001)

# Compile the model with categorical_crossentropy loss and adam optimizer
model.compile(loss='categorical_crossentropy', optimizer=opitmizer, metrics=['accuracy'])

# Print the model archetecture
model.summary()

# Train the model on the training data
history = model.fit([text1_train, text2_train, int_train.to_numpy().reshape(-1, 1), float_train.to_numpy().reshape(-1, 1)],
                    tf.keras.utils.to_categorical(y_train-1, num_classes=3), 
                    epochs=75, batch_size=32, verbose=1)

# Evaluate the model on test data
test_loss, test_acc = model.evaluate([text1_test, text2_test, int_test.to_numpy().reshape(-1, 1), float_test.to_numpy().reshape(-1, 1)],
                                     tf.keras.utils.to_categorical(y_test-1, num_classes=3))
print('Test accuracy:', test_acc)
print('Test loss:', test_loss)

model.save("CEILA_NN.h5")