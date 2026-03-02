---
date: 2019-06-25 16:08:28+00:00
images:
- url: /assets/images/1514.jpg
- url: /assets/images/1515.jpg
link_previews:
- description: Главная
  image: http://ansysconference.ru/static/templates/cascon2019/dist/images/OG-image.png
  title: Главная — Конференция CADFEM\ANSYS
  url: https://ansysconference.ru/
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/p9vWYY-2A9
original_url: https://t.me/MagicDPD/1514
source: tg
title: Открыта регистрация на ACUM (CASCON) XVI
---

Стали известны даты главного CAE события года — ежегодной большой конференции пользователей CADFEM/ANSYS. 16-ая конференция пройдет с 22 по 24 октября в Москве на базе отеля «Москва Марриотт Новый Арбат». Регистрация уже открыта на сайте конференции https://ansysconference.ru/ Участие платное, но для тех, кто с докладом, оно в 2 раза дешевле.

#ACUM #ANSYS #CADFEM

https://wp.me/p9vWYY-2A9

by Юрий Новожилов

MAT_GENERALIZED_PHASE_CHANGE


Эта модель материала появилась в 11-ой версии LS-DYNA, и как-то долго оставалась незамеченной мной, а зря. Прежде всего модель позволяет отслеживать до 24-х фаз в металле, подвергающемуся тепловому воздействию (сварка, прокатка, штамповка, 3D печать и т.д.). 







 JMAK = Johnson-Mehl-Avrami-Kolmogorov







Но просто фазами тут все не ограничивается: надо смотреть на результаты, предоставляемые моделью. Немного поколдовав с картой DATABASE_EXTENT_BINARY, можно заказать для shell/solid вывод следующих дополнительных результатов.







Нет, вы это видите: распределение размера зерна, предела текучести, модуля упругости по объему тела!!!



Дополнительные статьи по теме:



https://www.dynalook.com/conferences/12th-european-ls-dyna-conference-2019/ls-dyna-on-demand/merten_dynamore.pdf/view



https://www.dynalook.com/conferences/12th-european-ls-dyna-conference-2019/ls-dyna-on-demand/merten_dynamore.pdf/view
