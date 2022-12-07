# Flowvisor

FlowVisor is a fairly heavy piece of software in its' current implementation and these system requirements should not be taken too lightly - the number of slices, size of the flowspace, and number of datapaths present in your network all contribute to the scaling factors.

# FVCTL
The fvctl program is a command line tool for configuring, debugging, monitoring, and administering running FlowVisor instances. It is able to show the current state of a FlowVisor, including features, configuration, and flowspace entries.

1. How does FlowVisor slice ARP?
The way the flowvisor handles arps is that it takes an arp request "who has $ip? tell $mac" and sends that to the slice that has flowspace for nw_dst=$ip.

2. Why does my controller get errors when it tries to flood an ARP?
If your controller sends a flowmod without Layer 3 information, FV gives you an error, because if it installed that flowmod, the switch would match all ARPs. If your controller's flowmod includes L3 information, FV will pass along the flowmod as you expect. The NOX pyswitch controller, in particular, is known not to do this, and thus won't work with FlowVisor's ARP slicing.

3. When I start FV, I don't get any errors on the terminal, but it doesn't start up.
Check /var/log/flowvisor/flowvisor-stderr.log, which is where FV logs startup errors (until it comes up enough to start using syslog).

4. Why am I getting a null pointer exception when I start FV?
One possibility is if FV died badly, and left the database with a stale lock file. If you're 100% sure that FV isn't running, check in /usr/local/share/db; if you see a db.lck or dbex.lck file, you can safely remove this (but ONLY if FV is really NOT running).

5. Why am I getting a "java.lang.Error: Failed to create temporary file for jnidispatch library: java.i" error when I start FV?
This can happen if /tmp/jna is owned by a user other than 'flowvisor' (typically root). If the directory is empty, it should be safe to remove it.

6. Can I run flowvisor as root or another user?
True through flowvisor 0.8.5 The flowvisor startup script (default: /etc/init.d/flowvisor) sets a variable FV_USER=flowvisor. The flowvisor program expects this user to exist AND be in the sudoers file. (default: /etc/sudoers)
As of 0.8.6 You may start FlowVisor as root (at your own risk) by setting the environment variable FV_RUN_AS_ROOT to 'yes'.

7. How do I backup my FlowVisor config and (re)load it?
You can dump the flowvisor config at any time from a running config by running (this is the recommended approach):
 ```bash
 $ fvctl dumpConfig config.json
 ```
 Alternatively, you can simply backup the internal database by copying it:
 ```bash
 $ cp <path_to_db>/FlowVisorDB <safe_backup_place>
 ```
 To reload flowvisor, you an either:
```bash
 $ fvconfig load config.json or copy the database back to its installed location.
```

8. I updated to 0.10 and I am getting a warning when FlowVisor starts up?


If the warning is of the form:

WARN: Table/View 'FSRQUEUE' already exists in Schema 'APP'.

Then this is normal, FlowVisor is updating the database structure to better serve you ;).

### Slice Limits

Define resource limits per slice. The configuration will be stored in the db, in a key value table associated to each slice.

#### Limit Types

1. Number of flow entries per slice per dpid - requires flow tracking, even if rudimentary. Basically this needs a mechanism for counting the current number of flows installed at the switch by this slice. Should the sum of all flow entries at one dpid be summed? It would let fv know when a particular dpid is about to barf.
Bandwidth - requires queue support. The idea being that a slice will have a queue attached to it which is unknown to the slice controller. ie. Controller emits flow mod, output we change it to flow mod, enqueue.

2. Table access (1.1) - requires 1.1 support multiple tables support. This is pretty straight forward but may have to wait a while.

3. Control channel rate - requires some rate limiting support at the switch end. Problem is here, how does fv set this up at the switch.

4. Set of priorities slice has access to - assigns a certain set of priorities to a slice, these priorities would be mapped to the priorities pushed in a flow mod from a controller. This is a poor man''s virtualized priorities.

5. Limit flow timeout values - FV should handle flow timeout. Possibly by re-writing them to some (small-ish) value and reinstalling flowmod for the time the controller expects the flow to be installed.

