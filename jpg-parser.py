import sys
import binascii

if (len(sys.argv) < 2):
    print('Pouziti:')
    print('    skript.py <nazev souboru>')
    exit()
f = open(sys.argv[1], 'rb')
if (f.read(2) != b'\xff\xd8'):
    print('neni JPEG soubor!!')
else:
    print('OK, jedna se o JPEG soubor')
while True: #jednotlive markery
    bytes = f.read(2)
    if (bytes == b''):
        print('Chyba: predcasny EOF')
        exit()
    print('Marker ' + binascii.hexlify(bytes).decode('ascii') + ' @ ' + str(f.tell())+' = '+hex(f.tell()))
    if (bytes == b'\xff\xd9'):
        print('Chyba: Predcasny marker EOI: FF D9')
        exit()
    if (bytes == b'\xff\xda'):
        print('SOS')
        break
    if (bytes[0] != 0xff):
        print('Chyba: Zacatek markeru se nerovna FF, ale ' + hex(bytes[0]))
        exit()
    bdelka = f.read(2)
    delka = 256 * bdelka[0] + bdelka[1] - 2
    if (delka <= 0):
        print('Chyba: zaporna delka '+delka+' = '+binascii.hexlify(bdelka).decode('ascii'))
        exit()
    f.read(delka)
    
while True:
    byte = f.read(1)
    if (byte == b''):
        print('Chyba: predcasny EOF')
        exit()
    if (byte == b'\xff' and f.read(1) == b'\xd9'):
        print('EOI')
        break

if (f.read() != b''):
    print('Chyba: po EOI by nemelo nic nasledovat')
    
print('OK: Parse probehl bez chyby')    

    