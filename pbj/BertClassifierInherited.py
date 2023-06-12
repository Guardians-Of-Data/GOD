from transformers import TFBertForSequenceClassification
from tensorflow.keras.layers import Dense, Dropout

class CustomBertClassifier(TFBertForSequenceClassification):
    def __init__(self, model_name, num_hidden_layers=2, hidden_size=768, num_labels=2, hidden_dropout_prob=0.2, attention_probs_dropout_prob=0.2, **kwargs):
        super(CustomBertClassifier, self).__init__(model_name, num_labels=num_labels, **kwargs)
        
        # Add additional hidden layers and dropouts
        for _ in range(num_hidden_layers):
            self.bert.encoder.layer.append(self.get_hidden_layer(hidden_size))
            self.bert.pooler.dense = self.get_hidden_layer(hidden_size)
            self.dropout = Dropout(hidden_dropout_prob)
        
        self.classifier = Dense(num_labels, activation='sigmoid')
        
    def get_hidden_layer(self, hidden_size):
        return self.bert.encoder.layer[0].__class__(self.config, self.bert.encoder.layer[0].intermediate.dense.out_features, hidden_size)

# # Example usage in model_fit function
# def model_fit(train_inp, train_label, val_inp, val_label, file_path, model_filename, model_name, max_length):
#     model_save_path = file_path + '/models/{0}.h5'.format(model_filename)
#     monitor = 'val_loss'
#     learning_rate = 2e-5
#     epsilon = 1e-08
#     dropout_rate = 0.2
#     batch_size = 16
#     epochs = 5

#     es = EarlyStopping(monitor=monitor, mode='max', verbose=1, patience=3)
#     callbacks = [tf.keras.callbacks.ModelCheckpoint(filepath=model_save_path, save_weights_only=False, monitor=monitor, mode='min', save_best_only=True), es]

#     loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
#     metric = tf.keras.metrics.SparseCategoricalAccuracy('accuracy')
#     optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate, epsilon=epsilon)

#     input_ids = Input(shape=(max_length,), dtype='int64', name='input_ids')
#     attention_mask = Input(shape=(max_length,), dtype='int64', name='attention_mask')

#     model = CustomBertClassifier(model_name)
#     bert_output = model(input_ids, attention_mask=attention_mask)[0]

#     hidden1 = Dense(768, activation='relu')(bert_output)
#     dropout1 = Dropout(dropout_rate)(hidden1)
#     hidden2 = Dense(256, activation='relu')(dropout1)
