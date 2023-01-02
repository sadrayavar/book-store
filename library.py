import random
import string


class LibraryBackEnd:
    database = None
    first = None
    last = None
    emptyRows = []

    def __init__(self, databaseName, newFile=False):
        if newFile is False:
            # read database
            rows = open(databaseName, 'r').readlines()

            for i in range(len(rows)):
                rows[i] = self.stringToList(rows[i])  # convert string to list
                if rows[i] == None:
                    self.emptyRows.append(i+1)  # set empty rows
                else:
                    if rows[i][0] == 'None':  # set first
                        self.first = i+1
                    if rows[i][1] == 'None':  # set last
                        self.last = i+1

            if (self.first == None):
                print('Database does not have a first book')
            if (self.last == None):
                print('Database does not have a last book')
            if not (self.first == None or self.last == None):
                self.database = databaseName
        else:
            try:  # create database
                open(databaseName, 'x')
            except:  # delete current database contents
                open(databaseName, 'w').write('')
            self.database = databaseName
            self.first = 1

    def add(self, ISBN, title, author, publisher, pubDate, category, supply, people):
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

    def remove(self, bookPlace):
        def temp(bookPlace):
            # define book and bookPlace
            book = self.readFromDatabase(bookPlace)
            if book is None:
                return
            formerPlace = book[0]
            nextPlace = book[1]

            if formerPlace == 'None' and nextPlace == 'None':
                pass
            elif formerPlace == 'None':
                self.first = nextPlace
                next = self.readFromDatabase(nextPlace)
                next[0] = formerPlace
                self.writeToDatabase(next, nextPlace)
            elif nextPlace == 'None':
                self.last = formerPlace
                former = self.readFromDatabase(formerPlace)
                former[1] = nextPlace
                self.writeToDatabase(former, formerPlace)
            else:
                former = self.readFromDatabase(formerPlace)
                former[1] = nextPlace
                self.writeToDatabase(former, formerPlace)

                next = self.readFromDatabase(nextPlace)
                next[0] = formerPlace
                self.writeToDatabase(next, nextPlace)

            # edit book
            self.writeToDatabase('\n', bookPlace)

            # add empty row to emptyRows list
            self.emptyRows.append(bookPlace)

        if isinstance(bookPlace, list):
            for place in bookPlace:
                temp(place)
        else:
            temp(bookPlace)

    def search(self, searchParam, value):
        try:
            value = int(value)
        except:
            pass

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

    def sort(self, sortParam):
        numOfBooks = len(open(self.database, 'r').readlines())
        if (numOfBooks < 2):
            return None
        if (sortParam == "ISBN"):
            for i in range(numOfBooks-1):
                book = self.readFromDatabase(i)
                nextBook = self.readFromDatabase(i+1)
                if (book[2] > nextBook[2]):
                    holder = book[:2]
                    book = nextBook[:2]+book[2:]
                    nextBook = holder+nextBook[2:]
                    self.remove(i+1)
                    self.writeToDatabase(book+'\n', i+1)
                    self.remove(i)
                    self.writeToDatabase(nextBook+'\n', i)

    def display(self):
        numOfBooks = len(open(self.database, 'r').readlines())
        i = 0
        while (i < numOfBooks):
            book = self.readFromDatabase(i)
            i += 1
            print(book[2:])

    def edit(self, line, editParam, newValue, innerParam=None):
        if (editParam == 'ISBN'):
            editParam = 0
        elif (editParam == 'title'):
            editParam = 1
        elif (editParam == 'author'):
            editParam = 2
        elif (editParam == 'publisher'):
            editParam = 3
        elif (editParam == 'pubDate'):
            editParam = 4
        elif (editParam == 'category'):
            editParam = 5
        elif (editParam == 'supply'):
            editParam = 6
        elif (editParam == 'people'):
            editParam = 7

        book = self.readFromDatabase(line)
        if innerParam is None:
            book[editParam+2] = newValue
        else:
            book[editParam+2][innerParam] = newValue
        self.writeToDatabase(book, line)

        pass

    # helper methods

    def bookCount(self):
        if self.first == None:
            return 0
        else:
            book = self.readFromDatabase(self.first)
            nextPlace = book[1]
            output = 1
            while nextPlace != "None":
                book = self.readFromDatabase(nextPlace)
                nextPlace = book[1]
                output += 1
            return output

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
        try:
            book = book.split(',')
            book[-1] = book[-1].split(':')
            book[-3] = book[-3].split(':')
            for i in range(len(book[-1])):
                try:
                    book[-1][i] = int(book[-1][i])
                except:
                    pass
            for i in range(len(book)-1):
                try:
                    book[i] = int(book[i])
                except:
                    pass
            return book
        except:
            return None

    def paramToString(self, former, next, ISBN, title, author, publisher, pubDate, category, supply, people):
        def temp(list):
            return ':'.join(str(item) for item in list)
        return f'{former},{next},{ISBN},{title},{author},{publisher},{pubDate},{temp(category)},{supply},{temp(people)}\n'


