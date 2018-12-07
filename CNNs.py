#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 17:52:47 2018

@author: kiyoshitaro
"""





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 02:04:25 2018

@author: kiyoshitaro
"""

import os
#import zipfile
import pandas as pd
import numpy as np
import time
import tensorflow as tf


begin = time.time()
unlabeled_train_data = pd.read_csv(os.path.join(os.path.dirname('__file__'),'data','unlabeledTrainData.tsv'),header=0,
                    delimiter="\t", quoting=3)
train_data = pd.read_csv(os.path.join(os.path.dirname('__file__'),'data','labeledTrainData.tsv'),header=0,
                    delimiter="\t", quoting=3)

test_data = pd.read_csv(os.path.join(os.path.dirname('__file__'),'data','testData.tsv'),header=0,
                    delimiter="\t", quoting=3)
print("Review : ", train_data["review"][0])


test_review_vect = pd.read_pickle("data/test_review_vect_200.pickle")[0]
train_review_vect = pd.read_pickle("data/train_review_vect_200.pickle")[0]
train_labels = train_data["sentiment"]

sent_length = len(test_review_vect[0])
word_vect_length = len(test_review_vect[0][0])
num_classes = 2
filter_sizes = [3,5,7] 
batch_size = 32


graph = tf.Graph()
with graph.as_default():
    
    tf_train_sents = tf.placeholder(shape = [batch_size, sent_length,word_vect_length], dtype = tf.float32)
    tf_train_labels = tf.placeholder(shape = [batch_size, num_classes], dtype = tf.float32)
    tf_test_sents = tf.constant(test_review_vect)
        
    con_w1 = tf.Variable(tf.truncated_normal(shape = [filter_sizes[0],word_vect_length], dtype = tf.float32))
    con_b1 = tf.Variable(tf.random_uniform(shape = [1], dtype = tf.float32))

    con_w2 = tf.Variable(tf.truncated_normal(shape = [filter_sizes[1],word_vect_length],dtype = tf.float32))
    con_b2 = tf.Variable(tf.random_normal(shape = [1], dtype = tf.float32))

    con_w3 = tf.Variable(tf.truncated_normal(shape=[filter_sizes[2]], dtype = tf.float32))
    con_b3 = tf.Variable(tf.random_normal(shape=[1], dtype = tf.float32))

    fc_w1 = tf.Variable(tf.truncated_normal(shape = [len(filter_sizes),num_classes],dtype = tf.float32))    
    fc_b1 = tf.Variable(tf.random_normal(shape = [num_classes], dtype = tf.float32))


    def model(data)
        conv1 = tf.nn.conv1d(data, con_w1, stride =1 , padding = "SAME") 
        hidden1_1 = tf.nn.relu(conv1 + con_b1)
        conv2 = tf.nn.conv1d(sent_inputs, con_w2, stride =1 , padding = "SAME") 
        hidden1_2 = tf.nn.relu(conv2+ con_b2)
        conv3 = tf.nn.conv1d(sent_inputs, con_w3, stride =1 , padding = "SAME") 
        hidden1_3 = tf.nn.relu(conv3+ con_b3)
        
        hidden2_1 = tf.reduce_mean(hidden1_1,axis = 1)
        hidden2_2 = tf.reduce_mean(hidden1_2,axis = 1)
        hidden2_3 = tf.reduce_mean(hidden1_3,axis = 1)
        
        hidden2 = tf.concat(values = [hidden2_1, hidden2_2, hidden2_3], axis = 1)
        return tf.matmul(hidden2, fc_w1) + fc_b1
    
    logits =  model(tf_test_sents)  
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels = tf_train_labels,logits = logits))
    optimizer = tf.train.MomentumOptimizer(learning_rate=0.01, momentum=0.9).minimize(loss)

    test_predict = tf.argmax(tf.nn.softmax(model(tf_test_sents)))

num_steps = 30

with tf.Session(graph=graph) as session:
  tf.initialize_all_variables().run()
  print('Initialized')
  for step in range(num_steps):
    offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
    batch_data = train_review_vect[offset:(offset + batch_size), :, :, :]
    batch_labels = train_labels[offset:(offset + batch_size), :]
    feed_dict = {tf_train_sents : batch_data, tf_train_labels : batch_labels}
    _, l, predictions = session.run(
      [optimizer, loss, test_predict], feed_dict=feed_dict)
    if (step % 50 == 0):
      print('Minibatch loss at step %d: %f' % (step, l))

#train_gen = BatchGenerator(batch_size,train_questions,train_labels)
#test_gen = BatchGenerator(batch_size,test_questions,test_labels)

#with tf.Session(graph= graph) as session:
#    for step in range(num_steps):
#        avg_loss = []
#        for tr_i in range((len(train_review_clear)//batch_size) -1 ):
##            tr_inputs, tr_labels = train_gen.generate_batch()
#            l,_ = session.run([loss, optimizer], feed_dict = {tf_train_sent:tr_inputs, tf_train_label:tr_labels, tf_test_sent:})
#            avg_loss.append(l)
#            
#        print("Train loss ar epoch: ", step , " : " , np.mean(avg_loss))









