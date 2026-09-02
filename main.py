from expense_tracker_oop import ExpenseTracker
from input_utils import get_valid_amount, get_valid_choice


tracker = ExpenseTracker()


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

      tracker.add_expense(name, amount, category)
      tracker.save()

      print("Harcama eklendi.")

    elif seçim == 2:

      total = tracker.calculate_total()
      print(f"Toplam harcama: {total} TL")

    elif seçim == 3:

        tracker.show_expenses()

    elif seçim == 4:

        category = input("Kategori adı: ")

        filtered_expenses = tracker.get_by_category(category)

        if not filtered_expenses:
            print("Bu kategoride harcama bulunamadı.")
        else:
            for expense in filtered_expenses:
                print(
                  f"Name: {expense.name}, "
                  f"Category: {expense.category}, "
                  f"Amount: {expense.amount}"
                )

    elif seçim == 5:

        print("Program sonlandırılıyor.")
        break

    elif seçim == 6:

        category = input("Kategori adı: ")

        total = tracker.calculate_category_total(category)

        print(f"{category} kategorisinin toplamı: {total} TL")

    elif seçim == 7:

        name = input("Silinecek harcama adı: ")
        category = input("Silinecek harcama kategorisi: ")

        deleted = tracker.delete_expense(name, category)

        if deleted:
          tracker.save()
          print("Harcama silindi.")
        else:
          print("Harcama bulunamadı.")

    elif seçim == 8:

        name = input("Harcama adı: ")
        category = input("Kategori: ")
        new_amount = get_valid_amount()

        updated = tracker.update_expense(name, category, new_amount)

        if updated:
            tracker.save()
            print("Harcama güncellendi.")
        else:
            print("Harcama bulunamadı.")









        
        