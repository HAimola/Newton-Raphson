from enum import Enum, auto
from typing import Generator
import math
from dataclasses import dataclass, field


class Op(Enum):
    EXP = 0
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    OPEN_PAREN = auto()
    CLOSE_PAREN = auto()
    ABS = auto()
    SIN = auto()
    COS = auto()
    TAN = auto()
    LOG = auto()
    LN = auto()
    SQRT = auto()
    PI = auto()
    E = auto()
    OP_COUNT = auto()


OP_NAMES = {"^": Op.EXP,
            "+": Op.PLUS,
            "-": Op.MINUS,
            "*": Op.MUL,
            "/": Op.DIV,
            "(": Op.OPEN_PAREN,
            ")": Op.CLOSE_PAREN,
            "abs": Op.ABS,
            "sin": Op.SIN,
            "cos": Op.COS,
            "tan": Op.TAN,
            "log": Op.LOG,
            "ln": Op.LN,
            "sqrt": Op.SQRT,
            "PI": Op.PI,
            "E": Op.E,
            }


def uncallable_func():
    raise ValueError("Can't convert operation to function.")


OP_FUNCS = {Op.EXP: lambda x, exp: x ** exp,
            Op.PLUS: lambda x, y: x + y,
            Op.MINUS: lambda x, y: x - y,
            Op.MUL: lambda x, y: x * y,
            Op.DIV: lambda x, y: x / y,
            Op.OPEN_PAREN: uncallable_func,
            Op.CLOSE_PAREN: uncallable_func,
            Op.ABS: math.fabs,
            Op.SIN: math.sin,
            Op.COS: math.cos,
            Op.TAN: math.tan,
            Op.LOG: math.log,
            Op.LN: math.log,
            Op.SQRT: math.sqrt,
            Op.PI: math.pi,
            Op.E: math.e,
            }


class TokenType(Enum):
    OP = auto()
    LITERAL = auto()
    IDENTIFIER = auto()


@dataclass(frozen=True)
class Token:
    typ: TokenType
    val: float or Op
    # TODO: accept range of locations for evaluated expressions
    loc: int = field(default=0)

    def __str__(self):
        return f"Token(typ={self.typ.name}, val={self.val}, loc={self.loc})"


@dataclass
class Node:
    def __init__(self, data=None):
        self.data = data
        self.left = None
        self.right = None
        self.root = None

    def add_left(self, other):
        assert isinstance(other, Node)
        other.root = self
        self.left = other

    def add_right(self, other):
        other.root = self
        self.right = other

    def __str__(self):
        return f"Node[{self.data=}]"


class Equation:
    def __init__(self, equ: str, identifiers: list[str] or None = None):
        assert isinstance(equ, str), f"Can't parse object of type '{type(equ)}'. Use a string instead."
        assert equ, "Equation input string cannot be empty."

        identifiers = identifiers if identifiers else []

        for ident in identifiers:
            if ident in OP_NAMES:
                raise SyntaxError(f"Cannot use reserved word '{ident}' as an identifier.")
            if len(ident) > 10:
                raise SyntaxError(f"Identifier name '{ident}' too long. Choose a name that is at "
                                  f"most 10 characters long.")

        self.equ: str = equ
        self.identifiers: list[str] = identifiers
        self.__tree: ParseTree = parse_tree([token for token in tokenize_from_str(self.equ, self.identifiers)],
                                            self.equ)

    def traverse(self) -> Generator[Node, None, None]:
        self.__tree.go_to_highest_root()
        yield from self.__tree.traverse()

    def __str__(self) -> str:
        self.__tree.go_to_highest_root()
        return self.__tree.__str__()

    def __len__(self):
        return len([node for node in self.__tree.traverse()])


_MISSING = object()  # Sentinel to differentiate between Node with value 'None' and no Node at all


class ParseTree:
    def __init__(self, node):
        assert isinstance(node, Node)
        self.node = node

    @property
    def current_data(self):
        return self.node.data

    @current_data.setter
    def current_data(self, value):
        if isinstance(value, Token):
            self.node.data = value

    @property
    def left_data(self) -> _MISSING or Token:
        if self.node.left:
            return self.node.left.data
        else:
            return _MISSING

    @left_data.setter
    def left_data(self, val):
        if self.node.left:
            self.node.left.data = val
        else:
            self.node.left = Node(val)

    @property
    def right_data(self) -> _MISSING or Token:
        if self.node.right:
            return self.node.right.data
        else:
            return _MISSING

    @property
    def root_data(self) -> _MISSING or Token:
        if self.node.root:
            return self.node.root.data
        else:
            return _MISSING

    def go_root(self):
        if self.node.root:
            self.node = self.node.root
        else:
            raise ValueError("Node has no root!")

    def go_to_highest_root(self):
        while True:
            try:
                self.go_root()
            except ValueError:
                break

    def go_right(self):
        if self.node.right:
            self.node = self.node.right
        else:
            raise ValueError("No such branch to the right of the tree!")

    def go_left(self):
        if self.node.left:
            self.node = self.node.left
        else:
            raise ValueError("No such branch to the left of the tree!")

    def set_as_left_child(self, node: Node):
        assert isinstance(node, Node)

        tmp = Node()
        tmp.add_left(node)
        self.node = tmp

    def traverse(self, root=None) -> Generator[Node, None, None]:
        if root is None:
            root = self.node

        if root.left and root.left.data is not _MISSING:
            yield from self.traverse(root.left)

        yield root

        if root.right and root.right.data is not _MISSING:
            yield from self.traverse(root.right)

    def __str__(self) -> str:
        out_str = ""
        for node in self.traverse():
            out_str += f"{node.data.__str__()}\n"
        return out_str


