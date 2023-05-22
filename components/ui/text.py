import wx
from .colors import COLORS


class Text(wx.StaticText):
    def __init__(self, parent, label, size=wx.DefaultSize, style=wx.ALIGN_CENTER):
        super().__init__(parent, label=label, size=size, style=style)
        self.SetForegroundColour(COLORS.GRAY_100)
        # make font monospace
        font = wx.Font(10, wx.FONTFAMILY_TELETYPE,
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(font)
