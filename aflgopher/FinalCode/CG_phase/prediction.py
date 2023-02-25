import os
import numpy as np

from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.models import Sequential

import matplotlib.pyplot as plt
import traverseCG

import argparse

def data_transfer(file):

    data_list = []
    with open(file, 'r') as f:
        for line in f.readlines():
            if '----' not in line:
                data_list.append(line.strip())

    return data_list

def func_to_token(data):

    token_dict = {}

    for i in range(len(data)):
        token_dict[data[i]] = i

    return token_dict

def generate_sequence(trace, token):

    trace_dir = os.listdir(trace)
    trace_list =[]

    for i in trace_dir:
        token_trace = []
        original_trace = data_transfer(trace + '/' + i)

        if original_trace != []:
            # print(trace + '/' + i)
            for j in original_trace:
                token_trace.append(token[j])

            trace_list.append(token_trace)

        # TODO： Large dataset
        # if int(i) < 1073237:
        #     token_trace = []
        #     original_trace = data_transfer(trace + '/' + i)
        #
        #     if original_trace != []:
        #         # print(trace + '/' + i)
        #         for j in original_trace:
        #             token_trace.append(token[j])
        #
        #         trace_list.append(token_trace)

    return trace_list

def sequence_quota(data, index=None):

    if index == "sequence":
        len_list = []
        for i in data:
            len_list.append(len(i))

        return max(len_list), min(len_list), np.mean(len_list)

    else:
        pass

def pad_seq(sequence, max_length=1000):

    input_sequence = np.array(pad_sequences(sequence, maxlen=max_length, padding='pre'))

    return input_sequence

def plot_graphs(model, category):
    plt.plot(model.history[category])
    plt.xlabel("Epochs")
    plt.ylabel(category)
    plt.show()

def mask_prediction(token,dot_file):

    G, _ = traverseCG.load_graphs(dot_file)
    suc_dict = traverseCG.get_successors(G)

    func_num = len(token.keys())
    mask = np.zeros((func_num,func_num))

    for k, v in suc_dict.items():
        # if k == 'xmlFreeMutex':
        #     print(v)
        # calculate row number
        if k == 'main':
            row = token['xmllint.c main']
        else:
            for i in token.keys():
                if k == i.split()[-1]:
                    row = token[i]

        # calculate column
        for suc in v:
            for t in token.keys():
                if suc == t.split()[-1]:
                    # if row == 1602:
                    #     print(t.split()[-1])
                    col = token[t]
                    mask[row,col] = 1

    # # TODO: Test the Mask
    # print(mask[4])
    # index = 0
    # for i in range(func_num):
    #     if mask[4][i] != 0:
    #         index += 1
    # print(index)

    return mask, suc_dict

