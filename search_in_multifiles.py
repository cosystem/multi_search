import os
import re
import datetime

def listdir_fullpath(directory):
    # return [os.path.join(d, f) for f in os.listdir(d)] # os.listdir() is slow
    return [item.path for item in os.scandir(directory)] # os.scandir() is faster and only available after Python 3.5

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

def searchany_infile(infilepath, *searchstring, verbose=False):
    searchresult = []
    with open(infilepath, 'r') as f:
        if verbose:
            print(infilepath) # for debugging
        try:
            for num, line in enumerate(f, 1):
                if any(s in line for s in searchstring):
                    searchresult.append((str(num), line))
        except UnicodeDecodeError as e:
            print('Error for reading', infilepath+':', e)
    #print('Searched file: ' + infilepath)
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

def makerule(pattern):
    def filename_rule(filename, *arg):
        return re.search(pattern, filename)
    return filename_rule

# traverse dir tree and list files with os.walk()
def selectfiles(searchpath, filerules=lambda x, y:True, dirrules=lambda x: True):
    '''
    traverse dir and return a generator for all files
    options:
        filerules: select files based on certain rule (arg: path, filename; return True/False)
        dirrules: select directory (arg: path; retrun True/False, default)
    '''
    for path, dirnames, filenames in os.walk(searchpath):
        if dirrules(path):
            for filename in filenames:
                if filerules(filename, path):
                    yield os.path.join(path, filename)

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
    filename_rule = makerule('R$')


if __name__ == '__main__':
    # main()
    filename_rule = makerule('txt$')
    for i in selectfiles(rootpath, filerules=filename_rule):
        print(i)
