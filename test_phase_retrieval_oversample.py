import numpy as np
import matplotlib.pyplot as plt
from phase_retrieval import fienup_phase_retrieval
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage import io

np.random.seed(12345)


def test_oversample_ratio(image, ratio=2, method="HIO"):

    size = image.shape

    pad_size = (size[0] * (ratio - 1) // 2, size[1] * (ratio - 1) // 2)
    image_padded = np.pad(image, pad_size, 'constant', constant_values=0)
    magnitudes_oversampled = np.abs(np.fft.fft2(image_padded))
    mask = np.pad(np.ones(size), pad_size, 'constant', constant_values=0)

    result_oversampled, _, err = fienup_phase_retrieval(magnitudes_oversampled,
                                                      steps=1000,
                                                      suppmat=mask,
                                                      mode='HIO',
                                                      verbose=True,
                                                      use_cupy=True)

    image_quality = psnr(image_padded,result_oversampled,data_range=255)

    plt.figure(figsize=(12, 4))
    plt.suptitle("Oversample: X%d, PSNR: %.2f"%(ratio, image_quality))

    plt.subplot(1, 3, 1)
    plt.imshow(image_padded, cmap='gray')
    plt.title('Image Oversampled')
    plt.subplot(1, 3, 2)
    plt.imshow(result_oversampled, cmap='gray')
    plt.title('Image Retrieved')
    plt.subplot(1, 3, 3)
    plt.plot(err[20:])
    plt.title('Magnitude Error')
    plt.tight_layout()
    plt.savefig('./asset/result_oversampling_x%d.png'%ratio)
    plt.show()


if __name__ == "__main__":
    image = io.imread('./images/cameraman.png', mode='F')
    test_oversample_ratio(image, ratio=1, method="ER")
    test_oversample_ratio(image, ratio=2, method="ER")
    test_oversample_ratio(image, ratio=4, method="ER")
