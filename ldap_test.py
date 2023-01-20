from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPException, LDAPBindError

# ldap server hostname and port
ldsp_server = f"ldap://ldap.kin:389"

# dn
root_dn = "dc=rezal,dc=fr"

# ldap user and password
ldap_user_name = 'admin'
ldap_password = 'rezal@K1N'

# user
user = f'cn={ldap_user_name},root_dn'

server = Server(ldsp_server, get_info=ALL)

connection = Connection(server,
                        user=user,
                        password=ldap_password,
                        auto_bind=True)

print(f" *** Response from the ldap bind is \n{connection}")
