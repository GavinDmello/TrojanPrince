from pygame import time,event,mouse,MOUSEBUTTONDOWN,MOUSEBUTTONUP,NOEVENT

_Clic = [0,0,0,0,0,0]
_Ticks = [time.Clock(),time.Clock(),time.Clock(),time.Clock(),time.Clock(),time.Clock()]
LAPS = 200
_NoEvent_Clock = time.Clock()
_Inactiv = 0
ButtonDelay = 500
ButtonRepeat = 100
_ButtonTick = ButtonDelay

def wait():
    ev=event.wait()
    _foo(ev)
    return ev

def poll():
    ev=event.poll()
    _foo(ev)
    return ev

def get(evs=range(50)):
    ev=event.get(evs)
    for e in ev: _foo(e)
    return ev

def _foo(e):
    global _Clic,_Ticks,_Inactiv,_ButtonTick
    if e.type==NOEVENT:
        _Inactiv+=_NoEvent_Clock.tick()

        if _Inactiv>=ButtonDelay and _Inactiv>=_ButtonTick:
            _ButtonTick+=ButtonRepeat
            e.dict.update({'inactiv':_Inactiv,'repeat_buttons':mouse.get_pressed(),'mouse_pos':mouse.get_pos()})
        else:
            e.dict.update({'inactiv':_Inactiv,'repeat_buttons':[0,0,0,0,0],'mouse_pos':mouse.get_pos()})
    else:
        _Inactiv = 0
        _ButtonTick = ButtonDelay
        if e.type==MOUSEBUTTONDOWN:
            if  _Ticks[e.button].tick()>LAPS or e.button!=_Clic[0]: _Clic=[e.button,0,0,0,0,0]
        elif e.type==MOUSEBUTTONUP:
            if _Ticks[e.button].tick()>LAPS: _Clic=[e.button,0,0,0,0,0]
            else:
                _Clic[e.button]+=1
            e.dict.update({'click':_Clic})

