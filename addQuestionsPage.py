from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3

class AddQuestionsPage(QWidget):
	def __init__(self, mainWindow):
		QWidget.__init__(self)
		self.mainWindow = mainWindow
		mainLayout = QVBoxLayout()

		self.addQuestionsLabel = QLabel("Add questions")
		self.addQuestionsLabel.setFont(QFont('Arial', 33))
		self.addQuestionsLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
		mainLayout.addWidget(self.addQuestionsLabel)

		self.questionInput = QTextEdit(self)
		self.questionInput.setText("Type your question")
		self.questionInput.setFont(QFont('Arial', 40))
		mainLayout.addWidget(self.questionInput)

		self.answerInput = QLineEdit(self)
		self.answerInput.setText("answer")
		self.answerInput.setFont(QFont('Arial', 20))
		mainLayout.addWidget(self.answerInput)

		bottomLayout = QHBoxLayout()

		self.homeButton = QPushButton("Home")
		self.homeButton.setFont(QFont('Arial', 20))
		self.homeButton.clicked.connect(lambda: self.homeButtonClick(self.sender()))
		bottomLayout.addWidget(self.homeButton)

		self.addQuestionButton = QPushButton("Add!")
		self.addQuestionButton.setFont(QFont('Arial', 20))
		self.addQuestionButton.clicked.connect(self.addQuestionButtonClicked)
		bottomLayout.addWidget(self.addQuestionButton)

		mainLayout.addLayout(bottomLayout)
	   
		self.setLayout(mainLayout)

	def addQuestionButtonClicked(self, button):
		newQuestion = self.questionInput.toPlainText()
		newQuestion = newQuestion.replace("'","''")
		newAnswers = self.answerInput.text()
		print(newQuestion)
		print(newAnswers)
		self.questionInput.clear()
		self.answerInput.clear()

		connection = sqlite3.connect("Universal.db")
		cursor = connection.cursor()
		#insert new question into questions table
		print("INSERT INTO questions (question, streak, askDate, listID) VALUES ('" + newQuestion + "', 0, DATE('now'), " + str(self.listID) + ")")
		cursor.execute("INSERT INTO questions (question, streak, askDate, listID) VALUES ('" + newQuestion + "', 0, DATE('now'), " + str(self.listID) + ")")
		connection.commit()
		#get new question's ID
		cursor.execute("SELECT last_insert_rowid()")
		newQuestionID = cursor.fetchall()[0][0]
		#insert new answers into answers table
		answers = newAnswers.lower()
		answers = answers.replace(" ", "")
		answers = answers.split(",")
		for answer in answers:
			answer = answer.replace("'","''")
			print("INSERT INTO answers (questionID, answer) VALUES (" + str(newQuestionID) + ", '" + answer + "')")
			cursor.execute("INSERT INTO answers (questionID, answer) VALUES (" + str(newQuestionID) + ", '" + answer + "')")
			connection.commit()
		connection.close()

	def homeButtonClick(self, button):
		self.mainWindow.stack.setCurrentWidget(self.mainWindow.homePage)

	def setListToAddTo(self, listName, listID):
		self.listName = listName
		self.listID = listID
		self.addQuestionsLabel.setText("You are adding questions to: " + listName)