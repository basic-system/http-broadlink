from flask import render_template
from flask import render_template, flash, redirect, session, url_for, request, g
from flask import request, jsonify
from app import app
import br

Br = br.Broadlink()

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html",
        title = 'Broadlink devices',
        devices = Br.device_info)

@app.route('/edit_name', methods = ['POST'])
def edit_name():
    value =  request.form.get('value')
    mac =  request.form.get('mac')
    print(mac, value)
    Br.set_name(mac, value)
    return jsonify({"status": "ok"})

@app.route('/get_sensors', methods = ['GET', 'POST'])
def get_sensors():
    mac = request.values.get('mac')
    sensor = request.values.get('sensor', None)
    if mac:
        sensors = Br.get_sensors(mac)
        if sensor:
            return jsonify({sensor:sensors[sensor]})
        else:
            return jsonify(sensors)
    else:
        return jsonify({'result':'can not find mac'})

@app.route('/switch', methods = ['GET', 'POST'])
def switch():
    mac = request.values.get('mac')
    action = request.values.get('action')
    if mac and action in ['on', 'off', 'status']:
        if action == 'on':
            res =  Br.sp_change_status(mac, True)
        if action == 'off':
            res =  Br.sp_change_status(mac, False)
        if action == 'status':
            res = Br.dev_status(mac)
            if res:
                return "0"
            else:
                return "1"
        if res:
            return jsonify({'result': 'ok'})
        else:
            return jsonify({'result': 'false'})
    else:
        return jsonify({'result':'can not find mac'})


@app.route('/remove', methods = ['GET', 'POST'])
def remove():
    mac = request.values.get('mac')
    if mac:
        Br.remove_dev(mac)
        return redirect(url_for('index'))
    else:
        return jsonify({'result':'can not find mac'})

@app.route('/add_rm_device', methods = ['GET', 'POST'])
def add_rm_device():
    mac = request.values.get('mac')
    if mac:
        name = Br.add_rm_device(mac)
        return jsonify({'name': name})
    else:
        return jsonify({'result':'can not find mac'})

@app.route('/remove_rm_device', methods = ['GET', 'POST'])
def remove_rm_device():
    mac = request.values.get('mac')
    name = request.values.get('name')
    if mac and name:
        Br.remove_rm_device(mac, name)
        return jsonify({'result': "{} removed".format(name)})
    else:
        return jsonify({'result':'can not find mac'})


@app.route('/editrm_name', methods = ['GET', 'POST'])
def edit_rm_device():
    mac = request.values.get('mac')
    name = request.values.get('name')
    new_name = request.values.get('value')
    print(mac, name, new_name)
    if mac and name and new_name:
        if name == new_name:
            return jsonify({'result': "{} is the same".format(name)})
        Br.edit_rm_device(mac, name, new_name)
        return jsonify({'result': "{} changed".format(name)})
    else:
        return jsonify({'result':'can not find mac or name'})


@app.route('/add_button', methods = ['GET', 'POST'])
def add_button():
    device = request.values.get('device')
    mac = request.values.get('mac')
    name = request.values.get('name')
    print(device, mac, name)
    Br.add_button(mac, device, name)
    return jsonify({'result': 'good'})

@app.route('/press_button', methods = ['GET', 'POST'])
def press_button():
    device = request.values.get('device')
    mac = request.values.get('mac')
    name = request.values.get('name')
    print(device, mac, name)
    Br.press_button(mac, device, name)
    return jsonify({'result': 'good'})
