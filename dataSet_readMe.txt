'''This is the log and documentFile for dataSet of fast noodels.

This will contain all the constructions and all the log records. The detail will contain all the changes and improvements that are applied to this project not just the dataSet! And, as well, these stuff can be also found in git log.

And the structure of this file is like:

		////diagram_begin////

		----------------------------------------------------
		###date	
			#discription 
			details...
		@@@
		some notes...
		----------------------------------------------------

		////diagram_end////


*Author: by Yuyu Qian
*Date Created 13/12/2017

'''


----------------------------------------------------
### 13/12/2017

	#The label and color meaning of the dataSet  

	fork 			-- Blue
	red_bag 		-- Purple
	silver_bag 		-- Yellow
	transparent_bag -- Green

----------------------------------------------------
###14/12/2017
#The method about how to cut original images into two subimages(Later on, it should be five, but in the begining, I will make it simple as a demonstration) 
	
	%%%%%%In the "PLT" python package "Image" method:
	The region is defined by a 4-tuple, where coordinates are (left, upper, right, lower). The Python Imaging Library uses a coordinate system with (0, 0) in the upper left corner. 
	%%%%%%

	And the absolute coordinates of the noodle bowls are:
	      _________
		 @_Graph 1_@

	=======Bowl1=========
	(280,90)	(610,90)
	(280.420)	(610,420)
	=====================

	=======Bowl2=========
	(680,90)	(1010,90)
	(680.420)	(1010,420)
	=====================

	So the 4-tuple region is: (280,90,610,420) and (680,90,1010,420)
----------------------------------------------------
###28/12/2017
#Fixed some bugs, and manage to split .png images, by the information in "corresponding" .xml files.

@@@
The .xml files in 2017.9.28 folder can not be detective. How to fix it ?
@@@
It turned out, there was a sub extra folder called 2017.9.28 in 2017.10.23, so the correct data of 2017.9.28 got overwrited wrong,
and then I did't know, so the regular expression can not parse it!

@@@
Today, I found out, that all the .png are not the same shooting angle actually! .png will stay be the same direction in one whole day, but different among days.

@@@
Since the construction of original data is a mess. So better not to consider about the .xlsx, just use any .xml file related to .png no matter who made it. Otherwise, it will add much effort to do it, I can do it later on.

@@@
There are three types of .png files
they are shooted in different angle and position
So I devided them manully:               _________
								        @_Graph 2_@

	========Data_.pngType========                  ==== Type Details ====
			2017.9.21 1				|Type1 (280,90)(610,420) | (680,90)(1010,420)
			2017.9.22 1				|Type2 (70,100)(400,430) | (470,100)(800,430) | (870,90)(1200,420)
			2017.9.25 1				|Type3 (260,90)(590,420) | (665,90)(995,420)
			2017.9.26 1				|Type4 (70,95)(400,425)  | (470,100)(800,430) | (870,90)(1200,420)
			2017.9.27 1
			2017.9.28 1								^Type2 is similar to Type4^
			2017.9.29 1
			2017.9.30 1
			2017.10.9 1
			2017.10.10 1/2 !!!!!!
			2017.10.11 2
			2017.10.12 2
			2017.10.13 2
			2017.10.16 2
			2017.10.17 2
			2017.10.18 2
			2017.10.19 2 #Error Samples
			2017.10.20 2
			2017.10.23 2
			2017.10.24 4
			2017.10.25 4
			2017.10.26 4
			2017.10.27 4
			2017.10.30 4
			2017.10.31 4
			2017.11.01 4 #Error Samples
			2017.11.02 4/3 !!!!!!
			2017.11.03 3
			2017.11.06 3
			2017.11.07 3
			2017.11.09 3
			2017.11.14 3
			2017.11.16 3 #Error Samples
			2017.11.17 1
			2017.11.20 1
			2017.11.24 1
			2017.12.4 1
			2017.12.5 1
			2017.12.6 1
			2017.12.7 1
	========Data_.pngType========

----------------------------------------------------
###1/11/2018
#found that some .xml files are empty
											      _________
												 @_Graph 3_@

									The Four Parts of A Sub Noodel Image
		*( x_lu , y_lu )----------------*( (x_lu + x_rd)/2 , y_lu ) ------------------*( x_rd , y_lu )
		       	|									  |										  |
		       	|									  |										  |
		       	|									  |										  |
		       	|			Quadrant  	2			  |				Quadrant	1			  |
		       	|									  |										  |
		       	|									  |										  |
		       	|									  |										  |
 *( x_lu , (y_lu + y_rd)/2 )--------*( (x_lu + x_rd)/2 , (y_lu + y_rd)/2 )--------*( x_rd , (y_lu + y_rd)/2 )
 				|									  |										  |
 				|									  |										  |
 				|									  |										  |
		       	|			Quadrant  	3			  |				Quadrant	4			  |
 				|									  |										  |
 				|									  |										  |
 				|									  |										  |
		*( x_lu , y_rd )----------------*( (x_lu + x_rd)/2 , y_rd ) ------------------*( x_rd , y_rd )


