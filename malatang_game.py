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
        self.font = pg.font.Font("fig/DotGothic16-Regular.ttf", 40) # 表示する文字の設定

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

        # 半透明の黒い背景を作成
        bg = pg.Surface((390, 120), pg.SRCALPHA)
        pg.draw.rect(bg, (0, 0, 0), (0, 0, 390, 120), border_radius=20)
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

        screen.blit(day_img, (30, 20))
        screen.blit(time_img, (30, 65))


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
        self.font = pg.font.Font("fig/DotGothic16-Regular.ttf", 30)  # 操作説明
        self.title_font = pg.font.Font("fig/DotGothic16-Regular.ttf", 45)  # 操作説明タイトル

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
        screen.blit(title, (450, 100))

        # 操作説明
        texts = [
            "数字キー・クリック：具材を選択する",
            "上下キー：辛さを変更する(3段階)",
            "Qキー：操作方法を開く・閉じる"
        ]

        for i, text in enumerate(texts):
            img = self.font.render(
                text, True, (255, 255, 255)
            )
            screen.blit(img, (300, 220 + i * 65))

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("★麻辣湯★")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    clock = pg.time.Clock()

    timer = Time() # タイマーを作成
    help_screen = Help()  # 操作方法を作成
    
    font = pg.font.Font("fig/DotGothic16-Regular.ttf", 40)

    while True: 

        dt = clock.tick(50) / 1000 #経過時間を秒に変換

        for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
            if event.type == pg.QUIT:
                return 0

            if event.type == pg.KEYDOWN:
                # Qキーで操作方法の表示・非表示を切り替える
                if event.key == pg.K_q:
                    help_screen.toggle()

                # 時間切れの場合はEnterキーで次の日に進む
                if event.key == pg.K_RETURN and timer.owari:
                    if not help_screen.show:
                        timer.next_day()

        # 操作方法が表示していない時だけ時間を進める
        time_up = False

        if not help_screen.show:
            time_up = timer.update(dt)

        if time_up:
            print("時間切れ!")

        # 背景を表示
        screen.blit(bg_img, (0, 0))

        # 残り時間と日数を表示
        timer.draw(screen)

        # 時間切れの時メッセージを表示
        if timer.owari:
            img = font.render(
                "営業終了!Enterで次の日へ",
                True, (255, 255, 255)
            )
            screen.blit(img, (220, 300))

        # 操作説明を表示(最後に描画する)
        help_screen.draw(screen)

        pg.display.update() # 画面更新

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
