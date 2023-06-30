from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(int, env.list("ADMINS")))
DB_NAME = env.str("DB_NAME")
DB_USER = env.str("DB_USER")
DB_PASSWORD = env.str("DB_PASSWORD")
DB_HOST = env.str("DB_HOST")
DB_PORT = env.str("DB_PORT")
