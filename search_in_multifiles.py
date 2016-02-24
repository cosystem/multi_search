import os

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

#def write_list_to_file(inlist, outfile):
#    with open(outfile, mode='a', encoding='utf-8') as outfile:
#        for line in inlist:
#            outfile.write(line)
#            outfile.write('\n')

def savefile(intuplelist, outfile, rootpath, searchstring):
    with open(outfile, 'a', encoding = 'utf-8') as myfile:
        myfile.write(' '.join(('Search', '\"'+searchstring+'\"', 'in all sub-directories under', rootpath)))
        myfile.write('\n')
        myfile.write('\n')
        myfile.write('=================================')
        myfile.write('\n')
        for filename, linenum_line_list in intuplelist:
            myfile.write(filename)
            myfile.write('\n')
            myfile.write('\n')
            if len(linenum_line_list) > 0:
                for linenum, line in linenum_line_list:
                    myfile.write(' '.join(('---- line No.', linenum+':', ' ', line)))
                    myfile.write('\n')
            else:
                myfile.write('---- no hits')
                myfile.write('\n')
            myfile.write('==================================')
            myfile.write('\n')

def searchinfile(infilepath, searchstring):
    searchresult = []
    with open(infilepath, 'r') as f:
        for num, line in enumerate(f, 1):
            if searchstring in line:
                searchresult.append((str(num), line))
    print('Searched file: ' + infilepath)
    return (infilepath, searchresult)

def multi_search(pathlist, searchstring, outlist):
    if len(pathlist) == 1:
        if os.path.isdir(pathlist[0]):
            subpathlist = listdir_fullpath(pathlist[0])
            multi_search(subpathlist, searchstring, outlist)
        elif os.path.isfile(pathlist[0]):
            resultinfile = searchinfile(pathlist[0], searchstring)
            outlist.append(resultinfile)
        else:
            print('Do not know what is', pathlist[0])
    elif len(pathlist) > 1:
        if os.path.isdir(pathlist[0]):
            subpathlist = listdir_fullpath(pathlist[0])
            multi_search(subpathlist, searchstring, outlist)
            multi_search(pathlist[1:], searchstring, outlist)
        elif os.path.isfile(pathlist[0]):
            resultinfile = searchinfile(pathlist[0], searchstring)
            outlist.append(resultinfile)
            multi_search(pathlist[1:], searchstring, outlist)
        else:
            print('Do not know what is', pathlist[0])
    else:
        pass
    return outlist

def main():
    rootpath = input('Please specify the root path: ')
    searchstring = input('Please specify the search string: ')
    pathlist = listdir_fullpath(rootpath)
    result_storage = []
    allresults = multi_search(pathlist, searchstring, result_storage)
    # sort the result list based the number of hits
    allresults.sort(key=lambda t: len(t[1]), reverse=True)

    # save to file
    outfilename = 'search_results.txt'
    outfilepath = os.path.join(rootpath, outfilename)
    savefile(allresults, outfilepath, rootpath, searchstring)

if __name__ == '__main__':
    main()
