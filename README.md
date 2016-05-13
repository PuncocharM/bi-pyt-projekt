# bi-pyt-projekt

Potřebné externí balíčky: Pillow ("pip install Pillow")

---

usage: main.py [-h] [-c meta_text meta_soubor soubor_out] [-g soubor_out] soubor_in

Stereoskopicke obrazky: skript umi nacist JPEG soubor a jeho levou polovinu
ulozit do jineho souboru spolu s nestandartnimi metadaty ve forme textove
zpravy a prilozeneho souboru. Zroven tato metadata umi i cist.

positional arguments:
  soubor_in             nazev vstupniho souboru s JPEG obrazkem

optional arguments:
  -h, --help            show this help message and exit
  -c meta_text meta_soubor soubor_out, --crop meta_text meta_soubor soubor_out
                        crop nacte soubor_in, a jeho polovinu ulozi s polu s
                        meta_zpravou a meta_souborem do souboru soubor_out
  -g soubor_out, --get soubor_out
                        Ze souboru soubor_in ziska ulozenou zpravu a ulozeny
                        soubor zapise do soubor_out
