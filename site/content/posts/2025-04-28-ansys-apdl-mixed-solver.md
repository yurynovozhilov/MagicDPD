---
layout: post
title: "Ansys APDL Mixed Solver"
date: 2025-04-28T12:03:05+00:00
author: "Yury Novozhilov"
source: vk
---

Ansys APDL Mixed Solver

Я просмотрел интересное нововведение в 2025 R1. В новом релизе появился целый новый решатель для СЛАУ. Теперь у нас есть не только прямой (Sprase) и итеративный (PCG) но и промежуточный вариант, названный Mixed Solver. Новый решатель должен кушать меньше памяти чем прямой, но сходиться лучше, чем итеративный. При это он должен особенно хорошо ускоряться на GPU даже с FP32 (это уже не гражданские карты, но еще не серверные числодробилки).

https://www.youtube.com/watch?v=TKnsFCBUscM

https://www.youtube.com/watch?v=TKnsFCBUscM
