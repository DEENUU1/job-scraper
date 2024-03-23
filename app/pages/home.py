from flet import (
    UserControl,
    Column,
    AppBar,
    ElevatedButton,
    Text
)


class Home(UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        return Column(
            controls=[
                Text("Test!"),
            ],
        )
