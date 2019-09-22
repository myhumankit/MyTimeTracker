from random import choice

secret_key = "".join(
    [choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]
)

print(secret_key)
