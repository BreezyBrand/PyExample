import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    c = ft.Column(
        [
            ft.CupertinoCheckbox(
                label="Cupertino Checkbox tristate",
                value=True,
                tristate=True,
                fill_color={
                    ft.ControlState.HOVERED: ft.Colors.PINK_200,
                    ft.ControlState.PRESSED: ft.Colors.LIME_ACCENT_200,
                    ft.ControlState.SELECTED: ft.Colors.DEEP_ORANGE_200,
                    ft.ControlState.DEFAULT: ft.Colors.TEAL_200,
                },
                check_color=ft.Colors.GREY_900,
            ),
            ft.CupertinoCheckbox(
                label="Cupertino Checkbox circle border",
                value=True,
                shape=ft.CircleBorder(),
                scale=ft.Scale(2, alignment=ft.Alignment(-1, 0)),
            ),
            ft.CupertinoCheckbox(
                label="Cupertino Checkbox border states",
                value=True,
                border_side={
                    ft.ControlState.HOVERED: ft.BorderSide(width=5, stroke_align=5),
                    ft.ControlState.DEFAULT: ft.BorderSide(width=3, stroke_align=5),
                    ft.ControlState.FOCUSED: ft.BorderSide(width=3, stroke_align=5),
                },
                # scale=ft.Scale(2, alignment=ft.Alignment(-0.9, 0)),
            ),
            ft.CupertinoCheckbox(
                label="Cupertino Checkbox label position",
                value=True,
                label_position=ft.LabelPosition.LEFT,
            ),
        ]
    )
    page.add(c)


ft.app(main)
