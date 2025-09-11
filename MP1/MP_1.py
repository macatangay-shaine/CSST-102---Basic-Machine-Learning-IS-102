"""
Enhanced Mini Expert System: University Logic Rules
With CSV Row Updates per Student
"""

import csv
import os
from datetime import datetime

FILENAME = "logic_results.csv"

# ----------------- Logic Functions ----------------- #
def impl(P, Q):
    return (not P) or Q  # Implication (P -> Q)

def tf(b: bool) -> str:
    return "T" if b else "F"

# ----------------- CSV Helpers ----------------- #
def init_csv():
    headers = [
        "timestamp", "student",
        "AttendanceRule", "AttendanceDetail",
        "GradingRule", "GradingDetail",
        "LoginSystemRule", "LoginDetail",
        "BonusPointsRule", "BonusDetail",
        "LibraryBorrowingRule", "LibraryDetail"
    ]
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def load_all_records():
    records = []
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                records.append(row)
    return records

def save_all_records(records):
    if not records:
        return
    headers = records[0].keys()
    with open(FILENAME, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(records)

def update_student_record(student, updates):
    records = load_all_records()
    found = False
    for row in records:
        if row["student"] == student:
            row.update(updates)
            row["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            found = True
            break

    if not found:  # new student entry
        new_row = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "student": student,
            "AttendanceRule": "", "AttendanceDetail": "",
            "GradingRule": "", "GradingDetail": "",
            "LoginSystemRule": "", "LoginDetail": "",
            "BonusPointsRule": "", "BonusDetail": "",
            "LibraryBorrowingRule": "", "LibraryDetail": ""
        }
        new_row.update(updates)
        records.append(new_row)

    save_all_records(records)

# ----------------- Rule Checkers ----------------- #
def attendance_rule(student):
    print("\n--- Attendance Rule Checker ---")
    late = input("Is the student late? (T/F): ").strip().upper() == "T"
    excuse = input("Did the student bring an excuse letter (T/F): ").strip().upper() == "T"

    result = impl(late, excuse)
    outcome = result
    detail = f"attendance={82.5 if not late else 70.0} -> {'eligible' if result else 'not eligible'}"

    print("Result:", "Eligible" if result else "Not Eligible")
    update_student_record(student, {
        "AttendanceRule": str(outcome),
        "AttendanceDetail": detail
    })

def grading_rule(student):
    print("\n--- Grading Rule Checker ---")
    try:
        grade = float(input("Enter Student Grade: "))
    except ValueError:
        print("Invalid Grade Input")
        return
    
    passed = grade >= 75
    detail = f"grade={grade} -> {'pass' if passed else 'fail'}"

    print("Result:", "Pass" if passed else "Fail")
    update_student_record(student, {
        "GradingRule": str(passed),
        "GradingDetail": detail
    })

def login_rule(student):
    print("\n--- Login System Checker ---")
    correct_password = "admin123"
    attempt = input("Enter Password: ")

    user_ok = attempt == correct_password
    pass_ok = user_ok
    locked = not user_ok
    success = user_ok and pass_ok and not locked

    detail = f"user_ok={user_ok}, pass_ok={pass_ok}, locked={locked} -> {'login success' if success else 'login denied'}"
    print("Result:", "Login Success" if success else "Login Denied")

    update_student_record(student, {
        "LoginSystemRule": str(success),
        "LoginDetail": detail
    })

def bonus_rule(student):
    print("\n--- Bonus Points Checker ---")
    participated = input("Did the student participate? (T/F): ").strip().upper() == "T"
    base = float(input("Enter base grade: "))
    bonus = 5.0 if participated else 0.0
    final = base + bonus

    detail = f"participated={participated}, base={base} -> bonus {bonus}, final={final}"
    print("Result: Final grade =", final)

    update_student_record(student, {
        "BonusPointsRule": str(participated),
        "BonusDetail": detail
    })

def library_rule(student):
    print("\n--- Library Borrowing Checker ---")
    valid_id = input("Does the student have a valid ID? (T/F): ").strip().upper() == "T"
    overdue = input("Does the student have overdue books? (T/F): ").strip().upper() == "T"

    allowed = valid_id and not overdue
    detail = f"id_valid={valid_id}, overdue={overdue} -> {'can borrow' if allowed else 'cannot borrow'}"
    print("Result:", "Allowed to Borrow" if allowed else "Borrowing Denied")

    update_student_record(student, {
        "LibraryBorrowingRule": str(allowed),
        "LibraryDetail": detail
    })

# ----------------- View Records ----------------- #
def view_records():
    student_name = input("Enter the student name to view records: ").strip().title()
    records = load_all_records()
    found = False
    for row in records:
        if row["student"] == student_name:
            found = True
            print(f"\n=== Record for {student_name} ===")
            for key, value in row.items():
                if key not in ["timestamp", "student"] and value:
                    print(f"{key}: {value}")
    if not found:
        print(f"No records found for {student_name}.")

# ----------------- Main Menu ----------------- #
def main():
    print("=== University Logic Rule System ===")
    student_name = input("Enter Student Name: ").strip().title()

    while True:
        print("\n==============================")
        print("          Main Menu")
        print("==============================")
        print("1) Attendance Rule Checker")
        print("2) Grading Rule Checker")
        print("3) Login System Rule Checker")
        print("4) Bonus Points Checker")
        print("5) Library Borrowing Checker")
        print("6) View Student Records")
        print("7) Exit")

        choice = input("Choose an Option: ").strip()

        match choice:
            case "1": attendance_rule(student_name)
            case "2": grading_rule(student_name)
            case "3": login_rule(student_name)
            case "4": bonus_rule(student_name)
            case "5": library_rule(student_name)
            case "6": view_records()
            case "7":
                print("Exiting... Results saved to logic_results.csv")
                break
            case _: print("Unknown Choice")

if __name__ == "__main__":
    init_csv()
    main()

