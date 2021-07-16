import random
import string


def random_generator_id():
    random_id = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    return random_id


def generate_otp():
    pin = ''.join(random.choice('0123456789') for _ in range(6))
    return pin


if __name__ == "__main__":
    m = generate_otp()
    print(m)