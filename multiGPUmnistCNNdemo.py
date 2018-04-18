''' Multi-GPU Training Example.
Train a convolutional neural network on multiple GPU with TensorFlow.
This example is using TensorFlow layers, see 'convolutional_network_raw' example
for a raw TensorFlow implementation with variables.
This example is using the MNIST database of handwritten digits
(http://yann.lecun.com/exdb/mnist/)
Author: Aymeric Damien
Project: https://github.com/aymericdamien/TensorFlow-Examples/
'''

from __future__ import division, print_function, absolute_import

import numpy as np
import tensorflow as tf
import argparse
import os.path
import sys
import time

# Import MNIST data
from tensorflow.examples.tutorials.mnist import input_data

import argparse

mnist = input_data.read_data_sets("/tmp/data4/", one_hot=True)

# Basic model parameters as external flags.
FLAGS = None

# Training Parameters
num_gpus = 2
num_steps = 20000  # this is the parameter to control the step
learning_rate = 0.05
# batch_size = 1024
display_step = 100

eval_batch_size = 100
# eval_total_size = 100 #2000
eval_num_epochs = 1000

##########
# learning_rate=0.01
num_epochs = 1000
batch_size = 100
train_dir = './tmp/data4/'

##########
# Network Parameters
num_classes = 2 # MNIST total classes (0-9 digits)
dropout = 0.75 # Dropout, probability to keep units

import NetStructureV2
IMAGE_PIXELS = NetStructureV2.IMAGE_PIXELS

# Build a convolutional neural network
def conv_net(x, n_classes, dropout, reuse, is_training):
    # Define a scope for reusing the variables
    with tf.variable_scope('ConvNet', reuse=reuse):
        # MNIST data input is a 1-D vector of 784 features (28*28 pixels)
        # Reshape to match picture format [Height x Width x Channel]
        # Tensor input become 4-D: [Batch Size, Height, Width, Channel]
        x = tf.reshape(x, shape=[-1, 330, 165, 3])

        # Convolution Layer with 64 filters and a kernel size of 5
        x = tf.layers.conv2d(x, 64, 5, activation=tf.nn.relu)
        # Max Pooling (down-sampling) with strides of 2 and kernel size of 2
        x = tf.layers.max_pooling2d(x, 11, 11)

        # Convolution Layer with 256 filters and a kernel size of 5
        x = tf.layers.conv2d(x, 256, 5, activation=tf.nn.relu)
        # Convolution Layer with 512 filters and a kernel size of 5
        x = tf.layers.conv2d(x, 512, 2, activation=tf.nn.relu)
        # Max Pooling (down-sampling) with strides of 2 and kernel size of 2
        x = tf.layers.max_pooling2d(x, 5, 5)

        # Flatten the data to a 1-D vector for the fully connected layer
        x = tf.contrib.layers.flatten(x)

        # Fully connected layer (in contrib folder for now)
        x = tf.layers.dense(x, 128)
        # Apply Dropout (if is_training is False, dropout is not applied)
        x = tf.layers.dropout(x, rate=dropout, training=is_training)

        # Fully connected layer (in contrib folder for now)
        x = tf.layers.dense(x, 64)
        # Apply Dropout (if is_training is False, dropout is not applied)
        x = tf.layers.dropout(x, rate=dropout, training=is_training)

        # Output layer, class prediction
        out = tf.layers.dense(x, n_classes)
         # Because 'softmax_cross_entropy_with_logits' loss already apply
        # softmax, we only apply softmax to testing network
        out = tf.nn.softmax(out) if not is_training else out

    return out

def average_gradients(tower_grads):
    average_grads = []
    for grad_and_vars in zip(*tower_grads):
        # Note that each grad_and_vars looks like the following:
        #   ((grad0_gpu0, var0_gpu0), ... , (grad0_gpuN, var0_gpuN))
        grads = []
        for g, _ in grad_and_vars:
            # Add 0 dimension to the gradients to represent the tower.
            expanded_g = tf.expand_dims(g, 0)

            # Append on a 'tower' dimension which we will average over below.
            grads.append(expanded_g)

        # Average over the 'tower' dimension.
        grad = tf.concat(grads, 0)
        grad = tf.reduce_mean(grad, 0)

        # Keep in mind that the Variables are redundant because they are shared
        # across towers. So .. we will just return the first tower's pointer to
        # the Variable.
        v = grad_and_vars[0][1]
        grad_and_var = (grad, v)
        average_grads.append(grad_and_var)
    return average_grads
