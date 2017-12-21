# -*- coding: utf-8 -*-

# import matplotlib.pyplot as plt
# import tensorflow as tf
import numpy as np
import errno
import os
import sys
import re
# Here I use pillow as a maintained fork of PIL
from PIL import Image
from os.path import join, getsize

'''
    This function is used to get all the files' and sub_folders' name for further operation
    
    :args
        file_path = the path you want to explore
    :returns
        image_name = dict contains all the image names 
        image_path = dict contains all the images' path
'''

'''
    This function is a print function used to print temporary results
    
    :arg
'''
def testprint(display_data):
    if is_test:
        print(display_data)

def get_all_image_names(file_path, is_test):
    image_names = []
    image_paths = []
    image_filename_Includingfolder = {}
    xml_names = []
    xml_paths = []
    xml_filename_Includingfolder = {}
    for root, dirs, files in os.walk(file_path):
        # print(root, "consumes", end=" ")
        # print(sum(getsize(join(root, name)) for name in files), end=" ")
        # print("bytes in", len(files), "non-directory files", end=" ")
        # print(os.path.isdir(os.path.join(root, files)))
        # print(root)
        # the file_path = "./康师傅/", so each time get into another directory, should record the sub path
        if dirs: # print the dirs only when it's a real directory(not a blank directory as: [])
            testprint(dirs) # this is the directory names
            testprint(root) # :) this is the root, so don't actually need to record the path anyway
        for filesingle in files:
            filename, suffix = os.path.splitext(filesingle)
            if suffix == '.xml':
            # if 0:
                #use regular expression to get the includeing directory
                folder = re.search(r'(../康师傅/)(.*(?=\\))(\\*)(.*)', root)
                #group(2) is the first sub folder name
                #group(1) is the file_path(inputed)
                #group(0) is all combined
                #group(4) is the second sub folder name
                # test codes
                # testprint(folder.group(0))
                # testprint(folder.group(1))
                # testprint(folder.group(2))
                # testprint(folder.group(3))
                # testprint(folder.group(4))
                if folder: #it may be None if not match in RE
                    if folder.group(4):
                        xml_filename_Includingfolder[str(filename + suffix)] = [str(folder.group(4)), str( file_path + folder.group(2) + '/' + folder.group(4) + '/' )]
                        xml_names.append(str(filename+suffix))
                        xml_paths.append(str( file_path + folder.group(2) + '/' + folder.group(4) + '/' ))
                    elif folder.group(2):
                        xml_filename_Includingfolder[str(filename + suffix)] = [str(folder.group(2)), str( file_path + folder.group(2) )]
                        xml_names.append(str(filename+suffix))
                        xml_paths.append(str( file_path + folder.group(2) ))
                    else:
                        xml_filename_Includingfolder[str(filename + suffix)] = [str(file_path), str(file_path)]
                        xml_names.append(str(filename+suffix))
                        xml_paths.append(str(file_path))
        # print(files)
        if '不一致图片' in dirs:
            # dirs.remove('不一致图片')  # don't visit 不一致图片 directories
            pass # you should deal with this situation
    return image_names, image_paths, image_filename_Includingfolder, xml_names, xml_paths, xml_filename_Includingfolder

'''
    This function is used to extract the noodle_only parts out of the original images which contains a lot of useless information
    
    :arg
        image = the original image you want to deal with(only one, and should be the image type)
    :returns
        noodel_* = the No.* noodel sub_image in the original image    
'''
def split_original_image(image):
    box_1 = (280, 90, 610, 420)
    box_2 = (680, 90, 1010, 420)
    # original_image = Image.open(fileNameWithPath) # to prevent from doing open and close operators too frequently, not here, use in main
    noodel_1 = original_image.crop(box_1)
    noodel_2 = original_image.crop(box_2)
    ##Uesd to show images on screen
    # noodel_1.show()
    # noodel_2.show()
    return noodel_1, noodel_2

'''
    This function is an improved version of function get_half_noodel()
    
    :arg
        noodle_only = the image only with noodle 
        ...* = the coordinates of the noodle, so this function can still deal with the original images
    :returns
        ...* = all the half of the noodle image, 330 * 165
'''
def get_helf_noodel_improved(noodle_only, up_left_x = 0, up_left_y = 0, down_right_x = 330, down_right_y = 330):
    pixel = 330
    box_horizontal_left = (up_left_x, up_left_y, down_right_x - pixel/2, down_right_y)
    box_horizontal_right = (up_left_x - pixel/2, up_left_y, down_right_x, down_right_y)

    box_longitudinal_up = (up_left_x, up_left_y, down_right_x, down_right_y - pixel/2)
    box_longitudinal_down = (up_left_x, up_left_y, down_right_x - pixel/2, down_right_y)

    box_cross_center = (up_left_x, up_left_y + pixel/4, down_right_x, down_right_y - pixel/4)
    box_vertical_center = (up_left_x + pixel/4, up_left_y, down_right_x - pixel/4, down_right_y)

    part_horizontal_left = noodle_only.crop(box_horizontal_left)
    part_horizontal_right = noodle_only.crop(box_horizontal_right)
    part_longitudinal_up = noodle_only.crop(box_longitudinal_up)
    part_longitudinal_down = noodle_only.crop(box_longitudinal_down)
    part_cross_center = noodle_only.crop(box_cross_center)
    part_vertical_center = noodle_only.crop(box_vertical_center)

    return part_horizontal_left, part_horizontal_right, part_longitudinal_up, part_longitudinal_down,\
            part_cross_center, part_vertical_center

