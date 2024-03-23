from flet import (
    Page,
    RouteChangeEvent,
    View,
    AppBar,
    Text,
    ElevatedButton,
    MainAxisAlignment,
    CrossAxisAlignment,
    ViewPopEvent
)
from .pages.home import Home


def app(page: Page) -> None:
    page.title = "Flet App"

    def route_change(e: RouteChangeEvent) -> None:
        page.views.clear()

        if page.route == "/":
            home_view = Home(page)
            page.views.append(
                View(
                    route="/",
                    controls=[
                        AppBar(title=Text("Home")),
                        home_view,
                        ElevatedButton(text="Go to store", on_click=lambda _: page.go("/store"))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )
        elif page.route == "/store":
            page.views.append(
                View(
                    route="/store",
                    controls=[
                        AppBar(title=Text("Store")),
                        Text("Welcome to the store!"),
                        ElevatedButton(text="Go home", on_click=lambda _: page.go("/"))
                    ],
                    vertical_alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=26
                )
            )
        page.update()

    def view_pop(e: ViewPopEvent) -> None:
        page.views.pop()
        top_view: View = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
