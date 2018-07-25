from fabric import Connection

class SSHAdapter():
    def connect(self, host, user):
        self.conn = Connection(host=host, user=user)

    def run_command(self, cmd, pwd=None):
        if pwd is not None:
            self.conn.cd(pwd)
        self.conn.run(cmd)

    def put_file(self, local_path, remote_path):
        self.conn.put(local_path, remote_path)

    def get_file(self, remote_path, local_path):
        self.conn.get(remote_path, local_path)
