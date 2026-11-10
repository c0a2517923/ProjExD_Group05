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
class Goods(pg.sprite.Sprite):
    """
    商品棚に表示する具材を管理するクラス
    """
    # 商品とパスを対応させる辞書
    goods_dic = {"春雨":"fig/harusame.png",
                 "チンゲン菜":"fig/tingensai.png",
                 "豚肉":"fig/niku.png",
                 "キクラゲ":"fig/kikurage.png",
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

        # 商品した商品の個数を管理
        self.count = 0

    def select(self, select_list: list[str]):
        """
        商品を選択してselect_listに商品を追加する
        引数 select_list:
        プレイヤーが選択した商品を保存するリスト
        """
        # 商品を1つ追加する
        # 選択した商品をリストへ追加
        select_list.append(self.name)

        # 選択個数を1増やす
        self.count += 1

        print(f"{self.name} × {self.count}")
        print(f"現在の選択：{select_list}")

    def deselect(self, select_list: list[str]):
        """
        商品を1個選択解除する
        """
        # 1個以上選択されている場合だけ減らす
        if self.count > 0:

            select_list.remove(self.name)

            self.count -= 1

            print(f"{self.name} × {self.count}")
            print(f"現在の選択：{select_list}")

    def reset(self):
        """
        商品の選択状態を解除する
        """
        self.count = 0
        

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

    margin_x = 100
    margin_y = 50

    dialog_w = WIDTH - (margin_x * 2)
    dialog_h = HEIGHT - (margin_y * 2)

    gameover_screen = pg.Surface((dialog_w, dialog_h))
    pg.draw.rect(gameover_screen, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))  # 黒い矩形を作る
    gameover_screen.set_alpha(210)  # 透明度の調節

    fonto_go = pg.font.Font(FONT_PATH, 100)
    fonto_sc = pg.font.Font(FONT_PATH, 80)
    font_gu = pg.font.Font(FONT_PATH, 40)
    
    # "Game Over"の白文字を作る (少し上に配置)
    txt = fonto_go.render("Game Over", True, (255, 255, 255)) 
    txt_rect = txt.get_rect()
    txt_rect.center = dialog_w / 2, dialog_h / 2 - 100  # 中心から上に80ピクセルずらす
    gameover_screen.blit(txt, txt_rect)

    # スコアの白文字を作る (少し下に配置)
    score_txt = fonto_sc.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_txt.get_rect()
    score_rect.center = dialog_w / 2, dialog_h / 2  # 中心から下に50ピクセルずらす
    gameover_screen.blit(score_txt, score_rect)

    # 画面に操作案内を追加
    guide_txt = font_gu.render("Press ENTER to Restart / ESC to Exit", True, (200, 200, 200))
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
                screen.blit(self.image, (30+50*i, 150))

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
        return self.my_spices

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
        self.spice_keys = list(spices_dict.keys())
        self.spice_index = 0
        self.spice_key = (self.spice_keys[self.spice_index])
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
        self.spice_index = ( self.spice_index + 1) % len(self.spice_keys)
        self.spice_key = (self.spice_keys[self.spice_index])
        self.img = pg.transform.scale(pg.image.load(self.spice_key),(350, 250))

    def get_spicelevel(self):
        """
        現在の辛さのレベル名(中辛など)を返す
        """
        return self.spices_dict[ self.spice_key ]
        

class Score:
    """
    提供した麻辣湯の数によってスコアがもらえるクラス
    正しく麻辣湯を提供できたら +1000点
    
    """
    def __init__(self):
        self.font = pg.font.Font(FONT_PATH, 40)  # フォントの指定
        self.color = (255, 255, 255)  # 文字の色の指定
        self.value = 0  # 初期スコア
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)  # スコア表示設定
        self.rect = self.image.get_rect()  # imageのrectを取得
        self.rect.left = 35  # 文字の左上のx座標
        self.rect.top = 205  # 文字の左上のy座標

    def update(self, screen: pg.Surface):
        """
        スコアを画面左上に表示する
        引数 screen：ゲーム画面のSurface
        戻り値：なし
        """
        self.image = self.font.render(f"Score: {self.value}", 0, self.color)
        screen.blit(self.image, self.rect)
        

