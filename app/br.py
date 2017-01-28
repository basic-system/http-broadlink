import broadlink
import json
import time
import base64

class Broadlink():
    def __init__(self):
        self.devices = []
        self.device_info = []
        self.device_info_file = 'device_info'

        self._set_device_info()

    def _read_saved_info(self):
        device_info = {}
        try:
            with open(self.device_info_file) as f:
                device_info = json.loads(f.read())
        except Exception as e:
            print("can't read file: {}".format(e))

        return device_info
        # self.device_info = device_info


    def _get_broadlink_devices(self):
        self.devices = broadlink.discover(timeout=7)
        print(self.devices)
        for d in self.devices:
            d.auth()

    def _set_device_info(self):
        read_info = {}
        read_info = self._read_saved_info()
        print("read_info: {}".format(read_info))
        self._get_broadlink_devices()
        new_info = []
        for d in self.devices:
            mac_txt = str(d.mac).encode('hex')
            # mac_txt = "{}:{}:{}:{}:{}:{}".format(mac_txt[0:2],mac_txt[2:4],mac_txt[4:6],mac_txt[6:8],mac_txt[8:10],mac_txt[10:12])
            mac_txt = "{}:{}:{}:{}:{}:{}".format(mac_txt[10:12],mac_txt[8:10],mac_txt[6:8],mac_txt[4:6],mac_txt[2:4],mac_txt[0:2])
            dev = {'name': mac_txt, 'mac': mac_txt, 'type': d.get_type()}
            if dev['type'] == 'RM2' or dev['type'] == 'A1':
                sensors = self.get_sensors(mac_txt)
                dev['sensors'] = sensors
            if dev['type'] == 'SP2':
                dev['status'] = self.dev_status(mac_txt)

            found = False
            for sdev in read_info:
                if dev['mac'] == sdev['mac']:
                    print("found {}".format(dev['mac']))
                    found = True
                    read_info.remove(sdev)
                    if dev['type'] == 'RM2' or dev['type'] == 'A1':
                        sdev['sensors'] = dev['sensors']
                    if dev['type'] == 'SP2':
                        sdev['status'] = dev['status']
                    sdev['removed'] = False
                    new_info.append(sdev)
            if not found:
                new_info.append(dev)
        print("read_info after remove is {}".format(read_info))
        for dev in read_info:
            dev['removed'] = True
            new_info.append(dev)
        new_info.sort()
        self.device_info = new_info
        self._save_info()
        print(self.device_info)

    def _mac_to_dev(self, mac):
        # mac_bin = mac.replace(':', '').decode('hex')
        mac_arr = mac.split(':')
        mac_arr.reverse()
        mac = "".join(mac_arr)
        mac_bin = mac.decode('hex')
        for dev in self.devices:
            if dev.mac == mac_bin:
                return dev
        return False

    def _save_info(self):
        try:
            with open(self.device_info_file, 'w') as f:
                f.write(json.dumps(self.device_info, indent=4))
        except Exception as e:
            print("Can't save device info: {}".format(e))

    def get_sensors(self, mac):
        dev = self._mac_to_dev(mac)
        if not dev:
            return False
        dev_type = dev.get_type()
        if dev_type == 'RM2':
            return self.get_rm_sensors(dev)
        elif dev_type == 'A1':
            return self.get_a1_sensors(dev)
        else:
            return False

    def get_a1_sensors(self, device):
        return device.check_sensors()

    def get_rm_sensors(self, device):
        temp = device.check_temperature()
        return {'temperature': temp}

    def dev_status(self, mac):
        dev = self._mac_to_dev(mac)
        if not dev:
            return False
        dev_type = dev.get_type()
        if dev_type == 'SP2':
            return dev.check_power()

    def sp_change_status(self, mac, status=None):
        dev = self._mac_to_dev(mac)
        if not dev:
            return False
        dev_type = dev.get_type()
        if dev_type != 'SP2':
            return False
        if status is None:
            status = device.check_power()
            status = not status
        dev.set_power(status)
        for d in self.device_info:
            if d['mac'] == mac:
                d['status'] = status
                self._save_info()
        return True

    def set_name(self, mac, name):
        for dev in self.device_info:
            if dev['mac'] == mac:
                self.device_info.remove(dev)
                dev.update({'name': name})
                self.device_info.append(dev)
        self._save_info()


    def remove_dev(self, mac):
        for dev in self.device_info:
            if dev['mac'] == mac:
                self.device_info.remove(dev)
        self._save_info()

    def add_rm_device(self, mac, name=None):
        for dev in self.device_info:
            if dev['mac'] == mac:
                self.device_info.remove(dev)
                rm_devices = dev.get('devices',{})
                if name is None:
                    name = 'new_device1'
                    while True:
                        if name not in rm_devices:
                            break
                        else:
                            counter = int(name[-1:])
                            name = name[:-1] + str(int(name[-1:]) + 1)
                if name in rm_devices:
                    print('device {} already exsits'.format(name))
                else:
                    rm_devices.update({name:{'buttons': {}}})
                    print('add {} device'.format(name))
                dev['devices'] = rm_devices
                self.device_info.append(dev)
        self._save_info()
        return name

    def edit_rm_device(self, mac, name, new_name):
        for dev in self.device_info:
            if dev['mac'] == mac:
                print(name, new_name)
                self.device_info.remove(dev)
                rm_devices = dev.get('devices',{})
                print(rm_devices)
                if name in rm_devices:
                    rmdev_info = rm_devices.pop(name)
                    rm_devices.update({new_name: rmdev_info})

                dev['devices'] = rm_devices
                self.device_info.append(dev)
                break
        print(self.device_info)
        self._save_info()


    def remove_rm_device(self, mac, name):
        for dev in self.device_info:
            if dev['mac'] == mac:
                self.device_info.remove(dev)
                rm_devices = dev.get('devices',{})
                if name in rm_devices:
                    rm_devices.pop(name)
                dev['devices'] = rm_devices
                self.device_info.append(dev)
        self._save_info()


    def add_button(self, mac, device, name):
        found_dev = None
        found_rm = None
        for dev in self.device_info:
            if dev['mac'] == mac and dev['type'] == 'RM2':
                found_rm = dev
                if 'devices' in dev and device in dev['devices']:
                    found_dev = device

        if found_rm is None:
            return ''

        result = ''
        dev = self._mac_to_dev(found_rm['mac'])
        dev.enter_learning()
        time.sleep(4)
        result = dev.check_data()

        print(found_rm)
        self.device_info.remove(found_rm)

        new_dev = found_rm
        button = {name: {'cmd': result.encode('base64')}}
        if 'devices' not in new_dev:
            new_dev['devices'] = {}
        if device not in new_dev['devices']:
            new_dev['devices'].update({device:{'buttons': {}}})
        new_dev['devices'][device]['buttons'].update(button)
        self.device_info.append(new_dev)
        print(self.device_info)
        self._save_info()
        return True

    def press_button(self, mac, device, name):
        print(mac, device, name)
        dev_rm = self._mac_to_dev(mac)
        found_rm = None
        for dev in self.device_info:
            if dev['mac'] == mac and dev['type'] == 'RM2':
                found_rm = dev
        cmd = found_rm['devices'][device]['buttons'][name]['cmd']
        dev_rm.send_data(cmd.decode('base64'))
        return True
