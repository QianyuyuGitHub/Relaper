# -*- coding: utf-8 -*-

# import matplotlib.pyplot as plt
# import tensorflow as tf
import errno
import os
import re

import openpyxl as xl  # this is used to parse the .xlsx files
# Here I use pillow as a maintained fork of PIL
from PIL import Image

'''
    This function is a print function used to print temporary results
    
    :arg
'''
def testprint(display_data, end_cus = '\n'):
    if is_test:
        print(display_data, end=end_cus)
'''
    This function is used to get all the files' and sub_folders' name for further operation
    
    :args
        file_path = the path you want to explore
        is_test = whether it's a test mode or real implementation
    :returns
        image_names = list contains all the image names 
        image_paths = list contains all the images' path
        image_filename_Includingfolder = dict contains image imageName as key, [former directory, whole path] as value
        xml_names = list of xml file names 
        xml_paths = list of xml file paths
        xml_filename_Includingfolder = dict contains xml fileName as key, [former directory, whole path, #2former directory, #2whole path, #3former directory, #3whole path] as value
'''
def get_all_image_and_xml_files(file_path, is_test = 0):
    image_names = []
    image_paths = []
    image_filename_Includingfolder = {}
    xml_names = []
    xml_paths = []
    xml_filename_Includingfolder = {}
    count1 = 0
    count2 = 0
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
                    #if the .xml is not the only one, actually, they are not:
                    if (str(filename + suffix)) in xml_filename_Includingfolder:
                        # testprint("gocha!")
                        if folder.group(4):
                            xml_filename_Includingfolder[str(filename + suffix)].extend([str(folder.group(4)), str( file_path + folder.group(2) + '/' + folder.group(4) + '/' )])
                            xml_names.append(str(filename+suffix))
                            xml_paths.append(str( file_path + folder.group(2) + '/' + folder.group(4) + '/' ))
                        elif folder.group(2):
                            xml_filename_Includingfolder[str(filename + suffix)].extend([str(folder.group(2)), str( file_path + folder.group(2) )])
                            xml_names.append(str(filename+suffix))
                            xml_paths.append(str( file_path + folder.group(2) ))
                        else:
                            xml_filename_Includingfolder[str(filename + suffix)].extend([str(file_path), str(file_path)])
                            xml_names.append(str(filename+suffix))
                            xml_paths.append(str(file_path))
                    else:
                        if folder.group(4):
                            xml_filename_Includingfolder[str(filename + suffix)] = [str(folder.group(4)), str(file_path + folder.group(2) + '/' + folder.group(4) + '/' )]
                            xml_names.append(str(filename+suffix))
                            xml_paths.append(str(file_path + folder.group(2) + '/' + folder.group(4) + '/' ))
                        elif folder.group(2):
                            xml_filename_Includingfolder[str(filename + suffix)] = [str(folder.group(2)), str(file_path + folder.group(2) )]
                            xml_names.append(str(filename+suffix))
                            xml_paths.append(str(file_path + folder.group(2) ))
                        else:
                            xml_filename_Includingfolder[str(filename + suffix)] = [str(file_path), str(file_path)]
                            xml_names.append(str(filename+suffix))
                            xml_paths.append(str(file_path))
            if suffix == '.png':
            # if 0:
                #use regular expression to get the includeing directory
                folder = re.search(r'(../康师傅/)(.*(?=\\))(\\*)(.*)', root)
                if folder: #it may be None if not match in RE
                    if folder.group(4):
                        image_filename_Includingfolder[str(filename + suffix)] = [str(folder.group(4)), str( file_path + folder.group(2) + '/' + folder.group(4) + '/' )]
                        image_names.append(str(filename+suffix))
                        image_paths.append(str( file_path + folder.group(2) + '/' + folder.group(4) + '/' ))
                    elif folder.group(2):
                        image_filename_Includingfolder[str(filename + suffix)] = [str(folder.group(2)), str( file_path + folder.group(2) )]
                        image_names.append(str(filename+suffix))
                        image_paths.append(str( file_path + folder.group(2) ))
                    else:
                        image_filename_Includingfolder[str(filename + suffix)] = [str(file_path), str(file_path)]
                        image_names.append(str(filename+suffix))
                        image_paths.append(str(file_path))
        # print(files)
        if '不一致图片' in dirs:
            # dirs.remove('不一致图片')  # don't visit 不一致图片 directories
            pass # you should deal with this situation
    testprint('Image Total')
    return image_names, image_paths, image_filename_Includingfolder, xml_names, xml_paths, xml_filename_Includingfolder
