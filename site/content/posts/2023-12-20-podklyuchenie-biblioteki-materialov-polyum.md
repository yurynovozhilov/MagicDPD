---
layout: post
title: "Подключение библиотеки материалов PolyUMod к WB LS-DYNA"
date: 2023-12-20T15:01:27+00:00
author: "Yury Novozhilov"
source: vk
---

Все просто и сложно одновременно. Подключение библиотеки идет через *MAT_USER_DEFINED_MATERIAL_MODELS, а это значит, что вам нужно использовать кастомный решатель, собранный для PolyUMod. Правда заменять ничего в директории решателя не надо. Надо поправить просто отредактировать файл %APPDATA%\Ansys\v232\ACTLSDYNA\lsdyna_solvers.xml - возможность выбора кастомного решателя появиться в GUI.

https://youtu.be/D5stZQ6gjGo

[How to Use the PolyUMod Library with Ansys LS-DYNA in Workbench](https://youtu.be/D5stZQ6gjGo)
