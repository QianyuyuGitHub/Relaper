In this folder called NewData, the construction of the new data is:

NewData/ 
		|1/
			|0/
			|1/
			|2/
		|2/	 |	
		|3/	 |
		|4/  |
		|5/  |
		|6/  |
		 |   |
		 |   |
		 |   ---------------------------------------------------------
		 |															 |
		 |															 |
		 |															 |
		 |															 |
	 The type of location of sub images.@1               The lable of new .png image.@2




@1  There are six types of location exist: each type of location is a position relating to a sqaure in 330*330 / pixle^2, which only contains the noodle area 


----------------------------------
|			 	| 				 |
|				| 			 	 |
|				| 			 	 |
|				| 			 	 |
|				| 			 	 |
|	   	1 		| 		 2	 	 |
|				| 			 	 |
|				| 			 	 |
|				| 			 	 |
|				| 			 	 |
|				| 			 	 |
----------------------------------

----------------------------------
|								 |
|								 |
|				3				 |
|								 |
|								 |
----------------------------------
|								 |
|								 |
|				4				 |
|								 |
|								 |
----------------------------------


----------------------------------
|		|				|		 |
|		|				|		 |
|		|				|		 |
|		|				|		 |
|		|				|		 |
|		|		5		|		 |
|		|				|		 |
|		|				|		 |
|		|				|		 |
|		|				|		 |
|		|				|		 |
----------------------------------



----------------------------------
|								 |
|								 |
|								 |
----------------------------------
|								 |
|								 |
|				6				 |
|								 |
|								 |
----------------------------------
|								 |
|								 |
|								 |
----------------------------------

@2 The lables of new .png files are int type not boolen type, the type should be 0/1/2, where 0 denotes the False which means there is no folk in the image,
on the contract, 1 denotes the True which means most parts of folk lie in the image, in the meantime, 2 denotes other circumstances.
	As you can see, the basic idea is to rank the sub rigions of noodle areas to determine which one is the most "True" one, and which one is the opposite.


#############!!!!!!!!!!!!!!##############
the NewData need to be recheck, especially the negative samples, cause the ranking system is a rough and coarse. So you have to kick out samples that is obviously not 
corresponding to the lable.