def get_all_xlsx_files(file_path, is_test = 0):
    xlsx_names = []
    xlsx_paths = []
    xlsx_filename_Includingfolder = {}
    count = 0
    for root, dirs, files in os.walk(file_path):
        # if dirs: # print the dirs only when it's a real directory(not a blank directory as: [])
        #     testprint("Directorys:", ' ')
        #     testprint(dirs) # this is the directory names
        #     testprint("Roots:", ' ')
        #     testprint(root) # :) this is the root, so don't actually need to record the path anyway
        for filesingle in files:
            filename, suffix = os.path.splitext(filesingle)
            # if suffix == '.xlsx':
            #     print(filename)
            #     print(suffix)
            if suffix == '.xlsx':
            # if 0:
                #use regular expression to get the includeing directory
                # folder = re.search(r'(../康师傅/)(.*(?=\\))(\\*)(.*)', root) #this is wrong
                folder = re.search(r'(../康师傅)(/)(.*)', root)
                # # test codes
                # if folder:
                #     testprint(folder.group(0))
                #     testprint(folder.group(1))
                #     testprint(folder.group(2))
                #     testprint(folder.group(3))
                if folder:
                    if folder.group(3):
                        xlsx_filename_Includingfolder[str(filename + suffix)] = [str(folder.group(3)), str(file_path + folder.group(3) + '/')]
                        xlsx_names.append(str(filename+suffix))
                        xlsx_paths.append(str( file_path + folder.group(3) + '/' ))
                        count += 1
    testprint(count)
    return xlsx_names, xlsx_paths, xlsx_filename_Includingfolder
'''
    This function is used to extract the noodle_only parts out of the original images which contains a lot of useless information
    
    :arg
        image = the original image you want to deal with(only one, and should be the image type)
    :returns
        noodle_* = the No.* noodle sub_image in the original image    
'''
def split_original_image(Image_wait_to_split):
    box_1 = (280, 90, 610, 420)
    box_2 = (680, 90, 1010, 420)
    # original_image = Image.open(fileNameWithPath) # to prevent from doing open and close operators too frequently, not here, use in main
    noodle_1 = Image_wait_to_split.crop(box_1)
    noodle_2 = Image_wait_to_split.crop(box_2)
    ##Uesd to show images on screen
    # noodle_1.show()
    # noodle_2.show()
    return noodle_1, noodle_2

'''
    This function is an improved version of function get_half_noodle()
    
    :arg
        noodle_only = the image only with noodle 
        ...* = the coordinates of the noodle, so this function can still deal with the original images, have default values
    :returns
        ...* = all the half of the noodle image, 330 * 165
'''
def get_helf_noodle_improved(noodle_only, up_left_x = 0, up_left_y = 0, down_right_x = 330, down_right_y = 330, pixel = 330):
    box_horizontal_left = (up_left_x, up_left_y, down_right_x - pixel/2, down_right_y)
    box_horizontal_right = (up_left_x + pixel/2, up_left_y, down_right_x, down_right_y)

    box_longitudinal_up = (up_left_x, up_left_y, down_right_x, down_right_y - pixel/2)
    box_longitudinal_down = (up_left_x, up_left_y + pixel/2, down_right_x, down_right_y)

    # in this part, since the round off error, the image will have one more pixel
    # the solution is simple, add a offset to them
    # 330/4 = 82.5
    # print(up_left_y + pixel/4)        ||  82.5
    # print(down_right_y - pixel/4)     ||  247.5
    # offset = 0.3 is just some figure that works, I don't exactly know why
    box_cross_center = (up_left_x, up_left_y + pixel/4, down_right_x, down_right_y - pixel/4 - 0.3)
    box_vertical_center = (up_left_x + pixel/4, up_left_y, down_right_x - pixel/4 - 0.3, down_right_y)

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

def parse_xml_file(xml_file_name):
    pass

