import numpy as np

import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


# === Create data and simulate results =====


N = 20000
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# === Create data and simulate results =====
x_data = np.random.randn(N,3)
w_real = [0.3, 0.5, 0.1]
b_real = -0.2
wxb = np.matmul(w_real,x_data.T) + b_real
y_data_pre_noise = sigmoid(wxb)
y_data = np.random.binomial(1, y_data_pre_noise)


import tensorflow as tf


NUM_STEPS = 50
g = tf.Graph()
wb_=[]
with g.as_default():
    x = tf.placeholder(tf.float32, shape=[None,3])
    y_true = tf.placeholder(tf.float32, shape=None)

    with tf.name_scope('inference') as scope:
        w = tf.Variable([[0,0,0]], dtype=tf.float32, name='weights')
        b = tf.Variable(0, dtype=tf.float32, name='bias')
        y_pred = tf.matmul(w, tf.transpose(x)) + b
        y_pred = tf.sigmoid(y_pred)

    with tf.name_scope('loss') as scope:
        loss = tf.nn.sigmoid_cross_entropy_with_logits(labels=y_true,logits=y_pred)
        loss = tf.reduce_mean(loss)
    

    with tf.name_scope('train') as scope:
        learning_rate = 0.5
        optimizer = tf.train.GradientDescentOptimizer(learning_rate)
        train = optimizer.minimize(loss)

    # Before starting, initialize the variables.  We will 'run' this first.
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        for step in range(NUM_STEPS):
            sess.run(train, {x: x_data, y_true: y_data})
            if step%5 == 0:
                print(step, sess.run([w,b]))
                wb_.append(sess.run([w,b]))

        print(10, sess.run([w,b]))

print(wb_)
print('#' * 30)
print(w_real, b_real)


