import math
import os
import random
import sys
import time
import pygame as pg


os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ

# ---- クラス ------


# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("★麻辣湯★")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    clock = pg.time.Clock()

    while True: 

        for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
            if event.type == pg.QUIT:
                return 0


        screen.blit(bg_img, [0, 0]) # 画面表示


        pg.display.update() # 画面更新
        clock.tick(50)

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
