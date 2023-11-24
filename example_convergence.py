import numpy as np
import imageio
import matplotlib.pyplot as plt
from phase_retrieval import fienup_phase_retrieval

np.random.seed(12345)
image = imageio.v2.imread('./images/star.png', mode='F')
image_padded = np.pad(image, (128,128), 'constant',constant_values=0)
magnitudes_oversampled = np.abs(np.fft.fft2(image_padded))
mask = np.pad(np.ones((256,256)), (128,128), 'constant',constant_values=0)

result_HIO, pha,err_HIO = fienup_phase_retrieval(magnitudes_oversampled,
                                                     steps=500,
                                                     suppmat=mask,
                                                     mode='HIO',
                                                     verbose=False)

result_ER, _,err_ER = fienup_phase_retrieval(magnitudes_oversampled,
                                                   pha=pha,
                                                   steps=100,
                                                   suppmat=mask,
                                                   mode='ER',
                                                   verbose=False)

plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
plt.imshow(image_padded, cmap='gray')
plt.title('Image')
plt.subplot(2,2,2)
plt.imshow(result_HIO, cmap='gray')
plt.title('Result_HIO')
plt.subplot(2,2,3)
plt.imshow(result_ER, cmap='gray')
plt.title('Result_ER')

plt.subplot(2,2,4)
err=np.concatenate((err_HIO,err_ER),axis=0)
plt.plot(err[20:])
plt.title('Result_ER')
plt.tight_layout()
plt.savefig('./asset/result_convergence.png')
plt.show()