import os
import sys
from Crypto.Cipher import AES
import rsa
from colorama import *
from argparse import *
from hashlib import *
from random import *

class Loader:
    def __init__(self):
        self.n = None

    def Load(self, FileName : str) -> bytes:
        try:
            f = open(FileName, 'rb')
            d = f.read()
            f.close()
            if Verbose == True:
                print(Cyan + f'File {FileName} Loaded..' + Reset)
            return d
        except Exception as e:
            print(Red + f'Error Happened in Loader.Load() : {str(e)}')
            sys.exit(0)

    def SaveFile(self, FileName : str, FileData : bytes):
        try:
            f = open(FileName, 'wb')
            f.write(FileData)
            f.close()
            if Verbose == True:
                print(Cyan + f'File {FileName} Saved..' + Reset)
        except Exception as e:
            print(Red + f'Error Happened in Loader.SaveFile() : {str(e)}' + Reset)
            sys.exit(0)

class KeyGenerator:
    def __init__(self):
        self.al : list[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z',
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z',
                    '!', '@', '#', '$', '^', '&', '*', '(', ')',
                    '-', '_', '=', '+', '[', ']', '{', '}', '|', ';',
                    ':', '"', '<', '>', ',', '.', '?', '/', '`', '~']
        self.defMinorKeys : list[str] = ['AG/}<;802|?!', 'WkBMfX&&D*:[', '2u^{=,kCA"~,', '/D@0Ru4J{;^x', 'qp{-_5S2=*b3', '{mdNw+O8C$1v', 
                                         'GRkeg{of*3^N', '8j.@},kF8CK;', 'gKO)}&98K3fv', 'J/ixrCQlevU-', 'MV1Ic+f6#O/]', '8QDv4T.z,N"0', 
                                         'F5/23y_ZR#^)', 'Y@encZ`nQu!`', 'prNzuvo:I~W4', '=6NNl$!uZ_H(', '-^}&{)2VR3PA', 'E3N0xgi~}:TR', 
                                         '.8LAw`Eve0iQ', 'b8p[`2OR3FBH', ':ScEi0m$T-O6', 'olK7$$;lxnOT', 'HJueFp.d350p', ')AR:m{PK!yo_', 
                                         ']]&]9Kfw@S91', 'Ut7n:2#@}^~u', '(*,;sYdqwkDf', '0Us?Q-m7!]b`', '8_8FdZIF}fAB', 'E-asGy/LXo=p']
        self.defMajorKeys : list[str] = ['::?j.w*5G>r&1TAUZ>:u1_1K01;l=)(S', '16"Ki/K5@?kXq(mG6>I$?mK=xQt#RVjm', '/&J|<GTGG_fs8o(Pmq6*mwma>7iGp_G`', 
                                         '"<Jkh}>ITL<>Yid!o9,=h~XvRPEYLe@F', 'lNK)9c<n8eU]+H]dpb84mIYZNpc}dYQi', '~A.BZsKJrRF=j5PCPbw4[4`PvG=Ol(kG', 
                                         '//ElC$C(kZ^kEVY0fIV/Q<e1d6a5g=H[', '8*PY}r.PM;6Y/I$jchdWjD&J*[am)!U@', '=PeEK1dLl#3]U1-S!6.T[eqr=Wj+I9P#', 
                                         'cPPMNC7dW.bWp$va*ZA:v6=ZINsXcH2|', '$wEe7Oc2`iZLa2;-KfC/VH_7=_|Nxir.', ']n-cr]jF|UcvB9i0"4dRa~B3t1f)P;OA', 
                                         'Q58w9e`PFNwniyS@4K^ohSa26Y:]zp$;', 'N]#q7S^N>K"!fh(qa)LZUoXt=>j6a6B2', '#K[UcaZ&c#_vLyw$VdWtG&!U)6L(WtI>', 
                                         'zDrhie)NmK&IeP#djwm{9hHG`zMXRdfZ', '[[f[HkdTlC}4!PHe![9u9F"UC;Lm1CAj', '>C-b+;JaIlaJWHKw,j{}D-lA;G:?GX7V', 
                                         'Q/<($5bxjzJ+BNTMb/b*dvjiw0-DW6VT', '90*K4nAAl;;/hiM=W?0iF><`t7y3WI+2', 'CpMs~]7CJa7}pO{=NQb/HLv1iS+hv/<R', 
                                         'YKBXQibAo9"qH*I8$=JHI[7sh!>;<N][', '@R$tqMKLH+Wv9_ccp&CjDM^Nvx+VI+sR', '"Yv*GAk2R~ocm(`^~54>PQzf;Fz{ZOS}', 
                                         ']p$7p^h)`.lB"zSBem`D}dMdfSEjHjLp', 'ZC#J-OtD9/KBRkKA}-<q0A)TpXZ$Q)h/', 'bd@Uy^[)C$mya0u9"<hZgr0?jzLfv*Y*', 
                                         'og(X>jn2aJ34Va&n+"#8+-Ox:Cu>a8vq', '_[5N!:<sca+2k2XQ?IHtqk"/*Zb@t0WS', 'rF!?)(h2Qn{XWOCq)Y;B8(Bc5y]DVA2_']

    def GenerateRandomMinorKey(self) -> str:
        try:
            k : str = ''
            if Verbose == True:
                print(Cyan + 'Generating Random Minor Key..' + Reset)
            for x in range(12):
                c = choice(self.al)
                k = k+c
                if Verbose == True:
                    print(Magenta + f'Generated : {k}' + Reset)
            vm = self.ValidateMinorKey(k)
            if vm == True:
                return k
        except Exception as e:
            print(Red + f'Error Happened in KeyGenerator.GenerateRandomMinorKey() : {str(e)}' + Reset)
            sys.exit(0)

    def GenerateRandomMajorKey(self) -> str:
        try:
            k : str = ''
            if Verbose == True:
                print(Cyan + 'Generating Random Major Key..' + Reset)
            for x in range(32):
                c = choice(self.al)
                k = k+c
                if Verbose == True:
                    print(Magenta + f'Generated : {k}' + Reset)
            vm = self.ValidateMajorKey(k)
            if vm == True:
                return k
        except Exception as e:
            print(Red + f'Error Happened in KeyGenerator.GenerateRandomMajorKey() : {str(e)}' + Reset)
            sys.exit(0)

    def ValidateMinorKey(self, MinorKey : str) -> bytes:
        try:
            if len(MinorKey) == 12:
                if Verbose == True:
                    print(Cyan + f'Minor Key {MinorKey} Validated..' + Reset)
                return True
            else:
                print(Grey + 'Minor Key Length Must be equal to 12 digits' + Reset)
                return False
        except Exception as e:
            print(Red + f'Error Happened in KeyGenerator.ValidateMinorKey() : {str(e)}' + Reset)
            sys.exit(0)

    def ValidateMajorKey(self, MajorKey : str) -> bool:
        try:
            if len(MajorKey) == 32:
                if Verbose == True:
                    print(Cyan + f'Major Key {MajorKey} Validated..' + Reset)
                return True
            else:
                print(Grey + 'Major Key Length Must be equal to 32 digits' + Reset)
                return False
        except Exception as e:
            print(Red + f'Error Happened in KeyGenerator.ValidateMajorKey() : {str(e)}' + Reset)
            sys.exit(0)

    def GenerateRandomMinorKeyList(self, Count : int) -> list[str]:
        try:
            l : list[str] = []
            if Verbose == True:
                print(Cyan + 'Generating Random Minor Key List' + Reset)
            for x in range(Count):
                k = self.GenerateRandomMinorKey()
                l.append(k)
                if Verbose == True:
                    print(Cyan + f'Minor Key {k} Added To The List' + Reset)
            return l
        except Exception as e:
            print(Red + f'Error Happened in KeyGenerator.GenerateRandomMinorKeyList() : {str(e)}' + Reset)
            sys.exit(0)

    def GenerateRandomMajorKeyList(self, Count : int) -> list[str]:
        try:
            l : list[str] = []
            if Verbose == True:
                print(Cyan + 'Generating Random Major Key List' + Reset)
            for x in range(Count):
                k = self.GenerateRandomMajorKey()
                l.append(k)
                if Verbose == True:
                    print(Cyan + f'Major Key {k} Added To The List' + Reset)
            return l
        except Exception as e:
            print(Red + f'Error Happened in KeyGenerator.GenerateRandomMajorKeyList() : {str(e)}' + Reset)
            sys.exit(0)

