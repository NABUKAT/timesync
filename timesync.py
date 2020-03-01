# -*- coding: utf-8 -*-
import sys
import time
import datetime
import math
import wave 
import pyaudio
import os

# スクリプトパス
script_path = os.path.dirname(os.path.abspath(__file__))

# 15分間電波送信する
def sendwav_15m():
    timer_mgmt(maxmin=15)

# タイマー管理
def timer_mgmt(maxmin=15):
    cnt = 0
    nowsec = 0
    while True:
        now = datetime.datetime.now()
        new_nowsec = now.second
        if nowsec != new_nowsec:
            if new_nowsec == 0:
                print("", flush=True)
                print(now.strftime('%Y/%m/%d %H:%M '), flush=True, end="")
                cnt = cnt + 1
                if cnt > maxmin:
                    break
            protocol_mgmt(now, new_nowsec)
            nowsec = new_nowsec
        time.sleep(0.01)

# プロトコル管理
def protocol_mgmt(now, t):
    # マーカー
    if t == 0:
        send_wave(2)
    # 分(40m)
    elif t == 1:
        b = math.floor(now.minute / 40)
        send_wave(b)
    # 分(20m)
    elif t == 2:
        b = math.floor((now.minute % 40) / 20)
        send_wave(b)
    # 分(10m)
    elif t == 3:
        b = math.floor((now.minute % 20) / 10)
        send_wave(b)
    # ゼロ
    elif t == 4:
        send_wave(0)
    # 分(8m)
    elif t == 5:
        b = math.floor((now.minute % 10) / 8)
        send_wave(b)
    # 分(4m)
    elif t == 6:
        b = math.floor(((now.minute % 10) % 8) / 4)
        send_wave(b)
    # 分(2m)
    elif t == 7:
        b = math.floor(((now.minute % 10) % 4) / 2)
        send_wave(b)
    # 分(1m)
    elif t == 8:
        b = now.minute % 2
        send_wave(b)
    # ポジションマーカー
    elif t == 9:
        send_wave(3)
    # ゼロ
    elif t == 10:
        send_wave(0)
    # ゼロ
    elif t == 11:
        send_wave(0)
    # 時(20h)
    elif t == 12:
        b = math.floor(now.hour / 20)
        send_wave(b)
    # 時(10h)
    elif t == 13:
        b = math.floor((now.hour % 20) / 10)
        send_wave(b)
    # ゼロ
    elif t == 14:
        send_wave(0)
    # 時(8h)
    elif t == 15:
        b = math.floor((now.hour % 10) / 8)
        send_wave(b)
    # 時(4h)
    elif t == 16:
        b = math.floor(((now.hour % 10) % 8) / 4)
        send_wave(b)
    # 時(2h)
    elif t == 17:
        b = math.floor(((now.hour % 10) % 4) / 2)
        send_wave(b)
    # 時(1h)
    elif t == 18:
        b = now.hour % 2
        send_wave(b)
    # ポジションマーカー
    elif t == 19:
        send_wave(3)
    # ゼロ
    elif t == 20:
        send_wave(0)
    # ゼロ
    elif t == 21:
        send_wave(0)
    # 通算日(200d)
    elif t == 22:
        yd = get_yearday(now)
        b = math.floor(yd / 200)
        send_wave(b)
    # 通算日(100d)
    elif t == 23:
        yd = get_yearday(now)
        b = math.floor((yd % 200) / 100)
        send_wave(b)
    # ゼロ
    elif t == 24:
        send_wave(0)
    # 通算日(80d)
    elif t == 25:
        yd = get_yearday(now)
        b = math.floor((yd % 100) / 80)
        send_wave(b)
    # 通算日(40d)
    elif t == 26:
        yd = get_yearday(now)
        b = math.floor(((yd % 100) % 80) / 40)
        send_wave(b)
    # 通算日(20d)
    elif t == 27:
        yd = get_yearday(now)
        b = math.floor(((yd % 100) % 40) / 20)
        send_wave(b)
    # 通算日(10d)
    elif t == 28:
        yd = get_yearday(now)
        b = math.floor(((yd % 100) % 20) / 10)
        send_wave(b)
    # ポジションマーカー
    elif t == 29:
        send_wave(3)
    # 通算日(8d)
    elif t == 30:
        yd = get_yearday(now)
        b = math.floor((yd % 10) / 8)
        send_wave(b)
    # 通算日(4d)
    elif t == 31:
        yd = get_yearday(now)
        b = math.floor(((yd % 10) % 8) / 4)
        send_wave(b)
    # 通算日(2d)
    elif t == 32:
        yd = get_yearday(now)
        b = math.floor(((yd % 10) % 4) / 2)
        send_wave(b)
    # 通算日(1d)
    elif t == 33:
        yd = get_yearday(now)
        b = yd % 2
        send_wave(b)
    # ゼロ
    elif t == 34:
        send_wave(0)
    # ゼロ
    elif t == 35:
        send_wave(0)
    # パリティ(PA1)
    elif t == 36:
        b = get_parity(now, 1)
        send_wave(b)
    # パリティ(PA2)
    elif t == 37:
        b = get_parity(now, 2)
        send_wave(b)
    # 予備ビット(SU1)
    elif t == 38:
        send_wave(0)
    # ポジションマーカー
    elif t == 39:
        send_wave(3)
    # 予備ビット(SU2)
    elif t == 40:
        send_wave(0)
    # 年(80y)
    elif t == 41:
        b = math.floor((now.year % 100) / 80)
        send_wave(b)
    # 年(40y)
    elif t == 42:
        b = math.floor(((now.year % 100) % 80) / 40)
        send_wave(b)
    # 年(20y)
    elif t == 43:
        b = math.floor(((now.year % 100) % 40) / 20)
        send_wave(b)
    # 年(10y)
    elif t == 44:
        b = math.floor(((now.year % 100) % 20) / 10)
        send_wave(b)
    # 年(8y)
    elif t == 45:
        b = math.floor((now.year % 10) / 8)
        send_wave(b)
    # 年(4y)
    elif t == 46:
        b = math.floor(((now.year % 10) % 8) / 4)
        send_wave(b)
    # 年(2y)
    elif t == 47:
        b = math.floor(((now.year % 10) % 4) / 2)
        send_wave(b)
    # 年(1y)
    elif t == 48:
        b = now.year % 2
        send_wave(b)
    # ポジションマーカー
    elif t == 49:
        send_wave(3)
    # 曜日(4w)
    elif t == 50:
        wd = now.isoweekday() % 7
        b = math.floor(wd / 4)
        send_wave(b)
    # 曜日(2w)
    elif t == 51:
        wd = now.isoweekday() % 7
        b = math.floor((wd % 4) / 2)
        send_wave(b)
    # 曜日(1w)
    elif t == 52:
        wd = now.isoweekday() % 7
        b = wd % 2
        send_wave(b)
    # うるう秒(LS1)
    elif t == 53:
        send_wave(0)
    # うるう秒(LS2)
    elif t == 54:
        send_wave(0)
    # ゼロ
    elif t == 55:
        send_wave(0)
    # ゼロ
    elif t == 56:
        send_wave(0)
    # ゼロ
    elif t == 57:
        send_wave(0)
    # ゼロ
    elif t == 58:
        send_wave(0)
    # ポジションマーカー
    elif t == 59:
        send_wave(3)

