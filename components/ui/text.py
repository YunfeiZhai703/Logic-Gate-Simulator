import wx
from .colors import COLORS

fonts = {
    "roman": wx.FONTFAMILY_ROMAN,
    "script": wx.FONTFAMILY_SCRIPT,
    "decorative": wx.FONTFAMILY_DECORATIVE,
    "swiss": wx.FONTFAMILY_SWISS,
    "modern": wx.FONTFAMILY_MODERN,
    "teletype": wx.FONTFAMILY_TELETYPE,
    "default": wx.FONTFAMILY_DEFAULT,
}


class Text(wx.StaticText):
    """Text is a component that displays tex using a specified font and styling"""

    def __init__(
            self,
            parent,
            label,
            size=wx.DefaultSize,
            style=wx.ALIGN_CENTER,
            font_size=10,
            font_family="default"):
        super().__init__(parent, label=label, size=size, style=style)
        self.SetForegroundColour(COLORS.GRAY_100)
        # make font monospace

        font = wx.Font(font_size, fonts[font_family],
                       wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.SetFont(font)
