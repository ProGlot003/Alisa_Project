from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)
import translate

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')

Session_data = {}
current_status = "start"
current_dialog = "start"
dialog_sport = None
flag = False
flag_end_football = False
mood_alisa = 10
score_ronaldo = 0
question_1 = False
question_2 = False
question_3 = False
question_4 = False
question_5 = False
flag_leo = False
flag_info_ney = False
not_test_ron = 1
current_status_1 = None
knowledge_about_ney = ["очень знаменитый", "хороший футболист", "играет в PSG",
                       "играет в ПСЖ"]
topic_alisa = ["talk_sport", "translate", "gallery", "city"]


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    main_dialog(response, request.json)

    logging.info('Request: %r', response)

    return json.dumps(response)


def main_dialog(res, req):
    global current_status, current_dialog, Session_data, dialog_sport, flag, flag_end_football, mood_alisa, \
        score_ronaldo, question_1, question_2, question_3, question_4, question_5, not_test_ron, knowledge_about_ney, \
        flag_leo, flag_info_ney, topic_alisa, current_status_1

    user_id = req['session']['user_id']
    if current_dialog == "start":
        if req['session']['new']:
            res['response']['text'] = 'Привет! '
            Session_data[user_id] = {
                'suggests': [],
                'username': "Пользователь"
            }

            return
        if current_status == "start":
            res['response']['text'] = 'О чем хочешь поговорить?'
            current_status = "start_question"
            Session_data[user_id] = {
                'suggests': [
                    "Давай о спорте.",
                    "Просто поболтать.",
                    "Вопросы по городам.",
                    "Покажи города.",
                    "Не знаю, выбери сама.",
                ],
                'username': "Пользователь"
            }
            Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?', 'Чем занимаешься?']

            res['response']['buttons'] = get_suggests(user_id)
            return

        if current_status == "start_question":
            if req['request']['original_utterance'].lower() in ['давай о спорте.', 'спорт.', 'спорте', 'спорте.',
                                                                'давай о спорте.', 'давай о спорте', 'спортом',
                                                                'спортом.']:
                current_status = "talk_sport"
                res['response']['text'] = 'Отлично! О каком спорте поговорим?'
                Session_data[user_id] = {
                    'suggests': [
                        "Футбол",
                        "Баскетбол.",
                        "Хоккей.",
                    ],
                    'username': "Пользователь"
                }

                res['response']['buttons'] = get_suggests(user_id)
                return
        if current_status == "talk_sport":
            if req['request']['original_utterance'].lower() in ['футбол', 'футболе.', 'футболом', 'футбол.',
                                                                'футболе.', 'Футболом.']:
                res['response']['text'] = 'Этот спорт мне нравится больше всего. Кто твой любимый футболист?'
                dialog_sport = 'football'
                Session_data[user_id] = {
                    'suggests': [
                        "Месси.",
                        "Роналду.",
                        "Неймар.",
                    ],
                    'username': "Пользователь"

                }

                res['response']['buttons'] = get_suggests(user_id)
                return
            if dialog_sport == 'football':
                if req['request']['original_utterance'].lower() in ['месси', 'месси.', 'лео.', 'лео', 'лионель',
                                                                    'лионель.', 'лионель месси.''лионель месси',
                                                                    'меси.', 'меси']:
                    res['response'][
                        'text'] = 'Мне он тоже нравится больше всех. Он просто' \
                                  ' гений. Хочешь покажу его самое красивое фото?'
                    dialog_sport = 'football_messi'
                    Session_data[user_id] = {
                        'suggests': [
                            "Да, давай.",
                            "Нет, не надо.",
                        ],
                        'username': "Пользователь"

                    }

                    res['response']['buttons'] = get_suggests(user_id)
                    return
            if dialog_sport == 'football_messi':
                if req['request']['original_utterance'].lower() in ['да', 'давай.', 'почему бы и нет', 'ага', 'угу',
                                                                    'да, давай.']:
                    res['response']['text'] = 'Тогда напиши:"ЛеоМесси"'
                    flag_leo = True
                    return
                if not flag_leo and req['request']['original_utterance'].lower() not in ['да', 'давай.',
                                                                                         'почему бы и нет', 'ага',
                                                                                         'угу',
                                                                                         'да, давай.']:
                    current_status = "start"
                    res['response']['text'] = 'Тогда давай переключим тему.'
                    # mood_alisa -= 1
                    Session_data[user_id] = {
                        'suggests': [
                            "Просто поболтать.",
                            "Вопросы по городам.",
                            "Покажи города.",
                            "Не знаю, выбери сама.",
                        ],
                        'username': "Пользователь"
                    }
                    Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                      'Чем занимаешься?']

                    res['response']['buttons'] = get_suggests(user_id)
                    return

                if dialog_sport == 'football_messi' and flag_leo and not flag and not flag_end_football:
                    res['response']['card'] = {}
                    res['response']['card']['type'] = 'BigImage'
                    res['response']['card']['title'] = 'Месси. Понравилось?'
                    res['response']['card']['image_id'] = '1652229/5ba76fc57d55506fdb93'
                    res['response']['text'] = 'Понравилось?'
                    flag = False
                    flag_end_football = True
                    Session_data[user_id] = {
                        'suggests': [
                            "Да.",
                            "Нет.",
                        ],
                        'username': "Пользователь"

                    }

                    res['response']['buttons'] = get_suggests(user_id)
                    return
                if dialog_sport == 'football_messi' and flag_end_football:
                    if req['request']['original_utterance'].lower() in ['да.', 'да', 'ага', 'угу', 'очень',
                                                                        'еще бы']:
                        res['response']['text'] = 'Я старалась:) Давай сменим тему.'
                        # mood_alisa += 1
                        current_status = "start_question"
                        Session_data[user_id] = {
                            'suggests': [
                                "Просто поболтать.",
                                "Вопросы по городам.",
                                "Покажи города.",
                                "Не знаю, выбери сама.",
                            ],
                            'username': "Пользователь"
                        }
                        Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                          'Чем занимаешься?']

                        res['response']['buttons'] = get_suggests(user_id)
                        return
                    if dialog_sport == 'football_messi' and flag_end_football:
                        if req['request']['original_utterance'].lower() in ['нет.', 'нет', 'не-а', 'ноу', 'не очень']:
                            res['response']['text'] = 'Всем не угодишь, а я ведь старалась:( Давай сменим тему.'
                            # mood_alisa -= 1
                            current_status = "start_question"
                            Session_data[user_id] = {
                                'suggests': [
                                    "Просто поболтать.",
                                    "Вопросы по городам.",
                                    "Покажи города.",
                                    "Не знаю, выбери сама.",
                                ],
                                'username': "Пользователь"
                            }
                            Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                              'Чем занимаешься?']

                            res['response']['buttons'] = get_suggests(user_id)
                            return
            if dialog_sport == 'football':
                if req['request']['original_utterance'].lower() in ['роналду', 'роналду.', 'криш.', 'криро',
                                                                    'криштиану',
                                                                    'криштиану роналду.']:
                    dialog_sport = 'football_ronaldo'
                    res['response'][
                        'text'] = 'На мой взгляд, Лео лучше, но о нём я тоже смогу поддержать разговор. Хочешь' \
                                  ' узнать о том, как хорошо ты о нем знаешь?'
                    Session_data[user_id] = {
                        'suggests': [
                            "Да, давай.",
                            "Нет, не хочу.",
                        ],
                        'username': "Пользователь"

                    }

                    res['response']['buttons'] = get_suggests(user_id)
                    return
            if current_status == "talk_sport" and dialog_sport == 'football_ronaldo':
                if req['request']['original_utterance'].lower() in ['да, давай.', 'да',
                                                                    'ага.',
                                                                    'ага',
                                                                    'угу',
                                                                    'угу.']:
                    res['response'][
                        'text'] = 'Хорошо. В тесте будет 5 вопрос, за каждый правильный дается один балл,' \
                                  ' за каждый неправильный снимается балл. Первый вопрос: В каком' \
                                  ' году Роналдо стал выступать за Манчестер Юнайтед?'
                    question_1 = True
                    not_test_ron = 0
                    dialog_sport = 'football_ronaldo_test'
                    Session_data[user_id] = {
                        'suggests': [
                            "2003",
                            "2009",
                            "2018",
                            "он там не выступал",
                        ],
                        'username': "Пользователь"

                    }

                    res['response']['buttons'] = get_suggests(user_id)
                    return
                if req['request']['original_utterance'].lower() not in ['да, давай.', 'да',
                                                                        'ага.',
                                                                        'ага',
                                                                        'угу',
                                                                        'угу.']:
                    res['response'][
                        'text'] = 'Большего' \
                                  ' о нём я не знаю, поэтому давай переключать тему.'
                    current_status = "start_question"
                    Session_data[user_id] = {
                        'suggests': [
                            "Просто поболтать.",
                            "Вопросы по городам.",
                            "Покажи города.",
                            "Не знаю, выбери сама.",
                        ],
                        'username': "Пользователь"
                    }
                    Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                      'Чем занимаешься?']

                    res['response']['buttons'] = get_suggests(user_id)
                    return

            if question_1 and dialog_sport == 'football_ronaldo_test' and req['request'][
                'original_utterance'].lower() in [
                '2003', 'две тысячи третий', 'две тысячи третьем', 'две тысячи третьем году',
            ]:
                score_ronaldo += 1
                res['response'][
                    'text'] = 'Это правильный ответ. Переходим ко 2 вопросу. Сколько лет он выступал' \
                              ' за этот клуб?'
                Session_data[user_id] = {
                    'suggests': [
                        "6",
                        "8",
                        "9",
                        "он и сейчас там выступает",
                    ],
                    'username': "Пользователь"

                }
                question_1 = False
                question_2 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_1 and dialog_sport == 'football_ronaldo_test' and req['request'][
                'original_utterance'].lower() not in [
                '2003', 'две тысячи третий', 'две тысячи третьем', 'две тысячи третьем году',
            ]:
                if score_ronaldo > 0:
                    score_ronaldo -= 1
                else:
                    score_ronaldo = 0
                res['response'][
                    'text'] = 'Это неправильный ответ. Переходим ко 2 вопросу. Сколько лет он выступал' \
                              ' за этот клуб?'
                Session_data[user_id] = {
                    'suggests': [
                        "6",
                        "8",
                        "9",
                        "он и сейчас там выступает",
                    ],
                    'username': "Пользователь"

                }

                question_1 = False
                question_2 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_2 and req['request'][
                'original_utterance'].lower() in [
                '6', 'шесть', 'шесть лет', 'лет шесть',
            ]:
                score_ronaldo += 1
                res['response'][
                    'text'] = 'Это правильный ответ. Переходим ко 3 вопросу.Сколько золотых мячей он выиграл?'
                Session_data[user_id] = {
                    'suggests': [
                        "4",
                        "5",
                        "6",
                        "Ни одного",
                    ],
                    'username': "Пользователь"

                }
                question_2 = False
                question_3 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_2 and req['request'][
                'original_utterance'].lower() not in [
                '6', 'шесть', 'шесть лет', 'лет шесть',
            ]:
                if score_ronaldo > 0:
                    score_ronaldo -= 1
                else:
                    score_ronaldo = 0
                res['response'][
                    'text'] = 'Это неправильный ответ. Переходим ко 3 вопросу.Сколько золотых мячей он выиграл?'
                Session_data[user_id] = {
                    'suggests': [
                        "4",
                        "5",
                        "6",
                        "Ни одного",
                    ],
                    'username': "Пользователь"

                }
                question_2 = False
                question_3 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_3 and req['request'][
                'original_utterance'].lower() in [
                '5', 'пять', 'пять лет', 'лет пять',
            ]:
                score_ronaldo += 1
                res['response'][
                    'text'] = 'Это правильный ответ. Переходим ко 4 вопросу. В каком году он выиграл первый ЗМ?'
                Session_data[user_id] = {
                    'suggests': [
                        "2006",
                        "2016",
                        "2009",
                        "2008",
                    ],
                    'username': "Пользователь"

                }
                question_3 = False
                question_4 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_3 and req['request'][
                'original_utterance'].lower() not in [
                '5', 'пять', 'пять лет', 'лет пять',
            ]:
                if score_ronaldo > 0:
                    score_ronaldo -= 1
                else:
                    score_ronaldo = 0
                res['response'][
                    'text'] = 'Это неправильный ответ. Переходим ко 4 вопросу. В каком году он выиграл первый ЗМ?'
                Session_data[user_id] = {
                    'suggests': [
                        "2006",
                        "2016",
                        "2009",
                        "2008",
                    ],
                    'username': "Пользователь"

                }
                question_3 = False
                question_4 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_4 and req['request'][
                'original_utterance'].lower() not in [
                '2008', 'две тысячи восьмой', 'в две тысячи восьмом', 'две тысячи восьмой год',
            ]:
                if score_ronaldo > 0:
                    score_ronaldo -= 1
                else:
                    score_ronaldo = 0
                res['response'][
                    'text'] = 'Это неправильный ответ. Переходим ко 5 вопросу. Где этот игрок играет сейчас?'
                Session_data[user_id] = {
                    'suggests': [
                        "Реал Мадрид",
                        "Ювентус",
                        "Барселона",
                        "Манчестер Юнайтед",
                    ],
                    'username': "Пользователь"

                }
                question_4 = False
                question_5 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_4 and req['request'][
                'original_utterance'].lower() in [
                '2008', 'две тысячи восьмой', 'в две тысячи восьмом', 'две тысячи восьмой год',
            ]:
                score_ronaldo += 1
                res['response'][
                    'text'] = 'Это правильный ответ. Переходим ко 5 вопросу. Где этот игрок играет сейчас?'
                Session_data[user_id] = {
                    'suggests': [
                        "Реал Мадрид",
                        "Ювентус",
                        "Барселона",
                        "Манчестер Юнайтед",
                    ],
                    'username': "Пользователь"

                }
                question_4 = False
                question_5 = True

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_5 and req['request'][
                'original_utterance'].lower() in [
                'Ювентус', 'Юве', 'В Ювентусе', 'В Юве',
            ]:
                score_ronaldo += 1
                res['response'][
                    'text'] = 'Это правильный ответ. Вот твои баллы: ' + str(
                    score_ronaldo) + 'Ты доволен результатами?'
                Session_data[user_id] = {
                    'suggests': [
                        "Да, очень",
                        "Нет",
                    ],
                    'username': "Пользователь"

                }
                question_5 = False

                res['response']['buttons'] = get_suggests(user_id)
                return
            if question_5 and req['request'][
                'original_utterance'].lower() not in [
                'Ювентус', 'Юве', 'В Ювентусе', 'В Юве',
            ]:
                if score_ronaldo > 0:
                    score_ronaldo -= 1
                else:
                    score_ronaldo = 0
                res['response'][
                    'text'] = 'Это неправильный ответ. Вот твои баллы: ' + str(
                    score_ronaldo) + 'Ты доволен результатами?'
                Session_data[user_id] = {
                    'suggests': [
                        "Да, очень",
                        "Нет",
                    ],
                    'username': "Пользователь"

                }
                question_5 = False
                not_test_ron = 5
                res['response']['buttons'] = get_suggests(user_id)
                return
            if not_test_ron == 5:
                if req['request']['original_utterance'].lower() in [
                    'да, очень', 'да', 'очень', 'ага',
                ]:
                    res['response'][
                        'text'] = 'Отлично, поздравляю, ты молодец! Большего' \
                                  ' о нём я не знаю, поэтому давай переключать тему.'
                    current_status = "start_question"
                    Session_data[user_id] = {
                        'suggests': [
                            "Просто поболтать.",
                            "Вопросы по городам.",
                            "Покажи города.",
                            "Не знаю, выбери сама.",
                        ],
                        'username': "Пользователь"
                    }
                    Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                      'Чем занимаешься?']

                    res['response']['buttons'] = get_suggests(user_id)
                    return
            if dialog_sport == 'football':
                if req['request']['original_utterance'].lower() in ['неймар', 'неймар.', 'ней.']:
                    dialog_sport = 'football_neymar'
                    res['response'][
                        'text'] = 'Его я знаю плохо. Расскажи ' \
                                  'мне что-нибудь о нем в нескольких сообщениях. Надеюсь ты сможешь' \
                                  ' сообщить что-то новое :)'
                    Session_data[user_id] = {
                        'suggests': [
                            "Ну давай попробую.",
                            "Я не смогу что-то вспомнить.",
                        ],
                        'username': "Пользователь"

                    }

                    res['response']['buttons'] = get_suggests(user_id)
                    return
            if dialog_sport == 'football_neymar':
                if not flag_info_ney and req['request']['original_utterance'].lower() in ['ну давай попробую.',
                                                                                          'давай.',
                                                                                          'сейчас попробую']:
                    flag_info_ney = True
                    res['response'][
                        'text'] = 'Я тебя внимательно слушаю'
                    return
                if not flag_info_ney and req['request']['original_utterance'].lower() not in ['ну давай попробую.',
                                                                                              'давай.',
                                                                                              'сейчас попробую'] or \
                        req['request']['original_utterance'].lower() in ['я не смогу что-то вспомнить.', 'нет.',
                                                                         'не хочу']:
                    res['response'][
                        'text'] = 'Очень жаль, я надеялась на тебя. Тогда давай поговорим о чём-нибудь другом.'
                    current_status = "start_question"
                    Session_data[user_id] = {
                        'suggests': [
                            "Просто поболтать.",
                            "Вопросы по городам.",
                            "Покажи города.",
                            "Не знаю, выбери сама.",
                        ],
                        'username': "Пользователь"
                    }
                    Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                      'Чем занимаешься?']

                    res['response']['buttons'] = get_suggests(user_id)
                    return
                if any([i_know(alisa, req['request']['original_utterance'].lower()) for alisa in
                        knowledge_about_ney]) and flag_info_ney:
                    res['response'][
                        'text'] = 'Ну обо всем об этом я знала. Вот, что я узнала от тебя: "' + str(". ".join(
                        knowledge_about_ney)) + '" Спасибо, что рассказал мне о нем,' \
                                                ' было интересно тебя послушать. Давай ещё о' \
                                                ' чём-нибудь поговорим.'
                    current_status = "start_question"
                    Session_data[user_id] = {
                        'suggests': [
                            "Просто поболтать.",
                            "Вопросы по городам.",
                            "Покажи города.",
                            "Не знаю, выбери сама.",
                        ],
                        'username': "Пользователь"
                    }
                    Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                      'Чем занимаешься?']

                    res['response']['buttons'] = get_suggests(user_id)
                    return
                if not any([i_know(alisa, req['request']['original_utterance'].lower()) for alisa in
                            knowledge_about_ney]):
                    res['response'][
                        'text'] = 'Ого первый раз об этом услышала, продолжай, мне очень интересно.'
                    knowledge_about_ney.append(req['request']['original_utterance'].lower())
                    return
        if current_status == "talk_sport":
            if req['request']['original_utterance'].lower() in ['баскетбол', 'баскетболе.', 'баскетболом', 'баскетбол.',
                                                                'баскетболе.', 'баскетболом.']:
                res['response']['text'] = 'Я в нём очень мало разбираюсь.' \
                                          ' Все, что я пока могу, это вывести тебе турнирую таблицу на данный момент.'
                dialog_sport = 'basketball'
                Session_data[user_id] = {
                    'suggests': [
                        "Давай.",
                        "Спасибо, не надо.",
                    ],
                    'username': "Пользователь"

                }
                session = Session_data[user_id]
                suggests = [

                    {'title': suggest, 'hide': True}

                    for suggest in session['suggests']

                ]
                suggests.append({
                    "title": "Давай.",
                    "url": "https://yandex.ru/search/?text=баскетбольная лига",
                    "hide": True
                })

                res['response']['buttons'] = get_suggests(user_id)
                return
            if current_status == "talk_sport" and dialog_sport == 'basketball':
                if req['request']['original_utterance'].lower() in ['давай.', 'давай', 'да', 'да.',
                                                                    'покажи.', 'покажи']:
                    res['response']['text'] = 'Там вот такие результаты. Было интересно?'
                return
    if current_status == "start_question" and req['request']['original_utterance'].lower() in [
        'не знаю, выбери сама.', 'не знаю.', 'выбери сама',
        'а что сама предложишь.',
        'давай о спорте.', 'давай о спорте', 'спортом',
        'спортом.']:
        current_status_1 = "random_topic"
    if current_status_1 == "random_topic":
        current = random.choice(topic_alisa)
        if current == "translate":
            res['response'][
                'text'] = 'Давай я тогда тебе что-нибудь переведу, переводить буду с ' + lang
            current_dialog = current
            return
        if current == "gallery":
            res['response'][
                'text'] = 'Давай я покажу фотографии городов, о которых я слышала,' \
                          ' говори название, а я скажу знаю я его или нет.'
            current_dialog = current
            return
        if current == "city":
            res['response'][
                'text'] = 'Давай расскажу про города тебе.'
            current_status = current
            return
        if current == "talk_sport":
            res['response'][
                'text'] = 'Давай поговорим о спорте. Выбери о каком:"Футбол","Баскетбол","Хоккей"'
            current_status = current
            Session_data[user_id] = {
                'suggests': [
                    "Футбол",
                    "Баскетбол.",
                    "Хоккей.",
                ],
                'username': "Пользователь"
            }

            res['response']['buttons'] = get_suggests(user_id)
            return

    if req['request']['original_utterance'].lower() in ['вопросы по городам.']:
        current_dialog = "talk"
        # if "?" in req['request']['original_utterance'].lower():

    if req['request']['original_utterance'].lower() in ['вопросы по городам.']:
        current_dialog = "city"
        res['response'][
            'text'] = 'Отлично! Я могу сказать в какой стране город или сказать расстояние между городами!'

        return
    if current_dialog == "city":
        cities = get_cities(req)

        if len(cities) == 0:

            res['response']['text'] = 'Ты не написал название не одного города!'

        elif len(cities) == 1:

            res['response']['text'] = 'Этот город в стране - ' + get_geo_info(cities[0], 'country')

        elif len(cities) == 2:

            distance = get_distance(get_geo_info(cities[0], 'coordinates'), get_geo_info(cities[1], 'coordinates'))
            res['response']['text'] = 'Расстояние между этими городами: ' + str(round(distance)) + ' км.'

        else:

            res['response']['text'] = 'Слишком много городов!'
        return
    if req['request']['original_utterance'].lower() in ['переведи текст.', 'переведи', 'переводчик',
                                                        'нужно перевести']:
        current_dialog = "translate"
        res['response']['text'] = 'Отлично! Что нужно перевести?'
        Session_data[user_id]['suggests'] = [
            "Русский-английский",
            "Английский-русский"
        ]
        res['response']['text'] = Session_data[user_id]['username'] + '. Выбери язык'
        res['response']['buttons'] = get_suggests(user_id)
        current_status = 'start'
        current_dialog = 'translate'

        return

    if req['request']['original_utterance'].lower() in ['покажи города.']:
        current_dialog = "gallery"
        res['response']['text'] = 'Отлично!'
        Session_data[user_id]['suggests'] = [
            "Тамбов",
            "Москва",
            "Воронеж"
        ]
        res['response']['text'] = Session_data[user_id]['username'] + ', Какой город показать?'
        res['response']['buttons'] = get_suggests(user_id)
        current_status = 'start'
        current_dialog = 'gallery'

        return
    """if current_dialog == "talk":
        if current_status == 'talk_name':
            Session_data[user_id]['username'] = get_first_name(req).title()
            res['response']['text'] = 'Приятно познакомиться, ' + Session_data[user_id]['username']
            current_status = 'talk_alisa'
            return
        if '?' in req['request']['original_utterance'].lower():
            current_status = 'talk_user'
        else:
            current_status = 'talk_alisa'
        if current_status == 'talk_alisa':
            if len(Session_data[user_id]['quest']) < 1:
                res['response']['text'] = 'Не знаю, о чем еще спросить'
                Session_data[user_id]['quest'] = ['Как погода?', 'Как тебя зовут?', 'Тебе много лет?',
                                                  'Чем занимаешься?']
                current_dialog = "start"
                current_status = "start_question"
                Session_data[user_id]['suggests'] = [
                    "Переведи текст.",
                    "Найди в интернете",
                ]
                res['response']['buttons'] = get_suggests(user_id)
                return
            st_q = ['Интересно', 'Понятно', 'Ясно']
            c_q = random.choice(Session_data[user_id]['quest'])
            Session_data[user_id]['quest'].remove(c_q)
            if c_q == 'Как тебя зовут?':
                current_status = 'talk_name'
            res['response']['text'] = random.choice(st_q) + '. ' + c_q

            return

        elif current_status == 'talk_user':

            end_q = ['Что-нибудь еще спросишь?', 'Еще поговорим?', 'Мммм']
            if 'погода' in req['request']['original_utterance'].lower():
                res['response']['text'] = 'Нормальная' + '. ' + random.choice(end_q)
                return
            if 'имя' in req['request']['original_utterance'].lower():
                res['response']['text'] = 'Алиса' + '. ' + random.choice(end_q)
                return
            if 'лет' in req['request']['original_utterance'].lower():
                res['response']['text'] = 'Не знаю. Мало. ' + '. ' + random.choice(end_q)
                return
            res['response']['text'] = 'Не понятно о чем ты'
            return
        else:
            res['response']['text'] = 'Ты неразговорчивый. Что-нибудь хочешь?'
            current_dialog = "start"
            current_status = "start_question"
            Session_data[user_id] = [
                "Просто поболтать.",
                "Переведи текст.",
                "Найди в интернете",
            ]
            res['response']['buttons'] = get_suggests(user_id)
            return"""
    if current_dialog == "translate":
        translite_dialog(res, req)
        return
    # if current_status == 'city':
    #   city_dialog(res, req)
    #   return
    if current_dialog == 'gallery':
        gallery_dialog(res, req)
        return


