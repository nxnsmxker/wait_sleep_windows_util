import os, re, psutil, asyncio, subprocess


needed_modules = open("needed_modules_list.txt","w+")
needed_modules.writelines(["pip install re\n","pip install os\n", "pip install asyncio\n", "pip install psutil\n", "pip install subprocess\n"])
needed_modules.close()


def main():
    process_list = " ".join(
        os.popen("wmic process get description, processid").read().split()[2:]
    )
    process_list_beautiful = []
    process_list_beautiful = list(
        set([x.strip() for x in re.split(r"\d+", process_list)])
    )
    print(process_list_beautiful)

    process_name = input("copy & paste process_name from above:\n")
    processes_pids = [
        p.info
        for p in psutil.process_iter(attrs=["pid", "name"])
        if process_name in p.info["name"]
    ]
    if len(processes_pids) == 0:
        process_name = input(
            "Could not find such process\n" + "copy & paste process_name from above:\n"
        )
        processes_pids = [
            p.info
            for p in psutil.process_iter(attrs=["pid", "name"])
            if process_name in p.info["name"]
        ]
    i = 0
    for process_pid in processes_pids:
        print(i, end="\t")
        print(process_pid, end="\n")
        i += 1

    input_pid = input("input process number or A if all the ids are correct:\n").strip()

    if input_pid == "A":
        input_pid = 0
    
    work_proc_silent = open("work_proc_silent.pyw","w+")
    work_proc_silent.writelines(f'''import os, psutil, asyncio, sys
async def stop_fucker(pid):
    pids_all = [p.info for p in psutil.process_iter(attrs=["name"])]
    pids_all = [p["name"] for p in pids_all]
    while str(pid) in pids_all:
        pids_all = [p.info for p in psutil.process_iter(attrs=["name"])]
        pids_all = [p["name"] for p in pids_all]
        await asyncio.sleep(100)
    os.system(r"rundll32.exe powrprof.dll,SetSuspendState Standby")

asyncio.run(stop_fucker("{processes_pids[int(input_pid)]['name']}"))
sys.exit()''')
    work_proc_silent.close()

main()
subprocess.Popen(['pythonw', 'work_proc_silent.pyw'])
