import json
import subprocess

import psutil
from platform import uname


def correct_size(bts, ending='iB'):
    size = 1024
    for item in ["", "K", "M", "G", "T", "P"]:
        if bts < size:
            return f"{bts:.2f}{item}{ending}"
        bts /= size


def creating_file():
    collect_info_dict = dict()
    if 'info' not in collect_info_dict:
        collect_info_dict['info'] = dict()
        collect_info_dict['info']['system_info'] = dict()
        collect_info_dict['info']['system_info'] = {'system': {'comp_name': uname().node,
                                                               'os_name': f"{uname().system} {uname().release}",
                                                               'version': uname().version,
                                                               'machine': uname().machine},
                                                    'processor': {'name': uname().processor,
                                                                  'phisycal_core': psutil.cpu_count(logical=False),
                                                                  'all_core': psutil.cpu_count(logical=True),
                                                                  'freq_max': f"{psutil.cpu_freq().max:.2f}Мгц"},
                                                    'ram': {'volume': correct_size(psutil.virtual_memory().total),
                                                            'aviable': correct_size(psutil.virtual_memory().available),
                                                            'used': correct_size(psutil.virtual_memory().used)}}

    for partition in psutil.disk_partitions():
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue
        if 'disk_info' not in collect_info_dict['info']:
            collect_info_dict['info']['disk_info'] = dict()
        if f"'device': {partition.device}" not in collect_info_dict['info']['disk_info']:
            collect_info_dict['info']['disk_info'][partition.device] = dict()
            collect_info_dict['info']['disk_info'][partition.device] = {'file_system': partition.fstype,
                                                                        'size_total': correct_size(
                                                                            partition_usage.total),
                                                                        'size_used': correct_size(
                                                                            partition_usage.used),
                                                                        'size_free': correct_size(
                                                                            partition_usage.free),
                                                                        'percent':
                                                                            f'{partition_usage.percent}'}

    for interface_name, interface_address in psutil.net_if_addrs().items():
        if interface_name == 'Loopback Pseudo-Interface 1':
            continue
        else:
            if 'net_info' not in collect_info_dict['info']:
                collect_info_dict['info']['net_info'] = dict()
            if interface_name not in collect_info_dict['info']['net_info']:
                collect_info_dict['info']['net_info'][interface_name] = dict()
                collect_info_dict['info']['net_info'][interface_name] = {
                    'mac': interface_address[0].address.replace("-", ":"),
                    'ipv4': interface_address[1].address,
                    'ipv6': interface_address[2].address}

    return collect_info_dict


