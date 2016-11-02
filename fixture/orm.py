# orm - object relational mapping, to interact with db not using SQL
from pony.orm import *
from datetime import datetime
from model.group import Group
from model.contact import Contact
from pymysql.converters import decoders

class ORMFixture:

    db = Database()

    class ORMGroup(db.Entity):
        # db.Entity to link class with obj we created under,
        # class describes obj that will be stored in db
        _table_ = 'group_list'
        # id located in table colomn 'group_ID'
        id = PrimaryKey(int, column='group_id')
        name = Optional(str, column='group_name')
        header = Optional(str, column='group_header')
        footer = Optional(str, column='group_footer')
        # describing links to db tables through table, linked to column, link with what,
        # lazy = info extracted (retrieved) only when we access it
        contacts = Set(lambda: ORMFixture.ORMContact, table='address_in_groups', column='id', reverse='groups', lazy=True)

    class ORMContact(db.Entity):
        _table_ = 'addressbook'
        id = PrimaryKey(int, column='id')
        firstname = Optional(str, column='firstname')
        lastname = Optional(str, column='lastname')
        # needed to filter deleted elements in bd that aren't shown in UI
        deprecated = Optional(datetime, column='deprecated')
        groups = Set(lambda: ORMFixture.ORMGroup, table='address_in_groups', column='group_id', reverse='contacts', lazy=True)

    def __init__(self, host, name, user, password):
        # bind = link db with
        # conv=decoders from pymysql to transform deprecated fields
        self.db.bind('mysql', host=host, database=name, user=user, password=password, conv=decoders)
        self.db.generate_mapping()
        # to see sql requests 'pony' make
        sql_debug(True)

    # method to convert object to our model(package) objects
    def convert_groups_to_model(self, groups):
        def convert(group):
            return Group(id=str(group.id), name=group.name, header=group.header, footer=group.footer)
        return list(map(convert, groups))

    @db_session
    def get_group_list(self):
        # db_session is required when working with data, # with db_session: # 2nd option how u create db session
        # when we are selecting objects from ORMGroup, data from db is converted to objs of this class
        # SELECT `g`.`group_id`, `g`.`group_name`, `g`.`group_header`, `g`.`group_footer`
        # FROM `group_list` `g`
        return self.convert_groups_to_model(select(g for g in ORMFixture.ORMGroup))

    # method to convert object to our model(package) objects
    def convert_contacts_to_model(self, contacts):
        def convert(contact):
            return Contact(id=str(contact.id), firstname=contact.firstname, lastname=contact.lastname)
        return list(map(convert, contacts))

    @db_session
    def get_contact_list(self):
        # SELECT `c`.`id`, `c`.`firstname`, `c`.`lastname`, `c`.`deprecated`
        # FROM `addressbook` `c`
        # WHERE `c`.`deprecated` IS NULL
        # contact for contact in ORMFixture.ORMContanct if deprecated values in db == 0 == None
        return self.convert_contacts_to_model(select(c for c in ORMFixture.ORMContact if c.deprecated is None))

    @db_session
    def get_contacts_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(orm_group.contacts)


    @db_session
    def get_contacts_not_in_group(self, group):
        orm_group = list(select(g for g in ORMFixture.ORMGroup if g.id == group.id))[0]
        return self.convert_contacts_to_model(
            select(c for c in ORMFixture.ORMContact if c.deprecated is None and orm_group not in c.groups))





