#def cal_distribute_num_word(array_list_words):
#    length = [len(array_list_words[i]) for i in range(len(array_list_words))]
#    mat = np.zeros(max(length))
#    for i in range(len(length)):
#        mat[length[i]-1] = mat[length[i]-1] + 1
#    return mat
#
#distr_words_test = cal_distribute_num_word(test_review_clear)
#distr_words_train = cal_distribute_num_word(train_review_clear)
#distr_words_all = cal_distribute_num_word(all_review_clear)
#
#max_sent_length = 200
#for i in range(len(train_review_clear)):
#    train_review_clear[i] = train_review_clear[i][:max_sent_length]
##    for _ in range(max_sent_length - len(train_review_clear[i])):
##        train_review_clear[i].append("pad")
#
#for i in range(len(test_review_clear)):
#    test_review_clear[i] = test_review_clear[i][:max_sent_length]
##    for _ in range(max_sent_length - len(test_review_clear[i])):
##        test_review_clear[i].append("pad")
#


#        
#def build_dataset(data):
#    words = []
#    data_list = []
#    count = []
#    
#    for sent in data:
#        words.extend(sent)
#    print("Length words: ", len(words))
#    
#    count.extend(collections.Counter(words).most_common())
#    dictionary = dict()
#    for w, _ in count:
#        dictionary[w] = len(dictionary)
#    for sent in data:
#        tmp = list()
#        for word in sent: 
#            index = dictionary[word]
#            tmp.append(index)
#        
#        data_list.append(tmp)
#    
#    reverse_dictionary = dict(zip(dictionary.values(),dictionary.keys()))
#    
#    return data_list, count , dictionary, reverse_dictionary
#
#review_index , count , dictionary , reverse_dictionary = build_dataset(all_review_clear)
#filter_sizes = [3,5,7] 
#sent_length = max_sent_length
#batch_size = 32
#num_classes = 2
#dictionary_size = len(dictionary)
#
#
#all_labels = [0,1] 

#class BatchGenerator(object):
#    '''
#    Generates a batch of data
#    '''
#    def __init__(self,batch_size,questions,labels):
#        self.questions = questions
#        self.labels = labels
#        self.text_size = len(questions)
#        self.batch_size = batch_size
#        self.data_index = 0
#        assert len(self.questions)==len(self.labels)
#        
#    def generate_batch(self):
#        '''
#        Data generation function. This outputs two matrices
#        inputs: a batch of questions where each question is a tensor of size
#        [sent_length, vocabulary_size] with each word one-hot-encoded
#        labels_ohe: one-hot-encoded labels corresponding to the questions in inputs
#        '''
#        global sent_length,num_classes
#        global dictionary, all_labels
#        
#        # Numpy arrays holding input and label data
#        inputs = np.zeros((self.batch_size,sent_length,dictionary_size),dtype=np.float32)
#        labels_ohe = np.zeros((self.batch_size,num_classes),dtype=np.float32)
#        
#        # When we reach the end of the dataset
#        # start from beginning
#        if self.data_index + self.batch_size >= self.text_size:
#            self.data_index = 0
#            
#        # For each question in the dataset
#        for qi,que in enumerate(self.questions[self.data_index:self.data_index+self.batch_size]):
#            # For each word in the question
#            for wi,word in enumerate(que): 
#                # Set the element at the word ID index to 1
#                # this gives the one-hot-encoded vector of that word
#                inputs[qi,wi,dictionary[word]] = 1.0
#            
#            # Set the index corrsponding to that particular class to 1
#            labels_ohe[qi,all_labels.index(self.labels[self.data_index + qi])] = 1.0
#        
#        # Update the data index to get the next batch of data
#        self.data_index = (self.data_index + self.batch_size)%self.text_size
#            
#        return inputs,labels_ohe
#    
#    def return_index(self):
#        # Get the current index of data
#        return self.data_index
#
## Test our batch generator
#sample_gen = BatchGenerator(batch_size,train_review_clear,train_data_raw["sentiment"])
## Generate a single batch
#sample_batch_inputs,sample_batch_labels = sample_gen.generate_batch()
## Generate another batch
#sample_batch_inputs_2,sample_batch_labels_2 = sample_gen.generate_batch()
#
## Make sure that we infact have the question 0 as the 0th element of our batch
#assert np.all(np.asarray([dictionary[w] for w in train_questions[0]],dtype=np.int32) 
#              == np.argmax(sample_batch_inputs[0,:,:],axis=1))
#
# Print some data labels we obtained
#print('Sample batch labels')
#print(np.argmax(sample_batch_labels,axis=1))
#print(np.argmax(sample_batch_labels_2,axis=1))


        
        
