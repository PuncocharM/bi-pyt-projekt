import io
import jpgparser
from PIL import Image
from argparse import ArgumentParser

parser = ArgumentParser(description='Stereoskopicke obrazky: skript umi nacist JPEG soubor a jeho levou polovinu ulozit do jineho souboru spolu s nestandartnimi metadaty. Zroven tato metadata umi i cist.')
parser.add_argument('-a', '--akce', choices=['crop', 'getmeta'], help='Akce crop nacte soubor, a jeho polovinu ulozi s polu s metadaty do vystupniho souboru "out_<vstupni soubor.jpg>". Akce getmeta zobrazi metadata ulozena akci crop.', required=True)
parser.add_argument('soubor', help='nazev souboru s JPEG obrazkem')
args = parser.parse_args()


if args.akce == 'crop':
    # vlastni test, jestli se jedna o JPEG soubor
    if jpgparser.JpegStructure.fromFile(args.soubor) == None:
        exit()
    # seriznuti obrazku na polovinu a ulozeni do bytestreamu
    img = Image.open(args.soubor)
    imgCropped = img.crop((0,0,img.width//2, img.height))
    bio = io.BytesIO()
    imgCropped.save(bio, 'jpeg')
    bio.seek(0)
    
    js = jpgparser.JpegStructure.fromStream(bio)
    if js == None:
        exit()
    zprava = input('Zadejte tajnou zpravu: ').encode('ascii')
    js.addMarker(jpgparser.Marker(b'\xff\xef', None, zprava))
    js.writeToFile('out_'+args.soubor)
          

if args.akce == 'getmeta':
    js = jpgparser.JpegStructure.fromFile(args.soubor)
    if (js == None):
        exit()
    markers = js.getMarkers(b'\xff\xef')
    if (len(markers) <= 0):
        print('Soubor neobsahuje hledana metadata')
    else:
        for marker in markers:
            print('Tajna zprava = "' + marker.data.decode('ascii') + '"')
    
        