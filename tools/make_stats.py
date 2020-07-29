import numpy as np
import matplotlib as plt
import argparse
import os
import json
from collections import OrderedDict

#
# Utilities
#


def find_ocurrence(s, pattern, oc):
    pos = -1
    for i in range(0, oc):
        pos = s.find(pattern, pos + 1)
    return pos


def name_machine(machine_folder):
    name = machine_folder[machine_folder.find(".")+1:]
    # Check if dir is relative by .
    if machine_folder.find(".") < machine_folder.find("/"):
        # how many ?
        dots = machine_folder.count(".") - 4  # nam.hostwiththreedots
        name = machine_folder[find_ocurrence(machine_folder, ".", dots + 1)+1:]
    return name


def resort_pps_dict(rates_dict):
    rates = list(rates_dict.keys())
    rates = [int(rate) for rate in rates]
    rates.sort()
    sorted_pps = OrderedDict()
    for rate in rates:
        sorted_pps[str(rate)] = rates_dict[str(rate)]
    return sorted_pps


def plot_series():
    pass

#
# Extraction helpers
#


def recover_cpu_profile(machine_folders):
    machine_cpu = dict()

    for machine_f in machine_folders:
        name = name_machine(machine_f)
        machine_cpu[name] = dict()
        measurements = os.listdir(machine_f)
        for data in measurements:
            with open(machine_f+"/"+data) as f:
                lines = f.readlines()
                # names like cpu-hostsip-pps.log
                # CPU like %usr %nice %sys %iowait %irq
                pps = data[find_ocurrence(data, "-", 2)+1:data.find(".log")]
                machine_cpu[name][pps] = lines[0].strip()
            # Resort
            machine_cpu[name] = resort_pps_dict(machine_cpu[name])
    return machine_cpu


def recover_mem_profile(machine_folders):
    # It uses full paths
    # Per machine do profile capture
    machine_mems = dict()
    for machine_f in machine_folders:
        name = name_machine(machine_f)
        machine_mems[name] = dict()
        measurements = os.listdir(machine_f)
        for data in measurements:
            with open(machine_f+"/"+data) as f:
                lines = f.readlines()
                # names like cpu-hostsip-pps.log
                pps = data[find_ocurrence(data, "-", 2)+1:data.find(".log")]
                # Data like RAM SWAP
                machine_mems[name][pps] = lines[0].strip()+" "+lines[1].strip()
            # Sort and replace
            machine_mems[name] = resort_pps_dict(machine_mems[name])

    return machine_mems


def recover_servers_net(machine_folders):
    machine_net = dict()
    for machine_f in machine_folders:
        name = name_machine(machine_f)
        machine_net[name] = dict()
        measurements = os.listdir(machine_f)
        for data in measurements:
            with open(machine_f+"/"+data) as f:
                lines = f.readlines()
                pps = data[data.find("-")+1:find_ocurrence(data, "-", 2)]
                #  %answered query_rate query_avglen reply_rate reply_avglen
                machine_net[name][pps] = lines[0].strip()
            # Sort rates
            machine_net[name] = resort_pps_dict(machine_net[name])

    return machine_net


def recover_observer_net(file):

    packets = dict()

    def recover_stats(position, limit, data, results, pps, name):
        # Find stats position
        stats_pos = -1
        read_interval_cnt = 0
        for i in range(position, limit):
            if "Interval" in data[i]:
                read_interval_cnt = read_interval_cnt + 1
            if read_interval_cnt == 2:
                stats_pos = i
                read_interval_cnt = 0
                break
        # Read interval values
        new_position = stats_pos + 2  # line after second interval is ignored
        results[pps][name] = dict()
        results[pps][name]["interval"] = []
        results[pps][name]["total"] = []
        results[pps][name]["machine1"] = []
        results[pps][name]["machine2"] = []
        results[pps][name]["machine3"] = []
        for i in range(new_position, limit):
            if "======" in data[i]:
                new_position = i
                break
            values = data[i].strip()[1:len(data[i])-1].split("|")
            interval_length = values[0].strip().replace("<>", "").split("  ")
            interval_length = float(
                interval_length[1])-float(interval_length[0])
            results[pps][name]["interval"].append(interval_length)
            results[pps][name]["total"].append(int(values[3].strip()))
            results[pps][name]["machine1"].append(int(values[5].strip()))
            results[pps][name]["machine2"].append(int(values[7].strip()))
            results[pps][name]["machine3"].append(int(values[9].strip()))

        return new_position

    with open(file) as f:
        lines = f.readlines()
        # Loop control
        cnt = 0
        total = len(lines)
        # Check control
        read_pps = False
        # Naming vars
        pps_value = ""

        while cnt < total:
            # Find our packets per second speed tag
            if "pps" in lines[cnt]:
                pps_value = lines[cnt][lines[cnt].find(
                    " "):lines[cnt].find("pps")]
                read_pps = True
                packets[pps_value] = dict()
            # Look for stats based on tag
            if read_pps:
                cnt = recover_stats(cnt, total, lines,
                                    packets, pps_value, "sent")
                cnt = recover_stats(cnt, total, lines,
                                    packets, pps_value, "recv")
                read_pps = False
            # Move forward
            cnt = cnt + 1

    return packets

