---
layout: post
title: "PrePoMax + OpenRadioss"
date: 2024-12-12T13:46:05+00:00
author: "Yury Novozhilov"
source: vk
original_url: https://vk.com/wall-97265142_2855
---

PrePoMax + OpenRadioss

Еще одна ступенька на пути человеческой опенсорсной FEM среды. Появился ковертор, переводящий .inp файлы из PrePoMax (читай формата Abaqus/Calculix) в .rad формат, понятный Radioss и OpenRadioss. Стоит наверно отметить, что я бы советовал проверять всякие специфичные для решателя фишки на корректность конвертации. Но в целом - я теперь ну вот прям совсем не вижу смысла в разработке своих кодов для прочности.

https://github.com/OpenRadioss/Tools/tree/main/input_converters/inp2rad
