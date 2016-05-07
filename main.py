import io
import sys
import binascii
from PIL import Image
import jpgparser

jp = jpgparser.JpegStructure.fromFile("RESTAURACE POHADKA - YoureGone.jpg" )

if (len(sys.argv) < 3):
    print('Pouziti:')
    print('    skript.py <Operace> <nazev souboru>')
    print('    Operace: "crop" nebo "getmeta"')
    print('        crop orizne obrazek, prida tajnou zpravu a ulozi do out.jpg')
    print('        getmeta zobrazi skrytou zpravu')
    exit()


if sys.argv[1] == 'crop':        
    img = Image.open(sys.argv[2])
    imgCropped = img.crop((0,0,img.width//2, img.height))
    f = io.BytesIO()
    imgCropped.save(f, 'jpeg')
    f.seek(0)

    fo2 = open('out2.jpg', 'wb')
    fo2.write(f.getvalue())
    fo2.close()

    fo = open('out.jpg', 'wb')
    #f = open(sys.argv[1], 'rb')

    if (f.read(2) != b'\xff\xd8'):
        print('Chyba: nejedna se o JPEG soubor')
        
    fo.write(b'\xff\xd8')    

    while True: #jednotlive markery
        bts = f.read(2)
        if (bts == b''):
            print('Chyba: predcasny EOF')
            exit()
        print('Marker ' + binascii.hexlify(bts).decode('ascii') + ' @ ' + str(f.tell())+' = '+hex(f.tell()))
        if (bts[0] != 0xff):
            print('Chyba: Zacatek markeru se nerovna FF, ale ' + hex(bts[0]))
            exit()
        if (bts == b'\xff\xd9'):
            print('Chyba: Predcasny marker EOI: FF D9')
            exit()
        if (bts == b'\xff\xda'):
            print('ffda = SOS')
            break
        fo.write(bts)#
        bdelka = f.read(2)
        fo.write(bdelka)#
        delka = 256 * bdelka[0] + bdelka[1] - 2
        if (delka <= 0):
            print('Chyba: zaporna delka '+delka+' = '+binascii.hexlify(bdelka).decode('ascii'))
            exit()
        blok = f.read(delka)
        fo.write(blok)#
        
    zprava = b'Lorem Ipsum'
    delka = len(zprava)+2
    bdelka1 = bytes([delka])
    bdelka = (2-len(bdelka1)) * b'\x00' + bdelka1
    fo.write(b'\xff\xef')
    fo.write(bdelka)
    fo.write(zprava)
    fo.write(b'\xff\xda')#
      
    while True:
        byte = f.read(1)
        fo.write(byte)
        if (byte == b''):
            print('Chyba: predcasny EOF')
            exit()
        if (byte == b'\xff'):
            tmp = f.read(1)
            fo.write(tmp)
            if (tmp == b'\xd9'):
                print('ffd9 = EOI @ ' + str(f.tell())+' = '+hex(f.tell()))
                break

    if (f.read() != b''):
        print('Chyba: po EOI by nemelo nic nasledovat')
        
    print('OK: Parse probehl bez chyby')    
    fo.close()


if sys.argv[1] == 'getmeta':
    f = open(sys.argv[2], 'rb')
    if (f.read(2) != b'\xff\xd8'):
        print('Chyba: nejedna se o JPEG soubor')
    while True: #jednotlive markery
        bts = f.read(2)
        if (bts == b''):
            print('Chyba: predcasny EOF')
            exit()
        print('Marker ' + binascii.hexlify(bts).decode('ascii') + ' @ ' + str(f.tell())+' = '+hex(f.tell()))
        if (bts[0] != 0xff):
            print('Chyba: Zacatek markeru se nerovna FF, ale ' + hex(bts[0]))
            exit()
        if (bts == b'\xff\xd9'):
            print('Chyba: Predcasny marker EOI: FF D9')
            exit()    
        if (bts == b'\xff\xda'):
            print('ffda = SOS')
            break
        bdelka = f.read(2)
        delka = 256 * bdelka[0] + bdelka[1] - 2
        if (delka <= 0):
            print('Chyba: zaporna delka '+str(delka)+' = '+binascii.hexlify(bdelka).decode('ascii'))
            exit()
        blok = f.read(delka)
        if (bts == b'\xff\xef'):
            print('Meta je ('+str(delka)+'): '+blok.decode('ascii'))
            exit()
    
        