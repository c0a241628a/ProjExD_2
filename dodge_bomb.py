import os
import random
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


def check_bound(rct: pg.Rect) -> tuple[bool, bool]: #  pgのRectだと伝える,真理値はbool
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True 
    if rct.left < 0 or WIDTH < rct.right: # 横方向判定
        yoko = False 
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate    

def main():
    pg.display.set_caption("逃げろ！こうかとん")  # タイトル
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 6行目
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像
    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)  # 0.9倍
    kk_rct = kk_img.get_rect()  # Rect
    kk_rct.center = 300, 200  # 初期座標
    #  設定だからwhileの外↓
    bb_img = pg.Surface((20,20)) #  空の四角形
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #  (10,10)で中心、半径10
    bb_img.set_colorkey((0, 0, 0)) #  背景を透明に
    bb_rct = bb_img.get_rect()  # Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 初期座標
    vx, vy = +5, +5 #  速度
    
    clock = pg.time.Clock()
    tmr = 0
    while True: #ゲームのループ
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])  # 背景の貼り付け
        
        if kk_rct.colliderect(bb_rct): #  ぶつかったら
            print("Game Over")
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():  #keyにpg,mvにタプルが入る
            if key_lst[key]:
                sum_mv[0] += mv[0]  #上下
                sum_mv[1] += mv[1]  #左右
        kk_rct.move_ip(sum_mv)  # 合わせて動かす
        if check_bound(kk_rct) != (True, True): #  鳥が画面の外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #  なかったことに
        screen.blit(kk_img, kk_rct)  # 移動の描画
        
        bb_rct.move_ip(vx, vy)  # 爆弾を動かす
        yoko, tate = check_bound(bb_rct)
        if not yoko: #  左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:#  上下どちらかにはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
            
        
        
        pg.display.update()  # 画面の更新
        tmr += 1
        clock.tick(50)  # フレームレート


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