def i_know(alisa, user):
    s = 0
    alisa = alisa.lower().split()
    user = user.lower().split()
    for a in alisa:
        for u in user:
            if a == u:
                s += 1
    if s > 2:
        return True
    return False


lang = "ru-en"


def translite_dialog(res, req):
    global current_status, current_dialog, Session_data, lang
    user_id = req['session']['user_id']
    if current_status == "start":
        if req['request']['original_utterance'] == "Русский-английский":

            lang = 'ru-en'

        else:
            lang = 'en-ru'
        res['response']['text'] = Session_data[user_id]['username'] + " скажи текст"
        current_status = 'start_translite'
        return

    if 'хватит' in req['request']['original_utterance'].lower():
        current_dialog = 'start'
        res['response']['text'] = "Была рада помочь"
        current_status = 'end_translite'
        return
    if current_status == 'start_translite':
        res['response']['text'] = "Перевод: " + translate.translate(req['request']['original_utterance'], lang)[0]
        current_status = 'start_translite'
        return


def gallery_dialog(res, req):
    global current_status, current_dialog, Session_data
    if current_dialog == "gallery":
        cities = {
            'тамбов':
                '1030494/15ee1b701a627af980e2'
            ,
            'леомесси':
                '1652229/5ba76fc57d55506fdb93'
            ,
            'москва':
                '1521359/53fc3bb34e2483f6794a'
            ,
            'воронеж':
                '1521359/0b2c34dc9f54dc235084'
            ,
            'нью-йорк':
                '1652229/728d5c86707054d4745f'
            ,
            'париж':
                '1652229/f77136c2364eb90a3ea8'

        }
        user_id = req['session']['user_id']

        city = req['request']['original_utterance'].lower()
        if city == "хватит":
            current_dialog = "start"
            current_status = "start"
            res['response']['text'] = 'Ок'
            return
        if city in cities:
            res['response']['card'] = {}
            res['response']['card']['type'] = 'BigImage'
            res['response']['card']['title'] = 'Этот город я знаю.'
            res['response']['card']['image_id'] = cities[city]
            res['response']['text'] = req['request']['original_utterance']
        else:
            res['response']['text'] = 'Первый раз слышу об этом городе.'
        return
    else:
        return


def city_dialog(res, req):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Отлично! Я могу сказать в какой стране город или сказать расстояние между городами!'

        return

    cities = get_cities(req)

    if len(cities) == 0:

        res['response']['text'] = 'Ты не написал название не одного города!'

    elif len(cities) == 1:

        res['response']['text'] = 'Этот город в стране - ' + get_geo_info(cities[0], 'country')

    elif len(cities) == 2:

        distance = get_distance(get_geo_info(cities[0], 'coordinates'), get_geo_info(cities[1], 'coordinates'))
        res['response']['text'] = 'Расстояние между этими городами: ' + str(round(distance)) + ' км.'

    else:

        res['response']['text'] = 'Слишком много городов!'
    return


def get_cities(req):
    cities = []

    for entity in req['request']['nlu']['entities']:

        if entity['type'] == 'YANDEX.GEO':

            if 'city' in entity['value'].keys():
                cities.append(entity['value']['city'])

    return cities


def get_first_name(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.FIO':
            return entity['value'].get('first_name', None)


def get_suggests(user_id):
    session = Session_data[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]
    Session_data[user_id] = session

    return suggests


if __name__ == '__main__':
    app.run()
