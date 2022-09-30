from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
class HomePage(QWidget):
    def __init__(self, mainWindow):


        QWidget.__init__(self)
        self.mainWindow = mainWindow
        mainLayout = QVBoxLayout()

        welcomeLabel = QLabel(self)
        welcomeLabel.setFont(QFont('Arial', 40))
        welcomeLabel.setText("WELCOME")  
        welcomeLabel.setTextFormat(Qt.TextFormat.PlainText)
        welcomeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(welcomeLabel)

        reviseButton = QPushButton("Revise", self)
        reviseButton.setFont(QFont('Arial', 20))
        reviseButton.clicked.connect(self.reviseButtonClick)
        mainLayout.addWidget(reviseButton)

        addQuestionsButton = QPushButton("Add Questions", self)
        addQuestionsButton.clicked.connect(self.addQuestionsButtonClick)
        addQuestionsButton.setFont(QFont('Arial', 20))
        mainLayout.addWidget(addQuestionsButton)

        timeTravelButton = QPushButton("Time Travel", self)
        timeTravelButton.clicked.connect(self.timeTravelButtonClick)
        timeTravelButton.setFont(QFont('Arial', 20))
        mainLayout.addWidget(timeTravelButton)

        deleteListsButton = QPushButton("Delete Lists", self)
        deleteListsButton.clicked.connect(self.deleteListsButtonClick)
        deleteListsButton.setFont(QFont('Arial', 20))
        mainLayout.addWidget(deleteListsButton)

        mainLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(mainLayout)

    def deleteListsButtonClick(self):
        self.mainWindow.listSelectionPage.configForDeleteLists()
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.listSelectionPage)

    def timeTravelButtonClick(self):
        self.mainWindow.listSelectionPage.configForTimeTravel()
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.listSelectionPage)

    def reviseButtonClick(self):
        self.mainWindow.listSelectionPage.configForRevision()
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.listSelectionPage)

    def addQuestionsButtonClick(self):
        self.mainWindow.listSelectionPage.configForAddingQuestions()
        self.mainWindow.stack.setCurrentWidget(self.mainWindow.listSelectionPage)
        
