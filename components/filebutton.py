from .ui.button import Button
import wx
import os


class FileButton(Button):
    def __init__(self, parent, notebook: wx.Notebook, **kwargs):
        Button.__init__(self, parent, label="Open File",
                        onClick=lambda event: self.openFile(event, notebook),
                        size="md",
                        ** kwargs)

        # bmp = wx.Bitmap("components/assests/upload.png")
        # self.SetBitmap(bmp)

    def openFile(self, event, notebook):
        wildcard = "TXT files (*.txt)|*.txt"
        dlg = wx.FileDialog(self, "Open file...", os.getcwd(),
                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST, wildcard=wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            # read file contents
            with open(path, 'r') as f:
                notebook.uploaded_code = f.read()
        notebook.Refresh()

        dlg.Destroy()
