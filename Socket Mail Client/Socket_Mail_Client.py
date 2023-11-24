#from Send import SendTO, SendCC, SendBCC, Send1Txt, Send1Types, SendLimit, SendTypes
from Dowload import Dowload_SaveMail
from Filter import Filt
from classes import EmailClient




if __name__ == "__main__":
    email_client = EmailClient()
    
    while True:
        Dowload_SaveMail()
        print("Vui lòng chọn Menu:")
        print("1. Để gửi email")
        print("2. Để xem danh sách các email đã nhận")
        print("3. Thoát")

        choice = input("Bạn chọn: ")

        if choice == "1":
            to = input("To: ")
            cc = input("CC: ")
            bcc = input("BCC: ")
            subject = input("Subject: ")
            content = input("Content: ")
            has_attachment = input("Có gửi kèm file (1. có, 2. không): ") == "1"

            num_attachments = 0
            attachment_paths = []

            if has_attachment:
                num_attachments = int(input("Số lượng file muốn gửi: "))
                for i in range(num_attachments):
                    path = input(f"Cho biết đường dẫn file thứ {i + 1}: ")
                    attachment_paths.append(path)

            email_client.send_email(
                to,
                cc,
                bcc,
                subject,
                content,
                has_attachment,
                num_attachments,
                attachment_paths,
            )

        elif choice == "2":
            email_client.display_mailbox_folders()
            folder_choice = input("Bạn muốn xem email trong folder nào: ")

            if folder_choice.isdigit() and 1 <= int(folder_choice) <= 5:
                folder_name = {
                    "1": "inbox",
                    "2": "project",
                    "3": "important",
                    "4": "work",
                    "5": "spam",
                }[folder_choice]

                email_client.display_emails_in_folder(folder_name)
                email_index = input(
                    "Bạn muốn đọc Email thứ mấy (nhấn enter để thoát): "
                )

                if email_index.isdigit():
                    email_client.read_email(folder_name, int(email_index))
            # kiểm tra và lưu attached file 
        elif choice == "3":
            break
