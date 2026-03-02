from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Tuple


ALLOWED_VARIABLES = {"a", "b", "c", "d", "e"}


@dataclass(frozen=True)
class Token:
    kind: str
    value: str
    position: int


class Node:
    def evaluate(self, assignment: Dict[str, int]) -> int:
        raise NotImplementedError

    def variables(self) -> set[str]:
        raise NotImplementedError


@dataclass(frozen=True)
class ConstNode(Node):
    value: int

    def evaluate(self, assignment: Dict[str, int]) -> int:  # noqa: ARG002
        return int(bool(self.value))

    def variables(self) -> set[str]:
        return set()


@dataclass(frozen=True)
class VarNode(Node):
    name: str

    def evaluate(self, assignment: Dict[str, int]) -> int:
        if self.name not in assignment:
            raise ValueError(f"Variable '{self.name}' is not defined in assignment.")
        return int(bool(assignment[self.name]))

    def variables(self) -> set[str]:
        return {self.name}


@dataclass(frozen=True)
class NotNode(Node):
    child: Node

    def evaluate(self, assignment: Dict[str, int]) -> int:
        return 1 - self.child.evaluate(assignment)

    def variables(self) -> set[str]:
        return self.child.variables()


@dataclass(frozen=True)
class BinaryNode(Node):
    op: str
    left: Node
    right: Node

    def evaluate(self, assignment: Dict[str, int]) -> int:
        left_value = self.left.evaluate(assignment)
        right_value = self.right.evaluate(assignment)
        if self.op == "&":
            return left_value & right_value
        if self.op == "|":
            return left_value | right_value
        if self.op == "->":
            return int((1 - left_value) | right_value)
        if self.op == "~":
            return int(left_value == right_value)
        raise ValueError(f"Unknown binary operator: {self.op}")

    def variables(self) -> set[str]:
        return self.left.variables() | self.right.variables()


@dataclass(frozen=True)
class ParsedExpression:
    source: str
    root: Node
    variables: Tuple[str, ...]


class _Tokenizer:
    _replacements = {
        "¬": "!",
        "∧": "&",
        "∨": "|",
        "→": "->",
        "⇒": "->",
        "↔": "~",
        "≡": "~",
    }

    def __init__(self, text: str) -> None:
        self._text = self._normalize(text)

    @property
    def normalized_text(self) -> str:
        return self._text

    @classmethod
    def _normalize(cls, text: str) -> str:
        normalized = text
        for source, target in cls._replacements.items():
            normalized = normalized.replace(source, target)
        return normalized

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        text = self._text
        index = 0
        while index < len(text):
            current = text[index]
            if current.isspace():
                index += 1
                continue
            if text.startswith("->", index):
                tokens.append(Token("IMP", "->", index))
                index += 2
                continue
            if current == "!":
                tokens.append(Token("NOT", current, index))
                index += 1
                continue
            if current == "&":
                tokens.append(Token("AND", current, index))
                index += 1
                continue
            if current == "|":
                tokens.append(Token("OR", current, index))
                index += 1
                continue
            if current == "~":
                tokens.append(Token("EQ", current, index))
                index += 1
                continue
            if current == "(":
                tokens.append(Token("LPAREN", current, index))
                index += 1
                continue
            if current == ")":
                tokens.append(Token("RPAREN", current, index))
                index += 1
                continue
            if current in {"0", "1"}:
                tokens.append(Token("CONST", current, index))
                index += 1
                continue
            lowered = current.lower()
            if lowered in ALLOWED_VARIABLES:
                tokens.append(Token("VAR", lowered, index))
                index += 1
                continue
            raise ValueError(f"Unsupported character '{current}' at position {index}.")
        tokens.append(Token("END", "", len(text)))
        return tokens


class _Parser:
    def __init__(self, tokens: Iterable[Token]) -> None:
        self._tokens = list(tokens)
        self._position = 0

    @property
    def _current(self) -> Token:
        return self._tokens[self._position]

    def _match(self, kind: str) -> bool:
        if self._current.kind == kind:
            self._position += 1
            return True
        return False

    def _consume(self, kind: str) -> Token:
        token = self._current
        if token.kind != kind:
            raise ValueError(
                f"Expected token '{kind}' at position {token.position}, got '{token.kind}'."
            )
        self._position += 1
        return token

    def parse(self) -> Node:
        node = self._parse_equivalence()
        self._consume("END")
        return node

    def _parse_equivalence(self) -> Node:
        node = self._parse_implication()
        while self._match("EQ"):
            right = self._parse_implication()
            node = BinaryNode("~", node, right)
        return node

    def _parse_implication(self) -> Node:
        node = self._parse_or()
        if self._match("IMP"):
            right = self._parse_implication()
            return BinaryNode("->", node, right)
        return node

    def _parse_or(self) -> Node:
        node = self._parse_and()
        while self._match("OR"):
            right = self._parse_and()
            node = BinaryNode("|", node, right)
        return node

    def _parse_and(self) -> Node:
        node = self._parse_unary()
        while self._match("AND"):
            right = self._parse_unary()
            node = BinaryNode("&", node, right)
        return node

    def _parse_unary(self) -> Node:
        if self._match("NOT"):
            return NotNode(self._parse_unary())
        return self._parse_primary()

    def _parse_primary(self) -> Node:
        token = self._current
        if self._match("VAR"):
            return VarNode(token.value)
        if self._match("CONST"):
            return ConstNode(int(token.value))
        if self._match("LPAREN"):
            inner = self._parse_equivalence()
            self._consume("RPAREN")
            return inner
        raise ValueError(
            f"Expected variable, constant, or '(' at position {token.position}."
        )


def parse_expression(text: str) -> ParsedExpression:
    tokenizer = _Tokenizer(text)
    tokens = tokenizer.tokenize()
    parser = _Parser(tokens)
    root = parser.parse()
    variables = tuple(sorted(root.variables()))
    if len(variables) > 5:
        raise ValueError("At most 5 variables are supported.")
    return ParsedExpression(source=tokenizer.normalized_text, root=root, variables=variables)
