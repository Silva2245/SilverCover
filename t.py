import os
import sys
from random import *
from colorama import *

class KeyGenerator:
    def __init__(self):
        self.al = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                    'u', 'v', 'w', 'x', 'y', 'z',
                    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                    'U', 'V', 'W', 'X', 'Y', 'Z',
                    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                    '-', '_', '=', '+', '[', ']', '{', '}', '|', ';',
                    ':', '"', "'", '<', '>', ',', '.', '?', '/', '`', '~']

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

if __name__ == '__main__':

    Verbose : bool = True
    Red = Fore.RED + Style.BRIGHT
    Green = Fore.GREEN + Style.BRIGHT
    Cyan = Fore.CYAN + Style.BRIGHT
    Grey = Fore.LIGHTBLACK_EX + Style.BRIGHT
    Black = Fore.BLACK + Style.BRIGHT
    Magenta = Fore.MAGENTA + Style.BRIGHT
    Reset = Fore.RESET + Style.RESET_ALL

    kg = KeyGenerator()
    k = kg.GenerateRandomMinorKey()