# By default, all variables will be placed on '/gpu:0'
# So we need a custom device function, to assign all variables to '/cpu:0'
# Note: If GPUs are peered, '/gpu:0' can be a faster option
PS_OPS = ['Variable', 'VariableV2', 'AutoReloadVariable']

def assign_to_device(device, ps_device='/cpu:0'):
    def _assign(op):
        node_def = op if isinstance(op, tf.NodeDef) else op.node_def
        if node_def.op in PS_OPS:
            return "/" + ps_device
        else:
            return device

    return _assign

# Constants used for dealing with the files, matches convert_to_records.
TRAIN_FILE = 'train.tfrecords'
VALIDATION_FILE = 'validation.tfrecords'

def decode(serialized_example):
  features = tf.parse_single_example(
      serialized_example,
      # Defaults are not specified since both keys are required.
      features={
          'image_raw': tf.FixedLenFeature([], tf.string),
          'label': tf.FixedLenFeature([], tf.string), ###label decode!!!!!
      })

  # Convert from a scalar string tensor (whose single string has
  # length mnist.IMAGE_PIXELS) to a uint8 tensor with shape
  # [mnist.IMAGE_PIXELS].
  image = tf.decode_raw(features['image_raw'], tf.uint8)
  image.set_shape(IMAGE_PIXELS)
  # Convert label from a scalar uint8 tensor to an int32 scalar.
  label = tf.decode_raw(features['label'], tf.int32)
  label = tf.cast(label, tf.int32)

  return image, label

def augment(image, label):
  # OPTIONAL: Could reshape into a 28x28 image and apply distortions
  # here.  Since we are not applying any distortions in this
  # example, and the next step expects the image to be flattened
  # into a vector, we don't bother.
  return image, label

def normalize(image, label):
  # Convert from [0, 255] -> [-0.5, 0.5] floats.
  image = tf.cast(image, tf.float32) * (1. / 255) - 0.5

  return image, label

def inputs(train, batch_size, num_epochs):
  """Reads input data num_epochs times.
  Args:
    train: Selects between the training (True) and validation (False) data.
    batch_size: Number of examples per returned batch.
    num_epochs: Number of times to read the input data, or 0/None to
       train forever.
  Returns:
    A tuple (images, labels), where:
    * images is a float tensor with shape [batch_size, mnist.IMAGE_PIXELS]
      in the range [-0.5, 0.5].
    * labels is an int32 tensor with shape [batch_size] with the true label,
      a number in the range [0, mnist.NUM_CLASSES).
    This function creates a one_shot_iterator, meaning that it will only iterate
    over the dataset once. On the other hand there is no special initialization
    required.
  """
  if not num_epochs: num_epochs = None
  filename = os.path.join(train_dir,
                          TRAIN_FILE if train else VALIDATION_FILE)

  with tf.name_scope('input'):
    # TFRecordDataset opens a protobuf and reads entries line by line
    # could also be [list, of, filenames]
    dataset = tf.data.TFRecordDataset(filename)
    dataset = dataset.repeat(num_epochs)

    # map takes a python function and applies it to every sample
    dataset = dataset.map(decode)
    dataset = dataset.map(augment)
    dataset = dataset.map(normalize)

    #the parameter is the queue size
    dataset = dataset.shuffle(1000 + 3 * batch_size)
    dataset = dataset.batch(batch_size)

    iterator = dataset.make_one_shot_iterator()
  return iterator.get_next()

