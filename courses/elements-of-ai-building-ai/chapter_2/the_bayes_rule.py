def bot8(pbot, p8_bot, p8_human):
    p8 = p8_bot * pbot + p8_human * (1-pbot)
    pbot_8 = pbot * p8_bot / p8
    print(pbot_8)

# you can change these values to test your program with different values
pbot = 0.1
p8_bot = 0.8
p8_human = 0.05

bot8(pbot, p8_bot, p8_human)
