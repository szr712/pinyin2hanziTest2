# from multiprocessing import Process, Lock

# def f(l, i):
#     # l.acquire()
#     try:
#         print('hello world', i)
#     finally:
#         pass
#         # l.release()

from pypinyin import lazy_pinyin,Style


if __name__ == '__main__':
    # lock = Lock()

    # for num in range(10):
    #     Process(target=f, args=(lock, num)).start()
    # list = [0, 2, 0,1,2,0,2]
    # sublist=[0,2]
    
    pinyin_list = lazy_pinyin("和的定义域不同故不是同一函数", style=Style.TONE3)
    print(pinyin_list)
