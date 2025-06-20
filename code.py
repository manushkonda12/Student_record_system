import sqlite3

conn = sqlite3.connect("students.db")  # Connect to SQLite database
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    roll_no TEXT UNIQUE NOT NULL,
    branch TEXT,
    cgpa REAL
)                                       
''')
conn.commit()                  # Created table


def add_student():                    # Functions
    name = input("Enter name: ")
    roll_no = input("Enter roll no: ")
    branch = input("Enter branch: ")
    cgpa = float(input("Enter CGPA: "))
    try:
        cursor.execute("INSERT INTO students (name, roll_no, branch, cgpa) VALUES (?, ?, ?, ?)",
                       (name, roll_no, branch, cgpa))
        conn.commit()
        print("Student added.")
    except sqlite3.IntegrityError:
        print("Roll number must be unique.")

def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def search_student():
    roll_no = input("Enter roll no to search: ")
    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
    row = cursor.fetchone()
    print(row if row else "Not found.")

def update_student():
    roll_no = input("Enter roll no to update: ")
    cursor.execute("SELECT * FROM students WHERE roll_no=?", (roll_no,))
    record = cursor.fetchone()
    if record:
        name = input(f"New name [{record[1]}]: ") or record[1]
        branch = input(f"New branch [{record[3]}]: ") or record[3]
        cgpa = input(f"New CGPA [{record[4]}]: ") or record[4]
        cursor.execute("UPDATE students SET name=?, branch=?, cgpa=? WHERE roll_no=?",
                       (name, branch, float(cgpa), roll_no))
        conn.commit()
        print("Updated.")
    else:
        print("Student not found.")

def delete_student():
    roll_no = input("Enter roll no to delete: ")
    cursor.execute("DELETE FROM students WHERE roll_no=?", (roll_no,))
    conn.commit()
    print("Deleted." if cursor.rowcount else "Not found.")


def main():
    while True:
        print("\n1. Add\n2. View\n3. Search\n4. Update\n5. Delete\n6. Exit")
        choice = input("Choice: ")
        if choice == '1': add_student()
        elif choice == '2': view_students()
        elif choice == '3': search_student()
        elif choice == '4': update_student()
        elif choice == '5': delete_student()
        elif choice == '6': break
        else: print("Invalid choice.")

main()
conn.close()

