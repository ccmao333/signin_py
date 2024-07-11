from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import os
import io
import base64
import textwrap

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + '\\image\\'
TTF_DD_DIR = BASE_DIR + 'TTF\\DingTalk JinBuTi.ttf'
TTF_YY_DIR = BASE_DIR + 'TTF\\猫啃网秀雅圆.ttf'
Image_Cx_DIR = BASE_DIR + '查询.png'
Image_Se_DIR = BASE_DIR + '色色十连.png'
Image_qd_w = BASE_DIR + '白天样板.png'
Image_qd_w_yg = BASE_DIR + '白天样板-鱼干.png'
Image_qd_b = BASE_DIR + '夜晚样板.png'
Image_qd_b_yg = BASE_DIR + '夜晚样板-鱼干.png'
Image_zlk_DIR = BASE_DIR + '资料卡.png'
Image_xx_DIR = BASE_DIR + '资料卡标识\\xx_.png'
Image_yl_DIR = BASE_DIR + '资料卡标识\\yl_.png'
Image_ty_DIR = BASE_DIR + '资料卡标识\\ty_.png'
Image_hg_DIR = BASE_DIR + '资料卡标识\\hg_.png'
Image_mlb_DIR = BASE_DIR + '猫粮榜.png'
Fc_DIR = BASE_DIR + 'AC.png'
DB_DIR = os.path.dirname(__file__)

from cbp import *
from Sqledit import *

def SigninBin(user_name: str, CatM: int,yg:int, row: list[str], transpose: bool,thursday:bool) -> object:
    cid = row[0]  # 唯一编号
    group_id = row[1]  # 群
    user_id = row[2]  # QQ
    ml = row[3]  # 猫粮
    yg = row[4]  # 鱼干 特殊情况用
    hex = row[5]  # 幸运色HEX
    yq = row[6]  # 月签
    lj = row[7]  # 累计
    pm = get_group_count(group_id)  # 签到排名
    maxdays = days()  # 星期
    Memory_image = Image.new("RGBA", (980, 472), "white")  # 内存图形.创建 (980, 472)
    if is_daytime():
        if thursday:
            image_Bin = Image.open(Image_qd_w_yg)
        else:
            image_Bin = Image.open(Image_qd_w)
        TTF_Color = ['#2f76a8', '#7fe2a4']
    else:
        if thursday:
            image_Bin = Image.open(Image_qd_b)
        else:
            image_Bin = Image.open(Image_qd_b_yg)
        TTF_Color = ['#4f84af', '#80ffbf']
    LuckColor = Image.new("RGB", (100, 100), f"{row[5]}")  # 今日幸运色
    User_Bin = Image.open(load_image_data(f'{user_id}'))  # 加载头像数据
    Memory_image.paste(User_Bin.resize((150, 150)), (24, 28))  # 头像大小 画头像
    Memory_image.paste(image_Bin, mask=image_Bin)  # 主样板
    Memory_image.paste(LuckColor, (237, 283))  # 幸运色图片
    # >>画图结束<< 画文字开始
    Draw = ImageDraw.Draw(Memory_image)
    fontA = ImageFont.truetype(TTF_DD_DIR, 30)
    fontB = ImageFont.truetype(TTF_DD_DIR, 40)
    fontC = ImageFont.truetype(TTF_DD_DIR, 100)
    fontD = ImageFont.truetype(TTF_YY_DIR, 23)
    Draw.text((245, 33), f'{user_name}', font=fontA, fill=TTF_Color[0])  # 昵称
    Draw.text((615, 33), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), font=fontA, fill=TTF_Color[0])  # 签到时间
    Draw.text((245, 100), f'+{CatM}', font=fontA, fill=TTF_Color[0])  # +猫粮
    if thursday:
        Draw.text((610, 100), f'+{yg}', font=fontA, fill=TTF_Color[0])  # 鱼干
    else:
        Draw.text((610, 100), f'{ml} 猫粮', font=fontA, fill=TTF_Color[0])  # 总猫粮

    Draw.text((290 - Draw.textlength(f'{hex}', font=fontB) / 2, 390), f'{hex}', font=fontB, fill=TTF_Color[0])  # 幸运色代码
    Draw.text((380 - Draw.textlength(f'{yq}/{maxdays}', font=fontB) / 2, 157), f'{yq}/{maxdays}', font=fontB,fill=TTF_Color[0])  # 月签
    Draw.text((770 - Draw.textlength(lj, font=fontB) / 2, 157), lj, font=fontB, fill=TTF_Color[0])  # 累计签到
    if cid == 'New':
        Draw.text((0, 200), 'New', font=fontA, fill=TTF_Color[1])  # CID
    else:
        Draw.text((0, 200), f'CID[ {cid} ]', font=fontA, fill=TTF_Color[1])  # CID
    Draw.text((0, 390), get_day_of_week(), font=fontA, fill=TTF_Color[1])  # 星期
    Draw.text((460 - Draw.textlength(pm, font=fontC) / 2, 285), pm, font=fontC, fill=TTF_Color[0])  # 排名

    # 一言切片
    YiyanText = yiyan()
    YiyanText = textwrap.fill(YiyanText, width=21)
    Draw.text((558, 258), YiyanText, font=fontD, fill='#727272')
    # 反向指令
    if transpose: Memory_image = Memory_image.transpose(Image.FLIP_LEFT_RIGHT)  
    buffer = io.BytesIO()
    Memory_image.save(buffer, format="png")
    base64_data = base64.b64encode(buffer.getvalue())
    return base64_data.decode()


