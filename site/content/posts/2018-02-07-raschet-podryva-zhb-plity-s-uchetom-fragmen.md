---
author: GlukRazor
date: 2018-02-07 18:00:53+00:00
images:
- url: /assets/images/775.jpg
layout: post
link_previews:
- description: PBM simulation of the combined effect of blast and fragmentation loading
    of concrete wallThe structure response of a concrete wall subject to the combined
    bl...
  image: https://i.ytimg.com/vi/QHbO6tRPI3c/maxresdefault.jpg
  title: 'LS-DYNA PBM: Combined effect of blast and fragmentation loading of concrete
    wall'
  url: https://www.youtube.com/watch?v=QHbO6tRPI3c
source: vk
tags:
- ParticleBlast
- DEFINE_ADAPTIVE_SOLID_TO_SPH
- LSTC
- LS
- SPH
- fragmentation
- CONSTRAINED_BEAM_IN_SOLID
- fracture
- blast
- concrete
- reinforcement
title: Расчет подрыва ЖБ плиты с учетом фрагментации
---

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

https://www.youtube.com/watch?v=QHbO6tRPI3c
https://wp.me/p9vWYY-1BK
