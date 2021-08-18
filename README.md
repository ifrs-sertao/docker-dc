=========================================
Samba4 Active Directory Domain Controller
=========================================
Sobe uma versão de desenvolvimento do Samba 4 DC em Docker.


Abstract
--------

Docker Image, preloaded with Samba4 and a dcpromo-script
that promotes the container on startup using the supplied variables.


Build
-----

.. code:: bash
  
  $ sudo docker build -t samba4/dc .


Run
---
No exemplo **SAMBA_REALM=EXAMPLE.ORG**, **SAMBA_DOMAIN=example** e **SAMBA_HOST_NAME=dc**. Outras variáveis ambiente e portas podem ser customizadas.

```shell
sudo docker run --privileged --name dc --rm -d -e SAMBA_DOMAIN=example -e SAMBA_HOST_NAME=dc -e SAMBA_ADMINPASS=Abc123! -e SAMBA_KRBTGTPASS=Abc123! -e SAMBA_REALM=EXAMPLE.ORG -p 2222:22 -p 5353:53 -p 88:88 -p 135:135 -p 139:139 -p 389:389   -p 445:445 -p 464:464 -p 636:636 -p 1024:1024 -p 3268:3268 -p 3269:3269 xnandersson/dc /usr/local/bin/dcpromo.py
```

Administer
----------
É possivel administrar via bash com samba-tools (ou acessando via Portainer)
```shell

  $ sudo docker exec -ti dc /bin/bash
  # samba-tool user create nandersson Secret012
  # samba-tool user setpassword Administrator
  # samba-tool user setpassword nandersson
  # samba-tool user list
  # samba-tool group add Staff
  # samba-tool group add Superusers
  # samba-tool group addmembers Staff nandersson
  # samba-tool group addmembers Superusers nandersson
```

Package Dependencies
--------------------

```shell
  $ sudo apt-get install docker.io devscripts python3-dev libldap2-dev libsasl2-dev python3-venv ldap-utils -y
  $ sudo docker pull ubuntu:latest
  $ sudo usermod -a -G docker ${USER} 
  $ su - ${USER}
```  

Pytest
------
```shell

  $ python3 -m venv ~/venv3/docker-dc
  $ source ~/venv3/docker-dc/bin/activate
  $ pip install -U pip
  $ pip install -r requirements.txt
  $ echo TLS_REQCERT ALLOW >> ~/.ldaprc
  $ pytest
  ```

Python Example 
--------------
Exemplo de consulta usando Python.
```python
  import ldap

  con = ldap.initialize('ldaps://127.0.0.1')
  con.set_option(ldap.OPT_X_SASL_NOCANON, 1)
  con.set_option(ldap.OPT_REFERRALS, 0)
  con.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
  con.protocol_version = ldap.VERSION3
  con.simple_bind_s('Administrator@example.ORG', 'Abc123!')

  entries = con.search_s(
    base="dc=example,dc=org", 
    scope=ldap.SCOPE_SUBTREE, 
    filterstr='(objectClass=User)', 
    attrlist=('cn','displayName'))

  for entry in entries:
    print(entry)
```
LDAP Search Example
-------------------
Exemplos de consultas usando LDAP Search.
```shell
  $ ldapsearch  -H ldap://localhost:3268 -b 'cn=users,dc=example,dc=org' -x -D "Administrator@example.ORG"  -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldap://localhost      -b 'cn=users,dc=example,dc=org' -x -D "Administrator@example.ORG"  -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldap://localhost:3268 -b 'cn=users,dc=example,dc=org' -x -D "Administrator@example.ORG" -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
  $ ldapsearch  -H ldaps://localhost:3269 -b 'dc=example,dc=org' -x -w 'Abc123!'  -D "example\Administrator" -s sub  '(sAMAccountName=nandersson)'
  $ ldapsearch  -H ldap://localhost:389 -b 'cn=users,dc=example,dc=org' -x -D "Administrator@example.ORG" -s sub -Z "(cn=*)" cn mail sn -w 'Abc123!'
```
DNS Example  
-----------
```shell
  $ samba-tool dns zonelist 192.168.1.10
  $ samba-tool dns zonelist 192.168.1.10  -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns zonecreate 192.168.1.10 1.168.192.in-addr.arpa
  $ samba-tool dns zonecreate 192.168.1.10 1.168.192.in-addr.arpa -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 10 PTR dc.example.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 example.org kubernetes A 192.168.1.12 -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 12 PTR kubernetes.example.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 example.org freeswitch A 192.168.1.14 -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 14 PTR freeswitch.example.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 1.168.192.in-addr.arpa 15 PTR docker.example.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 example.org docker A 192.168.1.15 -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns add 192.168.1.10 example.org k8s CNAME kubernetes.example.org -U Administrator --password='Yb92!!Ha99'
  $ samba-tool dns query 192.168.1.10 1.168.192.in-addr.arpa 1.168.192.in-addr.arpa ALL -U Administrator --password='Abc123!'
```
# TO DO

- [ ] Configurar dentro de uma stack com docker-compose
- [ ] Incluir na stack um client com LDAP Search