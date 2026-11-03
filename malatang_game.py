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

class Life:
    """
    残機数を管理・表示するクラス
    """
    def __init__(self, num :int):
        self.num = num  # 残機数を保存
        self.image = pg.Surface((40, 40)) #40×40の空のSurfaceを生成
        
         # ハートの形を作る座標を計算
        points = [(16*math.sin(t/100)**3 +20,
        -(13*math.cos(t/100)-5*math.cos(2*t/100)-2*math.cos(3*t/100)-math.cos(4*t/100)) +20
        ) for t in range(0, 628) ]
        
         # 青色のハートを描画
        pg.draw.polygon(self.image, (0, 0, 255), points)
        self.image.set_colorkey((0, 0, 0))


    def update(self, screen: pg.Surface):
            """
            残基数に応じたハートを画面左上に表示する
            引数 screen：ゲーム画面のSurface
            戻り値：なし
            """
            for i in range(self.num):  # 残基数の分だけ繰り返す
                # ハートを画面の左上から50ピクセル間隔で描画
                screen.blit(self.image, (30+50*i, 70))

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("麻辣湯アルバイター☆彡")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    life = Life(3)   # 初期残機数を3に設定
    clock = pg.time.Clock()
    

    while True: 

        for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
            if event.type == pg.QUIT:
                return 0


        screen.blit(bg_img, [0, 0]) # 画面表示

        life.update(screen)  #　残機数分のハートを表示

        pg.display.update() # 画面更新
        clock.tick(50)

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
