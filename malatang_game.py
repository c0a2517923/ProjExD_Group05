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
class Goods(pg.sprite.Sprite):
    """
    商品棚に表示する具材を管理するクラス
    """
    # 商品とパスを対応させる辞書
    goods_dic = {"春雨":"fig/harusame.png",
                 "青梗菜":"fig/tingensai.png",
                 "豚肉":"fig/niku.png",
                 "きくらげ":"きくらげ",
                 "サーカス団子":"fig/sakasudango.png"}
    
    def _init_(self, name:str, xy:tuple[int,int]):
        """
        商品画像を生成する
        引数1 name：商品名
        引数2 xy：商品の表示する位置
        """
        super().__init__()

        # 商品名保存
        self.name = name
        # 商品名に対応する画像を読み込む
        self.image = pg.image.load(__class__.goods_dic[name]).convert_alpha()
        # 商品画像のRectを取得する
        self.rect = self.image.get_rect()
        # 商品の表示位置を設定
        self.rect.center = xy

        # 商品が選択されているか
        self.selected = False
# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("★麻辣湯★")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    clock = pg.time.Clock()


    # 商品をまとめて管理するGroup
    goods = pg.sprite.Group()

    # 商品棚に商品を追加 引数(位置)を商品関数に渡す
    goods.add(
        Goods("春雨",(150,200)),
        Goods("青梗菜", (300, 200)),
        Goods("豚肉", (450, 200)),
        Goods("きくらげ", (600, 200)),
        Goods("サーカス団子", (750, 200))
    )
    # 商品をまとめて表示
    goods.draw(screen)





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
