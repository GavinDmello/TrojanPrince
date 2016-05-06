#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
font.init()
from math import cos,radians
try: import GetEvent
except: from . import GetEvent

def menu(
         menu,                          # iterable of str as ("item",) or ("item::tooltip",)
         font1      = None,             # font object|None(pygame default font): unhighlighted item font
         font2      = None,             # font object|None(font1): highlighted item font
         color1     = (128,128,128),    # (int,int,int)|color object: unhighlighted item color
         color2     = None,             # (int,int,int)|color object|None(calculated from the light arg): highlighted/neon item color
         interline  = 5,                # int: items spacing
         justify    = True,             # boolean
         light      = 5,                # int in range [-10,10]: use if color2 is None
         speed      = 300,              # int (0 = no sliding): anim speed
         lag        = 30,               # int in range [0,90]
         neon       = True,             # boolean: set neon effect
         tooltipfont= None,             # font object|None(pygame default font)
         tooltiptime= 2000,             # int
         cursor_img = None,
         hotspot    = (0,0),
         x          = None,
         y          = None,
         topleft    = None,
         midtop     = None,
         topright   = None,
         midleft    = None,
         center     = None,
         midright   = None,
         bottomleft = None,
         midbottom  = None,
         bottomright= None,
         centerx    = None,
         centery    = None
        ):
    """
    menu(
         menu,                          # iterable of str as ("item",) or ("item::tooltip",)
         font1      = None,             # font object|None(pygame default font): unhighlighted item font
         font2      = None,             # font object|None(font1): highlighted item font
         color1     = (128,128,128),    # (int,int,int)|color object: unhighlighted item color
         color2     = None,             # (int,int,int)|color object|None(calculated from the light arg): highlighted/neon item color
         interline  = 5,                # int: items spacing
         justify    = True,             # boolean
         light      = 5,                # int in range [-10,10]: use if color2 is None
         speed      = 300,              # int (0 = no sliding): anim speed
         lag        = 30,               # int in range [0,90]
         neon       = True,             # boolean: set neon effect
         tooltipfont= None,             # font object|None(pygame default font)
         tooltiptime= 2000              # int
         cursor_img = None,
         hotspot    = (0,0),
         x          = None,
         y          = None,
         topleft    = None,
         midtop     = None,
         topright   = None,
         midleft    = None,
         center     = None,
         midright   = None,
         bottomleft = None,
         midbottom  = None,
         bottomright= None,
         centerx    = None,
         centery    = None

    return: (None,None) if hit escape else (item,index)

    """
    global hold_bg_cursor
    shad = 100 # test

    class Item(Rect,object):
        def __init__(self,rect,label,tooltip):
            Rect.__init__(self,rect)
            self.label = label
            render1 = font1.render(label,1,color1)
            if justify: self.centerx = r1.centerx
            self.render1 = Surface(render1.get_rect().inflate(3,3).size,SRCALPHA)
            self.render1.blit(render1,(3,3))
            self.render1.fill((0,0,0,shad),special_flags=BLEND_RGBA_MIN)
            #sub1 = scr.subsurface(self.move(3,3)).copy().convert_alpha()       # test uncomment
            #surfarray.pixels_alpha(sub1)[:] = surfarray.array_alpha(render1)   # test uncomment
            sub1 = render1                                                      # test comment
            self.render1.blit(sub1,(0,0))
            self.render2 = font2.render(label,1,color2)
            self.white = self.render2.copy()
            self.white.fill((255,255,255,0),special_flags=BLEND_RGBA_MAX)
            if neon:
                render2 = font2.render(label,1,color1)
                renderneon = self.render2.copy()
                self.render2 = Surface(render2.get_rect().inflate(2,2).size,SRCALPHA)
                for pos in ((0,0),(0,1),(0,2),(1,0),(2,0),(0,2),(1,2),(2,2)):
                    self.render2.blit(renderneon,pos)
                self.render2.blit(render2,(1,1))
            if tooltip:
                tooltip = tooltipfont.render(tooltip,1,(200,200,200))
                r = tooltip.get_rect().inflate(11,7)
                self.tooltip = Surface(r.size,SRCALPHA)
                r = self.tooltip.fill((0,0,0,shad),(3,3,r.w-3,r.h-3))
                r = self.tooltip.fill((200,200,200,30),r.move(-3,-3))
                self.tooltip.fill((0,0,0,200),r.inflate(-2,-2))
                self.tooltip.blit(tooltip,(4,2))
            else:
                self.tooltip = None

    def show():
        i = Rect((0,0),menu[idx].render2.get_size())
        if justify: i.center = menu[idx].center
        else: i.midleft = menu[idx].midleft
        del_cursor()
        scr.blit(bg,r2,r2)
        [scr.blit(item.render1,item) for item in menu if item!=menu[idx]]
        scr.blit(menu[idx].white,i)
        show_cursor()
        display.update(r2)
        time.wait(50)
        del_cursor()
        r = scr.blit(menu[idx].render2,i)
        show_cursor()
        display.update(r.inflate(2,2))
        return r

    def anim():
        a = [menu[0]] if lag else menu[:]
        c = 0
        qq = show_cursor()
        t1 = t2 = 0
        laps = 1000./speed
        z = []
        while a:
            cc = clk.tick()
            t1 += cc
            t2 += cc

            if t2 >= 20 or t1 >= laps:
                dc = scr.blit(hold_bg_cursor,qq)
                z.append(dc)
                for ev in event.get():
                    if ev.type == MOUSEMOTION:
                        hold_rect_cursor.topleft = ev.pos
                        hold_rect_cursor.move_ip(-hotspot[0],-hotspot[1])
                t2 -= 20

            if t1 >= laps:
                for i in a:
                    z.append(scr.blit(bg,i.inflate(6,6),i.inflate(6,6)))
                    i.x = i.animx.pop(0)
                    z.append(scr.blit(i.render1,i).inflate(6,6))
                c +=1
                if not a[0].animx:
                    i = a.pop(0)
                    if not lag: break
                if lag:
                    foo,bar = divmod(c,lag)
                    if not bar and foo < len(menu):
                        a.append(menu[foo])
                t1 -= laps

            if z:
                qq = show_cursor()
                z.append(qq)
                display.update(z)
                z = []


    def del_cursor():
        return scr.blit(hold_bg_cursor,scrrect.clip(hold_rect_cursor))

    def show_cursor():
        global hold_bg_cursor
        hold_bg_cursor = scr.subsurface(scrrect.clip(hold_rect_cursor)).copy()
        return scr.blit(cursor_img,hold_rect_cursor)

    was_visible = mouse.set_visible(not cursor_img)
    tooltip_offset = mouse.get_cursor()[0] if not cursor_img else (cursor_img.get_width()-hotspot[0],cursor_img.get_height()-hotspot[1])
    events = event.get()
    scr = display.get_surface()
    scrrect = scr.get_rect()
    bg = scr.copy()
    if not font1: font1 = font.Font(None,scrrect.h//len(menu)//3)
    if not font2: font2 = font1
    if not color1: color1 = (128,128,128)
    if not color2: color2 = list(map(lambda x:x+int(((255-x)if light>0 else x)*(light/10.)),color1))
    if not tooltipfont: tooltipfont = font.Font(None,int(font1.size('')[1]//1.5))
    menu,tooltip = zip(*[i.partition('::')[0::2]for i in menu])
    m = max(menu,key=font1.size)
    r1 = Rect((0,0),font1.size(m))
    ih = r1.size[1]
    r2 = Rect((0,0),font2.size(m))
    r2.union_ip(r1)
    w,h = r2.w-r1.w,r2.h-r1.h
    r1.h = (r1.h+interline)*len(menu)-interline
    r2 = r1.inflate(w,h).inflate(6,6)

    pos = {"x":x,
           "y":y,
           "topleft":topleft,
           "midtop":midtop,
           "topright":topright,
           "midleft":midleft,
           "center":center,
           "midright":midright,
           "bottomleft":bottomleft,
           "midbottom":midbottom,
           "bottomright":bottomright,
           "centerx":centerx,
           "centery":centery}

    r2.center = scrrect.center
    for k,v in pos.items():
        if v != None:
           setattr(r2,k,v)

    if justify: r1.center = r2.center
    else : r1.midleft = r2.midleft

    menu = [Item(((r1.x,r1.y+e*(ih+interline)),font1.size(i)),i,tooltip[e]) for e,i in enumerate(menu)if i]

    hold_rect_cursor = Rect(mouse.get_pos(),cursor_img.get_size() if cursor_img else (0,0))
    hold_rect_cursor.move_ip(-hotspot[0],-hotspot[1])
    hold_bg_cursor   = Surface((0,0))
    if not cursor_img:
        cursor_img   = Surface((0,0))

    clk  = time.Clock()
    clkt = 0
    if speed:
        for i in menu:
            z = r1.w-i.x+r1.x
            i.animx = [cos(radians(x))*(i.x+z)-z for x in list(range(90,-1,-1))]
            i.x = i.animx.pop(0)
        anim()
        for i in menu:
            z = scrrect.w+i.x-r1.x
            i.animx = [cos(radians(x))*(-z+i.x)+z for x in list(range(0,-91,-1))]
            i.x = i.animx.pop(0)

    #~ display.update(del_cursor())

    #mouse.set_pos(menu[0].center)
    event.post(event.Event(MOUSEMOTION,{'pos':mouse.get_pos()}))
    idx = 0
    tooltip_seen = 0
    r = show()
    dirty = ()
    while True:
        ev = GetEvent.poll()
        if ev.type == NOEVENT and ev.inactiv >= tooltiptime:
            if not tooltip_seen and menu[idx].tooltip and r.collidepoint(mouse.get_pos()):
                rr0 = del_cursor()
                rcom = menu[idx].tooltip.get_rect(topleft=mouse.get_pos()).inflate(4,4).move(tooltip_offset).clamp(scrrect).clip(scrrect)
                combg = scr.subsurface(rcom).copy()
                scr.blit(menu[idx].tooltip,rcom)
                dirty += (rr0,rcom,show_cursor())
                tooltip_seen = 1
        if ev.type == MOUSEMOTION:
            idx_ = Rect(ev.pos,(0,0)).collidelist(menu)
            if idx_ != idx:
                if tooltip_seen and (not r.collidepoint(mouse.get_pos()) or idx_ > -1):
                    dirty += (del_cursor(),scr.blit(combg,rcom),show_cursor())
                    tooltip_seen = 0
                if idx_ > -1:
                    idx = idx_
                    r = show()
            rr0 = del_cursor()
            hold_rect_cursor.topleft = ev.pos
            hold_rect_cursor.move_ip(-hotspot[0],-hotspot[1])
            dirty += (rr0,show_cursor())

        elif ev.type == MOUSEBUTTONUP and ev.button == 1 and r.collidepoint(ev.pos):
            ret = menu[idx].label,idx
            break
        elif ev.type == KEYDOWN:
            try:
                idx = (idx + {K_UP:-1,K_DOWN:1}[ev.key])%len(menu)
                if tooltip_seen:
                    dirty += (del_cursor(),scr.blit(combg,rcom),show_cursor())
                    tooltip_seen = 0
                r = show()
            except:
                if ev.key in (K_RETURN,K_KP_ENTER):
                    ret = menu[idx].label,idx
                    break
                elif ev.key == K_ESCAPE:
                    ret = None,None
                    break
        clkt += clk.tick(500)
        if dirty:
            display.update(dirty)
            dirty = ()
            clkt = 0


    if tooltip_seen:
        display.update(scr.blit(combg,rcom))
    scr.blit(bg,r2,r2)

    if speed:
        [scr.blit(i.render1,i) for i in menu]
        display.update(r2)
        anim()
    else: display.update(r2)

    display.update(del_cursor())

    for ev in events: event.post(ev)
    mouse.set_visible(was_visible)
    return ret

if __name__ == '__main__':
    from os.path import dirname,join
    import pygame,classes,process,sys
    here = dirname(__file__)
    scr = display.set_mode((0,0),FULLSCREEN)
    bg = image.load(join(here,'bg.png'))
    scr.blit(bg,bg.get_rect(center=scr.get_rect().center))
    #~ scr.fill(-1)
    display.flip();print(menu.__doc__)

    while True:

        resp = menu(['play',
                     'instructions',
                     'quit::good bye'],
                     font1      = pygame.font.Font(join(here,'321impact.ttf'),25),
                     font2      = pygame.font.Font(join(here,'321impact.ttf'),30),
                     tooltipfont= pygame.font.Font(join(here,"Roboto-MediumItalic.ttf"),12),
                     color1     = (255,80,40),
                     light      = 9,
                     tooltiptime= 1000,
                     cursor_img = image.load('mouse.png'),
                     hotspot    = (38,15))

        if resp[0] == "play":
            pygame.init()
            SCREENWIDTH=800
            SCREENHEIGHT=600
#screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
            screen=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT),0 ,32)
            clock=pygame.time.Clock()
            FPS=24
            total_frames=0
            background=pygame.image.load("images/space3.jpg")
            hero=classes.Hero_space(0,450,100,100,"images/hero_space.png")
            filename = "laser1.mp3"
            tem=0;
            pygame.time.set_timer(USEREVENT+1,80)

            start_time = pygame.time.get_ticks()   # Time in milliseconds
            stop_after = 15* 1000

            #pygame.mixer.init()
            #pygame.mixer.music.load('sejourn.mp3')
            #pygame.mixer.music.play(-1)
            #sound=pygame.mixer.music.load(filename)
            end_it=False
            while end_it==False:
                screen.fill((0,0,0))
                myfont=pygame.font.SysFont("monospace",30)
                lable=myfont.render("Armitage.Inc presents",1,(255,255,0))
                for event in pygame.event.get():
                    if event.type==MOUSEBUTTONDOWN:
                        end_it=True



                screen.blit(lable,(200,200))
                pygame.display.flip()
                time=0

            while True:
               # print(total_frames)

                total=(classes.total_score)
                #print(time)

                current_time = pygame.time.get_ticks()
                tem=current_time/1000

                #if (current_time - start_time) >= stop_after:
                   # process.end_game(total)








                screen.blit(background,(0,0))
                myfont=pygame.font.SysFont("monospace",30)
                lable=myfont.render("Time "+str(tem),1,(255,255,0))
                screen.blit(lable,(600,0))
                myfont1=pygame.font.SysFont("monospace",30)
                lable1=myfont1.render(str(total),1,(255,255,0))
                screen.blit(lable1,(700,550))
                process.process(hero,FPS,total_frames)
                hero.motion(SCREENWIDTH,SCREENHEIGHT)
                classes.Enemy_space.update_all(SCREENWIDTH)
                classes.Pro.movement()
                total_frames+=1
                classes.Baseclass.allsprite.draw(screen)
                classes.Pro.List.draw(screen)
                clock.tick(FPS)
                pygame.display.flip()




#clr=(122,23,41)
#img_bug=pygame.image.load("index.png")
#i=0




  #  i+=1
   # if i>255:
    #   i%=255

   # screen.fill((160,i,35))
    #pygame.draw.line(screen,clr,(0,0),(640,360),5)
    #screen.blit(img_bug,(200,200))

            print(resp)
            quit()
        elif resp[0]=='quit':
            quit()
        elif resp[0]=='instructions':
            pass
