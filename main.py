from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity, ReplyKeyboardMarkup

import vk_api
from vk_api.audio import VkAudio

import logging

from threading import Thread

import time

from config import *




def start(update, context):
    keyboard = [[InlineKeyboardButton('Help', callback_data='menu_help'),
    			 InlineKeyboardButton('Settings', callback_data='menu_settings')]]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text("Hello, I'm vk-music-bot.", reply_markup=reply_markup)


def search_audios(update, context):
	global playlist_type
	global vk_session
	global searched_tracks
	global playlist_page

	playlist_page = 1

	update.message.reply_text('Searching...')


	vkaudio = VkAudio(vk_session)
	searched_tracks = list(vkaudio.search(update.message.text))


	playlist_type = 'searched'

	playlist = make_playlist(playlist_type)
	update.message.reply_text('Playlist:', reply_markup=playlist)


def get_audio_by_link(update, context):
	global playlist_type
	global vk_session
	global vk
	global user_tracks
	global playlist_page

	playlist_page = 1


	loop_message = update.message.reply_text('Wait a few seconds...')


	owner_id = update.message.text
	response = vk.utils.resolveScreenName(screen_name=owner_id.split('/')[-1])
	owner_id = response['object_id']

	vkaudio = VkAudio(vk_session) 
	
	try:
		user_tracks = vkaudio.get(owner_id=owner_id)
	except:
		update.message.reply_text("User's audios are closed.")


	playlist_type = 'user'

	playlist = make_playlist(playlist_type)
	update.message.reply_text('Playlist:', reply_markup=playlist)




def download_track(update, context):
	print ('Working##############################################')
	global user_tracks
	global searched_tracks


	if playlist_type == 'user':
		query = update.callback_query

		track_id = int(query.data.split('_')[-1])


		context.bot.send_audio(
			chat_id=query.message.chat_id, 
			audio=user_tracks[track_id]['url'],
			caption=user_tracks[track_id]['artist']+'\n'+user_tracks[track_id]['title']
			)
	elif playlist_type == 'searched':
		query = update.callback_query

		track_id = int(query.data.split('_')[-1])


		context.bot.send_audio(
			chat_id=query.message.chat_id, 
			audio=searched_tracks[track_id]['url'],
			caption=searched_tracks[track_id]['artist']+'\n'+searched_tracks[track_id]['title']
			)		


def swipe_tracks(update, context):
	global playlist_page
	global user_tracks
	global playlist_type



	query = update.callback_query

	if (playlist_page == 1) & (query.data == 'swipe_left'):
		error_msg = 'error'
		return error_msg
	else:
		if query.data == 'swipe_left':
			playlist_page -= 1
			playlist = make_playlist(playlist_type)
			if playlist == 'error':
				playlist_page += 1
				print (playlist)
			else:
				query.edit_message_reply_markup(reply_markup=playlist)
		elif query.data == 'swipe_right':
			playlist_page += 1
			playlist = make_playlist(playlist_type)

			if playlist == 'error':
				playlist_page -= 1
				print (playlist)
			else:
				query.edit_message_reply_markup(reply_markup=playlist)
		return 0		




def make_playlist(playlist_type):
	global playlist_page

	if playlist_type == 'user':
		global user_tracks
		keyboard = []
		track_count = len(user_tracks)
		page_count = track_count/10 if (track_count%10)==0 else (track_count//10)+1

		print ('##########################################################################')
		print (track_count, page_count)
		print (playlist_page)
		print ('##########################################################################')

		if playlist_page <= page_count:
			if (track_count-10*(playlist_page-1)) >= 10:
				for i in range(10*(playlist_page-1), 10*(playlist_page-1)+10):
					keyboard.append([InlineKeyboardButton(user_tracks[i]['artist']+' - '+user_tracks[i]['title'], 
													callback_data='track_'+str(i))])
			elif (track_count-10*(playlist_page-1)) == 0:
				error_msg = 'error'
				return error_msg
			else:
				for i in range(track_count):
					keyboard.append([InlineKeyboardButton(user_tracks[i]['artist']+'-'+user_tracks[i]['title'], 
													callback_data='track_'+str(i))])
		else:
			error_msg = 'error'
			return error_msg


		
		keyboard.append([InlineKeyboardButton(u'\U000025C0', callback_data='swipe_left'),
	                 InlineKeyboardButton(u'\U000025B6', callback_data='swipe_right')])

		reply_markup = InlineKeyboardMarkup(keyboard)

		return reply_markup

	elif playlist_type == 'searched':
		global searched_tracks
		keyboard = []

		#print ('##########################################################################')
		#print (track_count, page_count)
		#print (playlist_page)
		#print ('##########################################################################')

		for i in range(10*(playlist_page-1), 10*(playlist_page-1)+10):
			keyboard.append([InlineKeyboardButton(searched_tracks[i]['artist']+'-'+searched_tracks[i]['title'], 
								callback_data='track_'+str(i))])


		keyboard.append([InlineKeyboardButton(u'\U000025C0', callback_data='swipe_left'),
	                 InlineKeyboardButton(u'\U000025B6', callback_data='swipe_right')])

		reply_markup = InlineKeyboardMarkup(keyboard)

		return reply_markup


def main():
	logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


	updater = Updater(token=tg_bot_token, use_context=True)
	dispatcher = updater.dispatcher

	start_handler = CommandHandler('start', start)

	link_handler = MessageHandler(
						Filters.text & (Filters.entity(MessageEntity.URL) |
	                    Filters.entity(MessageEntity.TEXT_LINK)), get_audio_by_link)

	search_audios_handler = MessageHandler(Filters.text, search_audios)

	track_buttons_handler = CallbackQueryHandler(download_track, pattern=r'track_\d+')

	swipe_buttons_handler = CallbackQueryHandler(swipe_tracks, pattern=r'swipe_(left|right)')


	dispatcher.add_handler(start_handler)
	dispatcher.add_handler(link_handler)
	dispatcher.add_handler(search_audios_handler)
	dispatcher.add_handler(track_buttons_handler)
	dispatcher.add_handler(swipe_buttons_handler)

	updater.start_polling()


if __name__ == '__main__':
	playlist_page = 1

	user_tracks = ''
	searched_tracks = ''

	playlist_type = ''

	vk_session = vk_api.VkApi(vk_login, vk_pass)
	try:
	    vk_session.auth()
	except vk_api.AuthError as error_msg:
	    print(error_msg)

	vk = vk_session.get_api()
	main()