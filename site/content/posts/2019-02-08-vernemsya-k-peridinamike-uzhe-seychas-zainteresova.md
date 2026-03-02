---
date: 2019-02-08 04:35:29+00:00
images:
- url: /assets/images/1337.jpg
- url: /assets/images/1338.jpg
- url: /assets/images/1339.jpg
- url: /assets/images/1340.jpg
link_previews:
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/s9vWYY-5356
- description: ''
  image: http://yourmine.ru/i/parking/glob_parking.png
  title: "Ð¡Ñ\x80Ð¾Ðº Ñ\x80ÐµÐ³Ð¸Ñ\x81Ñ\x82Ñ\x80Ð°Ñ\x86Ð¸Ð¸ Ð´Ð¾Ð¼ÐµÐ½Ð° magicdpd.ru
    Ð¸Ñ\x81Ñ\x82Ñ\x91Ðº"
  url: https://wp.me/s9vWYY-4867
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/6/6f/Al_tensile_test.jpg
  title: Перидинамика — Википедия
  url: https://ru.wikipedia.org/wiki/Перидинамика
- description: ''
  image: ''
  title: Index
  url: http://ftp.lstc.com/anonymous/outgoing/whu/Class/
original_url: https://t.me/MagicDPD/1337
source: tg
title: Вернемся к перидинамике. Уже сейчас заинтересованные пользователи могут запросит
---

А еще там будет много вкусностей про Smoothed Particle Galerkin (#SPG) для пластического разрушения.
#peridynamics #lsdyna




 Файл Recent Development of Advanced FEM and Meshfree Methods in LS-DYNA for Solid and Structural Analyses.pdf
 Файл Implementation of Peridynamic Theory to LS-DYNA for Prediction of Crack Propagation in a Composite Lamina.pdf

#LS_DYNA #LSTC #peridynamics #SPG

https://wp.me/s9vWYY-5356

by GlukRazor

Работают ли бессрочные методы?


Работают ли бессрочные методы?
Небольшая статья с очередной конференции по #LSDYNA. В статье рассказывается о сравнении расчета с применением сеточных и бессрочных методов с экспериментом — разрывом металлического образца.
Постановки:
— #FEM #Lagrangian
— #FEM #ALE
— #SPH
— #EFG
— #SPG
Точную кривую не описал не один из методов. Точная форма получилась только у ALE. Хуже всех, естественно выступил SPH, с его численной нестабильностью при работе на растяжение. На мой вкус EFG дал самую хорошую кривую, но с формой беда.
Прям захотелось повторить численный эксперимент.


http://www.dynalook.com/14th-international-ls-dyna-conference/constitutivemodeling/necking-and-failure-simulation-of-lead-material-using-ale-and-mesh-free-methods-in-ls-dyna-r

#ALE #EFG #FEM #Lagrangian #LS_DYNA #SPG #SPH

https://wp.me/s9vWYY-4867

by GlukRazor

Хрупкое разрушение


Тут у меня коллеги интересовались моделированием хрупкого разрушения материалов в #LSDYNA. Самым передовым и многообещающим методом расчета такого разрушения и трещенообразования является перидинамика (https://ru.wikipedia.org/wiki/Перидинамика)
Так вот, я поскреб по сусекам, посмотрел, что у меня есть в волшебном хранилище знаний, и нашел отличную ссылку на репозиторий господина Cheng-Tang Wu (одного из главных разработчиков #LSTC в этом направлении), где он выкладываем свой учебный курс по бессрочным методам (корме перидинамики есть еще #EFG и #SPG).
Внимание, в составе данного учебного курса есть работающие примеры со всем перечисленными бессрочными методами расчета разрушения!
#meshless #peridynamics #AdaptiveEFG
P.S. Насколько я понял, ключевые карты SECTION_SOLID_PERI и MAT_ELASTIC_PERI пока реализованы только в beta версиях решателя поколения R10.
http://ftp.lstc.com/anonymous/outgoing/whu/Class/


Index of /anonymous/outgoing/whu/Class

Материалы 15-ой конференции LS-DYNA


Стали доступны материалы конференции, проведенной две недели назад  в Детройте, США. Это значит, что в свободный доступ попал большой массив (182 штуки) свежайших статей от ведущих разработчиков и пользователей LS-DYNA. Спасибо LSTC за такую щедрую политику распространения информации. Если надо объяснять, то не надо объяснять.
Что я уже успел отметить для себя при беглом просмотре части материалов (все будет позднее подробно рассказано в паблике):

S-ALE домен научился двигаться за центром тяжести себя самого
Подробное описание MLS-SPH формулировки, стабильной на растяжение и кручение
Вычислительно эффективные IGA-элементы
Обзор работы основных моделей бетонов для SPH
Аналог *CONSTRAINED_LAGRANGE_IN_SOLID для SPG
Расчеты динамики парашютов с использованием как ALE-FSI, так и ICFD-FSI

Программа конференции: https://www.dynamore.de/en/downloads/flyer/2018/int.-ls-dyna-conference-2018-agenda
Материалы для изучения:
