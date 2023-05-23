"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import wx


from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from components.ui import Button, Text, NumberInput, TextBox, COLORS
from components import Canvas, FileButton, Box


class Gui(wx.Frame):
    """Configure the main window and all the widgets.

    This class provides a graphical user interface for the Logic Simulator and
    enables the user to change the circuit properties and run simulations.

    Parameters
    ----------
    title: title of the window.

    Public methods
    --------------
    on_menu(self, event): Event handler for the file menu.

    on_spin(self, event): Event handler for when the user changes the spin
                           control value.

    on_run_button(self, event): Event handler for when the user clicks the run
                                button.

    on_text_box(self, event): Event handler for when the user enters text.
    """

    def __init__(self, title, path, names, devices, network, monitors):
        """Initialise widgets and layout."""
        super().__init__(parent=None, title=title, size=(800, 600))

        self.setup_menu()
        self.SetBackgroundColour(COLORS.GRAY_950)

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = Box(self, dir="col")

        self.canvas = Canvas(right_sizer, devices, monitors)

        Heading(self).Attach(left_sizer, 0, wx.EXPAND, 5)

        DevicesPanel(self, canvas=self.canvas).Attach(
            left_sizer, 3, wx.EXPAND | wx.ALL, 5)

        right_sizer.Add(self.canvas,
                        3, wx.EXPAND | wx.ALL, 5)

        right_bottom_block = Box(
            right_sizer, dir="row")

        right_bottom_left = Box(
            right_bottom_block, dir="col", bg_color=COLORS.GRAY_800)

        right_bottom_left.Add(
            Text(right_bottom_left, "Switches"), 1, wx.ALL, 5)

        right_bottom_right = Box(
            right_bottom_block, dir="col", bg_color=COLORS.GRAY_800)
        right_bottom_right.Add(
            Text(right_bottom_right, "Cycles"), 1, wx.ALL, 5)

        right_bottom_block.Add(right_bottom_left, 1, wx.EXPAND | wx.ALL, 5)
        right_bottom_block.Add(right_bottom_right, 1, wx.EXPAND | wx.ALL, 5)

        right_sizer.Add(right_bottom_block, 2, wx.EXPAND, 5)

        main_sizer.Add(left_sizer, 2, wx.ALL, 5)
        main_sizer.Add(right_sizer, 5, wx.EXPAND | wx.ALL, 5)

        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

    def setup_menu(self):
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_ABOUT, "&About")
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.on_menu)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)
        if Id == wx.ID_ABOUT:
            wx.MessageBox("Logic Simulator\nCreated by Mojisola Agboola\n2017",
                          "About Logsim", wx.ICON_INFORMATION | wx.OK)


class Heading(wx.BoxSizer):
    def __init__(self, parent):
        """Initialise the heading."""
        super().__init__(wx.HORIZONTAL)
        self.Add(
            Button(parent, "Logic Simulator", size="md",
                   bg_color=COLORS.RED_800, hover_bg_color=COLORS.RED_700,
                   ), 1, wx.ALL, 5)

        self.Add(FileButton(parent), 1, wx.ALL, 5)

    def Attach(self, parent: wx.BoxSizer, proportion, flag, border):
        """Attach the heading to the parent."""
        parent.Add(self, proportion, flag, border)


class DevicesPanel(Box):
    def __init__(self, parent, canvas):
        """Initialise the devices panel."""
        super().__init__(parent, dir="col")

        self.canvas = canvas

        self.Add(Text(self, "Devices"), 1, wx.ALL, 5)
        self.Add(NumberInput(
            self, value=10, onChange=self.on_spin), 1, wx.ALL, 5)
        self.Add(Button(self, "Run",
                        onClick=self.on_run_button), 1, wx.ALL, 5)
        self.Add(TextBox(self, "Enter text",
                         onChange=self.on_text_box), 1, wx.ALL, 5)

    def Attach(self, parent: wx.BoxSizer, proportion, flag, border):
        """Attach the heading to the parent."""
        parent.Add(self, proportion, flag, border)

    def on_spin(self, event):
        """Handle the event when the user changes the spin control value."""
        # Get the spin control value from the event object
        spin_value = event.GetInt()
        text = "".join(["New spin control value: ", str(spin_value)])
        self.canvas.render(text)

    def on_run_button(self, event):
        """Handle the event when the user clicks the run button."""
        text = "Run button pressed."
        self.canvas.render(text)

    def on_text_box(self, event):
        """Handle the event when the user enters text."""
        # Get the text box value from the event object
        text_box_value = event.GetString()
        text = "".join(["New text box value: ", text_box_value])
        self.canvas.render(text)