class Injector:
    def __init__(self):
        self.l = Loader()
        SplitMsg = str('Spectre').encode('utf-8')
        self.Splitter = md5(SplitMsg).hexdigest().encode('utf-8')
        if Verbose == True:
            print(Cyan + 'Injector Splitter Initialized..' + Reset)

    def Steg(self, Data1 : bytes, Data2 : bytes) -> bytes:
        try:
            nd = Data1 + self.Splitter + Data2
            if Verbose == True:
                print(Cyan + 'Data Injected Using Steg..' + Reset)
            return nd
        except Exception as e:
            print(Red + f'Error Happened in Injector.Steg() : {str(e)}' + Reset)
            sys.exit(0)

    def DeSteg(self, Data : bytes) -> tuple[bytes]:
        try:
            sd : tuple[bytes]= Data.split(self.Splitter)
            if Verbose == True:
                print(Cyan + 'Data Extracted Using DeSteg..' + Reset)
            return sd
        except Exception as e:
            print(Red + f'Error Happened in Injector.DeSteg() : {str(e)}' + Reset)
            sys.exit(0)

    def StegFile(self, StegFileName : str, InjectFileName : str):
        try:
            StegFileData = self.l.Load(StegFileName)
            InjectFileData = self.l.Load(InjectFileName)
            FinalData = self.Steg(StegFileData, InjectFileData)
            NewFileName = StegFileName + '.s'
            self.l.SaveFile(NewFileName, FinalData)
            if Verbose == True:
                print(Cyan + f'File {InjectFileName} Injected into {StegFileName} and Saved as {NewFileName}..' + Reset)
        except Exception as e:
            print(Red + f'Error Happened in Injector.StegFile() : {str(e)}' + Reset)
            sys.exit(0)

    def DeStegFile(self, DeStegFileName : str):
        try:
            StegFileData = self.l.Load(DeStegFileName)
            FileData, StegData = self.DeSteg(StegFileData)
            NewFileName = DeStegFileName.replace('.s', '')
            self.l.SaveFile(NewFileName, FileData)
            self.l.SaveFile('StegData', StegData)
            if Verbose == True:
                print(Cyan + f'File {DeStegFileName} DeStegged and Saved as {NewFileName} and StegData..' + Reset)
        except Exception as e:
            print(Red + f'Error Happened in Injector.DeStegFile() : {str(e)}' + Reset)
            sys.exit(0)

