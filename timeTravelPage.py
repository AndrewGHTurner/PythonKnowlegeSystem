from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sqlite3

class TimeTravelPage(QWidget):
	def __init__(self, mainWindow):
		QWidget.__init__(self)
		self.mainWindow = mainWindow

		mainLayout = QVBoxLayout()

		self.title = QLabel(self)
		self.title.setFont(QFont('Arial', 30))
		self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.title.setTextFormat(Qt.TextFormat.PlainText)
		mainLayout.addWidget(self.title)

		self.sublistCheckBox = QCheckBox("Also time travel with sublists", self)
		self.sublistCheckBox.setFont(QFont('Arial', 20))
		mainLayout.addWidget(self.sublistCheckBox)

		self.dayTimeTravelButton = QPushButton("Time travel One Day!")
		self.dayTimeTravelButton.setFont(QFont('Arial', 50)) 
		self.dayTimeTravelButton.setStyleSheet("background-color:LightCoral;")
		self.dayTimeTravelButton.objectName = "day"
		self.dayTimeTravelButton.clicked.connect(lambda: self.timeTravelClick(self.sender()))
		mainLayout.addWidget(self.dayTimeTravelButton)

		self.universeTimeTravelButton = QPushButton("Time travel\n the age\n of the universe!")
		self.universeTimeTravelButton.setFont(QFont('Arial', 100)) 
		self.universeTimeTravelButton.setStyleSheet("background-color:Red;")
		self.universeTimeTravelButton.objectName = "universe"
		self.universeTimeTravelButton.clicked.connect(lambda: self.timeTravelClick(self.sender()))
		mainLayout.addWidget(self.universeTimeTravelButton)

		self.homeButton = QPushButton("Home")
		self.homeButton.setFont(QFont('Arial', 30))
		self.homeButton.clicked.connect(self.homeButtonClick)
		mainLayout.addWidget(self.homeButton)

		mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.setLayout(mainLayout)

		self.listName = ""
		self.listID = ""
		self.listIDs = []#holds the IDs for time travel with sublists

   
	def getSubLists(self, listID):
		if listID in self.listIDs:#prevents duplicates and issues with loops in the list tree
			print("Loop encountered!")
		else:
			self.listIDs.append(listID)
			self.mainWindow.cursor.execute("SELECT childID FROM sublists WHERE parentID = " + str(listID))
			results = self.mainWindow.cursor.fetchall()
			if len(results) != 0:
				for result in results:
					newParentListID = result[0]
					self.getSubLists(newParentListID)#returns a list!

	def timeTravelClick(self, button):
		if self.sublistCheckBox.isChecked():#bring every date to today's date
			self.getSubLists(self.listID)#returns the sublistIDs and the listID as a python list to self.listIDs
		elif self.listID not in self.listIDs:
			self.listIDs.append(self.listID)
		for listID in self.listIDs:
			print("I")
			if button.objectName == "day":
				self.mainWindow.cursor.execute("UPDATE questions SET askDate = DATE(askDate, '-1 day') WHERE listID = " + str(listID))
					
			else:#time travel for the age of the universe
				self.mainWindow.cursor.execute("UPDATE questions SET askDate = DATE('now') WHERE listID = " + str(listID))
			self.mainWindow.connection.commit()    			
   

	def homeButtonClick(self):
		self.mainWindow.stack.setCurrentWidget(self.mainWindow.homePage)    

	def setListToTimeTravelWith(self, listName, listID):
		self.listIDs = []#reset to empty list if this is the second usage
		self.listName = listName
		self.listID = listID
		self.title.setText("You are time travelling with: " + listName)
