#!/opt/cycle/jetpack/system/embedded/bin/python -m pytest
import os
import subprocess
import tempfile
import time
import uuid


def test_hello_world():
    script_path = os.path.expanduser("~/hello_world.sh")
    job_name = str(uuid.uuid4())
    with open(script_path, 'w') as fw:
        fw.write(
"""#!/bin/bash
#
#SBATCH --job-name=%s
#SBATCH --output=test_hello_world.txt
#
#SBATCH --ntasks=1
srun hostname
srun sleep 60""" % job_name)
    
    subprocess.check_call(["sbatch", script_path])

    deadline = time.time() + 20 * 60
    while time.time() < deadline:
        time.sleep(1)
        stdout = subprocess.check_output(['squeue', '--format', "%j", "-h"])
        if job_name not in stdout:
            return
    raise AssertionError("Timed out waiting for job %s to finish" % job_name)