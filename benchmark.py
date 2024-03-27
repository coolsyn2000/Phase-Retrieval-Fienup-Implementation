import numpy as np
from phase_retrieval import fienup_phase_retrieval
import time


def benchmark_pr(input_size, iter, cupy):
    input = np.random.rand(*input_size)

    mask = np.ones_like(input)

    start_time = time.time()
    fienup_phase_retrieval(input,
                           steps=iter,
                           suppmat=mask,
                           mode='HIO',
                           verbose=False,
                           use_cupy=cupy)
    end_time = time.time()

    return end_time - start_time


if __name__ == "__main__":

    print("cupy time: %.4f s" % benchmark_pr((256, 256), 5000, True))

    print("numpy time: %.4f s" % benchmark_pr((256, 256), 5000, False))
