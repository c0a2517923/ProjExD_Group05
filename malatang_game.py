import math
import os
import random
import sys
import time
import pygame as pg

pg.init()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
WIDTH = 1100  # ゲームウィンドウの幅
HEIGHT = 650  # ゲームウィンドウの高さ

FONT_PATH = f"DotGothic16/DotGothic16-Regular.ttf"  # ドット風フォント

# ---- クラス ------

def gameover(screen: pg.Surface, score: int) -> bool:
    """
    引数: Surface, スコア(int)
    戻り値: なし
    GameOver画面と最終スコアの表示
    """
    # BGMの再生
    pg.mixer.music.stop()  # 現在流れているBGMをストップ
    pg.mixer.music.load("sound/hotaru.mp3")  # ダウンロードした音源ファイルをロード
    pg.mixer.music.play(-1)  # ループ再生

    margin_x = 150
    margin_y = 100

    dialog_w = WIDTH - (margin_x * 2)
    dialog_h = HEIGHT - (margin_y * 2)

    gameover_screen = pg.Surface((dialog_w, dialog_h))
    pg.draw.rect(gameover_screen, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))  # 黒い矩形を作る
    gameover_screen.set_alpha(210)  # 透明度の調節

    fonto = pg.font.Font(None, 80)
    font_small = pg.font.Font(None, 40)
    
    # "Game Over"の白文字を作る (少し上に配置)
    txt = fonto.render("Game Over", True, (255, 255, 255)) 
    txt_rect = txt.get_rect()
    txt_rect.center = dialog_w / 2, dialog_h / 2 - 80  # 中心から上に80ピクセルずらす
    gameover_screen.blit(txt, txt_rect)

    # スコアの白文字を作る (少し下に配置)
    score_txt = fonto.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_txt.get_rect()
    score_rect.center = dialog_w / 2, dialog_h / 2  # 中心から下に50ピクセルずらす
    gameover_screen.blit(score_txt, score_rect)

    # 画面に操作案内を追加
    guide_txt = font_small.render("Press ENTER to Restart / ESC to Exit", True, (200, 200, 200))
    guide_rect = guide_txt.get_rect()
    guide_rect.center = dialog_w / 2, dialog_h / 2 + 80
    gameover_screen.blit(guide_txt, guide_rect)

    screen.blit(gameover_screen, (margin_x, margin_y))  # Screenを表示
    pg.display.update()

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  # ウィンドウの×ボタンが押されたとき
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:  # Enterキーが押されたら True(リスタート)
                    return True
                elif event.key == pg.K_ESCAPE:  # Escキーが押されたら False(終了)
                    return False


