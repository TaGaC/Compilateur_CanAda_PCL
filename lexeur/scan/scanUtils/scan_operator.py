def scan_operator(source_code: str, position: int, op: list) -> "tuple[int, str, int]":
    temp = source_code[position: position + 2]

    if (temp[0] in op and temp in op) or temp == ":=" or temp == "==":
        return 1, temp, position + 2
    else:
        return 1 if temp[0] in op else 2, temp[0], position + 1
