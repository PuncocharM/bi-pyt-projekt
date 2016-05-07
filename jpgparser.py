import io
import sys
import binascii
from PIL import Image


        
class JpegStructure:
    markers = {}

    @staticmethod
    def fromBytes(bts):
        bio = io.BytesIO(bts)
        return fromStream(bts)
    
    @staticmethod
    def fromFile(fileName):
        f = open(fileName, 'rb')
        r = JpegStructure.fromStream(f)
        f.close()
        return r
    
    @staticmethod
    def fromStream(stream):
        js = JpegStructure()
        if (stream.read(2) != b'\xff\xd8'):
            print('Chyba: nejedna se o JPEG soubor')
            return None

        while True: #jednotlive markery
            bts = stream.read(2)
            if (bts == b''):
                print('Chyba: predcasny EOF')
                exit()
            print('Marker ' + binascii.hexlify(bts).decode('ascii') + ' @ ' + str(stream.tell())+' = '+hex(stream.tell()))
            if (bts[0] != 0xff):
                print('Chyba: Zacatek markeru se nerovna FF, ale ' + hex(bts[0]))
                exit()
            if (bts == b'\xff\xd9'):
                print('Chyba: Predcasny marker EOI: FF D9')
                exit()
            if (bts == b'\xff\xda'):
                print('ffda = SOS')
                break
            bdelka = stream.read(2)
            delka = 256 * bdelka[0] + bdelka[1] - 2
            if (delka <= 0):
                print('Chyba: zaporna delka '+delka+' = '+binascii.hexlify(bdelka).decode('ascii'))
                exit()
            blok = stream.read(delka)

          
        while True:
            byte = stream.read(1)
            if (byte == b''):
                print('Chyba: predcasny EOF')
                exit()
            if (byte == b'\xff'):
                tmp = stream.read(1)
                if (tmp == b'\xd9'):
                    print('ffd9 = EOI @ ' + str(stream.tell())+' = '+hex(stream.tell()))
                    break

        if (stream.read() != b''):
            print('Chyba: po EOI by nemelo nic nasledovat')
            
        print('OK: Parse probehl bez chyby')    
            
        
        
        
        
        