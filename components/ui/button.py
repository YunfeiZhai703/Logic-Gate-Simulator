"""
Class for button widget using wxPython
"""

import wx
from .colors import COLORS
from typing import Literal, Tuple, Union

button_size_type = Union[Literal["xs", "sm",
                                 "md", "lg", "xl"], Tuple[int, int]]


class Button(wx.Button):
    """Button widget class."""

    def __init__(self, parent, label, handler, bg_color=COLORS.GRAY_800,
                 hover_bg_color=COLORS.GRAY_700,
                 fg_color=COLORS.WHITE,
                 hover_fg_color=COLORS.RED_200,
                 size: button_size_type = "sm"
                 ):
        """Custom button widget.

        Args:
            parent (): Parent widget.
            label (str): Text to display on the button.
            handler (function): callback function to call when the button is clicked.
            bg_color (COLORS, optional): Bg color. Defaults to COLORS.GRAY_800.
            hover_bg_color (COLORS, optional): Hover BG color. Defaults to COLORS.GRAY_700.
            fg_color (COLORS, optional): Foreground color. Defaults to COLORS.WHITE.
            hover_fg_color (COLORS, optional): Foreground hover color. Defaults to COLORS.RED_200.
            size (buttonSizeType, optional): xs, sm, md, kg, xl or Tuple[int, int]. Defaults to "sm".
        """

        super().__init__(parent, label=label, style=wx.BORDER_NONE)
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_bg_color = hover_bg_color
        self.hover_fg_color = hover_fg_color

        self.SetBackgroundColour(bg_color)
        self.SetForegroundColour(fg_color)

        self.Bind(wx.EVT_BUTTON, handler)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnHover)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnUnHover)

        self.SetSize(size)

    def SetSize(self, size: button_size_type):
        """Set the size of the button."""
        if isinstance(size, str):
            if size == "xs":
                self.SetMinSize((50, 20))
            elif size == "sm":
                self.SetMinSize((70, 25))
            elif size == "md":
                self.SetMinSize((100, 30))
            elif size == "lg":
                self.SetMinSize((200, 50))
            elif size == "xl":
                self.SetMinSize((250, 60))
        elif isinstance(size, tuple):
            self.SetMinSize(size)

    def OnHover(self, event):
        self.SetBackgroundColour(self.hover_bg_color)
        self.SetForegroundColour(self.hover_fg_color)
        self.Refresh()  # Refresh the button to apply changes
        event.Skip()

    def OnUnHover(self, event):
        self.SetBackgroundColour(self.bg_color)
        self.SetForegroundColour(self.fg_color)
        self.Refresh()  # Refresh the button to apply changes
        event.Skip()
