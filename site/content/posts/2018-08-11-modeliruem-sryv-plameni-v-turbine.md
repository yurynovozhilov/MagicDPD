---
author: GlukRazor
date: 2018-08-11 18:00:43+00:00
images:
- url: /assets/images/1068.jpg
layout: post
link_previews:
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/a/a6/4-Stroke-Engine.gif
  title: Камера сгорания — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%BC%D0%B5%D1%80%D0%B0_%D1%81%D0%B3%D0%BE%D1%80%D0%B0%D0%BD%D0%B8%D1%8F
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/e/ea/%D0%9F%D0%B8%D0%BC%D0%BE%D0%BD%D0%B5%D0%BD%D0%BA%D0%BE_%D0%98%D0%B7-%D0%BB%D0%B5%D1%81%D1%83_1900.jpg
  title: Топливо — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%A2%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%BE
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/c/c3/Liquid_oxygen_in_a_beaker_4.jpg
  title: Кислород — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%9A%D0%B8%D1%81%D0%BB%D0%BE%D1%80%D0%BE%D0%B4
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Bird_Diversity_2013.png/960px-Bird_Diversity_2013.png
  title: Птицы — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%9F%D1%82%D0%B8%D1%86%D1%8B
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/2/2b/Bogota_hailstorm.jpg
  title: Град — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%93%D1%80%D0%B0%D0%B4
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/4/4a/MtCleveland_ISS013-E-24184.jpg
  title: Вулканический пепел — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%92%D1%83%D0%BB%D0%BA%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%BF%D0%B5%D0%BF%D0%B5%D0%BB
- description: ''
  image: https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Pedalarm_Bruch.jpg/1280px-Pedalarm_Bruch.jpg
  title: Усталость материала — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%A3%D1%81%D1%82%D0%B0%D0%BB%D0%BE%D1%81%D1%82%D1%8C_%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B0
- description: ''
  image: ''
  title: Воздушно-реактивный двигатель — Википедия
  url: https://ru.wikipedia.org/wiki/%D0%92%D0%BE%D0%B7%D0%B4%D1%83%D1%88%D0%BD%D0%BE-%D1%80%D0%B5%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9_%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D1%82%D0%B5%D0%BB%D1%8C
source: vk
tags:
- Flameout
- CFD
- Combustion
- ANSYS
- FGM
- Fluent
title: Моделируем срыв пламени в турбине
---

Согласно Википедии, срыв пламени — затухание пламени в камере сгорания, как нарушение работы воздушно-реактивного двигателя; может быть вызвано такими причинами, как: нехватка топлива, нарушение работы компрессора, недостаток кислорода, повреждение инородными телами (например, попадание птиц, града или вулканического пепла), крайне неблагоприятные погодные условия (ветер, влажность, дождь, изморось), усталостные механические повреждения.
ANSYS в своем блоге опубликовал очень занимательную статью на тему моделирования данного процесса. Тут и исследования работы фарсунок, и моделирование турбулентных течений в нестационарных постановках, и химия. Конечно,  не обошлось без доли магии под названием Flamelet Generated Manifold (FGM). Короче, я поплыл к середине поста. Но если вы в теме, то текст должен зайти на ура.
Полезные ссылки по теме:
How to Efficiently Simulate a Gas Turbine Flameout

Efficiently Modeling Turbulent Combustion with Realistic Chemistry Using a Flamelet-Generated Manifold


#ANSYS #CFD #Combustion #FGM #Flameout #Fluent
http://bit.ly/2KGgZTr

https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D0%BC%D0%B5%D1%80%D0%B0_%D1%81%D0%B3%D0%BE%D1%80%D0%B0%D0%BD%D0%B8%D1%8F
https://ru.wikipedia.org/wiki/%D0%92%D0%BE%D0%B7%D0%B4%D1%83%D1%88%D0%BD%D0%BE-%D1%80%D0%B5%D0%B0%D0%BA%D1%82%D0%B8%D0%B2%D0%BD%D1%8B%D0%B9_%D0%B4%D0%B2%D0%B8%D0%B3%D0%B0%D1%82%D0%B5%D0%BB%D1%8C
https://ru.wikipedia.org/wiki/%D0%A2%D0%BE%D0%BF%D0%BB%D0%B8%D0%B2%D0%BE
https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BC%D0%BF%D0%B0%D0%B6_(%D0%B0%D0%B2%D0%B8%D0%B0%D1%86%D0%B8%D1%8F)
https://ru.wikipedia.org/wiki/%D0%9A%D0%B8%D1%81%D0%BB%D0%BE%D1%80%D0%BE%D0%B4
https://ru.wikipedia.org/wiki/%D0%9F%D1%82%D0%B8%D1%86%D1%8B
https://ru.wikipedia.org/wiki/%D0%93%D1%80%D0%B0%D0%B4
https://ru.wikipedia.org/wiki/%D0%92%D1%83%D0%BB%D0%BA%D0%B0%D0%BD%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9_%D0%BF%D0%B5%D0%BF%D0%B5%D0%BB
https://ru.wikipedia.org/wiki/%D0%A3%D1%81%D1%82%D0%B0%D0%BB%D0%BE%D1%81%D1%82%D1%8C_%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D0%B0
https://www.ansys-blog.com/how-to-efficiently-simulate-a-gas-turbine-flameout/
https://www.ansys-blog.com/turbulent-combustion-flamelet-generated-manifolds/
http://bit.ly/2KGgZTr