def sign_cx_Bin(row: list[str], transpose: bool) -> object:
    cid = row[0]  # 唯一编号
    group_id = row[1]  # 群
    user_id = row[2]  # QQ
    ml = row[3]  # 猫粮
    yg = row[4]  # 鱼干 特殊情况用
    hex_t = hex = row[5]  # 幸运色HEX
    yq = row[6]  # 月签
    lj = row[7]  # 累计
    zhqd = row[8]
    _user_time = datetime.strptime(zhqd, "%Y-%m-%d %H:%M:%S")
    _system_time = datetime.now().strftime("%Y-%m-%d")
    if _user_time.strftime("%Y-%m-%d") != _system_time:
        hex = '#efcbb2'
        hex_t = 'Null'

    list = sql_command(group_id, user_id)

    Memory_image = Image.new("RGBA", (1258, 720))
    # 今日幸运色
    Color = Image.new("RGB", (1258, 720), hex)
    # 幸运色图片
    Memory_image.paste(Color, (0, 0))
    # 加载头像数据
    User_Bin = Image.open(load_image_data(user_id))
    # 头像大小 画头像
    Memory_image.paste(User_Bin.resize((200, 200)), (251, 58))
    # 空样板
    image_Bin = Image.open(Image_Cx_DIR)  
    FC_Bin = Image.open(Fc_DIR)
    # 主样板
    Memory_image.paste(image_Bin, mask=image_Bin)  

    Draw = ImageDraw.Draw(Memory_image)
    fontA = ImageFont.truetype(TTF_DD_DIR, 30)
    fontB = ImageFont.truetype(TTF_DD_DIR, 40)
    fontC = ImageFont.truetype(TTF_DD_DIR, 60)
    fontD = ImageFont.truetype(TTF_DD_DIR, 100)

    Draw.text((0, 680), f'CID[ {cid} ]', font=fontA, fill=(45, 220, 142))  # CID
    Draw.text((120, 280), ml, font=fontB, fill='#764ba2')  # 猫粮
    Draw.text((120, 370), yg, font=fontB, fill='#764ba2')  # 鱼干
    Draw.text((550 - Draw.textlength('?', font=fontC) / 2, 265), '?', font=fontC, fill='#764ba2')  # 排名
    Draw.text((550 - Draw.textlength(lj, font=fontC) / 2, 360), lj, font=fontC, fill='#764ba2')  # 累计签到
    Draw.text((350 - Draw.textlength(hex_t, font=fontD) / 2, 470), hex_t, font=fontD, fill=hex)  # Hex
    Draw.rectangle((692, 110, 1235, 172), outline=(128, 128, 255), width=5)
    Draw.text((710, 115), '日', font=fontB, fill=(45, 220, 142))
    Draw.text((785, 115), '一', font=fontB, fill=(120, 54, 253))
    Draw.text((865, 115), '二', font=fontB, fill=(120, 54, 253))
    Draw.text((945, 115), '三', font=fontB, fill=(120, 54, 253))
    Draw.text((1025, 115), '四', font=fontB, fill=(120, 54, 253))
    Draw.text((1105, 115), '五', font=fontB, fill=(120, 54, 253))
    Draw.text((1185, 115), '六', font=fontB, fill=(45, 220, 142))

    Draw.text((690, 70), get_month_name(), font=fontA, fill=(120, 54, 253))
    i = 0
    x = 0
    n = week()
    dayint = days()
    for a in range(dayint):
        i += 1
        if i == list[a]:
            Memory_image.paste(FC_Bin, (700 + 80 * n, 175 + 65 * x), mask=FC_Bin)
        Draw.text((725 + 80 * n - Draw.textlength(str(i), font=fontB) / 2, 175 + 65 * x), str(i), font=fontB,fill=(247, 74, 74))  # 画日期
        n += 1
        if n == 7:
            n = 0
            x += 1
    # 出图咧
    if transpose: Memory_image = Memory_image.transpose(Image.FLIP_LEFT_RIGHT)  # 水平翻转
    buffer = io.BytesIO()
    Memory_image.save(buffer, format="png")
    base64_data = base64.b64encode(buffer.getvalue())
    return base64_data.decode()

