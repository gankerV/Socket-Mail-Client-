from Send import send_email
from Show import display_emails_in_folder,display_mailbox_folders,read_email


class EmailClient:
    def __init__(self):
        self.mailbox = {
            'inbox': [],
            'project': [],
            'important': [],
            'work': [],
            'spam': []
        }
    
    def send_email(self, to, cc, bcc, subject, content, has_attachment, num_attachments, attachment_paths):
        send_email(to, cc, bcc, subject, content, has_attachment, num_attachments, attachment_paths)

    def display_mailbox_folders(self):
        display_mailbox_folders()

    def display_emails_in_folder(self, folder_name):
        display_emails_in_folder(folder_name)

    def read_email(self, folder_name, email_index):
        read_email(folder_name, email_index)
       
