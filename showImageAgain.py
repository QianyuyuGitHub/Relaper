from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from PIL import Image
import tensorflow as tf

savePath = './ImageReture/'

filename_queue = tf.train.string_input_producer(["./TFRecord_one/train-00000-of-00002.tfrecords"]) #读入流中
reader = tf.TFRecordReader()
_, serialized_example = reader.read(filename_queue)   #返回文件名和文件
features = tf.parse_single_example(serialized_example,
                                   features={
                                       # 'label': tf.FixedLenFeature([], tf.int64),
                                       # 'img_raw' : tf.FixedLenFeature([], tf.string),
                                        'image/height': tf.FixedLenFeature([], tf.int64),
                                        'image/width': tf.FixedLenFeature([], tf.int64),
                                        'image/colorspace': tf.FixedLenFeature([], tf.string),
                                        'image/channels': tf.FixedLenFeature([], tf.int64),
                                        'image/class/label': tf.FixedLenFeature([], tf.int64),
                                        'image/class/text': tf.FixedLenFeature([], tf.string),
                                        'image/format': tf.FixedLenFeature([], tf.string),
                                        'image/filename': tf.FixedLenFeature([], tf.string),
                                        'image/encoded': tf.FixedLenFeature([], tf.string),
                                   })  #取出包含image和label的feature对象
image = tf.decode_raw(features['image/encoded'], tf.uint8)
image = tf.reshape(image, [128, 128, 3])
label = tf.cast(features['image/class/label'], tf.int32)
with tf.Session() as sess: #开始一个会话
    init_op = tf.initialize_all_variables()
    sess.run(init_op)
    coord =tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    for i in range(20):
        example, lb = sess.run([image, label])#在会话中取出image和label
        img=Image.fromarray(example, 'RGB')#这里Image是之前提到的
        img.save(savePath + str(i) + '_''Label_' + str(lb) + '.jpg')#存下图片
        print(example, lb)
    coord.request_stop()
    coord.join(threads)
