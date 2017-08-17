"""Minimalistic PySciter sample for Windows."""
import limp
import sciter
import ctypes
import asyncio
# import json
from multiprocessing import Process,Queue
from threading import Thread
from json import load as JLoad, loads as JLoads
from os import path as osPath, getcwd, mkdir

from EventManager import EventManager
from FunManager import ServiceEvent, GuiCallBack

ctypes.windll.user32.SetProcessDPIAware(2)

def startServiceP(cfg, _GuiRecvMsg, _CtrlRecvMsg):
    print('startServiceP')
    async def eventLoop( _CtrlRecvMsg, handlers, funMap ):
        while 1:
            try:
                # 获取事件的阻塞时间设为1秒
                event = await _CtrlRecvMsg.get(timeout = 1)
                print(event['type_'], event['event_'])
                if event['type_'] == 'sys' and event['event_'] == 'close_app':
                    break
                if event['type_'] in handlers:
                    getattr(funMap, '__'.join((event['type_'], event['event_'])))( event.get('data_',None) )
            except Exception as e:
                pass
    async def downloadLoop():
        await asyncio.sleep(1)

    funMap = ServiceEvent( cfg, _GuiRecvMsg )
    handlers = ['tumblr', 'sys']

    asyncio.ensure_future(eventLoop(_CtrlRecvMsg, handlers, funMap))
    asyncio.ensure_future(downloadLoop())
    # EventManager( _CtrlRecvMsg, handlers, funMap ).Start()
    # loop = asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop)
    loop.run_forever()

def queueLoop( _GuiRecvMsg, funCall ):
    guiCallBack = GuiCallBack( funCall )
    handlers = ['tumblr', 'sys']
    EventManager( _GuiRecvMsg, handlers, guiCallBack ).Start()

class Frame(sciter.Window):
    def __init__(self):
        '''
            ismain=False, ispopup=False, ischild=False, resizeable=True,
            parent=None, uni_theme=False, debug=True,
            pos=None,  pos=(x, y)
            size=None
        '''
        super().__init__(ismain=True, debug=True)
        self.set_dispatch_options(enable=True, require_attribute=False)

    def _document_ready(self, target):
        print('ready')
        self.cfg = self.initCfg()
        self.GuiRecvMsg = Queue()
        self.CtrlRecvMsg = Queue()
        p = Process(target = startServiceP, args = ( self.cfg, self.GuiRecvMsg, self.CtrlRecvMsg ))
        p.daemon = True
        p.start()
        t = Thread(target = queueLoop, args=( self.GuiRecvMsg, self.call_function ))
        t.daemon = True
        t.start()
        self.call_function('hideStartScreen')

    def document_close(self):
        print("close")

    def initCfg(self):
        cfg = {"tumblr":{"alt_sizes":-3,"preview_size":-4,"dashboard_param":{"limit":5,"offset":0},"posts_param":{"limit":5,"offset":0}},"proxies":"","imgTemp":"","imgSave":""}
        with open('data.json', 'r') as f:
            cfg.update( JLoad(f) )
        current_folder = getcwd()
        cfg['imgTemp'] = ( cfg['imgTemp'] or osPath.join( current_folder, 'imgTemp') )
        if not osPath.isdir( cfg['imgTemp'] ):
            mkdir(cfg['imgTemp'])
        cfg['imgSave'] = ( cfg['imgSave'] or osPath.join( current_folder, 'imgSave') )
        if not osPath.isdir( cfg['imgSave'] ):
            mkdir(cfg['imgSave'])
        return cfg

    def signal(self, t, e, d = None):
        print('signal',t,e)
        '''接收界面事件并转发'''
        self.CtrlRecvMsg.put({
            'type_' : str(t).strip('"'),
            'event_' : str(e).strip('"'),
            'data_' : d if not d else JLoads(str(d))
        })


if __name__ == '__main__':
    frame = Frame()
    frame.load_file("Gui/main.html")
    frame.run_app()
