import sys
import socket
import struct
import subprocess
import ipaddress


def numberToNetmask(number):
    if int(number) < 1 or int(number) > 32:
        print("Wrong mask number")
        sys.exit()
    host_bits = 32 - int(number)
    netmask = socket.inet_ntoa(struct.pack('!I', (1 << 32) - (1 << host_bits)))
    return netmask


def get_subnet_mask(ip):
    config = subprocess.Popen('ipconfig', stdout=subprocess.PIPE)
    while True:
        line = config.stdout.readline()
        if ip.encode() in line:
            break
    mask = config.stdout.readline().split(b':')[-1].replace(b' ', b'').decode()
    return mask


def numbersToBin(tab):
    i = 0
    try:
        for number in tab:
            tab[i] = int(number)
            i += 1
    except ValueError:
        print("Value Error")
        sys.exit()

    tabBin = [0, 0, 0, 0]
    i = 0
    for x in tab:
        tabBin[i] = bin(x)[2:].zfill(8)
        i += 1
    return tabBin


def ipcheck(ip):
    i = 0
    try:
        for number in ip:
            ip[i] = int(number)
            i += 1
    except ValueError:
        print("Value Error")
        file.write("Value Error")
        file.close()
        sys.exit()
    if len(ip) != 4:
        print("Wrong lenght's address")
        file.write("Wrong lenght's address")
        file.close()
        sys.exit()
    for x in ip:
        if x < 0 or x > 255:
            print("Wrong ip address")
            file.write("Wrong ip address")
            file.close()
            sys.exit()


def ipclass(ip):
    x = int(ip[0])
    if x >= 1 and x < 128:
        return "A"
    elif x < 192:
        return "B"
    elif x < 224:
        return "C"
    elif x < 240:
        return "D"
    elif x <= 255:
        return "E"


def subnet(ipdz, maskdz):
    host = ipaddress.IPv4Address(ipdz)
    mask = ipaddress.IPv4Address(maskdz)
    return ipaddress.IPv4Address(int(host) & int(mask))


def publicOrPrivate(ip):
    if (ip[0] == 10 or (ip[0] == 172 and '16' <= ip[1] <= '31') or (ip[0] == 192 and ip[1] == 168)):
        return ("Private")
    else:
        return ("Public")


def combineTabToString(tab):
    res = ""
    i = 1
    for x in tab:
        res += x
        if i < 4:
            i += 1
            res += "."
    return res


def splittingToSingleNumbers(tab):
    tab_list = []
    for j in range(0, len(tab)):
        for i in range(0, len(tab[j])):
            tab_list.append(tab[j][i])
            i += 1
        j += 1
    return tab_list


def combingToBinary(list):
    tab = ["", "", "", ""]
    for j in range(0, 8):
        tab[0] += str(list[j])
    for j in range(8, 16):
        tab[1] += str(list[j])
    for j in range(16, 24):
        tab[2] += str(list[j])
    for j in range(24, 32):
        tab[3] += str(list[j])
    return tab


def binaryToDecimal(tab):
    dec = str(int(tab[0], 2)) + "." + str(int(tab[1], 2)) + "." + str(int(tab[2], 2)) + "." + str(int(tab[3], 2))
    return dec;


file = open("result.txt", "w")
# ----------------------------------------------------------------------------------------DATA-INPUT
inputX = ['', '']
if (len(sys.argv) == 1):
    hostname = socket.gethostname()
    inputX[0] = socket.gethostbyname(hostname)
    ipDec = inputX[0]
    inputX[1] = get_subnet_mask(inputX[0])[:-2]
    maskDec = inputX[1]
    maskNumber = sum([bin(int(x)).count('1') for x in maskDec.split('.')])
    inputX[1] = str(maskNumber)
else:
    inputX = str(sys.argv[1])
    inputX = inputX.split("/")
    ipDec = inputX[0]
    maskNumber = inputX[1]
    maskDec = numberToNetmask(maskNumber)
print("\nInput:", str(inputX[0] + "/" + inputX[1]))
file.write("Input: " + str(inputX[0] + "/" + inputX[1]) + "\n")

