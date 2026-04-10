---
layout: post
title: "Полноценное #HPC в облаке"
date: 2016-08-01T07:03:57+00:00
author: "GlukRazor"
source: vk
tags:
  - CFD
  - Infiniband
  - RDMA
  - ANSYS
  - HPC
  - Azure
  - Cloud
  - AWS
---

http://www.engineering.com/DesignSoftware/DesignSoftwareArticles/ArticleID/12777/ANSYS-CFD-Sees-Scalability-to-1024-Cores-on-Microsoft-Azure.aspx

Инфоповод по сообщению во множестве блогов: #ANSYS #CFD распараллелился почти линейно на 1024 ядра в облаке #Azure. Новость эта несет в себе сразу две морали.

Первая мораль: ANSYS начинает рассматривать Azure как дополнение к #AWS - и это очень хорошо. Конкуренция облаков - это всегда хорошо для пользователя.

Вторая мораль: если дать CFD коду нормальный интерконнект, то он полетит даже в облаке. Как я уже много раз говорил, у Microsoft в Azure есть полноценный #Infiniband с поддержкой #RDMA. Infiniband = HPC, а значит можно очень хорошо посчитать.

А еще я очень жду, когда же у AWS тоже будет интреконнект.

[ANSYS CFD Sees Scalability to 1024 Cores on Microsoft Azure](https://www.engineering.com/DesignSoftware/DesignSoftwareArticles/ArticleID/12777/ANSYS-CFD-Sees-Scalability-to-1024-Cores-on-Microsoft-Azure.aspx)
http://www.engineering.com/DesignSoftware/DesignSoftwareArticles/ArticleID/12777/ANSYS-CFD-Sees-Scalability-to-1024-Cores-on-Microsoft-Azure.aspx
