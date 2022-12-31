# former, next, ISBN, title, author, publisher, pubDate, category, supply, people
# edit sort display
# 2915972317011, 'book name', 'sadra yavarzadeh herisi', 'entesharat sadrayalastLine', 2022012026, ['falsafe', 'comedy', 'dram', 'adventures', 'not adventures'], 999,  [4407469698, 4407469698, 4407469698]
class Library:
    database = None
    first = None
    last = None
    emptyRows = []

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
            if (self.first == None or self.last == None):
                exit()
        else:
            try:  # create database
                open(databaseName, 'x')
            except:  # delete current database contents
                open(databaseName, 'w').write('')
            self.first = 1

    def add(self, ISBN, title, author, publisher, pubDate, category, supply, people):
        # check if the book is added already
        doesExist = self.search("ISBN", ISBN)
        if (doesExist):
            print(f'{ISBN} is already in the database: {doesExist[0]}')
        else:
            '''
            data:
            last book place
            next empty row = last book place (after add)

            functions:
            1- get next empty row
            2- edit last book to point to the next empty row
            3- insert book to the next empty row
            4- update last book place
            '''
            lastBookPlace = self.last
            nextEmptyRow = None

            # get next empty row
            if (len(self.emptyRows) == 0):
                if (self.last == None):
                    nextEmptyRow = 1
                else:
                    tempLines = open(self.database, 'r').readlines()
                    nextEmptyRow = len(tempLines)+1
            else:
                nextEmptyRow = self.emptyRows.pop()

            # edit last book to point to the next empty row
            if (lastBookPlace != None):
                lastBook = self.readFromDatabase(lastBookPlace)
                lastBook[1] = nextEmptyRow
                self.writeToDatabase(lastBook, lastBookPlace)

            # insert book to the next empty row
            book = self.paramToString(
                lastBookPlace, None, ISBN, title, author, publisher, pubDate, category, supply, people)
            self.writeToDatabase(book, nextEmptyRow)

            # update last book place
            self.last = nextEmptyRow

    def remove(self, rowList):
        def temp(where):
            # define book and bookplace
            place = self.search('ISBN', where)[0]
            this = self.readFromDatabase(place)

            # define former book
            former = self.readFromDatabase(this[0])
            former[1] = this[1]
            self.writeToDatabase(former, this[0])

            # define next book
            next = self.readFromDatabase(this[1])
            next[0] = this[0]
            self.writeToDatabase(next, this[1])

            # edit book
            self.writeToDatabase('\n', place)

            # add empty row to emptyRows list
            self.emptyRows.append(place)

        if isinstance(rowList, list):
            for row in rowList:
                temp(row)
        else:
            temp(rowList)

    def search(self, searchParam, value):
        if (searchParam == 'ISBN'):
            key = 2
        elif (searchParam == 'title'):
            key = 3
        elif (searchParam == 'author'):
            key = 4
        elif (searchParam == 'publisher'):
            key = 5
        elif (searchParam == 'pubDate'):
            key = 6
        elif (searchParam == 'category'):
            key = 7
        elif (searchParam == 'supply'):
            key = 8
        elif (searchParam == 'people'):
            key = 9
        else:
            print('search parameter must be one of the values below:\ntitle\nauthor\npublisher\npubDate\ncategory\nsupply\npeople')
            exit()

        output = []
        where = self.first
        canBreak = False

        def turnBookItemsToList(book):
            for i in range(len(book)):  # turn not list keys to list
                if (not (isinstance(book[i], list))):
                    temp = []
                    temp.append(book[i])
                    book[i] = temp

        while (where != 'None'):
            book = self.readFromDatabase(where)
            if (book == None):  # returns None if database is empty
                return False

            turnBookItemsToList(book)

            for item in book[key]:
                if (value == item):  # add to output list
                    output.append(where)
                    where = book[1][0]
                    break
                elif (book[1][0] == 'None'):
                    canBreak = True
                    break
            where = book[1][0]
            if (canBreak):
                break

        if (len(output) == 0):
            return False
        else:
            return output

    # helper functions

    def readFromDatabase(self, where):
        where -= 1
        try:
            rows = open(self.database, 'r').readlines()
            return self.stringToList(rows[where])
        except:
            return None

    def writeToDatabase(self, what, where):
        where -= 1
        if (not (isinstance(what, str))):
            what = self.paramToString(
                what[0], what[1], what[2], what[3], what[4], what[5], what[6], what[7], what[8], what[9])

        rows = open(self.database, 'r').readlines()

        if (len(rows) <= where):
            rows.append(what)
        else:
            rows[where] = what

        file = open(self.database, 'w')
        file.writelines(rows)
        file.close()

    def stringToList(self, book):
        book = book.split(',')
        book[-1] = book[-1].split(':')
        book[-3] = book[-3].split(':')
        for i in range(len(book[-1])):
            book[-1][i] = int(book[-1][i])
        for i in range(len(book)-1):
            try:
                book[i] = int(book[i])
            except:
                pass
        return book

    def paramToString(self, former, next, ISBN, title, author, publisher, pubDate, category, supply, people):
        def temp(list):
            return ':'.join(str(item) for item in list)
        return f'{former},{next},{ISBN},{title},{author},{publisher},{pubDate},{temp(category)},{supply},{temp(people)}\n'


b = Library('database.csv', True)

b.add(2915972317010, '', '', '', 0, [
      'ali', 'hasan', 'qolam'], 0,  [1, 2, 3, 4])
b.add(2915972317011, '', '', '', 0, ['ali', 'hasan'], 0,  [1, 2, 3])
b.add(2915972317014, '', '', '', 0, ['ali', ''], 0,  [1, 2])
b.remove(2915972317011)
b.add(2975972317010, '', '', '', 0, [
      'ali', 'hasan', 'qolam'], 0,  [1, 2, 3, 4])
b.add(2915973317011, '', '', '', 0, ['ali', 'hasan'], 0,  [1, 2, 3])
b.add(2914972317014, '', '', '', 0, ['ali', ''], 0,  [1, 2])
print(b.search('category', 'hasan'))
print(b.search('category', 'qolam'))
print(b.search('category', 'ali'))
