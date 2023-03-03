https://www.nlpnotebook.com/python/internationalization/localization/gettext/text/translation/2019/11/25/i18n-and-l10n.html
https://phrase.com/blog/posts/translate-python-gnu-gettext/

<python_path> = "C:\Users\javim\AppData\Local\Programs\Python\Python310"

**Poner todos los strings del programa como: _(string)**

print(_("Hello world"))

**Crear plantilla con todos los strings a traducir encontrados**

`python <python_path>/Tools/i18n/pygettext.py -d base -o data/locale/base.pot reproc.py program`

**Completar la estructura:**

Copiando el base.pot como los base.mo

```
locale
├── en
│   └── LC_MESSAGES
│       ├── base.mo
│       └── base.po
├── es
│   └── LC_MESSAGES
│       ├── base.mo
│       └── base.po
└── base.pot
```

En cada base.mo traducir los strings, donde:

```
msgid "Texto identificador"
msgstr "Texto traducido"
```

**Compilar base.mo a base.po**

Por cada idioma:

`cd data/locale/<idioma>/LC_MESSAGES`

`python <python_path>/Tools/i18n/msgfmt.py -o base.mo base`

---

**Ejemplo**

```python
import gettext
gt = gettext.translation("base", localedir="data/locale", languages=["es"])
gt.install()
_ = gt.gettext
print(_("Hello world"))
```