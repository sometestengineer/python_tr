import mysql.connector
from fixture.orm import ORMFixture
from model.group import Group

db = ORMFixture(host='127.0.0.1', name='addressbook', user='root', password='')

try:
    # id table 'address_in_groups' column 'group_id'
    l = db.get_contacts_not_in_group(Group(id='131'))
    for item in l:
        print item
    print len(l)
finally:
    pass


# db = ORMFixture(host='127.0.0.1', name='addressbook', user='root', password='')
#
# try:
#     # from that obj we connecting
#     l = db.get_contact_list()
#     for item in l:
#         print item
#     print len(l)
# finally:
#     # orm automatically closes connection
#     pass  # db.destroy()


# db = ORMFixture(host='127.0.0.1', name='addressbook', user='root', password='')
#
# try:
#     l = db.get_group_list()
#     for item in l:
#         print item
#     print len(l)
# finally:
#     # orm automatically closes connection
#     pass  # db.destroy()


# connection = mysql.connector.connect(host='127.0.0.1', database='addressbook', user='root', password='')
#
# try:
#     # from that obj we connecting
#     cursor = connection.cursor()
#     cursor.execute('select * from group_list')
#     for row in cursor.fetchall():
#         print row
# finally:
#     connection.close()
