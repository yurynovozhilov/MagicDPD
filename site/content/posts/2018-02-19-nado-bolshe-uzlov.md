---
date: 2018-02-19 18:00:53+00:00
images:
- url: /assets/images/805.jpg
link_previews:
- description: ''
  image: ''
  title: three.js webgl - geometry - cube
  url: http://ftp.lstc.com/anonymous/outgoing/marleigh/hex64.html
original_url: https://t.me/MagicDPD/805
source: tg
title: Надо больше узлов!!!
---

Совсем недавно я писал про то, как LSTC реализовали новые чудесные 27-узловые solid элементы в LS-DYNA. Оказалось, что данный рекорд по количеству узлов продержался недолго.
Копаясь в черновиках документации к еще невышедшим версиям LS-DYNA (например, вот тут http://ftp.lstc.com/user/manuals/DRAFT/DRAFT_Vol_I_13Feb2018.pdf), я нашел упоминание 64-узлового (!!!) hex элемента. Судя по описанию, данный элемент будет работать не с привычными для explicit кодов линейными функциями формы, а с кубическими! Для пользователей обычных сеточных генераторов создана особая карта *ELEMENT_SOLID_H8TOH64, которая дает решателю директиву автоматически добавить недостающие 56 узлов к классическим линейным hex елементам.
Визуализация узлов и порядка их нумерации: http://ftp.lstc.com/anonymous/outgoing/marleigh/hex64.html
 
#H8TOH27 #H8TOH64 #LSDYNA #LSTC