# 注文内容の正誤判定
def check_order(order_list: list[str], select_list: list[str],order_spice: str, select_spice: str) -> bool:
    """
    具材と辛さが両方一致しているか判定
    完全一致：True
    不一致：False
    引数1 order_list：お客さんが注文した具材のリスト
    引数2 select_list：プレイヤーが選択した具材のリスト
    """
    # 具材の種類・個数を判定
    goods_result = (sorted(order_list) == sorted(select_list))

    # 辛さを判定
    spice_result = (order_spice == select_spice)

    # 両方正解ならTrue
    return goods_result and spice_result

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
# ---- クラス ------
class Time:
    """
    制限時間と日数を管理するクラス
    """

    def __init__(self):
        """
        時間管理に必要な属性を初期化する。
        引数：なし
        戻り値：なし
        """
        self.day = 1 # 現在の日数
        self.time_limit = 60 # 1日の制限時間(秒)
        self.nokori = self.time_limit # 残り時間
        self.owari = False # 時間切れかどうか
        self.font = pg.font.Font(FONT_PATH, 24) # 表示する文字の設定

    def update(self, dt: float) -> bool:
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

    def reset(self):
        """
        残り時間をリセットするメソッド
        引数：なし
        戻り値：なし
        """
        self.nokori = self.time_limit
        self.owari = False

    def get_customer_count(self) -> int:
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

        # 半透明の黒い背景を作成
        bg = pg.Surface((400, 250), pg.SRCALPHA)
        pg.draw.rect(bg, (0, 0, 0), (0, 0, 400, 250), border_radius=20)
        bg.set_alpha(150)
        screen.blit(bg, (20, 15))

        # 日数を表示
        day_img = self.font.render(
            f"{self.day}日目", True, (255, 255, 255)
        )

        # 残り時間の表示
        time_img = self.font.render(
            f"残り時間：{math.ceil(self.nokori)}秒",
            True, (255, 255, 255)
        )

        screen.blit(day_img, (35, 25))
        screen.blit(time_img, (35, 85))