'''
    This function is used to deal with more than one images situation, and base on the function split_original_image()
    
    :arg
        process_num = the num of images that you want to peocess
        imageNames = name list of images
        imagePaths = path list of images 
        image_Name_IncludingFolder = ...
        xmlName = ...
        xmlPaths = ...
        xml_Name_IncludingFolder = ...
    :returns
        None
'''
def split_images_in_batch_and_save(process_num, imageNames, imagePaths, image_Name_IncludingFolder, xmlNames, xmlPaths, xml_Name_IncludingFolder):
    imageCount = 0
    # for image, xml in zip(imageNames, xmlNames): # they are not in the same order
    for image in imageNames:
        split_Name_and_Suffix = re.search(r'(\S*(?=\.))(\.*)(\S*)', image)
        imageNameWithoutSuffix, suffix = split_Name_and_Suffix.group(1),split_Name_and_Suffix.group(3)
        # testprint(imageNameWithoutSuffix)
        # testprint(suffix)
        xml_name_to_search = imageNameWithoutSuffix + '.xml'
        if xml_name_to_search in xmlNames:
            if process_num == imageCount:
                break
            # before save images to files, need to find out the label by parsing the .xml files:
            # parse_xml_file(xml_Name_IncludingFolder[image][1]+ )

            original_image = Image.open(image_Name_IncludingFolder[image][1]+image)
            # here the noodle_image1 hasn't been refresh! but why is that？
            # cause you idiot used a original_image parameter in the function! Be careful
            noodle_image1, noodle_image2 = split_original_image(original_image)
            # noodle_image1, noodle_image2 = split_original_image(image_Name_IncludingFolder[image][1]+image)
            # noodle_image1.show()
            part_horizontal_left, part_horizontal_right, part_longitudinal_up, part_longitudinal_down,\
            part_cross_center, part_vertical_center = get_helf_noodle_improved(noodle_image1)

            part_longitudinal_up = part_longitudinal_up.rotate(90, resample=0, expand=1)
            part_longitudinal_down = part_longitudinal_down.rotate(90, resample=0, expand=1)
            part_vertical_center = part_vertical_center.rotate(90, resample=0, expand=1)
            # save_image_to_files_standerd(part_horizontal_left, '1', 'hl_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_horizontal_right, '1', 'hr_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_longitudinal_up, '1', 'lu_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_longitudinal_down, '1', 'ld_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_cross_center, '1', 'cc_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_vertical_center, '1', 'vc_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_horizontal_left, '1', 'hl_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_horizontal_right, '1', 'hr_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_longitudinal_up, '1', 'lu_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_longitudinal_down, '1', 'ld_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_cross_center, '1', 'cc_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_vertical_center, '1', 'vc_test' + str(imageCount), './test/')

            part_horizontal_left, part_horizontal_right, part_longitudinal_up, part_longitudinal_down,\
            part_cross_center, part_vertical_center = get_helf_noodle_improved(noodle_image2)

            part_longitudinal_up = part_longitudinal_up.rotate(90, resample=0, expand=1)
            part_longitudinal_down = part_longitudinal_down.rotate(90, resample=0, expand=1)
            part_vertical_center = part_vertical_center.rotate(90, resample=0, expand=1)
            # save_image_to_files_standerd(part_horizontal_left, '1', 'hl_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_horizontal_right, '1', 'hr_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_longitudinal_up, '1', 'lu_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_longitudinal_down, '1', 'ld_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_cross_center, '1', 'cc_test' + str(imageCount), './test/')
            # save_image_to_files_standerd(part_vertical_center, '1', 'vc_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_horizontal_left, '1', 'hl_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_horizontal_right, '1', 'hr_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_longitudinal_up, '1', 'lu_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_longitudinal_down, '1', 'ld_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_cross_center, '1', 'cc_test' + str(imageCount), './test/')
            save_image_to_files_standerd_JPEG(part_vertical_center, '1', 'vc_test' + str(imageCount), './test/')

        imageCount += 1
'''
    This function simply store the image to the corresponding folders
    
    :arg
        image = image that will be stored, it's a image itself already, can be directory stored
            ///but I think maybe it's a smarter way not to do that, cause it will slow the program down I suppose
            ///maybe just send the name and read in sub-function will be more efficient? Don't know yet.
        label = to denote the positive or negative samples
        tag = to denote the position of image where it belong to it's original Noodle_Image
    :returns
        None
'''
def save_image_to_files_standerd(image, label, tag, directory = ''):
    if directory:
        try:
            os.makedirs(directory, exist_ok=False)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise    # Error when creating new folder/directory
            # for imageName in images:
            #     image = Image.open(imageName)
        try:
            image.save(directory+str(tag)+'.png')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    else:
        try:
            path = './' + label + '/'
            os.makedirs(path, exist_ok=False)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise    # Error when creating new folder/directory
        try:
            # originalImage.save(path_1 + outFile[0])  #no need regenerate original images? Maybe need, cause the origin directory is a mess
            image.save('./' + str(label) + '/' + str(tag)+'.png')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

