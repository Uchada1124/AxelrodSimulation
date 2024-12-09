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
    
class PVL(Strategy):
    '''
    Pavlov戦略の考察
    ALLDを対戦したとき, ('C', 'D'): 'D'と('D', 'D'): 'C'を繰り返すからALLDには弱そう. 
    TFT, ALLD, ALLC, PVLでの戦いで, 想像よりも人口が伸びない. 
    ランダムとかもっと多くの戦略タイプと戦った時でないと真価は発揮しないと予想する. 
    '''
    def __init__(self) -> None:
        super().__init__("PVL")

    def choose_action(self, previous_actions: List[Tuple[str, str]]) -> str:
        if not previous_actions:
            return 'C'

        return_action = {
            ('C', 'C'): 'C',
            ('C', 'D'): 'D',
            ('D', 'C'): 'D',
            ('D', 'D'): 'C'
        }

        return return_action[previous_actions[-1]]
