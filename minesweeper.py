import sys
from random import shuffle
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

difficulty = {
    "easy": {"row": 9, "column": 9, "mines": 10},
    "medium": {"row": 16, "column": 16, "mines": 40},
    "hard": {"row": 16, "column": 30, "mines": 90},
}


class Button(QPushButton):
    def __init__(self, x, y, number=0, *args, **kwargs):
        super(Button, self).__init__(*args, **kwargs)
        self.opened = 0
        self.id = number
        self.x = x
        self.y = y
        self.is_mine = False
        self.bomb_counter = 0
        self.is_open = False
        self.label = ''
        self.flag = False


class Ui_difficulty(QMainWindow):
    def __init__(self):
        super().__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.setup_ui(self.MainWindow)
        self.MainWindow.show()

    def setup_ui(self, difficulty):
        difficulty.setObjectName("difficulty")
        difficulty.setFixedSize(330, 130)
        centralwidget = QtWidgets.QWidget(difficulty)
        centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 330, 55))
        font = QtGui.QFont()
        font.setFamily("Fixedsys")
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        self.label.setFont(QtGui.QFont("Fixedsys", 30, weight=QtGui.QFont.Bold))
        self.label.setObjectName("label")
        self.button_easy = QtWidgets.QPushButton(centralwidget)
        self.button_easy.setGeometry(QtCore.QRect(50, 60, 75, 24))
        self.button_easy.setObjectName("pushButton")
        self.button_easy.setFont(font)
        self.button_medium = QtWidgets.QPushButton(centralwidget)
        self.button_medium.setGeometry(QtCore.QRect(130, 60, 75, 24))
        self.button_medium.setObjectName("button_medium")
        self.button_medium.setFont(font)
        self.button_hard = QtWidgets.QPushButton(centralwidget)
        self.button_hard.setGeometry(QtCore.QRect(210, 60, 75, 24))
        self.button_hard.setObjectName("button_hard")
        self.button_hard.setFont(font)
        difficulty.setCentralWidget(centralwidget)
        statusbar = QtWidgets.QStatusBar(difficulty)
        statusbar.setObjectName("statusbar")
        difficulty.setStatusBar(statusbar)
        self.button_easy.clicked.connect(lambda: self.exit("easy"))
        self.button_medium.clicked.connect(lambda: self.exit("medium"))
        self.button_hard.clicked.connect(lambda: self.exit("hard"))
        self.retranslate_ui(difficulty)
        QtCore.QMetaObject.connectSlotsByName(difficulty)

    def exit(self, diff):
        Ui_difficulty.user_choise = diff
        Ui_MainWindow(Ui_difficulty.user_choise)
        self.MainWindow.close()

    def retranslate_ui(self, difficulty):
        _translate = QtCore.QCoreApplication.translate
        difficulty.setWindowTitle(_translate("difficulty", "Difficulty"))
        self.label.setText(_translate("difficulty", "Select difficulty"))
        self.button_easy.setText(_translate("difficulty", "Easy"))
        self.button_medium.setText(_translate("difficulty", "Medium"))
        self.button_hard.setText(_translate("difficulty", "Hard"))


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, diff, parent=None):
        super().__init__(parent)
        self.diff = diff
        self.points = 0
        self.buttons = []
        for i in range(difficulty[self.diff]["row"] + 2):
            temp = []
            for j in range(difficulty[self.diff]["column"] + 2):
                self.btn = Button(x=i, y=j)
                self.btn.installEventFilter(self)
                self.btn.setFont(QtGui.QFont("Fixedsys"))
                self.btn.clicked.connect(lambda checked=False, elem=self.btn: self.indexes(elem))
                self.btn.setFixedSize(QSize(30, 30))
                temp.append(self.btn)
            self.buttons.append(temp)
        self.MainWindow = QtWidgets.QMainWindow()
        self.setup_ui(self.MainWindow)
        self.MainWindow.show()

    Game_over = False
    First_click = True

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        if self.diff == 'easy':
            MainWindow.setFixedSize(300, 340)
        elif self.diff == 'medium':
            MainWindow.setFixedSize(500, 550)
        elif self.diff == 'hard':
            MainWindow.setFixedSize(950, 570)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(size_policy)
        centralwidget = QtWidgets.QWidget(MainWindow)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(centralwidget.sizePolicy().hasHeightForWidth())
        centralwidget.setSizePolicy(size_policy)
        centralwidget.setObjectName("centralwidget")
        gridLayout = QtWidgets.QGridLayout(centralwidget)
        gridLayout.setObjectName("gridLayout")
        self.mines_container = QtWidgets.QWidget(centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.mines_container.sizePolicy().hasHeightForWidth())
        self.mines_container.setSizePolicy(size_policy)
        self.mines_container.setObjectName("mines_container")
        self.container = QtWidgets.QGridLayout(self.mines_container)
        self.container.setContentsMargins(0, 0, 0, 0)
        self.container.setSpacing(0)
        self.container.setObjectName("container")
        gridLayout.addWidget(self.mines_container, 1, 0, 1, 6)
        self.scores = QtWidgets.QLabel(centralwidget)
        self.scores.setText("0")
        self.scores.setFont(QtGui.QFont("Fixedsys"))
        self.scores.setObjectName("scores")
        gridLayout.addWidget(self.scores, 2, 1, 1, 1)
        self.scorelabel = QtWidgets.QLabel(centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.scorelabel.sizePolicy().hasHeightForWidth())
        self.scorelabel.setSizePolicy(size_policy)
        self.scorelabel.setAutoFillBackground(False)
        self.scorelabel.setScaledContents(False)
        self.scorelabel.setOpenExternalLinks(False)
        self.scorelabel.setObjectName("scorelabel")
        self.flag_counter = difficulty[self.diff]['mines']
        gridLayout.addWidget(self.scorelabel, 2, 0, 1, 1)
        self.mines = QtWidgets.QLabel(centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.mines.sizePolicy().hasHeightForWidth())
        self.mines.setSizePolicy(size_policy)
        self.mines.setText(str(difficulty[self.diff]["mines"]))
        self.mines.setObjectName("mines")
        gridLayout.addWidget(self.mines, 2, 5, 1, 1)
        self.mineslabel = QtWidgets.QLabel(centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.mineslabel.sizePolicy().hasHeightForWidth())
        self.mineslabel.setSizePolicy(size_policy)
        self.mines.setFont(QtGui.QFont("Fixedsys"))
        self.mineslabel.setObjectName("mineslabel")
        gridLayout.addWidget(self.mineslabel, 2, 4, 1, 1)
        MainWindow.setCentralWidget(centralwidget)
        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.start()
        self.opened = 0

    def start(self):
        self.insert_buttons()

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.RightButton:
                if obj.is_open:
                    pass
                elif obj.label == '?':
                    obj.label = ''
                    obj.setText(obj.label)
                    obj.setEnabled(True)
                    obj.flag = False
                    self.flag_counter += 1
                elif self.flag_counter < 1:
                    pass
                else:
                    if obj.label == '':
                        obj.label = '?'
                        obj.setText(obj.label)
                        obj.setEnabled(False)
                        obj.flag = True
                        self.flag_counter -= 1
                self.mines.setText(str(self.flag_counter))

        return QtCore.QObject.event(obj, event)

    def indexes(self, elem: Button):
        if Ui_MainWindow.First_click:
            self.mine_id(elem.id)
            self.count_mines()
            Ui_MainWindow.First_click = False
        if elem.is_mine:
            elem.setStyleSheet("background-color: purple")
            elem.is_open = True
            Ui_MainWindow.Game_over = True
            self.open_button()
            self.gameover()
        elif elem.bomb_counter:
            elem.setText(str(elem.bomb_counter))
            elem.setStyleSheet("QPushButton {border:  none}")
            elem.is_open = True
            if elem.bomb_counter:
                self.opened += 1
            self.points += 100
            if self.opened >= difficulty[self.diff]['row'] * difficulty[self.diff][
                'column'] - \
                    len(self.mine_index):
                self.victory()
            self.scores.setText(str(self.points))
            elem.clicked.disconnect()
            if elem.bomb_counter == 1:
                elem.setStyleSheet("color: blue")
            elif elem.bomb_counter == 2:
                elem.setStyleSheet("color: green")
            elif elem.bomb_counter == 3:
                elem.setStyleSheet("color: red")
            elif elem.bomb_counter == 4:
                elem.setStyleSheet('color: orange')
            elif elem.bomb_counter == 5:
                elem.setStyleSheet("color: purple")
            elif elem.bomb_counter == 6:
                elem.setStyleSheet("color: yellow")
            elif elem.bomb_counter == 7:
                elem.setStyleSheet('color: brown')
            elif elem.bomb_counter == 8:
                elem.setStyleSheet('color: black')
        else:
            self.first_search(elem)

    def first_search(self, btn: Button):
        queue = [btn]
        while queue:
            crnt_btn = queue.pop()
            if crnt_btn.bomb_counter:
                crnt_btn.is_open = True
                crnt_btn.setText(str(crnt_btn.bomb_counter))
                crnt_btn.setStyleSheet("QPushButton {border: none}")
            if crnt_btn.is_open and not crnt_btn.bomb_counter == 0:
                self.opened += 1
                if crnt_btn.bomb_counter == 1:
                    crnt_btn.setStyleSheet("color: blue")
                elif crnt_btn.bomb_counter == 2:
                    crnt_btn.setStyleSheet("color: green")
                elif crnt_btn.bomb_counter == 3:
                    crnt_btn.setStyleSheet("color: red")
                elif crnt_btn.bomb_counter == 4:
                    crnt_btn.setStyleSheet('color: orange')
                elif crnt_btn.bomb_counter == 5:
                    crnt_btn.setStyleSheet("color: purple")
                elif crnt_btn.bomb_counter == 6:
                    crnt_btn.setStyleSheet("color: yellow")
                elif crnt_btn.bomb_counter == 7:
                    crnt_btn.setStyleSheet('color: brown')
                elif crnt_btn.bomb_counter == 8:
                    crnt_btn.setStyleSheet('color: black')
                self.points += 100
                if self.opened >= difficulty[self.diff]['row'] * difficulty[self.diff][
                    'column'] - \
                        len(self.mine_index):
                    self.victory()
                self.scores.setText(str(self.points))
                if crnt_btn.flag and crnt_btn.bomb_counter:
                    crnt_btn.setEnabled(True)
                    self.flag_counter += 1
                    self.mines.setText(str(self.flag_counter))
            else:
                self.points += 100
                crnt_btn.setText(str(""))
                crnt_btn.setStyleSheet("QPushButton {border:  none}")
                self.scores.setText(str(self.points))
                if crnt_btn.flag:
                    crnt_btn.setEnabled(True)
                    self.flag_counter += 1
                    self.mines.setText(str(self.flag_counter))
            crnt_btn.clicked.disconnect()
            crnt_btn.is_open = True
            if crnt_btn.bomb_counter == 0 and not crnt_btn.bomb_counter:
                self.opened += 1
            if self.opened >= difficulty[self.diff]['row'] * difficulty[self.diff][
                'column'] - \
                    len(self.mine_index):
                self.victory()
            if crnt_btn.bomb_counter == 0:
                x, y = crnt_btn.x, crnt_btn.y
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        next_btn = self.buttons[x + dx][y + dy]
                        if (
                                not next_btn.is_open
                                and 1 <= next_btn.x <= difficulty[self.diff]["row"]
                                and 1 <= next_btn.y <= difficulty[self.diff]["column"]
                                and next_btn not in queue
                        ):
                            queue.append(next_btn)

    def insert_buttons(self):
        count = 1
        for i in range(1, difficulty[self.diff]["row"] + 1):
            for j in range(1, difficulty[self.diff]["column"] + 1):
                btn = self.buttons[i][j]
                btn.id = count
                self.container.addWidget(btn, i, j)
                count += 1

    def open_button(self):
        for i in range(difficulty[self.diff]["row"] + 2):
            for j in range(difficulty[self.diff]["column"] + 2):
                opened_btn = self.buttons[i][j]
                if opened_btn.is_mine:
                    opened_btn.setStyleSheet("background-color: purple")
                elif opened_btn.bomb_counter == 0:
                    opened_btn.setText("")
                else:
                    opened_btn.setText(str(opened_btn.bomb_counter))
                    if opened_btn.bomb_counter == 1:
                        opened_btn.setStyleSheet("color: blue")
                    elif opened_btn.bomb_counter == 2:
                        opened_btn.setStyleSheet("color: green")
                    elif opened_btn.bomb_counter == 3:
                        opened_btn.setStyleSheet("color: red")
                    elif opened_btn.bomb_counter == 4:
                        opened_btn.setStyleSheet('color: orange')
                    elif opened_btn.bomb_counter == 5:
                        opened_btn.setStyleSheet("color: purple")
                    elif opened_btn.bomb_counter == 6:
                        opened_btn.setStyleSheet("color: yellow")
                    elif opened_btn.bomb_counter == 7:
                        opened_btn.setStyleSheet('color: brown')
                    elif opened_btn.bomb_counter == 8:
                        opened_btn.setStyleSheet('color: black')
                opened_btn.setDisabled(True)

    def mine_id(self, id: int):
        self.mine_index = self.generatemines(id)
        for i in range(1, difficulty[self.diff]["row"] + 1):
            for j in range(1, difficulty[self.diff]["column"] + 1):
                btn = self.buttons[i][j]
                if btn.id in self.mine_index:
                    btn.is_mine = True

    def count_mines(self):
        for i in range(1, difficulty[self.diff]["row"] + 1):
            for j in range(1, difficulty[self.diff]["column"] + 1):
                btn = self.buttons[i][j]
                bomb_counter = 0
                if not btn.is_mine:
                    for row_dx in [-1, 0, 1]:
                        for col_dx in [-1, 0, 1]:
                            neighbour = self.buttons[i + row_dx][j + col_dx]
                            if neighbour.is_mine:
                                bomb_counter += 1
                btn.bomb_counter = bomb_counter

    def generatemines(self, exclude_number: int):
        index = list(range(1, difficulty[self.diff]["row"] * difficulty[self.diff]["column"] + 1))
        index.remove(exclude_number)
        shuffle(index)
        return index[:difficulty[self.diff]["mines"]]

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Minesweeper"))
        self.scorelabel.setText(_translate("MainWindow", "Score:"))
        self.scorelabel.setFont(QtGui.QFont("Fixedsys"))
        self.mineslabel.setText(_translate("MainWindow", "Mines:"))
        self.mineslabel.setFont(QtGui.QFont("Fixedsys"))

    def gameover(self):
        gameover = QMessageBox()
        gameover.setWindowTitle("GameOver")
        gameover.setText("BOOM\nyou stepped on a mine :^(")
        change_difficulty = gameover.addButton('Change difficulty', QMessageBox.ActionRole)
        gameover.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        gameover.accepted.connect(self.restart)
        gameover.rejected.connect(lambda: sys.exit(0))
        gameover.exec_()
        if gameover.clickedButton() == change_difficulty:
            self.change_difficulty()

    def victory(self):
        win = QMessageBox()
        win.setWindowTitle("Victory")
        win.setText("Congratulations")
        win.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry)
        win.rejected.connect(lambda: sys.exit(0))
        win.accepted.connect(self.restart)
        win.exec_()

    def change_difficulty(self):
        Ui_difficulty()
        self.MainWindow.close()
        self.opened = 0
        self.points = 0
        Ui_MainWindow.First_click = True

    def restart(self):
        self.opened = 0
        self.points = 0
        Ui_MainWindow.First_click = True
        flag_counter = difficulty[self.diff]['mines']
        self.mines.setText(str(flag_counter))
        self.scores.setText(str(self.points))
        for i in range(difficulty[self.diff]["row"] + 2):
            for j in range(difficulty[self.diff]["column"] + 2):
                opened_btn = self.buttons[i][j]
                opened_btn.deleteLater()
        self.__init__(self.diff)


app = QtWidgets.QApplication(sys.argv)
ex = Ui_difficulty()
sys.exit(app.exec())
