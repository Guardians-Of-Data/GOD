from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.models import Model
import tensorflow as tf
from transformers import TFBertForSequenceClassification

class BertClassifierWithHiddenLayers:
    def __init__(self, file_path, model_filename, model_save_path, model_name, max_length):
        self.file_path = file_path
        self.model_filename = model_filename
        self.model_name = model_name
        self.max_length = max_length
        self.model_save_path = model_save_path
        self.batch_size = 16  # Add batch_size as an attribute
        self.epochs = 5  # Add epochs as an attribute
        self.model = None
        self.callbacks = None  # Add callbacks as an attribute

        
    def build_model(self):
        monitor = 'val_loss'
        learning_rate = 2e-5
        epsilon = 1e-08
        dropout_rate = 0.2
        batch_size = 16
        epochs = 5

        # es = EarlyStopping(monitor=monitor, mode='max', verbose=1, patience=3)
        self.callbacks = [tf.keras.callbacks.ModelCheckpoint(filepath=self.model_save_path, save_weights_only=False, monitor=monitor, mode='min', save_best_only=True), EarlyStopping(monitor=monitor, mode='max', verbose=1, patience=3)]

        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
        metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, epsilon=epsilon)

        input_ids = Input(shape=(self.max_length,), dtype='int64', name='input_ids')
        attention_mask = Input(shape=(self.max_length,), dtype='int64', name='attention_mask')

        bert_model = TFBertForSequenceClassification.from_pretrained(self.model_name, from_pt=True)
        bert_output = bert_model(input_ids, attention_mask = attention_mask)[0]

        hidden1 = Dense(768, activation='relu')(bert_output)
        dropout1 = Dropout(dropout_rate)(hidden1)
        hidden2 = Dense(256, activation='relu')(dropout1)
        dropout2 = Dropout(dropout_rate)(hidden2)
        classifier = Dense(2, activation='sigmoid')(dropout2)

        self.model = Model(inputs=[input_ids, attention_mask], outputs=classifier)

        self.model.compile(loss=loss, optimizer=optimizer, metrics=[metric])
        self.model.summary()

    def fit(self, train_inp, train_mask, train_label, val_inp, val_mask, val_label):
        self.build_model()
        
        history = self.model.fit(
            {'input_ids': train_inp, 'attention_mask': train_mask},
            train_label,
            batch_size = self.batch_size,
            validation_data=(
                {'input_ids': val_inp, 'attention_mask': val_mask},
                val_label
            ),
            epochs = self.epochs,
            callbacks = self.callbacks
        )

        return history, self.model
