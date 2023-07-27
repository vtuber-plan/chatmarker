import time
import flet as ft

from typing import List, TypedDict

class ChatMessage(TypedDict):
    role: str
    content: str

def ui_chat_message(message: ChatMessage):
    role = message["role"]
    content = message["content"]

    if role == "user":
        avatar = ft.CircleAvatar(
            foreground_image_url="https://avatars.githubusercontent.com/u/1551736?s=80&v=4",
            tooltip="user",
        )
    elif role == "assistant":
        avatar = ft.CircleAvatar(
            foreground_image_url="https://avatars.githubusercontent.com/u/14957082?s=48&v=4",
            tooltip="assistant",
        )
    else:
        avatar = ft.CircleAvatar(
            foreground_image_url="https://avatars.githubusercontent.com/u/1693078?s=80&v=4",
            tooltip="system",
        )
    text = ft.TextField(label="Standard", multiline=True, min_lines=1, max_lines=7, value=content, expand=True)
    chat_line = ft.Row([avatar, text])
    return chat_line

def ui_chat_view(page: ft.Page, messages: List[ChatMessage]):
    chat_view = ft.ListView(expand=True, spacing=10, auto_scroll=False, padding=5)
    for i, message in enumerate(messages):
        chat_view.controls.append(ui_chat_message(message))
    
    return chat_view

def ui_topbar(page: ft.Page):
    content = ft.Row([
        ft.ElevatedButton("Open"),
        ft.ElevatedButton("Download")
    ])
    topbar = ft.Container(
        content=content,
        bgcolor=ft.colors.YELLOW,
        padding=5,
    )
    return topbar

def ui_midarea(page: ft.Page):
    chat_view = ui_chat_view(page, messages)
    content = ft.Row([chat_view], expand=True)
    midarea = ft.Container(
        content=content,
        padding=5,
        expand=True
    )
    return midarea

def ui_bottombar(page: ft.Page):
    content = ft.Row([
        ft.ElevatedButton("Previous"),
        ft.ElevatedButton("Next")
    ])
    bottombar = ft.Container(
        content=content,
        bgcolor=ft.colors.WHITE,
        padding=0,
    )
    return bottombar

from test_data import messages

def main(page: ft.Page):
    page.title = "ChatMarker"
    page.vertical_alignment = "top"

    def page_resize(e):
        print("New page size:", page.window_width, page.window_height)

    page.on_resize = page_resize

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.PALETTE),
        leading_width=40,
        title=ft.Text("ChatMarker"),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.IconButton(ft.icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(text="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        text="Checked item", checked=False, on_click=check_item_clicked
                    ),
                ]
            ),
        ],
    )

    # file picker
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    page.update()

    # views
    mid_area = ui_midarea(page)
    bottombar = ui_bottombar(page)
    
    main_column = ft.Column([mid_area, bottombar], expand=True)
    
    page.add(main_column)

ft.app(target=main)