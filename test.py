
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

import numpy as np
import tensorflow as tf

from tensorflow.examples.tutorials.mnist import mnist
# print(type(int))

import numpy
c = numpy.array([ [[1, 2], [1, 2], [1, 2]],
                  [[1, 2], [1, 2], [1, 2]],
                  [[1, 2], [1, 2], [1, 2]],
                  [[1, 2], [1, 2], [1, 2]]])
print(c.shape)

from PIL import Image
import re
import os


def test():
    image_Path = '../NewData_rotated_jpeg/'
    count = 0
    imageCompressedArray = []
    for root, dirs, files in os.walk(image_Path):
        for filesingle in files:
            rootRe = re.search(r'(.+(?=\d))(\d)', root)
            # print('Label:', rootRe.group(2))
            img = Image.open(str(root) + '/' + str(filesingle))
            imageArray = numpy.asarray(img) # ([] [165] [330] [3])
            imageCompressedArray.append(imageArray)
            # if count == 0:
            #     imageCompressedArray = imageArray
            # if count == 1:
            #     imageCompressedArray = numpy.array(imageCompressedArray, imageArray)
            # else:
            #     imageCompressedArray = numpy.append(imageCompressedArray, imageArray, 0)
            if count == 23:
                imageCompressedArray = numpy.asarray(imageCompressedArray)
                print("Shape of the imageCompressedArray", imageCompressedArray.shape)
                cutArray = imageCompressedArray[:5]
                print("Shape of the cutArray", cutArray.shape)
                print("File counts to:", count)
                return 0
            count += 1
    print("File counts to:", count)

test()
