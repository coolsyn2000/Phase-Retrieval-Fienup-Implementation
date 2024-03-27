from tqdm import tqdm

try:
    import cupy as cp
    import numpy as np

    xp = cp
    is_cupy_imported = True

except ImportError:
    import numpy as np

    xp = np
    is_cupy_imported = False


def fienup_phase_retrieval(mag, pha=None, suppmat=None, beta=0.8,
                           steps=200, mode='HIO', verbose=True, use_cupy=True):
    assert beta > 0, 'step size must be a positive number'
    assert steps > 0, 'steps must be a positive number'
    assert mode == 'HIO' or mode == 'ER', 'mode must be \'HIO\', \'ER\''

    if use_cupy is False:
        xp = np
    elif use_cupy is True and is_cupy_imported is True:
        xp = cp
    if is_cupy_imported is False and use_cupy is True:
        print("cupy is not imported yet, using numpy")

    if suppmat is None:
        suppmat = xp.ones(mag.shape)

    assert mag.shape == suppmat.shape, 'mask and mag must have same shape'

    if pha is None:
        pha = xp.exp(1j * 2 * xp.pi * xp.random.rand(*mag.shape))

    if xp == cp:
        mag = cp.asarray(mag)
        suppmat = cp.asarray(suppmat)
        pha = cp.asarray(suppmat)

    err = xp.zeros(steps)

    # sample random phase and initialize image x
    y_hat = mag * pha
    x = xp.zeros(mag.shape)

    # previous iterate
    x_p = None

    # main loop
    for i in tqdm(range(steps), disable=not verbose):

        # inverse fourier transform
        y = xp.real(xp.fft.ifft2(y_hat))

        # previous iterate
        if x_p is None:
            x_p = y
        else:
            x_p = x

            # updates for elements that satisfy object domain constraints
        if mode == "HIO" or mode == "ER":
            x = y

        # find elements that violate object domain constraints
        # or are not masked
        indices = xp.logical_or(xp.logical_and(y < 0, suppmat),
                                xp.logical_not(suppmat))

        # updates for elements that violate object domain constraints
        if mode == "HIO":
            x[indices] = x_p[indices] - beta * y[indices]
        elif mode == "ER":
            x[indices] = 0

        # fourier transform
        x_hat = xp.fft.fft2(x)

        # satisfy fourier domain constraints
        # (replace magnitude with input magnitude)
        y_hat = mag * xp.exp(1j * xp.angle(x_hat))

        err[i] = (xp.mean(xp.square(xp.abs(x_hat)) - xp.square(mag)))

    # suppmat .* x
    x[indices] = 0

    # If using CuPy, convert result back to NumPy array before returning
    if use_cupy and is_cupy_imported:
        return cp.asnumpy(x), cp.asnumpy(xp.exp(1j * xp.angle(x_hat))), cp.asnumpy(err)
    else:
        return x, xp.exp(1j * xp.angle(x_hat)), err


# Example usage
if __name__ == "__main__":
    mag = xp.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=xp.float32)
    x, pha, err = fienup_phase_retrieval(mag, steps=10, verbose=False)
    print(x)
