from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sqlite3
#buttons will hold numeric IDs of lists as their object names
#layouts will hold list names as their object names
class ListSelectionPage(QWidget):
	def __init__(self, mainWindow):
		QWidget.__init__(self)
		self.mainWindow = mainWindow
		mainLayout = QVBoxLayout()
		#makes the "Select Your Lists" label
		self.selectLabel = QLabel(self)
		self.selectLabel.setFont(QFont('Arial', 40))
		self.selectLabel.setText("Select your lists to revise")
		self.selectLabel.setTextFormat(Qt.TextFormat.PlainText)
		self.selectLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
		mainLayout.addWidget(self.selectLabel)

		#makes the scroll area widget to show the lists in
		self.listWidget = QWidget()                                          
		self.listView = QScrollArea()                                      
		self.listViewLayout = QVBoxLayout()                             
		self.listViewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)                           
		self.listWidget.setLayout(self.listViewLayout)                     
		self.listView.setWidget(self.listWidget)                           
		self.listView.setWidgetResizable(True)
		mainLayout.addWidget(self.listView)

		addListLayout = QHBoxLayout()
		self.listNameInput = QLineEdit(self)
		self.listNameInput.setFont(QFont('Arial', 20))
		addListButton = QPushButton("Add List", self)
		addListButton.setFont(QFont('Arial', 20))
		addListButton.clicked.connect(self.addListButtonClicked)
		addListLayout.addWidget(self.listNameInput)
		addListLayout.addWidget(addListButton)
		#needs to be in a widget to me made invisible
		self.addListWidget = QWidget()
		self.addListWidget.setLayout(addListLayout)
		mainLayout.addWidget(self.addListWidget)
		self.addListWidget.setVisible(False)

		youSelectedLable = QLabel("You have selected:")
		youSelectedLable.setFont(QFont('Arial', 20))
		youSelectedLable.setAlignment(Qt.AlignmentFlag.AlignCenter)
		mainLayout.addWidget(youSelectedLable)

		selectedListWidget = QWidget()                                          
		selectedListView = QScrollArea()                                      
		self.selectedListViewLayout = QVBoxLayout()                             
		self.selectedListViewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)                           
		selectedListWidget.setLayout(self.selectedListViewLayout)                     
		selectedListView.setWidget(selectedListWidget)                           
		selectedListView.setWidgetResizable(True)
		mainLayout.addWidget(selectedListView)

		goButton = QPushButton("GO!")
		goButton.clicked.connect(self.goButtonClick)
		goButton.setFont(QFont('Arial', 20))
		goButton.setStyleSheet("background-color : LimeGreen")

		homeButton = QPushButton("Home")
		homeButton.setFont(QFont('Arial', 20))
		homeButton.clicked.connect(self.homeButtonClick)

		buttonLayout = QHBoxLayout()
		buttonLayout.addWidget(homeButton)
		buttonLayout.addWidget(goButton)

		mainLayout.addLayout(buttonLayout)

		self.listIDs = []
		self.selectedLists = []
		self.parentsOfLists = []

		self.setLayout(mainLayout)

				#home button in the couner not in the layout
		self.sublistRoute = []

		self.config = ""

	def configForDeleteLists(self):
		self.reset()
		self.config = "delete lists"
		self.mainWindow.listSelectionPage.selectLabel.setText("Select any lists to delete")

	def configForRevision(self):
		self.reset()
		self.config = "revision"
		self.mainWindow.listSelectionPage.selectLabel.setText("Select your lists to revise")

	def configForTimeTravel(self):
		self.reset()
		self.config = "time travel"
		self.mainWindow.listSelectionPage.selectLabel.setText("Select a list to time travel with")

	def configForAddingQuestions(self):
		self.reset()
		self.config = "adding questions"
		self.mainWindow.listSelectionPage.selectLabel.setText("Select a list to add to")

	def clearSelectedListView(self):
		while self.selectedListViewLayout.count():
			self.selectedListViewLayout.takeAt(0).widget().deleteLater()

	def clearListView(self):
		while self.listViewLayout.count():
			self.listViewLayout.takeAt(0).widget().deleteLater()

	def getSubLists(self, parentID):
		print("PARENT ID = " + str(parentID))

		print(str(parentID))
		self.mainWindow.cursor.execute("SELECT childID FROM sublists WHERE parentID = " + str(parentID))
		children = self.mainWindow.cursor.fetchall()
		if len(children) != 0:
			for child in children:
				childID = child[0]
				if childID in self.listIDs:#prevents duplicates and issues with loops in the list tree
					print("Loop encountered!")
				else:
					self.parentsOfLists.append(parentID)
					self.listIDs.append(childID)
					self.getSubLists(childID)#returns a list!

	def backButtonClick(self, button):
		print(self.sublistRoute)
		self.sublistRoute.pop()
		print(self.sublistRoute)
		if len(self.sublistRoute) > 0:
			button.parent().objectName = self.sublistRoute[-1][0]
			button.objectName = self.sublistRoute[-1][1]
			self.sublistRoute.pop()#the entry removed here will immediatly be re-added by the search button click
			self.searchButtonClick(button)
		else:
			self.mainWindow.listSelectionPage.addListWidget.setVisible(False)
			self.clearListView()
			self.makeListViewRow("Universal", 1, False)#ID of "Universal" will always be 1
			self.currentListID = 0            


	def makeListViewRow(self, name, listID, back):
		name = str(name)
		listRowLayout = QHBoxLayout()
		listRow = QWidget()
		listName = QLabel(name)
		listName.setFont(QFont('Arial', 33))
		listRowLayout.addWidget(listName)



		if back == True:
			listRow.setStyleSheet("background-color:DeepSkyBlue;")
			backButton = QPushButton("Back")
			backButton.objectName = listID
			backButton.clicked.connect(lambda: self.backButtonClick(self.sender()))
			listRowLayout.addWidget(backButton)
		else:
			selectButton = QPushButton("Select")
			selectButton.objectName = listID
			selectButton.setStyleSheet("background-color : PaleGreen;")
			selectButton.clicked.connect(lambda: self.selectButtonClick(self.sender()))

			searchButton = QPushButton("Search")
			searchButton.objectName = listID
			searchButton.setStyleSheet("background-color : #FFAE42;")#colour is yellow orange
			searchButton.clicked.connect(lambda: self.searchButtonClick(self.sender()))

			listRowLayout.addWidget(searchButton)
			listRowLayout.addWidget(selectButton)
		

		listRow.objectName = name
		listRow.setLayout(listRowLayout)

		self.listViewLayout.addWidget(listRow)

	def makeSelectedListViewRow(self, name, listID):
		self.selectedListID = listID
		selectedListRowLayout = QHBoxLayout()
		removeButton = QPushButton("Remove")
		removeButton.objectName = listID
		removeButton.clicked.connect(lambda: self.removeButtonClick(self.sender()))
		removeButton.setStyleSheet("background-color : red;")
		ListNameLable = QLabel(name)
		ListNameLable.setFont(QFont('Arial', 33))
		selectedListRowLayout.addWidget(ListNameLable)
		selectedListRowLayout.addWidget(removeButton)
		selectedListRow = QWidget()
		selectedListRow.objectName = name
		selectedListRow.setLayout(selectedListRowLayout)
		self.selectedListViewLayout.addWidget(selectedListRow)

	def removeButtonClick(self, button):
		listName = button.parent().objectName
		listID = button.objectName
		self.selectedLists.remove((listName, listID))

		self.makeListViewRow(listName, listID, False)
		button.parent().deleteLater()

	def selectButtonClick(self, button):
		listName = button.parent().objectName
		listID = button.objectName
		self.selectedLists.append((listName, listID))
		self.makeSelectedListViewRow(listName, listID)
		button.parent().deleteLater()

	def searchButtonClick(self, button):
		oldListName = button.parent().objectName
		oldListID = button.objectName
		self.sublistRoute.append((oldListName, oldListID))
		self.currentListID = oldListID
		if self.config == "adding questions" and self.currentListID != 0:
			self.mainWindow.listSelectionPage.addListWidget.setVisible(True)
		#select names and IDs of sublists
		connection = sqlite3.connect("Universal.db")
		cursor = connection.cursor()
		cursor.execute("SELECT listName, listID FROM listNames INNER JOIN sublists ON listNames.listID = sublists.childID WHERE sublists.parentID = " + str(self.currentListID))
		#add new lists to listView
		self.clearListView()
		self.makeListViewRow(oldListName, oldListID, True)
		for result in cursor.fetchall():
			print(result)
			self.makeListViewRow(result[0], result[1], False)
		#UNFINISHED


	def addListButtonClicked(self):
		if self.currentListID != 0:#0 is not a listID. all lists must be sublists of it
			#add new list name
			connection = sqlite3.connect("Universal.db")
			cursor = connection.cursor()
			newListName = self.listNameInput.text()
			newListName = newListName.replace("'","''")
			print("INSERT INTO listNames VALUES " + newListName)
			cursor.execute("INSERT INTO listNames (listName) VALUES ('" + newListName + "')")
			connection.commit()
			#get new list's ID
			cursor.execute("SELECT last_insert_rowid()")
			newListID = cursor.fetchall()[0][0]
			#add to scroll
			self.makeListViewRow(newListName, newListID, False)
			#insert new list as child of its parent in sublists table
			print("INSERT INTO sublists (parentID, childID) VALUES (" + str(self.currentListID) + ", " + str(newListID) + ")")
			cursor.execute("INSERT INTO sublists (parentID, childID) VALUES (" + str(self.currentListID) + ", " + str(newListID) + ")")
			connection.commit()

 
		else:
			print("EVERY NEW LIST HAS TO BE A SUBLIST OF universalRoot!!!")
	def reset(self):
		self.clearListView()
		self.clearSelectedListView()
		self.makeListViewRow("Universal", 1, False)#ID of "Universal" will always be 1
		self.selectedLists = []
		self.sublistRoute = []#the route down the list tree
		self.parentsOfLists = []
		self.currentListID = 0


	def goButtonClick(self):
		if (len(self.selectedLists) == 0):
			print("CHOOSE A LIST!!!!!")
		elif self.config == "revision":
			self.listIDs = []
			for llist in self.selectedLists:
				self.getSubLists(llist[1])
				if llist[1] in self.listIDs:
					print("Repete")
				else:
					self.listIDs.append(llist[1])
			print("SELECTED:")
			print(self.listIDs)
			self.mainWindow.stack.setCurrentWidget(self.mainWindow.revisionPage)
			self.mainWindow.revisionPage.setUp(self.listIDs)

		elif self.config == "adding questions":
			if(len(self.selectedLists) > 1):
				print("You have selected too many lists you idiot!")
			self.mainWindow.addQuestionsPage.setListToAddTo(self.selectedLists[0][0], self.selectedLists[0][1])
			self.mainWindow.stack.setCurrentWidget(self.mainWindow.addQuestionsPage)

		elif self.config == "time travel":
			if(len(self.selectedLists) > 1):
				print("You have selected too many lists you idiot!")
			self.mainWindow.timeTravelPage.setListToTimeTravelWith(self.selectedLists[0][0], self.selectedLists[0][1])
			self.mainWindow.stack.setCurrentWidget(self.mainWindow.timeTravelPage)

		elif self.config == "delete lists":
			if(len(self.selectedLists) > 1):
				print("You have selected too many lists you idiot!")
			else:			
				if len(self.sublistRoute) < 1:
					print("YOU CANNOT DELETE THE ROOT LIST YOU IDIOT")
				else:
					self.mainWindow.deleteListsPage.setUp(self.selectedLists[0], self.sublistRoute[-1])
					self.mainWindow.stack.setCurrentWidget(self.mainWindow.deleteListsPage)
			
		else:
			print("ERROR")

	def homeButtonClick(self):
		self.mainWindow.stack.setCurrentWidget(self.mainWindow.homePage)


