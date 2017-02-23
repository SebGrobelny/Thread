import thread
import os

class glb:
    lst = []
    running = 0
    rlock = thread.allocate_lock()
    alock = thread.allocate_lock()


def count_bytes(chunk):
    ctr = 0
    for l in chunk:
        if l == '\n':
            glb.alock.acquire()
            glb.lst.append(ctr)
            glb.alock.release()
            ctr = 0
        else:
            ctr += 1
    glb.rlock.acquire()
    glb.running -= 1
    glb.rlock.release()


def linelengths(filenm, ntrh):
    lst = [] f = open(filenm, 'rb')
    size = os.path.getsize(filenm)
    chunk = size / ntrh
    f_contents = f.read()
    glb.running = ntrh

    for t in range(ntrh):
        min_idx = t * chunk
        max_idx = (t+1) * chunk
        thd_read = f_contents[min_idx:max_idx]
        thread.start_new_thread(count_bytes, (thd_read, ))

    while glb.running > 0: pass

    return glb.lst
