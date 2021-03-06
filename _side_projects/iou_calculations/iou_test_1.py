# from https://gist.github.com/vierja/38f93bb8c463dce5500c0adf8648d371

import tensorflow as tf
import numpy as np

def bbox_overlap_iou(bboxes1, bboxes2):
    """
    Args:
        bboxes1: shape (total_bboxes1, 4)
            with x1, y1, x2, y2 point order.
        bboxes2: shape (total_bboxes2, 4)
            with x1, y1, x2, y2 point order.

        p1 *-----
           |     |
           |_____* p2

    Returns:
        Tensor with shape (total_bboxes1, total_bboxes2)
        with the IoU (intersection over union) of bboxes1[i] and bboxes2[j]
        in [i, j].
    """

    x11, y11, x12, y12 = tf.split(bboxes1, 4, axis=1)
    x21, y21, x22, y22 = tf.split(bboxes2, 4, axis=1)

    xI1 = tf.maximum(x11, tf.transpose(x21))
    yI1 = tf.maximum(y11, tf.transpose(y21))

    xI2 = tf.minimum(x12, tf.transpose(x22))
    yI2 = tf.minimum(y12, tf.transpose(y22))

    # inter_area = (xI2 - xI1 + 1) * (yI2 - yI1 + 1)
    inter_area = tf.maximum((xI2 - xI1 + 1), 0) * tf.maximum((yI2 - yI1 + 1), 0)

    bboxes1_area = (x12 - x11 + 1) * (y12 - y11 + 1)
    bboxes2_area = (x22 - x21 + 1) * (y22 - y21 + 1)

    union = (bboxes1_area + tf.transpose(bboxes2_area)) - inter_area

    return inter_area / union


if __name__ == '__main__':
    bboxes1 = tf.placeholder(tf.float32)
    bboxes2 = tf.placeholder(tf.float32)
    overlap_op = bbox_overlap_iou(bboxes1, bboxes2)

    bboxes1_vals = [[39, 63, 203, 112], [0, 0, 10, 10]]
    bboxes2_vals = [[3, 4, 24, 32], [54, 66, 198, 114], [6, 7, 60, 44]]

    bboxes1_vals = [[0, 0, 1, 1], [0, 0, 0, 0]] # i => i rows in result
    bboxes2_vals = [[0, 0, 1, 1.5], [0, 0, 1, 1]] # j => j columns in result

    with tf.Session() as sess:
        overlap = sess.run(overlap_op, feed_dict={
            bboxes1: np.array(bboxes1_vals),
            bboxes2: np.array(bboxes2_vals),
        })

        print(overlap)
