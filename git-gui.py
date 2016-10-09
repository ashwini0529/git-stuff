#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import requests
from PyQt4.QtCore import *
from PyQt4.QtGui import *

repo_name = None
user_name = None


class Main(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()

    def initUI(self):
        self.win = QWidget()

        self.repo_view = False

        self.l1 = QLabel("Github Username")

        self.nm = QLineEdit(self)
        self.nm.setMinimumWidth(200)
        self.nm.editingFinished.connect(self.enterPress)

        self.l2 = QLabel("Repository")

        self.add1 = QLineEdit(self)
        self.add1.setMinimumWidth(200)

        self.fbox = QFormLayout()
        self.fbox.addRow(self.l1, self.nm)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.add1)
        self.fbox.addRow(self.l2, self.vbox)

        self.submitButton = QPushButton("Submit")
        self.cancelButton = QPushButton("Cancel")
        self.fbox.addRow(self.submitButton, self.cancelButton)
        self.submitButton.clicked.connect(self.submit)

        self.win.setLayout(self.fbox)
        self.setWindowTitle("Github GUI")
        self.setCentralWidget(self.win)
        self.resize(self.win.minimumSize())
        self.show()

    def enterPress(self):
        self.add1.setFocus()

    def submit(self):
        global repo_name
        global user_name
        repo_name = self.add1.text()
        user_name = self.nm.text()
        if(repo_name is None or user_name is None):
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("User or repo name can't be empty")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            return
        self.switch_view()

    def switch_view(self):
        if(self.repo_view is False):
            self.repo_view = True
            global user_name
            global repo_name
            user_page = "http://github.com/" + user_name
            repo_page = user_page + "/" + repo_name
            res = requests.get(user_page)
            if(res.status_code == 404):
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("User doesn't exists.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                self.repo_view = False
                return
            else:
                soup = BeautifulSoup(res.text, "html.parser")
                followers = soup.find('a', {'href': '/' + user_name + '?tab=followers'}).find('span').text.strip()
                following = soup.find('a', {'href': '/' + user_name + '?tab=following'}).find('span').text.strip()
                res = requests.get(repo_page)
                if(res.status_code == 404):
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Repository doesn't exists.")
                    msg.setWindowTitle("Error")
                    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                    self.repo_view = False
                    return

            soup = BeautifulSoup(res.text, "html.parser")
            try:
                short_desc = soup.find("span", {"itemprop": "about"}).text
            except:
                short_desc = "No description available"

            issue_tag = soup.find('a', {"data-hotkey": "g i"})
            issues = issue_tag.find('span', {'class': 'counter'}).text

            pr_tag = soup.find('a', {"data-hotkey": "g p"})
            prs = pr_tag.find('span', {'class': 'counter'}).text

            main_tag = soup.find('li', {'class': 'commits'})

            commits = main_tag.find('span').text.strip()
            branches = main_tag.find_next("li").find('span').text.strip()
            releases = main_tag.find_next("li").find_next("li").find('span').text.strip()
            contributors = main_tag.find_next("li").find_next("li").find_next("li").find('span').text.strip()

            overview_files = soup.findAll('tr', {'class': 'js-navigation-item'})
            files = list()

            for file in overview_files:
                files.append([file.find('a').text.strip(),
                              file.find('td', {'class': 'message'}).find('a').attrs["title"],
                              file.find('td', {'class': 'age'}).text.strip()
                              ])

            try:
                watchers = soup.find('a', {'href': '/' + user_name + '/' + repo_name + '/watchers'}).text.strip()
            except:
                watchers = "0"
            try:
                stars = soup.find('a', {'href': '/' + user_name + '/' + repo_name + '/stargazers'}).text.strip()
            except:
                stars = "0"
            try:
                forks = soup.find('a', {'href': '/' + user_name + '/' + repo_name + '/network'}).text.strip()
            except:
                forks = "0"

            self.font = QFont("Times", 16, QFont.Bold)

            self.user = QLabel(user_name)
            self.user.setFont(self.font)
            self.repo_name = QLabel(repo_name)
            self.repo_name.setFont(self.font)
            self.title = QLabel(short_desc)
            self.title.setFont(self.font)

            self.issue = QLabel("Issues | " + issues)
            self.pr = QLabel("Pull Requests | " + prs)

            self.follower = QLabel("Followers | " + followers)
            self.followee = QLabel("Following | " + following)

            self.watcher = QLabel("Watchers | " + watchers)
            self.star = QLabel("Stars | " + stars)
            self.fork = QLabel("Forks | " + forks)

            self.commit = QLabel(commits + " commits")
            self.branch = QLabel(branches + " branches")
            self.release = QLabel(releases + " releases")
            self.contributor = QLabel(contributors + " contributors")

            self.file_overview = QLabel("Files Overview")

            self.main_grid = QGridLayout()
            self.main_grid.setSpacing(0)

            self.area = QScrollArea(self)
            self.area.setWidgetResizable(True)

            self.main_grid.addWidget(self.user, 0, 0)
            self.main_grid.addWidget(self.follower, 0, 2)
            self.main_grid.addWidget(self.followee, 0, 3)
            self.main_grid.addWidget(self.repo_name, 1, 0)
            self.main_grid.addWidget(self.watcher, 2, 1)
            self.main_grid.addWidget(self.star, 2, 2)
            self.main_grid.addWidget(self.fork, 2, 3)
            self.main_grid.addWidget(self.title, 3, 0)

            self.main_grid.addWidget(self.issue, 4, 0)
            self.main_grid.addWidget(self.pr, 4, 2)

            for i in range(len(files)):
                self.main_grid.addWidget(QLabel(files[i][0]), i + 6, 0)
                self.main_grid.addWidget(QLabel(files[i][1]), i + 6, 1)
                self.main_grid.addWidget(QLabel(files[i][2]), i + 6, 3)

            self.central_widget = QWidget()
            self.central_widget.setLayout(self.main_grid)
            self.area.setWidget(self.central_widget)

            self.vbar = self.area.verticalScrollBar()
            self.vbar.setValue(self.vbar.maximum())

            self.setCentralWidget(self.area)

            self.resize(self.central_widget.width() + 20, self.central_widget.height() + 20)
            self.show()

        else:
            self.repo_view = False
            self.initUI()

    def keyPressEvent(self, event):
        key = event.key()
        if(key == Qt.Key_Backspace):
            self.switch_view()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    sys.exit(app.exec_())
