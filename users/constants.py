import enum


USER_NAME_MAX_LENGTH = 124
USER_SURNAME_MAX_LENGTH = 124
USER_PHONE_MAX_LENGTH = 12
USER_ABOUT_MAX_LENGTH = 256
AVATAR_SIZE = 200
AVATAR_FONT_SIZE = 80
AVATAR_FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
AVATAR_TEXT_COLOR = 'white'
PAGINATE_BY = 12


class AvatarColor(enum.StrEnum):
    TEAL = '#01696f'
    BLUE_GRAY = '#4f98a3'
    GREEN = '#6daa45'
    ORANGE = '#da7101'
    PURPLE = '#a86fdf'
    YELLOW = '#d19900'
    PINK = '#dd6974'
    DARK_BLUE = '#006494'


AVATAR_PALETTE = list(AvatarColor)
