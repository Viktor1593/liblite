'''
    simple realisation of massage box
'''

from PyQt5.QtWidgets import QMessageBox

def msgbox(text: str, buttons: any = QMessageBox.Ok, fun_ok: any = None, fun_cancel: any = None, msg_type: any = QMessageBox.Information, title: str = "Внимание!", add_info: any = None, detailed_info: any = None):
    '''
    raise msgbox
    
    :param text: text to display
    :param buttons: buttons to display: Ok | Open | Save | Cancel | Close | Discard | Apply | Reset | RestoreDefaults | Help | SaveAll | Yes | YesToAll | No | NoToAll | Abort | Retry | Ignore | NoButton
    :param fun_ok: function to call if pressed ok (developing)
    :param fun_cancel: function to call if pressed ok (developing)
    :param msg_type: icon of msg box: NoIcon | Question | Information | Warning | Critical
    :param title: Sets the title of the message box to title. On macOS, the window title is ignored (as required by the macOS Guidelines).
    :param add_info: fuller description for the message
    :param detailed_info: the text to be displayed in the details area
	:return: Nothing
    '''
    msg = QMessageBox()
    msg.setIcon(msg_type)
    msg.setText(text)
    msg.setWindowTitle(title)
    if add_info is not None:
        msg.setInformativeText(add_info)
    if detailed_info is not None:
        msg.setDetailedText(detailed_info)
    msg.exec_()
    return None
