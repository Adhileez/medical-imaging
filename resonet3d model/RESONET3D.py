from keras.layers import Input, Conv3D, MaxPooling3D, Conv3DTranspose, concatenate, Dropout, Activation, BatchNormalization, add, Multiply, Lambda
from keras.models import Model
import keras.backend as K
import keras

def attention_gate(input, gating_signal, inter_channels):
    theta_x = Conv3D(inter_channels, (2, 2, 2), strides=(2, 2, 2), padding='same')(input)
    phi_g = Conv3D(inter_channels, (1, 1, 1), padding='same')(gating_signal)
    add_xg = add([theta_x, phi_g])
    act_xg = Activation('relu')(add_xg)
    psi = Conv3D(1, (1, 1, 1), padding='same', activation='sigmoid')(act_xg)
    upsample_psi = Conv3DTranspose(1, (2, 2, 2), strides=(2, 2, 2), padding='same')(psi)
    output = Multiply()([input, upsample_psi])
    return output

def ResoNet3D(IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH, IMG_CHANNELS, num_classes):
    inputs = Input((IMG_HEIGHT, IMG_WIDTH, IMG_DEPTH, IMG_CHANNELS))
    s = inputs

    def res_block(x, n_filters, dropout):
        res = Conv3D(n_filters, (3, 3, 3), activation=None, kernel_initializer='he_normal', padding='same')(x)
        res = BatchNormalization()(res)
        res = Activation('relu')(res)
        res = Conv3D(n_filters, (3, 3, 3), activation=None, kernel_initializer='he_normal', padding='same')(res)
        res = BatchNormalization()(res)
        shortcut = Conv3D(n_filters, (1, 1, 1), activation=None, kernel_initializer='he_normal', padding='same')(x)
        shortcut = BatchNormalization()(shortcut)
        res = add([shortcut, res])
        res = Activation('relu')(res)
        if dropout > 0:
            res = Dropout(dropout)(res)
        return res

    c1 = res_block(s, 16, 0.1)
    p1 = MaxPooling3D((2, 2, 2))(c1)
    c2 = res_block(p1, 32, 0.1)
    p2 = MaxPooling3D((2, 2, 2))(c2)
    c3 = res_block(p2, 64, 0.2)
    p3 = MaxPooling3D((2, 2, 2))(c3)
    c4 = res_block(p3, 128, 0.2)
    p4 = MaxPooling3D((2, 2, 2))(c4)
    c5 = res_block(p4, 256, 0.3)

    u6 = Conv3DTranspose(128, (2, 2, 2), strides=(2, 2, 2), padding='same')(c5)
    u6 = concatenate([u6, c4])
    u6 = attention_gate(u6, c5, 128)
    c6 = res_block(u6, 128, 0.2)
    u7 = Conv3DTranspose(64, (2, 2, 2), strides=(2, 2, 2), padding='same')(c6)
    u7 = concatenate([u7, c3])
    u7 = attention_gate(u7, c6, 64)
    c7 = res_block(u7, 64, 0.2)
    u8 = Conv3DTranspose(32, (2, 2, 2), strides=(2, 2, 2), padding='same')(c7)
    u8 = concatenate([u8, c2])
    u8 = attention_gate(u8, c7, 32)
    c8 = res_block(u8, 32, 0.1)
    u9 = Conv3DTranspose(16, (2, 2, 2), strides=(2, 2, 2), padding='same')(c8)
    u9 = concatenate([u9, c1])
    u9 = attention_gate(u9, c8, 16)
    c9 = res_block(u9, 16, 0.1)

    outputs = Conv3D(num_classes, (1, 1, 1), activation='softmax')(c9)
    model = Model(inputs=[inputs], outputs=[outputs])
    model.summary()

    return model

model = ResoNet3D(128, 128, 128, 3, 4)
print(model.input_shape)
print(model.output_shape)