![Alt text](https://img1.sdnlab.com/wp-content/uploads/2014/11/02-flowvisor%E5%B7%A5%E4%BD%9C%E5%8E%9F%E7%90%86.png =300x300)

##### Notes
- All connections (to switches and controllers) are handled through a single poll loop
- Switches are handed off to an FVClassifier instance per switch once they make a connection to FlowVisor
- For each switch, FlowVisor internally creates an FVSlicer instance for each slice (making for Switch x Slice number of FVSlicer instances in the FlowVisor process)

# Mempelajari Flowvisor
Flowvisor adalah controller OpenFlow yang bertindak sebagai sebuah hypervisor/proxy antara switch dan multiple controllers. Dapat men-slice multiple switch secara paralel dan melakukan slicing network secara efektif.

Flowvisor membuat beraneka ragam “slices” dari network resource dan memberikan kontrol terhadap setiap slice ke controller yang berbeda-beda. Slice dapat didefinisi sebagai kombinasi dari port switch (layer 1), src/dst ethernet address or type (layer 2), src/dst IP address or type (layer 3), dan src/dst TCP/UDP port or ICMP code/type (layer 4).

# Input/Output (I/O) Logic
Flowvisor memiliki dua logical structure untuk input dan output-nya, yaitu classifier (org.flowvisor.classifier.FVClassifier.java) dan slicer (org.flowvisor.slicerFVSlicer.java).

**Classifier** berfungsi untuk mencari tahu apa yang harus dilakukan terhadap OpenFlow messages yang dikirim ke switch atau berasal dari switch (ke arah dataplane).

**Slicer** berfungsi untuk mencari tahu apa yang harus dilakukan terhadap messages yang dikirim ke controller atau berasal dari controller (ke arah control plane).

Kedua kelas logical structure di atas sama-sama memiliki method sendMsg() dan handleIOEvent(). Berikut penjelasan dari kedua method tersebut:
- **handleIOEvent()**
Method ini akan terpancing (triggered) ketika suatu message diterima dari controller (pada FVSlicer) atau dari switch (pada FVClassifier) sebelum FlowVIsor melakukan penulisan ulang (rewriting). Message yang diterima disini merupakan message mentah dari wire.
- **sendMsg()**
Method ini digunakan untuk mengirim suatu message ke controller (pada FVSlicer) atau ke switch (pada FVClassifier) setelah segala jenis penulisan ulang (rewriting) dilakukan. Pesan yang akan dikirim adalah pesan pasca-proses (yang sudah diproses) yang akan dikirim kembali ke wire.

# Message Source Code Layout

Semua logika pemrosesan message disimpan di dalam org.flowvisor.messages.*
Setiap message mengimplementasikan interface Classifiable dan Sliceable.

Berikut penjelasan dari interface tersebut:
- Classifiable

Memaksa semua kelas message untuk memiliki method classifyFromSwitch(FVClassifier fvClassifier) yang digunakan untuk mengetahui slice tujuan dari message yang datang dari switch.

- Sliceable

Memaksa semua kelas message untuk memiliki method sliceFromController(FVClassifier fvClassifier, FVSlicer fvSlicer). Ketika flowvisor menerima message dari controller dan ingin meneruskannya ke switch yang tepat, method ini digunakan untuk menentukan message-level rewriting berdasarkan kebijakan (policy) slicing untuk menjamin isolasi. Method ini juga menggunakan dua parameter, yaitu:
- FVClassifier fvClassifier
Untuk menentukan tujuan potensial dari message tersebut.
- FVSlicer fvSlicer
Untuk mendapatkan kebijakan slicing dan source dari message tersebut.

# ComNet sEmu

ComNetsEmu is a testbed and network emulator designed for the NFV/SDN teaching book "Computing in Communication Networks: From Theory to Practice". The design focuses on emulating all examples and applications on a single computer, for example on a laptop. ComNetsEmu extends the famous Mininet network emulator to support better emulation of versatile Computing In The Network (COIN) applications. It extends and puts forward the concepts and work in the Containernet project. It uses a slightly different approach to extend the Mininet compared to Containernet. It's main focus is to use "sibling containers" to emulate network systems with computing.

Common facts about ComNetsEmu:

- Emulation accuracy is highly considered, but it can not be guaranteed for arbitrary topology. All emulated nodes (processes) share the same underlying compute, storage and network resources when running it on a single system. ComNetsEmu is heavier than vanilla Mininet due to stricter node isolation. Choosing reasonable emulation parameters is required for correct simulation results. RT-Tests is installed on the test VM. RT-Tests can be used to evaluate the real-time performance of the current emulation system.

- ComNetsEmu is mainly developed with Python3.8. To reduce the complexity of dependencies (third-party packages, frameworks etc.), ComNetsEmu tries to leverage as much of the powerful Python standard library as possible, and prefers simple third-party dependencies when necessary.

- Examples and applications in this repository are mainly developed with high-level script language for simplicity. These programs are not performance optimized. Please contact us if you want highly optimized implementation of the concepts introduced in this book. For example, we had a DPDK-accelerated version of the low-latency (sub-millisecond) Random Linear Network Coding (RLNC) network function.

#### Main Features
- Use Docker hosts in Mininet topologies.

- Manage application Docker containers deployed inside Docker hosts. "Docker-in-Docker" (sibling containers) is used as a lightweight emulation of nested virtualization. A Docker host with multiple internal Docker containers deployed is used to mimic an actual physical host running Docker containers (application containers).

- A collection of application examples for "Computing In Communication Networks" with sample codes and detailed documentation. All examples can be easily reproduced and extended.


### Comparison With Mininet
Check the homepage of Mininet for this great network emulator. One main difference of this extension is: ComNetsEmu allows developer to deploy Docker containers INSIDE Mininet's hosts (Instead of Mininet's default Host or CPULimitedHost, ComNetsEmu uses Docker containers for hosts), which is beneficial to emulate many practical compute and network setups. By default all Mininet's hosts share the host file system and PID space. And it is non-trivial to let the application containers to share the networking stack of the Mininet's host. So in ComNetsEmu, the Mininet's hosts are also Docker containers. New (heavyweight but more isolated/practical) host/node types are also listed as potential enhancements to Mininet in Mininet's official hackathon. ComNetsEmu aims at adding essential features/enhancements to Mininet for better emulations for SDN/NFV applications.

