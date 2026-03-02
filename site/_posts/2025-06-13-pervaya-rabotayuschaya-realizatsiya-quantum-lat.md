---
layout: post
title: "Первая работающая реализация Quantum Lattice Boltzmann Metho"
date: 2025-06-13T11:02:28+00:00
author: "Yury Novozhilov"
source: vk
original_url: https://vk.com/wall-97265142_2963
---

Сегодня снова поговорим о квантовых вычислениях. На прошлой неделе Ansys и Nvidia опубликовали пресс-релиз о том, что им удалось впервые выполнить вычислительную гидродинамическую (CFD) симуляцию с помощью квантового компьютера. Сам по себе пресс-релиз — это интересно, но настоящая ценность кроется в научной основе: результаты базируются на препринте статьи «Algorithmic Advances Towards a Realizable Quantum Lattice Boltzmann Method», поданной к публикации коллективом исследователей из Ansys Inc. и IonQ Inc. (Apurva Tiwari, Jason Iaconis, Jezer Jojo, Sayonee Ray, Martin Roetteler, Chris Hill, Jay Pathak) в журнале Quantum Physics 15 апреля 2025 года.

Это первая в мире работа, в которой квантовый компьютер действительно выполняет CFD-моделирование и использует для этого специализированных метод Quantum Lattice Boltzmann Method (QLBM). Этот алгоритм был предложен ещё Budinski в 2021 году, а теперь прошёл первую проверку на реальном квантовом оборудовании. Размерность решаемой двумерной задачи достигла впечатляющих 68 миллиардов узлов сетки, реализованных всего на 39 кубитах суперкомпьютера Gefion.

Пока что реализовано решение лишь линейного уравнения адвекции-диффузии, но в перспективе разработчики планируют расширить алгоритмы для моделирования более сложных нелинейных систем, таких как полноценные уравнения Навье–Стокса. Архитектура и алгоритмы специально оптимизированы под современные NISQ-устройства с ограниченным числом кубитов и уровнем шумов.

https://quantumzeitgeist.com/quantum-lattice-boltzmann-method-first-hardware-implementation-of-2d-3d-fluid-simulations/
https://arxiv.org/pdf/2504.10870
https://www.ansys.com/blog/scaling-quantum-computing-research
