import time
import ml
import image
from ml.utils import NMS

model = "yolo11n-seg_float16.tflite"
net = ml.Model(model)
labels = ["plate"]
print(net)

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (255, 255, 0),
    (0, 0, 255),
    (255, 0, 255),
    (0, 255, 255),
    (255, 255, 255),
]

@micropython.native
def yolov11(model, input, output):
    out = output[0]
    ib, ih, iw, ic = model.input_shape[0]
    ob, ow, oc = model.output_shape[0]
    if ob != 1:
        raise(ValueError("Expected model output batch to be 1!"))
    if oc < 6:
        raise(ValueError("Expected model output channels to be >= 6"))

    ol = ob * ow * oc
    nms = NMS(iw, ih, input[0].roi)
    m = time.ticks_ms()

    for i in range(ow):
        score = out[0, i, 4]
        if score > 0.5:
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

# Инициализация камеры
sensor = image.Sensor()
sensor.reset()  # Сбросить настройки камеры
sensor.set_framesize(image.FRAME_SIZE_QQVGA)  # Установить низкое разрешение
sensor.set_pixformat(image.YUV)  # Установить формат YUV, если поддерживается
sensor.run(1)  # Начать захват изображений

clock = time.clock()
while True:
    clock.tick()

    img = sensor.snapshot()  # Захватить изображение с камеры

    for i, detection_list in enumerate(net.predict([img], callback=yolov11)):
        print("********** %s **********" % labels[i])
        for rect, score in detection_list:
            print(rect, "score", score)
            img.draw_rectangle(rect, color=colors[i], thickness=2)

    print(clock.fps(), "fps", end="\n")
