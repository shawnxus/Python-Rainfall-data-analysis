#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 23:48:36 2017

@author: Sheng Xu (u5538588)
"""
import os
import csv

info = []
slist = []
mon = ""
valid_month = ["1","2","3","4","5","6","7","8","9","10","11","12"]
frequency = 0
t_threshold = ""

def path_check(path_str):
    '''The function will repeatedly check whether or not the path is valid and file can be found, 
    only the valid path will be passed '''
    while not os.path.isfile(path_str):
        path_str = path_check(input("Invalid path! Please enter the correct path (start with '/', and include '/filename.csv'):\n"))
    return path_str

def aggregation_check(aggregation):
    '''The function will repeatedly check whether the input aggregation type is valid (1 to 4)'''
    while (not aggregation == "1") and (not aggregation == "2") and (not aggregation == "3") and (not aggregation == "4"):
        aggregation = aggregation_check(input("Invalid option !\nPlease choose the type of time series aggregation: \n1. Daily; \n2. Monthly; \n3. A specific month;\n4. Yearly;\nPlease choose from 1 to 4:\n"))
    return aggregation

def month_check(mon):
    '''The function will repeatedly check whether the input month for aggregation type 3 is valid 
    (1 to 12)'''
    while not mon in valid_month:
        mon = month_check(input("Invalid option !\nPlease choose the month of aggregation: \n1. Jan; \n2. Feb; \n   ...\n12. Dec\nPlease choose from 1 to 12:\n"))
    return mon

def threshold_type_check(t_threshold):
    '''The function will repeatedly check whether the type of threshold is valid (1:highest, or 2:lowest)'''
    while (not t_threshold == "1") and (not t_threshold == "2"):
        t_threshold = threshold_type_check(input("Invalid option !\nPlease choose the type of the threshold: \n1. High;\n2. Low\nPlease choose from 1 to 2:\n"))
    return t_threshold

def freq_check(frequency):
    '''The function will repeatedly check whether the value of frequency is valid 
    (positive integer)'''
    if not frequency.isdigit():
        frequency = freq_check(input("Invalid input !\nPlease enter the frequency of the entries (positive integer ranging from 2 only):\n"))
    elif int(frequency) <=1 or int(frequency) > len(info):
        frequency = freq_check(input("Frequency is out of data range !\nPlease enter the frequency of the entries (positive integer ranging from 2 only):\n"))
    return frequency

def remove_invalid(olist,elist):
    '''The function remove the data which is recorded multiple times
    or spans more than one month/year respectively'''
    nlist = []
    for o in olist:
        for e in elist:
            if not e in o:
              nlist.append(o)                   # only return the valid data(not in the error data list)
    return nlist

def reformat(olist):
    nlist = []
    for i in olist:
        if int(mon) == int(i[3][5:]):
            nlist.append([i[0],i[1],i[2],i[3][0:4],int(i[3][0:4])])
    return nlist

def error_data_monthly(errorData,nperiod,ndata,ndate,nmonth,nyear,data,month,year):
    '''The function will record the unsatisfying data which spans more than one month
    or was recorded multiple times'''
    eData = []
    if nperiod.isdigit() and ndate.isdigit():
        if int(nperiod)>int(ndate):                        # check if record spans more than one month(period > date)
            eData = [str(nyear)+"/"+str(nmonth)]           # remove conflicting data(may not precisely but enough to discard this particular month)
            if not eData in errorData:
                errorData.append(eData)
            eData = [str(year)+"/"+str(month)]
            if not eData in errorData:
                errorData.append(eData)
    if data!="" and ndata!="" and nperiod!="" and nperiod!="1" and nmonth.isdigit(): # check if data was recorded once only (period overlap between adjacent data)
        eData = [str(nyear)+"/"+str(nmonth)]
        if not eData in errorData:
            errorData.append(eData)
    return errorData

def error_data_yearly(eData,nperiod,ndata,ndate,nmonth,nyear,year,data):
    '''The function will record the unsatisfying data which spans more than one year
    or was recorded multiple times'''
    if nperiod.isdigit() and ndate.isdigit() and (nmonth=="01" or nmonth =="1"):    # trigger of entering a new year
        if int(nperiod)>int(ndate):                         # check if period of observed in new year's Jan spans to the last year
            if not nyear in eData:
                eData.append(nyear)
            if not year in eData:
                eData.append(year)
    if data!="" and ndata!="" and nperiod!="" and nperiod!="1" and ndate.isdigit(): # remove conflicting data
        if not nyear in eData:
            eData.append(nyear)
    return eData

def data_restore_daily(fileName):
    '''The function will read the file and restore the information, of which the data was 
    observed for a single day only, into a list with the headings removed'''
    info = []
    total_days = 0
    fileobj = open(fileName)
    reader = csv.reader(fileobj)
    for row in reader:
        if row[4].isdigit():                                    # headings will be ignored when calculating total days in the file
            total_days = total_days+1
        if (row[6]=="1" or row[6]=="") and (row[5]!=""):        # only the data observed for a single day can be kept
            productCode = row[0]
            stationNo = row[1]
            year = row[2]
            month = row[3]
            day = row[4]
            data = float(row[5])
            info.append([productCode,stationNo,round(data,2),str(year)+"/"+str(month)+"/"+str(day),total_days])
    fileobj.close()
    return info

def data_restore_monthly(fileName):
    '''The function will read the file, calculate the total rainfall for each month and restore 
    the results into a list with the headings removed'''
    info = []
    errorData=[]
    days_pm = 0
    data_pm = 0.00
    ndata_pm = 0
    productCode = ""
    stationNo = ""
    year = ""
    month = ""
    data = 0.0
    period = 0
    total_month = 0
    fileobj = open(fileName)
    reader = csv.reader(fileobj)
    for row in reader:
        if row[3].isdigit() and month.isdigit() and (not row[3]==month):    # if char of month(in the file) changes, increase the number of total month
            total_month = total_month+1
        errorData = error_data_monthly(errorData,row[6],row[4],row[4],row[3],row[2],data,month,year)
        if row[4] == "01" or row[4] == "1":                     # store monthly data at the beginning of next month
            if ndata_pm == days_pm:                             # the monthly data is valid only when number of recorded data = number of days
                info.append([productCode,stationNo,round(data_pm,2),str(year)+"/"+str(month),total_month])
            days_pm = 0
            data_pm = 0
            ndata_pm = 0
        productCode = row[0]                            # reassign new information to the virables for checks
        stationNo = row[1]
        year = row[2]
        month = row[3]
        data = row[5]
        period = row[6]
        days_pm = days_pm+1
        if data.replace('.','',1).isdigit():            # check if there is data record(field is float type)
            if not period.isdigit():                    # data with blank period will be treated as daily observation
                ndata_pm = ndata_pm+1   
            else:
                ndata_pm = ndata_pm+int(row[6])
            data_pm = data_pm + float(row[5])           # calculate total value of data(from daily to monthly)
    fileobj.close()
    if not len(errorData) == 0:                         # discard data which spans more than one month or is recorded multiple times
        info = remove_invalid(info,errorData)
    if mon.isdigit():                                   # change format of recorded data if aggregation type is 3
        info = reformat(info)
    return info

def data_restore_yearly(fileName):
    '''The function will read the file, calculate the total rainfall for each year and restore 
    the results into a list with the headings removed'''
    info = []
    eData=[]
    days_py = 0
    data_py = 0
    ndata_py = 0
    productCode = ""
    stationNo = ""
    year = ""
    data = 0.00
    period = 0
    fileobj = open(fileName)
    reader = csv.reader(fileobj)
    for row in reader:
        eData = error_data_yearly(eData,row[6],row[5],row[4],row[3],row[2],year,data)
        if (row[4] == "01" or row[4] == "1") and (row[3]=="01" or row[3]=="1"):         # check validity of last yearly data at the beginning of new year
            if ndata_py == days_py:                                                     # the yearly data is valid only when number of records = number of days
                info.append([productCode,stationNo,round(data_py,2),year,int(year)])
            days_py = 0
            data_py = 0
            ndata_py = 0
        productCode = row[0]
        stationNo = row[1]
        year = row[2]
        data = row[5]
        period = row[6]
        days_py = days_py+1
        if data.replace('.','',1).isdigit():                # there is data record(float type)
            if not period.isdigit():                        # treat data with blank period field as daily observation
                ndata_py = ndata_py+1
            else:
                ndata_py = ndata_py+int(row[6])
            data_py = data_py + float(row[5])               # sum the data in last year
    fileobj.close()
    if not len(eData)==0:                                   # if has, remove conflicting data or which spans more than one year
        info = remove_invalid(info,eData)
    return info
    
def sort_info():
    '''The function will sort the information according to the value of data 
    (from smallest to largest)'''
    return sorted(info,key = lambda x: x[2])    

def check_conB(olist,check):
    '''The function will check whether the number of results <= N/F
    and discard the elements caused the failure for this condition'''
    nlist = []
    if len(olist)>check:                    # if number of data is greater than N/F, set threshold to the (N/F-1)th data 
        discard = olist[-1][2]              # record the value of data to be discard
        for o in olist:                     # record data have the different value(data shares same value would cause this condition)
            if not discard in o:
                nlist.append(o)
            else:
                break
        return nlist
    else:
        return olist

def method_B():
    results = []
    order = int(len(info)/int(frequency))           # calculated the threshold N/F
    if t_threshold =='1':                           # type of threshold (1: extremely high value)
        slist.reverse()                             # reverse the data such that data ordered from largest to smallest
        threshold = slist[order-1][2]               # the value of calculated data will be the temporary threshold
        for i in slist:
            if i[2] >= threshold:                   # from the largest to smallest, check whether the data satisfys the threshold condition
                results.append(i)
            else:                                   # finalizing check since the rest data wont satisfy the condition
                break
    else:
        threshold = slist[order-1][2]               # the order_th smallest data will be the temporary threshold
        for i in slist:
            if i[2] <= threshold:                   # from the smallest to largest, check whether the data satisfys the threshold condition
                results.append(i)
            else:
                break
    results = check_conB(results,order)
    if not len(results) ==0:
        threshold = results[-1][2]
        print("The threshold from method b is: "+str(threshold)+"mm")
        print("Found "+str(len(results))+" data satisfies the threshold:")
        for r in results:
            print("          "+str(r[3])+": "+str(r[2])+"mm")
    else:
        print("In method B: No valid threshold was found !")

def raw_sol():
    '''The function will read the sorted information list, then return 
    the raw solutions of method a. The fisrt unsatisfying information
    will be attached at the end for further operation'''
    sol = []
    sol.append(slist[0])
    for i in range(1,len(slist)):           # repeatedly check whether the time difference between current data and each previous one is greater than the frequency
        for j in range (0,i):
            if abs(int(slist[i][4]-slist[j][4])) >= int(frequency):
                if not slist[i] in sol:
                    sol.append(slist[i])
            else:
                sol.append(slist[i])        # attach the first unsatisfying information
                return sol                  # end of generating raw solutions(no more data will be satisfying)
def method_A():
    rawSol = []
    rawSol = raw_sol()
    finalSol = []
    if len(rawSol) in range(0,2):   # false condition: 0: no solution; 1: single solution(invalid);
        print("In method A: No valid threshold was found !")    
    else:
        for r in rawSol:
            if not r[2] == rawSol[-1][2]:           # filtering the data which have the same value of the unsatisfying one
                finalSol.append(r)
        if not len(finalSol)==0:
            print("The threshold from method a is: "+str(finalSol[-1][2])+"mm")
            print("Found "+str(len(finalSol))+" data satisfy the threshold:")
            for f in finalSol:
                print("          "+str(f[3])+": "+str(f[2])+"mm")
        else:                                       # data may be unsatisfyiing from the beginning(such as '0's under daily aggregation)
            print("In method A: No valid threshold was found !")
                    
path_str = str(path_check(input("Please enter the path of the files(start with '/'):\n")))
aggregation = aggregation_check(input("Please choose the type of time series aggregation: \n1. Daily; \n2. Monthly; \n3. A specific month;\n4. Yearly;\nPlease choose from 1 to 4:\n"))
if aggregation == "3":
    mon = month_check(input("Please choose the month of aggregation: \n1. Jan; \n2. Feb; \n   ...\n12. Dec\nPlease choose from 1 to 12:\n"))
t_threshold = threshold_type_check(input("Please choose the type of the threshold: \n1. High;\n2. Low\nPlease choose from 1 to 2:\n"))
if aggregation =="1":
    info = data_restore_daily(path_str)
elif aggregation =="2" or aggregation =="3":
    info = data_restore_monthly(path_str)
elif aggregation =="4":
    info = data_restore_yearly(path_str)

frequency = freq_check(input("Please enter the frequency of the entries (positive integer ranging from 2 only):\n"))
slist = sort_info()
print("========================================")
method_B()
print("----------------------------------------")
method_A()
print("========================================")