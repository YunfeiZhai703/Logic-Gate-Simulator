"""Implement the graphical user interface for the Logic Simulator.

Used in the Logic Simulator project to enable the user to run the simulation
or adjust the network properties.

Classes:
--------
MyGLCanvas - handles all canvas drawing operations.
Gui - configures the main window and all the widgets.
"""
import random
import wx


from names import Names
from devices import Devices
from network import Network
from monitors import Monitors
from scanner import Scanner
from parse import Parser
from components.ui import Button, Text, NumberInput, TextBox, COLORS
from components import Canvas, FileButton, Box, ScrollBox


class Gui(wx.Frame):
    # notebook

    def __init__(self, title, path, names, devices, network, monitors):
        super().__init__(parent=None, title=title, size=(800, 600))

        nb = wx.Notebook(self, style=wx.NB_FIXEDWIDTH)
        self.nb = nb
        nb.SetBackgroundColour(COLORS.GRAY_400)
        nb.canvas = Canvas(nb, devices, monitors)
        nb.uploaded_code = self._read_file(path)
        nb.AddPage(MainPage("Logic Simulator", path, names, devices,
                   network, monitors, notebook=nb), "Main")

        nb.AddPage(nb.canvas, "Graphs")
        nb.AddPage(CodePage(nb), "Code")
        nb.AddPage(Button(nb, label="Save", onClick=self.print_code), "Test")
        self.setup_menu()

        self.Show()

    def _read_file(self, path):
        """Read the file specified by path."""
        try:
            with open(path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return "No Code Uploded"

    def setup_menu(self):
        fileMenu = wx.Menu()
        menuBar = wx.MenuBar()
        fileMenu.Append(wx.ID_EXIT, "&Exit")
        menuBar.Append(fileMenu, "&File")
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.on_menu)

    def print_code(self, event):
        print(self.nb.uploaded_code)

    def on_menu(self, event):
        """Handle the event when the user selects a menu item."""
        Id = event.GetId()
        if Id == wx.ID_EXIT:
            self.Close(True)


class MainPage(wx.Panel):

    def __init__(self, title, path, names, devices, network, monitors, notebook=None):
        """Initialise widgets and layout."""
        super().__init__(parent=notebook)

        self.SetBackgroundColour(COLORS.GRAY_950)
        self.number_of_cycles = 10

        # Configure sizers for layout
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer = Box(self, dir="col")

        self.canvas = Canvas(right_sizer, devices, monitors)
        self.canvas2 = notebook.canvas

        Heading(self, notebook).Attach(left_sizer, 0, wx.EXPAND, 5)

        DevicesPanel(self, canvas=self.canvas).Attach(
            left_sizer, 3, wx.EXPAND | wx.ALL, 5)

        right_sizer.Add(self.canvas,
                        3, wx.EXPAND | wx.ALL, 5)

        right_bottom_block = Box(
            right_sizer, dir="row")

        right_bottom_left = Box(
            right_bottom_block, dir="col", bg_color=COLORS.GRAY_800)

        right_bottom_left.Add(
            Text(right_bottom_left, "Switches"), 0, wx.ALL, 5)

        right_bottom_block.Add(right_bottom_left, 1, wx.EXPAND | wx.ALL, 5)

        right_sizer.Add(right_bottom_block, 1, wx.EXPAND, 5)

        ConfigurationPanel(right_bottom_block, self.on_start, self.on_number_input).Attach(
            right_bottom_block, 1, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(left_sizer, 2, wx.ALL, 5)
        main_sizer.Add(right_sizer, 5, wx.EXPAND | wx.ALL, 5)

        self.SetSizeHints(600, 600)
        self.SetSizer(main_sizer)

    def on_start(self, event):
        # randomly generate a signal of 1 and 0 length 10
        random_signal = [random.randint(0, 1)
                         for i in range(self.number_of_cycles)]
        print(random_signal)
        self.canvas.add_signal(
            random_signal, "A" + str(len(self.canvas.signals))
        )
        self.canvas2.add_signal(
            random_signal, "A" + str(len(self.canvas.signals))
        )
        self.canvas.Refresh()

    def on_number_input(self, event):
        """Handle the event when the user changes the spin control value."""
        self.number_of_cycles = event.GetInt()


class Heading(wx.BoxSizer):
    def __init__(self, parent, notebook: wx.Notebook):
        """Initialise the heading."""
        super().__init__(wx.HORIZONTAL)

        self.Add(
            Button(parent, "Logic Simulator", size="md",
                   bg_color=COLORS.RED_800, hover_bg_color=COLORS.RED_700,
                   onClick=self.on_click
                   ), 1, wx.ALL, 5)

        self.Add(FileButton(parent, notebook), 1, wx.ALL, 5)

    def Attach(self, parent: wx.BoxSizer, proportion, flag, border):
        """Attach the heading to the parent."""
        parent.Add(self, proportion, flag, border)

    def on_click(self, event):
        wx.MessageBox("Logic Simulator\nTeam 19 - Lakee, Dhillon, Yunfei\n2023",
                      "About Logsim", wx.ICON_INFORMATION | wx.OK)


class DevicesPanel(Box):
    def __init__(self, parent, canvas):
        """Initialise the devices panel."""
        super().__init__(parent, dir="col")
        self.parent = parent
        self.canvas = canvas

        self.Add(Text(self, "Devices"), 1, wx.ALL, 5)


class ConfigurationPanel(Box):
    def __init__(self, parent, on_start, on_number_input):
        """Initialise the devices panel."""
        super().__init__(parent, dir="col", bg_color=COLORS.GRAY_800)
        self.parent = parent

        self.Add(Text(self, "Configuration"), 0, wx.ALL, 5)

        cycles_input = Box(self, dir="row")
        cycles_input.Add(Text(cycles_input, "Number of Cycles",
                         style=wx.ALIGN_LEFT), 2, wx.ALL, 8)

        cycles_input.Add(NumberInput(
            cycles_input, value=10, onChange=on_number_input), 2, wx.ALL, 5)

        self.Add(cycles_input, 0, wx.CENTER, 10)

        self.Add(Button(self, "Start Simulation",
                        onClick=on_start,
                        bg_color=COLORS.GREEN_800,
                        hover_bg_color=COLORS.GREEN_700,
                        size="md"), 0, wx.ALL, 20)


class CodePage(ScrollBox):
    def __init__(self, parent: wx.Notebook):
        super().__init__(parent, dir="col")
        self.parent = parent
        self.code = parent.uploaded_code

        self.Add(Text(self, self.code, style=wx.ALIGN_LEFT,
                 font_family="modern"), 0, wx.ALL, 5)

        # update the text when the parent's uploaded code changes
        parent.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_page_changed)

    def on_page_changed(self, event):
        """Handle the event when the user changes the page."""
        self.code = self.parent.uploaded_code
        self.GetChildren()[0].SetLabel(self.code)