# ----------------------------------------------------------------------------------------IP
ip = ipDec.split(".")
ipcheck(ip)
ipBin = numbersToBin(ip)
print("\nIP decimal:", ipDec)
file.write("\nIP decimal: " + str(ipDec) + "\n")
print("IP binary:", combineTabToString(ipBin))
file.write("IP binary: " + str(combineTabToString(ipBin)) + "\n")

# ----------------------------------------------------------------------------------------MASK
maskBin = numbersToBin(maskDec.split("."))
print("\nMask number:", maskNumber)
file.write("\nMask number: " + str(maskNumber) + "\n")
print("Mask decimal:", maskDec)
file.write("Mask decimal: " + str(maskDec) + "\n")
print("Mask binary:", combineTabToString(maskBin))
file.write("Mask binary: " + str(combineTabToString(maskBin)) + "\n")

# -----------------------------------------=-----------------------------------------------HOST-BITS
maskSingle = splittingToSingleNumbers(maskBin)
numberOfHostBits = 32
for x in maskSingle:
    if x == "1":
        numberOfHostBits -= 1
    else:
        break
print("Number of host's bits:", numberOfHostBits)
file.write("Number of host's bits: " + str(numberOfHostBits) + "\n")

# ----------------------------------------------------------------------------------------NET
netDec = str(subnet(ipDec, maskDec))
netBin = numbersToBin(netDec.split("."))
print("\nNetwork decimal:", netDec)
file.write("\nNetwork decimal: " + str(netDec) + "\n")
print("Network binary:", combineTabToString(netBin))
file.write("Network binary: " + str(combineTabToString(netBin)) + "\n")
print("Network class:", ipclass(ip))
file.write("Network class: " + str(ipclass(ip)) + "\n")
print("Network type:", publicOrPrivate(ip))
file.write("Network type: " + str(publicOrPrivate(ip)) + "\n")

# ----------------------------------------------------------------------------------------BROADCAST
broadcastDec = str(ipaddress.IPv4Network(ipDec + '/' + maskDec, False).broadcast_address)
broadcastBin = numbersToBin(broadcastDec.split("."))
print("\nBroadcast decimal:", broadcastDec)
file.write("\nBroadcast decimal: " + str(broadcastDec) + "\n")
print("Broadcast binary:", combineTabToString(broadcastBin))
file.write("Broadcast binary: " + str(combineTabToString(broadcastBin)) + "\n")

# ----------------------------------------------------------------------------------------FIRST-HOST
firstHostSingle = splittingToSingleNumbers(netBin)
i = -1
while firstHostSingle[i] == 1 and i <= -numberOfHostBits:
    firstHostSingle[i] = 0
    i -= 1
firstHostSingle[i] = 1
firstHostBin = combingToBinary(firstHostSingle)
firstHostDec = binaryToDecimal(firstHostBin)
print("\nFirst host decimal:", firstHostDec)
file.write("\nFirst host decimal: " + str(firstHostDec) + "\n")
print("First host binary:", combineTabToString(firstHostBin))
file.write("First host binary: " + str(combineTabToString(firstHostBin)) + "\n")

# ----------------------------------------------------------------------------------------LAST-HOST
lastHostSingle = splittingToSingleNumbers(broadcastBin)
i = -1
while lastHostSingle[i] == 0 and i <= -numberOfHostBits:
    lastHostSingle[i] = 1
    i -= 1
lastHostSingle[i] = 0
lastHostBin = combingToBinary(lastHostSingle)
lastHostDec = binaryToDecimal(lastHostBin)
print("\nLast host decimal:", lastHostDec)
file.write("\nLast host decimal: " + str(lastHostDec) + "\n")
print("Last host binary:", combineTabToString(lastHostBin))
file.write("Last host binary: " + str(combineTabToString(lastHostBin)) + "\n")

# ----------------------------------------------------------------------------------------MAX-HOSTS
maxHosts = 2 ** numberOfHostBits - 2
print("\nMaximum number of hosts:", maxHosts)
file.write("\nMaximum number of hosts: " + str(maxHosts) + "\n")

# ----------------------------------------------------------------------------------------PING
if (ipDec == netDec or ip == broadcastDec):
    print("IP is 'network' or 'broadcast'")
else:
    choice = input("\nDo you want to ping this IP? y=yes\n")
    if (choice == 'y'):
        command = ['ping', ipDec]
        subprocess.call(command)

file.close()