def save_image_to_files_standerd_JPEG(image, label, tag, directory = ''):
    if directory:
        try:
            os.makedirs(directory, exist_ok=False)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise    # Error when creating new folder/directory
            # for imageName in images:
            #     image = Image.open(imageName)
        try:
            image.save(directory+str(tag)+'.jpeg')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    else:
        try:
            path = './' + label + '/'
            os.makedirs(path, exist_ok=False)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise    # Error when creating new folder/directory
        try:
            # originalImage.save(path_1 + outFile[0])  #no need regenerate original images? Maybe need, cause the origin directory is a mess
            image.save('./' + str(label) + '/' + str(tag)+'.png')
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

'''
    This function is used to save the return image from function split_original_image() into files.
    
    :arg
        originalImage = the original image unsplit
        noodle_* = the No.* image of splits
        fileSavePath = the path you want to preserve the new input images 
        count = used for batch saving task, it will name the image with count in middle name(dafult: count = 0) 
    :returns
        None
        
'''
def save_images_to_files_process(originalImage, noodle_1, noodle_2, fileSavePath = './OutputImage/', count = 0):
    count = 0
    # for infile in sys.argv[1:]:
    outFileName, outFileSuffix = os.path.splitext(inFileName_absolute)
    outFile = [] #deal with the name, cause need the original name to locate the image in directories quickly
    temp = "noodle_lelf_" + str(count) + ".jpeg"
    outFile.append(temp)
    temp = "noodle_right_" + str(count) + ".jpeg"
    outFile.append(temp)
    temp = "original_image_"+ str(count) + ".jpeg"
    outFile.append(temp)
    # if infile != outfile:
    original_middle_path = "whole_noodle/"
    noodle_only_path = "noodle_only/"

    path_1 = fileSavePath + original_middle_path
    path_2 = fileSavePath + noodle_only_path
    # path_3 = fileSavePath + noodle_only_path
    try:
        # os.makedirs(path_1, exist_ok=False)
        os.makedirs(path_2, exist_ok=False)
        # os.makedirs(path_2, exist_ok=False)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise    # Error when creating new folder/directory

    try:
        # originalImage.save(path_1 + outFile[0])  #no need regenerate original images? Maybe need, casue the original directory is a mess
        noodle_1.save(path_2 + outFile[1])
        noodle_2.save(path_2 + outFile[2])
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

'''
    This is function to determine if the .xml can be used to label the origin image data
    :arg
        xml_file_name
        xml_Name_IncludingFolder 
        xlsx_Name_Path_Dict
    :returns
        if this can be used?
'''
def Get_image_corresponding_xml(image_Name_IncludingFolder_xlsxFolder, xml_Name_IncludingFolder):
    for image, folder_list in image_Name_IncludingFolder_xlsxFolder.items():
        xlsx_folder = folder_list[2]

    xml_file_root_folder = xml_Name_IncludingFolder[xml_file_name][0]

    #.xlsx file processing, use a dict to store the result
    xlsxRootFolder_imagesCorrespondingPersonName = {}
    # xlsx_file_name_with_path = xlsx_Name_Path_Dict[xml_file_name][1] + xml_file_name + '.xlsx'
    xlsx_sheets = xl.load_workbook(xlsx_file_name_with_path, read_only=True) # read_only mode to deal with xlsx files
    run = 1
    row_num = run + 1
    column_num = run + 1
    xlsx_first_sheet = xlsx_sheets['Sheet1']
    run = 1
    ele1 = xlsx_first_sheet.cell(row=1, column=2)
    ele2 = xlsx_first_sheet.cell(row=1, column=3)
    ele3 = xlsx_first_sheet.cell(row=1, column=4)
    firstPersonName = ele1.value
    secondPersonName = ele2.value
    thirdPersonName = ele3.value
    while(run): #this is first layer
        ele = xlsx_first_sheet.cell(row=row_num, column=column_num)
        if ele.value == 'OK':
            testprint(firstPersonName, ': ')
            testprint(ele.value)
            row_num += 1
            column_num += 0
        elif ele.value is None:
            testprint("The .xlsx file reach the end!")
            run = 0
        else:
            testprint(' First person fail.', ' || ')
            ele = xlsx_first_sheet.cell(row=row_num, column=column_num + 1)
            if ele.value == 'OK':
                testprint(secondPersonName, ': ')
                testprint('OK')
                row_num += 1
                column_num += 0
            else:
                testprint(' Second person also fail.', ' || ')
                ele = xlsx_first_sheet.cell(row=row_num, column=column_num + 2)
                if ele.value == 'OK':
                    testprint(thirdPersonName, ': ')
                    testprint('OK')
                    row_num += 1
                    column_num += 0
                else:
                    testprint(' ALL FAILED: Located in ', end_cus=' Row: ')
                    testprint(row_num, end_cus='')
                    testprint(' Column: ', end_cus='')
                    testprint(column_num)
            row_num += 1

