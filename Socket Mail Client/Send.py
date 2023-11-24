# lấy thông tin General trong Config.xml 
def ReadGeneral():
def Input():

def SendTO():
    
def SendCC():
    

def SendBCC():
    
#gửi 1 file Txt
def Send1Txt():

#gửi 1 file với nhiều kiểu
def Send1Types():
    
def SendTypes():
# gửi nhiều file với nhiều kiểu

#gửi với dung lượng file bị giới hạn 
def SendLimit():


#gộp các hàm trên thành 1 hàm 
def send_email(self, to, cc, bcc, subject, content, has_attachment, num_attachments, attachment_paths):
        # Code 
        # ...

        print("Đã gửi email thành công")