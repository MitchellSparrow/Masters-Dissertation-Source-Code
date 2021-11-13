import paramiko
import os
from secrets import USERNAME, PASSWORD

class MySFTPClient(paramiko.SFTPClient):
    def put_dir(self, source, target):
        ''' Uploads the contents of the source directory to the target path. The
            target directory needs to exists. All subdirectories in source are 
            created under target.
        '''
        for item in os.listdir(source):
            #print(item)
            if os.path.isfile(os.path.join(source, item)):
                # The following if condition just ensures that the model is not copied over each time
                # The model is quite a large file therefore it takes a while to copy it over
                print(item)
                if not (item == "my_model_2_3.h5" or item == "my_model_6.h5" or item == "my_model_10.h5" or item == "my_model_11.h5" or item == "my_model_13.h5"):
                    self.put(os.path.join(source, item), '%s/%s' % (target, item))
                
            else:
                self.mkdir('%s/%s' % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), '%s/%s' % (target, item))

    def mkdir(self, path, mode=511, ignore_existing=False):
        ''' Augments mkdir by adding an option to not fail if the folder exists  '''
        try:
            super(MySFTPClient, self).mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

HOST = 'gerty.cobotmakerspace.org'
PORT = 22
username = USERNAME
password = PASSWORD

transport = paramiko.Transport((HOST, PORT))
transport.connect(username=USERNAME, password=PASSWORD)
sftp = MySFTPClient.from_transport(transport)
sftp.mkdir('/home/mitchellsparrow/tmp/complete_program/', ignore_existing=True)
sftp.put_dir("C:\\Users\\mitch\\Documents\\Mitch Files\\University\\Postgrad\\Dissertation\\Code\\Robot_Control\\v1\\complete_program", '/home/mitchellsparrow/tmp/complete_program/')
sftp.close()