import os
import sys
import time
import subprocess
import random
import telnetlib
import json
import signal

vm_count = 0

class VM:
    @staticmethod
    def cleanup():
        pid_files = [f for f in os.listdir(os.getcwd()) if f.endswith('.pid')]
        for f in pid_files:
            with open(f) as pid_file:
                try:
                    pid = int(pid_file.read())
                except:
                    pass
                finally:
                    os.kill(pid, signal.SIGKILL)
            os.remove(f)

    def __init__(self, name=None):
        global vm_count
        vm_count += 1
        if name is None:
            self.name = str(vm_count)
        else:
            self.name = name

        self.qmp_port = random.randint(9000, 9999)
        self.pid_file = f'qemu-{self.qmp_port}.pid'

        if os.path.exists(self.pid_file):
            os.remove(self.pid_file)

        qemu_cmd = 'qemu-system-x86_64'
        qemu_arg = [
            '-snapshot', '-m', '80M',
            '-device', 'virtio-blk-pci,drive=SystemDisk',
            '-drive', 'id=SystemDisk,if=none,format=qcow2,file=disk.qcow2',
            '-chardev',
            f'socket,id=qmp,port={self.qmp_port},host=localhost,server=on',
            '-mon', 'chardev=qmp,mode=control,pretty=on',
            '-nographic', '-serial', 'mon:stdio',
            '-pidfile', self.pid_file
        ]

        print(f"Starting VM {self.name} ...")

        self.proc = subprocess.Popen([qemu_cmd] + qemu_arg,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while True:
            time.sleep(1)

            try:
                self.comm = telnetlib.Telnet('127.0.0.1', self.qmp_port)
            except ConnectionRefusedError:
                continue
            finally:
                break

        self.read_qmp()
        time.sleep(1)

        self.run_command("qmp_capabilities")
        time.sleep(5)

    def __del__(self):
        print(f"Terminating VM {self.name} ...")

        self.proc.terminate()
        time.sleep(1)

        self.comm.close()
        time.sleep(1)

        if os.path.exists(self.pid_file):
            with open(self.pid_file) as pid_file:
                try:
                    pid = int(pid_file.read())
                except:
                    pass
                finally:
                    os.kill(pid, signal.SIGKILL)
            os.remove(self.pid_file)

    def read_qmp(self):
        buffer = ""
        brace_count = 0
        in_string = False
        escape = False
        output = []
        last_offset = 0
        offset = 0

        while True:
            # Read data from the Telnet connection
            data = self.comm.read_some().decode('utf-8')
            buffer += data

            for char in data:
                offset += 1
                if char == '"' and not escape:
                    in_string = not in_string
                elif char == '{' and not in_string:
                    brace_count += 1
                elif char == '}' and not in_string:
                    brace_count -= 1
                    if brace_count == 0:
                        # Parse the JSON data
                        try:
                            json_data = json.loads(buffer[last_offset:offset])
                            last_offset = offset
                            #print(json_data)
                            output.append(json_data)

                        except json.JSONDecodeError as e:
                            print(f"Failed to parse JSON: {e}")
                            return None

                elif char == '\\' and not escape:
                    escape = True
                    continue
                escape = False

            # Check if we have a complete JSON object
            if brace_count == 0 and buffer.strip():
                break

        return output

    def run_command(self, command, arguments=None):
        if arguments is None:
            self.comm.write(('{ "execute": "' + command + '" }').encode('utf-8'))
        else:
            self.comm.write(('{ "execute": "' + command + '", "arguments": ' + json.dumps(arguments) + ' }').encode('utf-8'))
        time.sleep(1)
        return self.read_qmp()

    def read_pmem(self, start, size):
        while True:
            tmp_file = "/tmp/pmemsave-" + str(random.randint(0,9999))
            if not os.path.exists(tmp_file):
                break

        self.run_command("pmemsave", arguments={"val": start, "size": size, "filename": tmp_file})

        mem = open(tmp_file, "rb").read()
        os.remove(tmp_file)
        return mem

    def mem_usage(self):
        nr_free = int.from_bytes(self.read_pmem(0x00952b00, 4), byteorder='little')
        return 80 * 1024 * 1024 - nr_free * 4096
        
