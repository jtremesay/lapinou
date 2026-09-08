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
    UIOnClickEvent,
    UIView,
)
from arcade.gui.experimental import UIPasswordInput

from lapinou.models.settings import Settings
from lapinou.ui.wood_frame import with_wood_frame_background


class SettingsView(UIView):
    def __init__(self, settings: Settings) -> None:
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

        llm_model_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        llm_model_row.add(
            UILabel(
                text="LLM Model", font_size=24, text_color=(0, 0, 255), align="left"
            )
        )
        self.llm_model_input = llm_model_row.add(UIInputText(width=200))
        if settings:
            self.llm_model_input.text = settings.llm_model

        google_api_key_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        google_api_key_row.add(
            UILabel(
                text="Google API Key",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.google_api_key_input = google_api_key_row.add(UIPasswordInput(width=200))
        if settings:
            self.google_api_key_input.text = settings.google_api_key or ""

        ollama_url_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        ollama_url_row.add(
            UILabel(
                text="Ollama URL", font_size=24, text_color=(0, 0, 255), align="left"
            )
        )
        self.ollama_url_input = ollama_url_row.add(UIInputText(width=200))
        if settings:
            self.ollama_url_input.text = settings.ollama_url or ""

        ollama_api_key_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        ollama_api_key_row.add(
            UILabel(
                text="Ollama API Key",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.ollama_api_key_input = ollama_api_key_row.add(UIPasswordInput(width=200))
        if settings:
            self.ollama_api_key_input.text = settings.ollama_api_key or ""

        button_row = root.add(
            UIButtonRow(spacing=10, align="center"), anchor_y="bottom", align_y=50
        )

        self.save_button = button_row.add(
            UIFlatButton(text="Save", width=100, height=40),
        )
        self.save_button.event("on_click")(self.on_save_button_click)
        self.main_menu_button = button_row.add(
            UIFlatButton(text="Main Menu", width=100, height=40),
        )
        self.main_menu_button.event("on_click")(self.on_main_menu_button_click)

    def on_save_button_click(self, event: UIOnClickEvent) -> None:
        # TODO: Validate inputs before saving
        new_settings = Settings(
            llm_model=self.llm_model_input.text,
            google_api_key=self.google_api_key_input.text or None,
            ollama_url=self.ollama_url_input.text or None,
            ollama_api_key=self.ollama_api_key_input.text or None,
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

    def on_main_menu_button_click(self, event: UIOnClickEvent) -> None:
        from .main_menu import MainMenuView

        self.window.show_view(MainMenuView(settings=self.settings))
