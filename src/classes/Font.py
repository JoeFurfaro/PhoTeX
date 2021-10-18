from typing import Optional

class Font(object):
    defs_map = {
        'Arial': None,
        'Helvetica': None,
        'Times New Roman': None,
        'Roboto': 'https://fonts.googleapis.com/css2?family=Roboto&display=swap',
        'Wingdings': None,
    }
    def __init__(self,
            family: str, size: Optional[int] = None, weight: Optional[str] = None
        ):
        self.family: str = family
        self.size: Optional[int] = size
        self.weight: Optional[str] = weight

    def render(self) -> str:
        s = f'font-family="{self.family}"'
        if self.size != None:
            s += f' font-size="{self.size}"'
        if self.weight != None:
            s += f' font-weight="{self.weight}"'
        return s

    def defs(self) -> str:
        if (self.family in Font.defs_map) and (self.family[0] != '@') and (Font.defs_map[self.family] != None):
            return f'<style type="text/css">\n\t@import url("{Font.defs_map[self.family]}");\n</style>'
        return ''