class Encryptor:
    def __init__(self):
        try:
            self.l = Loader()
            self.i = Injector()
            self.kg = KeyGenerator()
            self.defMnk : list[str] = self.kg.defMinorKeys
            self.defMjk : list[str] = self.kg.defMajorKeys
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.__init__() : {str(e)}' + Reset)
            sys.exit(0)

    def ValidateMajorKey(self, MajorKey : str) -> bool:
        try:
            if len(MajorKey) == 32:
                if Verbose == True:
                    print(Cyan + f'Major Key {MajorKey} Validated..' + Reset)
                return True
            else:
                print(Grey + 'Major Key Length Must be equal to 32 digits' + Reset)
                return False
        except Exception as e:
            print(Red + f'Error Happened in KeyGenerator.ValidateMajorKey() : {str(e)}' + Reset)
            sys.exit(0)

    def ValidateMinorKey(self, MinorKey : str) -> bool:
        try:
            if len(MinorKey) == 12:
                if Verbose == True:
                    print(Cyan + f'Minor Key {MinorKey} Validated..' + Reset)
                return True
            else:
                print(Grey + 'Minor Key Length Must be equal to 12 digits' + Reset)
                return False
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.ValidateMinorKey() : {str(e)}' + Reset)
            sys.exit(0)

    def AESEncrypt(self, Data : bytes, MajorKey : str, MinorKey : str) -> tuple[bytes]:
        try:
            mv : bool = True if self.ValidateMinorKey(MinorKey) == True and self.ValidateMajorKey(MajorKey) == True else False
            if mv == True:
                mnk = MinorKey.encode('utf-8')
                mjk = MajorKey.encode('utf-8')
                a = AES.new(key=mjk, mode=AES.MODE_GCM, nonce=mnk)
                cipher, tag = a.encrypt_and_digest(Data)
                if Verbose == True:
                    print(Cyan + 'AES Data Encrypted..' + Reset)
                return (cipher, tag)
            else:
                sys.exit(0)
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.AESEncrypt() : {str(e)}' + Reset)
            sys.exit(0)

    def AESDecrypt(self, Data : bytes, Tag : bytes, MajorKey : str, MinorKey : str) -> bytes:
        try:
            mv : bool = True if self.ValidateMinorKey(MinorKey) == True and self.ValidateMajorKey(MajorKey) == True else False
            if mv == True:
                mnk = MinorKey.encode('utf-8')
                mjk = MajorKey.encode('utf-8')
                a = AES.new(key=mjk, mode=AES.MODE_GCM, nonce=mnk)
                plain = a.decrypt_and_verify(Data, Tag)
                if Verbose == True:
                    print(Cyan + 'AES Data Decrypted..' + Reset)
                return plain
            else:
                sys.exit(0)
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.AESDecrypt() : {str(e)}' + Reset)
            sys.exit(0)

    def DefAESEncrypt(self, Data : bytes) -> tuple[bytes]:
        try:
            mnk : bytes = choice(self.defMnk).encode('utf-8')
            mjk : bytes = choice(self.defMjk).encode('utf-8')
            a = AES.new(key=mjk, mode=AES.MODE_GCM, nonce=mnk)
            CipherData, Tag = a.encrypt_and_digest()
            if Verbose == True:
                print(Green + f'Data Was Encrypted by Defualt Major Key {mjk.decode('utf-8')} and Default Minor Key {mnk.decode('utf-8')}' + Reset)
            return(CipherData, Tag)
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.DefAESEncrypt() : {str(e)}' + Reset)
            sys.exit(0)

    def DefAESDecrypt(self, Data : bytes, Tag : bytes) -> bytes:
        try:
            for x in self.defMjk:
                for y in self.defMnk:
                    try:
                        if Verbose == True:
                            print(Cyan + f'Trying Major Key {x} and Minor Key {y}' + Reset)
                        mnk : bytes = y.encode('utf-8')
                        mjk : bytes = x.encode('utf-8')
                        a = AES.new(key=mjk, mode=AES.MODE_GCM, nonce=mnk)
                        plain = a.decrypt_and_verify(Data, Tag)
                        if Verbose == True:
                            print(Green + 'Data Decrypted Successfully..' + Reset)
                        return plain
                    except Exception as crypt:
                        continue
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.DefAESDecrypt() : {str(e)}' + Reset)
            sys.exit(0)

    def RSAEncrypt(self, Data : bytes) -> bytes:
        try:
            puk = rsa.PublicKey(20297768998920710948566957692911632459181885511139138802377399903332400110486012369702459168570678588699444962080509870646721226080363238185198146221155304361042885813184024656100646116965161860597941527466729184389920596184769813419436181167516470318930468811142872899794424299953624681245365089369955010315852272570863590878860857551636083468886151989555761203969998409795533082736501106809059815676681719298502845770739658665237813750846241844782852292513140511692856701973937847766050564141678259053603277533047191086292210563871495613417280012378032354236409416607540631334161097002870857244462174918458513992419, 
                                65537)
            c = rsa.encrypt(Data, puk)
            if Verbose == True:
                print(Cyan + 'RSA Data Encrypted' + Reset)
            return c
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.RSAEncrypt() : {str(e)}' + Reset)
            sys.exit(0)

    def RSADecrypt(self, Data : bytes) -> bytes:
        try:
            pvk = rsa.PrivateKey(20297768998920710948566957692911632459181885511139138802377399903332400110486012369702459168570678588699444962080509870646721226080363238185198146221155304361042885813184024656100646116965161860597941527466729184389920596184769813419436181167516470318930468811142872899794424299953624681245365089369955010315852272570863590878860857551636083468886151989555761203969998409795533082736501106809059815676681719298502845770739658665237813750846241844782852292513140511692856701973937847766050564141678259053603277533047191086292210563871495613417280012378032354236409416607540631334161097002870857244462174918458513992419, 
                                 65537, 
                                 20162733411641320223120641969669655076143246237402827031654959963178701795821442716023006764623338675907084036138414530554834651251319516747708691535215702110384254838092881717759558155859270370733884544297290639378797026599092110157906447200611711464252139250716574891275414137834824913767837043920131529915028841419334169197421272313278691591178107025967557938652517694738268339400935311125049497766074939217160809541732185186606366426777837728509065803146093277775856466763673229504602864686155932668354991899234454416676577490481577701659336090319814162066744433526472571027843269741641194536998493164307062268881, 
                                 2331397915236034016851563210041123532860570149306846420039927911042796419560865361727275185277497266698788214480254857311709101551194252821723608740692074006933459556769971245555282687424079660941660426908801961406674401341885107720129202587081973086588092762072248723438782083576484216148323984214264144329808000859961167983467, 
                                 8706265398228142515451891283339361981366160308286588887413580587340018961203850182442536481776366649421619081954306833973897036125874368277382846022633529107255869818603070518528681046692283530434941449490538519922259409699807367155467766510965588816783421308323169399634892534262819044457)
            p = rsa.decrypt(Data, pvk)
            if Verbose == True:
                print(Cyan + 'RSA Data Decrypted' + Reset)
            return p
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.RSADecrypt() : {str(e)}' + Reset)
            sys.exit(0)

    def EncryptFile(self, FileName):
        try:
            FileData = self.l.Load(FileName)
            CipherFileData, Tag = self.AESEncrypt(FileData, MajorKey, MinorKey)
            CipherTag = self.RSAEncrypt(Tag)
            FinalData = self.i.Steg(CipherFileData, CipherTag)
            NewFileName = FileName + '.e'
            self.l.SaveFile(NewFileName, FinalData)
            if Verbose == True:
                print(Cyan + f'File {FileName} Encrypted and Saved as {NewFileName}..' + Reset)
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.EncryptFile() : {str(e)}' + Reset)
            sys.exit(0)

    def DecryptFile(self, FileName):
        try:
            Data = self.l.Load(FileName)
            CipherFileData, CipherTag = self.i.DeSteg(Data)
            Tag = self.RSADecrypt(CipherTag)
            FileData = self.AESDecrypt(CipherFileData, Tag, MajorKey, MinorKey)
            NewFileName = FileName.replace('.e', '')
            self.l.SaveFile(NewFileName, FileData)
            if Verbose == True:
                print(Cyan + f'File {FileName} Decrypted and Saved as {NewFileName}..' + Reset)
        except Exception as e:
            print(Red + f'Error Happened in Encryptor.DecryptFile() : {str(e)}' + Reset)
            sys.exit(0)