@dataclass
class CaptureGroup:
    expected: TokenType
    expiration: int
    offset_list: list[int]
    expected_op: field(default=None)
    e: Exception = field(default=SyntaxError)


def capture_groups():
    pass


def eval_tree(equ: Equation) -> ParseTree or float:
    backtrack = 0
    node_list = [node for node in equ.traverse()]

    if not equ.identifiers:
        for i in range(0, len(node_list)):
            node = node_list[i]

            if node.data.typ == TokenType.OP:
                if backtrack:
                    node = backtrack

                if node.right.data.typ == TokenType.OP:
                    backtrack = node
                    node = node.right

                result = OP_FUNCS[node.data.val](node.left.data.val, node.right.data.val)
                new_tk = Token(TokenType.LITERAL, result, -1)
                node.data = new_tk
                node.left = None
                node.right = None

    else:
        pass


def parse_tree(tk_list: list[Token], input_string) -> ParseTree:
    cap_group: list[CaptureGroup] = []

    tree: ParseTree = ParseTree(Node())
    assert len(tk_list), "No tokens to parse. Input string may be empty."

    for tk, next_tk in zip(tk_list, tk_list[1:]):
        print(tree)
        if tk.typ == TokenType.OP:
            if tk.val == Op.OPEN_PAREN:
                tree.node.add_left(Node())
                tree.go_left()

            elif tk.val == Op.CLOSE_PAREN:
                tree.go_root()

            elif tk.val == Op.PI:
                tree.current_data = Token(TokenType.LITERAL, math.pi, tk.loc)

            elif tk.val == Op.E:
                tree.current_data = Token(TokenType.LITERAL, math.e, tk.loc)

            else:
                if tk.val == Op.MUL:
                    pass

                if tk.val == Op.SIN:
                    pass

                try:
                    if tree.root_data:
                        tree.go_root()
                        tree.set_as_left_child(tree.node)
                    else:
                        tree.go_root()
                except ValueError:  # Create root to the left
                    tree.set_as_left_child(tree.node)
                tree.current_data = tk
                tree.node.add_right(Node())
                tree.go_right()

        if tk.typ == TokenType.LITERAL or tk.typ == TokenType.IDENTIFIER:
            tree.current_data = tk

    # if total_paren:
    #     loc = tree.current_data.loc + 1
    #     err_str = f"Parenthesis opened but not closed at location {loc}\n"
    #     err_str += f"{'':13}INPUT: {input_string+'_'}\n"
    #     err_str += f"{'':{20+loc}}{'^'}"
    #     raise SyntaxError(err_str)

    return tree


def reconstruct_str(tree: ParseTree) -> str:
    pass


def tokenize_from_str(equ: str, identifiers: list[str] = None) -> Generator[Token, None, None]:
    val: str = ""
    identifiers = identifiers if identifiers else []
    pos: int = 0

    # Iterate through the equation to tokenize
    while pos != len(equ):

        # Handling Literals
        while equ[pos].isdigit():
            val += equ[pos]
            pos += 1
            if pos == len(equ) and val:  # In case literal is the last char
                yield Token(TokenType.LITERAL, float(val), pos - len(val))
                return
        if val:
            yield Token(TokenType.LITERAL, float(val), pos - len(val))

        val = ""

        # Handling Operations and Identifiers
        while not equ[pos].isdigit():
            if equ[pos] == " ":  # Ignore whitespaces
                pos += 1
            else:
                val += equ[pos]
                pos += 1

            if val in OP_NAMES:
                yield Token(TokenType.OP, OP_NAMES[val], pos - len(val))
                break
            if val in identifiers:
                yield Token(TokenType.IDENTIFIER, val, pos - len(val))
                break
            if pos == len(equ):
                break

        if val and val not in OP_NAMES and val not in identifiers:
            raise ValueError(f"Operation '{val}' does not exist, isn't implemented or "
                             f"cannot be recognized as an identifier.")

        val = ""


def evaluate(input_string: str, identifiers: list[str] = None, debug: bool = True):
    if debug:
        tk_list = [tk for tk in tokenize_from_str(input_string, identifiers)]

        print(f"DEBUG: {input_string = }")
        print(f"       {len(input_string) = }")
        print(f"       {tk_list=}")
        print(f"       {len(tk_list) = }\n")

    equ = Equation(input_string, identifiers)
    return equ


if __name__ == "__main__":
    a = evaluate("20*(PI-300)*E")
    eval_tree(a)
    print(a)
