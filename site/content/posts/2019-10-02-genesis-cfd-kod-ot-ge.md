---
author: GlukRazor
date: 2019-10-02 13:00:16+00:00
images:
- url: /assets/images/1602.jpg
layout: post
link_previews:
- description: The ability to simulate turbulent phenomena using high-performance
    computing (HPC) can provide industry with important insights for efficient engine
    design. Second only to the ability to perform these critical simulations is the
    speed at which they run. If a company can run a model more quickly, the number
    of possible...
  image: ''
  title: GPUs Power GE Code at OLCF Hackathons
  url: https://www.olcf.ornl.gov/2019/09/12/gpus-power-ge-code-at-olcf-hackathons/
source: vk
tags:
- CFD
- HpMusic
- GPU
- GE
- HPC
- NVIDIA
- GENESIS
title: GENESIS - CFD код от GE
---

Вычислительный код GENESIS разрабатывается GE на базе существующей научной разработки hp-adaptive Multi-physics Simulation Code (hpMusic), так что правильнее его называть hpMusic/GENESIS.







Код, по заявлениям разработчиков, очень интересный.Это не традиционный метод конечных объемов, а некий собственный «flux reconstruction method», который представляет собой некую смесь лагранжева и эйлерова подхода к описанию среды. Если я правильно понял его суть, то каждый вихрь в этом методе считается в эйлеровой постановке, а вот перемещение эйлерова домена с вихрем по пространству — уже в лагранжевой. Говорят, что такая схема позволяет очень хорошо разложить задачу на большой массив GPU и минимизировать затраты на связь между доменами. Больше информации тут: https://www.olcf.ornl.gov/2019/09/12/gpus-power-ge-code-at-olcf-hackathons/





#CFD #GE #GENESIS #GPU #HPC #HpMusic #NVIDIA
https://bit.ly/2mYKCcQ

[GPUs Power GE Code at OLCF Hackathons](https://www.olcf.ornl.gov/2019/09/12/gpus-power-ge-code-at-olcf-hackathons/)
https://bit.ly/2mYKCcQ
