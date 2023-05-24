import wx
from .ui.colors import COLORS
from typing import Union

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

    def Attach(self, parent: Union[wx.BoxSizer, wx.Panel], proportion, flag, border):
        """Attach the heading to the parent."""
        parent.Add(self, proportion, flag, border)


class ScrollBox(wx.ScrolledWindow):
    def __init__(self, parent, bg_color=COLORS.GRAY_900, dir="col"):
        super().__init__(parent)
        self.SetBackgroundColour(bg_color)

        self.SetScrollRate(5, 5)

        self.sizer = wx.BoxSizer(directions[dir])
        self.SetSizer(self.sizer)

    def Add(self, item, proportion=0, flag=wx.ALL, border=0):
        self.sizer.Add(item, proportion, flag, border)

    def Attach(self, parent: Union[wx.BoxSizer, wx.Panel], proportion, flag, border):
        """Attach the heading to the parent."""
        parent.Add(self, proportion, flag, border)
