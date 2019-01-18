# django-channels2-tutorial + worker/background task example

這個專案修改自沈弘哲的django-channels2-tutorial 教學
主要是加上worker/background taskf 的例子

## 用法
簡單的說就是啟動docker-compose，然後到app container 裡面去啟動worker 程序。
```sh
docker-compose up -d
docker-compose run app bash # 進入app container

python manage.py runworker task-test # 啟動worker 程序
2019-01-18 03:51:35,927 - INFO - runworker - Running worker for channels ['task-test']
```
## 說明
1. 開啟chat-room 輸入一些東西，可以在終端機中看到輸出。
2. TestConsumer 內有二個方法，可以看到是藉由`type`來對應的。
3. 可以對照著channels_redis的[原始碼](https://github.com/django/channels_redis)一起來看。test2 會印出`self.channel_layer.__dict__`，這是`class RedisChannelLayer(BaseChannelLayer):`裡的資訊，往下可看到` async def send(self, channel, message):`這是執行`send` 方法上的參數的名字。
4. `"task-test"` 其實是channel的名稱，message參數其實又稱為event, 而且被要求是dict。這些資訊可以在channels_redis 的