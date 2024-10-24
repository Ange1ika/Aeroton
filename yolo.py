import time
import ml
import image
from ml.utils import NMS

model = 'yolo/lpd-yolov5-int8-quantized.tflite'

# Alternatively, models can be loaded from the filesystem storage.
net = ml.Model(model)
labels = ["plate"]
print(net)

colors = [  # Add more colors if you are detecting more than 7 types of classes at once.
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

@micropython.native
def yolov5(model, input, output):
    out = output[0]
    ib, ih, iw, ic = model.input_shape[0]
    ob, ow, oc = model.output_shape[0]
    if ob != 1:
        raise(ValueError("Expected model output batch to be 1!"))
    if oc < 6:
        raise(ValueError("Expected model output channels to be >= 6"))
    # cx, cy, cw, ch, score, classes[n]
    ol = ob * ow * oc
    nms = NMS(iw, ih, input[0].roi)
    m = time.ticks_ms()
    for i in range(ow):
        score = out[0, i, 4]
        if (score > 0.5):
            cx = out[0, i, 0]
            cy = out[0, i, 1]
            cw = out[0, i, 2] * 0.5
            ch = out[0, i, 3] * 0.5
            xmin = (cx - cw) * iw
            ymin = (cy - ch) * ih
            xmax = (cx + cw) * iw
            ymax = (cy + ch) * ih
            labels = out[0, i, 5:]
            label_index = max(enumerate(labels), key=lambda x: x[1])[0]
            nms.add_bounding_box(xmin, ymin, xmax, ymax, score, label_index)
    boxes = nms.get_bounding_boxes()
    print("time", time.ticks_diff(time.ticks_ms(), m))
    return boxes

clock = time.clock()
while True:
    clock.tick()

    img = image.Image("yolo/plate.jpg", copy_to_fb=True)
    img.to_rgb565()

    for i, detection_list in enumerate(
        net.predict([img], callback=yolov5)
    ):
        print("********** %s **********" % labels[i])
        for rect, score in detection_list:
            print(rect, "score", score)
            img.draw_rectangle(rect, color=colors[i], thickness=2)

    print(clock.fps(), "fps", end="\n")

