from typing import List, Tuple

class Strategy:
    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Strategy.registry[cls.__name__] = cls

    def __init__(self, name: str) -> None:
        self.name: str = name

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        raise NotImplementedError("This method should be implemented by subclasses")

class ALLC(Strategy):
    def __init__(self) -> None:
        super().__init__("ALLC")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        return 'C'

class ALLD(Strategy):
    def __init__(self) -> None:
        super().__init__("ALLD")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        return 'D'

class TFT(Strategy):
    def __init__(self) -> None:
        super().__init__("TFT")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        if not previous_actions:
            return 'C'
        return previous_actions[-1][1]

class TTT(Strategy):
    def __init__(self) -> None:
        super().__init__("TTT")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        if len(previous_actions) < 2:
            return 'C'

        if previous_actions[-1][1] == 'D' and previous_actions[-2][1] == 'D':
            return 'D'

        return 'C'