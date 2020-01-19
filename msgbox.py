

from PyQt5.QtWidgets import QMessageBox

def msgbox(text, buttons = QMessageBox.Ok, fun_ok = None, fun_cancel = None, msg_type = QMessageBox.Information, title = "Внимание!", add_info = None, detailed_info = None):
    msg = QMessageBox()
    msg.setIcon(msg_type)
    msg.setText(text)
    msg.setWindowTitle(title)
    if add_info is not None:
        msg.setInformativeText(add_info)
    if detailed_info is not None:
        msg.setDetailedText(detailed_info)
    return msg.exec_()