---
layout: post
title: "То, что сейчас любой уважающий себя код умеет получать преимущества от GPU - это уже не новость."
date: 2015-07-12T11:00:05+00:00
author: "GlukRazor"
source: vk
---

Давным-давно ANSYS Mechanical протоптал эту тропинку для неявных решателей методом конечных элементов. Потом Fluent задал тон для коммерческих CFD кодов общего назначения. В общем, ANSYS тут был пионером. Однако, все подобные коды всегда использовали GPGPU NVIDA.

И вот мне попадается статья про старый добрый NX Nastran, который оказывается вполне комфортно использует наработки AMD в области GPGPU для расчетов. Как давний поклонник ATI, GPU бизнес которой приобрел AMD, я очень рад!

[NX Nastran Performance Improvements](http://community.plm.automation.siemens.com/t5/Femap-Blog/NX-Nastran-Performance-Improvements/ba-p/304258)
