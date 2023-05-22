"""
Class for button widget using wxPython
"""

import wx


class Button(wx.Button):
    """Button widget class."""

    def __init__(self, parent, label, handler, bg_color="black", border_radius=5):
        """Initialise the button widget."""
        super().__init__(parent, label=label, style=wx.BORDER_NONE)
        self.Bind(wx.EVT_BUTTON, handler)
        self.SetBackgroundColour("grey")
        self.SetForegroundColour("white")
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnHover)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnUnHover)

        self.border_radius = border_radius

    def OnHover(self, event):
        self.SetBackgroundColour("grey")
        self.SetForegroundColour("yellow")
        self.Refresh()  # Refresh the button to apply changes
        event.Skip()

    def OnUnHover(self, event):
        self.SetBackgroundColour("grey")
        self.SetForegroundColour("white")
        self.Refresh()  # Refresh the button to apply changes
        event.Skip()

    # def DoGetBestSize(self):
    #     size = super().DoGetBestSize()
    #     size.IncBy(self.border_radius * 2, self.border_radius * 2)
    #     return size

    # def DoDrawForeground(self, dc, rect):
    #     dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
    #     dc.Clear()
    #     dc.SetBrush(wx.TRANSPARENT_BRUSH)
    #     dc.SetPen(wx.Pen(self.GetForegroundColour()))
    #     dc.DrawRoundedRectangle(rect, self.border_radius)
    #     super().DoDrawForeground(dc, rect)
