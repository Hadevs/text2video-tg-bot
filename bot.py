from pickle import TRUE
import telebot;
import replicate;
import os;

bot = telebot.TeleBot('5891533811:AAFCWgHoJkssbbJvpl25c-D0Pqo-jsG8HqI');

x = True
starting = ""
ending = ""

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(
        message.chat.id, 
        'Привет! Чтобы сгенерировать видео нужно задать начальную и финальную сцены. Напишите сначала начальную сцену.'
    )
	
@bot.message_handler(content_types=['text'])
def generate(message):
	global x, starting, ending
	if x == True:
		bot.send_message(message.chat.id, 'Теперь введите конечную сцену и вы получите видео')
		starting = message.text
		x = False
	else:
		ending = message.text
		images = generate_video_with_ai(starting,ending,message)
		for image in images:
			print("new result is:", image)
			bot.send_video(message.chat.id, image, caption= str(message.text) + ' было сгенерировано с помощью https://t.me/AiTextImagebot')
			bot.send_message(message.chat.id, 'Чтобы сгенерировать видео введите описание первой сцены')
		x = True
    
def generate_video_with_ai(start_scene, end_scene,message):
	try:
		model = replicate.models.get("andreasjansson/stable-diffusion-animation")
		version = model.versions.get("ca1f5e306e5721e19c473e0d094e6603f0456fe759c10715fcd6c1b79242d4a5")
		output = version.predict(prompt_start = start_scene, prompt_end = end_scene, output_format="mp4", gif_frames_per_second = "20", gif_ping_pong = True, guidance_scale = 7.5, prompt_strength = 0.9, film_interpolation = True,num_inference_steps = 50, num_animation_frames = 25, num_interpolation_steps =  5)
		print("result is:", output)
		return output
	except replicate.exceptions.ModelError:
		bot.send_message(
        message.chat.id, 
        'Кажется, что данный запрос содержит 18+ контент. Попробуйте еще раз или измените запрос.'
    )
	
	
bot.polling(none_stop=True, interval=0)