def get_half_noodle(image):
    pixel = 330
    # the first one
    box_1_horizontal_left = (280, 90, 610 - pixel/2, 420)
    box_1_horizontal_right = (280 - pixel/2, 90, 610, 420)

    box_1_longitudinal_up = (280, 90, 610, 420 - pixel/2)
    box_1_longitudinal_down = (280, 90, 610 - pixel/2, 420)

    box_1_cross_center = (280, 90 + pixel/4, 610, 420 - pixel/4)
    box_1_vertical_center = (280 + pixel/4, 90, 610 - pixel/4, 420)

    #the second one
    box_2_horizontal_left = (680, 90, 1010 - pixel/2, 420)
    box_2_horizontal_right = (680 - pixel/2, 90, 1010, 420)

    box_2_longitudinal_up = (680, 90, 1010, 420 - pixel/2)
    box_2_longitudinal_down = (680, 90, 1010 - pixel/2, 420)

    box_2_cross_center = (680, 90 + pixel/4, 1010, 420 - pixel/4)
    box_2_vertical_center = (680 + pixel/4, 90, 1010 - pixel/4, 420)

    part_1_horizontal_left = image.crop(box_1_horizontal_left)
    part_1_horizontal_right = image.crop(box_1_horizontal_right)
    part_1_longitudinal_up = image.crop(box_1_longitudinal_up)
    part_1_longitudinal_down = image.crop(box_1_longitudinal_down)
    part_1_cross_center = image.crop(box_1_cross_center)
    part_1_vertical_center = image.crop(box_1_vertical_center)

    part_2_horizontal_left = image.crop(box_2_horizontal_left)
    part_2_horizontal_right = image.crop(box_2_horizontal_right)
    part_2_longitudinal_up = image.crop(box_2_longitudinal_up)
    part_2_longitudinal_down = image.crop(box_2_longitudinal_down)
    part_2_cross_center = image.crop(box_2_cross_center)
    part_2_vertical_center = image.crop(box_2_vertical_center)
    return part_1_horizontal_left, part_1_horizontal_right, part_1_longitudinal_up, part_1_longitudinal_down,\
            part_1_cross_center, part_1_vertical_center, part_2_horizontal_left, part_2_horizontal_right,\
            part_2_longitudinal_up, part_2_longitudinal_down, part_2_cross_center, part_2_vertical_center


'''
    This function is used to deal with more than one images situation, and base on the function split_original_image()
    
    :arg
        process_num = the num of images that you want to peocess
    :returns
        None
'''
def split_images_in_batch(process_num):
    for i in range(process_num):
        pass

'''
    This function is used to save the return image from function split_original_image() into files.
    
    :arg
        originalImage = the original image unsplit
        noodel_* = the No.* image of splits
        fileSavePath = the path you want to preserve the new input images 
        count = used for batch saving task, it will name the image with count in middle name(dafult: count = 0) 
    :returns
        None
        
'''
def save_images_to_files_process(originalImage, noodel_1, noodel_2, fileSavePath = './OutputImage/', count = 0):
    count = 0
    # for infile in sys.argv[1:]:
    outFileName, outFileSuffix = os.path.splitext(inFileName_absolute)
    outFile = [] #deal with the name, cause need the original name to locate the image in directories quickly
    temp = "noodel_lelf_" + str(count) + ".jpeg"
    outFile.append(temp)
    temp = "noodel_right_" + str(count) + ".jpeg"
    outFile.append(temp)
    temp = "original_image_"+ str(count) + ".jpeg"
    outFile.append(temp)
    # if infile != outfile:
    original_middle_path = "whole_noodel/"
    noodel_only_path = "noodle_only/"

    path_1 = fileSavePath + original_middle_path
    path_2 = fileSavePath + noodel_only_path
    # path_3 = fileSavePath + noodel_only_path
    try:
        # os.makedirs(path_1, exist_ok=False)
        os.makedirs(path_2, exist_ok=False)
        # os.makedirs(path_2, exist_ok=False)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise    # Error when creating new folder/directory

    try:
        # originalImage.save(path_1 + outFile[0])  #no need regenerate original images? Maybe need, casue the original directory is a mess
        noodel_1.save(path_2 + outFile[1])
        noodel_2.save(path_2 + outFile[2])
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

if __name__ == '__main__':
    ###prototype 1 deal with one image:
    process = 'prototype2'
    if (process == 'prototype1'):
        origin_iamge_path =  "../康师傅/2017.9.21/2017.9.21原图/"
        inFileName_relative = "leaper_09_20170114_130001131_0000005624.png"
        inFileName_absolute = origin_iamge_path + inFileName_relative
        original_image = Image.open(inFileName_absolute)#Image.open(origin_iamge_path + "leaper_09_20170114_130001131_0000005624.png")
        print(original_image.format, original_image.size, original_image.mode)
        noodel_1_image, noodel_2_image = split_original_image(original_image)
        # show images: origin, split left, split right
        original_image.show()
        noodel_1_image.show()
        noodel_2_image.show()
        save_images_to_files_process(original_image, noodel_1_image, noodel_2_image)

    ###prototype 2 image_batch_process:
    if (process == 'prototype2'):
        is_test = 1 #this is used for marking if it's in a test or not
        main_path = "../康师傅/"
        test_path = "./test/"
        _, _, _, xmlNames, xmlPaths, xml_Name_IncludingFolder = get_all_image_names(main_path, is_test)
        print('xml name: ', xmlNames)
        print('xml path: ', xmlPaths)
        print('xml name-folder: ', xml_Name_IncludingFolder)
