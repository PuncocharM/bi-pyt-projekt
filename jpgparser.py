import io
import binascii


class Marker:
    '''
    Trida reprezentuje objekty markeru v jpeg souboru
    Obsahuje atributy head, length, data
    Vsechny tyto atributy jsou typu bytestring
        head je dvojbytovy a prvni byte by mel byt 0xff
        length je take dvojbytovy a reprezentuje delku dat + 2 v bytech
        data jsou samotna data markeru
    '''
    def __init__(self, head, length, data):
        '''
        Konstruktor prebira 3 parametry: head, length, data s tim, ze length muze byt None. V tom pripade se automaticky dopocita.
        '''
        self.head = head
        if length == None:
            delka = len(data)+2
            if (delka//256 > 255):
                print('Chyba: data markeru jsou prilis velka')
                return None
            bdelka1 = bytes([delka//256, delka%256])
            bdelka = (2-len(bdelka1)) * b'\x00' + bdelka1
            self.length = bdelka
        else:
            self.length = length
        self.data = data
    def toBytes(self):
        '''
        Vrati bytovy retezec pouzitelny do zapisu do JPEG souboru
        '''
        return self.head+self.length+self.data

        
class JpegStructure:
    '''
    Trida slouzi k naparsovani JPEG souboru. Overi jeho spravnou strukturu a rozebere ho na markery a na obrazova data.
    '''
    def __init__(self):
        self.markers = []
        self.imagestream = b''
    def addMarker(self,marker):
        '''Prida vlastni marker. Priklad pouziti js.addMarker(Marker(head, None, data))'''
        self.markers.append(marker)
    def getMarkers(self, head):
        '''Vrati seznam vsech markeru.'''
        r = []
        for marker in self.markers:
            if marker.head == head:
                r.append(marker)
        return r
    def setImageStream(self,imgstream):
        '''Nastavi obrazova data'''
        self.imagestream=imgstream
    def writeToFile(self, filename):
        '''Zapise reprezentovany JPEG soubor.'''
        try:
            with open(filename, 'wb') as f:
                f.write(b'\xff\xd8')
                for marker in self.markers:
                    f.write(marker.toBytes())
                f.write(b'\xff\xda')
                f.write(self.imagestream)
                f.write(b'\xff\xd9')
            print('Zapsano do souboru '+filename)
        except:
            print('Chyba: Nepodarilo se zapsat soubor '+filename+'.')

    # @staticmethod
    # def fromBytes(bts):
        # bio = io.BytesIO(bts)
        # return fromStream(bts)
    
    @staticmethod
    def fromFile(fileName):
        '''Staticka metoda. Vrati vytvorenou JpegStructure ze souboru nebo None pri chybe.'''
        try:
            with open(fileName, 'rb') as f:
                return JpegStructure.fromStream(f)
        except:
            print('Chyba: Nepodarilo se nacist soubor '+fileName+'.')
            return None
    
    @staticmethod
    def fromStream(stream):
        '''Staticka metoda. Vrati vytvorenou JpegStructure ze streamu nebo None pri chybe. Priklady streamu: bytestream, filestream.'''
        js = JpegStructure()
        if (stream.read(2) != b'\xff\xd8'):
            print('Chyba: nejedna se o JPEG soubor')
            return None

        #cyklus pres jednotlive markery
        while True:
            bts = stream.read(2)
            if (bts == b''):
                print('Chyba: predcasny konec souboru (EOF)')
                return None
            # print('Marker ' + binascii.hexlify(bts).decode('ascii') + ' @ ' + str(stream.tell())+' = '+hex(stream.tell()))
            if (bts[0] != 0xff):
                print('Chyba: Zacatek markeru se nerovna FF, ale ' + hex(bts[0]) + '. Pravdepodobne je chybna delka predchoziho markeru.')
                return None
            if (bts == b'\xff\xd9'):
                print('Chyba: Predcasny marker EOI (FF D9)')
                return None
            if (bts == b'\xff\xda'): # zacatek obrazovych dat, konec markeru
                # print('ffda = SOS')
                break
            bdelka = stream.read(2)
            delka = 256 * bdelka[0] + bdelka[1] - 2
            if (delka <= 0):
                print('Chyba: zaporna delka '+delka+' = '+binascii.hexlify(bdelka).decode('ascii'))
                return None
            data = stream.read(delka)
            js.addMarker(Marker(bts, bdelka, data))
            
        # nacteni obrazovych dat byt po bytu
        imagestream = bytearray()
        while True:
            byte = stream.read(1)
            imagestream.append(byte[0])
            if (byte == b''):
                print('Chyba: predcasny konec souboru (EOF)')
                return None
            if (byte == b'\xff'):
                tmp = stream.read(1)
                imagestream.append(tmp[0])
                if (tmp == b'\xd9'): # FF D9 znaci EOI = konec streamu
                    # print('ffd9 = EOI @ ' + str(stream.tell())+' = '+hex(stream.tell()))
                    break
        
        imagestream.pop() # odstrani znacku EOI
        imagestream.pop()
        js.setImageStream(imagestream)

        if (stream.read() != b''):
            print('Chyba: po EOI by nemelo nic nasledovat')
            
        # print('OK: Parse probehl bez chyby')    
        return js
            
        
        
        
        
        