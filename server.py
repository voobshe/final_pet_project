from bot import LisaBot
from bot_key import BOT_KEY

def main():
    global BOT_KEY
    #TODO добавить катюшин обработчик изображений
    bot = LisaBot(BOT_KEY, 0)
    bot.run()
    exit(0)

if __name__ == '__main__':
    ret = main()
    exit(ret)