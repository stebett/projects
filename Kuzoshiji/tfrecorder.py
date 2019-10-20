import pandas as pd
import hashlib
import tensorflow as tf
from PIL import Image 
from object_detection.utils import dataset_util


def getImageSize(image):
    width, height = Image.open('{}/{}'.format(train_dir, image)).size
    return [width, height]


def gen_example(height, 
                width, 
                filename, 
                key, 
                encoded_jpg, 
                xmin,
                xmax, 
                ymin, 
                ymax, 
                classes_text):
    example = tf.train.Example(features=tf.train.Features(feature={
      'image/height': dataset_util.int64_feature(height),
      'image/width': dataset_util.int64_feature(width),
      'image/filename': dataset_util.bytes_feature(
          filename.encode('utf8')),
      'image/source_id': dataset_util.bytes_feature(
          filename.encode('utf8')),
      'image/key/sha256': dataset_util.bytes_feature(key.encode('utf8')),
      'image/encoded': dataset_util.bytes_feature(encoded_jpg),
      'image/format': dataset_util.bytes_feature('jpeg'.encode('utf8')),
      'image/object/bbox/xmin': dataset_util.float_list_feature(xmin),
      'image/object/bbox/xmax': dataset_util.float_list_feature(xmax),
      'image/object/bbox/ymin': dataset_util.float_list_feature(ymin),
      'image/object/bbox/ymax': dataset_util.float_list_feature(ymax),
      'image/object/class/text': dataset_util.int64_feature(classes_text),
    }))
    return example

train_dir = 'data/train_images'
csv = pd.read_csv("data/df_yolo.csv").values

tiny_csv = csv[:10]

with tf.python_io.TFRecordWriter("data/tfrecords.tfrecords") as writer:

    for row in tiny_csv:
        filename = row[0]
        with tf.gfile.GFile('{}/{}'.format(train_dir, filename), 'rb') as fid:
            encoded_jpg = fid.read()

        width, height = getImageSize(filename)
        key = hashlib.sha256(encoded_jpg).hexdigest()
        classes_text = row[1]
        xmin = [float(row[2])]
        ymin = [float(row[3])]
        xmax = [float(row[4])]
        ymax = [float(row[5])]

        example = gen_example(height=height,
                                width=width,
                                filename=filename,
                                key=key,
                                encoded_jpg=encoded_jpg,
                                xmin=xmin,
                                xmax=xmax,
                                ymin=ymin,
                                ymax=ymax,
                                classes_text=classes_text)

        writer.write(example.SerializeToString())