def win_dop_info(dict_info):
    import windows_tools.product_key

    # motherboard
    man_moth_com = 'WMIC BASEBOARD GET Manufacturer /VALUE'.split()
    manufacturer = str(subprocess.check_output(man_moth_com, shell=True)).split("\\n")[2].replace("\\r", "").\
        split("=")[1]

    prod_com = 'WMIC BASEBOARD GET Product /VALUE'.split()
    product = str(subprocess.check_output(prod_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[1]

    # bios
    verb_com = 'WMIC BIOS GET Version /VALUE'.split()
    version_bios = str(subprocess.check_output(verb_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[1]

    man_bios_com = 'WMIC BIOS GET Manufacturer /VALUE'.split()
    manufacturer_bios = str(subprocess.check_output(man_bios_com, shell=True)).\
        split("\\n")[2].split("\\r")[0].split("=")[1]

    sn_bios_com = 'WMIC BIOS GET SerialNumber /VALUE'.split()
    serial_num_bios = str(subprocess.check_output(sn_bios_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[
        1]

    dv_bios_com = 'WMIC BIOS GET Description /VALUE'.split()
    date_version_bios = str(subprocess.check_output(dv_bios_com, shell=True)).\
        split("\\n")[2].split("\\r")[0].split("=")[1]

    smbios_com = 'WMIC BIOS GET SMBIOSBIOSVersion /VALUE'.split()
    smbios_ver = str(subprocess.check_output(smbios_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[1]

    # boot configuration
    boot_dir_com = 'WMIC BOOTCONFIG GET BootDirectory /VALUE'.split()
    boot_directory = str(subprocess.check_output(boot_dir_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[
        1]

    lastd_com = 'WMIC BOOTCONFIG GET LastDrive /VALUE'.split()
    last_drive = str(subprocess.check_output(lastd_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[1]

    # processor info
    proc_name_com = 'WMIC CPU GET Name /VALUE'.split()
    processor_name = str(subprocess.check_output(proc_name_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[
        1]

    proc_id_com = 'WMIC CPU GET ProcessorId /VALUE'.split()
    processor_id = str(subprocess.check_output(proc_id_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[1]

    # system info from SMBIOS
    uuid_sys_com = 'WMIC CSPRODUCT GET UUID /VALUE'.split()
    uuid_system = str(subprocess.check_output(uuid_sys_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[1]

    # monitor info
    mon_pnp_com = 'WMIC DESKTOPMONITOR GET PNPDeviceID /VALUE'.split()
    pnpdeviceid = str(subprocess.check_output(mon_pnp_com, shell=True)).split("\\n")[2].split("\\r")[0].split("=")[1]

    if 'other_info' not in dict_info['info']:
        dict_info['info']['other_info'] = dict()
        dict_info['info']['other_info'] = {'motherboard_manufacturer': manufacturer,
                                           'motherboard_product': product,
                                           'version_bios': version_bios,
                                           'manufacturer_bios': manufacturer_bios,
                                           'serial_number_bios': serial_num_bios,
                                           'date_version_bios': date_version_bios,
                                           'smbios_version': smbios_ver,
                                           'os_boot_directory': boot_directory,
                                           'last_drive': last_drive,
                                           'processor_name': processor_name,
                                           'processor_id': processor_id,
                                           'uuid_system': uuid_system,
                                           'pnp_device_id': pnpdeviceid}

    # disk info
    d_cap_com = 'WMIC DISKDRIVE GET Caption /VALUE'.split()
    disk_caption = str(subprocess.check_output(d_cap_com, shell=True)).strip().split("\\n")
    d_list = []
    for cap in disk_caption:
        if 'Caption=' in cap:
            d_list.append(cap.split("\\r")[0].split("=")[1])

    ser_dcom = 'WMIC DISKDRIVE GET SerialNumber /VALUE'.split()
    serial_num_disk = str(subprocess.check_output(ser_dcom, shell=True)).strip().split("\\n")
    d_sn_list = []
    for ser in serial_num_disk:
        if 'SerialNumber=' in ser:
            d_sn_list.append(ser.split("\\r")[0].split("=")[1].strip())

    for num in range(0, len(d_list)):
        if 'drive_name_serial' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['drive_name_serial'] = dict()
        if d_list[num] not in dict_info['info']['other_info']['drive_name_serial']:
            dict_info['info']['other_info']['drive_name_serial'][d_list[num]] = dict()
            dict_info['info']['other_info']['drive_name_serial'][d_list[num]] = d_sn_list[num]

    firm_rev_com = 'WMIC DISKDRIVE GET FirmwareRevision /VALUE'.split()
    firmvare_revision_disk = str(subprocess.check_output(firm_rev_com, shell=True)).strip().split("\\n")
    fr_list = []
    for num, fm in enumerate(firmvare_revision_disk):
        if 'FirmwareRevision=' in fm:
            fr_list.append(fm.split("\\r")[0].split("=")[1].strip())
    for nf in range(0, len(fr_list)):
        if 'drive_firmware' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['drive_firmware'] = dict()
        if f'drive_{str(nf)}' not in dict_info['info']['other_info']['drive_firmware']:
            dict_info['info']['other_info']['drive_firmware'][f'drive_{str(nf)}'] = dict()
            dict_info['info']['other_info']['drive_firmware'][f'drive_{str(nf)}'] = fr_list[nf]

    disk_sig_com = 'WMIC DISKDRIVE GET Signature /VALUE'.split()
    disk_signature = str(subprocess.check_output(disk_sig_com, shell=True)).strip().split("\\n")
    sig_list = []
    for sig in disk_signature:
        if 'Signature=' in sig:
            sig_list.append(sig.split("\\r")[0].split("=")[1].strip())
    for sgl in range(0, len(sig_list)):
        if 'disk_signature' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['disk_signature'] = dict()
        if f'sig_{sgl}' not in dict_info['info']['other_info']['disk_signature']:
            dict_info['info']['other_info']['disk_signature'][f'sig_{sgl}'] = sig_list[sgl]

    # volume disk info
    vdn_com = 'WMIC LOGICALDISK GET VolumeName /value'
    disk_volume_name = str(subprocess.check_output(vdn_com, shell=True)).strip().split("\\n")
    vol_name_list = []
    for voln in disk_volume_name:
        if 'VolumeName=' in voln:
            if voln.split("\\r")[0].split("=")[1].strip() == "":
                vol_name_list.append('Drive')
            else:
                vol_name_list.append(voln.split("\\r")[0].split("=")[1].strip())

    for vln in range(0, len(vol_name_list)):
        if 'volum_name' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['volum_name'] = dict()
        if f'volum_{vln}' not in dict_info['info']['other_info']['volum_name']:
            dict_info['info']['other_info']['volum_name'][f'volum_{vln}'] = dict()
            dict_info['info']['other_info']['volum_name'][f'volum_{vln}'] = vol_name_list[vln]

    vol_sn_com = 'WMIC LOGICALDISK GET VolumeSerialNumber /value'
    volume_serialnumber = str(subprocess.check_output(vol_sn_com, shell=True)).strip().split("\\n")
    vol_sn_list = []
    for vol_sn in volume_serialnumber:
        if 'VolumeSerialNumber=' in vol_sn:
            vol_sn_list.append(vol_sn.split("\\r")[0].split("=")[1].strip())

    for vsn in range(0, len(vol_sn_list)):
        if 'volume_serial_number' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['volume_serial_number'] = dict()
        if f'volume_serial_{vsn}' not in dict_info['info']['other_info']['volume_serial_number']:
            dict_info['info']['other_info']['volume_serial_number'][f'volume_serial_{vsn}'] = dict()
            dict_info['info']['other_info']['volume_serial_number'][f'volume_serial_{vsn}'] = vol_sn_list[vsn]

    # ram info
    formf_com = 'WMIC MEMORYCHIP GET FormFactor /value'.split()
    ram_form_factor = str(subprocess.check_output(formf_com, shell=True)).strip().split("\\n")
    for num, ffm in enumerate(ram_form_factor):
        if 'FormFactor=8' in ffm:
            if 'memory_form_factor' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_form_factor'] = dict()
            if f'memory_{num}' not in dict_info['info']['other_info']['memory_form_factor']:
                dict_info['info']['other_info']['memory_form_factor'][f'memory_{num}'] = dict()
                dict_info['info']['other_info']['memory_form_factor'][f'memory_{num}'] = \
                    ffm.split("\\r")[0].split("=")[1].strip()

    ram_man_com = 'WMIC MEMORYCHIP GET Manufacturer /value'.split()
    ram_manufacturer = str(subprocess.check_output(ram_man_com, shell=True)).strip().split("\\n")
    for num, ram_m in enumerate(ram_manufacturer):
        if 'Manufacturer=' in ram_m:
            if 'memory_manufacturer' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_manufacturer'] = dict()
            if f'manufacturer_{num}' not in dict_info['info']['other_info']['memory_manufacturer']:
                dict_info['info']['other_info']['memory_manufacturer'][f'manufacturer_{num}'] = dict()
                dict_info['info']['other_info']['memory_manufacturer'][f'manufacturer_{num}'] = \
                    ram_m.split("\\r")[0].split("=")[1].strip()

    ram_pn_com = 'WMIC MEMORYCHIP GET PartNumber /value'.split()
    ram_part_number = str(subprocess.check_output(ram_pn_com, shell=True)).strip().split("\\n")
    for num, rpn in enumerate(ram_part_number):
        if 'PartNumber=' in rpn:
            if 'memory_part_number' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_part_number'] = dict()
            if f'part_number_{num}' not in dict_info['info']['other_info']['memory_part_number']:
                dict_info['info']['other_info']['memory_part_number'][f'part_number_{num}'] = dict()
                dict_info['info']['other_info']['memory_part_number'][f'part_number_{num}'] = \
                    rpn.split("\\r")[0].split("=")[1].strip()

    ram_sn_com = 'WMIC MEMORYCHIP GET SerialNumber /value'.split()
    serial_number_ram = str(subprocess.check_output(ram_sn_com, shell=True)).strip().split("\\n")
    for num, sn_ram in enumerate(serial_number_ram):
        if 'SerialNumber=' in sn_ram:
            if 'memory_serial_number' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_serial_number'] = dict()
            if f'serial_number_{num}' not in dict_info['info']['other_info']['memory_serial_number']:
                dict_info['info']['other_info']['memory_serial_number'][f'serial_number_{num}'] = dict()
                dict_info['info']['other_info']['memory_serial_number'][f'serial_number_{num}'] = \
                    sn_ram.split("\\r")[0].split("=")[1].strip()

    ram_spf_com = 'WMIC MEMORYCHIP GET Speed /value'.split()
    ram_speed_frequency = str(subprocess.check_output(ram_spf_com, shell=True)).strip().split("\\n")
    for num, rsf in enumerate(ram_speed_frequency):
        if 'Speed=' in rsf:
            if 'memory_frequency' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['memory_frequency'] = dict()
            if f'frequency_{num}' not in dict_info['info']['other_info']['memory_frequency']:
                dict_info['info']['other_info']['memory_frequency'][f'frequency_{num}'] = dict()
                dict_info['info']['other_info']['memory_frequency'][f'frequency_{num}'] = \
                    rsf.split("\\r")[0].split("=")[1].strip()

    ram_mdev_com = 'WMIC MEMPHYSICAL get MemoryDevices /value'.split()
    ram_count_memory = str(subprocess.check_output(ram_mdev_com, shell=True)).strip().split("\\n")[2].split("\\r")[0].\
        split("=")[1]
    if 'count_memory' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['count_memory'] = dict()
        dict_info['info']['other_info']['count_memory'] = ram_count_memory

    # network adapter info
    cap_net_com = 'WMIC NIC get Caption /value'.split()
    caption_net_adapter = str(subprocess.check_output(cap_net_com, shell=True)).strip().split("\\n")
    for num, capnad in enumerate(caption_net_adapter):
        if 'Caption=' in capnad:
            if 'net_adapter_caption' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['net_adapter_caption'] = dict()
            if f'net_adapter_{num}' not in dict_info['info']['other_info']['net_adapter_caption']:
                dict_info['info']['other_info']['net_adapter_caption'][f'net_adapter_{num}'] = dict()
                dict_info['info']['other_info']['net_adapter_caption'][f'net_adapter_{num}'] = \
                    capnad.split("\\r")[0].split("=")[1].strip().split("]")[1].strip()

    net_giud_com = 'WMIC NIC get GUID /value'.split()
    guid_network_adapter = str(subprocess.check_output(net_giud_com, shell=True)).strip().split("\\n")
    for num, guid in enumerate(guid_network_adapter):
        if 'GUID=' in guid:
            if guid.split("\\r")[0].split("=")[1].strip():
                if 'guid_net_adapter' not in dict_info['info']['other_info']:
                    dict_info['info']['other_info']['guid_net_adapter'] = dict()
                if f'guid_{num}' not in dict_info['info']['other_info']['guid_net_adapter']:
                    dict_info['info']['other_info']['guid_net_adapter'][f'guid_{num}'] = dict()
                    dict_info['info']['other_info']['guid_net_adapter'][f'guid_{num}'] = \
                        guid.split("\\r")[0].split("=")[1].strip()

    # os information
    os_inst_date_com = 'WMIC OS get InstallDate /value'.split()
    os_install_date = str(subprocess.check_output(os_inst_date_com, shell=True)).strip().split("\\n")[2].\
        split("\\r")[0].split("=")[1]
    if 'os_install_date_time' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['os_install_date_time'] = dict()
        dict_info['info']['other_info']['os_install_date_time'] = f'{os_install_date[0:8]}, {os_install_date[8:14]}'

    os_sn_com = 'WMIC OS get SerialNumber /value'.split()
    os_serial_number = str(subprocess.check_output(os_sn_com, shell=True)).strip().split("\\n")[2].split("\\r")[0].\
        split("=")[1]

    if 'os_serial_number' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['os_serial_number'] = dict()
        dict_info['info']['other_info']['os_serial_number'] = os_serial_number

    # license cliendID
    lic_clid_com = 'wmic path softwarelicensingservice get ClientMachineID /value'
    client_machine_id_lic = \
        str(subprocess.check_output(lic_clid_com, shell=True)).strip().split("\\n")[2].split("\\r")[0].split("=")[1]
    if 'client_machine_id_lic' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['client_machine_id_lic'] = dict()
        dict_info['info']['other_info']['client_machine_id_lic'] = client_machine_id_lic

    serial_num_com = 'wmic path softwarelicensingservice get OA3xOriginalProductKey /value'.split()
    key_activate_win_uefi = \
        str(subprocess.check_output(serial_num_com, shell=True)).strip().split("\\n")[2].split("\\r")[0].split("=")[
                1]
    if key_activate_win_uefi == '':
        pkey = windows_tools.product_key.get_windows_product_key_from_reg()
        if 'key_activate_win' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['key_activate_win'] = dict()
            dict_info['info']['other_info']['key_activate_win'] = pkey
    else:
        if 'key_activate_win' not in dict_info['info']['other_info']:
            dict_info['info']['other_info']['key_activate_win'] = dict()
            dict_info['info']['other_info']['key_activate_win'] = key_activate_win_uefi

    # printer info
    prn_cap_com = 'WMIC PRINTER get Caption /value'.split()
    printer_caption = str(subprocess.check_output(prn_cap_com, shell=True)).strip().split("\\n")
    for num, prn in enumerate(printer_caption):
        if 'Caption=' in prn:
            if 'printer_caption' not in dict_info['info']['other_info']:
                dict_info['info']['other_info']['printer_caption'] = dict()
            if f'printer_{num}' not in dict_info['info']['other_info']['printer_caption']:
                dict_info['info']['other_info']['printer_caption'][f'printer_{num}'] = dict()
                dict_info['info']['other_info']['printer_caption'][f'printer_{num}'] = prn.split("\\r")[0].\
                    split("=")[1].strip()

    # time zone info
    time_z_com = 'WMIC TIMEZONE get Caption /value'.split()
    time_zone = str(subprocess.check_output(time_z_com, shell=True)).strip().split("\\n")[2].split("\\r")[0].\
        split("=")[1]
    if 'time_zone' not in dict_info['info']['other_info']:
        dict_info['info']['other_info']['time_zone'] = dict()
        dict_info['info']['other_info']['time_zone'] = time_zone

    return dict_info


def print_dop_info(dict_info_dop):
    for item in dict_info_dop['info']:
        if item == "other_info":
            print(f'[+] Дополнительная информация\n{"-"*33}')
            for elem in dict_info_dop['info'][item]:
                if elem == 'drive_name_serial':
                    print(f"\n[+] Диски: модель, серийный номер")
                    for drive in dict_info_dop['info'][item][elem]:
                        print(f"\t- {drive}: {dict_info_dop['info'][item][elem][drive]}")
                elif elem == 'drive_firmware':
                    print(f"\n[+] Версия прошивки:")
                    for firmware in dict_info_dop['info'][item][elem]:
                        print(f"\t- {firmware}: {dict_info_dop['info'][item][elem][firmware]}")
                elif elem == 'disk_signature':
                    print(f"\n[+] Цифровая подпись:")
                    for signature in dict_info_dop['info'][item][elem]:
                        print(f"\t- {signature}: {dict_info_dop['info'][item][elem][signature]}")
                elif elem == 'volum_name':
                    print(f"\n[+] Имя тома:")
                    for vol_n in dict_info_dop['info'][item][elem]:
                        print(f"\t- {vol_n}: {dict_info_dop['info'][item][elem][vol_n]}")
                elif elem == 'volume_serial_number':
                    print(f"\n[+] Серийный номер тома:")
                    for volume_serial in dict_info_dop['info'][item][elem]:
                        print(f"\t- {volume_serial}: {dict_info_dop['info'][item][elem][volume_serial]}")
                elif elem == 'memory_form_factor':
                    print(f"\n[+] RAM форм-фактор:")
                    for memory_ff in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_ff}: {dict_info_dop['info'][item][elem][memory_ff]}")
                elif elem == 'memory_manufacturer':
                    print(f"\n[+] Производитель RAM:")
                    for memory_man in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_man}: {dict_info_dop['info'][item][elem][memory_man]}")
                elif elem == 'memory_part_number':
                    print(f"\n[+] Инвентарный номер RAM:")
                    for memory_part in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_part}: {dict_info_dop['info'][item][elem][memory_part]}")
                elif elem == 'memory_serial_number':
                    print(f"\n[+] Серийный номер RAM:")
                    for memory_serial in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_serial}: {dict_info_dop['info'][item][elem][memory_serial]}")
                elif elem == 'memory_frequency':
                    print(f"\n[+] Частота RAM:")
                    for memory_fr in dict_info_dop['info'][item][elem]:
                        print(f"\t- {memory_fr}: {dict_info_dop['info'][item][elem][memory_fr]}")
                elif elem == 'net_adapter_caption':
                    print(f"\n[+] Название сетевого адаптера:")
                    for adapter_caption in dict_info_dop['info'][item][elem]:
                        print(f"\t- {adapter_caption}: {dict_info_dop['info'][item][elem][adapter_caption]}")
                elif elem == 'guid_net_adapter':
                    print(f"\n[+] GUID сетевого адаптера:")
                    for guid_net in dict_info_dop['info'][item][elem]:
                        print(f"\t- {guid_net}: {dict_info_dop['info'][item][elem][guid_net]}")
                elif elem == 'printer_caption':
                    print(f"\n[+] Название принтера:")
                    for prn_caption in dict_info_dop['info'][item][elem]:
                        print(f"\t- {prn_caption}: {dict_info_dop['info'][item][elem][prn_caption]}")
                else:
                    print(f"[+] {elem.upper()}: {dict_info_dop['info'][item][elem]}")


def print_info(dict_info):
    for item in dict_info['info']:
        if item == "system_info":
            for elem in dict_info['info'][item]:
                if elem == 'system':
                    print(f"[+] Информация о системе\n"
                          f"\t- Имя компьютера: {dict_info['info'][item][elem]['comp_name']}\n"
                          f"\t- Опереционная система: {dict_info['info'][item][elem]['os_name']}\n"
                          f"\t- Сборка: {dict_info['info'][item][elem]['version']}\n"
                          f"\t- Архитектура: {dict_info['info'][item][elem]['machine']}\n")
                if elem == 'processor':
                    print(f"[+] Информация о процессоре\n"
                          f"\t- Семейство: {dict_info['info'][item][elem]['name']}\n"
                          f"\t- Физические ядра: {dict_info['info'][item][elem]['phisycal_core']}\n"
                          f"\t- Всего ядер: {dict_info['info'][item][elem]['all_core']}\n"
                          f"\t- Максимальная частота: {dict_info['info'][item][elem]['freq_max']}\n")
                if elem == 'ram':
                    print(f"[+] Оперативная память\n"
                          f"\t- Объем: {dict_info['info'][item][elem]['volume']}\n"
                          f"\t- Доступно: {dict_info['info'][item][elem]['aviable']}\n"
                          f"\t- Используется: {dict_info['info'][item][elem]['used']}\n")
        if item == "disk_info":
            for elem in dict_info['info'][item]:
                print(f"[+] Информация о дисках\n"
                      f"\t- Имя диска: {elem}\n"
                      f"\t- Файловая система: {dict_info['info'][item][elem]['file_system']}\n"
                      f"\t- Объем диска: {dict_info['info'][item][elem]['size_total']}\n"
                      f"\t- Занято: {dict_info['info'][item][elem]['size_used']}\n"
                      f"\t- Свободно: {dict_info['info'][item][elem]['size_free']}\n"
                      f"\t- Заполненность: {dict_info['info'][item][elem]['percent']}%\n")
        if item == "net_info":
            for elem in dict_info['info'][item]:
                print(f"[+] Информация о сети\n"
                      f"\t- Имя интерфейса: {elem}\n"
                      f"\t- MAC-адрес: {dict_info['info'][item][elem]['mac']}\n"
                      f"\t- IPv4: {dict_info['info'][item][elem]['ipv4']}\n"
                      f"\t- IPv6: {dict_info['info'][item][elem]['ipv6']}\n")


def main():
    if uname().system == "Windows":
        dict_info = creating_file()
        dict_info_dop = win_dop_info(dict_info)
        with open(f'info_{uname().node}.json', 'w', encoding='utf-8') as file:
            json.dump(dict_info_dop, file, indent=4, ensure_ascii=False)
        print_info(dict_info)
        print_dop_info(dict_info_dop)
    elif uname().system == "Linux":
        dict_info = creating_file()
        with open(f'info_{uname().node}.json', 'w', encoding='utf-8') as file:
            json.dump(dict_info, file, indent=4, ensure_ascii=False)
        print_info(dict_info)


if __name__ == "__main__":
    main()