#
# Tests recovery function
#


def get_mem_usage(dirs, outDir):
    """
    Write mem usage per zones as csv
    server, ram, swap
    """
    rand = [d for d in dirs if "random" in d][0]
    real = [d for d in dirs if "real" in d][0]

    def read_and_split(parent, rep):
        files = os.listdir(parent)
        res = dict()
        for name in files:
            server = name.replace(
                "mem-usage-", "").replace(".log", "").replace(rep, "")
            res[server] = dict()
            with open(parent+"/"+name) as f:
                result = f.readlines()
                values = result[0].strip().split(" ")
                res[server]["ram"] = values[1]
                res[server]["swap"] = values[3]
        return res

    def write_csv(name, stats):

        servers = list(stats.keys())
        servers.sort()

        with open(name, "w") as f:
            f.write("{},{},{}\n".format("server", "ram", "swap"))
            for i in range(len(servers)):
                f.write("{},{},{}\n".format(
                    servers[i], stats[servers[i]]["ram"], stats[servers[i]]["swap"]))

    # Make series for both
    write_csv(outDir+"/random-usage.csv", read_and_split(rand, "random"))
    write_csv(outDir+"/real-usage.csv", read_and_split(real, "real"))

    return [outDir+"/random-usage.csv", outDir+"/real-usage.csv"]


def get_server_times(dirs, outDir):
    """
    Gather the response time stats from all servers
    """
    rand = [d for d in dirs if "random" in d]
    real = [d for d in dirs if "real" in d]

    def read_and_split(folders):
        # For each server get stats file
        servers = []
        average = []
        std = []
        median = []
        variance = []
        for folder in folders:
            servers.append(folder[folder.find("times")+6:])
            files = os.listdir(folder)
            for name in files:
                if "stats" in name:
                    with open(folder+"/"+name) as f:
                        lines = f.readlines()
                        median.append(lines[0].split(" ")[1])
                        average.append(lines[1].split(" ")[1])
                        std.append(lines[2].split(" ")[1])
                        variance.append(lines[3].split(" ")[1])
        return servers, average, std, median, variance

    def write_csv(name, s, avg, std, med, var):
        with open(name, "w") as f:
            f.write("{},{},{},{},{}\n".format("server", "avg (ms)",
                                              "std (ms)", "median (ms)", "var (ms)"))
            for i in range(len(s)):
                f.write("{},{},{},{},{}\n".format(
                    s[i], avg[i], std[i], med[i], var[i]))

    ra_s, ra_avg, ra_std, ra_median, ra_var = read_and_split(rand)
    re_s, re_avg, re_std, re_median, re_var = read_and_split(real)

    write_csv(outDir+"/random-times.csv", ra_s,
              ra_avg, ra_std, ra_median, ra_var)
    write_csv(outDir+"/real-times.csv", re_s,
              re_avg, re_std, re_median, re_var)

    return [outDir+"/random-times.csv", outDir+"/real-times.csv"]


