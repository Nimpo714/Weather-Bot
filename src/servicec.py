import emoji


def joiner(a: [], after_element: int):
    """ returns all elements after (element: int) in format -> str1+str2 """
    return "+".join(map(str, a[after_element:]))


def spliter(a: str):
    """ return timezone split
    Local Time: 2025-11-20T18:35:05.009 ->
    Local Time: 2025-11-20 : 18:35:05.009 """
    return a.split('T')


def emoji_decoder(emoji_list: None):
    """ return emoji list in format 😀 -> :grinning_face:"""
    if emoji_list is None:
        emoji_list = []

    # emoji_list [😀, ...] -> decode_emoji [:grinning_face:, ...]
    decode_emoji = []
    for i in emoji_list:
        decode_emoji.append(emoji.demojize(i))

    return decode_emoji


def f_e(emoji_decoded: str):
    """ fast emoji """
    return emoji.emojize(emoji_decoded)
