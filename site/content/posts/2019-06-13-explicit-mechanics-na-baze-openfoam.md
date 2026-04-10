---
layout: post
title: "Explicit Mechanics на базе OpenFOAM"
date: 2019-06-13T17:00:26+00:00
author: "GlukRazor"
source: vk
images:
  - url: "/assets/images/1505.jpg"
---

Очень любопытная работа, о которой я уже несколько раз упоминал в рамках паблика. Но как оказалось, идея намного глубже: коллеги не учат OpenFOAM считать классическую Explcit схему — коллеги разрабатывают свой собственный подход, который должен быть лишен таких неприятных «фишек» традиционных explicit кодов, как паразитная жесткость при объемных и сдвиговых деформациях, а так же эффект песочных часов.























Проект сейчас поддерживает упругие, гиперупргие и упруго-пластические материалы. Расширение совместимо в OpenFOAM 4-6.















Репозиторий проекта: https://github.com/jibranhaider/explicitSolidDynamics



Некоторые ссылки на литературу: https://www.esi-group.com/sites/default/files/resource/other/7496/abstract_jibran_haider_explicit-solid-dynamics-in-openfoam.pdf



На мой взгляд, это очень крутой проект, так как открытых explicit кодов практически не существует. Но до коммерческого применения пилить и пилить. Например, если вы

https://github.com/jibranhaider/explicitSolidDynamics
https://www.esi-group.com/sites/default/files/resource/other/7496/abstract_jibran_haider_explicit-solid-dynamics-in-openfoam.pdf
