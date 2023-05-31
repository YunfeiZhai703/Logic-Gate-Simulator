import random
import wx.glcanvas as wxcanvas
from OpenGL import GL, GLUT
import wx
import math

from devices import Devices
from monitors import Monitors


glColors = [
    (1.0, 0.0, 0.0),  # red
    (0.0, 1.0, 0.0),  # green
    (0.0, 0.0, 1.0),  # blue
    (1.0, 1.0, 0.0),  # yellow
    (1.0, 0.0, 1.0),  # magenta
    (0.0, 1.0, 1.0),  # cyan
    (0.5, 0.5, 0.5),  # grey
    (1.0, 0.5, 0.0),  # orange
    (0.0, 0.5, 0.0),  # dark green
    (0.5, 0.0, 0.5),  # purple
    (0.5, 0.0, 0.0),  # dark red
    (0.0, 0.0, 0.5),  # dark blue
    (0.0, 0.5, 0.5),  # dark cyan
    (0.5, 0.5, 0.0),  # dark yellow
    (0.5, 0.0, 0.0),  # dark red

]


class Canvas(wxcanvas.GLCanvas):
    """Handle all drawing operations.

    This class contains functions for drawing onto the canvas. It
    also contains handlers for events relating to the canvas.

    Parameters
    ----------
    parent: parent window.
    devices: instance of the devices.Devices() class.
    monitors: instance of the monitors.Monitors() class.

    Public methods
    --------------
    init_gl(self): Configures the OpenGL context.

    render(self, text): Handles all drawing operations.

    on_paint(self, event): Handles the paint event.

    on_size(self, event): Handles the canvas resize event.

    on_mouse(self, event): Handles mouse events.

    render_text(self, text, x_pos, y_pos): Handles text drawing
                                           operations.

    reset(self): Resets the canvas to its default state.

    remove_signal(self, label): Removes a signal from the canvas with label

    draw_signal_trace(self, signal, x_pos, y_pos, start_time, color): Draws a signal trace
                                                                      (see function for more details)
    add_signal(self, signal): Adds a signal to the canvas
    """

    def __init__(self, parent, devices: Devices, monitors: Monitors):
        """Initialise canvas properties and useful variables."""
        super().__init__(parent, -1,
                         attribList=[wxcanvas.WX_GL_RGBA,
                                     wxcanvas.WX_GL_DOUBLEBUFFER,
                                     wxcanvas.WX_GL_DEPTH_SIZE, 16, 0])
        GLUT.glutInit()
        self.init = False
        self.context = wxcanvas.GLContext(self)
        self.colors = glColors
        self.monitors = monitors
        self.devices = devices

        # Initialise variables for panning
        self.pan_x = 0
        self.pan_y = 0
        self.last_mouse_x = 0  # previous mouse x position
        self.last_mouse_y = 0  # previous mouse y position

        # Initialise variables for zooming
        self.zoom = 1

        self.signals = []

        # Bind events to the canvas
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_MOUSE_EVENTS, self.on_mouse)

    def init_gl(self):
        """Configure and initialise the OpenGL context."""
        size = self.GetClientSize()
        self.SetCurrent(self.context)
        GL.glDrawBuffer(GL.GL_BACK)
        self.set_bg_color()
        GL.glViewport(0, 0, size.width, size.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho(0, size.width, 0, size.height, -1, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glTranslated(self.pan_x, self.pan_y, 0.0)
        GL.glScaled(self.zoom, self.zoom, self.zoom)

    def reset(self):
        """Reset the canvas."""
        self.signals = []
        self.monitors.reset_monitors()

    def remove_signal(self, label):
        """Remove a signal from the canvas with label."""
        for signal in self.signals:
            if signal["name"] == label:
                self.signals.remove(signal)
                break

    def draw_signal_trace(
        self,
        signal: list,
        x_pos: int,
        y_pos: int,
        label: str,
        start_time: int,
        color: tuple = (
            0.0,
            0.0,
            1.0)):
        """Draw a signal trace.

        Args:
            signal (list): Signal to draw.
            x_pos (int): X position to draw the signal.
            y_pos (int): Y position to draw the signal.
            label (str): Label of the signal.
            start_time (int): Start time of the signal.
            color (tuple, optional): Color of plot. Defaults to ( 0.0, 0.0, 1.0).
        """

        GL.glColor3f(color[0], color[1], color[2])
        GL.glBegin(GL.GL_LINE_STRIP)
        for i in range(len(signal)):
            x = ((i + start_time) * 20) + x_pos
            x_next = ((i + start_time) * 20) + x_pos + 20
            if signal[i] == 0:
                y = y_pos
            else:
                y = y_pos + 25
            GL.glVertex2f(x, y)
            GL.glVertex2f(x_next, y)
        GL.glEnd()

        # Draw axis
        y_pos -= 10
        self.set_graph_color()
        GL.glBegin(GL.GL_LINES)
        GL.glVertex2f(x_pos, y_pos)
        GL.glVertex2f(x_pos, y_pos + 40)
        GL.glVertex2f(x_pos, y_pos)
        GL.glVertex2f(x_pos + ((len(signal) + start_time) * 20), y_pos)
        GL.glEnd()
        # draw axis ticks
        for i in range(len(signal) + start_time + 1):
            x = (i * 20) + x_pos
            self.set_graph_color()
            GL.glBegin(GL.GL_LINES)
            GL.glVertex2f(x, y_pos)
            GL.glVertex2f(x, y_pos - 4)
            GL.glEnd()
            self.render_text(str(i), x - 5, y_pos - 15)

        x_pos -= int(40 / 3 * len(label))
        self.render_text(label, x_pos, y_pos + 18)

    def add_signal(self, signal: list, label: str, start_time: int = 0):
        """Add a signal to the canvas.

        Args:
            signal (list): A list of 1 and 0s
            label (str): The label of the signal
            start_time (int, optional): The start time of the signal. Defaults to 0.
        """
        if label in [s["name"] for s in self.signals]:
            # edit existing signal
            for s in self.signals:
                if s["name"] == label:
                    s["signal"] = signal
        else:
            self.signals.append(
                {"name": label, "signal": signal, "start_time": start_time})

    def _get_color(self, index):
        """Get a color from the color list. If the index is out of range, a new color is generated."""
        if index < len(self.colors):
            return self.colors[index]
        else:
            random_color = (random.random(), random.random(), random.random())
            self.colors.append(random_color)
            return random_color

    def render(self, text):
        """Handle all drawing operations."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        # Clear everything
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

        # Draw specified text at position (10, 10)
        # self.render_text(text, 10, 10)

        for i, signal in enumerate(self.signals):
            self.draw_signal_trace(
                signal["signal"],
                50,
                60 * i + 50,
                signal["name"],
                signal["start_time"],
                self._get_color(i))

        # We have been drawing to the back buffer, flush the graphics pipeline
        # and swap the back buffer to the front
        GL.glFlush()
        self.SwapBuffers()

    def on_paint(self, event):
        """Handle the paint event."""
        self.SetCurrent(self.context)
        if not self.init:
            # Configure the viewport, modelview and projection matrices
            self.init_gl()
            self.init = True

        size = self.GetClientSize()
        text = "".join(["Canvas redrawn on paint event, size is ",
                        str(size.width), ", ", str(size.height)])
        self.render(text)

    def on_size(self, event):
        """Handle the canvas resize event."""
        # Forces reconfiguration of the viewport, modelview and projection
        # matrices on the next paint event
        self.init = False

    def on_mouse(self, event):
        """Handle mouse events."""
        text = ""
        # Calculate object coordinates of the mouse position
        size = self.GetClientSize()
        ox = (event.GetX() - self.pan_x) / self.zoom
        oy = (size.height - event.GetY() - self.pan_y) / self.zoom
        old_zoom = self.zoom
        if event.ButtonDown():
            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            text = "".join(["Mouse button pressed at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.ButtonUp():
            text = "".join(["Mouse button released at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Leaving():
            text = "".join(["Mouse left canvas at: ", str(event.GetX()),
                            ", ", str(event.GetY())])
        if event.Dragging():
            self.pan_x += event.GetX() - self.last_mouse_x
            self.pan_y -= event.GetY() - self.last_mouse_y
            # prevent panning outside the canvas
            # self.pan_x = max(self.pan_x, 0)
            # self.pan_y = max(self.pan_y, 0)
            # size = self.GetClientSize()
            # self.pan_x = min(self.pan_x, size.width * 0.8 - 1)
            # self.pan_y = min(self.pan_y, size.height * 0.8 - 1)
            # print(f"Size: {size.width} {size.height}")

            self.last_mouse_x = event.GetX()
            self.last_mouse_y = event.GetY()
            self.init = False
            text = "".join(["Mouse dragged to: ", str(event.GetX()),
                            ", ", str(event.GetY()), ". Pan is now: ",
                            str(self.pan_x), ", ", str(self.pan_y)])
        if event.GetWheelRotation() < 0:
            self.zoom *= (1.0 + (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Negative mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if event.GetWheelRotation() > 0:
            self.zoom /= (1.0 - (
                event.GetWheelRotation() / (20 * event.GetWheelDelta())))
            # Adjust pan so as to zoom around the mouse position
            self.pan_x -= (self.zoom - old_zoom) * ox
            self.pan_y -= (self.zoom - old_zoom) * oy
            self.init = False
            text = "".join(["Positive mouse wheel rotation. Zoom is now: ",
                            str(self.zoom)])
        if text:
            self.render(text)
        else:
            self.Refresh()  # triggers the paint event

    def render_text(self, text, x_pos, y_pos):
        """Handle text drawing operations."""
        self.set_graph_color()
        GL.glRasterPos2f(x_pos, y_pos)
        font = GLUT.GLUT_BITMAP_HELVETICA_12  # type: ignore

        for character in text:
            if character == '\n':
                y_pos = y_pos - 20
                GL.glRasterPos2f(x_pos, y_pos)
            else:
                GLUT.glutBitmapCharacter(font, ord(character))

    def set_bg_color(self):
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)

    def set_graph_color(self):
        GL.glColor3f(0.8, 0.8, 0.8)
