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

class Customer(pg.sprite.Sprite):
    """
    お客さんに関するクラス
    """
    def __init__(self, *groups):
        """
        お客さん画像Surfaceを生成する
        """
        super().__init__(*groups)
        self.img = pg.transform.scale(pg.image.load(f"fig/koukaton.png"),(500,500))
        self.rct = self.img.get_rect()
        self.rct.center = (WIDTH/2,HEIGHT/2)
        self.order_list = []

    def decide_order(self):
        pass

    def order(self):
        pass
    
    def speech(self):
        pass

class SpeechBubble():
    """
    ふきだしに関するクラス
    """
    def __init__(self):
        """
        ふきだしSurfaceを生成する
        text : 定型文
        """
        self.font = font
        self.text = "をください！"
        pass

    def draw(self, screen:pg.surface, order:list):
        """
        ふきだしを描画する
        order : お客さんの注文リスト
        """
        self.order = order

        pass

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("★麻辣湯★")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更
    bird = Customer()

    clock = pg.time.Clock()

    while True: 

        for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
            if event.type == pg.QUIT:
                return 0


        screen.blit(bg_img, [0, 0]) # 画面表示

        
        screen.blit(bird.img,bird.rct)

        pg.display.update() # 画面更新
        clock.tick(50)

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
