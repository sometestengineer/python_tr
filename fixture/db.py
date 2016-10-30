import mysql.connector
from model.group import Group


class DbFixture:

    def __init__(self, host, name, user, password):
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host, database=name, user=user, password=password)

    def get_group_list(self):
        list = []
        # it checks whether the connection is available and raises an InterfaceError when not
        cursor = self.connection.cursor()
        try:
            # Execute given statement using given parameters
            cursor.execute('select group_id, group_name, group_header, group_footer from group_list')
            for row in cursor:
                (id, name, header, footer) = row
                # id=str(id) in to string to compare UI fields with DB fields
                list.append(Group(id=str(id), name=name, header=header, footer=footer))
        finally:
            cursor.close()
        return list

    def destroy(self):
        self.connection.close()
