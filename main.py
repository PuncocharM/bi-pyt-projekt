import io
import jpgparser
from PIL import Image
from argparse import ArgumentParser

parser = ArgumentParser(description='Stereoskopicke obrazky: skript umi nacist JPEG soubor a jeho levou polovinu ulozit do jineho souboru spolu s nestandartnimi metadaty ve forme textove zpravy a prilozeneho souboru. Zroven tato metadata umi i cist.')
parser.add_argument('soubor_in', help='nazev vstupniho souboru s JPEG obrazkem')
parser.add_argument('-c', '--crop', nargs=3, metavar=('meta_text', 'meta_soubor', 'soubor_out'), help='crop nacte soubor_in, a jeho polovinu ulozi s polu s meta_zpravou a meta_souborem do souboru soubor_out')
parser.add_argument('-g', '--get', metavar='soubor_out', help='Ze souboru soubor_in ziska ulozenou zpravu a ulozeny soubor zapise do soubor_out')
args = parser.parse_args()


if args.crop:
    # vlastni test, jestli se jedna o JPEG soubor
    if jpgparser.JpegStructure.fromFile(args.soubor_in) == None:
        exit()
    # seriznuti obrazku na polovinu a ulozeni do bytestreamu
    img = Image.open(args.soubor_in)
    imgCropped = img.crop((0,0,img.width//2, img.height))
    bio = io.BytesIO()
    imgCropped.save(bio, 'jpeg')
    bio.seek(0)
    
    js = jpgparser.JpegStructure.fromStream(bio)
    if js == None:
        exit()
    js.addMarker(jpgparser.Marker(b'\xff\xef', None, args.crop[0].encode('ascii')))
    try:
        with open(args.crop[1], 'rb') as f:
            while True:
                fobsah = f.read(256*256-3)
                if fobsah == b'':
                    break
                js.addMarker(jpgparser.Marker(b'\xff\xee', None, fobsah))
    except IOError:
        print('Chyba: Nepodarilo se nacist soubor '+args.crop[1]+'.')
        exit()
    js.writeToFile(args.crop[2])
          

if args.get:
    js = jpgparser.JpegStructure.fromFile(args.soubor_in)
    if (js == None):
        exit()
    markers = js.getMarkers(b'\xff\xef')
    if (len(markers) <= 0):
        print('Soubor neobsahuje ukrytou zpravu')
    else:
        for marker in markers:
            print('Tajna zprava = "' + marker.data.decode('ascii') + '"')
    markers = js.getMarkers(b'\xff\xee')
    if (len(markers) <= 0):
        print('Soubor neobsahuje prilozeny soubor')
    else:
        try:
            with open(args.get, 'wb') as f:
                for marker in markers:
                    f.write(marker.data)
        except IOError:
            print('Chyba: pri zapisu do souboru '+args.get+'.')
    
        