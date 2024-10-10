# start-bilibili-live-obs-script
在仅使用obs推流到B站时，通过此脚本，省去在网页上点击“开始直播”的操作

![图片](https://github.com/user-attachments/assets/9e42515c-fb72-4716-95f2-567b3cd06c65)

使用方法：
1. 打开obs -> 工具 -> 脚本
2. 在“python设置”中设置python路径（obs中添加python脚本需要本地具备python环境）
3. 在本地python环境中安装必要的库：`pip install requests`
4. 添加脚本
5. 配置项：
    * room id: 房间号
    * area id: 分区ID，详见 [B站直播分区列表](https://api.live.bilibili.com/room/v1/Area/getList?show_pinyin=1)
    * cookie: 网页cookie。访问 [B站直播个人首页](https://link.bilibili.com) （若未登录则登录一下），F12打开devtools，切换到“网络”栏，随便选择一个请求（若没有则在开启devtools的情况下刷新一下页面），复制“请求标头”中的cookie字段粘贴到文本框，确认一下cookie中包含SESSDATA和bili_jct ![图片](https://github.com/user-attachments/assets/3bc9ff52-e723-4e7f-93ca-e9b4cff6f18d)
6. 点击`start live & pushing`则直播间变为直播状态，且obs开始推流（注：会根据接口返回的数据自动设置obs的推流地址和推流码）
7. 点击`stop live & pushing`则直播间变为直播结束状态，且obs停止推流
