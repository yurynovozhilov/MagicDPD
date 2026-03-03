---
layout: post
title: "Моделирование железобетона в оболочечной постановке"
date: 2018-07-16T18:00:22+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_1017
tags:
  - MATCONCRETEEC2
  - ARUP
  - Concrete
  - LSDYNA
  - LSTC
---

Моделирование железобетона в оболочечной постановке
В сеть попала презентация от LSTC и ARUP по использованию такой замечательной модели железобетона, как *MAT_CONCRETE_EC2, где EC2 - это от Eurocode. Чувствуете чем пахнет?

Модель *MAT_CONCRETE_EC2 позволяет такое, что любая модель бетона для твердотельной постановки позавидует:

Работа в оболочечной и балочной (армированные колонны) постановке
Автоматическая генерация входных параметров согласно классу прочности бетона по Eurocode2
Учет нескольких слоев армирования
Термическое разупрочнение для моделирования пожаров
Поддержка циклического нагружения

А еще, поддержка данной модели реализована в Beta ражиме внутри ANSYS Workbench LS-DYNA - данная модель материала доступна в Engineering Data!

У меня даже есть примеры диссертаций, где она использовалась:

http://www.byggmek.lth.se/fileadmin/byggnadsmekanik/publications/tvsm5000/web5193.pdf
https://paginas.fe.up.pt/~eurodyn2014/CD/papers/492_MS24_ABS_1957.pdf
https://hal.archives-ouvertes.fr/hal-01183176/document
https://www.dynalook.com/13th-international-ls-dyna-conference/blast/response-of-a-large-span-stay-cable-bridge-to-blast-loading

Ну и собственно материал, который стал инфоповодом для данного поста:
http://ftp.lstc.com/anonymous/outgoing/support/FAQ_kw/concrete/MAT_172_notes_03apr2018.pdf

#ARUP #Concrete #LSDYNA #LSTC #MATCONCRETEEC2
http://bit.ly/2uEXrIV
