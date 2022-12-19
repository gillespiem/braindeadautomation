from flask import Flask, request, render_template, jsonify
import requests
import json
import paramiko
app = Flask(__name__)


def execute_command(username, host, key, command):
    pkey = paramiko.RSAKey.from_private_key_file(key)
    
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, pkey=pkey)
    
    
    _stdin, _stdout,_stderr = client.exec_command(command)
    result = _stdout.channel.recv_exit_status()
    

    client.close()
    return str(result)


@app.route("/")
def default_route():
    return jsonify(
            status=0,
            message="Welcome to alexa0"
    )



@app.route("/hello")
def hello():
    return render_template(
            'hello.html',
            title='Hello World'
            )


@app.route("/synergy", methods=["GET"])
def synergy():
    args=request.args
    synergydevice = args.get("synergydevice", default="", type=str)

    if synergydevice == "laptop":
        results = execute_command("alexa0", "192.168.50.1", "/var/www/alexa0/keys/alexa0.key", "sudo -u madsara /usr/local/bin/synergy-work.sh")
    elif synergydevice == "desktop":
        results = execute_command("alexa0", "192.168.50.1", "/var/www/alexa0/keys/alexa0.key" ,"sudo -u madsara /usr/local/bin/synergy-home.sh")
    else:
        results = -1

    return jsonify(
            status=results
    )

def radiothermostat_settings():
    r = requests.get("http://192.168.38.4/tstat")
    response_json = json.loads(r.text)
    return response_json

@app.route("/thermostat_get", methods=["GET"])
def thermostat_get():
    response_json = radiothermostat_settings()
    #r = requests.get("http://192.168.38.4/tstat")
    #response_json = json.loads(r.text)

    return jsonify(
            response_json
    )

@app.route("/thermostat_set", methods=["POST"])
def thermostat_set():
    
    data = json.loads(request.data)
    mode = data.get("thermostat_mode", None)
    temp = data.get("setTemperature", None)

    if mode == "heat":
        t_mode = "t_heat"
    elif mode == "cool":
        t_mode = "t_cool"
       

    data = { t_mode :  int(temp)}
    r = requests.post("http://192.168.38.4/tstat", json = data)

    response_json = radiothermostat_settings()
    return jsonify(
            response_json
    )


"""
Dealing with the thermostat...
192.168.38.4/tstat
{"temp":66.50,"tmode":1,"fmode":2,"override":1,"hold":1,"t_heat":67.00,"tstate":1,"fstate":1,"time":{"day":5,"hour":16,"minute":14},"t_type_post":0}
tmode 2 is cooling, 1 is heating

post json with either t_heat or t_cool and the temperature value. IE: {"t_heat" : 66.50}


"""


"""
Dealing with Virtualization

sudo virsh list --name

sudo virsh reboot <name>

"""


"""
Network Overview
Show IP addresses
"""


if __name__ == "__main__":
    app.run(host='0.0.0.0')
