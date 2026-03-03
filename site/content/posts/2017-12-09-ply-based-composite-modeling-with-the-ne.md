---
layout: post
title: "Ply-based composite modeling with the new *ELEMENT_SHELL_COM"
date: 2017-12-09T07:16:05+00:00
author: "GlukRazor"
source: vk
---

Ply-based composite modeling with the new *ELEMENT_SHELL_COMPOSITE keyword.

http://ift.tt/2AFXG9h

Статья от 2011 года про дружбу LS-DYNA и ANSYS Composite PrepPost и пара комментариев к ней от меня:

1. *ELEMENT_SHELL_OFFSET_COMPOSITE при отображении shell-элементов в режиме "с толщиной" не понимают, к сожалению, ни LSPP, ни Hypermesh. Таким образом, укладки созданные в Composite PrepPost можно визуализировать только в Composite PrepPost.

2. *ELEMENT_SHELL_OFFSET_COMPOSITE требует указания PART_ID (PID), в свою очередь, *PART требует SECTION_ID (SID). В результате, чтобы все заработало, нужно в любом случае создавать *SECTION и указывать в нем произвольные толщины элементов, которые будут в ходе решения замещены решателем данными из *ELEMENT_SHELL_OFFSET_COMPOSITE. При этом (!), открывая такой k-файл в LSPP, следует помнить, что препроцессор будет апелировать в данным из *SECTION, а не из *ELEMENT_SHELL_OFFSET_COMPOSITE при расчете, например, массы или объема элементов. В пост-процессинге, открыв binout, LSPP читает "правильные" свойства из *ELEMENT_SHELL_OFFSET_COMPOSITE.

3. Используя нынешний релиз ANSYS Composite PrepPost, в него напрямую (т.е. в standalone режиме) можно закидывать дайновские k-файлы, заранее созданные в LSPP, Hypermesh или Notepad ;). Для этого нужно перейти в Composite PrepPost в Tools —> Preferences —> ACP —> Add-Ons и подключить LS-DYNA Interface (там это идет как Beta-Feature). После создания укладок в Composite PrepPost, это все можно СРАЗУ сохранить в k-файл, щелкнув правой кнопкой мыши в дереве Composite PrepPost на названии модели и выбрав "Save Analysis Model...".Media

http://ift.tt/2A91Wxf

http://ift.tt/2A6294d
http://ift.tt/2A614cm
http://ift.tt/2A614cm
http://ift.tt/2AGNeOM
http://ift.tt/2A91Wxf
