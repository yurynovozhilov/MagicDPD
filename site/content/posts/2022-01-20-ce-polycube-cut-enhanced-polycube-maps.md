---
layout: post
title: "CE-PolyCube: Cut-enhanced PolyCube-Maps for Feature-aware All-Hex Meshing"
date: 2022-01-20T17:00:12+00:00
author: "MagicDPD"
source: vk
tags:
  - opensource
  - mesh
  - PolyCube
  - ALLHEX
images:
  - url: "/assets/images/2092.jpg"
  - url: "/assets/images/2093.jpg"
---

Методы генерации сетки, основанные на объемных картах PolyCube-Map, предлагают автоматическую генерацию #ALLHEX сеток для замкнутых трехмерных многогранных объёмов, однако качество получаемой сетки ограничено особенностями геометрии. В представленной работе предлагается ряд улучшений к PolyCube-Maps. Основная идея проста и интуитивно понятна: исходный объем периодически декомпозируют на подобаемы (или добавляют линии раздела на слишком протяженных поверхностях), что приводит к улучшению получаемой сетки и лучшему описанию геометрии.

Что мне больше всего нравится в данном проекте, так это опубликованные исходники кода, рассчитанные на работу в 64-х битных версиях Windows

#PolyCube #mesh #opensource https://github.com/msraig/CE-PolyCube

[GitHub - msraig/CE-PolyCube: Source code of SIGGRAPH 2020 paper: Cut-enhanced PolyCube-Maps for Feature-aware All-Hex Meshing](https://github.com/msraig/CE-PolyCube)
