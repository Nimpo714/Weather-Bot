def joiner(a: None, after_element: int):
    """ returns all elements after (element: int) in format -> str1+str2 """
    return "+".join(map(str, a[after_element:]))

