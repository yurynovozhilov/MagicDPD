---
layout: post
title: "Как делать HPC для ANSYS 18"
date: 2017-02-09T17:02:27+00:00
author: "GlukRazor"
source: vk
tags:
  - CFD
  - ANSYS
  - HPC
  - Maxwell
  - CentOS
  - RSM
  - ARC
  - NVIDIA
  - GPGPU
  - Explicit
---

Как делать HPC для ANSYS 18
https://www.cadfem-cis.ru/products/ansys/ansys-update/

Коллеги, рад поделиться ссылкой на опубликованный недавно материал, по тематике #HPC для #ANSYS и построения правильно IT инфраструктуры для расчетов.

Вот в этом документе вы найдете очень много интересного и нового, чего иногда даже нет и в официальной документации - https://www.cadfem-cis.ru/fileadmin/data/file/content_prod/ansys/18/ANSYS18_tech.pdf

Главные фишки релиза 18.0 с точки зрения HPC:
- поддержка #CentOS 7
- cобственный встроенный бесплатный кластерный планировщик (aka workload manager, aka scheduler) для Windows и Linux - ANSYS #RSM Cluster (aka #ARC)
- ANSYS #CFD теперь считает на 4-х ядрах из коробки
- ANSYS #Explicit STR теперь считает на 2-х ядрах из коробки
- ANSYS #Maxwell теперь умеет использовать #GPGPU #NVIDIA
- Первый ANSYS HPC Pack это 10, а не 8 ядре

[Обновления ANSYS 19 – CADFEM](https://www.cadfem-cis.ru/products/ansys/ansys-update/)
https://www.cadfem-cis.ru/fileadmin/data/file/content_prod/ansys/18/ANSYS18_tech.pdf
