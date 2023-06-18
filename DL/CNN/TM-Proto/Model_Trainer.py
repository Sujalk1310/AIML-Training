import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

def TrainModel():
    print("Preprocessing...")
    train_datagen = ImageDataGenerator(rescale = 1./255,
                                    shear_range = 0.2,
                                    zoom_range = 0.2,
                                    horizontal_flip = True)
    training_set = train_datagen.flow_from_directory('dataset/Training',
                                                    target_size = (64, 64),
                                                    batch_size = 32,
                                                    class_mode = 'binary')

    test_datagen = ImageDataGenerator(rescale = 1./255)
    test_set = test_datagen.flow_from_directory('dataset/Testing',
                                                target_size = (64, 64),
                                                batch_size = 32,
                                                class_mode = 'binary')
    print()
    print("Creating model framework...")

    cnn = tf.keras.models.Sequential()

    cnn.add(tf.keras.layers.Conv2D(6, (5, 5), activation='relu', padding='same', input_shape=[64, 64, 3]))

    cnn.add(tf.keras.layers.MaxPool2D((2, 2)))

    cnn.add(tf.keras.layers.Conv2D(16, (5, 5), activation='relu', padding='valid'))

    cnn.add(tf.keras.layers.MaxPool2D((2, 2)))

    cnn.add(tf.keras.layers.Flatten())

    cnn.add(tf.keras.layers.Dense(units = 120, activation = 'relu'))

    cnn.add(tf.keras.layers.Dense(units = 84, activation = 'relu'))

    cnn.add(tf.keras.layers.Dense(units = 2, activation = 'softmax'))

    cnn.compile(optimizer = 'adam', loss = 'sparse_categorical_crossentropy', metrics = ['accuracy'])

    cnn.summary()

    checkpoint_filepath = 'tmp/checkpoint'
    model_checkpoint_callback = [
        tf.keras.callbacks.ModelCheckpoint(filepath = checkpoint_filepath, save_weights_only = True, monitor = 'val_accuracy', mode = 'max', save_best_only = True),
        tf.keras.callbacks.ReduceLROnPlateau(monitor='loss', patience=2, verbose=1),
        tf.keras.callbacks.EarlyStopping(monitor='loss', patience=5, verbose=1)
    ]
    print()
    print("Fitting the model...")
    cnn.fit(x = training_set, validation_data = test_set, epochs = 10, callbacks = [model_checkpoint_callback])

    cnn.load_weights(checkpoint_filepath)
    print()
    print("Model Scores...")
    scores = cnn.evaluate(test_set, verbose=0)
    print("%s: %.2f%%" % (cnn.metrics_names[1], scores[1]*100))

    cnn.save("model.h5")
    print()
    print("Saved model to disk...")