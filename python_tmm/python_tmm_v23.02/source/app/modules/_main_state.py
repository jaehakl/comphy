from lib.state import AbstractState

class MainState(AbstractState):
    def __init__(self):
        super().__init__()
        #본 프로그램에서 Widget과 Component 들이 공유할 데이터 등록
        self.use("status",["Ready"])

