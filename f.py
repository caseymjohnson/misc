import numpy as np
import cv2
import imageio
import os


# initial blank canvas
dims= (1000, 1000, 3)
canvas = np.zeros(dims)

# color mapping: progress flag RGB values
hues = [
    [228, 3, 3],
    [255, 140, 0],
    [255, 237, 0],
    [0, 128, 38],
    [36, 64, 142],
    [115, 41, 130],
    [255, 175, 200],
    [116, 215, 238],
    [97, 57, 21],
    [0, 0, 0]
]

# the rule that we apply
def evaluate_pixel(xy, hues, zoom, precision=3):
    x,y = xy
    if y == 0:
        y = 0.0001
    ratio = abs(round(x / y, precision))
    while True:
        individualDigits = [int(char) for char in str(ratio).replace('.', '')]
        ratio = sum(individualDigits)
        if len(individualDigits) <= 1:
            break
    return hues[int(ratio)]

# walk along canvas
def make_fractal(canvas, dims, hues, zoom, precision):
    nSteps = dims[0] * dims[1]
    step = 0
    for x in range (dims[1]):
        for y in range(dims[0]):
            xZoomed = int(x/zoom - (dims[1] / (2 * zoom)))
            yZoomed = int(y/zoom - (dims[0] / (2 * zoom)))
            hue = evaluate_pixel(( xZoomed, yZoomed), hues, zoom, precision)
            canvas[y, x] = hue # (y,x because you walk top to bottom in an image array - fun!)
            if (step % int(nSteps/100)) == 0:
                print(f' {100 * step / nSteps} percent complete', end='\r')
            step += 1
    return canvas

# show canvas
filenames = []
for precision in [3, 2, 1]:
    for zoom in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        canvas = make_fractal(canvas, dims, hues, zoom, precision)
        canvas = canvas[:, :, [2, 1, 0]]
        cv2.imshow('evaluated canvas', canvas / 255)
        fname = f'results/{len(os.listdir("results"))}fractal_.png'
        filenames.append(fname)
        cv2.imwrite(fname, canvas)
        #cv2.waitKey(0)

# write to a gif for kicks and giggles
images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('results/movie.gif', images)