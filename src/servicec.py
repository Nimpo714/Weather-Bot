from datetime import datetime, timedelta


def joiner(a: [], after_element: int):
    """ returns all elements after (element: int) in format -> str1+str2 """
    return "+".join(map(str, a[after_element:]))


def spliter(a: str):
    """ return timezone split
    Local Time: 2025-11-20T18:35:05.009 ->
    Local Time: 2025-11-20 : 18:35:05.009 """
    return a.split('T')


def date(days: int = 0):
    """ return date in format now_date + YYYY-MM-DD"""
    now = datetime.now()  # дата сейчас
    future_date = now + timedelta(days=days)  # будущая дата
    return future_date.strftime('%Y-%m-%d')
