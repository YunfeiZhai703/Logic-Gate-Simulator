"""
Class for button widget using wxPython
"""

import wx
from wx.lib.agw.gradientbutton import GradientButton
from .colors import COLORS
from typing import Tuple, Union

button_size_type = Union[str, Tuple[int, int], None]

# str: xs, sm, md, lg, xl (removed Literal due to python 3.7 compatibility)


class Button(GradientButton):
    """Button widget class."""

    def __init__(self, parent, label, onClick=None, color=wx.BLACK,
                 size: button_size_type = None
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
        self.SetBaseColours(color, wx.WHITE)

        if onClick:
            self.Bind(wx.EVT_BUTTON, onClick)

        if size:
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

    def SetColor(self, color):
        """Set the color of the button."""
        self.SetBaseColours(color, wx.WHITE)

    def SetBaseColours(self, startcolour=wx.BLACK, foregroundcolour=wx.WHITE):
        """Set the base colors of the button."""
        self.SetForegroundColour(foregroundcolour)

        self._bottomEndColour = startcolour
        self._bottomStartColour = startcolour
        self._topEndColour = startcolour
        self._topStartColour = startcolour

        self._pressedBottomColour = startcolour
        self._pressedTopColour = startcolour

        # self.SetBackgroundColour(startcolour)

    # def OnHover(self, event):
    #     self.SetBackgroundColour(self.hover_bg_color)
    #     self.SetForegroundColour(self.hover_fg_color)
    #     self.Refresh()  # Refresh the button to apply changes
    #     event.Skip()

    # def OnUnHover(self, event):
    #     self.SetBackgroundColour(self.bg_color)
    #     self.SetForegroundColour(self.fg_color)
    #     self.Refresh()  # Refresh the button to apply changes
    #     event.Skip()
