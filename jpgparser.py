import io
import binascii
from PIL import Image


class Marker:
    def __init__(self, head, length, data):
        self.head = head
        if length == None:
            delka = len(data)+2
            bdelka1 = bytes([delka])
            bdelka = (2-len(bdelka1)) * b'\x00' + bdelka1
            self.length = bdelka
        else:
            self.length = length
        self.data = data
    def toBytes(self):
        return self.head+self.length+self.data

        
class JpegStructure:
    def __init__(self):
        self.markers = []
        self.imagestream = b''
    def addMarker(self,marker):
        self.markers.append(marker)
    def getMarkers(self, head):
        r = []
        for marker in self.markers:
            if marker.head == head:
                r.append(marker)
        return r
    def setImageStream(self,imgstream):
        self.imagestream=imgstream
    def writeToFile(self, filename):
        with open(filename, 'wb') as f:
            f.write(b'\xff\xd8')
            for marker in self.markers:
                f.write(marker.toBytes())
            f.write(b'\xff\xda')
            f.write(self.imagestream)
            f.write(b'\xff\xd9')
        print('Zapsano do souboru '+filename)

    @staticmethod
    def fromBytes(bts):
        bio = io.BytesIO(bts)
        return fromStream(bts)
    
    @staticmethod
    def fromFile(fileName):
        with open(fileName, 'rb') as f:
            return JpegStructure.fromStream(f)
    
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
            # print('Marker ' + binascii.hexlify(bts).decode('ascii') + ' @ ' + str(stream.tell())+' = '+hex(stream.tell()))
            if (bts[0] != 0xff):
                print('Chyba: Zacatek markeru se nerovna FF, ale ' + hex(bts[0]))
                exit()
            if (bts == b'\xff\xd9'):
                print('Chyba: Predcasny marker EOI: FF D9')
                exit()
            if (bts == b'\xff\xda'):
                # print('ffda = SOS')
                break
            bdelka = stream.read(2)
            delka = 256 * bdelka[0] + bdelka[1] - 2
            if (delka <= 0):
                print('Chyba: zaporna delka '+delka+' = '+binascii.hexlify(bdelka).decode('ascii'))
                exit()
            blok = stream.read(delka)
            marker = Marker(bts, bdelka, blok)
            js.addMarker(marker)
            
        imagestream = bytearray()
        while True:
            byte = stream.read(1)
            imagestream.append(byte[0])
            if (byte == b''):
                print('Chyba: predcasny EOF')
                exit()
            if (byte == b'\xff'):
                tmp = stream.read(1)
                imagestream.append(tmp[0])
                if (tmp == b'\xd9'):
                    # print('ffd9 = EOI @ ' + str(stream.tell())+' = '+hex(stream.tell()))
                    break
        
        imagestream.pop()
        imagestream.pop()
        js.setImageStream(imagestream)

        if (stream.read() != b''):
            print('Chyba: po EOI by nemelo nic nasledovat')
            
        # print('OK: Parse probehl bez chyby')    
        return js
            
        
        
        
        
        