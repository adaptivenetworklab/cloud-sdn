#  Implementasi Ryu Controller Berbasis Microservice Terhadap Network Slicing dalam Jaringan Multi-Tenant 

## Desain Sistem
Pada penelitian ini akan digunakan Ryu SDN Controller yang sudah berbasis microservice sebagai control multi tenant dari sistem. Setiap subfungsi atau subsistem yang ada pada Ryu SDN Controller yang masih monolitik akan dipecah dan setiap subsistem tersebut akan dijalankan menggunakan Docker container. Kemudian sebagai pengontrol dan pembuat slice pada data plane akan digunakan fitur Flow Space dari Flowvisor Controller. Flowvisor ini juga akan dijalankan sebagai docker container. Topologi akan menyesuaikan dengan skenario uji tes yang akan diujikan nanti. Parameter yang akan diuji adalah delay, throughput, dan packet loss, dengan tools pengukuran loadnya menggunakan Iperf.

## Spesifikasi Testbed
Pada riset ini penelitian yang dilakukan menggunakan 2 Virtual machine (VM) yang akan dibangun di atas Openstack. Sistem operasi yang digunakan adalah Ubuntu 20.04. VM pertama akan diinstal Minikube sebagai container orchestrator, dan VM kedua akan diinstal mininet sebagai simulasi skenario topologi jaringan. 

Attempt | #1 | #2 | #3 | #4 | #5 | #6 | #7 | #8 | #9 | #10 | #11
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |---
Seconds | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269
--- | --- | --- | --- |--- |--- |--- |--- |--- |--- |--- |---
Third | 301 | 283 | 290 | 286 | 289 | 285 | 287 | 287 | 272 | 276 | 269
