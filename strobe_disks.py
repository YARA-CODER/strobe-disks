from PIL import Image, ImageShow, ImageDraw, ImageFile, ImageFont
from math import sin, cos, radians, pi, ceil, floor
from os.path import dirname, join
from pprint import pprint


SIZE = (2480, 3508)  # equivalent of A4 @ 300dpi
MIDPOINT = (SIZE[0] / 2, SIZE[1] / 2)
MARGIN = 50  # px
DISC_DIAM = 200  # mm
MARK_SIZE = 20  # px
mm2px = 11.81
fonts_path = join(dirname(__file__), 'fonts')

#font_1 = ImageFont.truetype("arial.ttf", 72, encoding="unic")
#font_2 = ImageFont.truetype("arial.ttf", 24, encoding="unic")
font_1 = ImageFont.truetype(join(fonts_path, 'SourceCodePro-Regular.ttf'), 72)
font_2 = ImageFont.truetype(join(fonts_path, 'SourceCodePro-Regular.ttf'), 24)
logo = Image.open(join('img', 'winylnetlogo.png'))

img = Image.new('RGBA', SIZE, (255, 255, 255, 0))
draw = ImageDraw.Draw(img)
logo = logo.resize((380, 380), resample=Image.LANCZOS)

arr = []


def drawMarks(d, rpm, f, mark_size, half_marks=False):
    '''draws stroboscopic marks with given criteria:
        number_of_marks - should match desired strobe frequency
        d               - diameter of pattern [mm]
        mark_size       - diameter of single mark [mm]
    '''
    num_of_marks = getMarksCount(rpm, f)
    num_of_marks = num_of_marks if half_marks else num_of_marks / 2
    angle = 0
    step = 360 / num_of_marks
    d *= mm2px
    mark_size *= mm2px
    radius = d / 2
    arr.append([rpm, num_of_marks])

    for _ in range(int(customRound(num_of_marks, .6, 0))):
        angle += step
        rad = radians(angle)
        p1 = (MIDPOINT[0] + radius * sin(rad), MIDPOINT[1] + radius * cos(rad))
        draw.ellipse((
            (p1[0] - mark_size, p1[1] - mark_size),
            (p1[0] + mark_size, p1[1] + mark_size)), fill='black')


arr_rads = []


def drawMarks2(d, rpm, f, mark_size, half_marks=False):
    '''draws stroboscopic marks with given criteria:
        number_of_marks - should match desired strobe frequency
        d               - diameter of pattern [mm]
        mark_size       - diameter of single mark [mm]
    '''
    num_of_marks = getMarksCount(rpm, f)
    num_of_marks = num_of_marks if half_marks else num_of_marks / 2
    angle = 0
    step = 360 / num_of_marks
    d *= mm2px
    mark_size *= mm2px
    radius = d / 2
    arr.append([rpm, num_of_marks])
    for i in range(int(customRound(num_of_marks, .8, 0))):
        # if (360 - angle - step)< step:
        #    step = (360-angle)
        angle += step

        rad = radians(angle)
        arr_rads.append([rpm, i, rad, angle, step])
        p1 = (MIDPOINT[0] + radius * sin(rad), MIDPOINT[1] + radius * cos(rad))
        draw.ellipse((
            (p1[0] - mark_size, p1[1] - mark_size),
            (p1[0] + mark_size, p1[1] + mark_size)), fill='black')


def customRound(num, treshold, digits=0):
    if num % 1 > treshold:
        return ceil(num)
    else:
        return floor(num)


def getCirleXY_from_midpoint(xy, d):
    '''
    xy - vector (x,y) of required midpoint
    d - circle diameter [px]
    returns (x1, y1, x2, y2) for draw_ellipse purpose'''
    x, y = xy
    x1, y1 = x - d / 2, y - d / 2
    x2, y2 = x + d / 2, y + d / 2
    return ((x1, y1), (x2, y2))


def getMarkSize(d, num_of_marks):
    circ = pi * d
    ms = circ / num_of_marks / 4
    return round(ms, 2)


def getMarksCount(rpm, f):
    return round(2 * f / rpm * 60, 2)


def drawSpindle(mp, spindle_size):
    spindle_size *= mm2px
    draw.line((
        (mp[0] - spindle_size / 2, mp[1]),
        (mp[0] + spindle_size / 2, mp[1])), fill='black', )

    draw.line((
        (mp[0], mp[1] - spindle_size / 2),
        (mp[0], mp[1] + spindle_size / 2)), fill='black', )

    draw.ellipse(getCirleXY_from_midpoint(mp, spindle_size), width=1, outline='black')


def drawDiscOutline():

    a, b = (
        (0 + MARGIN, (SIZE[1] - SIZE[0]) / 2 + MARGIN),
        (SIZE[0] - MARGIN, (SIZE[1] - SIZE[0]) / 2 + SIZE[0] - MARGIN))
    draw.ellipse((a, b), fill='white', outline='black', width=5)


def drawDiscDescriptionSimple(f):
    txt33 = f'\u219133\u00B9/\u2083'
    txt45 = f'\u219145'
    txt78 = f'\u219178'
    txtf = f'~{f}Hz'
    draw.text((MIDPOINT[0] - 150, MIDPOINT[1] - 1030), txt33, fill='black', font=font_1, align='left')
    draw.text((MIDPOINT[0] - 100, MIDPOINT[1] - 800), txt45, fill='black', font=font_1, align='left')
    draw.text((MIDPOINT[0] - 100, MIDPOINT[1] - 560), txt78, fill='black', font=font_1, align='left')
    draw.text((MIDPOINT[0] - 120, MIDPOINT[1] - 350), txtf, fill='black', font=font_1, align='left')


