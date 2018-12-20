import docker
import ldap
import pytest
import time 


@pytest.fixture
def active_directory(tmpdir):
  environment = {
	'SAMBA_DOMAIN': 'openforce',
	'SAMBA_HOST_NAME': 'dc',
	'SAMBA_ADMINPASS': 'Abc123!',
	'SAMBA_KRBTGTPASS': 'Abc123!',
	'SAMBA_REALM': 'OPENFORCE.ORG',
  }
  ports = {
	'22': 2222,
	'53': 5353,
	'88': 88,
	'135': 135,
	'139': 139,
	'389': 389,
	'445': 445,
	'464': 464,
	'636': 636,
	'1024': 1024,
	'3268': 3268,
	'3269': 3269
  }
  client = docker.from_env()
  container = client.containers.run('xnandersson/samba-ad-dc', command='dcpromo', privileged=True, ports=ports, name='dc', environment=environment, detach=True)
  time.sleep(5)
  yield
  container.kill()
  container.remove()
