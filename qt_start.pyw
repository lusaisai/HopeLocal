import sys
import time
from socket import socket
from threading import Thread
from PyQt4.QtGui import *
import start_services
import settings
import os.path
from multiprocessing import Process


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.create_main_window()
        self.create_actions()
        self.create_tray_icon()
        self.run_services()
        self.run_update_status_thread()

    def create_main_window(self):
        self.icon = QIcon(os.path.join(settings.app_dir, 'docs', 'hope.ico'))

        self.resize(320, 180)
        self.setWindowTitle("Hope")
        self.setWindowIcon(self.icon)

        self.restart_btn = QPushButton('Restart Services', self)
        self.restart_btn.resize(200, 80)
        self.restart_btn.move(60, 50)
        self.restart_btn.setFont(QFont("Consolas", 16))
        self.restart_btn.clicked.connect(self.restart)

        self.statusBar()

    def restart(self):
        self.restart_btn.setEnabled(False)
        reload(start_services)
        self.stop_services()
        self.run_services()
        self.restart_btn.setEnabled(True)
        self.statusBar().showMessage("Services restarted")
        self.run_update_status_thread()

    def create_actions(self):
        self.quit_action = QAction("&Quit", self, triggered=self.close)

    def create_tray_icon(self):
        self.tray_icon_menu = QMenu(self)
        self.tray_icon_menu.addAction(self.quit_action)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setContextMenu(self.tray_icon_menu)

        self.tray_icon.setIcon(self.icon)
        self.tray_icon.activated.connect(self.tray_activated)

        self.tray_icon.setToolTip("Hope")

        self.tray_icon.show()

    def tray_activated(self, reason):
        if reason == 2:
            if self.isVisible():
                self.hide()
            else:
                self.showNormal()

    def closeEvent(self, event):
            self.hide()
            event.ignore()

    def run_services(self):
        self.statusBar().showMessage("Running Services ...")
        self.process = Process(target=start_services.run_services)
        self.process.start()

    def stop_services(self):
        self.statusBar().showMessage("Stopping Services ...")
        if self.process:
            self.process.terminate()
            self.process = None

    def update_status(self):
        time.sleep(60)
        s = socket()
        s.connect(settings.info_server_address)
        while True:
            s.sendall('info')
            data = s.recv(4096)
            self.statusBar().showMessage(data)
            time.sleep(settings.ip_check_interval)

    def run_update_status_thread(self):
        t = Thread(target=self.update_status)
        t.setDaemon(True)
        t.start()

    def close(self):
        self.stop_services()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    # w.show()
    sys.exit(app.exec_())
