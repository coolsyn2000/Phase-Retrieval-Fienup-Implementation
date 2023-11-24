import numpy as np
import imageio
import matplotlib.pyplot as plt
from phase_retrieval import fienup_phase_retrieval

np.random.seed(12345)
image = imageio.v2.imread('./images/star.png', mode='F')
magnitudes = np.abs(np.fft.fft2(image))
result,_ = fienup_phase_retrieval(magnitudes,
                                steps=1000,
                                mode='HIO',
                                verbose=False)

image_padded = np.pad(image, (128,128), 'constant',constant_values=0)
magnitudes_oversampled = np.abs(np.fft.fft2(image_padded))
mask = np.pad(np.ones((256,256)), (128,128), 'constant',constant_values=0)
result_oversampled,_ = fienup_phase_retrieval(magnitudes_oversampled,
                                            steps=1000,
                                            suppmat=mask,
                                            mode='HIO',
                                            verbose=False)

plt.figure(figsize=(10,10))
plt.subplot(2,2,1)
plt.imshow(image, cmap='gray')
plt.title('Image')
plt.subplot(2,2,2)
plt.imshow(result, cmap='gray')
plt.title('Result')
plt.subplot(2,2,3)
plt.imshow(image_padded, cmap='gray')
plt.title('Image padded')
plt.subplot(2,2,4)
plt.imshow(result_oversampled, cmap='gray')
plt.title('Reconstruction oversampled')
plt.tight_layout()
plt.savefig('./asset/result_oversampling.png')
plt.show()