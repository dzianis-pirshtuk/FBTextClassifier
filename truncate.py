#!/usr/bin/python

import sys
import os
import os.path

def main():
    usage = sys.argv[0] + ' <Input CSV File> <Output CSV File> <Number of lines to keep>'
    
    if len(sys.argv) != 4:
        print usage
        print 'Invalid number of arguments'
        sys.exit(1)
    
    try:
        inFile = open(sys.argv[1], 'rb')
    except:
        print usage
        print 'Error opening input CSV file'
        sys.exit(1)
    
    try:
        outFile = open(sys.argv[2], 'wb')
    except:
        print usage
        print 'Error opening output CSV file'
        sys.exit(1)
    
    try:
        numLines = int(sys.argv[3])
    except:
        print usage
        print 'Number of lines must be an integer'
        sys.exit(1)
    
    
    for i in range(0, numLines):
        outFile.write(inFile.readline())
    
    inFile.close()
    outFile.close()
    
    print
    print 'Done!'
    print
    
if __name__ == '__main__':
    main()