def training(seq, func_num, max_sequence_len=1000):
    # create feature and label
    xs, labels = seq[:, :-1], seq[:, -1]
    ys = tf.keras.utils.to_categorical(labels, num_classes=func_num)

    seed = 10
    xs_train, xs_test, ys_train, ys_test = train_test_split(xs, ys, test_size=0.2, random_state=seed)

    #implement model
    # model = Sequential()
    # model.add(Embedding(func_num, 100, input_length=max_sequence_len - 1))
    # model.add(Bidirectional(LSTM(150)))
    # model.add(Dense(func_num, activation='softmax'))
    # adam = Adam(lr=0.01)
    # model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])
    # history = model.fit(xs, ys, epochs=50, verbose=1)
    # print(model.summary())
    # print(model)

    model = Sequential()
    model.add(Embedding(func_num, 25, input_length=max_sequence_len-1))
    model.add(LSTM(150, return_sequences=True))
    model.add(LSTM(150))
    model.add(Dense(150, activation='relu'))

    model.add(Dense(func_num, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.summary()

    model.fit(xs_train, ys_train, epochs=3, verbose=1, validation_data=(xs_test, ys_test))
    print(model)
    model.save('saved_model/first_model.h5')

    # TODO: TEST1
    # print(token_trace[17])
    # for _ in range(1):
    #     token_list = token_trace[17]
    #     token_list = pad_seq([token_list])
    #     predicted_x = model.predict(token_list[:, :-1], verbose=0)
    #     print(predicted_x)
    #     print(len(predicted_x[0]))
    #     predicted = np.argmax(predicted_x, axis=1)[0]
    #     output_word = ""
    #     # for word, index in token.items():
    #     #     if index == predicted:
    #     #         output_word = word
    #     #         break
    #     token_trace[17][-1] = predicted
    #
    # print(token_trace[17])

    # # TODO: TEST2
    # test_list = [4,0]
    # for _ in range(1):
    #     token_list = pad_seq([test_list])
    #     predicted_x = model.predict(token_list[:, :-1], verbose=0)
    #     print(predicted_x[0])
    #     print(len(predicted_x[0]))
    #     predicted = np.argmax(predicted_x, axis=1)[0]
    #     output_word = ""
    #     # for word, index in token.items():
    #     #     if index == predicted:
    #     #         output_word = word
    #     #         break
    #     test_list[-1] = predicted
    #
    # print(test_list)

    return model

def incremental_training(model, seq, func_num):

    model.summary()

    xs, labels = seq[:, :-1], seq[:, -1]
    ys = tf.keras.utils.to_categorical(labels, num_classes=func_num)

    seed = 10
    xs_train, xs_test, ys_train, ys_test = train_test_split(xs, ys, test_size=0.2, random_state=seed)

    model.fit(xs_train, ys_train, epochs=3, verbose=1, validation_data=(xs_test, ys_test))
    print(model)
    model.save('saved_model/first_model.h5')

    return model

def prediction(model, mask, pre_seq):

    # mask = mask_prediction(token, dot_file)

    token_list = pad_seq([pre_seq], max_length=999)
    predicted_x = model.predict(token_list, verbose=0)
    # print(predicted_x[0])
    # print(len(predicted_x[0]))
    row = pre_seq[-1]
    temp_mask = mask[row]
    # predicted = np.argmax(predicted_x, axis=1)[0]
    result = predicted_x * temp_mask


    return result

def mapping(dict, val):
    key = ""
    for k, v in dict.items():
        if v == val:
            key = k
    return key

def get_edge(model, token):

    CG_edge = {}

    for k, v in token.items():
        # # TODO: TEST
        # if v == 4:
        #     single_node_dist = {}
        #
        #     temp = [v]
        #     # predict_result = prediction(model, mask, token_trace[17][:-1])
        #     predict_result = prediction(model, mask, temp)
        #
        #     # print(np.argmax(predict_result, axis=1)[0])
        #     print(predict_result)
        #     total_prob = np.sum(predict_result[0])
        #
        #     non_zero_count = np.count_nonzero(predict_result[0])
        #
        #     for i in range(len(predict_result[0])):
        #         if predict_result[0][i] != 0:
        #             distance = predict_result[0][i] / total_prob
        #             key = mapping(token, i)
        #             if 1 / distance >= 1000:
        #                 # print("{} -> {} = {}".format(k.split()[1], key.split()[1], 1000))
        #                 single_node_dist[key.split()[1]] = 1000
        #             else:
        #                 # print("{} -> {} = {}".format(k.split()[1], key.split()[1], 1 / distance))
        #                 single_node_dist[key.split()[1]] = 1 / distance
        #     # TODO: libxml special
        #     if v == 0:
        #         CG_edge[k] = single_node_dist
        #     else:
        #         CG_edge[k.split()[1]] = single_node_dist
        #     # print(CG_edge)

        single_node_dist = {}

        temp = [v]
        # predict_result = prediction(model, mask, token_trace[17][:-1])
        predict_result = prediction(model, mask, temp)

        # print(np.argmax(predict_result, axis=1)[0])
        # print(predict_result)
        total_prob = np.sum(predict_result[0])

        non_zero_count = np.count_nonzero(predict_result[0])

        for i in range(len(predict_result[0])):
            if predict_result[0][i] != 0:
                distance = predict_result[0][i] / total_prob
                key = mapping(token, i)
                if 1 / distance >= 1000:
                    # print("{} -> {} = {}".format(k.split()[1], key.split()[1], 1000))
                    single_node_dist[key.split()[1]] = 1000
                else:
                    # print("{} -> {} = {}".format(k.split()[1], key.split()[1], 1 / distance))
                    single_node_dist[key.split()[1]] = 1 / distance
        # TODO: libxml special
        if v == 0:
            CG_edge[k] = single_node_dist
        else:
            CG_edge[k.split()[1]] = single_node_dist
        # print(CG_edge)

    return CG_edge

def dump(CG_edge):
    with open(os.environ.get('TMP_DIR')+'/CG_edge', 'a') as w:
        for k, v in CG_edge.items():
            for k1, v1 in v.items():
                w.write("{} -> {} = {}".format(k, k1, v1))
                w.write('\n')

    w.close()
    print('Finish dumping the weighted CG edges')


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--increment", type=bool, default=False)

    args = parser.parse_args()

    # file = 'func name.txt'
    file = '/home/eval5/Documents/aflgo/FinalCode/CG_phase/func name.txt'
    func_name_list = data_transfer(file)
    print('Total Function Number: {}'.format(len(func_name_list)))

    token = func_to_token(func_name_list)

    incremental_learning = args.increment
    print(incremental_learning)

    if incremental_learning == False:
        # print(token)
        # mask_prediction(token, /home/eval5/Documents/aflgo/FinalCode/CG_phase/newcallgraph.dot)

        # # trace_address = '../trace/ftrace-100k/ftrace'
        # trace_address = '../trace/Copy of ftrace/ftrace'
        # trace_address = '../trace/distill_trace'
        trace_address = '../trace/test_trace'
        token_trace = generate_sequence(trace_address, token)
        print("Total Trace Number: {}".format(len(token_trace)))

        max_length, min_length, mean_length = sequence_quota(token_trace, 'sequence')

        print("Max Length of Sequence: {}".format(max_length))
        print("Min Length of Sequence: {}".format(min_length))
        print("Mean Length of Sequence: {}".format(mean_length))

        input_sequence = pad_seq(token_trace)
        # print(input_sequence[1])

        # print(token_trace[17])
        model = training(input_sequence, len(func_name_list))
        # print(token_trace[17][:-1])
        #
        mask, suc_dict = mask_prediction(token, '/home/eval5/Documents/aflgo/FinalCode/CG_phase/newcallgraph.dot')

        CG_edge = get_edge(model, token)
        dump(CG_edge)
    else:
        trace_address = os.environ.get('IP_DIR')+'/CG'
        token_trace = generate_sequence(trace_address, token)
        print("Total Trace Number: {}".format(len(token_trace)))

        max_length, min_length, mean_length = sequence_quota(token_trace, 'sequence')

        print("Max Length of Sequence: {}".format(max_length))
        print("Min Length of Sequence: {}".format(min_length))
        print("Mean Length of Sequence: {}".format(mean_length))

        input_sequence = pad_seq(token_trace)
        # print(input_sequence[1])

        # print(token_trace[17])
        model_address = '/home/eval5/Documents/aflgo/FinalCode/CG_phase/saved_model/first_model.h5'
        model = tf.keras.models.load_model(model_address)
        new_model = incremental_training(model, input_sequence, len(func_name_list))
        # print(token_trace[17][:-1])
        #
        mask, suc_dict = mask_prediction(token, '/home/eval5/Documents/aflgo/FinalCode/CG_phase/newcallgraph.dot')

        CG_edge = get_edge(model, token)
        dump(CG_edge)



