# Lapinou - An agentic game engine
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

from typing import cast

from arcade.gui import (
    UIAnchorLayout,
    UIBoxLayout,
    UIButtonRow,
    UIFlatButton,
    UILabel,
    UIView,
)

from lapinou.models.settings import Settings
from lapinou.ui.wood_frame import with_wood_frame_background

# from llmrpg.ui.wood_frame import WoodFrameColor, WoodFramePattern, wood_frame_texture


class MainMenuView(UIView):
    def __init__(self, settings: Settings | None = None) -> None:
        super().__init__()
        root = self.ui.add(UIAnchorLayout(space_between=10))

        box = root.add(
            with_wood_frame_background(UIBoxLayout(vertical=True, space_between=10))
        )
        box.add(
            UILabel(
                text="Lapinou\nAn agentic game engine",
                multiline=True,
                font_size=24,
                text_color=(0, 0, 255),
                align="center",
            )
        )

        button_row = box.add(UIButtonRow())
        start_game_button = cast(UIFlatButton, button_row.add_button("Start Game"))
        load_game_button = cast(UIFlatButton, button_row.add_button("Load Game"))
        load_game_button.disabled = True  # TODO: Implement load game functionality
        settings_button = cast(UIFlatButton, button_row.add_button("Settings"))
        quit_button = cast(UIFlatButton, button_row.add_button("Quit"))

        @settings_button.event("on_click")
        def on_settings_button_click(event):
            from .settings import SettingsView

            self.window.show_view(SettingsView(settings=settings))

        @quit_button.event("on_click")
        def on_quit_button_click(event):
            self.window.close()
