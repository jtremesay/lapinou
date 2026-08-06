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
from os import environ

from pydantic_ai import Agent

from .models import Character


def create_agent(model: str | None = None) -> Agent:
    return Agent(model or environ["LAPINOU_MODEL"])


def create_character(agent: Agent | None = None) -> Character:
    if agent is None:
        agent = create_agent()

    return agent.run_sync("Generate a character", output_type=Character).output
