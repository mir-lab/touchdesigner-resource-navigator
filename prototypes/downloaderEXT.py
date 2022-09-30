from genericpath import isfile
from pathlib import Path, PureWindowsPath
import requests
import os

import threading
import random
from queue import Queue

class downlaoderAgent:

    def __init__(self, owner_op:OP) -> None:
        self.Owner = owner_op
        self.jobs = None
        self.total_remote_toxes = 0
        
        self.Downloads_remaining = tdu.Dependency(0)

    def Fetch_tox_components(self) -> None:
        manifest = f"{project.folder}/tox_manifest.txt"

        #TODO - this should be in the manifest file
        example_name = "Fundamentals"

        pallet_dir = app.userPaletteFolder
        derivative_user_dir = PureWindowsPath(pallet_dir).parents[0]
        example_dir = f"{derivative_user_dir}/Curriculum/{example_name}"

        print(example_dir)

        # check to make sure our target dir exists
        if os.path.isdir(example_dir):
            pass

        # create it if it does not yet exists
        else:
            valid_path = Path(example_dir)
            valid_path.mkdir(parents=True)

        # create a queue
        self.jobs = Queue()

        self._fill_queue(manifest, example_dir)
        op("execute_status").par.active = True
    
    def _fill_queue(self, manifest:str, example_dir:str) -> None:

        with open(manifest, 'r') as tox_manifest:
            lines = tox_manifest.readlines()
            self.total_remote_toxes = len(lines)

            # threaded downloader
            for each_line in lines:
                stripped_line = each_line.strip()
                base_name = os.path.basename(stripped_line)
                local_file_path = f"{example_dir}/{base_name}"

                # create a job for each download
                self.jobs.put([stripped_line, local_file_path])

        # start up 10 downloader threads
        for each_thread in range(10):
            worker = threading.Thread(target=self._download_tox, args=(self.jobs,))
            worker.start()

    def _download_tox(self, q:Queue) -> None:
        while not q.empty():
            value = q.get()

            tox_url = value[0]
            local_path = value[1]
            
            response = requests.get(tox_url)
            with open(local_path, "wb") as local_tox:
                local_tox.write(response.content)

            q.task_done()

    def _current_queue_size(self) -> int:
        return self.jobs.qsize()

    def Download_status(self) -> tuple:
        self.Downloads_remaining.val = self._current_queue_size()

        if self._current_queue_size() == 0:
            op("execute_status").par.active = False
        return self.total_remote_toxes, self._current_queue_size()