class Life:
    """
    残機数を管理・表示するクラス
    """
    def __init__(self, num :int):
        self.num = num  # 残機数を保存
        
         # ハート
        img = pg.image.load("fig/life.png")
        self.image = pg.transform.scale(img, (40, 40))  # 40×40のSurfaceを生成
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
class Customer(pg.sprite.Group):
    """
    お客さんに関するクラス
    """
    def __init__(self, *groups, toppings_dict:dict, spices_dict:dict, max:int):
        """
        お客さん画像Surfaceを生成する
        order : 注文内容を管理するインスタンス
        bowl :どんぶりを管理するインスタンス
        """
        super().__init__(*groups)
        self.img = pg.transform.scale(pg.image.load(f"fig/koukaton.png"),(500,500))
        self.activate = True

        self.order = Order(toppings_dict, spices_dict)
        self.order.set_order(max)

        self.bowl = Bowl(spices_dict=spices_dict)

    def draw(self, screen:pg.surface):
        """
        お客さん、ふきだし、注文内容を表示するメソッドをまとめて呼び出す
        """
        self.draw_customer(screen)  # お客さんの描画
        self.draw_speech_bubble(screen)  # ふきだし＆注文内容の描画

    def draw_customer(self, screen:pg.surface):
        """
        お客さんを描画するメソッド
        """
        my_rct = self.img.get_rect()
        my_rct.center = (WIDTH/2,HEIGHT/2)

        screen.blit(self.img,my_rct)

    def draw_speech_bubble(self, screen:pg.surface):
        """
        ふきだしを描画するメソッド
        """
        #  ふきだし四角
        my_rect = pg.draw.rect(screen, color=(255,255,255), rect=(WIDTH*2/3,10,350,380), width=0, border_radius=10) #ふきだしぬりつぶし
        left = my_rect.left
        top = my_rect.top
        right = my_rect.right
        bottom = my_rect.bottom
        my_color = (0,0,0)
        try_positions = [
            (left,bottom*5/10),
            (left-40,bottom*6/10),
            (left,bottom*6/10)
            ]

        #  ふきだし枠線
        pg.draw.rect(screen, my_color, rect=(left-10 , top+10, 10, bottom-30), width=0) #左
        pg.draw.rect(screen, my_color, rect=(left+10 , top-10, right-(left+20), 10), width=0) #上
        pg.draw.rect(screen, my_color, rect=(right , top+10, 10, bottom-30), width=0) #右
        pg.draw.rect(screen, my_color, rect=(left+10 , bottom, right-(left+20), 10), width=0) #下
        #  枠線四隅
        pg.draw.rect(screen, my_color, rect=(left , top, 10, 10), width=0) #左上
        pg.draw.rect(screen, my_color, rect=(right-10, top, 10, 10), width=0) #右上
        pg.draw.rect(screen, my_color, rect=(right-10, bottom-10, 10, 10), width=0) #右下
        pg.draw.rect(screen, my_color, rect=(left, bottom-10, 10, 10), width=0) #左下

        #  ふきだししっぽ
        my_rect = pg.draw.polygon(screen, (255,255,255), points=try_positions, width=0)
        #  しっぽ枠線
        pg.draw.rect(screen, my_color, rect=(left-10, (bottom*5/10), 10, 10), width=0) #頂点1
        pg.draw.rect(screen, my_color, rect=(left-20, (bottom*5/10)+10, 10, 10), width=0) #辺1
        pg.draw.rect(screen, my_color, rect=(left-30, (bottom*5/10)+20, 10, 10), width=0) #辺1
        pg.draw.rect(screen, my_color, rect=(left-40, (bottom*6/10)-10, 10, 10), width=0) #頂点2
        pg.draw.rect(screen, my_color, rect=(left-50, (bottom*6/10), 50, 10), width=0) #辺3

        self.draw_text(screen, left, top)

    def draw_text(self, screen:pg.surface, left_x:int, top_y:int):
        """
        注文内容を表示するメソッド
        """
        # フォントの設定
        font = pg.font.Font(FONT_PATH,40)
        font_color = (139,0,0)
        # フォントの座標
        x = left_x+20
        y = top_y+10
        y_space = 50  # 行間

        order_text,order_img = self.order.get_text()  # オーダークラスから注文内容を取得
        text_lines = order_text.splitlines()  # "\n"でテキストを分ける

        for i,text in enumerate(text_lines):
            text_surface = font.render(text, True, font_color)
            text_rct = text_surface.get_rect()
            text_rct.topleft = (x,y)
            screen.blit(text_surface, text_rct)

            y += y_space

            # 具材アイコンの表示(画像サイズ変える)

            if i < len(order_img):
                img_surface = pg.image.load(order_img[i])
                img_surface = pg.transform.scale(img_surface, (100,75))  # 画像のサイズ変更
                img_rct = img_surface.get_rect()
                img_rct.left = text_rct.right+10
                img_rct.centery = text_rct.centery
                screen.blit(img_surface, img_rct)

