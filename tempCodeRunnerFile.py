            具材アイコンの表示(画像サイズ変える)

            if i < len(order_img):
                img_surface = pg.image.load(order_img[i])
                img_surface = pg.transform.scale(img_surface, (100,75))  # 画像のサイズ変更
                img_rct = img_surface.get_rect()
                img_rct.left = text_rct.right+10
                img_rct.centery = text_rct.centery
                screen.blit(img_surface, img_rct)