class PlayGround:
    def __init__(self):
        self.n = None

    def Home(self):
        try:
            print(Cyan + '****************** Silver Cover ******************' + Reset)
            if EncFileName not in [None, 'None', '']:
                if Verbose == True:
                    print(Cyan + f'Encrypted File Name : {EncFileName}' + Reset)
                if MajorKey not in [None, 'None', ''] and MinorKey not in [None, 'None', '']:
                    e = Encryptor()
                    e.EncryptFile(EncFileName)
                else:
                    print(Grey + 'Major Key and Minor Key are required for Encryption..' + Reset)
                    sys.exit(0)
            elif DecFileName not in [None, 'None', '']:
                if Verbose == True:
                    print(Cyan + f'Decrypted File Name : {DecFileName}' + Reset)
                if MajorKey not in [None, 'None', ''] and MinorKey not in [None, 'None', '']:
                    d = Encryptor()
                    d.DecryptFile(DecFileName)
                else:
                    print(Grey + 'Major Key and Minor Key are required for Decryption..' + Reset)
                    sys.exit(0)
            elif StegFileName not in [None, 'None', '']:
                if Verbose == True:
                    print(Cyan + f'Steg File Name : {StegFileName}' + Reset)
                if InjectFileName not in [None, 'None', '']:
                    i = Injector()
                    i.StegFile(StegFileName, InjectFileName)
                else:
                    print(Grey + 'Inject File Name is required for Steg..' + Reset)
                    sys.exit(0)
            elif DeStegFileName not in [None, 'None', '']:
                if Verbose == True:
                    print(Cyan + f'DeSteg File Name : {DeStegFileName}' + Reset)
                i = Injector()
                i.DeStegFile(DeStegFileName)
            elif GenerateMinorKey == True:
                kg = KeyGenerator()
                RandomMinorKey : str = kg.GenerateRandomMinorKey()
                print(Green + f'Generated Minor Key : {RandomMinorKey}' + Reset)
            elif GenerateMajorKey == True:
                kg = KeyGenerator()
                RandomMajorKey : str = kg.GenerateRandomMajorKey()
                print(Green + f'Generated Major Key : {RandomMajorKey}' + Reset)
            elif GenerateMinorKeyList not in [None, 'None', ''] and GenerateMinorKeyList != 0:
                kg = KeyGenerator()
                MinorKeyList : list[str] = kg.GenerateRandomMinorKeyList(GenerateMinorKeyList)
                print(MinorKeyList)
            elif GenerateMajorKeyList not in [None, 'None', ''] and GenerateMinorKeyList != 0:
                kg = KeyGenerator()
                MajorKeyList : list[str] = kg.GenerateRandomMajorKeyList(GenerateMajorKeyList)
                print(MajorKeyList)
            elif EncryptText not in [None, 'None', '']:
                if MinorKey == 'def' and MajorKey == 'def':
                    e = Encryptor()
                    PlainData = EncryptText.encode('utf-8')
                    CipherData, DecryptionTag = e.DefAESEncrypt(PlainData)
                    print(Cyan + f'Cipher Data : {str(CipherData)}' + Reset)
                    print(Green + f'Decryption Tag : {str(DecryptionTag)}' + Reset)
                else:
                    pass
            elif DecryptText not in [None, 'None', ''] and Tagg not in [None, 'None', '']:
                if MinorKey == 'def' and MajorKey == 'def':
                    pass
                else:
                    pass
        except Exception as e:
            print(Red + f'Error Happened in PlayGround.Home() : {str(e)}' + Reset)
            sys.exit(0)

