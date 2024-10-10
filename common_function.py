import json

import datetime


# 現行common_function.pyから流用(使用モジュールのみ抜粋)

def getJST():
    t_delta = datetime.timedelta(hours=9)  # 9時間
    JST = datetime.timezone(t_delta, 'JST')  # UTCから9時間差の「JST」タイムゾーン
    return JST
