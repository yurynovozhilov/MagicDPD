---
date: 2019-01-10 17:01:22+00:00
images:
- url: /assets/images/1300.jpg
link_previews:
- description: Сегментация изображений является задачей разбиения цифрового изображения
    на одну или несколько областей, представляющих интерес. Это фундаментальная проблема
    в области компьютерного зрения, которая...
  image: https://habr.com/share/publication/332692/31dedc205152123e11cdec8e5b781266/
  title: Бинарная сегментация изображений методом фиксации уровня (Level set method)
  url: https://habr.com/post/332692/
- description: ''
  image: ''
  title: Software | M2DO - Multiscale, Multiphysics Design Optimization
  url: http://m2do.ucsd.edu/software/
- description: Contribute to M2DOLab/OpenLSTO development by creating an account on
    GitHub.
  image: https://opengraph.githubassets.com/bb35428f68a5171fd259cb03543e0d90a107495a193ef66216f0ea4e618642f0/M2DOLab/OpenLSTO
  title: GitHub - M2DOLab/OpenLSTO
  url: https://github.com/M2DOLab/OpenLSTO
original_url: https://t.me/MagicDPD/1300
source: tg
title: OpenLSTO - открытый код оптимизации топологии
---

Летом 2018 года команда&nbsp;M2DO (Multiscale Multiphysics Design Optimization Laboratory)&nbsp;Калифорнийского университета Сан-Диего представила новый код для решения задач топологической оптимизации&nbsp;OpenLSTO.&nbsp;



  
    Результаты 3D оптимизации
  



Название кода расшифровывается как&nbsp; «open-source software for level set based structural topology optimization», что может быть переведено на русский язык как «программное обеспечение с открытым исходным кодом для топологической оптимизации с использованием метода фиксации уровня». 


  Взаимосвязь между функцией фиксации уровня (снизу) и получаемым контуром (сверху)



Подробнее про работу метода на русском можно почитать статью на Хабре:&nbsp;https://habr.com/post/332692/. Данный метод сейчас начинает очень активно применяться при решении задач оптимизации топологии, так как дает хорошие гладкие формы новой геометрии быстро и эффективно. И OpenLSTO, насколько я знаю, первая open source реализация такого подхода.



  Результаты 2D оптимизации



Код, к сожалению, написан на C++. Без его знания вы хороших результатов не добьётесь, так как GUI у кода пока нет — есть только командная строка под *nix совместимыми операционными системами. Ну хоть результаты можно смотреть в ParaView.&nbsp;



   Домашняя страница проекта:&nbsp;http://m2do.ucsd.edu/software/ 
   Репозиторий GitHub:&nbsp;https://github.com/M2DOLab/OpenLSTO 
  Документация с учебными примерами:&nbsp;http://m2do.ucsd.edu/static/pdf/OpenLSTO-Tutorial-v1.0.pdf


#LevelSetMethod #M2DO #OpenSource #OpenLSTO #Optimization #Topology
http://bit.ly/2VLn1bU
