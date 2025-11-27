import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",      
        database="library_db"
    )

# ---------------------- MAIN MENU ----------------------
def main():
    while True:
        print("""************** SWAMI VIVEKANAND SCHOOL CHIRKUNDA **********************
************* ===== LIBRARY MANAGEMENT SYSTEM ===== *************
******* Designed and Maintained By: *************
MD FAISAL ANSARI - CLASS XII SCI - ROLL NO -34   [2025-26 ] 

Menu :
""")
        
        print("press 1 to Add Books")
        print("press 2 to Show All Books")
        print("press 3 to Find Book")
        print("press 4 to Rent Book")
        print("press 5 to Return Book")
        print("press 6 to Show Available Books")
        print("press 7 to Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_book()
        elif choice == "2":
            show_all_books()
        elif choice == "3":
            find_book()
        elif choice == "4":
            rent_book()
        elif choice == "5":
            return_book()
        elif choice == "6":
            show_available_books()
        elif choice == "7":
            print("Thanks for using the Library Management System!")
            break
        else:
            print("Invalid choice! Try again.\n")

def add_book():
    db = connect_db()
    cursor = db.cursor()

    name = input("Enter Book Name: ")
    quantity = int(input("Enter Quantity: "))
    shelf_no = input("Enter Shelf Number: ")
    language = input("Enter Language: ")
    rent_fee = int(input("Enter Rent Fee: "))

    cursor.execute("""
        INSERT INTO books (name, quantity, shelf_no, language, rent_fee)
        VALUES (%s, %s, %s, %s, %s)
    """, (name, quantity, shelf_no, language, rent_fee))

    db.commit()
    print("Book added successfully!\n")

def show_all_books():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, quantity, shelf_no, rent_fee FROM books")
    data = cursor.fetchall()

    print("\n----- ALL BOOKS -----")
    for row in data:
        print(f"Name: {row[0]} | Quantity: {row[1]} | Shelf: {row[2]} | Rent Fee: {row[3]}")
    print()

def find_book():
    db = connect_db()
    cursor = db.cursor()
    name = input("Enter book name to search: ")

    cursor.execute("SELECT name, quantity, shelf_no, language, rent_fee FROM books WHERE name=%s", (name,))
    book = cursor.fetchone()

    if book:
        print("\nBook Found:")
        print(f"Name: {book[0]}")
        print(f"Quantity: {book[1]}")
        print(f"Shelf Number: {book[2]}")
        print(f"Language: {book[3]}")
        print(f"Rent Fee: {book[4]}\n")
    else:
        print("Book not found!\n")

def rent_book():
    db = connect_db()
    cursor = db.cursor()

    name = input("Enter book name to rent: ")

    cursor.execute("SELECT quantity, rent_fee FROM books WHERE name=%s", (name,))
    result = cursor.fetchone()

    if not result:
        print("Book does not exist!\n")
        return

    quantity, rent_fee = result

    if quantity > 0:
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE name=%s", (name,))
        db.commit()
        print("Book rented successfully!\n")

        # --------- Customer Details ---------
        print("Enter Customer Details:")
        customer_name = input("Customer Name: ")
        phone = input("Phone Number: ")
        address = input("Address: ")
        rent_date = input("Date of Rent (YYYY-MM-DD): ")
        days_rented = int(input("Days Rented: "))

        total_cost = days_rented * rent_fee

        cursor.execute("""
            INSERT INTO customer_detail
            (customer_name, phone, address, book_name, rent_date, days_rented, rent_fee, total_cost)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (customer_name, phone, address, name, rent_date, days_rented, rent_fee, total_cost))

        db.commit()

        print(f"Customer record saved! Total cost to pay: ₹{total_cost}\n")

    else:
        print("Book is not available right now!\n")

def return_book():
    db = connect_db()
    cursor = db.cursor()

    name = input("Enter book name to return: ")

    cursor.execute("SELECT * FROM books WHERE name=%s", (name,))
    result = cursor.fetchone()

    if not result:
        print("This book does not exist in database!\n")
        return

    cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE name=%s", (name,))
    db.commit()
    print("Book returned successfully!\n")

def show_available_books():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT name, shelf_no, language, rent_fee FROM books WHERE quantity > 0")
    data = cursor.fetchall()

    print("\n----- AVAILABLE BOOKS -----")
    for row in data:
        print(f"Name: {row[0]} | Shelf: {row[1]} | Language: {row[2]} | Rent Fee: {row[3]}")
    print()

main()
