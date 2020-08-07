# -*- coding: utf-8 -*-
import numpy as np
import wave
import struct

# 共通定数
f0 = 13333 # 音声の周波数
fs = 44100 # サンプリング周波数(周波数の2倍以上)
A = 1     # 振幅

#--------------------
# marker.wav作成
#--------------------
sec = 0.2

y = []

# サンプリング点数分繰り返す
for n in np.arange(int(fs * sec)): 
    s = A * np.sin(2 * np.pi * f0 * n / fs)
    y.append(s)

# 16bit(65536値)符号付き整数に変換
yint = [int(x * 32767.0) for x in y]

# バイナリ化
biy = struct.pack("h" * len(yint), *yint)

# wavファイル化
wav = wave.Wave_write("wav/marker.wav")
pr = (1, 2, fs, len(biy), 'NONE', 'not compressed')
wav.setparams(pr)
wav.writeframes(biy)
wav.close()

#--------------------
# zero.wav作成
#--------------------
sec = 0.8

y = []

# サンプリング点数分繰り返す
for n in np.arange(int(fs * sec)):
    s = A * np.sin(2 * np.pi * f0 * n / fs)
    y.append(s)

# 16bit(65536値)符号付き整数に変換
yint = [int(x * 32767.0) for x in y]

# バイナリ化
biy = struct.pack("h" * len(yint), *yint)

# wavファイル化
wav = wave.Wave_write("wav/zero.wav")
pr = (1, 2, fs, len(biy), 'NONE', 'not compressed')
wav.setparams(pr)
wav.writeframes(biy)
wav.close()

#--------------------
# one.wav作成
#--------------------
sec = 0.5

y = []

# サンプリング点数分繰り返す
for n in np.arange(int(fs * sec)):
    s = A * np.sin(2 * np.pi * f0 * n / fs)
    y.append(s)

# 16bit(65536値)符号付き整数に変換
yint = [int(x * 32767.0) for x in y]

# バイナリ化
biy = struct.pack("h" * len(yint), *yint)

# wavファイル化
wav = wave.Wave_write("wav/one.wav")
pr = (1, 2, fs, len(biy), 'NONE', 'not compressed')
wav.setparams(pr)
wav.writeframes(biy)
wav.close()
