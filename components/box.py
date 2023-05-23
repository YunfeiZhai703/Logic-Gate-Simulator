import wx
from .ui.colors import COLORS

directions = {
    "col": wx.VERTICAL,
    "row": wx.HORIZONTAL
}


class Box(wx.Panel):
    def __init__(self, parent, bg_color=COLORS.GRAY_900, dir="col"):
        super().__init__(parent)
        self.SetBackgroundColour(bg_color)

        self.sizer = wx.BoxSizer(directions[dir])
        self.SetSizer(self.sizer)

    def Add(self, item, proportion=0, flag=wx.ALL, border=0):
        self.sizer.Add(item, proportion, flag, border)
