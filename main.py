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
####from psutil 
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(400, 40, 1000, 1000)
        self.stack = QStackedWidget(self)

        start = int(round(time.time() * 1000))
       #### process = psutil.Process(os.getpid())
    #    print("Using:" + str(process.memory_info().rss))
        self.homePage = HomePage(self)
     #   print("Using:" + str(process.memory_info().rss))
        self.listSelectionPage = ListSelectionPage(self)
      #  print("Using:" + str(process.memory_info().rss))
        self.revisionPage = RevisionPage(self)
    #    print("Using:" + str(process.memory_info().rss))
        self.addQuestionsPage = AddQuestionsPage(self)
     #   print("Using:" + str(process.memory_info().rss))
        self.timeTravelPage = TimeTravelPage(self)
     #   print("Using:" + str(process.memory_info().rss))
        self.deleteListsPage = DeleteListsPage(self)
        end = int(round(time.time() * 1000))

        print("Loading UI took " + str(end - start) + " milliseconds")
      ####  print("Using:" + str(process.memory_info().rss))

        self.stack.addWidget(self.homePage)
        self.stack.addWidget(self.listSelectionPage)
        self.stack.addWidget(self.revisionPage)
        self.stack.addWidget(self.addQuestionsPage)
        self.stack.addWidget(self.timeTravelPage)
        self.stack.addWidget(self.deleteListsPage)

        self.setCentralWidget(self.stack)
        self.stack.setCurrentWidget(self.homePage)

        #these will be a connection and cursor that are common to all of the pages of this application
        self.connection = sqlite3.connect("Universal.db")
        self.cursor = self.connection.cursor()
        self.setUpDatabase()
          # in bytes 

    def setUpDatabase(self):#this will create the database and it's tables if they are not already available
        self.cursor.execute("PRAGMA foreign_keys = ON")
        if (self.cursor.execute("PRAGMA foreign_keys").fetchall()[0][0] == 1):
            print("foreign keys are available")
        else:
            print("foreign keys are not available")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS questions("
                   "questionID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                   "question VARCHAR NOT NULL,"
                   "streak INTEGER NOT NULL,"
                   "askDate VARCHAR NOT NULL,"
                   "listID INTEGER NOT NULL"
                   ")")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS listIDIndex "
                   "ON questions(listID)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS answers("
                    "questionID INTEGER NOT NULL,"
                    "answer VARCHAR NOT NULL,"
                    "FOREIGN KEY (questionID) REFERENCES questions(questionID)"
                    ")")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS "
                    "questionIndexA ON answers(questionID)")


        self.cursor.execute("CREATE TABLE IF NOT EXISTS listNames("
                    "listID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                    "listName VARCHAR UNIQUE NOT NULL"
                    ")")
        self.cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS listIDIndexMain ON listNames(listID)")
        #add empty list that will be the root node of the system
        self.cursor.execute("INSERT OR IGNORE INTO listNames (listName) "
                    "VALUES ('UniversalRoot')")
        self.connection.commit()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sublists("
                    "parentID INTEGER NOT NULL,"
                    "childID INTEGER NOT NULL,"
                    "FOREIGN KEY (parentID) REFERENCES listNames(listID)"
                    "FOREIGN KEY (childID) REFERENCES listNames(listID)"
                    ")")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS "
                    "parentIndex ON sublists(parentID)")
        self.cursor.execute("CREATE INDEX IF NOT EXISTS "
                    "childIndex ON sublists(childID)")

    def closeEvent(self, event):#this will be run when the user closes the app
        print("Goodbye")
        self.connection.close()

def main():
    #set up the database if it isn't already

    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
    
	
if __name__ == '__main__':
   main()
