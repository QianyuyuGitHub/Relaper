import tensorflow as tf
import multiGPUmnistCNNdemo

with tf.Session() as sess:
    for i in range(multiGPUmnistCNNdemo.num_gpus):
        tf.device(multiGPUmnistCNNdemo.assign_to_device('/gpu:{}'.format(i), ps_device='/cpu:0'))
    new_saver = tf.train.import_meta_graph('./result/my_model_final.meta')
    # don't need to load the checkpoint cause you don't need to train it any longer
    new_saver.restore(sess, './result/my_model_final')
    image_batch, label_batch = multiGPUmnistCNNdemo.inputs(train=True, batch_size=multiGPUmnistCNNdemo.batch_size,
                           num_epochs=multiGPUmnistCNNdemo.num_epochs)
    print(sess.run(image_batch, multiGPUmnistCNNdemo.num_classes, multiGPUmnistCNNdemo.dropout,
                                       reuse=True, is_training=False))
