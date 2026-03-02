---
date: 2026-02-10 14:58:41+00:00
link_previews:
- description: "OpenLUDWIG now has a cumulant compressible solver, computes nodal
    loads on a set of given points for multiple STL models, and has a post-processor
    for surface data, net forces and nodal loads. A validation of the drag coefficient
    of a cube and a sphere in compressible regime has been added. \n\nThe release
    of Claude 4.6 last week and the rainy weather in Madrid enticed me to nudge the
    maturity of OpenLUDWIG up a notch last weekend. The new cumulant collision operator
    makes the solver stable at ext"
  image: https://media.licdn.com/dms/image/v2/D4E22AQEyGFGhGBufOA/feedshare-shrink_800/B4EZxET1xvH8Ag-/0/1770672577998?e=2147483647&v=beta&t=W198Yin-ct3DzEcUVO6wBDIa8MEfD_ddO2GMudOnuvY
  title: '#julialang #lbm #cfd | Raul Llamas'
  url: https://www.linkedin.com/posts/raul-llamas-405a5014a_julialang-lbm-cfd-ugcPost-7426739092937154561-Hkp6
original_url: https://t.me/MagicDPD/3103
source: tg
title: OpenLUDWIG
---

В свое посте про открытый решатель OpenLUDWIG не стесняеется гворить, что писал последнюю версию с Claude 4.6. Так почему я должен стесняться писать пост об этом солвере с Клодом!? Хотя бы дурацких опечаток не будет. Итак, вот что мы имеем.

GPU‑ускорение + LBM
LBM по природе отлично масштабируется на GPU. То, что солвер изначально заточен под GPU, означает на порядки более высокую производительность по сравнению с классическими CFD на CPU.

D3Q27 дискретизация
Это самая богатая решётка для 3D‑LBM.
Преимущества: лучшая изотропия, более точные турбулентные структуры, устойчивость на сложных скоростных полях.

Cumulant collision operator
Это «золотой стандарт» современной LBM‑математики.
Сильно повышает устойчивость, снижает численные ошибки, даёт хороший контроль над вязкостью. Это гораздо продвинутее классических BGK/MRT схем.

WALE турбулентность
WALE подходит для LES, автоматически подстраивается под вязкость и корректно работает даже возле стенок (wall‑adapted). Для LBM — очень удачная комбинация.

Многоуровневое адаптивное уточнение сетки
В LBM это непросто реализовать.
Если есть AMR, значит солвер поддерживает высокую точность на локальных зонах интереса (вихри, границы, пролёты), и экономит гигантское количество ячеек.

Граничные условия Bouzidi
Одни из самых точных LBM‑методов для криволинейных/произвольных поверхностей. Намного лучше стандартных bounce‑back.

Опциональная термальная DDF с коррекцией сжимаемости
Это тоже редкость — LBM обычно слаб для сжимаемых и тепловых задач.
Поддержка thermal double distribution function означает возможность моделировать тепловые эффекты, не доходя до полноценной энергетической Navier–Stokes.

Расчёт аэродинамических сил по поверхности
Большинство LBM‑солверов работают через momentum‑exchange метод;
наличие surface‑based force integration — признак точной аэродинамики, необходимой для aerospace/automotive задач.

https://www.linkedin.com/posts/raul-llamas-405a5014a_julialang-lbm-cfd-ugcPost-7426739092937154561-Hkp6
OpenLUDWIG
