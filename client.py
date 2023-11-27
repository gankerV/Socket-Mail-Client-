import socket
import uuid
import os
import base64
from email.utils import formatdate
import time
import threading
import random
import string


HOST = '127.0.0.1'
username = 'Nhat Cuong <co6la.knm@gmail.com>'
sender_mail = 'cuong1312mn@gmail.com'
receiver_mail = 'mangmaytinh@gmail.com'
password = 'mnbjkl1235'
imageTypeList = ['png', 'jpg', 'jpeg', 'gif', '.hiec']
textTypeList = ['txt']
applicationTypeList = ['pdf', 'zip', 'rar', 'docx']
fileTypeAll = [imageTypeList, textTypeList, applicationTypeList]
folder_path = 'C:/Users/NHAT CUONG/Documents/.vscode/python/SocketProject/'
project_filter = ['co6la.knm@gmail.com']
subject_filter = ['urgent', 'ASAP']
work_filter = ['report', 'meeting']
spam_filter = ['virus', 'hack', 'crack']
response_file_path = 'C:/Users/NHAT CUONG/Documents/.vscode/python/SocketProject/response.txt'
auto_load_time = 10
folders = ['Inbox/', 'Project/', 'Important/', 'Work/', 'Spam/']
letters = [string.digits, string.ascii_letters]
stop_thread = False