#,
def user_zlk(Data: list, group_name: str) -> object:
    user_id = Data.get('user_id')
    card = Data.get('card') or Data.get('nickname')
    title = Data.get('title')
    if not title: title = '[Undefined]'
    level = Data.get('level')
    join_time = Data.get('join_time')
    sexRGB = sex_int(Data.get('sex'))

    BG_Color = sexRGB[0]
    TTF_Color = sexRGB[1]
    
    Memory_image = Image.new("RGBA", (1000, 500))
    Draw = ImageDraw.Draw(Memory_image)

    Draw.rectangle([(0, 0), (1000, 500)], fill=BG_Color)
    User_Bin = Image.open(load_image_data(user_id))  # 加载头像数据
    Memory_image.paste(User_Bin.resize((500, 500)), (0, 0))  # 头像大小 画头像

    image_Bin = Image.open(Image_zlk_DIR)  # 空样板
    Memory_image.paste(image_Bin, mask=image_Bin)  # 主样板

    fontA = ImageFont.truetype(TTF_DD_DIR, 30)
    fontB = ImageFont.truetype(TTF_DD_DIR, 40)

    Draw.text((475, 220), 'Level:', font=fontA, fill=BG_Color)
    Draw.text((475, 285), '头衔:', font=fontA, fill=BG_Color)
    Draw.text((475, 355), '入群时间:', font=fontA, fill=BG_Color)
    Draw.text((475, 430), '在群时间:', font=fontA, fill=BG_Color)
    # ---
    Draw.text((470, 80), card, font=fontA, fill=BG_Color)
    Draw.text((570, 220), level, font=fontA, fill=TTF_Color)
    Draw.text((550, 285), title, font=fontA, fill=TTF_Color)
    Draw.text((615, 355), inttotime(join_time), font=fontA, fill=TTF_Color)
    Draw.text((615, 430), convert_group_time(infotimestamp() - join_time), font=fontA, fill=TTF_Color)
    Draw.text((750 - Draw.textlength(group_name, font=fontB) / 2, 0), group_name, font=fontB, fill=BG_Color)

    list = user_qqlevel(int(Data.get('qq_level')))
    #空等级判断
    if list != [0,0,0,0]:
        Arr = [Image_hg_DIR,Image_ty_DIR,Image_yl_DIR,Image_xx_DIR]
        x = 0
        n = 0
        for i in list:
            level_Bin = Image.open(Arr[n]).convert('RGBA').resize((40, 40))

            for j in range(i):
                Memory_image.paste(level_Bin, (475 + x, 140),mask=level_Bin)  # 头像大小 画头像
                x += 40
            n += 1
    else:
        Draw.text((475, 140), '[qqlevel object Error]', font=fontA, fill=(255, 0, 0))

    # Memory_image.show()
    # return 0
    # 出图咧
    buffer = io.BytesIO()
    Memory_image.save(buffer, format="png")
    base64_data = base64.b64encode(buffer.getvalue())
    return base64_data.decode()

