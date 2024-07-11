import random
from datetime import datetime
import requests
import calendar
import io
import time
import re
from datetime import datetime
# 取随机幸运色
class LuckColor():
    def __init__(self):
        self.rgb = []
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)
        self.rgb = [self.r, self.g, self.b]
        self.hex = "#{:02x}{:02x}{:02x}".format(self.r, self.g, self.b)
        pass

def vivo50()->bool:
   now = datetime.now()
   return now.weekday() == 3

#正则判断是否为AT消息 成功返回被AT的人 失败返回None
def At_re(data:str) -> str:
    import re
    result = re.search('[(at:qq=|CQ:at,qq=)[0-9]{5,10}]', data)
    if result:
        result = re.search('[0-9]{5,10}', result.group(0))
        return result.group(0)
    else:
        return None

# 返回本月的天数
def days() -> int:
    # 获取当前日期
    now = datetime.now()
    # 获取本月的第一天和最后一天
    first_day = now.replace(day=1)
    last_day = first_day.replace(day=calendar.monthrange(now.year, now.month)[1])
    # 计算本月天数
    days_count = (last_day - first_day).days + 1
    return days_count


# 一言
def yiyan():
   url = "https://v1.hitokoto.cn/"
   response = requests.get(url)

   if response.status_code == 200:
       content = response.json()
       return content["hitokoto"]
   else:
       return "请求失败，状态码：" + str(response.status_code)


# 今天星期几
def get_day_of_week():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    today = datetime.today().weekday()
    return days[today]

# 是否在6-23区间 否则返回False
def is_daytime() -> bool:
    return 6 < datetime.now().hour < 23

# 头像数据获取
def load_image_data(user_id:str):
    response = requests.get(f'http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640')
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        return None

# 头像数据获取
def load_image_data_min(user_id:str):
    response = requests.get(f'http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100')
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        return None

# 文本加法
def str_int(t:str, i:int) -> str:
    return str(int(t) + i)

# 时间 只取年月日
def time_format() :
    return datetime.now().strftime("%Y/%m/%d")

#Q等级计算
def user_qqlevel(Level:int) -> list:
    Crown = Level // 64
    Level = Level % 64

    Sun = Level // 16
    Level = Level % 16

    Moon = Level // 4
    Level = Level % 4

    Star = Level
    return [Crown, Sun, Moon, Star]

#时间戳转日期
def inttotime(timestamp:float):
    date_format = "%Y年%m月%d日"
    date = datetime.fromtimestamp(timestamp).strftime(date_format)
    return (date)

#秒 -> 时间
def convert_group_time(long_time):
    result = ""
    YYYY = long_time // 31536000
    if YYYY != 0:
        result += str(YYYY) + "年"
        long_time = long_time % 31536000

    M = long_time // 2592000
    if M != 0:
        result += str(M) + "个月"
        long_time = long_time % 2592000

    D = long_time // 86400
    if D != 0:
        result += str(D) + "天"
        long_time = long_time % 86400

    H = long_time // 3600
    if H != 0:
        result += str(H) + "小时"
        long_time = long_time % 3600

    m = long_time // 60
    if m != 0:
        result += str(m) + "分"

    return result


def infotimestamp() -> int:
    current_timestamp = time.time()
    return(int(current_timestamp))

#取月份
def get_month_name():
   month = datetime.now().month
   return ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")[month - 1]

def 时间格式转换(时间字符串):
   try:
       dt = datetime.strptime(时间字符串, '%Y-%m-%d %H:%M:%S')
   except ValueError:
       dt = datetime.strptime(时间字符串, '%Y-%m-%d')
   return dt.strftime('%Y-%m-%d 00:00:00')

def 时间格式转换_年月日(时间字符串):
   try:
       dt = datetime.strptime(时间字符串, '%Y-%m-%d %H:%M:%S')
   except ValueError:
       dt = datetime.strptime(时间字符串, '%Y-%m-%d')
   return str(dt.strftime('%Y-%m-%d'))

def 时间格式转换_时分秒(时间字符串):
   try:
       dt = datetime.strptime(时间字符串, '%Y-%m-%d %H:%M:%S')
   except ValueError:
       dt = datetime.strptime(时间字符串, '%Y-%m-%d')
   return str(dt.strftime('%H:%M:%S'))

def 首月判定(值, 比对):
    user_time = 时间格式转换(比对)

    当前年 = int(time.strftime('%Y', time.localtime()))  # 获取当前年份
    当前月 = int(time.strftime('%m', time.localtime()))  # 获取当前月份
    参数年 = int(time.strftime('%Y', time.strptime(user_time, '%Y-%m-%d 00:00:00')))  # 获取参数比对年份
    参数月 = int(time.strftime('%m', time.strptime(user_time, '%Y-%m-%d 00:00:00')))  # 获取参数比对月份

    if 当前年 > 参数年 or 当前月 > 参数月:  # 如果当前年份和月份都大于参数年份和月份
        return "1" # 返回值+1的文本型
    else:
        return str(int(值) + 1)  # 否则返回1的文本型


#倒排文本
def reverse_text(text):
   return text[::-1]

# 性别判断返回对应颜色列表  1 male 2 female 3 unknown
def sex_int(sex: str) -> list[int]:
   if sex in ['male']:
       return [(0, 126, 255),(64, 0, 128)]
   elif sex in ['female']:
       return [(240, 98, 146),(128, 128, 255)]
   else:
       return [(255, 161, 109),(192, 202, 0)]


#来自易语言 -**** -> RGBA -> Bin -> RGBint -> RGB
def RGBA_TO_RGB(argb_coilor: int) -> list[int]:
    r = (argb_coilor >> 16) & 0xFF
    g = (argb_coilor >> 8) & 0xFF
    b = argb_coilor & 0xFF
    rgb_color = [r, g, b]
    return rgb_color

#RGB -> RGB[int]
def RGB_TO_int(rgb_color: list[int]) -> int:
    return (rgb_color[0] << 16) + (rgb_color[1] << 8) + rgb_color[2]


# 返回本月1日是星期几
def week():
    today = datetime.today()
    first_day_of_month = today.replace(day=1)
    weekday = first_day_of_month.weekday()
    weekint = int(weekday + 1)
    if weekint == 7: return 1
    return weekint

def zaob():
    url = "http://dwz.2xb.cn/zaob"
    response = requests.get(url)
    Data = eval(response.text)
    return(Data["imageUrl"])

def get_user_honor(uin, gc,cookie):
    '获取群成员荣誉信息'
    url = f"https://qun.qq.com/interactive/userhonor?uin={uin}&gc={gc}&_wv=3&_wwv=128"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36"}
    response = requests.get(url, headers=headers, cookies={'ck': cookie})
    if response.status_code == 200:
        content = response.text
        match = re.search(r'window.__INITIAL_STATE__=(.*);\(function\(\)', content)
        if match:
            data = match.group(1)
            return data
    return None