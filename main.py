from expenses import (
    add_expense,
    calculate_category_total,
    calculate_total,
    show_expenses,
    get_by_category,
    delete_expense,
    update_expense,
    get_valid_amount,
    get_valid_choice

)

from storage import save_expenses, load_expenses


expenses = load_expenses()


while True:

    print("\n1. Harcama ekle")
    print("2. Toplam harcama")
    print("3. Harcamaları göster")
    print("4. Kategoriye göre göster")
    print("5. Çıkış")
    print("6. Kategori toplamı")
    print("7. Harcama sil")
    print("8. Harcama güncelle")

    seçim = get_valid_choice()

    if seçim == 1:

        name = input("Harcama adı: ")
        amount = get_valid_amount()      
        category = input("Harcama kategorisi: ")

        add_expense(expenses, name, amount, category)
        save_expenses(expenses)


    elif seçim == 2:

        total = calculate_total(expenses)
        print(f"Toplam harcama: {total} TL")


    elif seçim == 3:

        show_expenses(expenses)


    elif seçim == 4:

        category = input("Kategori adı: ")

        filtered_expenses = get_by_category(expenses, category)

        show_expenses(filtered_expenses)


    elif seçim == 5:

        print("Program sonlandırılıyor.")
        break

    elif seçim == 6:
       category = input("Kategori adı: ")
       total = calculate_category_total(expenses, category)
       print(f"{category} kategorisinin toplamı: {total} TL")

    elif seçim == 7:
        name = input("Silinecek harcama adı: ")
        category = input("Silinecek harcama kategorisi: ")

        deleted = delete_expense(expenses, name, category)

        if deleted:
            save_expenses(expenses)
            print("Harcama silindi.")
        else:
            print("Harcama bulunamadı.")


    elif seçim == 8:
        name = input("Harcama adı:")
        category = input("Kategori:")
        new_amount = int(input("Yeni tutar:"))

        updated = update_expense(expenses, name, category, new_amount)

        if updated:
            save_expenses(expenses)
            print("Harcama güncellendi.")

        else :
            print("Harcama bulunamadı.")





    else:

      print("Lütfen 1-8 arasında bir seçim yapın.")







        
        