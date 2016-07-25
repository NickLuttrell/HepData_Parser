# -*- coding: utf-8 -*-
"""
Created on Thu May 19 14:56:25 2016

@author: Nick Luttrell
"""

import sys
import re

def initFields(fignum, reaction, sqrt_s, output):
    output.write( "*dataend: \n\n" )
    output.write( "*dataset:\n" )
    output.write( "*location: {0}\n".format(fignum) )
    output.write( "*dscomment: \n" )
    output.write( "*obskey: \n" )
    output.write( "*reackey: {0}\n".format(reaction) )
    output.write( "*qual: SQRT(S) IN GEV:  {0}\n".format(sqrt_s) )
    output.write( "*xheader: \n")
    output.write( "*yheader: \n")
    
    
def reset():
    dataList = []
    qualifier = ""

    
def qualFormat(storage, output):
    qualifier = storage[0]
    for item in storage[1:len(storage)]:
        qualifier = qualifier + ": " + item
    output.write( "*qual: {0}\n".format(qualifier))
    qualifier = ""    


"""
userFormat(Command) - This function takes a line from the input file cmdfile
to arrange the columns for a given figure in the proper order and format. The relevant
arguments are:

'da#' where 'da' stands for 'data' and '#' should be replaced with a number 0 through 9 to specify the column
'st#' where 'st' stands for 'statistical error' and '#' should be replaced with a number 0 through 9 to specify the column. Assumes symmetric error
'sy##' where 'sy' stands for 'systematic error' and '##' should be replaced with numbers 0 through 9 to specify high and low error columns
'+# -#' in cases with asymmetrical high and low statistical errors

Note that indexing of columns begins at 0, and in cases where high and low systematic errors are equal, simply repeat the column number.
Each set of data with accompanying errors should be separated by a semicolon (spaces on both sides!) An ending semicolon should also appear.
In cases where there is a systematic error but not statistical, insert 'na' where the stat. error would be. HepData will not parse if this is not included!

An example line in format.txt might look like:  da0 ; da1 st2 sy43 ; da5 na sy66 ;
This creates a table in the form  x : y : y  (i.e. two y-values with error to be plotted against x)

"""

def userFormat(Command):
    
    try:
        data_format = Command
        print (data_format)
        return data_format
        
    except NameError:
        print ("IMPROPER INPUT! Enter a string with 'da0 ; da1 st2 sy43'")
        data_format = input("Enter the table format: ")
    except SyntaxError:
        print ("IMPROPER SYNTAX! Who knows what you did. Just try again.")
        data_format = input("Enter the table format: ")
        


def writeData(current_line, numcol, data_format, output):
    order = ""
    for item in data_format.split():
        try:
            if 'da' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                order += "%r" % float(current_line[int(col_index)])
            elif 'na' in item:
                order += " +- 0"
            elif '+' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                order += " +%r" % float(current_line[int(col_index)])
            elif '-' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                order += " -%r" % float(current_line[int(col_index)])
            elif 'st' in item:
                col_index = re.search(r"\d+(\.\d+)?", item)
                col_index = col_index.group(0)
                order += " +- %r" % float(current_line[int(col_index)])
            elif 'sy' in item:
                col_index = re.split('[a-z]+', item)
                col_index1 = col_index[1]
                try:
                    col_index2 = col_index[2]
                    order += " (DSYS=+%r, -%r)" % ( float(current_line[int(col_index1)]), float(current_line[int(col_index2)]) )
                except IndexError:
                    order += " (DSYS=+%r, -%r)" % ( float(current_line[int(item[2])]), float(current_line[int(item[3])]) )
                
            elif ';' in item:
                order += "; "
            else:
                print ("IMPROPER INPUT! Use a sequence like 'da0 ; da1 st2 sy43'")
                output.close()
                sys.exit()
                
        except IndexError:
            
            data_format = input("Index Error Occurred. Enter the table format: ")
            order = ""
            writeData(current_line, numcol, data_format, output)
    output.write( order + "\n" )

# End of header
