from PIL import Image
import os
import errno
import sys
import time
from tqdm import tqdm

def rotate_and_save(image_type, save_file_path):
    rotate_angle_list = [-90, 90, 0, 180, 0, 90]
    rotate_angle = rotate_angle_list[image_type -1]
    # first deal with the negative samples, Source_path = '../NewDataImproved/*/0/'
    Source_path = '../NewDataImproved/' + str(image_type) + '/0/'
    if os.path.isdir(Source_path) and rotate_angle != 0:
        for root, dirs, files in os.walk(Source_path):
            for filesingle in files:
                # filename, suffix = os.path.splitext(filesingle)
                # print(filesingle)
                # print(filename)
                img = Image.open(Source_path + str(filesingle))
                img_rotated = img.rotate(rotate_angle, expand=True)
                img_rotated.save(save_file_path + '0/' + str(filesingle))
    # then deal with the positive samples, Source_path = '../NewDataImproved/*/1/'
    Source_path = '../NewDataImproved/' + str(image_type) + '/1/'
    if os.path.isdir(Source_path) and rotate_angle != 0:
        for root, dirs, files in os.walk(Source_path):
            for filesingle in files:
                # filename, suffix = os.path.splitext(filesingle)
                # print(filesingle)
                # print(filename)
                img = Image.open(Source_path + str(filesingle))
                img_rotated = img.rotate(rotate_angle, expand=True)
                img_rotated.save(save_file_path + '1/' + str(filesingle))

def image_rotate(save_file_path):
    try:
        os.makedirs(save_file_path + '0/', exist_ok=False)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise    # Error when creating new folder/directory
    try:
        os.makedirs(save_file_path + '1/', exist_ok=False)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise    # Error when creating new folder/directory

    for image_type in tqdm(range(1, 7), desc='Whole Progress Percentage'):
        rotate_and_save(image_type, save_file_path)
    # # first deal with the negative samples, Source_path = '../NewDataImproved/*/0/'
    # Source_path = '../NewDataImproved/' + str(image_type) + '/0/'
    # for root, dirs, files in os.walk(Source_path):
    #     for filesingle in files:
    #         # filename, suffix = os.path.splitext(filesingle)
    #         print(filesingle)
    #         # print(filename)
    #         img = Image.open(Source_path + str(filesingle))
    #         img_rotated = img.rotate(-90, expand=True)
    #         img_rotated.save(save_file_path + '0/' + str(filesingle))


import ctypes  # An included library with Python install.

if __name__ == '__main__':
    # print("Hello")
    image_rotate('../NewData_rotated/')
    ctypes.windll.user32.MessageBoxW(0, "The whole process is done, please confirm", "Procedure Complete", 1)
