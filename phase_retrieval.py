import numpy as np

def fienup_phase_retrieval(mag, pha=None, suppmat=None, beta=0.8, 
                           steps=200, mode='HIO', verbose=True):
    
    assert beta > 0, 'step size must be a positive number'
    assert steps > 0, 'steps must be a positive number'
    assert mode == 'HIO' or mode == 'ER', 'mode must be \'HIO\', \'ER\''

    if suppmat is None:
        suppmat = np.ones(mag.shape)

    assert mag.shape == suppmat.shape, 'mask and mag must have same shape'

    if pha is None:
        pha = np.exp(1j*2*np.pi*np.random.rand(*mag.shape))
    
    err=np.zeros(steps)
        

    # sample random phase and initialize image x 
    y_hat = mag * pha
    x = np.zeros(mag.shape)

    # previous iterate
    x_p = None
        
    # main loop
    for i in range(0, steps):
        # show progress
        if i % 100 == 0 and verbose: 
            print("step", i, "of", steps)
        
        # inverse fourier transform
        y = np.real(np.fft.ifft2(y_hat))
        
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
        indices = np.logical_or(np.logical_and(y<0, suppmat), 
                                np.logical_not(suppmat))
        
        # updates for elements that violate object domain constraints
        if mode == "HIO":
            x[indices] = x_p[indices]-beta*y[indices] 
        elif mode == "ER":
            x[indices] = 0
        
        # fourier transform
        x_hat = np.fft.fft2(x)
        
        # satisfy fourier domain constraints
        # (replace magnitude with input magnitude)
        y_hat = mag*np.exp(1j*np.angle(x_hat))

        err[i] = (np.mean(np.square(np.abs(x_hat))-np.square(mag)))
    
    # return obj, pha, err
    return x, np.exp(1j*np.angle(x_hat)), err