def get_response_stats(dirs, outDir, name="response"):
    """
    Recover evolution of cpu and memory usage, response rate and observed response rate
    """
    rand = [d for d in dirs if "random" in d]
    real = [d for d in dirs if "real" in d]

    def make_stats_per_server(server, test_name):
        stats = dict()
        # Server like etcd, bind, knot
        for server_f in server:
            server_name = server_f[server_f.find(test_name+"-")+9:]
            stats[server_name] = dict()
            sub_f = os.listdir(server_f)
            cpus_f = []
            responses_f = []
            mem_f = []
            observer = ""
            # Group sub folders
            # folders like mem, cpu ...
            for f in sub_f:
                path = server_f+"/"+f
                if "cpu" in f:
                    cpus_f.append(path)
                elif "mem" in f:
                    mem_f.append(path)
                elif "wireshark" in f:
                    observer = path
                else:
                    responses_f.append(path)
            # Do specific test for each
            memory_evolution = recover_mem_profile(mem_f)
            cpu_evolution = recover_cpu_profile(cpus_f)
            net_evolution = recover_servers_net(responses_f)
            observations = recover_observer_net(observer)

            # Save
            stats[server_name]["mem"] = memory_evolution
            stats[server_name]["cpu"] = cpu_evolution
            stats[server_name]["net"] = net_evolution
            stats[server_name]["wireshark"] = observations

        return stats

    def unpack_and_save(stats, parent_dir, file_name_suffix):
        run_one = True
        # Check each server
        for server in stats.keys():
            if run_one:
                op_mode = "w"
            else:
                op_mode = "a"
            # Save mem evolution stats
            mem = stats[server]["mem"]
            with open(parent_dir+"/mem-evolution-"+file_name_suffix+".csv", op_mode) as f:
                if run_one:
                    f.write("server,machine,pps,ram,swap\n")
                for machine in mem.keys():
                    rates = mem[machine]
                    for pps in rates:
                        values = rates[pps].replace(" ", ",")
                        f.write("{},{},{},{}\n".format(
                            server, machine, pps, values))
            # Save cpu evolution
            cpu = stats[server]["cpu"]
            with open(parent_dir+"/cpu-evolution-"+file_name_suffix+".csv", op_mode) as f:
                if run_one:
                    f.write("server,machine,pps,usr,nice,sys,iowait,irq\n")
                for machine in cpu.keys():
                    rates = cpu[machine]
                    for pps in rates:
                        values = rates[pps].replace(" ", ",")
                        f.write("{},{},{},{}\n".format(
                            server, machine, pps, values))
            # Save network stats
            dev_net = stats[server]["net"]
            with open(parent_dir+"/responses-evolution-"+file_name_suffix+".csv", op_mode) as f:
                if run_one:
                    f.write(
                        "server,machine,pps,answered,query rate,query avg len,reply rate,reply avg len\n")
                for machine in dev_net.keys():
                    rates = dev_net[machine]
                    for pps in rates:
                        values = rates[pps].replace(" ", ",")
                        f.write("{},{},{},{}\n".format(
                            server, machine, pps, values))
            # Save wireshark stats
            wireshark = stats[server]["wireshark"]
            with open(parent_dir+"/throughput-evolution-"+file_name_suffix+".csv", op_mode) as f:
                if run_one:
                    f.write(
                        "target server,operation,pps,timespan,total packets,machine 1,machine 2,machine 3\n")
                rates = wireshark.keys()
                operations = ["sent", "recv"]
                for op in operations:
                    for pps in rates:
                        entries = len(wireshark[pps][op]["interval"])
                        # Make a resume of instances
                        timespan = 0.0
                        packets = 0
                        m1 = 0
                        m2 = 0
                        m3 = 0
                        for i in range(entries):
                            timespan = timespan + \
                                wireshark[pps][op]["interval"][i]
                            packets = packets + wireshark[pps][op]["total"][i]
                            m1 = m1 + wireshark[pps][op]["machine1"][i]
                            m2 = m2 + wireshark[pps][op]["machine2"][i]
                            m3 = m3 + wireshark[pps][op]["machine3"][i]
                        f.write("{},{},{},{},{},{},{},{}\n".format(
                            server, op, pps, timespan, packets, m1, m2, m3))
            run_one = False
        return [parent_dir+"/mem-evolution-"+file_name_suffix+".csv", parent_dir+"/cpu-evolution-"+file_name_suffix+".csv", parent_dir+"/responses-evolution-"+file_name_suffix+".csv", parent_dir+"/throughput-evolution-"+file_name_suffix+".csv"]

    random_csv = unpack_and_save(make_stats_per_server(
        rand, name), outDir, "random-"+name)
    real_csv = unpack_and_save(make_stats_per_server(
        real, name), outDir, "real-"+name)

    return random_csv, real_csv


def get_backend_resistance(dirs, outDir):
    """
    Under a controlled failure recover evolution of cpu and memory usage, response rate and observed response rate
    """
    return get_response_stats(dirs, outDir, "segfault")

#
# Plot helpers
#

def plot_mem_usage(files):
  pass

def main(resultsDir, outDir):
    # Look for folders
    folders = os.listdir(resultsDir)

    # There are two, real and flat (random) distributions
    # We take both dirs
    mem_dir = []
    response_dir = []
    times_dir = []
    segfault_dir = []

    for f in folders:
        path = resultsDir+"/"+f
        if "response" in f:
            response_dir.append(path)
        elif "times" in f:
            times_dir.append(path)
        elif "segfault" in f:
            segfault_dir.append(path)
        elif "mem" in f:
            mem_dir.append(path)

    # Make dirs
    if not os.path.exists(outDir + "/mem-usage"):
        os.makedirs(outDir + "/mem-usage")
    if not os.path.exists(outDir + "/time-response"):
        os.makedirs(outDir + "/time-response")
    if not os.path.exists(outDir + "/response-stats"):
        os.makedirs(outDir + "/response-stats")
    if not os.path.exists(outDir + "/segfault-stats"):
        os.makedirs(outDir + "/segfault-stats")

    # Compute for each group
    mem_usage = get_mem_usage(mem_dir, outDir + "/mem-usage")
    server_times = get_server_times(times_dir, outDir + "/time-response")
    random_res, real_res = get_response_stats(
        response_dir, outDir + "/response-stats")
    random_segfault, real_segfault = get_backend_resistance(
        segfault_dir, outDir + "/segfault-stats")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Make stats from results after a tests is complete. The results will be some charts and csv files for ease of use.")
    parser.add_argument("directory", type=str,
                        help="Directory containing the results")
    parser.add_argument("outputdir", type=str,
                        help="Where to put the computed stats", default="../stats")
    args = parser.parse_args()
    main(args.directory, args.outputdir)