# 電波の発信
def send_wave(sig):
    if sig == 0:
        print("0", flush=True, end="")
        play_wav(script_path + "/wav/zero.wav")
    elif sig == 1:
        print("1", flush=True, end="")
        play_wav(script_path + "/wav/one.wav")
    elif sig == 2:
        print("M", flush=True, end="")
        play_wav(script_path + "/wav/marker.wav")
    elif sig == 3:
        print("P", flush=True, end="")
        play_wav(script_path + "/wav/marker.wav")

# 通算日の計算
def get_yearday(now):
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    sumdays = 0
    for i in range(0, now.month-1):
        sumdays = sumdays + days[i]
    sumdays = sumdays + now.day
    if now.month > 2:
        sumdays = sumdays + get_uruu(now)
    return sumdays

# うるう年の計算
def get_uruu(now):
    if now.year % 400 == 0:
        return 1
    elif now.year % 100 == 0:
        return 0
    elif now.year % 4 == 0:
        return 1
    else:
        return 0

# パリティの計算(引数PA1⇒1, PA2⇒2)
def get_parity(now, pa):
    if pa == 1:
        b = math.floor(now.hour / 20)
        b += math.floor((now.hour % 20) / 10)
        b += math.floor((now.hour % 10) / 8)
        b += math.floor(((now.hour % 10) % 8) / 4)
        b += math.floor(((now.hour % 10) % 4) / 2)
        b += now.hour % 2
        ret = b % 2
    elif pa == 2:
        b = math.floor(now.minute / 40)
        b += math.floor((now.minute % 40) / 20)
        b += math.floor((now.minute % 20) / 10)
        b += math.floor((now.minute % 10) / 8)
        b += math.floor(((now.minute % 10) % 8) / 4)
        b += math.floor(((now.minute % 10) % 4) / 2)
        b += now.minute % 2
        ret = b % 2
    return ret

# 電波データ(wav)の再生
def play_wav(filepath):
    chunk = 128
    wf = wave.open(filepath, "r")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    frames_per_buffer=chunk,
                    output=True)
    data = wf.readframes(chunk)
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

if __name__ == '__main__':
    sendwav_15m()