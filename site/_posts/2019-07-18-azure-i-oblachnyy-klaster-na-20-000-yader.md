---
layout: post
title: "Azure и облачный кластер на 20 000 ядер"
date: 2019-07-18T13:00:18+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_1532
tags:
  - HPC
  - cloud
  - Azure
images:
  - url: "/assets/images/1532.jpg"
---

Коллеги из Microsoft немного поиграли мускулатурой в своих ЦОД West US 2 и East US. Недолго думая, они смогли собрать HPC кластер из 512 виртуальных машин (новая серия HC) = 22 528 физических вычислительных ядер Intel Xeon Platinum 8168 (безо всякого там Hyper Threading). При этом это действительно HPC, так как виртуалки были объединены настоящим интерконнектом 100 Gb/s InfiniBand (SR-IOV). Профит: очень быстрый кластер в облаке с хорошей масштабируемостью согласно бенчмаркам. И да, не забывайте, что Azure — главный партнер ANSYS в облаке.







Оригинальный текст:



Azure Benchmarks HC-series Across 20,000 cores for HPC



https://azure.microsoft.com/en-us/blog/azure-hc-series-virtual-machines-crosses-20000-cores-for-hpc-workloads/

#Azure #cloud #HPC

https://wp.me/p9vWYY-2BH
