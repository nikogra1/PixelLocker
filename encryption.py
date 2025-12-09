from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import sys

class Encryption():
    def __init__(self) -> None:
        pass
    def encrypt(self,dane,PIN:str):
            
        haslo_bajty = PIN.encode("UTF-32")
    
        """Wyprowadza klucz AES o długości 32 bajtów z hasła użytkownika i soli za pomocą PBKDF2HMAC."""
            
        # 480 000 iteracji to obecnie standard bezpieczeństwa (NIST)
        iteracje = 480000 

        sol = os.urandom(32)
            
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), 
            length=32, 
            salt=sol, 
            iterations=iteracje,
            )
        klucz = kdf.derive(haslo_bajty)

        aesgcm = AESGCM(klucz)

        nonce = os.urandom(12)

        dane = dane.encode("UTF-32")

        szyfrogram_z_tagiem = aesgcm.encrypt(nonce, dane, associated_data=None)

        return sol+nonce + szyfrogram_z_tagiem

    def decrypt(self,klucz: str,zaszyfrowane: bytes):
        SOL_ROZMIAR = 32
        haslo_bajty = klucz.encode('utf-32')
        sol = zaszyfrowane[:SOL_ROZMIAR] # Wydzielenie soli (16 bajtów)
        szyfrogram_bez_soli = zaszyfrowane[SOL_ROZMIAR:]
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(), 
            length=32, 
            salt=sol, 
            iterations=480000,
        )
        # Krok 2: Wyprowadzenie Klucza
        klucz_aes = kdf.derive(haslo_bajty)

        nonce = szyfrogram_bez_soli[:12]
        szyfrogram_z_tagiem = szyfrogram_bez_soli[12:]

        # Poprawka 2: Użycie poprawnej nazwy zmiennej (klucz_aes)
        aesgcm = AESGCM(klucz_aes) 
        
        try:
            dane_jawne = aesgcm.decrypt(nonce, szyfrogram_z_tagiem, associated_data=None)
            return dane_jawne
        except Exception as e:
            # Błąd występuje, jeśli klucz jest nieprawidłowy lub dane zostały zmienione (InvalidTag)
            raise ValueError("Nieprawidłowy klucz lub dane zostały naruszone.") from e
