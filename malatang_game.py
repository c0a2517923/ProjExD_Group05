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

# ----- クラスここまで ------


# ----- メイン ------

def main():
    pg.display.set_caption("麻辣湯アルバイター☆彡")  # タイトルの設定
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # ウィンドウサイズ
    bg_img = pg.image.load(f"fig/background.png")  # 正しい背景画像に変更する
    bg_img = pg.transform.scale(bg_img, (WIDTH, HEIGHT))  # 画像のサイズ変更

    while True:
        score = 0
        life = Life(3)   # 初期残機数を3に設定
        clock = pg.time.Clock()
        
        is_restart = False  # リスタートするかどうかを記録する変数
        while True: 

            for event in pg.event.get():    # ×ボタンでウィンドウを閉じる
                if event.type == pg.QUIT:
                    return 0
            screen.blit(bg_img, [0, 0]) # 画面表示

            life.update(screen)  #　残機数分のハートを表示
            if life.num <= 0:
                is_restart = gameover(screen, score)
                break

            pg.display.update() # 画面更新
            clock.tick(50)

        if is_restart == True:
                continue  # 外側のループの先頭に戻る（＝リスタート）
        else:
            return 0  # main関数を終了する（＝Escが押されたか、×で閉じられた）

# 呪文
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