A simple example is given with a for the emulation scenario: Assume Alice wants to send packets to Bob with random linear network coding. Packet has to be transmitted through two switches S1 and S2. Link losses (It is not true in the wired domain, however, we just want to simulate the channel losses, packets are dropped in the queue of the switch manually.) exit in each link on the data plane. In order to mitigate the channel losses, the recoding should be performed. According to the Service Function Chain proposed in RFC 7665, instead of directly forwarding packets to S2, the S1 can redirect the packets to a host on which multiple network functions are running. Recoding can be deployed as a virtualized network function (VNF) on NF1 or NF2 based on the channel loss rates. The recoding VNF can also migrate between NF1 and NF2 and be adaptive to the dynamics of the channel loss rates. For teaching purpose, we want the students can emulate all practical and real-world scenarios on NFV/SDN deployment on a single laptop. It should be as lightweight as possible. So in our Testbed, the physical machines (Alice, Bob, NFs) are emulated with Mininet Hosts. They have long-and-alive PIPEs open (stdin, stdout and stderr) that can be used by the Mininet manager to e.g. run arbitrary commands during the emulation. The VNFs or cloud applications are encapsulated in Docker containers and deployed inside each Mininet Host. In order to emulate this, the application containers (a.k.a internal containers) should be isolated: It should inherent from the resource isolation of corresponded Mininet Host and also inherent the network namespace of its Mininet Host. This is currently not supported in the Mininet's default host, therefore ComNetsEmu replaces it with Docker host (by integrating codes from Containernet) to have a "Docker-In-Docker" (sibling containers) setup. This approach is inspired by the design of Pod in the de-facto standard container orchestration platform Kubernetes.






