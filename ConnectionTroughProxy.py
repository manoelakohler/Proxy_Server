from paramiko import SSHClient, AutoAddPolicy, SFTPClient


def test_connection(client):
    global stdin, stdout, stderr
    stdin, stdout, stderr = client.exec_command('pwd')
    print(stdout.read())
    stdin, stdout, stderr = client.exec_command('ls')
    print(stdout.read())
    stdin, stdout, stderr = client.exec_command('mkdir aaaaaa')
    print(stdout.read())
    stdin, stdout, stderr = client.exec_command('ls')
    print(stdout.read())
    stdin, stdout, stderr = client.exec_command('rmdir aaaaaa')
    print(stdout.read())
    stdin, stdout, stderr = client.exec_command('ls')
    print(stdout.read())

# Set up the proxy (forwarding server) credentials
proxy_hostname = '<xxx.xxx.xxx.xxx>'
proxy_username = '<user_name>'
port = 22

# Instantiate a client and connect to the proxy server
proxy_client = SSHClient()
proxy_client.set_missing_host_key_policy(policy=AutoAddPolicy())
proxy_client.connect(
    proxy_hostname,
    port=port,
    username=proxy_username,
    key_filename=r'<private_key_file>'
)

test_connection(proxy_client)

# Get the client's transport and open a `direct-tcpip` channel passing
# the destination hostname:port and the local hostname:port
transport = proxy_client.get_transport()
dest_addr = ('<xxx.xxx.xxx.xxx>', port)
local_addr = ('<xxx.xxx.xxx.xxx>', port)
channel = transport.open_channel("direct-tcpip", dest_addr, local_addr)

# Create a NEW client and pass this channel to it as the `sock` (along with
# whatever credentials you need to auth into your REMOTE box
remote_client = SSHClient()
remote_client.set_missing_host_key_policy(policy=AutoAddPolicy())
remote_client.connect('localhost',
                      port=1234,
                      username='<user_name>',
                      key_filename=r'<private_key_file>',
                      sock=channel)

# `remote_client` should now be able to issue commands to the REMOTE box
test_connection(remote_client)

# Test sftp
sftp = SFTPClient.from_transport(t=remote_client.get_transport())

sftp.mkdir(path=r'teste')
sftp.listdir()
sftp.rmdir(path=r'teste')
sftp.listdir()



