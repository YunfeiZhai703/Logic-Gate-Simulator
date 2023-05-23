from .ui.button import Button
import wx
import os


class FileButton(Button):
    def __init__(self, parent, **kwargs):
        Button.__init__(self, parent, label="Open File",
                        onClick=self.openFile, **kwargs)
        self._file = None
        self._path = None

    def openFile(self, event):
        wildcard = "TXT files (*.txt)|*.txt"
        dlg = wx.FileDialog(self, "Open file...", os.getcwd(),
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self._path = dlg.GetPath()

            # read file contents
            with open(self._path, 'r') as f:
                self._file = f.read()
            print(self._file)
            # self.SetLabel(self._file)
        dlg.Destroy()
