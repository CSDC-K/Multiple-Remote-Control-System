import argparse
import os

def main():
    # Argümanları tanımla
    parser = argparse.ArgumentParser(description="Hata Durumunda Pencerenin Kapatılması içindir.")
    parser.add_argument('-t', type=str, help='Şifreleme Kodu')

    args = parser.parse_args()
    if args.t == "USIA72781SVAXQQQ__$FHBD":
        print("UNLOCKING...")
        os.system("taskkill /f /im taskLOCK.exe")

if __name__ == "__main__":
    main()
