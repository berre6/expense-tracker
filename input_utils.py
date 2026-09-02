
def get_valid_amount():
    while True:
        try:
            amount = int(input("Harcama miktarını giriniz: "))

            if amount <= 0:
                print("0'dan büyük bir sayı giriniz.")
                continue

            return amount

        except ValueError:
            print("Geçerli bir sayı giriniz.")


def get_valid_choice():
    while True:
        try:
            seçim = int(input("Seçiminizi yapın (1-8): "))

            if seçim < 1 or seçim > 8:
                print("1 ile 8 arasında bir seçim yapın.")
                continue

            return seçim

        except ValueError:
            print("Lütfen geçerli bir sayı girin.")




    