def drawDiscDescriptionAdvanced(f):
    # font = ImageFont.truetype("arial.ttf", 100)
    txt33 = '33\u00B9/\u2083 '
    txt45 = '45'
    txtf = f'~{f}Hz'  # \u0192= '
    txti1 = f'''ZEWNĘTRZNE znaczniki [x5] -  33\u00B9/\u2083 rpm\nWEWNĘTRZNE znaczniki [x5] -  45 rpm'''
    txti2 = f'''ŚRODKOWY pierścień w każdej grupie oznacza\nprędkość wg specyfikaji, pozostałe\nto odchyłki wg schematu:'''
    txti3 = f'(-4%) (-2%) (OK) (+2%) (+4%)'
    draw.text((MIDPOINT[0] - 450, MIDPOINT[1] - 50), txt33, fill='black', font=font_1, align='left')
    draw.text((MIDPOINT[0] + 300, MIDPOINT[1] - 50), txt45, fill='black', font=font_1, align='left')
    draw.text((MIDPOINT[0] - 120, MIDPOINT[1] - 350), txtf, fill='black', font=font_1, align='left')
    draw.text((MIDPOINT[0] - 230, MIDPOINT[1] + 200), txti1, fill='black', font=font_2, align='left')
    draw.text((MIDPOINT[0] - 230, MIDPOINT[1] + 270), txti2, fill='black', font=font_2, align='left')
    draw.text((MIDPOINT[0] - 180, MIDPOINT[1] + 370), txti3, fill='black', font=font_2, align='left')


def CreateStrobeDisk_simple(f=50):
    drawDiscOutline()
    pasteLogo()
    drawSpindle(MIDPOINT, 7)

    drawMarks2(rpm=33.333, f=f, d=190, mark_size=0.83, half_marks=True)
    drawMarks2(rpm=33.333, f=f, d=180, mark_size=1.66, half_marks=False)
    drawMarks2(rpm=45, f=f, d=150, mark_size=0.89, half_marks=True)
    drawMarks2(rpm=45, f=f, d=140, mark_size=1.78, half_marks=False)
    drawMarks2(rpm=78, f=f, d=110, mark_size=1.12, half_marks=True)
    drawMarks2(rpm=78, f=f, d=100, mark_size=2.24, half_marks=False)

    drawDiscDescriptionSimple(f=f)


def CreateStrobeDisk_advanced(f=50):
    drawDiscOutline()
    pasteLogo()
    drawSpindle(MIDPOINT, 7)
    drawDiscDescriptionAdvanced(f)
    # -4%, -2%, 0%, +2%, +4%
    drawMarks2(rpm=34.66, f=f, d=190, mark_size=0.80, half_marks=False)
    drawMarks2(rpm=34.00, f=f, d=180, mark_size=0.80, half_marks=False)
    drawMarks2(rpm=33.3333, f=f, d=170, mark_size=1.20, half_marks=False)
    drawMarks2(rpm=32.66, f=f, d=160, mark_size=0.80, half_marks=False)
    drawMarks2(rpm=32.00, f=f, d=150, mark_size=0.80, half_marks=False)

    drawMarks2(rpm=43.20, f=f, d=130, mark_size=0.75, half_marks=False)
    drawMarks2(rpm=44.10, f=f, d=120, mark_size=0.75, half_marks=False)
    drawMarks2(rpm=45.00, f=f, d=110, mark_size=1.10, half_marks=False)
    drawMarks2(rpm=45.90, f=f, d=100, mark_size=0.75, half_marks=False)
    drawMarks2(rpm=46.80, f=f, d=90, mark_size=0.75, half_marks=False)


def saveDisc(img, name):

    x1, y1 = MARGIN, (SIZE[1] - SIZE[0]) / 2 + MARGIN
    x2, y2 = SIZE[0] - MARGIN, (SIZE[1] - SIZE[0]) / 2 + SIZE[0] - MARGIN

    img2 = img.crop((x1, y1, x2, y2))
    img.mode = 'RGB'

    img2.save(f'generated_discs/TT_Strobe_Disk_{name}_{f}Hz.png', 'png')
    img.save(f'generated_discs/TT_Strobe_Disk_{name}_{f}Hz.pdf', 'pdf')


def pasteLogo():
    w, h = logo.size
    x, y = MIDPOINT
    box = (int(x - w / 2), int(y - h / 2), int(x + w / 2), int(y + h / 2))
    img.alpha_composite(logo, dest=(box[0], box[1]))


def getmarks():
    n = 180
    ds = [150, 140, 130, 120, 110, 100]
    for d in ds:
        ms = getMarkSize(d=d, num_of_marks=n)
        print(f'{d}: {round(ms,2)}\t {round(ms*2,2)}')


if __name__ == '__main__':

    f = 50
    CreateStrobeDisk_advanced(f=f)
    saveDisc(img, 'advanced')

    CreateStrobeDisk_simple(f=f)
    saveDisc(img, 'simple')
