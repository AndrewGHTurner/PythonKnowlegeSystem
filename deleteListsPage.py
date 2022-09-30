from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3

class DeleteListsPage(QWidget):
	def __init__(self, mainWindow):
		QWidget.__init__(self)
		self.mainWindow = mainWindow

		mainLayout = QVBoxLayout()

		self.titleLabel = QLabel(self)
		self.titleLabel.setFont(QFont('Arial', 40))
		self.titleLabel.setText("DELETE")  
		self.titleLabel.setTextFormat(Qt.TextFormat.PlainText)
		self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
		mainLayout.addWidget(self.titleLabel)

		treatSublistsLabel = QLabel(self)
		treatSublistsLabel.setFont(QFont('Arial', 30))
		treatSublistsLabel.setText("Select how to treat sublists:")
		treatSublistsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
		mainLayout.addWidget(treatSublistsLabel)

		sublistLayout = QHBoxLayout()

		self.migrateSublistsRadioButton = QRadioButton("Migrate Local Sublists")
		self.migrateSublistsRadioButton.toggled.connect(self.migrateSublistsSelected)
		self.migrateSublistsRadioButton.setToolTip("Sublists will be moved to the deleted lists parent")
		self.migrateSublistsRadioButton.setFont(QFont('Arial', 20))
		sublistLayout.addWidget(self.migrateSublistsRadioButton)

		self.deleteSublistsRadioButton = QRadioButton("Delete Local Sublists")
		self.deleteSublistsRadioButton.toggled.connect(self.deleteSublistsSelected)
		self.deleteSublistsRadioButton.setToolTip("Sublists will be deleted from the current parent")
		self.deleteSublistsRadioButton.setFont(QFont('Arial', 20))
		sublistLayout.addWidget(self.deleteSublistsRadioButton)
		mainLayout.addLayout(sublistLayout)

		self.totalDeleteRadioButton = QRadioButton("Total Delete")
		self.totalDeleteRadioButton.toggled.connect(self.totalDeleteSelected)
		self.totalDeleteRadioButton.setToolTip("Sublists will be deleted from all parent lists")
		self.totalDeleteRadioButton.setFont(QFont('Arial', 20))
		sublistLayout.addWidget(self.totalDeleteRadioButton)
		mainLayout.addLayout(sublistLayout)

		deleteButton = QPushButton("DELETE!")
		deleteButton.setFont(QFont('Arial', 100))
		deleteButton.setStyleSheet("background-color:red;")
		deleteButton.clicked.connect(self.deleteButtonClick)
		mainLayout.addWidget(deleteButton)

		mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
		self.setLayout(mainLayout)

		self.treatSublists = ""
		self.listToDelete = ""
		self.parentOfListToDelete = ""
		self.listIDs = []
		self.parentsOfLists = []

	def deleteButtonClick(self):
		if self.treatSublists == "":
			print("Choose a treatment method you idiot!!")
		else: 	
			listName = self.listToDelete[0]
			listID = self.listToDelete[1] 	
			self.deletePopup = QMessageBox()
			self.deletePopup.setIcon(QMessageBox.Warning)
			self.deletePopup.setText("You are deleting: " + listName)
			self.deletePopup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			self.deletePopup.buttonClicked.connect(self.deleteButtonPopupClick)

			self.deletePopup.show()

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

	def deleteButtonPopupClick(self, button):

		self.parentsOfLists = []
		if button.text() == "OK":
			print("H")
			if self.treatSublists == "migrate":
				print ("The migrate feature is not available")
			elif self.treatSublists == "delete local":
				print("The delete local feature is not available")
				# self.getSubLists(self.listToDelete[1])#puts data into self.listIDs
				# self.parentsOfLists.append(self.parentOfListToDelete)
				# self.listIDs.append(self.listToDelete[1])

				# C = 0
				# while C < len(self.listIDs):
				# 	childID = str(self.listIDs[c])#this is the one to delete
				# 	parentID = str(self.parentsOfLists[c])
				# 	#check if this child has other parent lists
				# 	self.mainWindow.cursor.execute("SELECT parentID FROM sublists WHERE childID =" + str(childID))
				# 	parents = self.mainWindow.cursor.fetchall()
				# 	if(len(parents) > 1):
				# 		#only delete the entry's for the correct parent of this list in sublists
				# 		print("list " + str(childID) + " has multiple parents so only the refrence can be deleted")
				# 		print("DELETE FROM sublists WHERE parentID = " + childID)
				# 		self.mainWindow.cursor.execute("DELETE FROM sublists WHERE parentID = " + childID)
				# 		self.mainWindow.connection.commit()
				# 		print("DELETE FROM sublists WHERE parentID = " + parentID)
				# 		self.mainWindow.cursor.execute("DELETE FROM sublists WHERE parentID = " + parentID)
				# 		self.mainWindow.connection.commit()						
				# 	else:
				# 		totalDelete(childID)
					#C = C + 1
				#the above needs redoing ... if andrew had a nutrition sublist it would be wrongly deleted ... probs needs totally redoing and making into a recursive function
			else:#TOTAL DELETE
				self.getSubLists(str(self.listToDelete[1]))
				self.parentsOfLists.append(self.parentOfListToDelete)
				self.listIDs.append(self.listToDelete[1])
				print(str(self.listIDs))
				print("Deleting " + str(self.listToDelete[1]))
				print("THIS function DOES NOT WORL")
				for listID in self.listIDs:
					#delete the answers
					self.mainWindow.cursor.execute("SELECT questionID FROM questions WHERE listID = " + str(listID))
					questionIDs = self.mainWindow.cursor.fetchall()
					for questionID in questionIDs:
						print("DELETE FROM answers WHERE questionID = " + str(questionID[0]))
						self.mainWindow.cursor.execute("DELETE FROM answers WHERE questionID = " + str(questionID[0]))
						self.mainWindow.connection.commit()
				for listID in self.listIDs:
					self.mainWindow.cursor.execute("DELETE FROM questions WHERE listID = " + str(listID))
					self.mainWindow.connection.commit()
					#delete all sublist entrys
					self.mainWindow.cursor.execute("DELETE FROM sublists WHERE childID = " + str(listID)) #rows where listID is the parent will be deleted when child lists are deleted
					self.mainWindow.connection.commit()

					self.mainWindow.cursor.execute("DELETE FROM sublists WHERE parentID = " + str(listID)) #rows where listID is the parent will be deleted when child lists are deleted
					self.mainWindow.connection.commit()
				for listID in self.listIDs:	
					self.mainWindow.cursor.execute("DELETE FROM listNames WHERE listID = " + str(listID))	
					self.mainWindow.connection.commit()				

					

	def totalDeleteSelected(self, selected):
		if selected:
			self.treatSublists = "total delete"				
 
	def deleteSublistsSelected(self, selected):
		if selected:
			self.treatSublists = "delete local"

	def migrateSublistsSelected(self, selected):
		if selected:
			self.treatSublists = "migrate"

	def setUp(self, listsToDelete, parentList):#parentList is needed in case a list to delete has multiple parents
		self.listToDelete = listsToDelete
		self.parentOfListToDelete = parentList
		self.treatSublists = ""
		listName = listsToDelete[0]
		listID = listsToDelete[1]
		self.titleLabel.setText("You are deleting: " + listName)
		self.listIDs = []
		self.parentsOfLists = []
