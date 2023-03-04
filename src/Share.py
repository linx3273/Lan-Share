import Reusables
import Buffer
from pathlib import Path
import os
from PyInquirer import prompt
from rich.progress import Progress
import time

msgs = Reusables.Msgs()

'''
Buffer send rule
1 - Send name
2 - Send size (if -1: it's a directory)
3 - Send bytes (if in case it's a file)

Buffer recv rule
1 - Get name
2 - Get size
3 - If size is -1 mkdir; otherwise receive bytes
'''


class Share:
    def __init__(self, path):
        # points to file/folder that must be sent or destination where file/folder must be received
        self._path = Path(path)
        self._conn = None  # holds the instance of the connection
        self._mode = None

    def send_files(self):
        """
        Method checks if the given file is a directory or a single file and transfers data accordingly. In case of a
        directory it also transfers all files under that directory including subdirectories.
        Sends -1 as file size, when sending utf-8 data for a directory.
        :return:
        1 - When it was able to send the files successfully
        """
        start = time.time()
        try:
            buffer = Buffer.Buffer(self._conn)

            if os.path.isdir(self._path):
                os.chdir(self._path)    # setting directory to directory where files are located

                # Given path is pointing to a directory so transfer accordingly
                # Walk through the directory as the files are being transferred
                for root, subdir, files in os.walk(self._path):
                    # sending current directory info to receiver
                    buffer.put_utf8(Path(root).relative_to(self._path.parent).as_posix())
                    buffer.put_utf8(str(-1))  # for directories sending size as -1

                    for file_name in files:
                        # sending file name
                        file_name = Path(root).joinpath(file_name).relative_to(self._path)

                        name = Path(self._path.name).joinpath(file_name).as_posix()
                        buffer.put_utf8(name)

                        # obtaining and sending file size
                        file_size = os.path.getsize(file_name)
                        buffer.put_utf8(str(file_size))

                        # sending file
                        with Progress() as progress:
                            task = progress.add_task(name, total=file_size)
                            with open(file_name, 'rb') as f:
                                data = f.read()
                                buffer.put_bytes(data)

                                progress.update(task, advance=len(data))

            else:
                # Given path points to a file, so transfer directly

                # sending file name
                buffer.put_utf8(self._path.name)

                # obtaining and sending file size
                file_size = os.path.getsize(self._path)
                buffer.put_utf8(str(file_size))

                # sending file
                with Progress() as progress:
                    task = progress.add_task(str(self._path), total=file_size)
                    with open(self._path, "rb") as f:
                        data = f.read()
                        buffer.put_bytes(data)

                        progress.update(task, advance=len(data))

            # returning back to original program directory
            os.chdir(Reusables.CWD)

            # upon completing sending of file successfully
            end = time.time()
            msgs.inf()
            msgs.console().print(f"Transfer completed in {end-start} seconds.")
            return 1
        except Exception as e:
            raise e

    def recv_files(self):
        """
        Receives the data that has been sent by the send method.
        Detects if the utf-8 sent is meant for a directory or a file by analyzing the size information provided for the
        utf-8. (-1 for directory, rest for file)
        :return:
        1 - When receives all files successfully
        """
        start = time.time()

        buffer = Buffer.Buffer(self._conn)

        # changing working directory to destination directory
        os.chdir(self._path)

        while True:
            inc_name = buffer.get_utf8()
            if not inc_name:
                break

            file_size = int(buffer.get_utf8())
            inc_name = Path(inc_name)
            if file_size == -1:
                # received info informs about a folder so create folder and receive files under it
                try:
                    os.mkdir(Path(inc_name))
                except:
                    # directory already exists, so do nothing
                    pass
            else:
                
                # file size is not -1 therefore it is a file
                with Progress() as progress:
                    task = progress.add_task(str(inc_name), total=file_size)

                    with open(inc_name, 'wb') as f:
                        remaining = file_size
                        while remaining:
                            chunk_size = 4096 if remaining >= 4096 else remaining
                            chunk = buffer.get_bytes(chunk_size)

                            if not chunk:
                                break

                            f.write(chunk)

                            remaining -= len(chunk)

                            progress.update(task, advance=len(chunk))

                        if remaining:
                            msgs.warn_msg()
                            msgs.console().print('File incomplete.  Missing', remaining, 'bytes.')

        end = time.time()
        msgs.inf()
        msgs.console().print(f"Transfer completed in {end - start} seconds.")
        return 1

    def set_mode(self):
        """
        Sets mode as either sender or receiver depending on user input. However, if the path is detected to be a file,
        then mode is automatically set as sender.
        """
        if os.path.isdir(self._path):
            questions = [
                {
                    'type': 'list',
                    'name': 'mode',
                    'message': 'sender or receiver?',
                    'choices': Reusables.MODE
                }
            ]

            self._mode = prompt(questions)['mode']
        else:
            # File is detected there definitely a sender
            msgs.inf()
            msgs.console().print("File detected. Switching to sender mode.")
            self._mode = Reusables.MODE[0]

    def get_mode(self):
        """
        Used in client side to get mode as sender or receiver based on what the host mode is
        """
        buff = Buffer.Buffer(self._conn)
        self._mode = buff.get_utf8()

    def transfer_handler(self, host=False):
        """
        Handles transferring of files based on where the instance is a sender or receiver.
        In case the instance is a host, then it will also inform the mode to the connected client.
        """
        buff = Buffer.Buffer(self._conn)

        if self._mode == Reusables.MODE[0]:
            # mode is sender
            # inform client to go to receiver mode
            if host:
                buff.put_utf8(Reusables.MODE[1])
            self.send_files()
        else:
            # mode is receiver
            # inform client to go to sender mode
            if host:
                buff.put_utf8(Reusables.MODE[0])
            self.recv_files()