if __name__ == '__main__':

    Red = Fore.RED + Style.BRIGHT
    Green = Fore.GREEN + Style.BRIGHT
    Cyan = Fore.CYAN + Style.BRIGHT
    Grey = Fore.LIGHTBLACK_EX + Style.BRIGHT
    Black = Fore.BLACK + Style.BRIGHT
    Magenta = Fore.MAGENTA + Style.BRIGHT
    Reset = Fore.RESET + Style.RESET_ALL

    p = ArgumentParser()
    p.add_argument('-v', type=str, metavar='Verbose')
    p.add_argument('-e', type=str, metavar='File Name To Be Encrypted')
    p.add_argument('-d', type=str, metavar='File Name To Be Decrypted')
    p.add_argument('-mnk', type=str, metavar='AES Minor Key')
    p.add_argument('-mjk', type=str, metavar='AES Major Key')
    p.add_argument('-s', type=str, metavar='File Name Used For Steg')
    p.add_argument('-f', type=str, metavar='File Name Injected Into Steg')
    p.add_argument('-ds', type=str, metavar='File Name Used For DeSteg')
    p.add_argument('-gmnk', type=str, metavar='Generate Random Minor Key')
    p.add_argument('-gmjk', type=str, metavar='Generate Random Major Key')
    p.add_argument('-gmnkl', type=int, metavar='Generate Random Minor Key List')
    p.add_argument('-gmjkl', type=int, metavar='Generate Random Major Key List')
    p.add_argument('-et', type=str, metavar='Encrypt Plain Text To Cipher Data')
    p.add_argument('-dt', type=str, metavar='Decrypt Cipher Data To Plain Text')
    p.add_argument('-tag', type=str, metavar='Tag for Decryption')
    a = p.parse_args()

    EncFileName = str(a.e)
    DecFileName = str(a.d)
    MinorKey = str(a.mnk)
    MajorKey = str(a.mjk)
    StegFileName = str(a.s)
    InjectFileName = str(a.f)
    DeStegFileName = str(a.ds)
    GenerateMinorKeyList : int = a.gmnkl
    GenerateMajorKeyList : int = a.gmjkl
    EncryptText = str(a.et)
    DecryptText = str(a.dt)
    Tagg = str(a.tag)

    Verbose : bool = True if str(a.v) in ['y', 'Y', 'yes', 'Yes', 'True', 'true'] and str(a.v) != None else False
    GenerateMinorKey : bool = True if str(a.gmnk) in ['y', 'Y', 'yes', 'Yes', 'True', 'true'] and str(a.gmnk) != None else False
    GenerateMajorKey : bool = True if str(a.gmjk) in ['y', 'Y', 'yes', 'Yes', 'True', 'true'] and str(a.gmjk) != None else False

    pg = PlayGround()
    pg.Home()
