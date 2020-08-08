# -*- coding: utf-8 -*-
import sys
import time
import datetime
import math
import wave 
import pyaudio
import os

# 送信継続時間(分)
xm = 50

# スクリプトパス
script_path = os.path.dirname(os.path.abspath(__file__))

# 音声再生用オブジェクト
filepath_z = script_path + "/wav/zero.wav"
filepath_o = script_path + "/wav/one.wav"
filepath_m = script_path + "/wav/marker.wav"
wf_z = None
wf_o = None
wf_m = None
p = None
stream = None
chunk = 1024

# x分間電波送信する
def sendwav_xm(xm):
    timer_mgmt(maxmin=xm)

# タイマー管理
def timer_mgmt(maxmin=15):
    global wf_z, wf_o, wf_m, stream, p
    wf_z = wave.open(filepath_z, "r")
    wf_o = wave.open(filepath_o, "r")
    wf_m = wave.open(filepath_m, "r")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf_z.getsampwidth()),
                    channels=wf_z.getnchannels(),
                    rate=wf_z.getframerate(),
                    frames_per_buffer=chunk,
                    #output_device_index=4,
                    output=True)
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
        time.sleep(0.001)    
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf_z.close()
    wf_o.close()
    wf_m.close()

# プロトコル管理
nb = 0
def protocol_mgmt(now, t):
    global nb
    # マーカー
    if t == 0:
        send_wave(2)
        nb = math.floor(now.minute / 40)
    # 分(40m)
    elif t == 1:
        send_wave(nb)
        nb = math.floor((now.minute % 40) / 20)
    # 分(20m)
    elif t == 2:
        send_wave(nb)
        nb = math.floor((now.minute % 20) / 10)
    # 分(10m)
    elif t == 3:
        send_wave(nb)
    # ゼロ
    elif t == 4:
        send_wave(0)
        nb = math.floor((now.minute % 10) / 8)
    # 分(8m)
    elif t == 5:
        send_wave(nb)
        nb = math.floor(((now.minute % 10) % 8) / 4)
    # 分(4m)
    elif t == 6:
        send_wave(nb)
        nb = math.floor(((now.minute % 10) % 4) / 2)
    # 分(2m)
    elif t == 7:
        send_wave(nb)
        nb = now.minute % 2
    # 分(1m)
    elif t == 8:
        send_wave(nb)
    # ポジションマーカー
    elif t == 9:
        send_wave(3)
    # ゼロ
    elif t == 10:
        send_wave(0)
    # ゼロ
    elif t == 11:
        send_wave(0)
        nb = math.floor(now.hour / 20)
    # 時(20h)
    elif t == 12:
        send_wave(nb)
        nb = math.floor((now.hour % 20) / 10)
    # 時(10h)
    elif t == 13:
        send_wave(nb)
    # ゼロ
    elif t == 14:
        send_wave(0)
        nb = math.floor((now.hour % 10) / 8)
    # 時(8h)
    elif t == 15:
        send_wave(nb)
        nb = math.floor(((now.hour % 10) % 8) / 4)
    # 時(4h)
    elif t == 16:
        send_wave(nb)
        nb = math.floor(((now.hour % 10) % 4) / 2)
    # 時(2h)
    elif t == 17:
        send_wave(nb)
        nb = now.hour % 2
    # 時(1h)
    elif t == 18:
        send_wave(nb)
    # ポジションマーカー
    elif t == 19:
        send_wave(3)
    # ゼロ
    elif t == 20:
        send_wave(0)
    # ゼロ
    elif t == 21:
        send_wave(0)
        yd = get_yearday(now)
        nb = math.floor(yd / 200)
    # 通算日(200d)
    elif t == 22:
        send_wave(nb)
        yd = get_yearday(now)
        nb = math.floor((yd % 200) / 100)
    # 通算日(100d)
    elif t == 23:
        send_wave(nb)
    # ゼロ
    elif t == 24:
        send_wave(0)
        yd = get_yearday(now)
        nb = math.floor((yd % 100) / 80)
    # 通算日(80d)
    elif t == 25:
        send_wave(nb)
        yd = get_yearday(now)
        nb = math.floor(((yd % 100) % 80) / 40)
    # 通算日(40d)
    elif t == 26:
        send_wave(nb)
        yd = get_yearday(now)
        nb = math.floor(((yd % 100) % 40) / 20)
    # 通算日(20d)
    elif t == 27:
        send_wave(nb)
        yd = get_yearday(now)
        nb = math.floor(((yd % 100) % 20) / 10)
    # 通算日(10d)
    elif t == 28:
        send_wave(nb)
    # ポジションマーカー
    elif t == 29:
        send_wave(3)
        yd = get_yearday(now)
        nb = math.floor((yd % 10) / 8)
    # 通算日(8d)
    elif t == 30:
        send_wave(nb)
        yd = get_yearday(now)
        nb = math.floor(((yd % 10) % 8) / 4)
    # 通算日(4d)
    elif t == 31:
        send_wave(nb)
        yd = get_yearday(now)
        nb = math.floor(((yd % 10) % 4) / 2)
    # 通算日(2d)
    elif t == 32:
        send_wave(nb)
        yd = get_yearday(now)
        nb = yd % 2
    # 通算日(1d)
    elif t == 33:
        send_wave(nb)
    # ゼロ
    elif t == 34:
        send_wave(0)
    # ゼロ
    elif t == 35:
        send_wave(0)
        nb = get_parity(now, 1)
    # パリティ(PA1)
    elif t == 36:
        send_wave(nb)
        nb = get_parity(now, 2)
    # パリティ(PA2)
    elif t == 37:
        send_wave(nb)
    # 予備ビット(SU1)
    elif t == 38:
        send_wave(0)
    # ポジションマーカー
    elif t == 39:
        send_wave(3)
    # 予備ビット(SU2)
    elif t == 40:
        send_wave(0)
        nb = math.floor((now.year % 100) / 80)
    # 年(80y)
    elif t == 41:
        send_wave(nb)
        nb = math.floor(((now.year % 100) % 80) / 40)
    # 年(40y)
    elif t == 42:
        send_wave(nb)
        nb = math.floor(((now.year % 100) % 40) / 20)
    # 年(20y)
    elif t == 43:
        send_wave(nb)
        nb = math.floor(((now.year % 100) % 20) / 10)
    # 年(10y)
    elif t == 44:
        send_wave(nb)
        nb = math.floor((now.year % 10) / 8)
    # 年(8y)
    elif t == 45:
        send_wave(nb)
        nb = math.floor(((now.year % 10) % 8) / 4)
    # 年(4y)
    elif t == 46:
        send_wave(nb)
        nb = math.floor(((now.year % 10) % 4) / 2)
    # 年(2y)
    elif t == 47:
        send_wave(nb)
        nb = now.year % 2
    # 年(1y)
    elif t == 48:
        send_wave(nb)
    # ポジションマーカー
    elif t == 49:
        send_wave(3)
        wd = now.isoweekday() % 7
        nb = math.floor(wd / 4)
    # 曜日(4w)
    elif t == 50:
        send_wave(nb)
        wd = now.isoweekday() % 7
        nb = math.floor((wd % 4) / 2)
    # 曜日(2w)
    elif t == 51:
        send_wave(nb)
        wd = now.isoweekday() % 7
        nb = wd % 2
    # 曜日(1w)
    elif t == 52:
        send_wave(nb)
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
        play_wav(sig)
    elif sig == 1:
        print("1", flush=True, end="")
        play_wav(sig)
    elif sig == 2:
        print("M", flush=True, end="")
        play_wav(sig)
    elif sig == 3:
        print("P", flush=True, end="")
        play_wav(sig)

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
def play_wav(sig):
    global wf_z, wf_o, wf_m, stream, p
    if sig == 0:
        wf_z.setpos(0)
        data = wf_z.readframes(chunk)
        while len(data) > 0:
            stream.write(data)
            data = wf_z.readframes(chunk)
    elif sig == 1:
        wf_o.setpos(0)
        data = wf_o.readframes(chunk)
        while len(data) > 0:
            stream.write(data)
            data = wf_o.readframes(chunk)
    else:
        wf_m.setpos(0)
        data = wf_m.readframes(chunk)
        while len(data) > 0:
            stream.write(data)
            data = wf_m.readframes(chunk)
    

if __name__ == '__main__':
    sendwav_xm(xm)
