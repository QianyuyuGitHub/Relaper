# Copyright 2015 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Train and Eval the MNIST network.

This version is like fully_connected_feed.py but uses data converted
to a TFRecords file containing tf.train.Example protocol buffers.
See:
https://www.tensorflow.org/programmers_guide/reading_data#reading_from_files
for context.

YOU MUST run convert_to_records before running this (but you only need to
run it once).
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import os.path
import sys
import time

import tensorflow as tf

from tensorflow.examples.tutorials.mnist import mnist

# Basic model parameters as external flags.
flags = tf.app.flags
FLAGS = flags.FLAGS
flags.DEFINE_integer("image_number", 4411, "Number of images in your tfrecord, default is 300.")
flags.DEFINE_integer("class_number", 2, "Number of class in your dataset/label.txt, default is 3.")
flags.DEFINE_integer("image_height", 165, "Height of the output image after crop and resize. Default is 299.")
flags.DEFINE_integer("image_width", 330, "Width of the output image after crop and resize. Default is 299.")
flags.DEFINE_integer("batch_size", 1000, "Width of the output image after crop and resize. Default is 299.")

# define a function to list tfrecord files.
def list_tfrecord_file(file_list):
    tfrecord_list = []
    for i in range(len(file_list)):
        current_file_abs_path = os.path.abspath(file_list[i])
        if current_file_abs_path.endswith(".tfrecord"):
            tfrecord_list.append(current_file_abs_path)
            print("Found %s successfully!" % file_list[i])
        else:
            pass
    return tfrecord_list


# list_dir = "./TFRecord_one/" # need to be changed

# Traverse current directory
def tfrecord_auto_traversal():
    current_folder_filename_list = os.listdir("./TFRecord_one/")
    if current_folder_filename_list != None:
        print("%s files were found under current folder. " % len(current_folder_filename_list))
        print("Please be noted that only files end with '*.tfrecord' will be load!")
        tfrecord_list = list_tfrecord_file(current_folder_filename_list)
        if len(tfrecord_list) != 0:
            for list_index in range(len(tfrecord_list)):
                print(tfrecord_list[list_index])
        else:
            print("Cannot find any tfrecord files, please check the path.")
    return tfrecord_list

filename_queue = tf.train.string_input_producer(
        tfrecord_auto_traversal(),
        shuffle=True)
'''
  example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': _int64_feature(height),
      'image/width': _int64_feature(width),
      'image/colorspace': _bytes_feature(tf.compat.as_bytes(colorspace)),
      'image/channels': _int64_feature(channels),
      'image/class/label': _int64_feature(label),
      'image/class/text': _bytes_feature(tf.compat.as_bytes(text)),
      'image/format': _bytes_feature(tf.compat.as_bytes(image_format)),
      'image/filename': _bytes_feature(tf.compat.as_bytes(os.path.basename(filename))),
      'image/encoded': _bytes_feature(tf.compat.as_bytes(image_buffer))}))
'''
def read_and_decode_qyy(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example, features={
        "encoded": tf.FixedLenFeature([], tf.string),
        "height": tf.FixedLenFeature([], tf.int64),
        "width": tf.FixedLenFeature([], tf.int64),
        "filename": tf.FixedLenFeature([], tf.string),
        "label": tf.FixedLenFeature([], tf.int64)})

    # image_encoded = features["encoded"]
    # image_raw = tf.image.decode_jpeg(image_encoded, channels=3)

    # current_image_object = image_object()

    # current_image_object.image = tf.image.resize_image_with_crop_or_pad(image_raw, FLAGS.image_height, FLAGS.image_width) # cropped image with size 299x299
    # # current_image_object.image = tf.cast(image_crop, tf.float32) * (1./255) - 0.5
    # current_image_object.height = features["height"] # height of the raw image
    # current_image_object.width = features["width"] # width of the raw image
    # current_image_object.filename = features["filename"] # filename of the raw image
    # current_image_object.label = tf.cast(features["label"], tf.int32) # label of the raw image

    im = tf.decode_raw(features["encoded"], tf.uint8)
    im = tf.reshape(im, [FLAGS.batch_size, FLAGS.image_height, FLAGS.image_width, 3])
    # im = tf.cast(im, tf.float32) * (1. / 128) - 0.5
    label = tf.cast(features["label"], tf.int64)

    return im, label
