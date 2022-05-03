import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import bot, dp
from pyowm import OWM
from pyowm.utils import config

config_dict = config.get_default_config_for_subscription_type('professional')
config_dict['language'] = 'ru' 

owm = OWM('127934e41dc5667bf248c54d9435ea1a', config_dict)
mgr = owm.weather_manager()

class FSMWeather(StatesGroup):
    city = State()


# @dp.message_handler(commands=['Погода'], state=None)
async def weather(message: types.Message, state:FSMContext):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    try:
        await FSMWeather.city.set()
        await message.answer('Напиши мне название города, в котором ты хочешь узнать погоду.')
    except Exception as exc:
        print(now, exc)
        await state.finish()


# @dp.message_handler(content_types=['text'], state=FSMWeather.city)
async def city(message: types.Message, state:FSMContext):
    nowdatetime = datetime.datetime.now()
    now = nowdatetime.strftime('[%d/%m/%Y %H:%M:%S]')
    async with state.proxy() as data:
        data['city'] = message.text
    try:
        observation = mgr.weather_at_place(str(message.text))
        w = observation.weather
        a = w.detailed_status
        # b = w.wind() 
        c = ("Температура на градуснике: " 
             + "\n"  + str(w.temperature('celsius')['temp'])  + "°С" 
             + "\n\nПо ощущению: " 
             + '\n' + str(w.temperature('celsius')['feels_like']) + "°С")
        d = (w.temperature('celsius')['feels_like'])
        # e = w.rain
        # f = w.clouds

        # current_temp = w.temperature ('celsius')["temp"]

        # await message.answer (w.detailed_status, w.wind, w.humidity, parse_mode=True) 
        # await bot.send_message(message_filter, message.text)
        # await message.answer (w.detailed_status)         # 'clouds'
        # w.detailed_status
        # w.wind()                  # {'speed': 4.6, 'deg': 330}

        # await message.answer (w.humidity)                # 87
        # w.humidity
        # await message.answer ("Температура на градуснике: " + str(w.temperature('celsius')['temp']) + "°С" + "\nПо ощущению: " + str(w.temperature('celsius')['feels_like']) + "°С")  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0, 'feels_like': 1.43}
        # await message.answer("<u>egbegb</u> " + str(w.temperature('celsius')['temp']))

        if d < 20 and \
            d >= 15:
            d = ("""
При такой температуре вполне комфортно можно ездить и в летней форме, \
добавив сначала рукава (около +17-18 градусов), а затем и «чулки», если столбик термометра приближается к +15°С.

В таком случае, как только температура поднимается до 20 градусов и выше, \
вы легким движением снимаете рукава, чулки и чувствуете себя сухо и комфортно.

Еще одно полезное приобретение в прохладную ветреную погоду, \
особенно при высокой влажности, когда ветер промораживает насквозь даже \
при относительно высокой температуре – жилетка, которая защитит ваше тело от лишнего переохлаждения.
""")
        elif d < 15 and \
            d >= 10:
            d = ("""
Приведем несколько рабочих вариантов, из которых вы всегда сможете выбрать наиболее вам подходящий.

Верх:

1. Джерси с коротким рукавом на термомайку с длинным рукавом. Жилетка в кармане джерси — на случай холодного ветра.
2. Джерси с длинным рукавом, термомайка под нее с длинным или коротким рукавом по вкусу. Жилетка в кармане.
3. Джерси с коротким рукавом, термомайка под нее с коротким рукавом и флисовые рукава отдельно. Жилетка в кармане.

Низ:

1. Теплые наколенники + летние трусы с памперсом.
2. Велотрусы в 3/4 (чуть ниже колена).
3. «Чулки» + летние трусы с памперсом.
4. Ближе к 10 градусам – длинные велоштаны без виндстоппера.

Перчатки:

1. На такую погоду стоит иметь легкие перчатки с длинными пальцами
2. Ближе к 10 градусам – перчатки с длинным пальцем и виндстоппером, но без утепления.

Туфли:

Ближе к 10 градусам стоит утеплить туфли легкими бахилами

Защита головы:

Ближе к 10 градусам стоит надевать под шлем легкую шапочку с виндстоппером на лбу под шлем.
""")
        elif d < 10 and \
            d >= 5:
            d = ("""
Верх:

Идеальная одежда для такой погоды – куртка с непродуваемой грудью, \
рукавами и плечами, но без утеплителя. Желательно при этом, особенно при езде на МТБ в лесу, чтобы «дышала» спина.

Низ:

Длинные велоштаны с легким утеплением, наличие защищающего от холодного ветра \
слоя в районе коленей приветствуется. Можно купить отдельно теплые наколенники с виндстоппером.

Перчатки:

В зависимости от терморегуляции вашего организма, вам оптимально подойдут \
либо перчатки с виндстоппером, но без дополнительного утепления, либо с легким утеплением. Но не совсем «зимние».

Туфли:

1. Самый простой вариант – бахилы с защитой от ветра и дождя. Однако он имеет как плюсы, \
так и минусы и многие в таком температурном режиме склоняются к следующему варианту, особенно, если запланированы выезды длиннее 2-х часов.
2. Легкие демисезонные туфли с защитой от ветра и влаги с легким утеплением.

Утепление головы:

Шапочка будет очень кстати, если вы не хотите отморозить уши уже через 15 минут езды.
""")
        elif d < 5 and \
            d >= 0:
            d = ("""
Если невнимательно подойти к выбору одежды в такую погоду, \
удовольствия может хватить буквально на пару минут, а после этого неминуемо захочется домой к маме.

Верх:

Ближе к нулю по Цельсию вам всё сильнее захочется более теплую куртку, чем вы надевали при +5-10. \
Эта куртка должна быть с виндстоппером и иметь легкий «начес» чтобы лучше удерживать комфортную температуру тела.
При этом ни в коем случае не вздумайте надевать пуховик или что-то в этом роде. \
Куртка должна «дышать», но не промокать. Возможно, ближе к 0°С, вы захотите надеть легкую флиску под куртку.
Ну и, конечно, не забываем о термофутболке с длинным рукавом. Без нее на велосипеде в прохладную погоду вообще делать нечего!

Низ:

Оптимальный выбор на такую погоду – зимние штаны с виндстоппером и тонким слоем флисового утеплителя.
Кстати, никогда не надевайте термобелье под велоодежду с памперсом. \
Просто не делайте этого, если не хотите возвращаться домой стоя 😉

Перчатки:

Теплые зимние перчатки с виндстоппером. В более легких вы имеете все шансы \
отморозить себе пальцы и плюнуть на все эту зимнюю езду на велосипеде.

Защита головы:

Очень важно в такую погоду защищать уши. Они не только очень сильно мерзнут на холодном ветру. \
Кроме этого, вы имеете отличные шансы подхватить воспаление внутренних частей уха, \
покатавшись в холодную ветренную погоду без защиты.
Один поход к ЛОР-у, а потом в аптеку за лекарствами обходится дороже отличной шапочки, \
которая защитит вашу голову и уши зимой! Не экономьте на здоровье!

Кстати, где-то в такую погоду уже можно задуматься о легкой «балаклаве», \
которая кроме ушей и верхней части головы, подставленной под ветер, защищает шею.

Ноги:

Если вы не купили утепленную обувь, самое время задуматься о ней! \
Или купить теплые неопреновые бахилы. Если в +5°С и более многие еще ездят в летней обуви без защиты, \
то около нуля сдаются почти все.
При езде в летней обуви под неопреновыми бахилами часто мерзнет стопа через \
дырки для крепления шипа подошве. Частично ситуацию исправляет несколько слоев фольги под стельку.
""")
        elif d < 0:
            d = ("""
Верх:

Зимняя куртка с виндстоппером и утеплением – обязательный аттрибут в такую погоду. \
Под ней – флиска по погоде и обязательно термобелье с длинным рукавом.

Низ:

Зимние велоштаны. Также, возможно, вам понравится идея дополнительно утеплить колени (они-то уж точно будут не против!).

Перчатки:

Теплые перчатки с виндстоппером. Хорошо работают перчатки для беговых лыж. \
В такую погоду пальцы рук – одна из самых нежных частей тела. Промерзают они очень быстро и, \
если нет нормальных перчаток, практически ничего не помогает.

На ноги:

Зимние ботинки. Точка. Игры с летней обувью и бахилами можно оставить для \
коротких шоссейных тренировок. Здесь бахилы могут сыграть с вами злую шутку, \
особенно, если вы умудритесь вступить в лужу или мокрый снег.

В рюкзаке:

Термос с горячим чаем, дополнительная куртка на случай аварийной остановки, запасные теплые перчатки.

Дополнительно:

Термофляга и гидратор под одеждой. При отрицательных температурах вода во \
фляге может замерзнуть неожиданно быстро. Не говоря уже о том, что через 15-20 минут \
езды она станет слишком холодной, чтобы её можно было комфортно пить. Задумайтесь об этом до выезда!
""")
        else:
            d = ("""
В такую погоду нужно надевать на себя летние велотрусы с памперсом, \
джерси с коротким рукавом, легкие перчатки, легкие носки и, конечно, шлем.
""")
        # await message.answer (w.rain)                    # {}
        # await message.answer (w.heat_index)              # None
        # await message.answer (w.clouds)                  # 75
        await message.answer(str(a.upper()) + "\n\n" + c + "\n" + str(d))
        print(now, message.from_user.first_name + ' запросил погоду в ' + data['city'])
    except:
        await message.reply(
            "Ты что мне тут вводишь?\nЧтобы узнать погоду нажми кнопку погоды и введи название города."
            )
        print(now, message.from_user.first_name + ' попробовал запросить погоду в ' + data['city'] + ', но не смог')
        await state.finish()
        # answer = forecast.will_be_clear_at(timestamps.tomorrow())
    # await message.reply(data['city'])
    await state.finish()


def register_handlers_weather(dp:Dispatcher):
    dp.register_message_handler(weather, commands=['Погода'])
    dp.register_message_handler(city, content_types=['text'], state=FSMWeather.city)