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


from arcade.gui import (
    UIAnchorLayout,
    UIBoxLayout,
    UIButtonRow,
    UIDropdown,
    UIInputText,
    UILabel,
    UIOnClickEvent,
    UIView,
)

from lapinou.models.character import Character, Gender
from lapinou.models.settings import Settings
from lapinou.ui.wood_frame import with_wood_frame_background


class CharacterCreationView(UIView):
    def __init__(self, settings: Settings | None = None) -> None:
        super().__init__()
        self.settings = settings

        root = self.ui.add(UIAnchorLayout())
        root.add(
            UILabel(
                text="Character Creation",
                font_size=32,
                text_color=(255, 255, 255),
                align="center",
            ),
            anchor_y="top",
            align_y=-50,
        )

        body = root.add(with_wood_frame_background(UIBoxLayout(vertical=True)))

        name_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        name_row.add(
            UILabel(
                text="Name",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.character_name_input = name_row.add(UIInputText(width=300))

        age_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        age_row.add(
            UILabel(
                text="Age",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.character_age_input = age_row.add(UIInputText(width=300))

        gender_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        gender_row.add(
            UILabel(
                text="Gender",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.gender_dropdown = gender_row.add(
            UIDropdown(width=300, options=[gender.value for gender in Gender])
        )

        occupation_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        occupation_row.add(
            UILabel(
                text="Occupation",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.occupation_input = occupation_row.add(UIInputText(width=300))

        biography_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        biography_row.add(
            UILabel(
                text="Biography",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.biography_input = biography_row.add(UIInputText(width=300, height=100))

        description_row = body.add(UIBoxLayout(vertical=False, space_between=10))
        description_row.add(
            UILabel(
                text="Description",
                font_size=24,
                text_color=(0, 0, 255),
                align="left",
            )
        )
        self.description_input = description_row.add(UIInputText(width=300, height=100))

        button_row = root.add(
            UIButtonRow(spacing=10, align="center"), anchor_y="bottom", align_y=50
        )

        create_button = button_row.add_button("Random")
        create_button = button_row.add_button(label="Create")
        create_button.event("on_click")(self.on_create_button_click)

    def on_create_button_click(self, event: UIOnClickEvent) -> None:
        # TODO: Validate inputs and handle errors

        character = Character(
            name=self.character_name_input.text,
            age=int(self.character_age_input.text),
            gender=Gender(self.gender_dropdown.value),
            occupation=self.occupation_input.text,
            biography=self.biography_input.text,
            description=self.description_input.text,
        )
        print(character.model_dump())
