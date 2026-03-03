---
layout: post
title: "Как работает бессеточный решатель Intact Solutions, Inc."
date: 2024-11-14T13:01:53+00:00
author: "Yury Novozhilov"
source: vk
---

Как работает бессеточный решатель Intact Solutions, Inc.

Читатели моего канала уже слышали про новый "бессетоный" стартап Intact Solutions, Inc. который очень агрессивно продвигает себя на рынке, дружит с nTopo и пытается унижать FEM решатели. Сегодня я наткнулся на их брошюру с полным описанием теории работы их метода с примерами, формулами, картинками и даже ссылками на научные стати.

При беглом прочтении, кажется, что коллеги используют так называемый Погруженный метод Галеркина ( Immersed Galerkin Method ) на основе фоновой воксельной сетки. Таким образом, это действительно можно назвать бессеточным методом (по крайней мере, вам не нужна конформная сетка). И модель получается не очень тяжелая. Но вот если сравнивать это с Trimmed Solid IGA  (из LS-DYNA или COREFORM), то точность расчет, особенно на границах области, страдает.

Короче, интесно видеть на рынке очередной способ уйти от надоевшей всем сетки конечных элементов.

https://www.linkedin.com/posts/jousefmurad_meshless-fea-intact-ugcPost-7254129225975087106-8A5B

[Meshless FEA Intact | Jousef Murad | 10 comments](https://www.linkedin.com/posts/jousefmurad_meshless-fea-intact-ugcPost-7254129225975087106-8A5B?utm_source=share&utm_medium=member_desktop)
https://www.linkedin.com/posts/jousefmurad_meshless-fea-intact-ugcPost-7254129225975087106-8A5B
