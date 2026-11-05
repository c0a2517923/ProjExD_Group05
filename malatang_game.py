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

class Score:
    """
    提供した麻辣湯の数によってスコアがもらえるクラス
    正しく麻辣湯を提供できたら +1000点
    
    """
    def __init__(self):
        self.font = pg.font.Font(None, 50)  # フォントの指定
        self.color = (255, 255, 255)  # 文字の色の指定
        self.value = 0  # 初期スコア
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)  # スコア表示設定
        self.rect = self.image.get_rect()  # imageのrectを取得
        self.rect.left = 30  # 文字の左上のx座標
        self.rect.top = 150  # 文字の左上のy座標

    def update(self, screen: pg.Surface):
        """
        スコアを画面左上に表示する
        引数 screen：ゲーム画面のSurface
        戻り値：なし
        """
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("★麻辣湯★")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    score = Score()

    clock = pg.time.Clock()

    
    while True: 

        for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
            if event.type == pg.QUIT:
                return 0


        screen.blit(bg_img, [0, 0]) # 画面表示

        score.update(screen)

        pg.display.update() # 画面更新
        clock.tick(50)

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
