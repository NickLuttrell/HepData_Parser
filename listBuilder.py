datafile = open('RawList.lis', 'r')

output = open("AuAu62p4.lis", "w")


for line in datafile:
    nextline = line.strip() # Remove excess white space.
    nextline = nextline.split()
    for item in nextline:
        if ".fz" in item:
            output.write("/star/data03/pwg/jdb/AuAu62p4/StarSim/" + item + "\n")