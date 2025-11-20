def joiner(a: None, after_element: int):
    """ returns all elements after (element: int) in format -> str1+str2 """
    return "+".join(map(str, a[after_element:]))


def spliter(a: str):
    """ return timezone split
    Local Time: 2025-11-20T18:35:05.009 ->
    Local Time: 2025-11-20 : 18:35:05.009 """
    return a.split('T')
