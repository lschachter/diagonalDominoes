from graphics import Point, Rectangle, Text, GraphWin


class InfoBox:
    """ """

    def __init__(
        self,
        window: GraphWin,
        center: Point,
        width: int,
        height: int,
        label: str,
        color: str = "white",
        textColor: str = "black",
        size: int = None,
    ) -> None:
        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.color = color
        self.lColor = textColor
        self.rect = Rectangle(p1, p2)
        self.rect.setFill(self.color)
        self.rect.draw(window)
        self.label = Text(center, label)
        self.label.setFill(self.lColor)
        self.label.draw(window)
        self.window = window

        if size:
            self.label.setSize(size)

    def delete(self) -> None:
        self.label.undraw()
        self.rect.undraw()


class Button(InfoBox):
    """A button is a labeled rectangle in a window.
    It is enabled or disabled with the activate()
    and deactivate() methods. The isClicked(pt) method
    returns true if the button is enabled and pt is inside it."""

    def __init__(
        self,
        window: GraphWin,
        center: Point,
        width: int,
        height: int,
        label: str,
        color: str = "white",
        textColor: str = "black",
        inverse: bool = False,
    ) -> None:
        """Creates a rectangular button, eg:
        qb = Button(myWin, centerPoint, width, height, "black", 'Quit')
        """
        super().__init__(
            window,
            center,
            width,
            height,
            label,
            color=color,
            textColor=textColor,
        )

        if inverse:
            # Shortcut to have black buttons with white labels
            self.color = textColor
            self.lColor = color
            self.rect.setFill(self.color)
            self.label.setFill(self.lColor)

        self.active = True

    def isClicked(self, pt: Point) -> bool:
        "Returns true if button active and pt is inside"
        return (
            self.active
            and self.xmin <= pt.getX() <= self.xmax
            and self.ymin <= pt.getY() <= self.ymax
        )

    def activate(self) -> None:
        "Sets this button to 'active'."
        self.rect.setOutline("black")
        self.active = True

    def choose(self) -> None:
        """Alters the look of the button to show it's been selected"""
        self.rect.setFill("DarkGray")
        self.rect.setWidth(2)

    def unchoose(self) -> None:
        """Resets the look of the button once another has been chosen"""
        self.label.setFill(self.lColor)
        self.rect.setFill(self.color)
        self.rect.setWidth(1)

    def deactivate(self) -> None:
        "Sets this button to 'inactive'."
        self.rect.setOutline(self.color)
        self.active = False

    def setTextSize(self, size: int) -> None:
        """Sets the size and face of the label"""
        self.label.setSize(size)

    def offSet(self, x: int, y: int) -> None:
        """Offsets the label from the button"""
        self.label.move(x, y)

    def die(self) -> None:
        """Effectively deletes the button"""
        self.active = False
        super().delete()


class WinButton(Button):
    def __init__(self, window: "GraphWin", playerName: str) -> None:
        """Winner button"""
        super().__init__(
            window,
            Point(window.getWidth() / 2, window.getHeight() / 2),
            200,
            100,
            f"Player {playerName} wins!",
        )
