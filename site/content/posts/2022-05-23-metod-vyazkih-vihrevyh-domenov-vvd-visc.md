---
layout: post
title: "Метод вязких вихревых доменов (ВВД, viscous vortex domains, "
date: 2022-05-23T17:00:20+00:00
author: "MagicDPD"
source: vk
original_url: https://vk.com/wall-97265142_2275
tags:
  - meshless
  - opensource
  - CFD
  - VVD
  - Vvflow
  - GitHub
images:
  - url: "/assets/images/2276.jpg"
  - url: "/assets/images/2277.jpg"
---

Метод вязких вихревых доменов (ВВД, viscous vortex domains, #VVD) - это #meshless метод вычислительной гидродинамики для прямого численного решения двумерных уравнений Навье-Стокса в координатах Лагранжа. Он не реализует никакой модели турбулентности и свободен от произвольных параметров. Основная идея этого метода состоит в том, чтобы представить поле вихря дискретными областями (доменами), которые перемещаются с диффузионной скоростью относительно жидкости и сохраняют свою циркуляцию.

Данный метод, например, реализован в #opensource коде #Vvflow #CFD suite, код которого доступен на #GitHub, а примеры его использования - на YouTube
https://youtu.be/H-snLmMQK0Y
https://youtu.be/3mULL6O6f38
https://youtu.be/kHJ4occRZ4M
https://youtu.be/9fr2C5RC-6Y
https://youtu.be/7xr_giqSfRc https://github.com/vvflow/vvflow
