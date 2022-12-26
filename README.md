# Logger
* 使用裝飾器將常用的 logging module 包裝後更便利使用
* 紀錄 function 開始與結束時間，並使用 try except 記錄報錯資訊
* 裝飾器使用 generator，因此 function 中使用 yield 搭配可將訊息紀錄下來

## 使用方式：
```python=
# 實例化
logger=Logger(logger_name＝'just for test')

＃ 使用裝飾器 @logger.catch 
@logger.catch
def person_age(age):
    for i in range(age):
        if i==18:
            ＃使用 yield 可將訊息紀錄下來
            yield f'我正年輕, 我才 {i} 歲'
            
        elif i==30:
            yield f'我正努力賺錢, 我已經 {i} 歲'
            
        elif i==40:
            yield f'我體力大不如前, 原來我已經 {i} 歲'
            
        elif i==55:
            yield f'身體變差了, 我已經 {i} 歲, 快退休了!'
            
    return i
    
person_age(45)
```
## log紀錄:
```
2022-12-26 22:28:31 - INFO - [person_age] start...
2022-12-26 22:28:31 - INFO - [person_age] msg : 我正年輕, 我才 18 歲 
2022-12-26 22:28:31 - INFO - [person_age] msg : 我正再努力賺錢, 我已經 30 歲 
2022-12-26 22:28:31 - INFO - [person_age] msg : 我體力大不如前, 原來我已經 40 歲 
2022-12-26 22:28:31 - INFO - [person_age] end.
```
