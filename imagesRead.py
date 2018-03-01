# Copyright 2016 The TensorFlow Authors. All Rights Reserved.
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

"""Functions for downloading and reading MNIST data."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import gzip

import numpy
from six.moves import xrange  # pylint: disable=redefined-builtin

from tensorflow.contrib.learn.python.learn.datasets import base
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import random_seed
from tensorflow.python.platform import gfile
from PIL import Image
import os
import re
import io
import base64

image_Path = '../NewData_rotated_jpeg/'

def compress_data_label(image_Path):
    '''
    this is used to return the compressed data from images in folder
    :param image_Path:
    :return:
    '''
    a = 0
    iamgeConpressed = []
    labelCompressed = []
    for root, dirs, files in os.walk(image_Path):
        for filesingle in files:
            # print(root)
            rootRe = re.search(r'(.+(?=\d))(\d)', root)
            # print('Label:', rootRe.group(2))
            img = Image.open(str(root) + '/' + str(filesingle))
            imageArray = numpy.asarray(img) # ([] [165] [330] [3])
            # print(imageArray)
            iamgeConpressed.append(imageArray)
            labelCompressed.append(rootRe.group(2))
            labelCompressedArray = numpy.asarray(labelCompressed)
            if a == 0:
                print('The fisrt layer size;', len(imageArray))
                print('The second layer size:', len(imageArray[0]))
                print('The last layer size:', len(imageArray[0][0]))
                a = 1
    print('The final index of iamgeConpressed is:', len(iamgeConpressed))
    print('The final index of labelConpressed is:', len(labelCompressedArray))
    print('The type of the labelCompressed is:', type(labelCompressedArray))
    return iamgeConpressed, labelCompressedArray



class DataSet(object):

  def __init__(self,
               images,
               labels,
               fake_data=False,
               one_hot=False,
               dtype=dtypes.float32,
               reshape=True,
               seed=None):
    """Construct a DataSet.
    one_hot arg is used only if fake_data is true.  `dtype` can be either
    `uint8` to leave the input as `[0, 255]`, or `float32` to rescale into
    `[0, 1]`.  Seed arg provides for convenient deterministic testing.
    """
    seed1, seed2 = random_seed.get_seed(seed)
    # If op level seed is not set, use whatever graph level seed is returned
    numpy.random.seed(seed1 if seed is None else seed2)
    dtype = dtypes.as_dtype(dtype).base_dtype
    if dtype not in (dtypes.uint8, dtypes.float32):
      raise TypeError('Invalid image dtype %r, expected uint8 or float32' %
                      dtype)
    if fake_data:
      self._num_examples = 10000
      self.one_hot = one_hot
    else:
      assert images.shape[0] == labels.shape[0], (
          'images.shape: %s labels.shape: %s' % (images.shape, labels.shape))
      self._num_examples = images.shape[0]

      # Convert shape from [num examples, rows, columns, depth]
      # to [num examples, rows*columns] (assuming depth == 1)
      if reshape:
        assert images.shape[3] == 1
        images = images.reshape(images.shape[0],
                                images.shape[1] * images.shape[2])
      if dtype == dtypes.float32:
        # Convert from [0, 255] -> [0.0, 1.0].
        images = images.astype(numpy.float32)
        images = numpy.multiply(images, 1.0 / 255.0)
    self._images = images
    self._labels = labels
    self._epochs_completed = 0
    self._index_in_epoch = 0

def read_data_sets(train_dir,
                   fake_data=False,
                   one_hot=False,
                   dtype=dtypes.float32,
                   reshape=True,
                   validation_size=2000,
                   seed=None,
                   source_url=image_Path):

    images, labels = compress_data_label(image_Path)

    validation_images = images[:validation_size]
    validation_labels = labels[:validation_size]
    train_images = images[validation_size:]
    train_labels = labels[validation_size:]
    test_images = train_images
    test_labels = train_labels

    options = dict(dtype=dtype, reshape=reshape, seed=seed)

    train = DataSet(train_images, train_labels, **options)
    validation = DataSet(validation_images, validation_labels, **options)
    test = DataSet(test_images, test_labels, **options)

    return base.Datasets(train=train, validation=validation, test=test)


if __name__ == '__main__':
    compress_data_label(image_Path)



