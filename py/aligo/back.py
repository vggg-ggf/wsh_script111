from aligo import Aligo,set_config_folder
 
folder_path1 = "/dockge"
folder_path2 = "/mnt/hdd/mt_photos"
# folder_path3 = "/etc/systemd/system"


set_config_folder('Aligo\\config')
ali = Aligo(name='账号1')


# def getinfo():
# 	user = ali.get_user()
# 	print(user)
# 	ll = ali.get_file_list()
# 	for file in ll:
# 		print(file.file_id, file.name, file.type)

# getinfo()        

def upload():
    ali.sync_folder(folder_path2,'66e6c4e4fb3265e6c6e740fe983b2e281b83efa1')
    ali.sync_folder(folder_path1,'669f8784d9eccd3dd1c249819a1923b6ea055807')
#    ali.sync_folder(folder_path3,'665a775a16ba96e45d1e499ba722eab2ad791bdf')
upload()