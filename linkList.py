# former, next, ISBN, title, author, publisher, publishDate, category, supply, people
# add remove edit get sort display
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
            self.first = 0
        print()

    def add(self, ISBN, title, author, publisher, publishDate, category, supply, people):

        if (self.getPlace(ISBN) == None):
            formerLast = self.last  # save last in temp
            self.setLast()  # increment last
            self.editLastBook(formerLast)  # replace None in the next parameter
            book = self.paramToString(formerLast, None, ISBN, title,
                                      author, publisher, publishDate, category, supply, people)
            self.writeToDatabase(book, self.getNext())
        else:
            print(f'ISBN {ISBN} is in the row: {self.getPlace(ISBN)}')


    def getPlace(self, id):
        link = self.first
        while (True):
            book = self.readFromDatabase(link)
            if (book == None):
                return None
            if (id == book[2]):
                return link
            else:
                if (book[1] == 'None'):
                    return None
                else:
                    link = book[1]

    # helper functions

    def editLastBook(self, formerLast):
        lastBook = self.readFromDatabase(formerLast)
        if (lastBook != None):
            lastBook[1] = self.last
            l = lastBook
            tempBook = self.paramToString(l[0], l[1], l[2], l[3], l[4],
                                          l[5], l[6], l[7], l[8], l[9])
            self.writeToDatabase(tempBook, formerLast)

    def getNext(self):
        if (self.last == None):
            return 2
        else:
            if (len(self.emptyRows) == 0):
                return self.last + 2
            else:
                return self.emptyRows[-1]

    def setLast(self):
        if (self.last == None):
            self.last = 0
        else:
            if (len(self.emptyRows) == 0):
                self.last += 1
            else:
                self.emptyRows.pop()

    def readFromDatabase(self, where):
        try:
            rows = open(self.database, 'r').readlines()
            return self.stringToList(rows[where])
        except:
            return None

    def writeToDatabase(self, what, where):
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

    def paramToString(self, former, next, ISBN, title, author, publisher, publishDate, category, supply, people):
        def temp(list):
            return ':'.join(str(item) for item in list)
        return f'{former},{next},{ISBN},{title},{author},{publisher},{publishDate},{temp(category)},{supply},{temp(people)}\n'


b = Library('database.csv', True)
b.add(2915972317010, '', '', '', 0, [''], 0,  [1])
b.add(2915972317011, '', '', '', 0, [''], 0,  [1])
b.add(2915972317014, '', '', '', 0, [''], 0,  [1])
