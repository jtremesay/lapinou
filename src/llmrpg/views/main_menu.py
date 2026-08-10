# llmrpg - An agentic rpg game
# Copyright (C) 2026 Jonathan Tremesaygues
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from arcade import SpriteCircle, SpriteList
from arcade.gui import UIBoxLayout, UIButtonRow, UILabel, UIView

from llmrpg.ui.wood_frame import WoodFrameColor, WoodFramePattern, wood_frame_texture


class MainMenuView(UIView):
    def __init__(self) -> None:
        super().__init__()
        root = self.ui.add(UIBoxLayout(vertical=False, space_between=10))

        root.add(
            UILabel(
                text="Main Menu 2",
                font_size=24,
                text_color=(0, 255, 0),
            )
            .with_background(
                texture=wood_frame_texture(WoodFrameColor.LIGHT, WoodFramePattern.PLAIN)
            )
            .with_padding(top=16, right=16, bottom=16, left=16),
        )

        row = UIButtonRow()
        row.add_button("Start Game")
        row.add_button("Load Game")
        row.add_button("Settings")

        root.add(
            UIBoxLayout(
                children=[
                    UILabel(
                        text="Main Menu 4",
                        font_size=24,
                        text_color=(0, 0, 255),
                    ),
                    UILabel(
                        text="Main Menu 5",
                        font_size=24,
                        text_color=(255, 0, 255),
                    ),
                    row,
                ],
                space_between=10,
            )
            .with_background(
                texture=wood_frame_texture(
                    WoodFrameColor.MEDIUM, WoodFramePattern.NAILED
                )
            )
            .with_padding(top=16, right=16, bottom=16, left=16),
        )

        self.sprite_list = SpriteList()
        self.sprite_list.append(
            SpriteCircle(
                radius=50,
                color=(255, 0, 0, 255),
                center_x=self.center_x,
                center_y=self.center_y,
            )
        )

    def on_draw_before_ui(self):
        self.sprite_list.draw()