# Constants used for dealing with the files, matches convert_to_records.
TRAIN_FILE = 'train-00000-of-00002.tfrecords'
VALIDATION_FILE = 'validation-00000-of-00002.tfrecords'



def decode(serialized_example):
  features = tf.parse_single_example(
      serialized_example,
      # Defaults are not specified since both keys are required.
      features={
          'image_raw': tf.FixedLenFeature([], tf.string),
          'label': tf.FixedLenFeature([], tf.int64),
      })

  # Convert from a scalar string tensor (whose single string has
  # length mnist.IMAGE_PIXELS) to a uint8 tensor with shape
  # [mnist.IMAGE_PIXELS].
  image = tf.decode_raw(features['image_raw'], tf.uint8)
  image.set_shape((mnist.IMAGE_PIXELS))

  # Convert label from a scalar uint8 tensor to an int32 scalar.
  label = tf.cast(features['label'], tf.int32)

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
  filename = os.path.join(FLAGS.train_dir,
                          TRAIN_FILE if train else VALIDATION_FILE)

  with tf.name_scope('input'): #this line just means here is a scope, dosen't mean anything elses
    # TFRecordDataset opens a protobuf and reads entries line by line
    # could also be [list, of, filenames]
    dataset = tf.data.TFRecordDataset(filename)
    dataset = dataset.repeat(num_epochs)

    # map takes a python function and applies it to every sample
    dataset = dataset.map(read_and_decode_qyy(filename_queue))
    dataset = dataset.map(augment)
    dataset = dataset.map(normalize)

    #the parameter is the queue size
    dataset = dataset.shuffle(1000 + 3 * batch_size)
    dataset = dataset.batch(batch_size)

    iterator = dataset.make_one_shot_iterator()
  return iterator.get_next()

def run_training():
  """Train MNIST for a number of steps."""

  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default():
    # Input images and labels.
    image_batch, label_batch = inputs(train=True, batch_size=FLAGS.batch_size,
                               num_epochs=FLAGS.num_epochs)

    # Build a Graph that computes predictions from the inference model.
    logits = mnist.inference(image_batch,
                             FLAGS.hidden1,
                             FLAGS.hidden2)

    # Add to the Graph the loss calculation.
    loss = mnist.loss(logits, label_batch)

    # Add to the Graph operations that train the model.
    train_op = mnist.training(loss, FLAGS.learning_rate)

    # The op for initializing the variables.
    init_op = tf.group(tf.global_variables_initializer(),
                       tf.local_variables_initializer())

    # Create a session for running operations in the Graph.
    with tf.Session() as sess:
      # Initialize the variables (the trained variables and the
      # epoch counter).
      sess.run(init_op)
      try:
        step = 0
        while True: #train until OutOfRangeError
          start_time = time.time()

          # Run one step of the model.  The return values are
          # the activations from the `train_op` (which is
          # discarded) and the `loss` op.  To inspect the values
          # of your ops or variables, you may include them in
          # the list passed to sess.run() and the value tensors
          # will be returned in the tuple from the call.
          _, loss_value = sess.run([train_op, loss])

          duration = time.time() - start_time

          # Print an overview fairly often.
          if step % 100 == 0:
            print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value,
                                                     duration))
          step += 1
      except tf.errors.OutOfRangeError:
        print('Done training for %d epochs, %d steps.' % (FLAGS.num_epochs, step))

def main(_):
  run_training()


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
      default=2,
      help='Number of epochs to run trainer.'
  )
  parser.add_argument(
      '--hidden1',
      type=int,
      default=128,
      help='Number of units in hidden layer 1.'
  )
  parser.add_argument(
      '--hidden2',
      type=int,
      default=32,
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
      default='/TFRecord_one',
      help='Directory with the training data.'
  )
  FLAGS, unparsed = parser.parse_known_args()
  tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)