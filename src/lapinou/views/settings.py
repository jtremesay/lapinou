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

import textwrap
from pathlib import Path

from arcade.gui import (
    UIAnchorLayout,
    UIBoxLayout,
    UIButtonRow,
    UIFlatButton,
    UIInputText,
    UILabel,
    UIManager,
    UIMessageBox,
    UIView,
)
from arcade.gui.experimental import UIPasswordInput

from lapinou.models.settings import Settings
from lapinou.ui.wood_frame import with_wood_frame_background


class SettingsView(UIView):
    def __init__(self, settings: Settings | None = None) -> None:
        super().__init__()
        self.settings = settings

        root = self.ui.add(UIAnchorLayout())
        root.add(
            UILabel(
                text="Settings",
                font_size=32,
                text_color=(255, 255, 255),
                align="center",
            ),
            anchor_y="top",
            align_y=-50,
        )

        body = root.add(with_wood_frame_background(UIBoxLayout(vertical=True)))

        row1 = body.add(UIBoxLayout(vertical=False, space_between=10))
        row1.add(
            UILabel(
                text="LLM Model", font_size=24, text_color=(0, 0, 255), align="left"
            )
        )
        llm_model_input = row1.add(UIInputText(width=200))
        if settings:
            llm_model_input.text = settings.llm_model

        row4 = body.add(UIBoxLayout(vertical=False, space_between=10))
        row4.add(
            UILabel(
                text="Google API Key",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        google_api_key_input = row4.add(UIPasswordInput(width=200))
        if settings:
            google_api_key_input.text = settings.google_api_key or ""

        row2 = body.add(UIBoxLayout(vertical=False, space_between=10))
        row2.add(
            UILabel(
                text="Ollama URL", font_size=24, text_color=(0, 0, 255), align="left"
            )
        )
        ollama_url_input = row2.add(UIInputText(width=200))
        if settings:
            ollama_url_input.text = settings.ollama_url or ""

        row3 = body.add(UIBoxLayout(vertical=False, space_between=10))
        row3.add(
            UILabel(
                text="Ollama API Key",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        ollama_api_key_input = row3.add(UIPasswordInput(width=200))
        if settings:
            ollama_api_key_input.text = settings.ollama_api_key or ""

        button_row = root.add(
            UIButtonRow(spacing=10, align="center"), anchor_y="bottom", align_y=50
        )

        save_button = button_row.add(
            UIFlatButton(text="Save", width=100, height=40),
        )
        main_menu_button = button_row.add(
            UIFlatButton(text="Main Menu", width=100, height=40),
        )

        @save_button.event("on_click")
        def on_save_button_click(event):
            new_settings = Settings(
                llm_model=llm_model_input.text,
                google_api_key=google_api_key_input.text or None,
                ollama_url=ollama_url_input.text or None,
                ollama_api_key=ollama_api_key_input.text or None,
            )
            new_settings.save_to_file(Path("settings.json"))
            self.settings = new_settings
            self.ui.add(
                UIMessageBox(
                    width=500,
                    height=350,
                    title="Settings Saved",
                    buttons=("Ok",),
                    message_text=textwrap.dedent("""
                    Your settings have been saved successfully.
                    """).strip(),
                ),
                layer=UIManager.OVERLAY_LAYER,
            )

        @main_menu_button.event("on_click")
        def on_main_menu_button_click(event):
            from .main_menu import MainMenuView

            self.window.show_view(MainMenuView(settings=self.settings))
