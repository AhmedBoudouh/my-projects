import random

def build_pin_train(real_pin): #build the train
    if len(real_pin) != 4 or not real_pin.isdigit():
        raise ValueError("PIN must be 4 digits")

    train = [''] * 8

    # chose 4 randomly position
    positions = random.sample(range(8), 4)

    # Put the numbers of pin in their position in order 
    for i, pos in enumerate(positions):
        train[pos] = real_pin[i]

    # Fill the other position with random numbers
    for i in range(8):
        if train[i] == '':
            train[i] = str(random.randint(0, 9))

    return train, positions
# extraction of numbers of pin from "train"
def extract_pin_from_train(train, positions):
    return ''.join([train[pos] for pos in positions])