from enum import Enum
class ActionType(Enum):
    MOVE = "move"
    TRANSFER = "transfer"
    BUY = "buy"

class Action:
    def __init__(self, type: ActionType):
        self.type = type

class MoveAction(Action):
    def __init__(self, pos: tuple):
        super().__init__(ActionType.MOVE)

        if self._check_pos_type(pos):
            self.pos = pos
        else:
            raise ValueError(f"the pos for {self.__class__} is invalid: {pos}")

    def _check_pos_type(self, pos: tuple):
        return isinstance(pos, tuple) and list(map(type, pos)) == [int, int]

class TranferAction(Action):
    def __init__(self, level: int):
        super().__init__(ActionType.TRANSFER)
        self.level = level

class BuyAction(Action):
    def __init__(self):
        super().__init__(ActionType.BUY)
