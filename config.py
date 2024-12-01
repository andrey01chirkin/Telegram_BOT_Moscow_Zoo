import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN') #Переменной Token присвойте Ваш токен
admin_list = [int(os.getenv('ADMIN_ID'))] #Перечислите в списке id админов для доступа к админ панели






