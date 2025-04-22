import os
import random
import math
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0, -5),
    pg.K_DOWN:(0, +5),
    pg.K_LEFT:(-5, 0),
    pg.K_RIGHT:(5, 0),
    } #  辞書

# MUKI辞書
kk_img = pg.image.load("fig/3.png")
kk_gyaku =  pg.transform.flip(kk_img, True, False)
MUKI = {
    (0, -5): pg.transform.rotozoom(kk_gyaku,   90, 0.9),   # 上
    (+5, -5): pg.transform.rotozoom(kk_gyaku, 45, 0.9),  # 右上
    (+5, 0):  pg.transform.rotozoom(kk_gyaku, 0, 0.9),  # 右
    (+5, +5): pg.transform.rotozoom(kk_gyaku, -45, 0.9), # 右下
    (0, +5):  pg.transform.rotozoom(kk_gyaku, -90, 0.9),  # 下
    (-5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 0.9),  # 左下
    (-5, 0):  pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9),   # 左
    (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 0.9),   # 左上
}


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


def gameover(screen: pg.Surface) -> None:
    bl_img = pg.Surface((1100, 650)) #  背景
    bl_img.set_alpha(100)
    pg.draw.rect(bl_img, (0, 0, 0), (0, 0, 1100, 650))
    bl_rct = bl_img.get_rect()
    screen.blit(bl_img, bl_rct)  #  描画
    
    naki_img = pg.image.load("fig/8.png") #  泣き鳥
    naki_rct = naki_img.get_rect()  # Rect
    naki_rct.center = 720, 325  # 初期座標
    screen.blit(naki_img, naki_rct)  #  描画
    
    naki2_img = pg.image.load("fig/8.png") #  泣き鳥2
    naki2_rct = naki2_img.get_rect()  # Rect
    naki2_rct.center = 350, 325  # 初期座標
    screen.blit(naki2_img, naki2_rct)  #  描画
    
    fonto = pg.font.Font(None, 80) #  文字
    txt = fonto.render("Game Over", True, (255, 255, 255)) 
    screen.blit(txt, [380, 300])
    
    pg.display.update()  # 画面更新
    time.sleep(5)  # 一時停止
    

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r), pg.SRCALPHA)
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    return MUKI.get(sum_mv, MUKI[(0, 0)])  # デフォルトで静止画像を返す




def calc_orientation(org: pg.Rect, dst: pg.Rect,  current_xy: tuple[float, float]) -> tuple[float, float]:
    org_x, org_y = org.center
    dst_x, dst_y = dst.center
    dx = dst_x - org_x
    dy = dst_y - org_y
    bekutoru = math.sqrt((dx**2 + dy**2))
    if bekutoru < 300:
        return current_xy
    dx = dx/bekutoru
    dx = dx*math.sqrt(50)
    dy = dy/bekutoru
    dy = dy*math.sqrt(50)
    return (dx,dy)


def get_kk_img(sum_mv: tuple[int, int]) -> pg.Surface:
    return MUKI.get(sum_mv, MUKI[(+5, 0)])

def main():
    pg.display.set_caption("逃げろ！こうかとん")  # タイトル
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 6行目
    bg_img = pg.image.load("fig/pg_bg.jpg")  # 背景画像
    sbb_accs = [a for a in range(1, 11)]
    
    kk_img = get_kk_img((0, 0))
    kk_rct = kk_img.get_rect()  # Rect
    kk_rct.center = 300, 200  # 初期座標
    #  設定だからwhileの外↓
    bb_img = pg.Surface((20,20)) #  空の四角形
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) #  (10,10)で中心、半径10
    bb_img.set_colorkey((0, 0, 0)) #  背景を透明に
    bb_rct = bb_img.get_rect()  # Rect
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 初期座標
    vx, vy = +5, +5
    
    bb_imgs, bb_accs = init_bb_imgs() 
    
    clock = pg.time.Clock()
    tmr = 0
    
    while True: #ゲームのループ
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])  # 背景の貼り付け
        
        if kk_rct.colliderect(bb_rct): #  ぶつかったら
            gameover(screen)
            return
        
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))
        
        index = min(tmr // 500, 9)
        avx = vx * bb_accs[index]
        avy = vy * bb_accs[index]
        bb_img = bb_imgs[index]

        
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():  #keyにpg,mvにタプルが入る
            if key_lst[key]:
                sum_mv[0] += mv[0]  #上下
                sum_mv[1] += mv[1]  #左右
        kk_img = get_kk_img(tuple(sum_mv))  # ← このタイミングで更新する
        kk_rct.move_ip(sum_mv)
        kk_rct.move_ip(sum_mv)  # 合わせて動かす
        if check_bound(kk_rct) != (True, True): #  鳥が画面の外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #  なかったことに
        screen.blit(kk_img, kk_rct)  # 移動の描画
        
        bb_rct.move_ip(avx, avy)  # 爆弾を動かす
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
            vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        pg.display.update()
        screen.blit(bb_img, bb_rct)  # 爆弾の描画
        
        pg.display.update()  # 画面の更新
        tmr += 1
        clock.tick(50)  # フレームレート


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
