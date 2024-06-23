# 系统推荐
Ubuntu 22 or 24

# 参数说明
- --file, 监控对象所在文件路径
- --concurrent, 请求的最大并发数, 不填默认为 10
- --token, telegram bot 的 token（BotFather获取）
- --chat_id, telegram 发送对象的 id（Get_ID_bot获取）

# 依赖
python >= 3.7

pip3 install requests

# 操作说明
## 上传文件
将 check.py 上传至服务器 /data 目录下（没有 /data 目录则新建）
## 整理监控对象
将需要监控的 ip:port 整理到 /data 下的一个文件，如 /data/targets.txt，一个条目一行，支持动态域名(套CDN不可用)

格式如下：
```text
google.com:10000
youtube.com:20000
1.1.1.1:30000
2.2.2.2:40000
3.3.3.3:50000
```
## 新建 cronjob
cronjob 加入定时任务，定时策略自行决定，示例为每十分钟执行一次

crontab -e

```shell
*/10 * * * * python3 /data/check.py --file /data/targets.txt --concurrent 10 --token xxxxx --id xxxxx >> /data/check.log
```
### 如何获取 id？

浏览器中输入

```bash
https://api.telegram.org/bot{token}/getUpdates
```

把`{token}`替换成你自己的bot tonke

显示：{
“ok”: true,
“result”: []
}
如果显示error，说明有错误

在这其中找到 "chat":{"id":-10000000000,"title":"xxxx",

### 如何检测 id是否正确？

```bash
curl -X POST "https://api.telegram.org/botXXX:YYYY/sendMessage" -d "chat_id=-zzzzzzzzzz&text=my sample text"
```

`XXX:YYYY` 替换成你的 bot tonke

`-zzzzzzzzzz` 替换成刚刚获取到的id  注意是带`-`号


#### 可将 python3 替换为其绝对路径 `which python3` 查看

### my

```bash
*/10 * * * * /usr/bin/python3 /serverslist/xx/check.py --file /serverslist/xx/xxtargets.txt --concurrent 10 --token telegrambottoken --id -chatid >> /serverslist/xx/xx.log
```

`/serverslist/xx/check.py` `/serverslist/xx/xxtargets.txt` `/serverslist/xx/xx.log`
