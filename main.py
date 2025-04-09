# main.py
import asyncio
from api.auth_module import Authenticator
from api.iclass_api import TronClassAPI

async def main():
    print("🔐 Logging in...")
    auth = Authenticator()
    session = auth.perform_auth()

    api = TronClassAPI(session)

    while True:
        print("\n📚 iClass TKU API Menu")
        print("1. Get Todos")
        print("2. Get Bulletins")
        print("3. Get Courses")
        print("4. Upload File")
        print("5. Submit Homework")
        print("6. Exit")

        choice = input("Select an option (1-6): ")

        if choice == "1":
            result = await api.get_todos()
            print("\n✅ Todos:")
            print(result)

        elif choice == "2":
            result = await api.get_bulletins()
            print("\n📢 Bulletins:")
            print(result)

        elif choice == "3":
            result = await api.get_courses()
            print("\n🎓 Courses:")
            print(result)

        elif choice == "4":
            file_path = input("Enter the file path to upload: ").strip()
            upload_id = await api.upload_file(file_path)
            print(f"\n📁 Uploaded file ID: {upload_id}")

        elif choice == "5":
            try:
                activity_id = int(input("Enter activity ID: "))
                upload_ids = input("Enter upload file IDs (comma-separated): ")
                upload_ids = [int(i.strip()) for i in upload_ids.split(",") if i.strip()]
                result = await api.submit_homework(activity_id, upload_ids)
                print("\n📨 Submission Result:")
                print(result)
            except ValueError:
                print("❌ Invalid input. Please enter numbers only.")

        elif choice == "6":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid option. Please choose a number between 1 and 6.")

if __name__ == '__main__':
    asyncio.run(main())
