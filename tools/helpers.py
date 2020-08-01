import numpy as np
import matplotlib as plt
import pandas as pd
    
def make_mem_usage(file, title):
    mem = pd.read_csv(file)
    mem['total'] = mem['ram']+mem['swap']
    servers = ['bind','knot','nsd','etcd','redis','cassandra']
    dfs = dict()
    # Subsample dataset
    for server in servers:
        dfs[server] = mem[mem['server'].str.contains(server)]
    # Compute the averages and put them toghether
    rams = []
    swaps = []
    names = []
    total = []
    for server in servers:
        df = dfs[server]
        rams.append(df['ram'].mean())
        swaps.append(df['swap'].mean())
        total.append(df['ram'].mean() + df['swap'].mean())
        names.append(server)

    averages = pd.DataFrame({"server":names,"ram":rams,"swap":swaps,"total":total})

    ax = averages.plot(kind='bar',rot=75, xlabel="Server", ylabel="Memory in MBs", title=title)
    ax.set_xticklabels(averages.server)
    return ax
    
def load_and_plot(file,title):
    df = pd.read_csv(file)
    ax = df['avg (ms)'].plot(kind='bar',rot=75, xlabel="Server", ylabel="Reponse time in ms", title=title, yerr=df['std (ms)'])
    ax.set_xticklabels(df.server)
    return ax

def aux(file,title):
    df = pd.read_csv(file)
    df = df.drop(index=df[df["server"] == "etcd"].index)
    ax = df['avg (ms)'].plot(kind='bar',rot=75, xlabel="Server", ylabel="Reponse time in ms", title=title, yerr=df['std (ms)'])
    ax.set_xticklabels(df.server)
    df = pd.read_csv(file)
    etcd = df[df["server"] == "etcd"]
    print("ETCD has {} ms of avg response time with {} ms of standard deviation\n".format(etcd.iloc[0]["avg (ms)"], etcd.iloc[0]["std (ms)"]))
    return ax