class MailSender:
    SERVER_PORT = 2225

    def randomBoundary():
        boundary = '------------'
        for i in range(24):
            index = int(random.choice([0, 1]))
            boundary += random.choice(letters[index])

        return boundary

    def getFileType(filename):
        dot_index = filename.rfind('.')
        return filename[dot_index + 1:]
    
    @staticmethod
    def noFile_MailSender(TO_list, CC_list, BCC_list, subject, content):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, MailSender.SERVER_PORT))
        response = c.recv(1024).decode()

        c.sendall(f'EHLO [{HOST}]\r\n'.encode())
        response = c.recv(1024).decode()

        c.sendall(f'MAIL FROM:<{sender_mail}>\r\n'.encode())
        response = c.recv(1024).decode()

        if TO_list != ['']:
            for i in range(len(TO_list)):
                c.sendall(f'RCPT TO:<{TO_list[i]}>\r\n'.encode())
                response = c.recv(1024).decode()

        if CC_list != ['']:
            for i in range(len(CC_list)):
                c.sendall(f'RCPT TO:<{CC_list[i]}>\r\n'.encode())
                response = c.recv(1024).decode()

        if BCC_list != ['']:
            for i in range(len(BCC_list)):
                c.sendall(f'RCPT TO:<{BCC_list[i]}>\r\n'.encode())
                response = c.recv(1024).decode()

        c.sendall(f'DATA\r\n'.encode())
        response = c.recv(1024).decode()

        email_data = f'Message-ID: <{str(uuid.uuid4())}@gmail.com>\r\n'
        email_data += f'Date: {formatdate(localtime=True)}\r\n'
        email_data += f'MIME-Version: 1.0\r\n'
        email_data += f'User-Agent: Mozilla Thunderbird\r\n'
        email_data += f'Content-Language: en-US\r\n'
        
        if TO_list == [''] and CC_list == [''] and BCC_list != ['']:
            email_data += f'To: undisclosed-recipients: ;\r'
        elif TO_list != [''] or CC_list != ['']:
            if TO_list != ['']:
                email_data += f'To: '
                for i in range(len(TO_list)):
                    if i > 0:
                        email_data += f', {TO_list[i]}'
                    else:
                        email_data += f'{TO_list[i]}'
            if CC_list != ['']:
                email_data += f'Cc: '
                for i in range(len(CC_list)):
                    if i > 0:
                        email_data += f', {CC_list[i]}'
                    else:
                        email_data += f'{CC_list[i]}'

        email_data += f'\nFrom: {username}\r\n'
        email_data += f'Subject: {subject}\r\n'
        email_data += f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'
        email_data += f'Content-Transfer-Encoding: 7bit\r\n\n'

        for i in range(len(content)):
            content_lines = '\r\n'.join(content[i][k:k + 72] for k in range(0, len(content[i]), 72))
            email_data += f'{content_lines}\r\n\n'
        
        email_data += f'.\r\n'

        c.sendall(email_data.encode())

    @staticmethod
    def file_MailSender(TO_list, CC_list, BCC_list, subject, content, attached_files):
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, MailSender.SERVER_PORT))
        response = c.recv(1024).decode()

        c.sendall(f'EHLO [{HOST}]\r\n'.encode())
        response = c.recv(1024).decode()

        c.sendall(f'MAIL FROM:<{sender_mail}>\r\n'.encode())
        response = c.recv(1024).decode()
        
        if TO_list != ['']:
            for i in range(len(TO_list)):
                c.sendall(f'RCPT TO:<{TO_list[i]}>\r\n'.encode())
                response = c.recv(1024).decode()

        if CC_list != ['']:
            for i in range(len(CC_list)):
                c.sendall(f'RCPT TO:<{CC_list[i]}>\r\n'.encode())
                response = c.recv(1024).decode()

        if BCC_list != ['']:
            for i in range(len(BCC_list)):
                c.sendall(f'RCPT TO:<{BCC_list[i]}>\r\n'.encode())
                response = c.recv(1024).decode()

        c.sendall(f'DATA\r\n'.encode())
        response = c.recv(1024).decode()

        email_data = f'Content-Type: multipart/mixed; boundary="{MailSender.randomBoundary()}"\r\n'
        email_data += f'Message-ID: <{str(uuid.uuid4())}@gmail.com>\r\n'
        email_data += f'Date: {formatdate(localtime=True)}\r\n'
        email_data += f'MIME-Version: 1.0\r\n'
        email_data += f'User-Agent: Mozilla Thunderbird\r\n'
        email_data += f'Content-Language: en-US\r\n'

        if TO_list == [''] and CC_list == [''] and BCC_list != ['']:
            email_data += f'To: undisclosed-recipients: ;\r'
        elif TO_list != [''] or CC_list != ['']:
            if TO_list != ['']:
                email_data += f'To: '
                for i in range(len(TO_list)):
                    if i > 0:
                        email_data += f', {TO_list[i]}'
                    else:
                        email_data += f'{TO_list[i]}'
            if CC_list != ['']:
                email_data += f'Cc: '
                for i in range(len(CC_list)):
                    if i > 0:
                        email_data += f', {CC_list[i]}'
                    else:
                        email_data += f'{CC_list[i]}'

        email_data += f'\nFrom: {username}\r\n'
        email_data += f'Subject: {subject}\r\n\n'
        email_data += f'This is a multi-part message in MIME format.\r\n'
        email_data += f'--{MailSender.randomBoundary()}\r\n'
        email_data += f'Content-Type: text/plain; charset=UTF-8; format=flowed\r\n'
        email_data += f'Content-Transfer-Encoding: 7bit\r\n\n'

        for i in range(len(content)):
            email_data += f'{content[i]}\r\n\n'

        for i in range(len(attached_files)):
            email_data += f'--{MailSender.randomBoundary()}\r\n'
            fileType = MailSender.getFileType(attached_files[i])
            fileName = os.path.basename(attached_files[i])

            if fileType in fileTypeAll[0]:
                email_data += f'Content-Type: image/{fileType}; name="{fileName}"\r\n'
            elif fileType in fileTypeAll[1]:
                email_data += f'Content-Type: text/plain; charset=UTF-8;\r\n'
                email_data += f'name="{fileName}"\r\n'
            elif fileType in fileTypeAll[2]:
                email_data += f'Content-Type: application/'
                if fileType == 'zip':
                    email_data += f'x-zip-compressed; name="{fileName}"\r\n'
                elif fileType == 'rar':
                    email_data += f'x-compressed; name="{fileName}"\r\n'
                elif fileType == 'pdf':
                    email_data += f'pdf; name="{fileName}"\r\n'
                elif fileType == 'docx':
                    email_data += f'vnd.openxmlformats-officedocument.wordprocessingml.document; name={fileName}\r\n'
            
            email_data += f'Content-Disposition: attachment; filename="{fileName}"\r\n'
            email_data += f'Content-Transfer-Encoding: base64\r\n\n'

            if os.path.exists(attached_files[i]):
                with open(attached_files[i], 'rb') as file:
                    file_content = file.read()
                    file_content_lines = '\r\n'.join(base64.b64encode(file_content).decode()[k:k + 72] for k in range(0, len(base64.b64encode(file_content).decode()), 72))
                    email_data += f'{file_content_lines}\r\n'
        
        email_data += '\n'
        email_data += f'--{MailSender.randomBoundary()}--\r\n.\r\n'

        c.sendall(email_data.encode())

