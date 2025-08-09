from numpy.typing import NDArray
import numpy as np
import math

def create_gauss_kernel(size: int, sigma: float) -> NDArray:
    s = np.linspace(- size // 2, size // 2 + 1, size)
    xx, yy = np.meshgrid(s,s)
    kernel = np.exp(-(xx**2+yy**2)/(2*sigma**2)) * (1/math.pi*sigma)
    return kernel / np.sum(kernel)

def convolve2d(image, kernel):
    (iH, iW) = image.shape
    (kH, kW) = kernel.shape
    pad = kH // 2

    padded = np.pad(image, pad, mode='constant')
    output = np.zeros_like(image)
    
    for y in range(iH):
        for x in range(iW):
            window = padded[y:y + kH, x:x + kW]
            output[y, x] = np.sum(window * kernel)
    return output

def smooth_with_gauss(image: NDArray, sigma: float) -> NDArray:
    sigma = 1 if sigma <= 0 else sigma
    kernel = create_gauss_kernel(5, sigma)
    return convolve2d(image, kernel)

def get_integral_by_simpson(f, a: float, b: float, n = 10) -> float:
    if n % 2 != 0:
        n += 1  
    
    h = (b - a) / n
    integral = f(a) + f(b) 

    for i in range(1, n):
        x = a + i * h
        if i % 2 == 1:
            integral += 4 * f(x)
        else:
            integral += 2 * f(x)
    
    return integral * h / 3



def minimize_scalar(func, bounds=(0, 1), tol=1e-2, max_iter=100):
    a, b = bounds
    gr = (5 ** 0.5 - 1) / 2

    x1 = a + (1 - gr) * (b - a)
    x2 = a + gr * (b - a)
    f1 = func(x1)
    f2 = func(x2)

    for _ in range(max_iter):
        if abs(b - a) < tol:
            break

        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + (1 - gr) * (b - a)
            f1 = func(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = a + gr * (b - a)
            f2 = func(x2)

    return (a + b) / 2




def zoom(arr, zoom_factors, order=1):
    if order != 1:
        raise ValueError("order only 1")

    zy, zx = zoom_factors
    h, w = arr.shape

    new_h = int(h * zy)
    new_w = int(w * zx)

    y_coords = np.linspace(0, h - 1, new_h)
    x_coords = np.linspace(0, w - 1, new_w)

    y0 = np.floor(y_coords).astype(int)
    y1 = np.minimum(y0 + 1, h - 1)
    x0 = np.floor(x_coords).astype(int)
    x1 = np.minimum(x0 + 1, w - 1)

    dy = y_coords - y0
    dx = x_coords - x0

    dy = dy[:, np.newaxis]
    dx = dx[np.newaxis, :]

    top = (1 - dx) * arr[y0][:, x0] + dx * arr[y0][:, x1]
    bottom = (1 - dx) * arr[y1][:, x0] + dx * arr[y1][:, x1]
    zoomed = (1 - dy) * top + dy * bottom

    return zoomed