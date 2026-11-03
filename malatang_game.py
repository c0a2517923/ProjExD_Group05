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
class Time:
    """
    制限時間と日数を管理するクラス
    """

    def __init__(self):
        """
        引数：time_limit (1日の制限時間、秒)
        戻り値：なし
        """
        self.day = 1 # 現在の日数
        self.time_limit = 60 # 1日の制限時間(秒)
        self.nokori = self.time_limit # 残り時間
        self.owari = False # 時間切れかどうか
        self.font = pg.font.Font("DotGothic16-Regular.ttf", 40) # 表示する文字の設定

    def update(self, dt):
        """
        経過時間に応じて残り時間を減らすメソッド
        引数：dt (前のフレームからの経過時間、秒)
        戻り値：時間切れになった瞬間はTrue、それ以外はFalse
        """
        if self.owari:
            return False

        self.nokori -= dt

        if self.nokori <= 0:
            self.nokori = 0
            self.owari = True
            return True # 時間切れを知らせる
        
        return False

    def next_day(self):
        """
        日数を1日進め、制限時間をリセットするメソッド
        引数：なし
        戻り値：なし
        """
        self.day += 1
        self.nokori = self.time_limit
        self.owari = False

    def get_customer_count(self):
        """
        日数に応じたお客さんの人数を取得するメソッド
        引数：なし
        戻り値：その日に来店するお客さんの人数（int）
        """
        return 3 + (self.day - 1) * 2

    def draw(self, screen):
        """
        現在の日数と残り時間を画面に表示するメソッド
        引数：screen（描画先のSurface）
        戻り値：なし
        """
        day_img = self.font.render(
            f"{self.day}日目", True, (255, 255, 255)
        )

        time_img = self.font.render(
            f"残り時間：{math.ceil(self.remaining)}秒",
            True, (255, 255, 255)
        )

        screen.blit(day_img, (30, 20))
        screen.blit(time_img, (30, 65))
    

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("★麻辣湯★")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    clock = pg.time.Clock()

    timer = Time() # タイマーを作成
    
    font = pg.font.Font("DotGothic16-Regular.ttf", 40)

    while True: 

        dt = clock.tick(50) / 1000 #経過時間を秒に変換

        for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
            if event.type == pg.QUIT:
                return 0

        if event.key == pg.K_RETURN and timer.owari:
            timer.next_day()


        screen.blit(bg_img, [0, 0]) # 画面表示


        pg.display.update() # 画面更新
        clock.tick(50)

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
