
# class magicMethod(object):
#
#     def __init__(self, age=18, gender='female'):
#         self.age = age
#         self.gender = gender
#
#     def listout(self):
#         print('The age of mine is:', self.age)
#         print('The gender of mine is:', self.gender)
#
# yoyo = magicMethod(20, 'male')
# yoyo.listout()
# zhang = magicMethod()
# zhang.listout()


# def foo_b(parameter):
#     def decorator(foo_ahead):
#         def wrapper(*args, **kwargs):
#             return foo_ahead(*args, **kwargs)
#         return wrapper
#     return decorator
#
# @foo_b
# def foo_a(bar_a):
#     print('bar is:', bar_a)
#
# foo_a(5)


# def greet_me(**kwargs):
#     for key, value in kwargs.items():
#         print("{0} == {1}".format(key, value))
#
# greet_me(a='yo', b='yoyo')

# print(dic_a)


# import numpy as np
# import tensorflow as tf
# N_SAMPLES = 100000
# NUM_THREADS = 2
# all_data = 10 * np.random.randn(N_SAMPLES, 4) + 1
# all_target = np.random.randint(0, 2, size=N_SAMPLES)
#
# # a common practice is to enqueue all data at once, but dequeue one by one：一次性enqueue，多次dequeue
# queue = tf.FIFOQueue(capacity=50, dtypes=[tf.float32, tf.int32], shapes=[[4], []]) #定义queue的结构
# enqueue_op = queue.enqueue_many([all_data, all_target]) # 将数据enqueue到queue对象中
# data_sample, label_sample = queue.dequeue() # 将数据从queue对象中dequeue出来
#
# #QueueRunner create a number of threads cooperating to enqueue tensors in the same queue
# qr = tf.train.QueueRunner(queue, [enqueue_op] * NUM_THREADS) # 自动分配多线程
# with tf.Session() as sess:
#     # create a coordinator, launch the queue runner threads.
#     #Coordinator help multiple threads stop together and report exceptions to a program that waits for them to stop
#     coord = tf.train.Coordinator() # 让多线程同时停下，并向等在的后续程序汇报错误
#     enqueue_threads = qr.create_threads(sess, coord=coord, start=True)
#     for step in range(100): # do to 100 iterations
#         if coord.should_stop():
#             break
#         one_data, one_label = sess.run([data_sample, label_sample])
#     coord.request_stop()
#     coord.join(enqueue_threads)
# print("all_data;", all_data)
# print("all_target:", all_target)



# import numpy as np
import tensorflow as tf
#
# from tensorflow.examples.tutorials.mnist import mnist
# # print(type(int))
#
# import numpy
# c = numpy.array([ [[1, 2], [1, 2], [1, 2]],
#                   [[1, 2], [1, 2], [1, 2]],
#                   [[1, 2], [1, 2], [1, 2]],
#                   [[1, 2], [1, 2], [1, 2]]])
# print(c.shape)
#
# from PIL import Image
# import re
# import os
#
#
# def test():
#     image_Path = '../NewData_rotated_jpeg/'
#     count = 0
#     imageCompressedArray = []
#     for root, dirs, files in os.walk(image_Path):
#         for filesingle in files:
#             rootRe = re.search(r'(.+(?=\d))(\d)', root)
#             # print('Label:', rootRe.group(2))
#             img = Image.open(str(root) + '/' + str(filesingle))
#             imageArray = numpy.asarray(img) # ([] [165] [330] [3])
#             imageCompressedArray.append(imageArray)
#             # if count == 0:
#             #     imageCompressedArray = imageArray
#             # if count == 1:
#             #     imageCompressedArray = numpy.array(imageCompressedArray, imageArray)
#             # else:
#             #     imageCompressedArray = numpy.append(imageCompressedArray, imageArray, 0)
#             if count == 23:
#                 imageCompressedArray = numpy.asarray(imageCompressedArray)
#                 print("Shape of the imageCompressedArray", imageCompressedArray.shape)
#                 cutArray = imageCompressedArray[:5]
#                 print("Shape of the cutArray", cutArray.shape)
#                 print("File counts to:", count)
#                 return 0
#             count += 1
#     print("File counts to:", count)
#
# test()
import NetStructureV2
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
  image.set_shape((NetStructureV2.IMAGE_PIXELS))

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
  filename = './tmp/data/'

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


def run_training():
  """Train MNIST for a number of steps."""

  # Tell TensorFlow that the model will be built into the default Graph.
  with tf.Graph().as_default():
    # Input images and labels.
    image_batch, label_batch = inputs(train=True, batch_size=10,
                               num_epochs=1)
    # for i in image_batch:
    print(tf.rank(image_batch))

run_training()
