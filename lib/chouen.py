from urllib.parse import urlencode


class ChouenException(Exception):
    ...


def getChouen(
    top: str = None,
    bottom: str = None,
    rainbow: bool = False,
):
    """
    hoge兆円のURLを取得します。
    """
    if top == None and bottom == None:
        raise ChouenException("topもしくはbottomのどちらかには値が必要です")
    datalist: list = [
        [top != None, ("top", top)],
        [bottom != None, ("bottom", bottom)],
        [rainbow, ("rainbow", "true")],
        [(top == None or bottom == None), ("single", "true")]
    ]

    paramlist: list[str] = []
    for n in datalist:
        if n[0]:
            paramlist.append(n[1])

    param = urlencode(paramlist)
    return "?".join(["https://gsapi.cbrx.io/image", param])
