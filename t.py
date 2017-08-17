import asyncio
from asyncio import Queue
# from FunManager import ServiceEvent, GuiCallBack

def startServiceP(cfg, _GuiRecvMsg, _CtrlRecvMsg):
    # print('startServiceP')
    # print(_CtrlRecvMsg.get())
    async def eventLoop( _CtrlRecvMsg, handlers, funMap ):
        print('eventLoop')
        while 1:

            print('i')
            try:
                # 获取事件的阻塞时间设为1秒
                # await asyncio.sleep(1)
                event = await _CtrlRecvMsg.get(timeout = 1)
                print(event['type_'], event['event_'])
                if event['type_'] == 'sys' and event['event_'] == 'close_app':
                    break
                # if event['type_'] in handlers:
                    # getattr(funMap, '__'.join((event['type_'], event['event_'])))( event.get('data_',None) )
            except Exception as e:
                pass
    async def downloadLoop(_CtrlRecvMsg, handlers, funMap):
        print('downloadLoop')
        while 1:
            print('d')
            event = await _CtrlRecvMsg.get(timeout = 1)
        

    # funMap = ServiceEvent( cfg, _GuiRecvMsg )
    funMap = None
    handlers = ['tumblr', 'sys']

    asyncio.ensure_future(eventLoop(_CtrlRecvMsg, handlers, funMap))
    asyncio.ensure_future(downloadLoop(_CtrlRecvMsg, handlers, funMap))
    # EventManager( _CtrlRecvMsg, handlers, funMap ).Start()
    # loop = asyncio.new_event_loop()
    loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop)
    loop.run_forever()
    print('e')

if __name__ == '__main__':
    cfg = {"tumblr":{"alt_sizes":-3,"preview_size":-4,"dashboard_param":{"limit":5,"offset":0},"posts_param":{"limit":5,"offset":0}},"proxies":"","imgTemp":"","imgSave":""}
    _GuiRecvMsg = Queue()
    _CtrlRecvMsg = Queue()
    _CtrlRecvMsg.put({
            'type_' : 'ttt',
            'event_' : 'xxx',
            'data_' : {
                'i':0
            }
        })
    startServiceP(cfg, _GuiRecvMsg, _CtrlRecvMsg)
    print('fds')