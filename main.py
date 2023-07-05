import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3

from homePage import HomePage
from listSelectionPage import ListSelectionPage
from revisionPage import RevisionPage
from addQuestionsPage import AddQuestionsPage
from timeTravelPage import TimeTravelPage
from deleteListsPage import DeleteListsPage

import os
import psutil 
import time
#main class via which the pages of this application are controlled and the database is created.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 40, 100, 100)#set dimensions of the window
        self.stack = QStackedWidget(self)#this will hold all pages of the application ... dynamically producing pages would be better in a very large application
        #used to chech the application isn't getting too slow or resauce heavy
        start = int(round(time.time() * 1000))
        process = psutil.Process(os.getpid())
        #create instances of each page in the application
        self.homePage = HomePage(self)
        self.listSelectionPage = ListSelectionPage(self)
        self.revisionPage = RevisionPage(self)
        self.addQuestionsPage = AddQuestionsPage(self)
        self.timeTravelPage = TimeTravelPage(self)
        self.deleteListsPage = DeleteListsPage(self)
        end = int(round(time.time() * 1000))
        #display loading time and memory usage
        print("Loading UI took " + str(end - start) + " milliseconds")
        print("Using:" + str(f"{process.memory_info().rss:,}") + " bytes of RAM")
        #add each page to the stacked widget in the main window
        self.stack.addWidget(self.homePage)
        self.stack.addWidget(self.listSelectionPage)
        self.stack.addWidget(self.revisionPage)
        self.stack.addWidget(self.addQuestionsPage)
        self.stack.addWidget(self.timeTravelPage)
        self.stack.addWidget(self.deleteListsPage)
        #fill the main window with the stached widget containing all of the pages and set the current page to the home page
        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.homePage)
        #these will be a connection and cursor that are common to all of the pages of this application
        self.connection = sqlite3.connect("Universal.db")
        self.cursor = self.connection.cursor()
        self.setUpDatabase()
    #create the database and it's tables if they are not already available
    def setUpDatabase(self):
        #check is foreign keys are supported
        self.cursor.execute("PRAGMA foreign_keys = ON")
        if (self.cursor.execute("PRAGMA foreign_keys").fetchall()[0][0] == 1):
            print("foreign keys are available")
        else:
            print("foreign keys are not available")
        #table containing questions
        self.cursor.execute("CREATE TABLE IF NOT EXISTS questions("
                   "questionID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                   "question VARCHAR NOT NULL,"
                   "streak INTEGER NOT NULL,"
                   "askDate VARCHAR NOT NULL,"
                   "listID INTEGER NOT NULL"
                   ")")
        #index to allow for quick selection of questions within a particular list
        self.cursor.execute("CREATE INDEX IF NOT EXISTS listIDIndex "
                   "ON questions(listID)")
        #table contaning the answers to the questions
        self.cursor.execute("CREATE TABLE IF NOT EXISTS answers("
                    "questionID INTEGER NOT NULL,"
                    "answer VARCHAR NOT NULL,"
                    "FOREIGN KEY (questionID) REFERENCES questions(questionID)"
                    ")")
        #idnex to allow for quick selection of answers to a particular question
        self.cursor.execute("CREATE INDEX IF NOT EXISTS "
                    "questionIndexA ON answers(questionID)")
        #table containing the human readable names of the question lists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS listNames("
                    "listID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                    "listName VARCHAR UNIQUE NOT NULL"
                    ")")
        #index to allow for quick selection of a list name given its ID
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS listIDIndexMain ON listNames(listID)")
        #add empty list that will be the root node of the system ... this list will encompas all others lists 
        self.cursor.execute("INSERT OR IGNORE INTO listNames (listName) "
                    "VALUES ('UniversalRoot')")
        self.connection.commit()
        #table containing parent and sublist relationships between lists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sublists("
                    "parentID INTEGER NOT NULL,"
                    "childID INTEGER NOT NULL,"
                    "FOREIGN KEY (parentID) REFERENCES listNames(listID)"
                    "FOREIGN KEY (childID) REFERENCES listNames(listID)"
                    ")")
        #index to allow for quick selection of sublists given a parent ID
        self.cursor.execute("CREATE INDEX IF NOT EXISTS "
                    "parentIndex ON sublists(parentID)")
        #index to allow for quick selection of superlists given a child ID
        self.cursor.execute("CREATE INDEX IF NOT EXISTS "
                    "childIndex ON sublists(childID)")
    #this will be run when the user closes the app
    def closeEvent(self, event):
        print("Goodbye")
        self.connection.close()

def main():
    #instansiate and display the application
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
    
if __name__ == '__main__':
   main()
