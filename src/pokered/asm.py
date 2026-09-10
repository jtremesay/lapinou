from collections.abc import Iterable
from pathlib import Path
from typing import Annotated, Literal, cast

from pydantic import BaseModel, Field


class Call(BaseModel):
    name: str
    args: list[str]
    kind: Literal["call"] = "call"


class Comment(BaseModel):
    text: str
    kind: Literal["comment"] = "comment"


class Define(BaseModel):
    name: str
    value: str
    kind: Literal["define"] = "define"


class Label(BaseModel):
    name: str
    kind: Literal["label"] = "label"


class Macro(BaseModel):
    name: str
    body: str
    kind: Literal["macro"] = "macro"


Node = Annotated[Call | Comment | Define | Label | Macro, Field(discriminator="kind")]


def strip_args(args: Iterable[str]) -> list[str]:
    return list(map(str.strip, args))


def parse_asm_file(
    file_path: Path,
    *,
    emit_calls: bool = False,
    emit_comment: bool = False,
    emit_defines: bool = False,
    emit_labels: bool = False,
    emit_macros: bool = False,
) -> list[Node]:
    nodes = []

    with open(file_path, "r") as f:
        parsing_macro = False
        macro_name = None
        macro_body = []
        for line in f:
            line, *comment = line.split(";", 1)
            line = line.strip()
            if line:
                if parsing_macro:
                    if line == "ENDM":
                        parsing_macro = False

                        if emit_macros:
                            assert macro_name is not None

                            nodes.append(
                                Macro(name=macro_name, body="\n".join(macro_body))
                            )

                        macro_name = None
                        macro_body = []
                    else:
                        macro_body.append(line)
                else:
                    if line.startswith("MACRO "):
                        parsing_macro = True
                        macro_name = line[6:].strip()
                    elif line.startswith("DEF "):
                        if emit_defines:
                            name, value = strip_args(line[4:].split(maxsplit=1))
                            nodes.append(Define(name=name, value=value))
                    elif line.endswith(":"):
                        if emit_labels:
                            nodes.append(Label(name=line[:-1].strip()))
                    elif emit_calls:
                        name, *args = line.split(maxsplit=1)
                        args = strip_args((args[0] if args else "").split(","))
                        nodes.append(Call(name=name, args=args))

            if emit_comment and comment:
                nodes.append(Comment(text=comment[0].strip()))

    return nodes


def parse_asm_call_file(file_path: Path) -> list[Call]:
    return [cast(Call, node) for node in parse_asm_file(file_path, emit_calls=True)]
