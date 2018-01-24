=============================================================================
		Author: Sheng Xu (u5538588)					Group Size:  1
=============================================================================
Please run the file "u5538588_assignment_py" to run the program, and follows 
the following steps to calculate the thresholds from method A and B:
-----------------------------------------------------------------------------
1). Give the path of the single file you want to import:
	"Please enter the path of the files(start with '/'):"
	
	Your need to Press "Enter" after typing the path in the new line.

	* a valid path should start with "/" and end with ".csv":
	  (	eg: /home/document/Rainfall_Canberra_070247.csv	)
-----------------------------------------------------------------------------
2).	Choose the aggregation type for data filtering and calculation:
	"	1. Daily; 
		2. Monthly; 
		3. A specific month;
		4. Yearly;
		Please choose from 1 to 4:"

	Press "Enter" after typing your choice in the new line.

	* Your only need to type in the single option number from "1" to "4";
-----------------------------------------------------------------------------
3).	If your choice of the above step is not "3", please skip this step.	
	If you have chosen the aggregation type "3", you will be asked to choose
	the month of the aggregation:
	"	1. Jan; 
		2. Feb; 
   		...
		12. Dec
		Please choose from 1 to 12:"

	Press "Enter" after typing your choice in the new line.

	* Again, your only need to type in the single option number
	  (in this case: choose one option from "1" to "12");
-----------------------------------------------------------------------------
4).	Now you will be asked to choose the type of threshold:
	"	1. High;
		2. Low
		Please choose from 1 to 2:"

	Press "Enter" after typing your choice in the new line.

	* Again, your only need to type in the single option number
	  (in this case: "1" or "2");
-----------------------------------------------------------------------------
5).	You are now asked to type in the frequency for calculation:
	"	Please enter the frequency of the entries (positive integer ranging 
		from 2 only):"

	Press "Enter" after typing frequency in the new line.

	* A valid frequency should be a positive integer, and should be in the 
	  range: [2, number of the filtered data]  (half open)
	* If the input is rejected, please check whether your input is a positive
	  integer or not; Or, try to reduce the input frequency value.
=============================================================================
Introduction of the output contents will be provided in the this section:

	The output of the program will start with the line "========" to seperate
the input section. It contains two parts: the results from method b, and the
results from method a. The two parts will be seperated by the line "--------"

	If there are valid results found in both parts, the results will be in 
the following format:
		"============================================================
			The threshold from method b is: [the threshold]mm
			Found [number of results] data satisfies the threshold:
						[Datetime]: [Corresponding data]mm
									.
									.
									.
		-------------------------------------------------------------
			The threshold from method a is: [the threshold]mm
			Found [number of results] data satisfies the threshold:
						[Datetime]: [Corresponding data]mm
									.
									.
									.
		============================================================"

Otherwise, the output will indicate no threshold was found from which method
Failure reason of each method will be introduced in the following section.
=============================================================================
For method A: 

As long as the data is unique within the timespan(frequency), no matter it's
or not the highest/lowest(such as '0'), it will be the valid threshold.

*Special case*: If there are multiple data(with the same value) satisfy the 
condition of being the threshold, as long as any pair of them appeared within
the timespan, this value will not be the valid threshold.
-----------------------------------------------------------------------------
For method B:

The number of data which higher/lower than the threshold will always less than
or equal to the value of N/F.

*Special case*: If there is a value shared by multiple data, and caused the
number of results greater than the value N/F, then the threshold will be the
last different data - which has the different value - in the sorted list
=============================================================================
					Assumptions and Announcement
-----------------------------------------------------------------------------
1. Before the process of filtering, data are firstly ordered based on the order
of occurrence in the original file. Therefore, no matter how many data were 
filtered out, for any pair of valid data, the time interval of them are always
constant. In other words, the "gap" between data are never affected by the 
filtering process.(eg: the time interval between the valid data[1950: 642.7mm]
and [1964: 407.5mm] are always 14 years)

2. When calculating the threshold under the daily aggregation, it is very common
that the time interval between "0"s are greater than F, and that number of "0"s
is greater than N/F. The simplest way to treat this value may just return null 
or indicates no threshold can be found under this condition. However, to ensure
the accuracy of the results, "0"s are treated "unbiased" as other values. So in
the program, the calculation related to this case is same as calculating results
based on the raw solutions which starts at multiple data with same values.







