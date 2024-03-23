from typing import List

import flet as ft

from config.settings import settings
from services.offer_service import OfferService
from config.database import get_db


STATUS_OPTIONS = [
    "NEW",
    "APPLICATION_SENT",
    "REJECTED",
    "IN_PROGRESS",
    "APPROVED"
]


def get_options() -> List[ft.dropdown.Option]:
    result = []
    for status in STATUS_OPTIONS:
        result.append(ft.dropdown.Option(status))
    return result


def app(page: ft.Page) -> None:
    page.title = settings.TITLE

    session = next(get_db())
    offer_service = OfferService(session)

    offers = offer_service.get_offers()
    options = get_options()
    lv = ft.ListView(expand=1, spacing=10, padding=20)

    for offer in offers:

        lv.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Checkbox(value=offer.archived, on_change=offer_service.update_archive(offer.id))
                    ),
                    ft.Container(
                        content=ft.Text(offer.title),
                    ),
                    ft.Container(
                        content=ft.Dropdown(
                            width=150,
                            hint_text=offer.status,
                            options=options
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(str(offer.created_at)),
                    )
                ]
            )
        )
    page.add(lv)
