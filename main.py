






# main.py — Master Orchestrator Al-Haqq Protocol TCG (Diperbarui v1.8)
import os
import sys

def print_banner():
    print("==================================================")
    print("       AL-HAQQ PROTOCOL TCG — COMMAND HUB         ")
    print("  Integritas Al-Haqq Framework & Karsa Kolektif   ")
    print("==================================================")

def show_menu():
    print("\nPilih opsi eksekusi sistem:")
    print("1. Jalankan Unit Test Suite Kartu & Rules (test_al_haqq.py)")
    print("2. Jalankan Unit Test Suite Phygital Verifier (test_phygital.py)")
    print("3. Generate Lembar Cetak Kartu & Agents (HTML)")
    print("4. Generate Payload Kriptografis Phygital (JSON)")
    print("5. Generate Buku Panduan Resmi (Rulebook)")
    print("6. Jalankan Streamlit Command Hub Dashboard")
    print("0. Keluar")

def main():
    print_banner()
    while True:
        show_menu()
        choice = input("\nMasukkan pilihan [0-6]: ").strip()
        
        if choice == "1":
            print("\n[+] Menjalankan Unit Test Suite Kartu & Rules...")
            os.system("python -m unittest test_al_haqq.py")
        elif choice == "2":
            print("\n[+] Menjalankan Unit Test Suite Phygital...")
            os.system("python -m unittest test_phygital.py")
        elif choice == "3":
            print("\n[+] Membuat Lembar Cetak Kartu & Agents...")
            os.system("python agent_sheet_generator.py")
        elif choice == "4":
            print("\n[+] Men-generate Payload Kriptografis Phygital...")
            os.system("python phygital_payload_generator.py")
        elif choice == "5":
            print("\n[+] Menyusun Buku Panduan Resmi...")
            os.system("python rulebook_generator.py")
        elif choice == "6":
            print("\n[+] Meluncurkan Streamlit Dashboard...")
            os.system("streamlit run al_haqq_dashboard.py")
        elif choice == "0":
            print("\nKeluar dari sistem. Salam Mizan & Kolaborasi!")
            sys.exit(0)
        else:
            print("\nPilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()