----------------------------------------------------
###1/12/2018
#redesign the get_sub_png_lable() function, it become get_sub_png_lable_modified()
											      _________
												 @_Graph 4_@

		 __________________PNG___________________
		|    _____        _____        _____     |
		|	|	  |      |     |      |     |    |                                         _________
		|	|     |      |     |      |     |    |  (each PNG has a Type information, see @_Graph 2_@ )
		|	|_____|      |_____|      |_____|    |							|
		|______|_________________________________|							|
			   |			|			 |								   / \
			   |			|			 |			3. Type of the corresponding xml file of PNG(1/2/3/4)
			   |			|			 |								   3|
			  / \			|			 |								   3|
	1.sub_noodle_locatio----|------------|----|		===Only contains one sub_noodle image's location
	 		  \ /			|			 |	  |1						   3|
			   |			|			 |	  |1						   3|
			   |			|			 |	  |1						   3|
			   |			|			 |	  |1						   3|
			   |			|			 |	  |1						   3|
			   |			|			 |	  |1						   3|
			   |			|			 |	  |1						   3|
			  / \		   / \          / \   |1                           3|
    2.       coordinates_of_all_noodels_folks |1    ===contains all three noodles' folks' coordinates
    									   2| |1						   3|
    									   2| |1						   3|
    									   2| |1						   3|
    									   2| |1						   3|
    									   2| |1						   3|
    									   2| |1						   3|
    									   2| |1						   3|
    									   2| |1						   3|____________________________________
    									    =================================----------------					3|
    									    							   1|			   2|					3|
    									    							   1|			   2|					3|
    									    							   1|			   2|					3|
    			Invoke Function ======>>get_sub_png_lable_modified(sub_noodle_location, xml_type, coordinates_of_all_noodels_folks)
    											   ||
    											   ||
    											   ||
    											   ||
    											   ||
											  _____||___________PNG___________________
											 |    _____        _____        _____     |
											 |	 | | | |      |     |      |     |    |
											 |	 | |5| |      |     |      |     |    |
											 |	 |_|_|_|      |_____|      |_____|    |
											 |________________________________________|

					Finally, the get_sub_png_lable_modified() function will return the lable of max_&_min rigions only of sub_noodle_image
					So for each of the PNG image, it need to invoke get_sub_png_lable_modified() function two/three times to get the lables 
					for all the sub_sub_sliced_images

	*Program*
		get_sub_png_lable_modified(sub_noodle_location, xml_type, coordinates_of_all_noodels_folks)


----------------------------------------------------
###1/12/2018
#correct the problem: the parse_xml_into_dict() can not kick out the "²»Ò»ÖÂÍ¼Æ¬" folder .xml, mess the coordinates.
	Now the parse_xml_into_dict() become parse_xml_into_dict_version2()
	
#get_sub_png_lable_modified() modified, as it use (if, elif ...) to judege the coordinates, the correct is to use (if, if ...) to make sure every rigion will be calculated
																				   _________
#And correct the lable function, it is not four quadrants but six sub rigions, as @_Graph 5_@ shows:


																					      _________
																						 @_Graph 5_@

																			The Six Parts of A Sub Noodel Image
		*( x_lu , y_lu )-------------*( (3*x_lu + x_rd)/4 , y_lu )-------------*( (x_lu + x_rd)/2 , y_lu ) ----------------*( (x_lu + 3*x_rd)/4 , y_lu)----------------*( x_rd , y_lu )
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
*( x_lu , (3*y_lu + y_rd)/4 )--*( (3*x_lu + x_rd)/4 , (3*y_lu + y_rd)/4 )--*( (x_lu + x_rd)/2 , (3*y_lu + y_rd)/4 )--*( (x_lu + 3*x_rd)/4 , (3*y_lu + y_rd)/4 )--*( x_rd , (3*y_lu + y_rd)/4 )
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 *( x_lu , (y_lu + y_rd)/2 )----*( (3*x_lu + x_rd)/4 , (y_lu + y_rd)/2 )----*( (x_lu + x_rd)/2 , (y_lu + y_rd)/2 )----*( (x_lu + 3*x_rd)/4 , (y_lu + y_rd)/2 )----*( x_rd , (y_lu + y_rd)/2 )
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
*( x_lu , (y_lu + 3*y_rd)/4 )--*( (3*x_lu + x_rd)/4 , (y_lu + 3*y_rd)/4 )--*( (x_lu + x_rd)/2 , (y_lu + 3*y_rd)/4 )--*( (x_lu + 3*x_rd)/4 , (y_lu + 3*y_rd)/4 )--*( x_rd , (y_lu + 3*y_rd)/4 )
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
 				|									 |										   |										   |									|
		*( x_lu , y_rd )-------------*( (3*x_lu + x_rd)/4 , y_rd )--------------*( (x_lu + x_rd)/2 , y_rd )-----------------*( (x_lu + 3*x_rd)/4 , y_rd )---------------*( x_rd , y_rd )


#the .png are not the same type even in same folder in some circumensetance
#the reason why some .xml files are empty is that some .png files are not correct, and even some none empty .xml files relates to incorrect