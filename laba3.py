import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog

# Сделаем упорядоченные списки букв.
# Русские и английские.

a = ord('а')
rusLow = [chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)]
a = ord('А')
rusCapital = [chr(i) for i in range(a,a+6)] + [chr(a+33)] + [chr(i) for i in range(a+6,a+32)]
a = ord('a')
engLow = [chr(i) for i in range(a,a+26)]
a = ord('A')
engCapital = [chr(i) for i in range(a,a+26)]

def encrypt(msg):
    res = ''
    for c in msg:
        # ROT20 - сдвигаем символ на 20 позиций. 
        # Если вылезли за конец алфавита, то начинаем с начала.
        if c in rusLow:
            idx = rusLow.index(c)
            idx += 20
            if idx >= len(rusLow):
                idx = idx - len(rusLow)
            res += rusLow[idx]
        elif c in rusCapital:
            idx = rusCapital.index(c)
            idx += 20
            if idx >= len(rusCapital):
                idx = idx - len(rusCapital)
            res += rusCapital[idx]
        elif c in engLow:
            idx = engLow.index(c)
            idx += 20
            if idx >= len(engLow):
                idx = idx - len(engLow)
            res += engLow[idx]
        elif c in engCapital:
            idx = engCapital.index(c)
            idx += 20
            if idx >= len(engCapital):
                idx = idx - len(engCapital)
            res += engCapital[idx]
        else:
            # Символы не из алфавитов оставляем как есть
            res += c
    return res

def decrypt(msg):
    # Аналогично encrypt, только сдвиг в другую сторону
    res = ''
    for c in msg:
        if c in rusLow:
            idx = rusLow.index(c)
            idx -= 20
            if idx < 0:
                idx += len(rusLow)
            res += rusLow[idx]
        elif c in rusCapital:
            idx = rusCapital.index(c)
            idx -= 20
            if idx < 0:
                idx += len(rusCapital)
            res += rusCapital[idx]
        elif c in engLow:
            idx = engLow.index(c)
            idx -= 20
            if idx < 0:
                idx += len(engLow)
            res += engLow[idx]
        elif c in engCapital:
            idx = engCapital.index(c)
            idx -= 20
            if idx < 0:
                idx += len(engCapital)
            res += engCapital[idx]
        else:
            # Символы не из алфавитов оставляем как есть
            res += c
    return res

class MainForm(QMainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        loadUi("form.ui", self)

    def onCryptClick(self):
        # Пользователь выбирает файл, в который сохранится зашифрованный результат
        fileName, _ = QFileDialog.getSaveFileName(None, "Text file", ".", "Text file (*.txt);;All files (*.*)")
        if not fileName:
            return
        msg = self.textEdit.toPlainText()
        res = encrypt(msg);
        f = open(fileName, "w")
        f.write(res)
        f.close()

    def onDecryptClick(self):
        # Загружаем шифрованый текст из файла
        fileName, _ = QFileDialog.getOpenFileName(None, "Text file", ".", "Text file (*.txt);;All files (*.*)")
        if not fileName:
            return
        f = open(fileName, "r")
        msg = f.read()
        res = decrypt(msg);
        self.textEdit_2.setPlainText(res)

    def onExitClick(self):
        msgbox = QMessageBox(QMessageBox.Question, "Confirm exit", "Вы действительно хотите выйти?")
        msgbox.addButton(QMessageBox.Yes)
        msgbox.addButton(QMessageBox.No)
        msgbox.setDefaultButton(QMessageBox.No)
        reply = msgbox.exec()
        if reply != QMessageBox.Yes:
            return
        widget.setCurrentWidget(loginWin)

# Окно логина или регистрации
class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.setMinimumSize(QtCore.QSize(400, 300))

    # проверим Существует ли такой логин и совпадает ли пароль
    def checkPass(self, login, passwd):
        # словарь логинов-паролей
        self.creds = {}
        # Храним логины-пароли в файле в зашифрованном виде,
        try:
            f = open("users.db")
            for l in f.readlines():
                l = decrypt(l.strip())
                (login, passwd) = l.split(":");
                self.creds[login] = passwd
            f.close()
        except:
            pass
        if login in self.creds and self.creds[login] == passwd:
            return True
        return False

    # Реакция на нажатие кнопки входа
    def tryLogin(self):
        login = self.lineEdit.text()
        passwd = self.lineEdit_2.text()
        if self.checkPass(login, passwd):
            widget.setFixedWidth(800)
            widget.setFixedHeight(600)
            widget.setCurrentWidget(cryptoform)
        else:
            error = QMessageBox()
            error.setWindowTitle("Ошибка входа")
            error.setText("Логин не существует либо пароль неверен")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec_()

    def newReg(self):
        widget.setCurrentWidget(newRegWin)

# Класс отвечающий за окно регистрации
class Registration(QMainWindow):
    def __init__(self):
        super(Registration, self).__init__()
        loadUi("registration.ui", self)

    def addReg(self):
        login = self.lineEdit.text().strip()
        passwd = self.lineEdit_2.text()
        passwd2 = self.lineEdit_3.text()
        if passwd != passwd2 or len(login) == 0 or len(passwd) == 0:
            error = QMessageBox()
            error.setWindowTitle("Ошибка")
            if passwd != passwd2:
                error.setText("Введены разные пароли!")
            if len(login) == 0:
                error.setText("Введен пустой логин!")
            if len(passwd) == 0:
                error.setText("Введен пустой пароль!")
            error.setIcon(QMessageBox.Warning)
            error.setStandardButtons(QMessageBox.Ok)
            error.exec()
        else:
            f = open("users.db", "a")
            l = encrypt(login + ":" + passwd)
            f.write(l + "\n")
            f.close()
            widget.setFixedWidth(400)
            widget.setFixedHeight(300)
            widget.setCurrentWidget(loginWin)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    cryptoform = MainForm()
    loginWin = Login()
    newRegWin = Registration()
    widget.addWidget(loginWin)
    widget.addWidget(cryptoform)
    widget.addWidget(newRegWin)
    widget.setFixedWidth(400)
    widget.setFixedHeight(300)
    widget.setCurrentWidget(loginWin)
    widget.show()
    sys.exit(app.exec())