if __name__ == '__main__':
    ###prototype 1 deal with one image:
    process = 'prototype4'


    if (process == 'prototype1'):
        origin_iamge_path =  "../康师傅/2017.9.21/2017.9.21原图/"
        inFileName_relative = "leaper_09_20170114_130001131_0000005624.png"
        inFileName_absolute = origin_iamge_path + inFileName_relative
        original_image = Image.open(inFileName_absolute)#Image.open(origin_iamge_path + "leaper_09_20170114_130001131_0000005624.png")
        print(original_image.format, original_image.size, original_image.mode)
        noodle_1_image, noodle_2_image = split_original_image(original_image)
        # show images: origin, split left, split right
        # original_image.show()
        # noodle_1_image.show()
        # noodle_2_image.show()
        # save_images_to_files_process(original_image, noodle_1_image, noodle_2_image)
        i1, i2, i3, i4, i5, i6 = get_helf_noodle_improved(noodle_1_image)
        # i1.show()
        # i2.show()
        # i3.show()
        # i4.show()
        i5.show()
        i6.show()
        print("i1_image_size: ",i1.size, end=' || ')
        print("i2_image_size: ",i2.size, end=' || ')
        print("i3_image_size: ",i3.size, end=' || ')
        print("i4_image_size: ",i4.size, end=' || ')
        print("i5_image_size: ",i5.size, end=' || ')
        print("i6_image_size: ",i6.size)


    ###prototype 2 image_batch_process:
    if (process == 'prototype2'):
        is_test = 1 #this is used for marking if it's in a test or not
        main_path = "../康师傅/"
        test_path = "./test/"
        imageNames, imagePaths, image_Name_IncludingFolder, xmlNames, xmlPaths, xml_Name_IncludingFolder = get_all_image_and_xml_files(main_path, is_test)
        # print('xml name: ', xmlNames)
        # print('xml path: ', xmlPaths)
        # print('xml name-folder: ', xml_Name_IncludingFolder)
        print("image name: ", imageNames)
        print("image path: ", imagePaths)
        print("image name-folder: ", image_Name_IncludingFolder)
        # testprint("This is a test: ")
        # testprint(image_Name_IncludingFolder[imageNames[0]][1])
        imageCount = len(imageNames)
        if len(imageNames) == len(imagePaths):
            print("There are ", imageCount, " images to be processed")
        # split_images_in_batch_and_save(len(imageNames), imageNames, imagePaths, image_Name_IncludingFolder, xmlNames, xmlPaths, xml_Name_IncludingFolder)
        split_images_in_batch_and_save(5, imageNames, imagePaths, image_Name_IncludingFolder, xmlNames, xmlPaths, xml_Name_IncludingFolder)

    ###prototype 3 .xlsx .xml parsing:
    if (process == 'prototype3'):
        is_test = 1 #this is used for marking if it's in a test or not
        main_path = "../康师傅/"
        test_path = "./test/"
        xlsxNames, xlsxPaths, xlsx_Name_IncludingFolder = get_all_xlsx_files(main_path, is_test)
        print(".xlsx name: ", xlsxNames)
        print(".xlsx path: ", xlsxPaths)
        print(".xlsx name-folder: ", xlsx_Name_IncludingFolder)
        # check the folder
        def xlsx_parse():
            pass
        xlsx = xlsxNames[0]
        xlsx_path = xlsx_Name_IncludingFolder[xlsx][1]
        file = xlsx_path + xlsx
        testprint(file)
        xlsx_sheets = xl.load_workbook(file, read_only= True) # read_only mode to deal with xlsx files

        run = 1
        row_num = run + 1
        column_num = run +1
        xlsx_first_sheet = xlsx_sheets['Sheet1']
        # replace all the testprint(ele.value) into detective result
        ele1 = xlsx_first_sheet.cell(row=1, column=2)
        ele2 = xlsx_first_sheet.cell(row=1, column=3)
        ele3 = xlsx_first_sheet.cell(row=1, column=4)
        firstPersonName = ele1.value
        secondPersonName = ele2.value
        thirdPersonName = ele3.value
        while(run): #this is first layer
            ele = xlsx_first_sheet.cell(row=row_num, column=column_num)
            if ele.value == 'OK':
                testprint(firstPersonName, ': ')
                testprint(ele.value)
                row_num += 1
                column_num += 0
            elif ele.value is None:
                testprint("The .xlsx file reach the end!")
                run = 0
            else:
                testprint(' First person fail.', ' || ')
                ele = xlsx_first_sheet.cell(row=row_num, column=column_num + 1)
                if ele.value == 'OK':
                    testprint(secondPersonName, ': ')
                    testprint('OK')
                    row_num += 1
                    column_num += 0
                else:
                    testprint(' Second person also fail.', ' || ')
                    ele = xlsx_first_sheet.cell(row=row_num, column=column_num + 2)
                    if ele.value == 'OK':
                        testprint(thirdPersonName, ': ')
                        testprint('OK')
                        row_num += 1
                        column_num += 0
                    else:
                        testprint(' ALL FAILED: Located in ', end_cus=' Row: ')
                        testprint(row_num, end_cus= '')
                        testprint(' Column: ', end_cus='')
                        testprint(column_num)
                row_num += 1

    ###prototype 4 .xml parsing
    if (process == 'prototype4'):
        is_test = 1 #this is used for marking if it's in a test or not
        main_path = "../康师傅/"
        test_path = "./test/"
        imageNames, imagePaths, image_Name_IncludingFolder, xmlNames, xmlPaths, xml_Name_IncludingFolder = get_all_image_and_xml_files(main_path, is_test)
        print('xml name: ', xmlNames)
        print('xml path: ', xmlPaths)
        print('xml name-folder: ', xml_Name_IncludingFolder)
        testprint(".xml files number in dict is: ", end_cus='')
        testprint(len(image_Name_IncludingFolder))
        # testprint("This is a test: ")
        # testprint(image_Name_IncludingFolder[imageNames[0]][1])
        imageCount = len(imageNames)
        if len(imageNames) == len(imagePaths):
            print("There are ", imageCount, " .png images to be processed")
        # split_images_in_batch_and_save(len(imageNames), imageNames, imagePaths, image_Name_IncludingFolder, xmlNames, xmlPaths, xml_Name_IncludingFolder)
        imageNames.sort()
        imagePaths.sort()
        xmlNames.sort()
        xmlPaths.sort()
        # print("image name: ", imageNames[:10])
        # print("image path: ", imagePaths[:10])
        # print("image name-folder: ", image_Name_IncludingFolder)
        #@@@@@
        image_Name_IncludingFolder_XLSXfolder = {}
        for imageName, [last_layer_folder, whole_path] in image_Name_IncludingFolder.items():
            folder = re.search(r'(../康师傅/)(.*?(?=/))(.*)', whole_path)
            # test print
            # testprint(folder.group(2))
            # the third part of the list is the folder where .xlsx in,
            image_Name_IncludingFolder_XLSXfolder[imageName] = [last_layer_folder, whole_path, folder.group(2)]
        #@@@@@
        xml_Folder_Name_wholePath = {}
        for xml, list in xml_Name_IncludingFolder.items():
            if len(list) == 2:
                [xmlfolder, xml_whole_path] = list
                folder1 = re.search(r'(../康师傅/)(.*?(?=/))(/?)(.*?(?=\d))(.*)', xml_whole_path)
                if folder1:
                    testprint(folder1.group(2), end_cus=' ')
                    testprint(folder1.group(4))
                if folder1:
                    if folder1.group(2) not in xml_Folder_Name_wholePath:
                        # xml_Folder_Name_wholePath[folder1.group(2)] = [xml, xmlfolder, xml_whole_path]
                        xml_Folder_Name_wholePath[folder1.group(2)] = [{xml: [xmlfolder, xml_whole_path]}]
                    else: # in fact after change list elements into dict, this situation will not occur, NOO! now, occur another!
                        # xml_Folder_Name_wholePath[folder1.group(2)].extend([xml, xmlfolder, xml_whole_path])
                        xml_Folder_Name_wholePath[folder1.group(2)].append([{xml: [xmlfolder, xml_whole_path]}])
            elif len(list) == 4:
                [xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2] = list
                folder1 = re.search(r'(../康师傅/)(.*?(?=/))(/?)(.*?(?=\d))(.*)', xml_whole_path)
                folder2 = re.search(r'(../康师傅/)(.*?(?=/))(/?)(.*?(?=\d))(.*)', xml_whole_path2)
                if folder1:
                    testprint(folder1.group(2), end_cus=' ')
                    testprint(folder1.group(4))
                if folder2:
                    testprint(folder2.group(2), end_cus=' ')
                    testprint(folder2.group(4))
                if folder1:
                    if folder1.group(2) not in xml_Folder_Name_wholePath:
                        # xml_Folder_Name_wholePath[folder1.group(2)] = [xml, xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2]
                        xml_Folder_Name_wholePath[folder1.group(2)] =[{xml: [xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2]}]
                    else: # in fact after change list elements into dict, this situation will not occur, NOO! now, occur another!
                        # xml_Folder_Name_wholePath[folder1.group(2)].extend([xml, xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2])
                        xml_Folder_Name_wholePath[folder1.group(2)].append([{xml: [xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2]}])
            elif len(list) == 6:
                [xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2, xmlfolder3, xml_whole_path3] = list
                folder1 = re.search(r'(../康师傅/)(.*?(?=/))(/?)(.*?(?=\d))(.*)', xml_whole_path)
                folder2 = re.search(r'(../康师傅/)(.*?(?=/))(/?)(.*?(?=\d))(.*)', xml_whole_path2)
                folder3 = re.search(r'(../康师傅/)(.*?(?=/))(/?)(.*?(?=\d))(.*)', xml_whole_path3)
                if folder1:
                    testprint(folder1.group(2), end_cus=' ')
                    testprint(folder1.group(4))
                if folder2:
                    testprint(folder2.group(2), end_cus=' ')
                    testprint(folder2.group(4))
                if folder3:
                    testprint(folder3.group(2), end_cus=' ')
                    testprint(folder3.group(4))
                if folder1:
                    if folder1.group(2) not in xml_Folder_Name_wholePath:
                        # xml_Folder_Name_wholePath[folder1.group(2)] = [xml, xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2, xmlfolder3, xml_whole_path3]
                        xml_Folder_Name_wholePath[folder1.group(2)] = [{xml: [xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2, xmlfolder3, xml_whole_path3]}]
                    else:# in fact after change list elements into dict, this situation will not occur, NOO! now, occur another!
                        # xml_Folder_Name_wholePath[folder1.group(2)].extend([xml, xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2, xmlfolder3, xml_whole_path3])
                        xml_Folder_Name_wholePath[folder1.group(2)].append([{xml: [xmlfolder, xml_whole_path, xmlfolder2, xml_whole_path2, xmlfolder3, xml_whole_path3]}])
            # folder = re.search(r'(../康师傅/)(.*?(?=/))(/?)(.*?(?=(\d|\s)))(.*)', xml_whole_path)
        testprint("After trans, .xml dict size: ", end_cus='')
        testprint(len(xml_Folder_Name_wholePath))
        testprint(xml_Folder_Name_wholePath)
        # print("image's corresponding .xml file root folder/ last-last-layer-folder: ", image_Name_IncludingFolder_XMLfolder)
        # split_images_in_batch_and_save(len(imageName), imageNames, imagePaths, image_Name_IncludingFolder, xmlNames, xmlPaths, xml_Name_IncludingFolder)
        # Get_image_corresponding_xml(image_Name_IncludingFolder_XLSXfolder, xml_Name_IncludingFolder)
