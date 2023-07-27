import telebot, datetime
import config
import dbfunc
bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "+":
        # проверим написано сообщение в ответ или нет
        try:
            reply_to_message_user_id = str(message.reply_to_message.from_user.id)  # Получим id пользователя
            reply_to_message_username = message.reply_to_message.from_user.username  # Получим имя пользователя
        except AttributeError:
            bot.send_message(message.chat.id, "Поставьте + в ответ на сообщение")
            reply_to_message_user_id = 0
        if reply_to_message_user_id != 0:
            # добавим пользователя в базу, insert_user_into_users проверит сама наличие пользователя в базе
            add_user = dbfunc.insert_user_into_users(reply_to_message_username, reply_to_message_user_id)
            # если add_user=2, то произошла ошибка на этапе создания пользователя
            if add_user != 2:
                message_date = str(datetime.datetime.today())  # получим дату для вставки в таблицу наград
                reply_message_user_id = str(message.from_user.id)  # получим id пользователя, который ставит +
                if reply_to_message_user_id != reply_message_user_id:
                    #проверим кто ставит +, самому себе ставить + нельзя
                    reward = dbfunc.add_user_reward(reply_to_message_user_id, 1, message_date[:-7])
                    # при reward = 0 значит не удалось поставить награду
                    if reward != 0:
                        kpi = dbfunc.select_top_kpi(reply_to_message_user_id)
                        #level_up_down(tg_user_id) чтобы получить уровень или потерять его
                        level = dbfunc.level_up_down(reply_to_message_user_id)
                        ans = "Репутация увеличена на 1 " + str(
                            message.reply_to_message.from_user.username) + " " + "(" + str(kpi) + ")" + level
                        bot.send_message(message.chat.id, ans)
                    else:
                        ans = "Не получилось, упс. " + str(message.reply_to_message.from_user.username)
                        bot.send_message(message.chat.id, ans)
                else:
                    bot.send_message(message.chat.id, 'себе + ставить нельзя')
            else:  # add_user = 2
                bot.send_message(message.chat.id, "не смог добавить пользователя")

    if message.text == "спасибо":
        # проверим написано сообщение в ответ или нет
        try:
            reply_to_message_user_id = str(message.reply_to_message.from_user.id)  # Получим id пользователя
            reply_to_message_username = message.reply_to_message.from_user.username  # Получим имя пользователя
        except AttributeError:
            bot.send_message(message.chat.id, "Поставьте + в ответ на сообщение")
            reply_to_message_user_id = 0
        if reply_to_message_user_id != 0:
            # добавим пользователя в базу, insert_user_into_users проверит сама наличие пользователя в базе
            add_user = dbfunc.insert_user_into_users(reply_to_message_username, reply_to_message_user_id)
            # если add_user=2, то произошла ошибка на этапе создания пользователя
            if add_user != 2:
                message_date = str(datetime.datetime.today())  # получим дату для вставки в таблицу наград
                reply_message_user_id = str(message.from_user.id)  # получим id пользователя, который ставит +
                if reply_to_message_user_id != reply_message_user_id:
                    # проверим кто ставит +, самому себе ставить + нельзя
                    reward = dbfunc.add_user_reward(reply_to_message_user_id, 1, message_date[:-7])
                    # при reward = 0 значит не удалось поставить награду
                    if reward != 0:
                        kpi = dbfunc.select_top_kpi(reply_to_message_user_id)
                        #level_up_down(tg_user_id) чтобы получить уровень или потерять его
                        level = dbfunc.level_up_down(reply_to_message_user_id)
                        ans = "Репутация увеличена на 1 " + str(
                            message.reply_to_message.from_user.username) + " " + "(" + str(kpi) + ")" + level
                        bot.send_message(message.chat.id, ans)
                    else:
                        ans = "Не получилось, упс. " + str(message.reply_to_message.from_user.username)
                        bot.send_message(message.chat.id, ans)
                else:
                    bot.send_message(message.chat.id, 'себе + ставить нельзя')
            else:  # add_user = 2
                bot.send_message(message.chat.id, "не смог добавить пользователя")

    if message.text == "/help":
        bot.send_message(message.chat.id, "я считаю карму")

    if message.text == "-":# поставили минус
        # проверим написано сообщение в ответ или нет
        try:
            # Получим id пользователя, которому -
            reply_to_message_user_id = str(message.reply_to_message.from_user.id)
            # Получим имя пользователя, которому -
            reply_to_message_username = message.reply_to_message.from_user.username
        except AttributeError:
            # если сообщение отправлено не в ответ
            bot.send_message(message.chat.id, "Поставьте + в ответ на сообщение")
            reply_to_message_user_id = 0
        if reply_to_message_user_id != 0:
            # добавим пользователя в базу, insert_user_into_users проверит сама наличие пользователя в базе
            add_user = dbfunc.insert_user_into_users(reply_to_message_username, reply_to_message_user_id)
            # если add_user=2, то произошла ошибка на этапе создания пользователя
            if add_user != 2:
                message_date = str(datetime.datetime.today())  # получим дату для вставки в таблицу наград
                # получим id пользователя, который ставит '-' для проверки на админа и запрету ставить '-' себе
                reply_message_user_id = str(message.from_user.id)
                is_admin = dbfunc.is_user_admin(reply_message_user_id)
                if is_admin == 1:
                    if reply_to_message_user_id != reply_message_user_id:  # рповерим кто ставит +, самому себе ставить + нельзя
                        reward = dbfunc.add_user_reward(reply_to_message_user_id, -1, message_date[:-7])
                        # при reward = 0 значит не удалось поставить награду
                        if reward != 0:
                            kpi = dbfunc.select_top_kpi(reply_to_message_user_id)
                            level = dbfunc.level_up_down(reply_to_message_user_id)
                            ans = "Репутация уменьшена на 1 " + str(
                                message.reply_to_message.from_user.username) + " " + "(" + str(kpi) + ")"  + level
                            bot.send_message(message.chat.id, ans)
                        else:
                            ans = "Не получилось, упс. " + str(message.reply_to_message.from_user.username)
                            bot.send_message(message.chat.id, ans)
                    else:
                        bot.send_message(message.chat.id, 'себе - ставить нельзя')
                else:
                    bot.send_message(message.chat.id, 'Понижать авторитет может только SuperViser чата')
            else:  # add_user = 2
                bot.send_message(message.chat.id, "не смог добавить пользователя")

    if message.text == "/profile":# покажем всю информацию о пользователе
        reply_message_user_id = str(message.from_user.id)# получим id пользователя
        request = dbfunc.profile(reply_message_user_id)
        level_now = dbfunc.select_user_level_from_users(reply_message_user_id)
        top_skills = ''
        for el in request:
            top_skills = top_skills + el[1] + '\n'
        bot.send_message(message.chat.id, "Ваш уровень = " + str(level_now)  + '\n' + "Список ваших навыков: "+ '\n' + top_skills )#


bot.polling(none_stop=True, interval=0)