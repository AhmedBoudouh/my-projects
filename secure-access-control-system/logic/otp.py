import random

SECRET_KEY = "Z9" #uUsed for calculate OTP

def generate_otp_from_x(x):# Generate a OTP (4 numbers) using the random X and a secret key
    
    key_value = sum(ord(c) for c in SECRET_KEY) % 100
    otp = (x * 31 + key_value * 17) % 10000
    return str(otp).zfill(4)

def generate_otp_cloud(x):  # Create a list (cloud) of 5 OTP including real one
    real_otp = generate_otp_from_x(x)
    cloud = set()
    cloud.add(real_otp)
    while len(cloud) < 5:
        fake = str(random.randint(0, 9999)).zfill(4)
        cloud.add(fake)
    cloud_list = list(cloud)
    random.shuffle(cloud_list)
    return cloud_list, real_otp  
