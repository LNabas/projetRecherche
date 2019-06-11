def read_csv( filename ):
    results = []
    with open( filename, 'r' ) as file:
        for line in file:
            line    = line.rstrip()
            columns = line.split( ';' )
            results.append( columns )
    return results
path    = "C:\\personnel\\python\\blog\\compare_csv"
before  = psutil.virtual_memory()
results = read_csv( path + "\\sample1.csv" )
after   = psutil.virtual_memory()
print( "psutil.size =", after.used - before.used )


def split_file(filename, temporary_radix, rows_count, get_key):
    """ Split file
        Split input file in several sorted files of rows_count lines.

        Parameters:
            filename: input full path name
            temporary_radix: full path radix to create splitted sorted files
            get_key: the function to extract sorting key from columns

        Return:
            number of generated files
    """
    # local variables
    file_counter = 0

    # write sub file
    def write_file(filename, rows):
        rows.sort(key=get_key)
        with open(filename, 'w') as output_file:
            for r in rows:
                print(*r, sep=';', end='\n', file=output_file)

    # loop
    with open(filename, "r") as input_file:
        rows = []
        for line in input_file:
            line = line.rstrip()
            columns = line.split(';')
            rows.append(columns)
            if len(rows) == rows_count:
                write_file(temporary_radix % (0, file_counter), rows)
                rows.clear()
                file_counter += 1
        if len(rows) > 0:
            write_file(temporary_radix % (0, file_counter), rows)
            file_counter += 1
    return file_counter


def fusion(temporary_radix, depth, id1, id2, new_id, get_key):
    """ File fusion
        F(id1) + F(id2) -> F(new_id)

        Parameters:
            temporary_radix: full path radix to read/write temporary files
            depth: depth
            id1: id of 1st file ("%s\\temp_%d_%d.csv" % ( temporary_path, depth, id1 ))
            id2: id of 2nd file ("%s\\temp_%d_%d.csv" % ( temporary_path, depth, id2 ))
            new_id: id of the new file ("%s\\temp_%d_%d.csv" % ( temporary_path, depth+1, new_id ))
            get_key: function to extract the columns from the line
    """
    # local variables
    columns1 = None
    columns2 = None
    name1 = temporary_radix % (depth, id1)
    name2 = temporary_radix % (depth, id2)
    name_o = temporary_radix % (depth + 1, new_id)

    # compare
    def compare():
        if None == columns1:
            return 1
        elif None == columns2 or get_key(columns1) < get_key(columns2):
            return -1
        else:
            return 1

    # open the files
    with open(name1, "r") as inFile1, \
            open(name2, "r") as inFile2, \
            open(name_o, "w") as outFile:
        while True:
            # read lines
            if not columns1:
                line = inFile1.readline().rstrip()
                if 0 != len(line):
                    columns1 = line.split(';')
            if not columns2:
                line = inFile2.readline().rstrip()
                if 0 != len(line):
                    columns2 = line.split(';')
            if not columns1 and not columns2:
                break
            # compare
            if compare() < 0:
                print(*columns1, sep=';', end='\n', file=outFile)
                columns1 = None
            else:
                print(*columns2, sep=';', end='\n', file=outFile)
                columns2 = None
    # finalize
    unlink(name1)
    unlink(name2)

    def sort_file(input_filename, \
                  sorted_filename, \
                  rows_count, \
                  temporary_radix="C:\\Temp\\temp_%d_%d.csv", \
                  get_key=lambda c: c):
        """Sort file

           Parameters:
               input_filename: input file name (file to sort)
               sorted_filename: output file name (sorted file)
               temporary_radix: full path radix name for temporary files ({path}\\temp_{depth}_{id}.csv)
               rows_count: number of rows per file in splitting phasis
               get_key: key function to sort
        """
        # initialize
        count = split_file(input_filename, temporary_radix, rows_count, get_key)
        depth = 0

        # main loop: keep 2 files, join them into one sorted file until all files are consumed
        while 1 < count:
            n = 0
            for i in range(0, count, 2):
                j = i + 1
                if count == j:
                    rename(temporary_radix % (depth, i), \
                           temporary_radix % (depth + 1, n))
                else:
                    fusion(temporary_radix, depth, i, j, n, get_key)
                n += 1
            depth += 1
            count = n

        # rename temporary file into attempted file
        rename(temporary_radix % (depth, 0), sorted_filename)

        get_key = lambda c: (c[1],)
        sort_file("C:\\personnel\\python\\blog\\compare_csv\\sample1.csv", \
                  "C:\\personnel\\python\\blog\\compare_csv\\sample1_sorted.csv", \
                  10000, \
                  "C:\\personnel\\python\\blog\\compare_csv\\temp\\temp_%d_%d.csv", \
                  get_key)