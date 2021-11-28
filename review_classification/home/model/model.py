import tensorflow as tf
import numpy as np
import pandas as pd

import os

TRAIN_DATA = "data.csv"
GLOVE_EMBEDDING = "glove.6B.100d.txt"
labels = ['Informative', 'Bug Report', 'Feature Request', 'Praise', 'Critic']
# max_words = 100000
max_words = 2295
max_len = 150
embed_size = 100


class Model(object):

    def predict(self, x):
        x = self.tokenizer.texts_to_sequences(x)
        x = tf.keras.preprocessing.sequence.pad_sequences(x, maxlen=max_len)
        pred = np.array(self.model.predict(x))

        for idx in range(len(pred)):
            pred[idx] = np.array([1 if pred[idx][i] > self.thresholds[i] else 0 for i in range(5)])

        return pred

    def __init__(self):
        train = pd.read_csv(TRAIN_DATA)
        train["content"].fillna("fillna")
        x_train = train["content"].str.lower()
        y_train = train[['Informative', 'Bug Report', 'Feature Request', 'Praise', 'Critic']].values
        total = np.sum(y_train, axis=0)
        self.thresholds = total / 490

        self.tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=max_words, lower=True)
        self.tokenizer.fit_on_texts(x_train)
        # x_train = self.tokenizer.texts_to_sequences(x_train)
        # x_train = tf.keras.preprocessing.sequence.pad_sequences(x_train, maxlen=max_len)
        embeddings_index = {}
        with open(GLOVE_EMBEDDING, encoding='utf8') as f:
            for line in f:
                values = line.rstrip().rsplit(' ')
                word = values[0]
                embed = np.asarray(values[1:], dtype='float32')
                embeddings_index[word] = embed
        word_index = self.tokenizer.word_index
        num_words = min(max_words, len(word_index) + 1)
        embedding_matrix = np.zeros((num_words, embed_size), dtype='float32')
        for word, i in word_index.items():
            if i >= max_words:
                continue
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
        input = tf.keras.layers.Input(shape=(max_len,))
        x = tf.keras.layers.Embedding(max_words, embed_size, weights=[embedding_matrix], trainable=False)(input)
        x = tf.keras.layers.Bidirectional(tf.keras.layers.GRU(128, return_sequences=True, dropout=0.1,
                                                              recurrent_dropout=0.1))(x)
        x = tf.keras.layers.Conv1D(64, kernel_size=3, padding="valid", kernel_initializer="glorot_uniform")(x)
        avg_pool = tf.keras.layers.GlobalAveragePooling1D()(x)
        max_pool = tf.keras.layers.GlobalMaxPooling1D()(x)
        x = tf.keras.layers.concatenate([avg_pool, max_pool])
        preds = tf.keras.layers.Dense(5, activation="sigmoid")(x)
        self.model = tf.keras.Model(input, preds)
        self.model.summary()
        self.model.compile(loss='binary_crossentropy', optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
                           metrics=['accuracy'])
        # batch_size = 128
        checkpoint_path = "training_1/cp.ckpt"
        checkpoint_dir = os.path.dirname(checkpoint_path)
        # cp_callback = tf.keras.callbacks.ModelCheckpoint(checkpoint_path,
        #                                                  save_weights_only=True,
        #                                                  verbose=1)
        # callbacks = [
        #     tf.keras.callbacks.EarlyStopping(patience=5, monitor='val_loss'),
        #     tf.keras.callbacks.TensorBoard(log_dir='./logs'),
        #     cp_callback
        # ]
        # self.model.fit(x_train, y_train, validation_split=0.2, batch_size=batch_size, epochs=1000, callbacks=callbacks, verbose=1)
        latest = tf.train.latest_checkpoint(checkpoint_dir)
        self.model.load_weights(latest)
