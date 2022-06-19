# -*- coding: utf-8 -*-

from aiogram import Bot, Dispatcher, executor
from tinydb import TinyDB, Query

db = TinyDB('db.json')
Mods = Query()

template = {
	"name": None,
	"downloads": 0,
	"uploads": 0,
	"stat": []
}

template_stat = {
	"time": None,
	"state": None,
}

bot_token = ''
bot = Bot(token=bot_token)


dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message):
	await message.reply("Привет, тут статистика установок/удалений модулей с @vsecoder_m")

@dp.message_handler(content_types=['text'])
async def parse_text(message):
	args = message.text.split(' ')

	if len(args) >= 2:
		if db.search(Mods.name == args[1]):
			if args[0] == '/download':
				stat = db.search(Mods.name == args[1])[0]['stat']
				t = template_stat
				t['state'] = 'download'
				t['time'] = str(message.date)
				stat.append(t)
				downloads = db.search(Mods.name == args[1].lower())[0]["downloads"] + 1
				db.update({'downloads': downloads}, Mods.name == args[1])
				db.update({'stat': stat}, Mods.name == args[1])
			if args[0] == '/upload':
				stat = db.search(Mods.name == args[1])[0]['stat']
				t = template_stat
				t['state'] = 'upload'
				t['time'] = str(message.date)
				stat.append(t)
				uploads = db.search(Mods.name == args[1].lower())[0]["uploads"] + 1
				db.update({'uploads': uploads}, Mods.name == args[1])

	if int(message.from_user.id) == 1218845111:
		if args[0] == '/add':
			if len(args) == 1:
				await message.reply("Не указано имя модуля")
			else:
				if db.search(Mods.name == args[1].lower()):
					return await message.reply("Модуль с таким именем уже существует")
				module = template
				module['name'] = args[1].lower()
				db.insert(module)
		if args[0] == '/db':
			await bot.send_document(message.chat.id, ('db.json',open('db.json', 'rb')))

if __name__ == "__main__":
	executor.start_polling(dp)