# Place all ops on CPU by default
def main(_):
    with tf.device('/cpu:0'):
        tower_grads = []
        reuse_vars = False

        # # tf Graph input
        # X = tf.placeholder(tf.float32, [None, num_input])
        # Y = tf.placeholder(tf.float32, [None, num_classes])
        image_batch, label_batch = inputs(train=True, batch_size=batch_size,
                           num_epochs=num_epochs)

        #for evalution
        batch_x_eval, batch_y_eval = inputs(train=False, batch_size=eval_batch_size,
                                            num_epochs=eval_num_epochs)
        # Add ops to save and restore all the variables.

        # conv1_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="ConvNet")  # not sure about that
        # saver = tf.train.Saver("ConvNet")  # to save the model

        # Loop over all GPUs and construct their own computation graph
        for i in range(num_gpus):
            with tf.device(assign_to_device('/gpu:{}'.format(i), ps_device='/cpu:0')):

                # # Split data between GPUs
                # _x = X[i * batch_size: (i+1) * batch_size]
                # _y = Y[i * batch_size: (i+1) * batch_size]
                # _x = image_batch[]
                # _y = label_batch[]

                # Because Dropout have different behavior at training and prediction time, we
                # need to create 2 distinct computation graphs that share the same weights.

                # Create a graph for training
                logits_train = conv_net(image_batch, num_classes, dropout,
                                        reuse=reuse_vars, is_training=True)
                # Create another graph for testing that reuse the same weights
                logits_test = conv_net(image_batch, num_classes, dropout,
                                       reuse=True, is_training=False)
                #evaluation
                logits_eval = conv_net(batch_x_eval, num_classes, dropout,
                                       reuse=True, is_training=False)
                # batch_x, batch_y = inputs(train=True, batch_size=batch_size,
                #                           num_epochs=num_epochs)

                # Define loss and optimizer (with train logits, for dropout to take effect)
                loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(
                    logits=logits_train, labels=label_batch))
                optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
                grads = optimizer.compute_gradients(loss_op)

                # Only first GPU compute accuracy
                if i == 0:

                    # Evaluate model (with test logits, for dropout to be disabled)
                    correct_pred_eval = tf.equal(tf.argmax(logits_eval, 0), tf.argmax(batch_y_eval, 0)) #argmax how to use
                    accuracy_eval = tf.reduce_mean(tf.cast(correct_pred_eval, tf.float32))
                    ## tensorflow.python.framework.errors_impl.UnimplementedError: Cast string to int32 is not supported ?????

                reuse_vars = True
                tower_grads.append(grads)

        tower_grads = average_gradients(tower_grads)
        train_op = optimizer.apply_gradients(tower_grads)

        # Initialize the variables (i.e. assign their default value)
        init = tf.global_variables_initializer()

        # Start Training
        config = tf.ConfigProto(allow_soft_placement=True) # https://github.com/tensorflow/tensorflow/issues/2292
        config.gpu_options.allow_growth = True
        # config.gpu_options.per_process_gpu_memory_fraction = 0.5
        with tf.Session(config=config) as sess:

            # Run the initializer
            sess.run(init)

            # Keep training until reach max iterations
            for step in range(1, num_steps + 1):
                # Get a batch for each GPU
                # batch_x, batch_y = mnist.train.next_batch(batch_size * num_gpus)
                # Run optimization op (backprop)
                ts = time.time()
                sess.run(train_op) #### no placeholders   no feed_dict={X: batch_x, Y: batch_y}
                te = time.time() - ts
                if step % display_step == 0 or step == 1:
                    # Calculate batch loss and accuracy
                    loss, acc = sess.run([loss_op, accuracy_eval])
                    print("Step " + str(step) + ": Minibatch Loss= " + \
                          "{:.4f}".format(loss) + ", Training Accuracy= " + \
                          "{:.3f}".format(acc) + ", %i Examples/sec" % float(batch_size /te))
                step += 1
            print("Optimization Finished!")

            tf.train.Saver().save(sess, "./result/my_model_final")
            # conv_vars = tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES, scope="x")
            # reuse_vars_dict = dict([(var.op.name, var) for var in reuse_vars])
            # restore_saver = tf.train.Saver(reuse_vars_dict)

            # restore_saver.restore(sess, "./my_model_final.ckpt")

            # save_path = saver.save(sess, "/tmp/CNNdemo.ckpt")
            export_dir = './tmp/'
            # tf.saved_model.simple_save(sess, export_dir, inputs={"x": x, "y": y}, outputs={"z": z}) #new method
            # print("Model saved in path: %s" % save_path)
            # try to edit it so that it fits the other parts
            # # Calculate accuracy for MNIST test images
            # print("Testing Accuracy:", \
            #     np.mean([sess.run(accuracy) for i in range(0, eval_total_size, eval_batch_size)]))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument(
      '--learning_rate',
      type=float,
      default=0.01,
      help='Initial learning rate.'
  )
  parser.add_argument(
      '--num_epochs',
      type=int,
      default=10000,
      help='Number of epochs to run trainer.'
  )
  parser.add_argument(
      '--hidden1',
      type=int,
      default=1024,
      help='Number of units in hidden layer 1.'
  )
  parser.add_argument(
      '--hidden2',
      type=int,
      default=128,
      help='Number of units in hidden layer 2.'
  )
  parser.add_argument(
      '--batch_size',
      type=int,
      default=100,
      help='Batch size.'
  )
  parser.add_argument(
      '--train_dir',
      type=str,
      default='./tmp/data4/',
      help='Directory with the training data.'
  )
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
