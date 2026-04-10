---
author: Yury Novozhilov
date: 2024-03-13 14:01:35+00:00
images:
- url: /assets/images/2667.jpg
layout: post
link_previews:
- description: This is a Beta feature. API Behavior and Implementation may change
    in future. Isogeometric Analysis (IGA) is a new approach using NURBS to capture
    the CAD geometry accurately than the FE analysis. The FE analysis discretize the
    CAD geometry approximately into smaller elements to capture the features. This
    approximation may affect the accuracy of the result and increase the computational
    cost. IGA uses spline to exactly represent the CAD geometry to analyse the geometry
    and solver solves on the s
  image: ''
  title: Isogeometric analysis | Ansys Developer Portal
  url: https://developer.ansys.com/docs/prime-mesh-python-client-library-2024-r1-sp1/user_guide/iga.md
source: vk
title: Ansys pyPrimeMesh научилса делать IGA
---

Это прям big deal, ибо PrimeMesh - это новый главный движок сеточной генерации для всея прочностного ансиса. И вот, в версии 2024 R1 SP1 там появилась beta поддержка генерации IGA оболочечных моделей под LS-DYNA. До сего момента, такие модели мог создавать только LSPP (только не сложные, только через боль) и ANSA (только за деньги, и совесем не часть Ansys). Теперь у нас появилась возможность потрогать за API то, как наверно через пару лет IGA будут выглядеть в WB.

https://developer.ansys.com/docs/prime-mesh-python-client-library-2024-r1-sp1/user_guide/iga.md

https://lsdyna.ansys.com/wp-content/uploads/2023/12/Creation-of-Unstructured-Splines-for-IGA-based-solutions-in-LS-DYNA-Mukul-Kanitkar-Ansys-1.pdf

https://developer.ansys.com/docs/prime-mesh-python-client-library-2024-r1-sp1/user_guide/iga.md
https://lsdyna.ansys.com/wp-content/uploads/2023/12/Creation-of-Unstructured-Splines-for-IGA-based-solutions-in-LS-DYNA-Mukul-Kanitkar-Ansys-1.pdf
