from .ui.button import Button
from .ui.colors import COLORS
import wx
import os


class FileButton(Button):
    def __init__(self, parent, notebook: wx.Notebook, **kwargs):
        Button.__init__(self, parent, label="Open File",
                        onClick=lambda event: self.openFile(event, notebook),
                        size="md",
                        color=COLORS.TEAL_700,
                        ** kwargs)

    def openFile(self, event, notebook):
        wildcard = "TXT files (*.txt)|*.txt"
        dlg = wx.FileDialog(
            self,
            "Open file...",
            os.getcwd(),
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
            wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            notebook.file_path = path
            with open(path, 'r') as f:
                notebook.uploaded_code = f.read()
        notebook.Refresh()

        dlg.Destroy()
