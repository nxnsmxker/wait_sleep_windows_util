import subprocess, os, time, asyncio
needed_modules = open("needed_modules_list.txt","w+")
needed_modules.writelines(["pip install subprocess\n","pip install os\n", "pip install time\n", "pip install asyncio\n"])
needed_modules.close()

hrs_min_sec = str(
     input("input time in hours,minutes,seconds\n\tformat: 1:5:40\n")
).split(":")
t = int(hrs_min_sec[0]) * 3600
t += int(hrs_min_sec[1]) * 60
t += int(hrs_min_sec[2])

silent_work = open("silent_work.pyw","w+")
silent_work.writelines(r'''import os, time, asyncio

async def output(sleep, text):
    await asyncio.sleep(sleep)
    print(text, end = "\r")

async def work():
    for time_left in range('''+str(t)+''', 0, -1):
        await output(1, f"time left: {time_left} s")


asyncio.run(work())
os.system(r"rundll32.exe powrprof.dll,SetSuspendState Standby")
''')

silent_work.close()

subprocess.Popen(['pythonw', 'silent_work.pyw'])
