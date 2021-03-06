# teelebot
Python实现的Telegram Bot机器人框架







## 说明 ##

本项目是基于Python和Telegram Bot API实现的Telegram Bot框架，实现了基本的插件系统。目前自带插件有以下几个：

* Menu  -   自动生成的插件菜单
*   Chat  -   调用 [青云客聊天机器人API](http://api.qingyunke.com/) 实现的对话功能
*  Hello  -   Hello World插件例子
*  Firefoxmoniter -  调用 [Firefox Moniter](https://monitor.firefox.com/) ,搜索自2007年起的公开数据外泄事件当中是否包含你的电子邮件
*  Bing - 调用第三方Bing壁纸接口 [bing](https://github.com/xCss/bing) 获取每日必应壁纸
*  ID - 获取你的用户ID
*  Top - 调用top命令查看服务器状态
*  Translate - 调用 [有道翻译](http://fanyi.youdao.com/)API 对文字进行翻译
*  Guard - 广告过滤， 使用 DFA 对消息进行过滤；入群验证码人机检测
*  Admin - 群管插件，管理员可通过指令对群进行管理(踢人、禁言等)



本项目在 Python 3.5 及以上版本测试通过。









## Telegram Bot API封装情况

### 已实现 47 + 0.5 * 3 个 ###

**Getting updates**

* getUpdates

**Available methods**

* getMe
* getFile & downloadFile
* sendMessage
* sendPhoto
* sendDocument
* kickChatMember
* unbanChatMember
* leaveChat
* getChat
* getChatAdministrators
* getChatMembersCount
* getChatMember
* setChatPermissions
* restrictChatMember
* promoteChatMember
* pinChatMessage
* unpinChatMessage
* sendVoice
* sendAnimation
* sendAudio
* sendVideo
* sendVideoNote
* getUserProfilePhotos
* setChatTitle
* setChatDescription
* setChatPhoto
* deleteChatPhoto
* sendLocation
* sendContact
* sendVenue
* sendChatAction
* forwardMessage
* kickChatMember
* unbanChatMember
* restrictChatMember
* setChatAdministratorCustomTitle
* setChatPermissions
* exportChatInviteLink
* setChatStickerSet
* deleteChatStickerSet
* sendMediaGroup（undone）
* answerCallbackQuery

**Updating messages**

* editMessageText
* editMessageCaption
* editMessageMedia  (undone)
* editMessageReplyMarkup
* stopPoll
* deleteMessage

**Inline mode**

* answerInlineQuery(undone)



目标是封装官方所有的接口







## Demo ##

* Telegram群组： [teelebot体验群](http://t.me/isteelebot)（t.me/isteelebot）









## 环境要求 ##

### Python版本

teelebot 只支持 Python3.x，不支持Python2.x。





## 使用 ##

#### 一、源码运行 ####

1.克隆或点击下载本项目到本地，保证本机安装有`Python3.x`版本和包`requests`；



2.`config.cfg` 配置文件

配置文件格式:

```python
[config]
key=your key
root=your user id
debug=False
timeout=60
plugin_dir=your plugin dir   //[Optional]
```

* Linux

在 `/root` 目录下创建文件夹 `.teelebot` ,并在其内新建配置文件 `config.cfg` ,按照上面的格式填写配置文件

* Windows

在 `C:\Users\<username>`  目录下创建文件夹 `.teelebot` ,并在其内新建配置文件 `config.cfg` ,按照上面的格式填写配置文件

* 指定配置文件

Linux 和 Windows 都可在命令行通过参数手动指定配置文件路径，命令格式：

```
python -m teelebot -c/-C <configure file path>
```

路径必须为绝对路径。



3.运行

终端下进入teelebot文件夹所在目录。

* 对于使用程序配置文件默认路径的：

  输入`python -m teelebot` 回车,正常情况下你应该能看见屏幕提示机器人开始运行。

* 对于命令行手动指定配置文件路径的：

  输入`python -m teelebot -c/-C <configure file path>` 回车,正常情况下你应该能看见屏幕提示机器人开始运行。



#### 二、Pip安装运行

##### 安装 #####

* 确保本机Python环境拥有pip包管理工具。

* 在本项目Releases页面下载包文件。

* 本机命令行进入包文件所在目录，执行：

  ```
  pip install <teelebot package file name>
  
  or
  
  pip3 install <teelebot package file name>
  ```

由于API未封装完毕，暂未上传至 `PyPI` ,故不能在线安装，望谅解。

##### 运行 #####

任意路径打开终端，输入以下命令：

- 对于使用程序配置文件默认路径的：

  输入`teelebot` 回车,正常情况下你应该能看见屏幕提示机器人开始运行。

- 对于命令行手动指定配置文件路径的：

  输入`teelebot -c/-C <configure file path>` 回车,正常情况下你应该能看见屏幕提示机器人开始运行。





可配合`supervisor`使用。





## 插件开发指南 (以 Hello 插件为例) BETA 0.5

#### 一、插件结构

一个完整的 `teelebot` 插件应当呈现为一个文件夹，即一个Python包，以 `Hello` 插件为例，最基本的目录结构如下：

```Python
Hello/
  ./__init__.py
  ./Hello.py
  ./Hello_screenshot.png
  ./readme.md
```

#### 二、规则

##### 命名

在构建teelebot插件中应当遵守的规则是：每个插件目录下应当存在一个与插件同名的`.py` 文件，比如插件 `Hello ` 中的 `Hello.py` 文件，并且此文件中必须存在作为插件入口的同名函数，以插件 `Hello` 为例：

```python
#file Hello/Hello.py

# -*- coding:utf-8 -*-
from teelebot import Bot

def Hello(message):
    pass
```

函数 `Hello()` 即为插件的入口函数，参数 `message` 用于接收消息数据。

##### 资源路径

若想在插件内进行打开文件等操作，需要使用的路径应当遵循以下的格式：

```python
bot.plugin_dir + "<plugin dir name>/<resource address>"
```

#### 三、自定义触发指令

插件的触发指令可不同于插件名，允许自定义。以插件 `Hello` 为例，触发指令为 `/helloworld` 而不是 `Hello`。

修改插件目录下的 `__init__.py` 文件设置触发指令：

```python
#file Hello/__init__.py

#/helloworld
#Hello World插件例子
```

第一行为触发指令，默认以 `/`  作为前缀；第二行为插件简介。







## 联系我 ##

* Email：hi#ojoll.com ( # == @ )
* Blog:    [北及](https://ojoll.com)
* Telegram群组：[teelebot体验群](http://t.me/isteelebot)（t.me/isteelebot）
* 其他：本repo 的 Issue







## 更新历史 ##

#### 2020-6-6

* v1.4.2 : 重构插件 Guard 部分代码，新增消息自毁,修复 captcha 可绕过验证的bug；修复 Admin 插件禁言时间显示bug；修复重构后插件 Guard 删除所有用户消息的 bug 

#### 2020-6-5

* v1.4.1 : 修复部分接口bug，完善 Admin 插件
* v1.4.0 : 修复 Guard 插件 captcha 验证码手动刷新无回调的bug；新增插件 Admin

#### 2020-6-4

* v1.3.9 : Guard 插件新增功能 captcha ，对入群用户进行人机检测，文案调整；插件 Menu 新增消息定时自毁

* v1.3.8 : 修复获取 callback_query 消息时无法获取触发 query 的用户的信息的bug

* v1.3.7 :  bug修复，消息轮询增加对部分Media类消息(photo、sticker、video、audio、document)的识别

#### 2020-6-2

* v1.3.6 : 新增 Updating messages 类型函数接口；bug修复

#### 2020-6-1

* v1.3.5 : 文件发送类函数支持直接发送 Bytes 流，完善 send 类函数返回值

#### 2020-5-30

* v1.3.4 : 修复插件 Guard 若干 bug；细节优化

* v1.3.3 : 插件 Guard 新增功能 guardadd,可通过Bot添加过滤关键词；代码优化

#### 2020-5-29

* v1.3.2 : 修复 kickMember 和 restrictChatMember 函数 until_date 时间问题，Guard 插件细节优化

* v1.3.1 : 修复 Firefoxiremoniter 插件 email 地址bug，插件Guard部分细节优化

#### 2020-5-28

* v1.3.0 : 新增插件 Guard，消息轮询增加对 new_chat_member 和 left_chat_participant 类型消息的识别
* v1.2.9 : 修复插件 Firefoxiremoniter 和 Top 的bug，新增插件 Translate

#### 2020-5-26

* v1.2.8 : 完善 getUpdates 函数，消息轮询增加对 callback_query 类型消息的识别，README增加插件开发指南(BETA 0.5)

* v1.2.7 : 为消息发送类函数添加 reply_markup 按钮功能，新增接口函数answerCallbackQuery

* v1.2.6 : 为消息发送类函数添加 reply_to_message_id 功能；插件适配reply_to_message_id 

#### 2020-3-22

* v1.2.5 : 修复debug模式控制失效的bug，部分插件的优化，增加每个插件的功能演示截图

* v1.2.4 : 增加插件 Top，bug修复

#### 2020-3-15

* v1.2.3 : 对Inline mode的初步支持，bug修复

* v1.2.2 : 封装2个接口，修复插件 Bing

#### 2020-3-14

* v1.2.1 : 新增插件 ID

* v1.2.0 : 封装8.5个接口，添加测试用例

#### 2019-8-25 ####

* v1.1.18 : 代码优化，Bug修复，一大波媒体相关接口的封装；Chat聊天插件增加机器人输入状态显示(还有小彩蛋)

#### 2019-8-24 ####

* v1.1.9 : 项目代码结构优化，Bug修复，第一个 Release发布(已删除)

#### 2019-8-23 ####

* v1.1.8 : 项目包化；支持自定义插件文件夹路径；配置文件存储路径优化，支持命令行输入

* v1.1.3 : 项目从TeeleBot更名为teelebot，文件路径和代码结构优化

#### 2019-8-22 ####

* v1.1.2 : 优化配置文件存储方式

#### 2019-8-21 ####

* v1.1.1 : 优化部分函数代码，添加插件Bing

* v1.1.0 : 一大波群管理相关接口的封装，代码优化

#### 2019-8-17 ####

* v1.0.8 : 修复程序编码问题，添加插件Firefoxmoniter

#### 2019-8-15 ####

* v1.0.7 : 重构部分代码，添加下载图片的功能

#### 2019-8-14 ####

* v1.0.1 : 修复了当接收数据为None时的错误
* v1.0.0 : 基本实现

