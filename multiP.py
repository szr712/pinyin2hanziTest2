import os
import sys
import math
import multiprocess


def sub_process(data, mdic, lock, mlist, sub_id):
    lock.acquire()
    mdic[sub_id] = sub_process
    mlist.append(sub_id)
    lock.release()


if __name__ == "__main__":

    num_process = 32
    data = [0]*32
    lock = multiprocess.Lock()
    with multiprocess.Manager() as m:
        mdic = m.dict()
        mlist = m.list()

        task_list = []
        batch_size = int(math.ceil(float(len(data))/float(num_process)))
        for i in range(num_process):
            tmp_data = data[i*batch_size:(i+1)*batch_size]
            p = multiprocess.Process(target=sub_process, args=(
                tmp_data, mdic, lock, mlist, i))
            task_list.append(p)
            p.start()
        for t in task_list:
            t.join()

        # to do
        print('dic', mdic)
        print('list', mlist)
