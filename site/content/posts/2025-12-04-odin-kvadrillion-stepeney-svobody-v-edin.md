---
layout: post
title: "Один квадриллион степеней свободы в единой задаче CFD"
date: 2025-12-04T09:03:46+00:00
author: "Yury Novozhilov"
source: vk
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
