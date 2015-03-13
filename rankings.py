"""  Select method-specific variable rankings from TMVA output

     default use of input     out.txt 
                    output    Variable_rankings.txt

"""

import sys, getopt
import os
import math
from array import array


def main():

    inputfile = 'out.txt'
    outputfile = 'Variable_rankings.txt'
    numlines = 5
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],'o:c:vdih',['ifile=','ofile=','n='])
    except getopt.GetoptError, err:
        #print 'Error input: rankings.py -i <inputfile> -o <outputfile>'
        print str(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'rankings.py --ifile <inputfile> --ofile <outputfile>'
            sys.exit()
        elif opt == '--ifile':
            inputfile = arg
        elif opt == '--ofile':
            outputfile = arg
        elif opt == '--n':
            numlines += arg
    print "Opening inputfile : ", inputfile
    if outputfile == '':
        outputfile = inputfile
    if numlines == 5:
        numlines = sum(1 for line in open(inputfile))

    nindex = 0
    file = open(inputfile, 'r')
    outfile = open(outputfile,'w')
    oprint = False
    #print numlines
    for line in file:
        if (line.find("Ranking input variables (method specific)...") >=0):
            oprint = True
        if (line.find("Read method") >=0):
            oprint = False
        if oprint == True and (line.find("--- BDTG  ") >=0):
            newline1 = line.replace("---","",1).replace("BDTG","").strip()
            newline2 = newline1.replace(":","",1)
            outfile.write(newline2+'\n')
            #nindex+=1
        #if nindex == numlines:
        #    break
    file.close()
    outfile.close()

if __name__ == "__main__":
    main()
