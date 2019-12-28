import tensorflow as tf
import numpy as np
import models
import dataset ## Controllare sul file originale come si loadda la roba
from tensorflow.keras.callbacks import (
    ReduceLROnPlateau,
    EarlyStopping,
    ModelCheckpoint,
    TensorBoard
)


YoloLoss = models.YoloLoss
YoloV3 = models.YoloV3

yolo_anchors = np.array([(10, 13), (16, 30), (33, 23), (30, 61), (62, 45),
                         (59, 119), (116, 90), (156, 198), (373, 326)],
                        np.float32) / 416

yolo_anchor_masks = np.array([[6, 7, 8], [3, 4, 5], [0, 1, 2]])
learning_rate = 0.0001
size = 450
batch_size = 2
epochs = 1



train_dataset = dataset.load_tfrecord_dataset(
            'data/tfrecord.tfrecord', 'data/class_file.txt')

train_dataset = train_dataset.shuffle(buffer_size=1024)  
train_dataset = train_dataset.batch(batch_size)
# train_dataset = train_dataset.map(lambda x, y: (
    # dataset.transform_images(x, size), ## transform_images Va messo in dataset_load
    # dataset.transform_targets(y, yolo_anchors, yolo_anchor_masks, 80)))
train_dataset = train_dataset.prefetch(
    buffer_size=tf.data.experimental.AUTOTUNE)

val_dataset = dataset.load_fake_dataset()

# val_dataset = dataset.load_tfrecord_dataset(
#     'data/tfrecord.tfrecord', 'data/class_file.txt')
# val_dataset = val_dataset.batch(batch_size)
# val_dataset = val_dataset.map(lambda x, y: (
# dataset.transform_images(x, FLAGS.size),
# dataset.transform_targets(y, anchors, anchor_masks, 80)))

optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
loss = [YoloLoss(yolo_anchors[mask]) for mask in yolo_anchor_masks]



model = YoloV3(size, training=True)

model.compile(optimizer=optimizer, loss=loss,
                      run_eagerly='fit')
callbacks = [
    ReduceLROnPlateau(verbose=1),
    EarlyStopping(patience=3, verbose=1),
    ModelCheckpoint('checkpoints/yolov3_train_{epoch}.tf',
                    verbose=1, save_weights_only=True),
    TensorBoard(log_dir='logs')
]
history = model.fit(train_dataset,
                    epochs=epochs,
                    callbacks=callbacks,
                    validation_data=val_dataset)
print('DAJJEEEE')