#猫粮榜
def mlb_Bin(group_id: int) -> object:
    Memory_image = Image.new("RGBA", (1280, 720))
    Draw = ImageDraw.Draw(Memory_image)

    SqlCommand = f"Select Distinct [CID],[QQ],[猫粮],[累计] From 'DefaultData' Where [Group]='{group_id}' Order By Cast([猫粮] as Numeric) Desc Limit 10"
    c = sql.cursor()
    cursor = c.execute(SqlCommand)
    if cursor:
        # --画头像
        i = n = x = 0
        for row in cursor:
            # if x == 10: break
            user_id = row[1]
            User_Bin = Image.open(load_image_data(user_id)).resize((100, 100))
            Memory_image.paste(User_Bin, (60 + 598 * n, 100 + 123 * i))
            i += 1
            x += 1
            if i == 5:
                n = 1
                i = 0
        # --画头像
        image_Bin = Image.open(Image_mlb_DIR)  # 空样板
        Memory_image.paste(image_Bin, mask=image_Bin)  # 主样板
        i = n = x = j = 0
        xy = [92, 215, 337, 461, 582]

        cursor = c.execute(SqlCommand)
        # --画文本
        for row in cursor:
            n += 1
            cid = str(row[0])
            ml = str(row[2])
            lj = str(row[3])
            fontA = ImageFont.truetype(TTF_DD_DIR, 35)
            fontB = ImageFont.truetype(TTF_DD_DIR, 50)
            Draw.text((160 + 600 * j, xy[x] + 10), f'CID:{cid}', font=fontA, fill=(255, 161, 109))
            Draw.text((160 + 600 * j, xy[x] + 60), f'{ml} [-] {lj}', font=fontA, fill=(192, 202, 0))
            Draw.text((580 + 600 * j - Draw.textlength(str(n), font=fontA) / 2, xy[x] + 25), str(n), font=fontB,fill=(255,226,101))
            x += 1
            if x == 5:
                j = 1
                x = 0
    else:
        return 0
    buffer = io.BytesIO()
    Memory_image.save(buffer, format="png")
    base64_data = base64.b64encode(buffer.getvalue())
    return base64_data.decode()

def sese(Data:list) -> object:
    usernick = Data.get('nickname')
    user_id = Data.get('user_id')
    list = []
    i = n = j = 0
    x = 147
    #空白模板
    image = Image.new('RGB', (1342, 950),(255, 255, 255))
    #图片模板
    image_Bin = Image.open(Image_Se_DIR)
    #发送人头像
    User_Bin = Image.open(load_image_data(user_id))
    image.paste(User_Bin.resize((211, 210)), (31, 7))
    # 创建一个可以在图像上绘图的对象
    Draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(TTF_DD_DIR, 35)
    for a in range(10):
        i+=1
        RED = random.randint(0, 255)
        GREEN = random.randint(0, 255)
        BLUE = random.randint(0, 255)
        #画RGB颜色条
        y0 = 26 + n
        y1 = 288 + n
        r_y1 = 256 + x * j
        g_y1 = 289 + x * j
        b_y1 = 322 + x * j
        j_y1 = 258 + x * j
        Draw.rectangle([(y0, r_y1), (y0 + RED, r_y1 + 8)], fill='red')
        Draw.rectangle([(y0, g_y1), (y0 + GREEN, g_y1 + 8)], fill='green')
        Draw.rectangle([(y0, b_y1), (y0 + BLUE, b_y1 + 8)], fill='blue')
        #画纯色矩形
        Draw.rectangle([(y1, j_y1), (y1 + 180, j_y1 + 73)], fill=(RED, GREEN, BLUE))
        #加入RGB列表
        list.append('#{:02x}{:02x}{:02x}'.format(RED, GREEN, BLUE))
        #计数调整
        j+= 1
        if i == 5:
            n = 680
            j = 0
    #样板叠加
    image.paste(image_Bin, mask=image_Bin)
    i = n = j = 0
    x = 147
    for a in range(10):
        i+=1
        Draw.text((460 + n, 270 + x * j), list[a], font=font, fill=(130,147,72))
        j+= 1
        if i == 5:
            n = 684
            j = 0
    #发送人昵称
    font = ImageFont.truetype(TTF_DD_DIR, 85)
    Draw.text((259, 50), f'{usernick}', font=font, fill=(45, 220, 142))
    buffer = io.BytesIO()
    image.save(buffer, format="png")
    base64_data = base64.b64encode(buffer.getvalue())
    return base64_data.decode()