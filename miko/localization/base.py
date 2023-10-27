import dataclasses


@dataclasses.dataclass
class BaseLocalization:
    """The base localization class"""
    welcome: str = "Welcome to the {name} reference API!"
    """The welcome message"""