class Help:
    """
    ゲームの操作方法を表示するクラス
    """

    def __init__(self):
        """
        引数：なし
        戻り値：なし
        """
        self.show = False  # 操作方法を表示するかどうか
        self.font = pg.font.Font("DotGothic16/DotGothic16-Regular.ttf", 30)  # 操作説明
        self.title_font = pg.font.Font("DotGothic16/DotGothic16-Regular.ttf", 45)  # 操作説明タイトル

    def toggle(self):
        """
        操作方法の表示・非表示を切り替えるメソッド
        引数：なし
        戻り値：なし
        """
        self.show = not self.show

    def draw(self, screen):
        """
        操作方法を表示させるメソッド
        引数：screen(描画先のSurface)
        戻り値：なし
        """
        if not self.show:
            return

        # 半透明の黒い背景画面
        overlay = pg.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)
        screen.blit(overlay, (0, 0))

        # タイトルを表示
        title = self.title_font.render(
            "操作方法", True, (255, 255, 255)
        )
        title_rect = title.get_rect(center=(WIDTH//2, 90))
        screen.blit(title, title_rect)

        # 操作説明
        texts = [
            "時間切れ・注文ミスでライフが－1",
            "数字キー：具材を選択する",
            "左クリック：具材を1つ追加する",
            "右クリック：具材を1つ解除する",
            "上キー：辛さを変更する",
            "Enterキー：商品を提供する",
            "Qキー：操作方法を開く・閉じる"
        ]

        for i, text in enumerate(texts):
            img = self.font.render(
                text, True, (255, 255, 255)
            )
            screen.blit(img, (280, 175 + i * 55))

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("麻辣湯アルバイター☆彡")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更
    table_img = pg.image.load(f"fig/table.png")
    table_img = pg.transform.scale(table_img, (WIDTH*1.1, HEIGHT))  # 画像のサイズ変更
    
    while True:
        # BGMの再生
        pg.mixer.music.stop()  # 現在流れているBGMをストップ
        pg.mixer.music.load("sound/contedefees_0177.mp3")  # ダウンロードした音源ファイルをロード
        pg.mixer.music.play(-1)  # ループ再生

        life = Life(3)   # 初期残機数を3に設定
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
        life = Life(3)   # 初期残機数を3に設定
        clock = pg.time.Clock()
        timer = Time() # タイマーを作成
        help_screen = Help()  # 操作方法を作成
        font = pg.font.Font("DotGothic16/DotGothic16-Regular.ttf", 40)

        # 商品の作成
        # 商品棚に商品を追加 引数(位置)を商品関数に渡す
        goods_list = [
            Goods("春雨", (150, 550)),
            Goods("チンゲン菜", (350, 550)),
            Goods("豚肉", (550, 550)),
            Goods("キクラゲ", (750, 550)),
            Goods("サーカス団子", (950, 550))
        ]
    
        # 商品をまとめて管理するGroup
        goods = pg.sprite.Group(goods_list)
    
        # プレイヤーが選択した商品
        select_list = []

        # プレイヤーがオーダーした商品
        order_list = customer.order.get_order()

        # Customer担当と統合したら削除し、Customer側のorder_listを使用する
        # 数字キーと商品の対応
        key_dic = {pg.K_1: 0, pg.K_2: 1, pg.K_3: 2, pg.K_4: 3, pg.K_5: 4}

        is_restart = False  # リスタートするかどうかを記録する変数

        while True: 

            dt = clock.tick(50) / 1000 #経過時間を秒に変換

            for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
                if event.type == pg.QUIT:
                    return 0

                if event.type == pg.KEYDOWN:
                    # Qキーで操作方法の表示・非表示を切り替える
                    if event.key == pg.K_q:
                        help_screen.toggle()
                        continue

                # 操作説明中と営業中はゲーム操作を受け付けない
                if help_screen.show or timer.owari:
                    continue
                
                 # 数字キーによる商品選択
                if event.type == pg.KEYDOWN:
                    # 1～5キーが押された場合、対応する商品番号を取得
                    if event.key in key_dic:
                        index = key_dic[event.key]
                        # 商品を選択
                        goods_list[index].select(select_list)
                    
                    # Bowl側の辛さ変更
                    if event.key == pg.K_UP:

                        customer.bowl.increase_sprice()
                    # ENTERキーで注文内容を判定
                    if event.key == pg.K_RETURN:
                        # 注文された具材
                        order_list = (customer.order.get_order())

                        # 注文された辛さ
                        order_spice = (customer.order.get_spiceslevel())
                        # プレイヤーが選択した辛さ
                        select_spice = (customer.bowl.get_spicelevel())

                        # 具材＋辛さを判定
                        result = check_order(
                            order_list,
                            select_list,
                            order_spice,
                            select_spice
                        )
                                
                        # # 動作確認用
                        # print(f"注文具材：{order_list}")
                        # print(f"注文辛さ：{order_spice}")
                        # print(f"選択具材：{select_list}")
                        # print(f"選択辛さ：{select_spice}")
                        # print(f"判定：{result}")
                                        
                        if result:
                            # print("注文成功！")
                            # 正解で1000点
                            score.value += 1000
                        else:
                            # print("注文失敗")
                            life.num -= 1  # 注文を間違えたら残機を1減らす

                        # 商品選択をリセット
                        reset_goods(goods,select_list)

                        # 次のお客さんを作成    
                        customer = Customer(toppings_dict=toppings_dict, spices_dict=spices_dict, max=5)

                        # 次の注文を取得
                        order_list = (customer.order.get_order())

                # マウスクリックによる商品選択
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos

                    for good in goods:
                        if good.rect.collidepoint(mouse_pos):
                            # 左クリック → 1個追加
                            if event.button == 1:
                                good.select(select_list)
                            # 右クリック → 1個減らす
                            elif event.button == 3:
                                good.deselect(select_list)

            # 操作方法が表示されていない時だけ時間を進める
            time_up = False
    
            if not help_screen.show:
                time_up = timer.update(dt)
    
            if time_up:
                print("時間切れ!")
                life.num -= 1  # 時間切れでライフを1減らす

                # 商品選択をリセット
                reset_goods(goods, select_list)

                # ライフが0になったら次の日へ
                if life.num <= 0:
                    customer = Customer(toppings_dict=toppings_dict, spices_dict=spices_dict, max=5)
                
                order_list = customer.order.get_order()
                timer.reset()

            screen.blit(bg_img, [0, 0]) # 画面表示
            customer.draw(screen)
            screen.blit(table_img,[-55,HEIGHT/3])
            customer.bowl.draw(screen)

            # 商品をまとめて表示
            goods.draw(screen)

            # 選択した商品が分かるように枠を表示
            for good in goods:
                # 1個以上選択されている場合
                if good.count > 0:

                    # 商品の周囲に赤枠を表示
                    pg.draw.rect(screen,(255, 0, 0),good.rect,4)

                    # 2個以上の場合だけ「×2」「×3」などを表示
                    if good.count >= 2:
                        count_font = pg.font.Font(FONT_PATH,28)
                        count_txt = count_font.render(f"×{good.count}", True,(255, 0, 0))
                        count_rect = count_txt.get_rect()

                        # 商品画像の下に表示
                        count_rect.midtop = (good.rect.centerx,good.rect.bottom + 5)
                        screen.blit(count_txt,count_rect)
            
            timer.draw(screen) # 残り時間と日数を表示
            life.update(screen)  #　残機数分のハートを表示
            score.update(screen) # Score表示
    
            # 操作説明を最後に表示
            help_screen.draw(screen)
            
            # ライフが0になったらゲームオーバー
            if life.num <= 0:
                is_restart = gameover(screen, score.value)
                break

            pg.display.update() # 画面更新

        if is_restart:
            pg.mixer.music.stop()  # 現在流れているBGMをストップ
            continue  # 外側のループの先頭に戻る（＝リスタート）
        else:
            pg.mixer.music.stop()  # 現在流れているBGMをストップ
            return 0  # main関数を終了する（＝Escが押されたか、×で閉じられた）

    
# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
