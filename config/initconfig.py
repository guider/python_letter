import configparser

CONFIG_FILE_NAME= './config.ini'

def load_config():
    config=configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    return config




if __name__=='__main__':
    conf = (load_config())
    print(conf['DATABASE']['db_name'])