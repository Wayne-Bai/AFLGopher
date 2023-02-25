import pandas as pd
import numpy as np
import tensorflow.compat.v1 as tf
import sys
import argparse
# file = 'global'
# file = 'function'
# file = 'argument'

parser = argparse.ArgumentParser()
parser.add_argument("--category", default=None)

args = parser.parse_args()

file = args.category

if file == 'global':
    data = pd.read_csv('global.csv')
    # print(data.shape)
elif file == 'function':
    data = pd.read_csv('function.csv')
elif file == 'argument':
    data = pd.read_csv('argument.csv')
else:
    print('Please provide correct category')
    sys.exit(0)

data = data['combination']
# print(data.head)

messages = data.to_frame()
# print(data.info)
# print(data['combination'][0])

frame_row, frame_col = messages.shape

corpus = set()

for i in range(frame_row):
    corpus.add(messages['combination'][i].replace('\t',' '))

# print(corpus)
# print(len(corpus))

words = []
for text in corpus:
    for word in text.split(' '):
        if word != '':
            words.append(word)

words = set(words)
words = list(words)
# print(words)
# print(len(words))

# TODO: Generating Input
word2int = {}

for i, word in enumerate(words):
    word2int[word] = i

sentences = []
for sentence in corpus:
    sentences.append(sentence.split())

WINDOW_SIZE = 4

new_data = []
for sentence in sentences:
    for idx, word in enumerate(sentence):
        for neighbor in sentence[max(idx - WINDOW_SIZE, 0): min(idx + WINDOW_SIZE, len(sentence)) + 1]:
            if neighbor != word:
                new_data.append([word, neighbor])

df = pd.DataFrame(new_data, columns=['input', 'label'])
# print(df.head(10))
# print(df.shape)

# TODO: Tensorflow Graph
ONE_HOT_DIM = len(words)

# function to convert numbers to one hot vectors
def to_one_hot_encoding(data_point_index):
    one_hot_encoding = np.zeros(ONE_HOT_DIM)
    one_hot_encoding[data_point_index] = 1
    return one_hot_encoding

X = []  # input word
Y = []  # target word

for x, y in zip(df['input'], df['label']):
    X.append(to_one_hot_encoding(word2int[x]))
    Y.append(to_one_hot_encoding(word2int[y]))

# convert them to numpy arrays
X_train = np.asarray(X)
Y_train = np.asarray(Y)


tf.disable_v2_behavior()
# making placeholders for X_train and Y_train
x = tf.placeholder(tf.float32, shape=(None, ONE_HOT_DIM))
y_label = tf.placeholder(tf.float32, shape=(None, ONE_HOT_DIM))

EMBEDDING_DIM = 8

# hidden layer: which represents word vector eventually
W1 = tf.Variable(tf.random_normal([ONE_HOT_DIM, EMBEDDING_DIM]))
b1 = tf.Variable(tf.random_normal([1]))  # bias
hidden_layer = tf.add(tf.matmul(x, W1), b1)

# output layer
W2 = tf.Variable(tf.random_normal([EMBEDDING_DIM, ONE_HOT_DIM]))
b2 = tf.Variable(tf.random_normal([1]))
prediction = tf.nn.softmax(tf.add(tf.matmul(hidden_layer, W2), b2))

# loss function: cross entropy
loss = tf.reduce_mean(-tf.reduce_sum(y_label * tf.log(prediction), axis=[1]))

# training operation
train_op = tf.train.GradientDescentOptimizer(0.05).minimize(loss)

sess = tf.Session()
init = tf.global_variables_initializer()
sess.run(init)

iteration = 500
for i in range(iteration):
    # input is X_train which is one hot encoded word
    # label is Y_train which is one hot encoded neighbor word
    sess.run(train_op, feed_dict={x: X_train, y_label: Y_train})
    if i % 25 == 0:
        print('iteration ' + ' loss is : ', sess.run(loss, feed_dict={x: X_train, y_label: Y_train}))

# Now the hidden layer (W1 + b1) is actually the word look up table
vectors = sess.run(W1 + b1)
# print(vectors)

vec = pd.DataFrame(vectors)
# print(vec)

# print(messages.head())
sentences = []
for msg in messages['combination']:
    if msg.replace('\t',' ') != '':
        sentences.append(msg.replace('\t',' '))

# print(type(sentences[0]))

# print(type(words))
len_words = len(words)
print(len_words)

dict_words = {}
for i in range(len_words):
    dict_words[words[i]] = list(vec.iloc[i, :])
# print(type(dict_words["end"]))

#TODO: calculating mean of vectors
list_final = []
for text in sentences:
    temp = text.split(' ')
    lt = []
    for s in temp:
        if s != '':
            lt.append(dict_words[s])
    npat = np.array(lt)
    t = np.mean(npat, axis=0).tolist()
    list_final.append(t)
# print(list_final)

cl_input = pd.DataFrame(list_final)
print(cl_input.shape)

if file == 'global':
    cl_input.to_csv('global_input.csv', index=False)
elif file == 'function':
    cl_input.to_csv('function_input.csv', index=False)
else:
    cl_input.to_csv('argument_input.csv', index=False)








# print(data.head)

