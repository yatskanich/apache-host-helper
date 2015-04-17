#!/usr/bin/env python3
# -*-coding: utf-8 -*-
import os


class WriteHost:
    www_dir = ''

    def __init__(self):
        self.choice = 0

    def get_choice(self):
        print('''
        ================================
        Select action:
        1 - create catalog end host file
        2 - create only host file
        3 - remove catalog and host
        4 - remove host only
        5 - exit
        ================================
        ''')
        try:
            self.choice = int(input('? '))
        except Exception:
            print('Your choice is wrong! Please, try again...')
            exit()

    def main(self):
        self.check_user_settings()
        self.get_choice()
        if self.choice == 1:
            self.create_catalog(1)
        elif self.choice == 2:
            self.create_host(2)
        elif self.choice == 3:
            catalog = str(input("Enter catalog name: "))
            hostname = str(input("Enter host name: "))
            self.remove_catalog(catalog)
            self.remove_host(hostname)
        elif self.choice == 4:
            hostname = str(input("Enter host name: "))
            self.remove_host(hostname)
        else:
            print("Good bye!")
            exit()

    def check_user_settings(self):
        if not os.path.isfile('user_settings.txt'):
            self.www_dir = str(input('Type your www dir like "/home/user/www":\n'))
            with open('user_settings.txt', 'w') as user_settings:
                user_settings.write(self.www_dir)
        else:
            with open('user_settings.txt', 'r') as user_settings:
                line = user_settings.read()
                self.www_dir = line

    def create_catalog(self, cat):
        catalog = str(input('Enter dir name for site ({www_dir}...):'.format(www_dir=self.www_dir)))
        if catalog == '':
            self.create_catalog(cat)

        if cat == 1:
            print('Creating directory {www_dir}{catalog}...\n'.format(www_dir=self.www_dir, catalog=catalog))
            os.system('mkdir {www_dir}{catalog}'.format(www_dir=self.www_dir, catalog=catalog))

        self.create_host(catalog)

    def create_host(self, catalog):
        hostname = input('Enter hostname:')
        if hostname == '':
            self.create_host(catalog)

        print('Add to host file... \n')
        with open('/etc/hosts', 'rt') as hosts_file:
            s = hosts_file.read() + '\n127.0.0.1 {hostname}'.format(hostname=hostname)
            with open('/tmp/etc_hosts.tmp', 'wt') as hosts_file:
                hosts_file.write(s)
        os.system('sudo mv /tmp/etc_hosts.tmp /etc/hosts')

        print('Generate virtual host file...\n')
        with open('/tmp/' + hostname + '.tmp', 'wt') as file:
            conf = '<VirtualHost *:80>\n'
            conf += '\tServerAdmin webmaster@slocalhost\n'
            conf += '\tServerName {hostname}\n'.format(hostname=hostname)
            conf += '\tServerAlias {hostname}\n'.format(hostname=hostname)
            conf += '\tDocumentRoot {www_dir}{catalog}\n'.format(www_dir=self.www_dir, catalog=catalog)
            conf += '\t<Directory />\n'
            conf += '\t\tOptions All\n'
            conf += '\t\tAllowOverride All\n'
            conf += '\t</Directory>\n'
            conf += '</VirtualHost>'
            file.write(conf)

        os.system('sudo mv /tmp/' + hostname + '.tmp /etc/apache2/sites-available/' + hostname + '.conf')
        os.system('sudo a2ensite ' + hostname + '.conf')
        os.system('sudo service apache2 restart')

    def remove_catalog(self, catalog):
        os.system('rm -rf {www_dir}{catalog}'.format(www_dir=self.www_dir, catalog=catalog))

    def remove_host(self, hostname):
        if os.path.isfile('/etc/apache2/sites-available/{hostname}.conf'.format(hostname=hostname)):
            os.system('sudo a2dissite ' + hostname + '.conf')
            os.system("sudo rm /etc/apache2/sites-available/{hostname}.conf".format(hostname=hostname))
        with open("/etc/hosts", "r") as hosts_file:
            lines = hosts_file.readlines()
        with open("/etc/hosts", "w") as hosts_file:
            for line in lines:
                if line != '127.0.0.1 {hostname}\n'.format(hostname=hostname):
                    hosts_file.write(line)
                elif line != '\n127.0.0.1 {hostname}\n'.format(hostname=hostname):
                    hosts_file.write(line)

        os.system('sudo service apache2 restart')

if __name__ == "__main__":
    print('Generate virtual host script.\n')
    h = WriteHost()
    h.main()