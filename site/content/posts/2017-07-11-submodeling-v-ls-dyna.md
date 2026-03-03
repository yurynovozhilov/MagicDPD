---
layout: post
title: "Submodeling в LS-DYNA"
date: 2017-07-11T17:00:59+00:00
author: "GlukRazor"
source: vk
tags:
  - Ozen
  - submodeling
  - Engineering
  - LSDYNA
---

Submodeling в LS-DYNA
https://support.ansys.com/staticassets/ANSYS/Conference/Santa Clara/downloads/Explicit Drop Test with ANSYS LS-DYNA - Chris Cowan.pdf

Есть такая замечательная техника уточнения модели, как подмоделирование или субмоделирование (#submodeling). Она заключается в создании глобальной модели с грубой сеткой, и последующем модеированием отдельных ее частей с большим уровнем точности. Эти подмодели просто вырезаются из геометрии большой модели. При этом, на границы среза подмодели передаются перемещения (жесткие граничные условия), полученные в глобальной модели.

Существует мнение, что техника submodeling применима только для квазистатической постановки. Как оказывается, это не совсем правда - статистику, как всегда, портит #LSDYNA. У нее есть замечательная методика Component Analysis, которая делает практически то же самое, что Submodeling, но для динамических задач.

Во вложении есть презентация Криса Соуэна (Chris Cowan) из #Ozen #Engineering об использовании данной техники на практике.

Всем заинтересованным надо почитать описание карт *INTERFACE_COMPONENT_SEGMENT и *INTERFACE_LINKING_SEGMENT

https://support.ansys.com/staticassets/ANSYS/Conference/Santa
