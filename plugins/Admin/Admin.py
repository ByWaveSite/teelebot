# -*- coding:utf-8 -*-
'''
creation time: 2020-6-4
last_modify: 2020-6-6
'''

from teelebot import Bot
from teelebot.handler import config
from threading import Timer

config = config()
bot = Bot()
gap = 15

def Admin(message):
    message_id = message["message_id"]
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]
    text = message["text"]
    bot_id = str(bot.getMe()["id"])
    prefix = "admin"

    command = { #命令注册
            "/adminkick": "kick",
            "/admindel": "del",
            "/adminpin": "pin",
            "/adminunpin": "unpin",
            "/adminmute": "mute",
            "/adminunmute": "unmute"
        }
    count = 0
    for c in command.keys():
        if c in str(text):
            count += 1

    if message["chat"]["type"] != "private":
        admins = administrators(chat_id=chat_id)
        admins.append(bot_id)
        if str(config["root"]) not in admins:
            admins.append(str(config["root"])) #root permission

    if message["chat"]["type"] == "private": #判断是否为私人对话
            status = bot.sendChatAction(chat_id, "typing")
            status = bot.sendMessage(chat_id, "抱歉，该指令不支持私人会话!", parse_mode="text", reply_to_message_id=message_id)
            timer = Timer(gap, timer_func_for_del, args=[chat_id, message_id])
            timer.start()
    elif text[1:len(prefix)+1] == prefix and count == 0: #菜单
        status = bot.sendChatAction(chat_id, "typing")
        msg = "<b>===== Admin 插件功能 =====</b>%0A%0A" +\
            "<b>/adminkick</b> - 踢人。格式:以回复要踢用户的消息的形式发送指令%0A" +\
            "<b>/admindel</b> - 删除消息。格式:以回复要删除的消息的形式发送指令%0A" +\
            "<b>/adminpin</b> - 置顶消息。格式:以回复要置顶的消息的形式发送指令%0A" +\
            "<b>/adminunpin</b> - 取消置顶。格式:以回复要取消置顶的消息的形式发送指令%0A" +\
            "<b>/adminmute</b> - 禁言用户。格式:以回复要禁言用户的消息的形式发送指令，指令后跟禁言时间(支持的时间：1m,10m,1h,1d,forever)，以空格作为分隔符%0A" +\
            "<b>/adminunmute</b> - 解除用户禁言。格式:以回复要解除禁言用户的消息的形式发送指令%0A" +\
            "%0A"
        status = bot.sendMessage(chat_id=chat_id, text=msg, parse_mode="HTML", reply_to_message_id=message["message_id"])

        timer = Timer(30, timer_func_for_del, args=[chat_id, status["message_id"]])
        timer.start()

    elif "reply_to_message" in message.keys():
        reply_to_message = message["reply_to_message"]
        target_message_id = reply_to_message["message_id"]
        target_user_id = reply_to_message["from"]["id"]
        target_chat_id = reply_to_message["chat"]["id"]

        if str(user_id) in admins and str(chat_id) == str(target_chat_id):
            if text[1:] == prefix + command["/adminkick"]:
                if str(target_user_id) not in admins:
                    status = bot.kickChatMember(chat_id=chat_id, user_id=target_user_id, until_date=60)
                    status_ = bot.unbanChatMember(chat_id=chat_id, user_id=target_user_id)
                    if status != False:
                        status = bot.sendChatAction(chat_id, "typing")
                        status = bot.sendMessage(chat_id=chat_id, text="已送该用户出群。", parse_mode="text", reply_to_message_id=message["message_id"])
                        timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                        timer.start()
                else:
                    status = bot.sendChatAction(chat_id, "typing")
                    status = bot.sendMessage(chat_id=chat_id, text="抱歉，无权处置该用户!", parse_mode="text", reply_to_message_id=message["message_id"])
                    timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                    timer.start()
            elif text[1:] == prefix + command["/admindel"]:
                status = bot.deleteMessage(chat_id=chat_id, message_id=target_message_id)
                if status == False:
                    status = bot.sendChatAction(chat_id, "typing")
                    status = bot.sendMessage(chat_id=chat_id, text="删除失败!", parse_mode="text", reply_to_message_id=message["message_id"])
                    timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                    timer.start()
            elif text[1:] == prefix + command["/adminpin"]:
                status = bot.pinChatMessage(chat_id=chat_id, message_id=target_message_id)
                if status == False:
                    status = bot.sendChatAction(chat_id, "typing")
                    status = bot.sendMessage(chat_id=chat_id, text="置顶失败!", parse_mode="text", reply_to_message_id=message["message_id"])
                    timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                    timer.start()
            elif text[1:] == prefix + command["/adminunpin"]:
                status = bot.unpinChatMessage(chat_id=chat_id)
                if status == False:
                    status = bot.sendChatAction(chat_id, "typing")
                    status = bot.sendMessage(chat_id=chat_id, text="取消置顶失败!", parse_mode="text", reply_to_message_id=message["message_id"])
                    timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                    timer.start()
            elif text[1:len(prefix + command["/adminmute"])+1] == prefix + command["/adminmute"]:
                if str(target_user_id) not in admins:
                    mute_time = {
                        "1m": 1 * 60,
                        "10m": 1 * 60 * 10,
                        "1h": 1 * 60 * 60,
                        "1d": 1 * 60 * 60 * 24,
                        "forever": 0
                    }
                    permissions = {
                        'can_send_messages':False,
                        'can_send_media_messages':False,
                        'can_send_polls':False,
                        'can_send_other_messages':False,
                        'can_add_web_page_previews':False,
                        'can_change_info':False,
                        'can_invite_users':False,
                        'can_pin_messages':False
                    }
                    if text[1:].split(' ')[1] in mute_time.keys():
                        status = bot.restrictChatMember(chat_id=chat_id, user_id=target_user_id,permissions=permissions, until_date=mute_time[text[1:].split(' ')[1]])
                        if status != False:
                            status = bot.sendChatAction(chat_id, "typing")
                            msg = "<b><a href='tg://user?id=" + str(target_user_id) + "'>" + str(target_user_id) + "</a></b> 已被禁言，持续时间：<b>" + str(text[1:].split(' ')[1]) + "</b>。"
                            status = bot.sendMessage(chat_id=chat_id, text=msg, parse_mode="HTML", reply_to_message_id=message["message_id"])
                            timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                            timer.start()
                        else:
                            status = bot.sendChatAction(chat_id, "typing")
                            msg = "<b><a href='tg://user?id=" + str(target_user_id) + "'>" + str(target_user_id) + "</a></b> 禁言失败!"
                            status = bot.sendMessage(chat_id=chat_id, text=msg, parse_mode="HTML", reply_to_message_id=message["message_id"])
                            timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                            timer.start()
                    else:
                        status = bot.sendChatAction(chat_id, "typing")
                        status = bot.sendMessage(chat_id=chat_id, text="无效指令，请检查格式!", parse_mode="text", reply_to_message_id=message["message_id"])
                        timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                        timer.start()
                else:
                    status = bot.sendChatAction(chat_id, "typing")
                    status = bot.sendMessage(chat_id=chat_id, text="抱歉，无权处置该用户!", parse_mode="text", reply_to_message_id=message["message_id"])
                    timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                    timer.start()
            elif text[1:] == prefix + command["/adminunmute"]:
                if str(target_user_id) not in admins:
                    status = bot.getChat(chat_id=chat_id)
                    permissions = status.get("permissions")
                    status = bot.restrictChatMember(chat_id=chat_id, user_id=target_user_id,permissions=permissions)
                    if status != False:
                        status = bot.sendChatAction(chat_id, "typing")
                        msg = "<b><a href='tg://user?id=" + str(target_user_id) + "'>" + str(target_user_id) + "</a></b> 已被解禁。"
                        status = bot.sendMessage(chat_id=chat_id, text=msg, parse_mode="HTML", reply_to_message_id=message["message_id"])
                        timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                        timer.start()
                else:
                    status = bot.sendChatAction(chat_id, "typing")
                    status = bot.sendMessage(chat_id=chat_id, text="抱歉，无权处置该用户!", parse_mode="text", reply_to_message_id=message["message_id"])
                    timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
                    timer.start()


        else:
            status = bot.sendChatAction(chat_id, "typing")
            status = bot.sendMessage(chat_id=chat_id, text="抱歉，您无权操作!", parse_mode="text", reply_to_message_id=message["message_id"])

            timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
            timer.start()
    else:
        status = bot.sendChatAction(chat_id, "typing")
        status = bot.sendMessage(chat_id=chat_id, text="未指定要操作的对象!", parse_mode="text", reply_to_message_id=message["message_id"])

        timer = Timer(gap, timer_func_for_del, args=[chat_id, status["message_id"]])
        timer.start()

    timer = Timer(gap, timer_func_for_del, args=[chat_id, message_id])
    timer.start()


def administrators(chat_id):
    admins = []
    results = bot.getChatAdministrators(chat_id=chat_id)
    if results != False:
        for result in results:
            if str(result["user"]["is_bot"]) == "False":
                admins.append(str(result["user"]["id"]))
    else:
        admins = False

    return admins

def timer_func_for_del(chat_id, message_id):
    status = bot.deleteMessage(chat_id=chat_id, message_id=message_id)