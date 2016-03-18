import os
import datetime

def listdir_fullpath(d):
    return [os.path.join(d, f) for f in os.listdir(d)]

#def write_list_to_file(inlist, outfile):
#    with open(outfile, mode='a', encoding='utf-8') as outfile:
#        for line in inlist:
#            outfile.write(line)
#            outfile.write('\n')

def outfilename():
    prefix, ext, timestamp = 'search', '.txt', datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return '_'.join((prefix, timestamp + ext))

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

def searchany_infile(infilepath, *searchstring):
    searchresult = []
    with open(infilepath, 'r') as f:
        for num, line in enumerate(f, 1):
            if any(s in line for s in searchstring):
                searchresult.append((str(num), line))
    print('Searched file: ' + infilepath)
    return (infilepath, searchresult)

def multi_search(pathlist, *searchstring):
    if len(pathlist) < 1:
        return []
    else:
        if os.path.isdir(pathlist[0]):
            subpathlist = listdir_fullpath(pathlist[0])
            return multi_search(subpathlist, *searchstring) +multi_search(pathlist[1:], *searchstring)
        elif os.path.isfile(pathlist[0]):
            resultinfile = searchany_infile(pathlist[0], *searchstring)
            return [resultinfile] + multi_search(pathlist[1:], *searchstring)
        else:
            print('Do not know what is', pathlist[0])
            return multi_search(pathlist[1:], *searchstring)

def main():
    rootpath = input('Please specify the root path: ')
    searchstring = input('Please specify the search string: ')
    searchlist = searchstring.split(',')
    pathlist = listdir_fullpath(rootpath)
    allresults = multi_search(pathlist, *searchlist)
    # sort the result list based the number of hits
    allresults.sort(key=lambda t: len(t[1]), reverse=True)

    # save to file
    outfile = outfilename()
    outdir = './'
    outfilepath = os.path.join(outdir, outfile)
    savefile(allresults, outfilepath, rootpath, searchstring)

if __name__ == '__main__':
    main()
