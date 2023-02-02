class Machine:
    """A vending machine class."""

    def __init__(
        self,
        id: int = 0,
        name: str = "NA",
        location: str = "NA",
        stocks: dict[str, int] = None,
    ):
        """Initialize the machine instance."""
        self.id = id
        self.name = name
        self.location = location
        self.stocks = dict()
