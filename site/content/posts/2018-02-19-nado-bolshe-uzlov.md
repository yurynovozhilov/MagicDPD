---
layout: post
title: "Надо больше узлов!"
date: 2018-02-19T18:00:53+00:00
author: "GlukRazor"
source: vk
tags:
  - LSTC
  - H8TOH27
  - H8TOH64
  - LSDYNA
images:
  - url: "/assets/images/807.jpg"
---

!!
Совсем недавно я писал про то, как LSTC реализовали новые чудесные 27-узловые solid элементы в LS-DYNA. Оказалось, что данный рекорд по количеству узлов продержался недолго.
Копаясь в черновиках документации к еще невышедшим версиям LS-DYNA (например, вот тут http://ftp.lstc.com/user/manuals/DRAFT/DRAFT_Vol_I_13Feb2018.pdf), я нашел упоминание 64-узлового (!!!) hex элемента. Судя по описанию, данный элемент будет работать не с привычными для explicit кодов линейными функциями формы, а с кубическими! Для пользователей обычных сеточных генераторов создана особая карта *ELEMENT_SOLID_H8TOH64, которая дает решателю директиву автоматически добавить недостающие 56 узлов к классическим линейным hex елементам.
Визуализация узлов и порядка их нумерации: http://ftp.lstc.com/anonymous/outgoing/marleigh/hex64.html

http://ftp.lstc.com/user/manuals/DRAFT/DRAFT_Vol_I_13Feb2018.pdf
http://ftp.lstc.com/anonymous/outgoing/marleigh/hex64.html
