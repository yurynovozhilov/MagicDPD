.PHONY: serve previews

# Запустить локальный Hugo-сервер с актуальными превью
serve: previews
	cd site && hugo server --buildDrafts

# Только сфетчить/обновить превью (модифицирует front matter постов)
previews:
	python fetch_link_previews.py
