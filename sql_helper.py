#!/usr/bin/env python3
# coding:utf-8

import pymysql.cursors
from config.initconfig import load_config
import  json



class MySQLClient(object):
    def _init_configuration(self):
        config = load_config()
        # self.db_host = config['DATABASE']['db_host']
        # self.db_user = config['DATABASE']['db_user']
        # self.db_password = config['DATABASE']['db_password']
        # self.db_name = config['DATABASE']['db_name']

        self.db_host = 'localhost'
        self.db_user = 'root'
        self.db_password ='Cbgj@2017'
        self.db_name = 'letters'

    def __init__(self):
        self._init_configuration()
        self.conn = pymysql.connect(host=self.db_host,
                                    user=self.db_user,
                                    passwd=self.db_password,
                                    db=self.db_name)
        self.conn.set_charset('utf8')

    def close(self):
        self.conn.close()

    def execute(self, sql, args=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(sql, args)
            self.conn.commit()
        except Exception as e:
            print(e)



    def insertLetter(self,resArgs):
        sql = "INSERT INTO `letter`(`content`,`chinese_word`,`imgurl`,`remote_id`) VALUES (%s,%s,%s,%s)"

        print(json.dumps(resArgs['content']))
        self.execute(sql,(resArgs['content'],resArgs['chinese_word'],resArgs['imgurl'],json.dumps(resArgs['id'])))

        # self.execute(sql,('content','chinese_word','imgurl','128'))
    """
    args sequence: `fakeid`, `to_uin`, `msg_id`, `nick_name`, `date_time`, `content`
    """

    def insert_member(self, args):
        sql = "INSERT INTO `members` (`fakeid`, `to_uin`, `msg_id`, `nick_name`, `date_time`, `content`) VALUES (%s, %s, %s, %s, %s, %s)"
        self.execute(sql, args)

    """
    args sequence: `fakeid`, `msg_id`, `date_time`, `to_uin`, `content`
    """

    def insert_messages(self, args):
        sql = "INSERT INTO `messages` (`fakeid`, `msg_id`, `date_time`, `to_uin`, `content`) VALUES (%s, %s, %s, %s, %s)"
        self.execute(sql, args)

    def select_table(self):
        with self.conn.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
