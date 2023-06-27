import os
import shutil

class util:
    def __init__(self):
        pass

    def setup_dir(self, server_id):
        if not os.path.exists(os.path.join(os.getcwd(), f"data/{server_id}")):
            os.mkdir(os.path.join(os.getcwd(), f"data/{server_id}"))

    def destroy_dir(self, server_id):
        shutil.rmtree(os.path.join(os.getcwd(), f"data/{server_id}"))