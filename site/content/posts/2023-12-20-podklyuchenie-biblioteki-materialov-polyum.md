---
author: Yury Novozhilov
date: 2023-12-20 15:01:27+00:00
layout: post
link_previews:
- description: This tutorial shows how you can use the PolyUMod library with Ansys
    LS-DYNA in Workbench. The key step is to copy the PolyUMod enhanced version of
    the LS-DYN...
  image: https://i.ytimg.com/vi/D5stZQ6gjGo/maxresdefault.jpg
  title: How to Use the PolyUMod Library with Ansys LS-DYNA in Workbench
  url: https://www.youtube.com/watch?v=D5stZQ6gjGo
source: vk
title: Подключение библиотеки материалов PolyUMod к WB LS-DYNA
---

Все просто и сложно одновременно. Подключение библиотеки идет через *MAT_USER_DEFINED_MATERIAL_MODELS, а это значит, что вам нужно использовать кастомный решатель, собранный для PolyUMod. Правда заменять ничего в директории решателя не надо. Надо поправить просто отредактировать файл %APPDATA%\Ansys\v232\ACTLSDYNA\lsdyna_solvers.xml - возможность выбора кастомного решателя появиться в GUI.

https://youtu.be/D5stZQ6gjGo

[How to Use the PolyUMod Library with Ansys LS-DYNA in Workbench](https://youtu.be/D5stZQ6gjGo)
