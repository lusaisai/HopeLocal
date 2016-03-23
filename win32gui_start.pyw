import win32api
import win32gui
import win32con
import os
import start_services
import settings
from multiprocessing import Process


class MainWindow:
    def __init__(self):
        msg_task_bar_restart = win32gui.RegisterWindowMessage("Hope")
        message_map = {
                msg_task_bar_restart: self.on_restart,
                win32con.WM_DESTROY: self.on_destroy,
                win32con.WM_COMMAND: self.on_command,
                win32con.WM_USER+20: self.on_task_bar_notify,
        }

        wc = win32gui.WNDCLASS()
        h_inst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "Hope"
        wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW
        wc.hCursor = win32api.LoadCursor(0, win32con.IDC_ARROW)
        wc.hbrBackground = win32con.COLOR_WINDOW
        wc.lpfnWndProc = message_map
        win32gui.RegisterClass(wc)

        style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
        self.hwnd = win32gui.CreateWindow(wc.lpszClassName, "Hope", style, 0, 0, win32con.CW_USEDEFAULT,
                                          win32con.CW_USEDEFAULT, 0, 0, h_inst, None)
        win32gui.UpdateWindow(self.hwnd)
        self.create_icons()
        self.process = None

    def create_icons(self):
        h_inst = win32api.GetModuleHandle(None)
        icon_file = os.path.join(settings.app_dir, 'docs', 'hope.ico')
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = win32gui.LoadImage(h_inst, icon_file, win32con.IMAGE_ICON, 0, 0, icon_flags)
        flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
        nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, "Hope")
        try:
            win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
        except RuntimeError:
            pass

    def on_restart(self, hwnd, msg, wparam, lparam):
        reload(start_services)
        self.create_icons()
        self.stop_services()
        self.run_services()

    def on_destroy(self, hwnd, msg, wparam, lparam):
        nid = (self.hwnd, 0)
        win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
        win32gui.PostQuitMessage(0)

    def on_task_bar_notify(self, hwnd, msg, wparam, lparam):
        if lparam == win32con.WM_LBUTTONUP or lparam == win32con.WM_RBUTTONUP:
            menu = win32gui.CreatePopupMenu()
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1024, "Restart")
            win32gui.AppendMenu(menu, win32con.MF_STRING, 1025, "Exit")
            pos = win32gui.GetCursorPos()
            win32gui.SetForegroundWindow(self.hwnd)
            win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
            win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)

    def run_services(self):
        self.process = Process(target=start_services.run_services)
        self.process.start()

    def stop_services(self):
        if self.process:
            self.process.terminate()
            self.process = None

    def on_command(self, hwnd, msg, wparam, lparam):
        item_id = win32api.LOWORD(wparam)
        if item_id == 1024:
            self.stop_services()
            self.run_services()
        elif item_id == 1025:
            self.stop_services()
            win32gui.DestroyWindow(self.hwnd)
        else:
            pass

if __name__ == '__main__':
    w = MainWindow()
    w.run_services()
    win32gui.PumpMessages()
