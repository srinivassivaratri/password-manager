# main.py
import vault
import time


def main():
    print("Welcome to the Password Manager")

    vault_data = None
    key = None
    last_action_time = time.time()
    TIMEOUT = 300  # 5 minutes

    while True:
        if vault_data and (time.time() - last_action_time > TIMEOUT):
            print("Session timed out. Please sign in again.")
            vault_data = None
            key = None

        print("\nMenu:")
        print("1. Create Vault")
        print("2. Sign In")
        print("3. Add Password Record")
        print("4. Retrieve Password Record")
        print("5. Update Password Record")
        print("6. Logout")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            vault.create_vault()
        elif choice == "2":
            vault_data, key = vault.sign_in()
            last_action_time = time.time()
        elif choice == "3":
            if vault_data and key:
                vault.create_password_record(vault_data, key)
                last_action_time = time.time()
            else:
                print("You need to sign in first.")
        elif choice == "4":
            if vault_data and key:
                vault.retrieve_password_record(vault_data, key)
                last_action_time = time.time()
            else:
                print("You need to sign in first.")
        elif choice == "5":
            if vault_data and key:
                vault.update_password_record(vault_data, key)
                last_action_time = time.time()
            else:
                print("You need to sign in first.")
        elif choice == "6":
            vault_data = None
            key = None
            print("Logged out.")
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
