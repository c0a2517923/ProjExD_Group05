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
                 "きくらげ":"fig/kikurage.png",
                 "サーカス団子":"fig/sakasudango.png"}
    
    def __init__(self, name:str, xy:tuple[int,int]):
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
        # 商品画像のサイズを小さく
        self.image = pg.transform.scale(self.image,(140, 100))
        # 商品画像のRectを取得する
        self.rect = self.image.get_rect()
        # 商品の表示位置を設定
        self.rect.center = xy

        # 商品が選択されているか
        self.selected = False

    def select(self, select_list: list[str]):
        """
        商品を選択してselect_listに商品を追加する
        引数 select_list:
        プレイヤーが選択した商品を保存するリスト
        """
        #まだ選択されていない場合
        if not self.selected:
            select_list.append(self.name)
            self.selected = True
            print(f"{self.name}を選択しました")

        # 押した商品だけ解除する
        else:
            select_list.remove(self.name)
            self.selected = False
            print(f"{self.name}の選択を解除しました")

            # 動作確認用
            print(f"現在の選択{select_list}") 

    def reset(self):
        """
        商品の選択状態を解除する
        """
        self.selected = False

# 注文内容の正誤判定
def check_order(order_list: list[str], select_list: list[str]) -> bool:
    """
    お客さんの注文内容とプレイヤーが選択した商品を比較
    完全一致：True
    不一致：False
    引数1 order_list：お客さんが注文した具材のリスト
    引数2 select_list：プレイヤーが選択した具材のリスト
    """
    # 選んだ順番は関係ない。sortedで並び替えて比較
    return sorted(order_list) == sorted(select_list)

# 商品の選択状態をリセットする関数
def reset_goods(goods: pg.sprite.Group, select_list: list[str]):
    """
    選択した商品の情報をすべてリセットする
    引数1 goods： 商品を管理しているGroup
    引数2 select_list：選択した商品を保存しているリスト
    """
    #選択した商品リストを空にする
    select_list.clear()

    # 全商品のselectedをFalseに戻す
    for good in goods:
        good.reset()

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("★麻辣湯★")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    clock = pg.time.Clock()

    # 商品の作成
    # 商品棚に商品を追加 引数(位置)を商品関数に渡す
    goods_list = [
        Goods("春雨", (150, 430)),
        Goods("青梗菜", (350, 430)),
        Goods("豚肉", (550, 430)),
        Goods("きくらげ", (750, 430)),
        Goods("サーカス団子", (950, 430))
    ]

    # 商品をまとめて管理するGroup
    goods = pg.sprite.Group(goods_list)

    # プレイヤーが選択した商品
    select_list = []

    # Customer担当と統合したら削除し、Customer側のorder_listを使用する
    # 数字キーと商品の対応
    key_dic = {pg.K_1: 0, pg.K_2: 1, pg.K_3: 2, pg.K_4: 3, pg.K_5: 4}

    while True: 

        for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
            if event.type == pg.QUIT:
                return 0
            
            # 数字キーによる商品選択
            if event.type == pg.KEYDOWN:
                # 1～5キーが押された場合、対応する商品番号を取得
                if event.key in key_dic:
                    index = key_dic[event.key]
                    # 商品を選択
                    goods_list[index].select(select_list)

                # ENTERキーで注文内容を判定
                if event.key == pg.K_RETURN:
                    # 注文と選択内容を比較
                    result = check_order(order_list, select_list)

                    # 動作確認用
                    print(f"注文：{order_list}")
                    print(f"選択：{select_list}")
                    print(f"判定：{result}")

                    if result:
                        print("注文成功！")
                    else:
                        print("注文失敗")

                    # 判定後に商品選択をリセット
                    reset_goods(goods, select_list)

            # マウスクリックによる商品選択
            if event.type == pg.MOUSEBUTTONDOWN:
                # 左クリックの場合
                if event.button == 1:
                    # クリックした位置を取得
                    mouse_pos = event.pos

                    # 全商品を確認
                    for good in goods:
                        # 商品画像の範囲をクリックした場合、商品を選択
                        if good.rect.collidepoint(mouse_pos):
                            good.select(select_list)

        screen.blit(bg_img, [0, 0]) # 画面表示
        
        # 商品をまとめて表示
        goods.draw(screen)

        # 選択した商品が分かるように枠を表示
        for good in goods:
            if good.selected:
                # 選択された商品の周囲に枠を表示
                pg.draw.rect(screen, (255, 0, 0), good.rect, 4)

        pg.display.update() # 画面更新
        clock.tick(50)

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
