import subprocess,re,yaml


class Test_pro():
    def __init__(self):
        self.search_devices = ["2 OnePlus Nord","2 Pixel 2","2 Pixel 3a","2 M2007J3SP"]
        self.constent = ['DeviceA','DeviceB',"DeviceC","DeviceD"]
        self.number = [0,1,2,3]
        self.Dut_info = []
        self.temp = []
        self.dict0 = {}
        self.android_device_info = []        
        self.android_devices = []
        self.number_of_devices_present = []
    def collecting_system_information(self):
        list_of_command = ["lsb_release -d","hostname",'lscpu | grep -E "Architecture|CPU op-mode |Vendor ID|Model name"']
        for i in list_of_command:
            executing_commands = subprocess.run(i,shell=True,capture_output=True)
            self.Dut_info.append((executing_commands.stdout.decode().split(" ")))
        keys = self.Dut_info[0][0].split("\t")[0].strip(":")
        values = self.Dut_info[0][0]+self.Dut_info[0][1]
        values = values.split(":")[1].lstrip("\t")
        self.dict0[keys] = values
        self.dict0['Hostname']=self.Dut_info[1][0].strip("\n")
        v = "".join(self.Dut_info[2])
        cpu_details = v.split(":")[1::2]
        cpu_details1 = v.split(":")[::2]
        sperate_keys = []
        sperate_vales = []
        sperate_keys.append(cpu_details1[0])
        sperate_vales.append(cpu_details[0].split("\n")[0])
        sperate_keys.append(cpu_details[0].split("\n")[1])
        sperate_vales.append(cpu_details1[1].split("\n")[0])
        sperate_vales.append(cpu_details[1].split("\n")[0])
        sperate_keys.append(cpu_details1[1].split("\n")[1])
        ip_address = subprocess.run("hostname -I",shell=True,capture_output=True)
        self.dict0["ip"] = ip_address.stdout.decode().split(" ")[0:1]
        for a,b in zip(sperate_keys,sperate_vales):
            self.dict0[a] = b
    def devices_info(self):
        cmd = "lsusb -v > connected_usb_info.txt"
        runner = subprocess.run(cmd,shell=True,capture_output=True)
        with open("connected_usb_info.txt","r") as data:
            data = data.read()
        pa = "idVendor(.*)\n..idProduct(.*)\n..bcdDevice(.*)\n..iManufacturer(.*)\n..iProduct(.*)\n..iSerial(.*)"
        requried_values = re.findall(pa,data)
        for i in requried_values:
            # print(i)
            value = i
            for j in value:
                self.android_device_info.append((j.strip()))
        for devices in self.search_devices:
            try:
                if devices in self.android_device_info:
                    self.index_position = self.android_device_info.index(devices)
                    for i in range(2):
                        self.device_info = self.android_devices.append("".join(self.android_device_info[self.index_position][1:].strip(" ")))
                        self.index_position +=1
                else:
                    pass
            except ValueError:
                print(f"these device is not connect {devices} to system")
        start_point = 0
        end_point = 2

        self.number_of_loop = len(self.android_devices)/2
        i = 0
        while i < self.number_of_loop:
            self.temp.append(self.android_devices[start_point:end_point])
            start_point = end_point
            end_point +=2
            self.dict0[self.constent[i]] = self.temp[i]
            i+=1
        print(self.dict0)

test_pro = Test_pro()
test_pro.collecting_system_information()
test_pro.devices_info()