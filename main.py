from expenses import (
    add_expense,
    calculate_total,
    show_expenses,
    get_by_category
)

from storage import save_expenses, load_expenses


expenses = load_expenses()


while True:

    print("\n1. Harcama ekle")
    print("2. Toplam harcama")
    print("3. Harcamaları göster")
    print("4. Kategoriye göre göster")
    print("5. Çıkış")

    seçim = input("Seçiminizi yapın (1-5): ")


    if seçim == "1":

        name = input("Harcama adı: ")

        while True:
            try:
                amount = int(input("Harcama miktarı: "))

                if amount <= 0:
                    print("Tutar 0'dan büyük olmalı.")
                    continue

                break

            except ValueError:
                print("Geçerli bir sayı girin.")

        category = input("Harcama kategorisi: ")

        add_expense(expenses, name, amount, category)
        save_expenses(expenses)


    elif seçim == "2":

        total = calculate_total(expenses)
        print(f"Toplam harcama: {total} TL")


    elif seçim == "3":

        show_expenses(expenses)


    elif seçim == "4":

        category = input("Kategori adı: ")

        filtered_expenses = get_by_category(expenses, category)

        show_expenses(filtered_expenses)


    elif seçim == "5":

        print("Program sonlandırılıyor.")
        break


    else:

        print("Lütfen 1-5 arasında bir seçim yapın.")




        
        