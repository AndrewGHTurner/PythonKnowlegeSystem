from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3
import random

import winsound

class RevisionPage(QWidget):
	def __init__(self, mainWindow):
		QWidget.__init__(self)
		self.mainWindow = mainWindow
		mainLayout = QVBoxLayout()

		self.answersGivenLabel = QLabel("Answers given: ")
		self.questionsCorrectLabel = QLabel("Correct answers: ")
		self.questionsLeftLabel = QLabel("Questions left: ")
		self.progressBar = QProgressBar(self)
		self.progressBar.setValue(25)
		mainLayout.addWidget(self.answersGivenLabel)
		mainLayout.addWidget(self.questionsCorrectLabel)
		mainLayout.addWidget(self.questionsLeftLabel)
		mainLayout.addWidget(self.progressBar)

		self.questionDisplay = QTextEdit(self)
		self.questionDisplay.setReadOnly(True)
		self.questionDisplay.setText("HELLO")
		self.questionDisplay.setFont(QFont('Arial', 40))
		mainLayout.addWidget(self.questionDisplay)

		self.answerBox = QLineEdit(self)
		self.answerBox.setText("answer")
		self.answerBox.setFont(QFont('Arial', 20))
		mainLayout.addWidget(self.answerBox)

		self.correctnessDisplay = QLabel(self)        
		self.correctnessDisplay.setFont(QFont('Arial', 40))
		self.correctnessDisplay.setText("HELLO")
		self.correctnessDisplay.setTextFormat(Qt.TextFormat.PlainText)
		self.correctnessDisplay.setAlignment(Qt.AlignmentFlag.AlignCenter)
		mainLayout.addWidget(self.correctnessDisplay)

		buttonLayout = QHBoxLayout()
		self.homeButton = QPushButton("Home")
		self.homeButton.setFont(QFont('Arial', 20))
		self.homeButton.clicked.connect(self.homeButtonClick)

		self.endterButton = QPushButton("Enter")
		self.endterButton.setFont(QFont('Arial', 20))
		self.endterButton.clicked.connect(self.enterButtonClick)

		buttonLayout.addWidget(self.homeButton)
		buttonLayout.addWidget(self.endterButton)
		buttonRow = QWidget()
		buttonRow.setLayout(buttonLayout)
		mainLayout.addWidget(buttonRow)

		self.setLayout(mainLayout)

		self.selectedLists = []
		self.selectedQuestionIDs = []
		self.currentQuestionID = ""



		self.connection = sqlite3.connect("Universal.db")
		self.cursor = self.connection.cursor()

	def setUp(self, selectedLists):
		print("HERE")
		self.selectedLists = selectedLists;#listIDs
		self.getUniqueQuestionIDs()
		self.progressBar.setValue(0)
		if len(self.selectedQuestionIDs) != 0:
			self.askQuestion(self.selectedQuestionIDs[0])
		else:
			print("You're up to date")
			self.homeButtonClick()

	def askQuestion(self, questionID):
		self.currentQuestionID = questionID
		self.cursor.execute("SELECT question FROM questions WHERE questionID = " + str(questionID))
		question = self.cursor.fetchall()[0][0]
		self.questionDisplay.setText(question)

	def processCorrectAnswer(self):
		frequency = 1500  # Set Frequency To 2500 Hertz
		duration = 500  # Set Duration To 1000 ms == 1 second
		winsound.Beep(frequency, duration)
		#update streak
		self.cursor.execute("UPDATE questions SET streak = streak + 1 WHERE questionID = " + str(self.currentQuestionID))
		self.connection.commit()
		#select new streak
		self.cursor.execute("SELECT streak FROM questions WHERE questionID = " + str(self.currentQuestionID))
		newStreak = self.cursor.fetchall()[0][0]
		#update the ask date
		self.cursor.execute("UPDATE questions SET askDate = DATE(DATE('now'), '+" + str(newStreak) + " day') WHERE questionID = " + str(self.currentQuestionID))
		self.connection.commit()
		self.correctnessDisplay.setText("Correct!")
		#remove ID of the question answered correctly
		self.selectedQuestionIDs.remove(self.currentQuestionID)

	def processWrongAnswer(self, correctAnswers):
		frequency = 500  # Set Frequency To 2500 Hertz
		duration = 500  # Set Duration To 1000 ms == 1 second
		winsound.Beep(frequency, duration)
		#set streak to zero
		self.cursor.execute("UPDATE questions SET streak = 0 WHERE questionID = " + str(self.currentQuestionID))
		self.connection.commit()

		correctAnswers = correctAnswers[:-2]
		self.correctnessDisplay.setText( "Wrong! The answer could be: " + correctAnswers)

	def enterButtonClick(self):

		print("Enter")
		userAnswer = self.answerBox.text()
		userAnswer = userAnswer.replace(" ", "")
		userAnswer = userAnswer.lower()
		self.cursor.execute("SELECT answer FROM answers WHERE questionID = " + str(self.currentQuestionID))
		answers = self.cursor.fetchall()
		correct = False
		correctAnswers = ""
		for answer in answers:
			answer = answer[0]
			print(answer)
			print(userAnswer)
			correctAnswers = correctAnswers + answer + ", "
			if answer == userAnswer:
				correct = True
				break
		if correct == True:
			self.processCorrectAnswer()
		else:
			self.processWrongAnswer(correctAnswers)
		self.answerBox.clear()
		#select an ID of a new question to ask
		if len(self.selectedQuestionIDs) > 0:
			self.currentQuestionID = self.selectedQuestionIDs[random.randint(0, len(self.selectedQuestionIDs) - 1)]
			self.askQuestion(self.currentQuestionID)
		else:
			#put an analysis page in here later
			self.homeButtonClick()

	def getUniqueQuestionIDs(self):
		conditions = "";
		for listID in self.selectedLists:
			conditions = conditions + "listID = " + str(listID) + " OR "
		conditions = conditions[:-3]
		print("SELECT questionID FROM questions WHERE (" + conditions + ") AND askDate <= DATE('now')")
		self.cursor.execute("SELECT questionID FROM questions WHERE (" + conditions + ") AND askDate <= DATE('now')")
		questionIDs = self.cursor.fetchall()
		print(questionIDs)
		for tup in questionIDs:
			self.selectedQuestionIDs.append(tup[0])
		random.shuffle(self.selectedQuestionIDs)

	def keyPressEvent(self, e):#this connects the enter key on the keyboard with the enter button 
		if e.key() == 16777220:
			self.enterButtonClick()


		


	def homeButtonClick(self):
		self.mainWindow.stack.setCurrentWidget(self.mainWindow.homePage)
