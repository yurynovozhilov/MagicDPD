---
author: Yury Novozhilov
date: 2025-12-04 09:03:46+00:00
layout: post
link_previews:
- description: Researchers used Lawrence Livermore National Laboratory's (LLNL) exascale
    supercomputer El Capitan to perform the largest fluid dynamics simulation ever
    — surpassing one quadrillion degrees of freedom in a single computational fluid
    dynamics (CFD) problem. The team focused the effort on rocket–rocket plume interactions.
    El Capitan is funded by the National Nuclear Security Administration's (NNSA)
    Advanced Simulation and Computing (ASC) program. The work — in part performed
    prior to the
  image: https://contenthub.llnl.gov/sites/contenthub/files/styles/scaled_425h/public/2025-11/External_Rocket_1280x720.jpg?itok=PzQNBERf
  title: Gordon Bell finalist team pushes scale of rocket simulation on El Capitan
  url: https://www.llnl.gov/article/53626/gordon-bell-finalist-team-pushes-scale-rocket-simulation-el-capitan
- description: We present an optimized implementation of the recently proposed information
    geometric regularization (IGR) for unprecedented scale simulation of compressible
    fluid flows applied to multi-engine spacecraft boosters. We improve upon state-of-the-art
    computational fluid dynamics (CFD) techniques along computational cost, memory
    footprint, and energy-to-solution metrics. Unified memory on coupled CPU--GPU
    or APU platforms increases problem size with negligible overhead. Mixed half/single-precision
    s
  image: /static/browse/0.3.4/images/arxiv-logo-fb.png
  title: 'Simulating many-engine spacecraft: Exceeding 1 quadrillion degrees of freedom
    via information geometric regularization'
  url: https://arxiv.org/abs/2505.07392
- description: Exascale multiphase flow solver — 2025 Gordon Bell Prize Finalist |
    200T grid points on 43K+ GPUs - MFlowCode/MFC
  image: https://repository-images.githubusercontent.com/198475661/b7e3edbe-e0d8-4d91-90d9-15fb90155d66
  title: 'GitHub - MFlowCode/MFC: Exascale multiphase flow solver — 2025 Gordon Bell
    Prize Finalist | 200T grid points on 43K+ GPUs'
  url: https://github.com/MFlowCode/MFC
source: vk
title: Один квадриллион степеней свободы в единой задаче CFD
---

Lawrence Livermore National Laboratory’s (LLNL)  провели на своем суперкомпьютере El Capitan (№1 в рейтинге TOP500, ~1,742 exaFLOPS) CFD моделирование взаимодействия выхлопных факелов нескольких ракетных двигателей (по типу SpaceX Super Heavy). Для расчета было задействовано 44 500 гибридный вычислителей AMD Instinct MI300A (CPU+GPU с общей унифицированной памятью = APU) размещенные в 11 136 вычислительных узлах. Таким образом, под один расчет были задействованы все мощности El Capitan полностью!

Расчет выполнял открытый код Multicomponent Flow Code, поддерживаемый группой Bryngelson. В модели учитывалась сжимаемость потока (число Маха до 10) и ударные волны. А вот на DNS мощностей не хватило.

Работа является финалистом премии ACM Gordon Bell Prize 2025 - высшей награды в области высокопроизводительных вычислений. Кроме выдающихся размеров, постановка может похвастаться еще и новой техникой регуляризации ударных волн под названием Information Geometric Regularization (IGR), разработанной профессорами Spencer Bryngelson (Georgia Tech), Florian Schäfer (NYU Courant) и Ruijia Cao.

Официальный пресс релиз:
https://www.llnl.gov/article/53626/gordon-bell-finalist-team-pushes-scale-rocket-simulation-el-capitan

Препринт научной статьи по итогам численного эксперимента:
https://arxiv.org/abs/2505.07392

Репозиторий использованного решателя на GitHub:
https://github.com/MFlowCode/MFC

[Gordon Bell finalist team pushes scale of rocket simulation on El Capitan](https://www.llnl.gov/article/53626/gordon-bell-finalist-team-pushes-scale-rocket-simulation-el-capitan)
https://arxiv.org/abs/2505.07392
https://github.com/MFlowCode/MFC