class MailReceiver:
    SERVER_PORT = 3335

    @staticmethod
    def folderCreater():
        for folder in folders:
            if not os.path.exists(os.path.join(folder_path, folder[:-1])):
                os.makedirs(os.path.join(folder_path, folder[:-1]))

    def getSenderEmailId(response):
        lines = response.splitlines()[1:-1]
        num_ids = [line.split(' ')[0] for line in lines]
        second_part = [line.split(' ')[1] for line in lines]
        email_ids = [element.split('.')[0] for element in second_part]

        return num_ids, email_ids

    def getFromInfo(lines):
        for i in range(len(lines)):
            headline = lines[i].split(':')[0]
            if headline == 'From':
                return lines[i].split('<')[1][:-2]

    def getSubjectInfo(lines):
        for i in range(len(lines)):
            headline = lines[i].split(':')[0]
            if headline == 'Subject':
                return lines[i].split(' ')[1]

    def getContentInfo(lines):
        start = 0
        end = 0
        content = ''

        for i in range(len(lines)):
            if lines[i] == 'Content-Transfer-Encoding: 7bit\n':
                start = i + 4
        
        for i in range(start, len(lines)):
            if lines[i].split(':')[0] == 'Content-Type':
                end = i - 5
                break
            elif lines[i] == '.\n':
                end = i - 3
                break
            elif i == len(lines) - 1:
                end = i

        count = 0
        for i in range(start, end):
            if count % 4 == 0:
                content += lines[i]
            count = count + 1

        return content

    def checkImportantMail(response):
        subject = MailReceiver.getSubjectInfo(response)

        for i in range(len(subject_filter)):
            index = str(subject).find(subject_filter[i])
            if index != -1:
                return True
            
        return False

    def checkWorkMail(response):
        content = MailReceiver.getContentInfo(response)

        for i in range(len(work_filter)):
            if content.find(work_filter[i]):
                return True
            
        return False

    def checkSpamMail(response):
        subject = MailReceiver.getSubjectInfo(response)
        content = MailReceiver.getContentInfo(response)

        for i in range(len(spam_filter)):
            index = subject.find(spam_filter[i])
            if index != -1:
                return True

            index = content.find(spam_filter[i])
            if index != -1:
                return True
            
        return False

    def mailFilter():
        with open(response_file_path, 'r') as file:
            lines = file.readlines()
            if MailReceiver.getFromInfo(lines) in project_filter:
                return 'Project/'
            elif MailReceiver.checkImportantMail(lines):
                return 'Important/'
            elif MailReceiver.checkWorkMail(lines):
                return 'Work/'
            elif MailReceiver.checkSpamMail(lines):
                return 'Spam/'
            else:
                return 'Inbox'

    def header_footerRemover(data):
        index = data.find('\n')
        return data[index + 1:-7]

    def checkExistFile(folder, mail_id, sender_name):
        read_file_name = '(đã đọc)' + ' ' + str(mail_id) + '_' + str(sender_name) + '.msg'
        unread_file_name = '(chưa đọc)' + ' ' + str(mail_id) + '_' + str(sender_name) + '.msg'
        for file_name in os.listdir(os.path.join(folder_path, folder)):
            if file_name == read_file_name or file_name == unread_file_name:
                return True
            
        return False

    def checkEndMail(data, boundary):
        if data.endswith(f'{boundary}--\r\n.\r\n'):
            return True
        elif data.endswith('.\r\n'):
            return True
        return False

    @staticmethod
    def mailLoader():
        c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        c.connect((HOST, MailReceiver.SERVER_PORT))
        response = c.recv(1024).decode()

        c.sendall(f'CAPA\r\n'.encode())
        response = c.recv(1024).decode()

        c.sendall(f'USER {receiver_mail}\r\n'.encode())
        response = c.recv(1024).decode()

        c.sendall(f'PASS {password}\r\n'.encode())
        response = c.recv(1024).decode()

        c.sendall(f'STAT\r\n'.encode())
        response = c.recv(1024).decode()

        c.sendall(f'LIST\r\n'.encode())
        response = c.recv(1024).decode()

        c.sendall(f'UIDL\r\n'.encode())
        response = c.recv(1024).decode()

        num_ids, mail_ids = MailReceiver.getSenderEmailId(response)
        
        times = 1
        boundary = ''

        for num_id in num_ids:
            num_id = int(num_id)

            c.sendall(f'RETR {num_id}\r\n'.encode())

            with open(response_file_path, 'w') as file:
                while True:
                    data = c.recv(1048576)

                    if times == 1:
                        index = data.decode().find('------------')
                        boundary = data.decode()[index:index + 36]

                    file.write(MailReceiver.header_footerRemover(data.decode()))

                    if MailReceiver.checkEndMail(data.decode(), boundary):
                        break

                    times = times + 1

            folder = MailReceiver.mailFilter()

            with open(response_file_path, 'r') as file:
                lines = file.readlines()
            
            sender_name = MailReceiver.getFromInfo(lines)
            
            file_name = '(chưa đọc)' + ' ' + str(mail_ids[num_id - 1]) + '_' + str(sender_name) + '.msg'
            
            if not MailReceiver.checkExistFile(folder, mail_ids[num_id - 1], sender_name):
                with open(os.path.join(folder_path, folder, file_name), 'wb') as write_file:
                    with open(response_file_path, 'rb') as read_file:
                        write_file.write(read_file.read())

        c.sendall(f'QUIT\r\n'.encode())

    @staticmethod
    def mailAutoLoader():
        while not stop_thread:
            MailReceiver.mailLoader()
            time.sleep(auto_load_time)

    @staticmethod
    def getMailsFromFolder(folder):
        index = 1

        for file_name in os.listdir(os.path.join(folder_path, folder)):
            if os.path.isfile(os.path.join(folder_path, folder, file_name)):
                print(index, '. ', file_name)
            
            index = index + 1

    @staticmethod
    def checkValidMailNum(folder_choose, file_choose):
        count = 0
        
        for file_name in os.listdir(os.path.join(folder_path, folders[folder_choose - 1])):
            count = count + 1

        if file_choose > count:
            return False
        return True

    def updateReadFile(folder_choose, file_choose):
        file_index = 1

        for file_name in os.listdir(os.path.join(folder_path, folders[folder_choose - 1])):
            if file_index == file_choose:
                index = file_name.find(') ')
                new_file_name = '(đã đọc)' + ' ' + file_name[index + 2:]
                new_file_path = folder_path + folders[folder_choose - 1] + new_file_name
                os.rename(os.path.join(folder_path, folders[folder_choose - 1], file_name), new_file_path)

            file_index = file_index + 1

    @staticmethod
    def readFile(folder_choose, file_choose):
        file_index = 1

        for file_name in os.listdir(os.path.join(folder_path, folders[folder_choose - 1])):
            if file_index == file_choose:
                with open(os.path.join(folder_path, folders[folder_choose - 1], file_name), 'r') as file:
                    lines = file.readlines()
                    print(MailReceiver.getContentInfo(lines))

                    break
            
            file_index = file_index + 1

    def is_base64(s):
        try:
            decoded_data = base64.b64decode(s)
            return True
        except base64.binascii.Error as e:
            return False

    def downFile(folder_link, folder_choose, file_choose):
        file_index = 1

        for file_name in os.listdir(os.path.join(folder_path, folders[folder_choose - 1])):
            if file_index == file_choose:
                with open(os.path.join(folder_path, folders[folder_choose - 1], file_name), 'r') as read_file:
                    boundary = read_file.readline().split('"')[1]

                    stop = False
                    while True:
                        if stop:
                            break
                        line = ''
                        while line.split(':')[0] != 'Content-Disposition':
                            line = read_file.readline()

                        attached_file_name = line.split('"')[1]
                        print(attached_file_name)

                        read_file.readline()
                        read_file.readline()

                        with open(os.path.join(folder_link, attached_file_name), 'wb') as write_file:
                            line = read_file.readline()
                            while not line in[f'--{boundary}\n', f'--{boundary}']:
                                if line != '\n':
                                    while not MailReceiver.is_base64(line):
                                        line = line + '='
                                    write_file.write(base64.b64decode(line))

                                line = read_file.readline()

                                if line == f'--{boundary}':
                                    stop = True
                                    break
                
                break
            
            file_index = file_index + 1

    @staticmethod
    def mailReceiver():
        folder_choose = 0
        file_choose = -1

        while True:
            print('\nĐây là danh sách các folder trong mailbox của bạn:')
            print('1. Inbox')
            print('2. Project')
            print('3. Important')
            print('4. Work')
            print('5. Spam')
            folder_choose = input('Bạn muốn xem email trong folder nào (Nhấn enter để thoát ra ngoài): ')

            if folder_choose == '':
                quit()

            if int(folder_choose) >= 1 and int(folder_choose) <= 5:
                break

        folder_choose = int(folder_choose)

        print('')

        while True:
            while True:
                print(f'Đây là danh sách email trong {folders[folder_choose - 1][:-1]} folder')
                MailReceiver.getMailsFromFolder(folders[folder_choose - 1])

                print('')

                file_choose = input('Bạn muốn đọc Email thứ mấy (Nhấn enter để thoát ra ngoài, nhấn 0 để xem lại danh sách mail): ')

                if file_choose == '':
                    quit()

                if file_choose == '0':
                    MailReceiver.mailReceiver()
                    quit()

                file_choose = int(file_choose)

                if not MailReceiver.checkValidMailNum(folder_choose, file_choose):
                    print(f'{folders[folder_choose - 1]} folder không có file thứ ', file_choose)
                    continue
                else:
                    break

            print(f'Nội dung của mail thứ {str(file_choose)}:')
            MailReceiver.readFile(folder_choose, file_choose)

            save = int(input('Trong email này có file đính kèm, bạn có muốn lưu không? (1. có, 2. không): '))

            if save == 1:
                folder_link = input('Cho biết đường dẫn đến thư mục bạn muốn lưu: ')
                MailReceiver.downFile(folder_link, folder_choose, file_choose)
            
            MailReceiver.updateReadFile(folder_choose, file_choose)

