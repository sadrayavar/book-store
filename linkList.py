class Library:
    database = None
    first = None
    last = None

    def __init__(self, databaseName, newFile=False):
        self.database = databaseName

        if newFile is False:
            # read database
            rows = open(self.database, 'r').readlines()

            # search for first and last
            for i in range(len(rows)):

                # convert string to list
                rows[i] = self.stringToList(
                    rows[i])
                if rows[i][0] == 'None':  # set first
                    self.first = i
                if rows[i][1] == 'None':  # set last
                    self.last = i

            if (self.first == None):
                print('Database does not have a first book')
            if (self.last == None):
                print('Database does not have a last book')
        else:
            try:  # create database
                open(databaseName, 'x')
            except:  # delete current database contents
                open(databaseName, 'w').write('')
            self.first = 0


b = Library('database.csv', True)
