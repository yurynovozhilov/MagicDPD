---
layout: post
title: "Расчет подрыва ЖБ плиты с учетом фрагментации"
date: 2018-02-07T18:00:53+00:00
author: "GlukRazor"
source: vk
original_url: https://vk.com/wall-97265142_774
tags:
  - fragmentation
  - DEFINE_ADAPTIVE_SOLID_TO_SPH
  - SPH
  - fracture
  - reinforcement
  - concrete
  - LS
  - ParticleBlast
  - blast
  - LSTC
  - CONSTRAINED_BEAM_IN_SOLID
images:
  - url: "/assets/images/775.jpg"
---

Расчет подрыва ЖБ плиты с учетом фрагментации
Очень красивый пример от LSTC, демонстрирующий работу LS-DYNA в области расчета взрывов и переноса нагрузок от них на конструкции. Разберем три составляющих успеха данного расчета.

<!--more-->

<ol>
<li>Имеем бетонную плиту, армированную стальными стержнями (естественно beam арматура внедряется в solid бетон при помощи специальных уравнений связи типа *CONSTRAINED_BEAM_IN_SOLID).</li>
<li>Дальше, на этой плите расположен заряд в оболочке из shell элементов. Заряд ВВ моделируется в постановке Particle Blast Method (PBM) - не надо заморачиваться с генерацией SPH или переходом в эйлеров домен. PBM решает быстро и точно!</li>
<li>И на десерт, для solid элементов бетона задается *DEFINE_ADAPTIVE_SOLID_TO_SPH - автоматическое переключение умерших solid элементов в SPH частицы, моделирующие разлет осколков. Надо отдельно отметить, что получающиеся SPH частицы могут не просто разлетаться, как точечные массы, но и работать как тот же самый бетон, но уже сильно поврежденный - между ними есть определенный потенциал взаимодействия.</li>
</ol>

https://www.youtube.com/watch?v=QHbO6tRPI3c
#blast #concrete #CONSTRAINED_BEAM_IN_SOLID #DEFINE_ADAPTIVE_SOLID_TO_SPH #fracture #fragmentation #LS-DYNA #LSTC #ParticleBlast #reinforcement #SPH
https://wp.me/p9vWYY-1BK
