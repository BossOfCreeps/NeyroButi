from __future__ import absolute_import, division, print_function
import os
import numpy as np
import tensorflow as tf

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "NeyroButi", "static", "photo")


def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()
    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)
    return graph


def read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255):
    image_reader = tf.image.decode_png(tf.read_file(file_name, "file_reader"), channels=3, name='png_reader')
    dims_expander = tf.expand_dims(tf.cast(image_reader, tf.float32), 0)
    resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
    normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
    return tf.Session().run(normalized)


def load_labels(label_file):
    label = []
    for l in tf.gfile.GFile(label_file).readlines():
        label.append(l.rstrip())
    return label


def get_data(filename):
    graph = load_graph("retrained_graph.pb")
    input_operation = graph.get_operation_by_name("import/Mul")
    output_operation = graph.get_operation_by_name("import/final_result")

    t = read_tensor_from_image_file(os.path.join(UPLOAD_FOLDER, filename + ".jpg"))

    with tf.Session(graph=graph) as sess:
        results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
    results = np.squeeze(results)
    labels = load_labels("retrained_labels.txt")

    if labels[0] == "seva":
        return results[0]
    else:
        return results[1]