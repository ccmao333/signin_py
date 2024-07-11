from nonebot import on_message, on_keyword, on_fullmatch, get_bot,on_regex
from datetime import datetime
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot, message
import random

import os
import sys
sys.path.append(os.path.dirname(__file__))

from .cbp import *
from .Sqledit import *
from .Signimg import *


# sign_qd = on_fullmatch('签到', priority=5, block=True)
# sign_dq = on_fullmatch('到签', priority=5, block=True)
# sign_cx = on_fullmatch('查询', priority=5, block=True)
# sign_xc = on_fullmatch('询查', priority=5, block=True)
sign_qd=on_regex('^签到$|^到签$', priority=5, block=True)
sign_cx=on_regex('^查询$|^询查$', priority=5, block=True)
sign_zb = on_fullmatch('早报', priority=5, block=True)
sign_mlb = on_fullmatch('猫粮榜', priority=5, block=True)
sign_zlk = on_regex('^资料卡\[(at:qq=|CQ:at,qq=)[0-9]{5,10}\]|资料卡', priority=5, block=True)
sign_Se = on_fullmatch('色色十连', priority=5, block=True)

#签到
@sign_qd.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    _group_id = event.group_id
    _user_id = event.user_id
    e_message = str(event.message)
    reverse = False
    if not event.sender.card:
        _user_name = event.sender.nickname
    else:
        _user_name = event.sender.card
    #反向指令
    if e_message in '到签':reverse = True
    # 获取数据
    Data = DefaultData(_group_id, _user_id)
    colorHex = LuckColor()
    ml = random.randint(1000, 3000)
    add_signinfrom_data(_group_id, _user_id)  # 签到表新增 防卡BUG
    KFC = vivo50()
    yg = 0
    # CID NEW?
    if Data is None:
        Data = ["New", _group_id, _user_id, "0", "0", "0", "1","1", "0"]
        Data[3] = ml
        Data[5] = colorHex.hex
        if KFC:
            Data[4] = str_int(Data[4], 50)
            yg = 50
        Sql_New(_group_id, _user_id, Data)  # 新数据
    else:
        _user_time = 时间格式转换_年月日(Data[8])
        _system_time = datetime.now().strftime("%Y-%m-%d")
        if _user_time == _system_time:
            _time = 时间格式转换_时分秒(Data[8])
            text = f"[CQ:at,qq={_user_id}]呜,今日签到过啦，明天再来哇~\n今天签到时间:{_time}(跑)"
            #反向指令
            if reverse:text = reverse_text(text)
            await bot.send_group_msg(group_id=_group_id,message=text)
            return
        zml = Data[3]
        Data[3] = str_int(zml, ml)
        Data[5] = colorHex.hex
        Data[6] = 首月判定(Data[6],Data[8])# 月签+ 否则赋1
        Data[7] = str(int(Data[7]) + 1) #累计+
        if KFC:
            Data[4] = str_int(Data[4], 50)
            yg = 50
        Sql_UPDATA(_group_id, _user_id, Data)  # 更新数据
    _image_data = SigninBin(_user_name, ml,yg, Data,reverse,KFC)
    _Message = message.MessageSegment.image(f"base64://{_image_data}")
    await bot.send_group_msg(group_id=_group_id, message=_Message)
#查询
@sign_cx.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id
    e_message = str(event.message)
    reverse = False
    # 获取数据
    Data = DefaultData(group_id, user_id)
    #反向指令
    if e_message in '询查':reverse = True
    # 无CID叉出去
    if Data is None:
        await bot.send_group_msg(group_id=group_id, message='Select猫在表中没有找到对应猫猫,请尝试签到w')
    image_data = sign_cx_Bin(Data,reverse)
    Message = message.MessageSegment.image(f"base64://{image_data}")
    await bot.send_group_msg(group_id=group_id, message=Message)

#早报
@sign_zb.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id
    file = zaob()
    Message = message.MessageSegment.image(file)
    await bot.send_group_msg(group_id=group_id, message=Message)
#资料卡
@sign_zlk.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    msg = str(event.message)
    data = At_re(msg)
    if data: 
        user_id = data
    elif msg == '资料卡':
        user_id = event.user_id
    else:
        print('指令不匹配')
        return
    group_id = event.group_id
    group_info = await bot.get_group_info(group_id=group_id)
    group_name = group_info['group_name']
    Data = await bot.get_group_member_info(group_id=group_id,user_id=user_id,no_cache=False)
    cookie = await bot.get_cookies(domain='qun.qq.com')
    #horData = get_user_honor(user_id, group_id, cookie)
    image_data = user_zlk(Data,group_name)
    Message = message.MessageSegment.image(f"base64://{image_data}")
    await bot.send_group_msg(group_id=group_id, message=Message)
#猫粮榜
@sign_mlb.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    group_id = event.group_id
    image_data = mlb_Bin(group_id)
    Message = message.MessageSegment.image(f"base64://{image_data}")
    await bot.send_group_msg(group_id=group_id, message=Message)
#色色十连
@sign_Se.handle()
async def _(bot: Bot, matcher: Matcher, event: GroupMessageEvent):
    group_id = event.group_id
    user_id = event.user_id
    Data = await bot.get_group_member_info(group_id=group_id,user_id=user_id,no_cache=False)
    image_data = sese(Data)
    Message = message.MessageSegment.image(f"base64://{image_data}")
    await bot.send_group_msg(group_id=group_id, message=Message)