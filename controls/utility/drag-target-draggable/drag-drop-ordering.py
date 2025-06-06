import logging
import flet as ft

# logging.basicConfig(level=logging.INFO)
# print("flet version: ", flet.version.version)


class ItemList(ft.Draggable):

    def __init__(self, page: ft.Page, list_row, list_name, color):
        self.page: ft.Page = page
        self.list_row = list_row
        self.list_name: str = list_name
        self.list_color = color
        self.items = ft.Column([], tight=True, spacing=5)
        self.end_indicator = ft.Container(
            bgcolor=ft.Colors.BLACK26,
            border_radius=ft.border_radius.all(30),
            height=3,
            width=200,
            opacity=0.0,
        )
        self.item_name = ft.TextField(
            label="New Item Name",
            width=200,
            height=50,
            bgcolor=ft.Colors.WHITE,
            on_submit=self.add_item_handler,
        )
        self.target = ft.DragTarget(
            group="items",
            content=ft.DragTarget(
                group="lists",
                content=ft.Container(
                    content=ft.Column(
                        [
                            self.item_name,
                            ft.TextButton(
                                "Add Item",
                                icon=ft.icons.ADD,
                                on_click=self.add_item_handler,
                            ),
                            self.items,
                            self.end_indicator,
                        ],
                        spacing=4,
                        tight=True,
                        expand=True,
                    ),
                    border=ft.border.all(2, ft.Colors.BLACK12),
                    border_radius=ft.border_radius.all(15),
                    bgcolor=self.list_color,
                    padding=ft.padding.all(20),
                ),
                data=self,
                on_accept=self.drag_accept,
                on_will_accept=self.drag_will_accept,
                on_leave=self.drag_leave,
            ),
            data=self,
            on_accept=self.item_drag_accept,
            on_will_accept=self.item_drag_will_accept,
            on_leave=self.item_drag_leave,
        )
        super().__init__(group="lists", content=self.target, data=self)

    def add_item_handler(self, e):
        self.add_item()

    def add_item(
        self,
        item: str = None,
        chosen_control: ft.Draggable = None,
        swap_control: ft.Draggable = None,
    ):

        controls_list = [x.controls[1] for x in self.items.controls]
        to_index = (
            controls_list.index(swap_control) if swap_control in controls_list else None
        )
        from_index = (
            controls_list.index(chosen_control)
            if chosen_control in controls_list
            else None
        )
        control_to_add = ft.Column(
            [
                ft.Container(
                    bgcolor=ft.Colors.BLACK26,
                    border_radius=ft.border_radius.all(30),
                    height=3,
                    alignment=ft.alignment.center_right,
                    width=200,
                    opacity=0.0,
                )
            ]
        )

        # rearrange (i.e. drag drop from same list)
        if (from_index is not None) and (to_index is not None):
            print("rearrange: ", to_index, from_index)
            self.items.controls.insert(to_index, self.items.controls.pop(from_index))
            self.set_indicator_opacity(swap_control, 0.0)

        # insert (drag from other list to middle of this list)
        elif to_index is not None:
            print("insert: ", to_index)
            new_item = Item(self, item)
            control_to_add.controls.append(new_item)
            self.items.controls.insert(to_index, control_to_add)

        # add new (drag from other list to end of this list, or use add item button)
        else:
            print("add new: ", item)
            new_item = new_item = (
                Item(self, item) if item else Item(self, self.item_name.value)
            )
            control_to_add.controls.append(new_item)
            self.items.controls.append(control_to_add)
            self.item_name.value = ""

        print("self.items: ", self.items.controls)
        self.update()
        self.page.update()

    def set_indicator_opacity(self, item, opacity):
        controls_list = [x.controls[1] for x in self.items.controls]
        self.items.controls[controls_list.index(item)].controls[0].opacity = opacity
        self.update()

    def remove_item(self, item):
        controls_list = [x.controls[1] for x in self.items.controls]
        del self.items.controls[controls_list.index(item)]
        self.update()

    def drag_accept(self, e):
        src = self.page.get_control(e.src_id)

        l = self.list_row.current.controls
        to_index = l.index(e.control.data)
        from_index = l.index(src.content.data)
        l[to_index], l[from_index] = l[from_index], l[to_index]
        self.end_indicator.opacity = 0.0
        self.page.update()

    def drag_will_accept(self, e):
        self.end_indicator.opacity = 0.0
        self.page.update()

    def drag_leave(self, e):
        self.end_indicator.opacity = 0.0
        self.page.update()

    def item_drag_accept(self, e):
        src = self.page.get_control(e.src_id)
        self.add_item(src.data.item_text)
        src.data.list.remove_item(src)
        self.end_indicator.opacity = 0.0
        self.page.update()

    def item_drag_will_accept(self, e):
        self.end_indicator.opacity = 1.0
        self.page.update()

    def item_drag_leave(self, e):
        self.end_indicator.opacity = 0.0
        self.page.update()


class Item(ft.Draggable):

    def __init__(self, list: ItemList, item_text: str):
        self.list = list
        self.item_text = item_text
        self.card_item = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(name=ft.icons.CIRCLE_OUTLINED),
                        ft.Text(value=f"{self.item_text}"),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                width=200,
                padding=7,
            ),
            elevation=1,
            data=self.list,
        )
        self.target = ft.DragTarget(
            group="items",
            content=self.card_item,
            on_accept=self.drag_accept,
            on_leave=self.drag_leave,
            on_will_accept=self.drag_will_accept,
        )
        super().__init__(group="items", content=self.target, data=self)

    def drag_accept(self, e: ft.DragTargetEvent):
        # this is the item picked up (Draggable control)
        src = self.list.page.get_control(f"{e.src_id}")

        # e.control is the DragTarget, i.e. This (self) Item in the list
        # skip if item is dropped on itself
        if src.content.content == e.control.content:
            e.control.content.elevation = 1
            self.list.set_indicator_opacity(self, 0.0)
            e.control.update()
            return

        # item dropped within same list but not on self
        if src.data.list == self.list:
            self.list.add_item(chosen_control=src, swap_control=self)
            self.list.set_indicator_opacity(self, 0.0)
            e.control.content.elevation = 1
            e.control.update()
            return

        # item added to different list
        self.list.add_item(src.data.item_text, swap_control=self)
        # remove from the list to which draggable belongs
        src.data.list.remove_item(src)
        self.list.set_indicator_opacity(self, 0.0)
        e.control.content.elevation = 1
        e.control.update()

    def drag_will_accept(self, e):
        self.list.set_indicator_opacity(self, 1.0)
        e.control.content.elevation = 20 if e.data == "true" else 1
        e.control.update()

    def drag_leave(self, e):
        self.list.set_indicator_opacity(self, 0.0)
        e.control.content.elevation = 1
        e.control.update()


def main(page: ft.Page):

    page.title = "Drag and drop ordering"
    list_row = ft.Ref[ft.Row]()

    page.add(
        ft.Row(
            [
                ItemList(page, list_row, "List 1", ft.Colors.DEEP_ORANGE_400),
                ItemList(page, list_row, "List 2", ft.Colors.PINK_400),
                ItemList(page, list_row, "List 3", ft.Colors.CYAN_400),
            ],
            vertical_alignment=ft.CrossAxisAlignment.START,
            ref=list_row,
        )
    )
    page.update()


ft.app(target=main)