class MailManipulation:
    def mailManupilation():
        while True:
            print('Vui lòng chọn Menu:')
            print('1. Để gửi mail')
            print('2. Để xem danh sách các email đã nhận')
            print('3. Thoát')

            choose = int(input('Bạn chọn: '))

            if choose == 1:
                attached_files = []
                content = []

                print('Đây là thông tin soạn email: (nếu không điền vui lòng nhấn enter để bỏ qua)')
                TO_list = [str(x) for x in input("To: ").split(', ')]
                CC_list = [str(x) for x in input("CC: ").split(', ')]
                BCC_list = [str(x) for x in input("BCC: ").split(', ')]
                
                subject = input('Subject: ')
                line = input('Content: ')
                while line != '.':
                    content.append(line)
                    line = input()
                attached_file_check = int(input('Có gửi kèm file (1. có, 2. không): '))

                if attached_file_check == 1:
                    attached_file_num = int(input('Số lượng file muốn gửi: '))
                    for i in range(attached_file_num):
                        attached_file = input(f'Cho biết đường dẫn file thứ {i + 1}:')
                        attached_files.append(attached_file)
                    
                    # Gửi mail có đính kèm file
                    MailSender.file_MailSender(TO_list, CC_list, BCC_list, subject, content, attached_files)
                elif attached_file_check == 2:
                    # Gửi mail không đính kèm file
                    MailSender.noFile_MailSender(TO_list, CC_list, BCC_list, subject, content)

                print('\nĐã gửi email thành công\n')

            elif choose == 2:
                MailReceiver.mailLoader()
                
                MailReceiver.mailReceiver()

            elif choose == 3:
                quit()

    @staticmethod
    def main():
        global stop_thread

        MailReceiver.folderCreater()

        mail_manupilation_thread = threading.Thread(target=MailManipulation.mailManupilation)
        mail_manupilation_thread.start()

        auto_load_mail_thread = threading.Thread(target=MailReceiver.mailAutoLoader)
        auto_load_mail_thread.start()

        mail_manupilation_thread.join()

        if not mail_manupilation_thread.is_alive():
            stop_thread = True

        auto_load_mail_thread.join()


if __name__ == "__main__":
    MailManipulation.main()