class Order():
    """
    オーダーを管理するクラス

    my_spiceslevel : 注文する辛さ
    my_order :注文する具材内容
    my_orderimg :注文する具材の画像
    """
    def __init__(self, toppings_dict:dict, spices_dict:dict):
        self.my_spices = None
        self.my_order = []
        self.my_orderimg = []
        self.toppings_dict = {v:k for k,v in toppings_dict.items()} # topping_dictの値とキーを入れ替えた辞書
        self.toppings = list(toppings_dict.values())
        self.spicess = [ v for v in spices_dict.values()]

    def set_order(self, max:int):
        """
        オーダーを決める
        max :注文の最大選択個数
        """
        order_num = random.randint(1,max)

        #  具材リストからランダムに取得
        for i in range(0,order_num):
            topping = random.choice(self.toppings)
            self.my_order.append(topping)
            self.my_orderimg.append( self.toppings_dict[topping] )

        #  辛さをランダムに決定
        self.my_spices = random.choice(self.spicess)

    def get_order(self):
        """
        注文具材の一覧を取得
        """
        return self.my_order.copy()

    def get_spiceslevel(self):
        """
        注文の辛さを取得
        """
        return self.my_spices.copy()

    def get_text(self):
        """
        注文表示用テキスト＆具材画像を返す
        """
        order_text = f""

        # テキストの生成
        for topping in self.my_order:
            order_text += topping + "\n"
        else:
            order_text += f"の{self.my_spices}\nをください"


        return order_text,self.my_orderimg

class Bowl(pg.sprite.Group):
    """
    どんぶりに関するクラス
    """

    def __init__(self, *sprites, spices_dict:dict):
        super().__init__(*sprites)
        self.spices_dict = spices_dict
        self.spice_iter = iter(spices_dict.keys())
        self.spice_key = next(self.spice_iter)
        self.img = pg.transform.scale(pg.image.load( self.spice_key ),(350,250))

    def draw(self,screen):
        """
        どんぶりを描画するメソッド
        """
        self.rct = self.img.get_rect()
        self.rct.center = (WIDTH/2,HEIGHT/2+100)
        screen.blit(self.img,self.rct)

    def increase_sprice(self):
        """
        辛さのレベルとどんぶりの画像を変えるメソッド
        """
        self.spice_img = next(self.spice_iter)
        self.img = pg.transform.scale(pg.image.load( self.spice_img ),(350,250))

    def get_spicelevel(self):
        """
        現在の辛さのレベル名(中辛など)を返す
        """
        return self.spices_dict[ self.spice_key ].copy()
        

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
        self.rect.top = 120  # 文字の左上のy座標

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
    pg.display.set_caption("麻辣湯アルバイター☆彡")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更
    table_img = pg.image.load(f"fig/table.png")
    table_img = pg.transform.scale(table_img, (WIDTH*1.1, HEIGHT))  # 画像のサイズ変更
    score = 0
    
    while True:

        life = Life(0)   # 初期残機数を3に設定
        toppings_dict = {
            f"fig/harusame.png":"春雨",
            f"fig/kikurage.png":"キクラゲ",
            f"fig/niku.png":"豚肉",
            f"fig/sakasudango.png":"サーカス団子",
            f"fig/tingensai.png":"チンゲン菜"
            }
        spices_dict = {
            f"fig/bowl_1.png":"ゼロ辛",
            f"fig/bowl_2.png":"中辛",
            f"fig/bowl_3.png":"大辛",
            f"fig/bowl_4.png":"激辛"
            }
    
        customer = Customer(    # お客さんインスタンス
            toppings_dict=toppings_dict,
            spices_dict=spices_dict, 
            max=5
            )

        score = Score()
        life = Life(0)   # 初期残機数を3に設定
        clock = pg.time.Clock()
        
        is_restart = False  # リスタートするかどうかを記録する変数

        while True: 

            for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
                if event.type == pg.QUIT:
                    return 0
                
            screen.blit(bg_img, [0, 0]) # 画面表示
            customer.draw(screen)
            screen.blit(table_img,[-55,HEIGHT/3])
            customer.bowl.draw(screen)



            life.update(screen)  #　残機数分のハートを表示
            if life.num <= 0:
                is_restart = gameover(screen, score.value)
                break

            score.update(screen)

            pg.display.update() # 画面更新
            clock.tick(50)

        if is_restart == True:
                continue  # 外側のループの先頭に戻る（＝リスタート）
        else:
            return 0  # main関数を終了する（＝Escが押されたか、×で閉じられた）
        screen.blit(bg_img, [0, 0]) # 画面表示

        pg.display.update() # 画面更新
        clock.tick(50)

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