class LibraryFrontEnd:
    back = None
    border = '\n###########################################\n'
    ranValue = False

    def __init__(self):
        self.back = self.configDatabase()
        self.talkToMe()

    def configDatabase(self):
        file = None
        inp = None
        print(f'\n\nWelcome!{self.border}')
        while not (inp == '1' or inp == '2'):
            print(
                'Select start method:\n1- Create a new database\n2- Import database')
            inp = input()
            print()
            if (inp == '1'):
                print(
                    'Your Database is created with the name of: database.csv')
                file = LibraryBackEnd('database.csv', True)
            elif (inp == '2'):
                while file == None:
                    print('Enter your database name: ("0" for default database name)')
                    fileName = input()
                    print('\nYour Database is connecting to app...\n')
                    if fileName == "0":
                        file = LibraryBackEnd('database.csv')
                    else:
                        try:
                            open(fileName, 'r')
                            file = LibraryBackEnd(fileName)
                        except:
                            print(f'\nStandard database format:\nformer,next,ISBN,title,author,publisher,pubDate,category1:...,supply,personID1:...\nand also should have exactly one first and one last\nexample:\nNone,2,...\n1,None,...\n')
                            file = None
        print(f'\nNow lets manage this library\n{self.border}')
        return file

    def talkToMe(self):
        while True:
            print(
                'Select one of the options below:\n1- Add\n2- Remove\n3- Search\n4- Sort\n5- Edit\n6- Display')
            inp = input()
            print()

            if (inp == '1'):
                self.addBook()
            elif (inp == '2'):
                self.removeBook()
            elif (inp == '3'):
                self.searchBook()
            elif (inp == '4'):
                self.sortBooks()
            elif (inp == '5'):
                self.editBooks()
            elif (inp == '6'):
                print(f'Double click on {self.back.database} (EASY)')
            else:
                print('Select one of the options abow')

            print(self.border)

    def addBook(self):

        def inputString(what, rang):
            key = None
            while key == None:
                if self.ranValue == False:
                    print(f'Enter {what}:')
                    key = input()
                if key == 'r' or self.ranValue == True:
                    self.ranValue = True
                    method = string.ascii_letters
                    length = random.randint(rang[0], rang[1]+1)
                    return ''.join(random.choice(method) for i in range(length))
                else:
                    if (len(key) < rang[0] or len(key) > rang[1]):
                        key = None
                        print(
                            f'\n{what} length should be {rang[0]}-{rang[1]}')
                    else:
                        return key

        def inputnumber(what, ran):
            key = None
            while key == None:
                if self.ranValue == False:
                    print(f'Enter {what}:')
                    key = input()
                if key == 'r' or self.ranValue == True:
                    self.ranValue = True
                    if isinstance(ran, int):
                        stop = 1
                        for i in range(ran):
                            stop *= 10
                        temp = random.randint(0, stop)
                        while len(str(temp)) < 13:
                            temp = '0'+str(temp)
                        return temp
                    else:
                        return random.randint(ran[0], ran[1]+1)
                else:
                    try:
                        int(key)
                    except:
                        key = None
                        print(f'\n{what} should be an integer number')
                        continue
                    if isinstance(ran, int):
                        if not len(str(key)) == ran:
                            key = None
                            print(f'\n{what} length should be {ran}')
                            continue
                    else:
                        if int(key) < ran[0] or int(key) > ran[1]:
                            key = None
                            print(
                                f'\n{what} should be {ran[0]}-{range[1]}')
                            continue
                    return int(key)

        print('Enter "r" to add a random book')

        # input ISBN
        ISBN = inputnumber('ISBN', 13)
        doesExist = self.back.search('ISBN', ISBN)
        if (doesExist):
            print(f'{ISBN} is already in the database: {doesExist}')
            return

        # input title
        title = inputString('Title', [5, 30])

        # input author
        firstName = inputString('Author First Name', [5, 15])
        lastName = inputString('Author Last Name', [5, 25])
        author = firstName+' '+lastName

        # input publisher
        publisher = inputString('Publisher', [5, 30])

        # input publishDate
        pubYear = inputnumber('Publish year', 4)
        pubMonth = inputnumber('Publish month', [1, 12])
        pubDay = inputnumber('Publish day', [1, 31])
        pubDate = int(str(pubYear)+str(pubMonth)+str(pubDay))

        # input category
        if not self.ranValue:
            print('How many category do you want to add')
        howMany = inputnumber('Category Number', [0, 11])
        category = []
        for i in range(howMany):
            category.append(inputString('Category', [4, 10]))

        # input supply
        supply = inputnumber('Supply', [0, 100])

        # input people
        if not self.ranValue:
            print('How many people do you want to add')
        howMany = inputnumber('People Number', [0, supply+1])
        people = []
        for i in range(howMany):
            people.append(inputnumber('People ID', 10))

        self.back.add(ISBN, title, author, publisher,
                      pubDate, category, supply, people)
        print(f'Your record added to row:\t{self.back.last}')
        self.ranValue = False

    def removeBook(self):
        # define remove option
        removeParam = self.selectOptions('select remove option:')

        print(f'Enter {removeParam[1]} value:')
        value = input()
        rows = self.back.search(removeParam[1], value)
        message = 'Book(s) in '
        if rows is not False:
            for i in rows:
                self.back.remove(i)
                message += str(i)+', '
            message = message[:-2]
            message += ' has been removed\n'
            print(message)

        else:
            print('Book(s) not found')

    def searchBook(self):
        # define option
        searchParam = self.selectOptions('select search option:')

        # define value
        print(f'Enter {searchParam[1]} value:')
        value = input()

        rows = self.back.search(searchParam[1], value)

        message = 'Book(s) are in: '
        if rows is not False:
            for i in rows:
                message += str(i)+', '
            message = message[:-2]
            print(message)

        else:
            print('Book(s) not found')

    def sortBooks(self):
        sortParam = self.selectOptions('select sort option:')
        if (sortParam == 'people'):  # sort by number list
            pass
        elif (sortParam == 'category'):  # sort by string list
            pass
        elif (sortParam == 'ISBN' or sortParam == 'pubDate' or sortParam == 'supply'):  # sort by number
            pass
        else:  # sort by string
            pass
        self.back.sort(sortParam)

    def editBooks(self):
        # input lines
        lines = []
        while True:
            print('Enter the row number (0 if its done)')
            inp = input()

            if (inp == '0'):
                if (len(lines) == 0):
                    print('Please select some lines')
                else:
                    break
            else:
                # check if the line is empty
                empty = False
                lineCount = len(open(self.back.database, 'r').readlines())
                if (int(inp) > lineCount):
                    empty = True
                for emptyRow in self.back.emptyRows:
                    if int(inp) is emptyRow:
                        empty = True
                        break

                if empty:
                    print('line is empty')
                else:
                    lines.append(int(inp)+1)

        editParam = self.selectOptions('\nWhat do you want to edit:')

        if (editParam[1] == 'people' or editParam[1] == 'category'):
            print(
                f'Enter the number of {editParam[1]} that you want to edit:\nExample: 1 for first')
            innerParam = input()
            innerParam = int(innerParam)-1

            for line in lines:
                book = self.back.readFromDatabase(line)
                print(
                    f'current value is:\t{book[int(editParam[0])+1][innerParam]}\nEnter new value:')
                newValue = input()

                self.back.edit(line, editParam[1], newValue, innerParam)
        else:
            for line in lines:
                book = self.back.readFromDatabase(line)
                print(
                    f'current value is:\t{book[int(editParam[0])+1]}\nEnter new value:')
                newValue = input()

                self.back.edit(line, editParam[1], newValue)

    # debug methods

    def selectOptions(self, text):
        param = None
        while param is None:
            print(text)
            print('1- ISBN')
            print('2- Title')
            print('3- Author')
            print('4- Publisher')
            print('5- Publish Date')
            print('6- Category(s)')
            print('7- Supply')
            print('8- People')

            param = input()
            param = [param]
            print()

            if param[0] == '1':
                param.append('ISBN')
            elif param[0] == '2':
                param.append('title')
            elif param[0] == '3':
                param.append('author')
            elif param[0] == '4':
                param.append('publisher')
            elif param[0] == '5':
                param.append('pubDate')
            elif param[0] == '6':
                param.append('category')
            elif param[0] == '7':
                param.append('supply')
            elif param[0] == '8':
                param.append('people')
            else:
                param = None

        return param


LibraryFrontEnd()
