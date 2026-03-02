---
date: 2018-02-09 18:01:27+00:00
images:
- url: /assets/images/775.jpg
link_previews:
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Skin_depth.svg/1280px-Skin_depth.svg.png
  title: Скин-эффект — Википедия
  url: https://ru.wikipedia.org/wiki/Скин-эффект
- description: This is the second part of a series of videos regarding the EM solver
    which explains the physics, keywords and main concepts for Electromagnetic forming/weld...
  image: https://i.ytimg.com/vi/LYhXfSLwz0c/maxresdefault.jpg
  title: 'LS-DYNA EM: Tutorial for Metal forming application (Part II)'
  url: https://www.youtube.com/watch?v=LYhXfSLwz0c
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/p9vWYY-1BP
original_url: https://t.me/MagicDPD/775
source: tg
title: 'Электромагнитный решатель LS-DYNA: добавим больше физики'
---

Продолжаем знакомиться с  возможностями решателя от LSTC в области электромагнитных расчетов. Второй видеоурок посвящен особенностям выбора шага по времени и настройке сетки модели.

<!--more-->

Собственно, сетка строится так, чтобы на поверхности проводника было хотя бы 3 элемента на толщину скин-слоя (https://ru.wikipedia.org/wiki/Скин-эффект). И опять нам рекомендуют использовать hex сетку.

Несмотря на то, что решатель в данном классе задач используется неявный (должен сходиться с любым шагом по времени), разработчики рекомендуют соблюдать критерий Куранта-Фридрихса-Леви в его электромагнитной формулировке. Так мы сможем повысить не только точность, но и стабильность расчета.

Кроме того, в видео показывают ряд интересных возможностей по постпроцессингу результатов - например, построение эпюр и линий поля.

Интересный факт: оказывается EM решатель LS-DYNA основан на библиотеках FEMSTER

https://www.youtube.com/watch?v=LYhXfSLwz0c
 #EM #FEMSTER #LS-DYNA #LSTC
https://wp.me/p9vWYY-1BP
