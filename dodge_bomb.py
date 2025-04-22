import os
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
    } #  辞書
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")  # タイトル
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 6行目
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # 0.9倍
    kk_rct = kk_img.get_rect()  # Rect
    kk_rct.center = 300, 200  # 初期座標
    clock = pg.time.Clock()
    tmr = 0
    while True: #ゲームのループ
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])  # 背景の貼り付け

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():  #keyにpg,mvにタプルが入る
            if key_lst[key]:
                sum_mv[0] += mv[0]  #上下
                sum_mv[1] += mv[1]  #左右
                
        kk_rct.move_ip(sum_mv)  # 合わせて動かす
        screen.blit(kk_img, kk_rct)  # 移動量
        pg.display.update()  # 画面の更新
        tmr += 1
        clock.tick(50)  # フレームレート


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
