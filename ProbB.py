import thread
import os

class glb:
    lst = []
    running = 0
    rlock = thread.allocate_lock()
    alock = thread.allocate_lock()


# TODO maybe take a start index (line) in the global array for the chunk that is taken #
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


# TODO (maybe hacky?) preprocess the amount of lines in each chunk (by searching for '/n' character) and set that in the global to be used later by each thread #
def linelengths(filenm, ntrh):
    f = open(filenm, 'rb')
    chunk = os.path.getsize(filenm) / ntrh
    f_contents = f.read()
    n_lines = f_contents.count('\n')
    for i in range(n_lines):
        glb.lst.append(0)

    glb.running = ntrh

    for t in range(ntrh):
        min_idx = t * chunk
        max_idx = (t+1) * chunk
        thd_read = f_contents[min_idx:max_idx]
        thread.start_new_thread(count_bytes, (thd_read, ))

    while glb.running > 0: pass

    return glb.lst
