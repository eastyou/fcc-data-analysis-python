import numpy as np
import pandas as pd
import tensorflow as tf

train_df = pd.read_csv('insurance.csv')

train_target = train_df.pop('charges')
train_features = pd.get_dummies(train_df).astype(float)

normalizer = tf.keras.layers.Normalization(axis=-1)
normalizer.adapt(np.array(train_features))

model = tf.keras.Sequential([
    normalizer,
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1),
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
    loss='mean_absolute_error',
    metrics=['mean_absolute_error'],
)

history = model.fit(
    train_features,
    train_target,
    validation_split=0.2,
    epochs=200,
    batch_size=32,
    verbose=0,
)

test_df = pd.read_csv('insurance_test.csv')
test_target = test_df.pop('charges')
test_features = pd.get_dummies(test_df).reindex(columns=train_features.columns, fill_value=0).astype(float)

predictions = model.predict(test_features).flatten()

# freeCodeCamp 需要把预测结果写回其在内存中的测试表
try:
    import __main__

    if hasattr(__main__, 'testing_predictions'):
        __main__.testing_predictions = predictions
except Exception:
    pass

model.save('health_cost_model.h5')
