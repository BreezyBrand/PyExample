from time import sleep
import flet as ft


def main(page: ft.Page):

    svg_content = """
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
 <g>
  <ellipse ry="{}" rx="{}" id="svg_1" cy="200" cx="200" stroke="#000" fill="#fff"/>
 </g>
</svg>
"""
    img = ft.Image(src=svg_content.format(0, 0))
    page.add(img)

    for c in range(0, 10):
        for i in range(0, 10):
            img.src = svg_content.format(i * 10, i * 10)
            img.update()
            sleep(0.1)


ft.app(target=main)
