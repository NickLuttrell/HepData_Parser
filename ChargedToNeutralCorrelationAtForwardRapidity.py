# -*- coding: utf-8 -*-
"""
Created on Wed May 18 10:54:20 2016

@author: Nick Luttrell
"""

import header

    
def easyTable(dataList, cmdlist, cmd_index):
    print ("Stepped into Easytable")

    numcol = len(dataList[2])
    print ("There are {0} columns\n".format(numcol))
    try:
        data_format = header.userFormat(cmdlist[cmd_index])
    except IndexError:
        print ("Index Error from cmdlist.")
        data_format = input("Enter the table format: ")
    
    columns = "x"
    for x in data_format[0:len(data_format) - 2]:
        if x == ";":
            columns = columns + ": y"
    output.write( "*data: {0}\n".format(columns) )
    
    startnum = 1
    for entry in dataList[startnum:len(dataList)]:
        header.writeData(entry, numcol, data_format, output)
 
       
    
def hardTable(dataList, cmdlist, cmd_index):
    print ("Stepped into Hardtable")
    storage = dataList[1]
    header.qualFormat(storage, output)
    
    numcol = len(dataList[2])
    print ("There are {0} columns\n".format(numcol))
    try:
        data_format = header.userFormat(cmdlist[cmd_index])
    except IndexError:
        print ("Index Error from cmdlist.")
        data_format = input("Enter the table format: ")
    
    columns = "x"
    for x in data_format[0:len(data_format) - 2]:
        if x == ";":
            columns = columns + ": y"
    output.write( "*data: {0}\n".format(columns) )
    
    startnum = 2
    for entry in dataList[startnum:len(dataList)]:
        try:
            float(entry[0])
            header.writeData(entry, numcol, data_format, output)
        except ValueError:
            print ("Creating subtable")
            header.initFields(fignum, reaction, sqrt_s, output)
            header.qualFormat(entry, output)
            output.write( "*data: {0}\n".format(columns) )

    
    
# Begin Main()
    
output = open("output.txt", "w")
cmdfile = open("C:\\Users\\Nick\Documents\\Hepdata\\2015\\Data_Files\\ChargedToNeutralCorrelationAtForwardRapidity\\format.txt", "r")

cmd_index = 0
cmdlist = []
for line in cmdfile:
    cmdlist.append(line)

# Define any values that remain unchanged throughout the paper (usually the reaction)
fignum = ""
delimiter = "Fig"
reaction = "AU AU --> X"
sqrt_s = "200"
    
dataList = []
datafile = open("C:\\Users\\Nick\Documents\\Hepdata\\2015\\Data_Files\\ChargedToNeutralCorrelationAtForwardRapidity\\data.txt", 'r')

for line in datafile:
    nextline = line.strip() # Remove excess white space.
    nextline = nextline.split()
    if not line.strip():
        continue
    elif delimiter not in nextline[0]:
        dataList.append(nextline)
    elif delimiter in nextline[0]:
        if dataList:            # Ensures that it doesn't fail at the first figure.
            print (dataList[len(dataList)-1])
            try:
                print (fignum)
                float(dataList[1][0])  # Check to see if there is a qualifier.
                header.initFields(fignum, reaction, sqrt_s, output)
                easyTable(dataList, cmdlist, cmd_index)
                cmd_index += 1
            except ValueError:
                header.initFields(fignum, reaction, sqrt_s, output)
                hardTable(dataList, cmdlist, cmd_index)
                cmd_index += 1
        fignum = "Figure" + nextline[1]
        dataList = []
        print (cmd_index)
    
output.write( "*E:")

datafile.close()
cmdfile.close()
output.close()