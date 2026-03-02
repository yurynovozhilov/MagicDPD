---
layout: post
title: "Ansys Batch Connections"
date: 2021-05-17T13:01:38+00:00
author: "MagicDPD"
source: vk
original_url: https://vk.com/wall-97265142_1953
tags:
  - ansys
  - meshing
  - batch_connections
---

Где-то год назад Ansys выкатил функцию Batch Connections и про нее почему-то мало кто знает до сих пор, хотя она очень полезна и важна.




https://www.youtube.com/watch?v=tWgSf6TUdfc




Итак, Batch Connections позволяет собирать сетки на больших и сложных оболочечных моделях, состоящих из большого числа поверхностей. В классическом построении сетки, вам необходимо построить Shared Topology склейку геометрии в единое целое, и потом уже строить сетку на одном ядре процессора. Batch Connections предлагает не склеивать геометрию, а отдать раскленную модель сеточному генератору. Тот сам сначала построить сетку на всех оболочечных телах параллельно многопоточно, а потом сделает сшивку по узлам, дотянув их по месту. Получается быстрее, проще и стабильнее - всем, кто работает с shell геометрией изучать обязательно!




https://www.youtube.com/watch?v=zxytjWbYEho





https://www.youtube.com/watch?v=1lJJo19fvug





https://www.youtube.com/watch?v=etEBANwvRxY





https://www.youtube.com/watch?v=etEBANwvRxY





https://www.youtube.com/watch?v=duYS7jTslhI





https://www.youtube.com/watch?v=QoDdM0Z5_Cg


#ansys #batch_connections #meshing
https://tinyurl.com/ygzw3232
