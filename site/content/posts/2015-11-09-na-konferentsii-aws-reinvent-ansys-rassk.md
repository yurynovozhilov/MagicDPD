---
author: GlukRazor
date: 2015-11-09 06:30:19+00:00
layout: post
link_previews:
- description: 'Learn more about AWS: http://amzn.to/1OqIvCBBuilding great products,
    ones that are aesthetically appealing as well as functionally sound, requires
    cutting-ed...'
  image: https://i.ytimg.com/vi/0EPnnKqs5TM/hqdefault.jpg
  title: AWS re:Invent 2015 | (CMP202) Engineering Simulation and Analysis in the
    Cloud
  url: https://www.youtube.com/watch?v=0EPnnKqs5TM
source: vk
tags:
- Amazon
- DCV
- ANSYS
- HPC
- NICE
- CycleComputing
- Cloud
- Chef
- AWS
title: На конференции AWS re:Invent ANSYS расскзал об архитектуре своего облачного
  решения ANSYS Enterprise Cloud в AWS.
---

Всю магию по созданию виртуального кластера для них делает Cycle Computing. Графикой естественно завидует NICE Software. Управление конфигурациями через Chef. Метаданные пишутся в базу Amazon RDS (наверно они приделали к ней аналог ANSYS EKM).

Однако проблемы, на которые я всегда обращаю внимание, остались открытыми:
- нет RDMA - большой кластер тормозит даже для CFD
- очень кривая организация виртуальных рабочих станций для постпроцессинга из-за ограничений на объем оперативной памяти.

Есть и замечательные, доселе невиданные возможности: вы получаете готовый к расчетами HPC кластер менее чем за 3 (три!!!) часа, и вы можете изменять его размер по запросу. Обычно проектирование и пуск кластера занимает месяцы :)

[AWS re:Invent 2015 | (CMP202) Engineering Simulation and Analysis in the Cloud](https://www.youtube.com/watch?v=0EPnnKqs5TM)
