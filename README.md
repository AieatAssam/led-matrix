# Led Matrix Display
This repository contains code for led matrix display to be run on Raspberry Pi hardware. 
Can be used with first generation Raspberry Pi Zero W and later.

Networking is required since the system is designed to be operated remotely via RabbitMQ (AMQP) commands.

## Installation
Clone the repository and run the following commands to create a virtual environment (venv) in _venv_ directory, activate it and install dependencies
```shell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
in the repository root. This will pull and install all the required packages, including Adafruit support for WS2812B LEDs via NeoPixel libraries.

By default the system is designed to operate on pin D18. This can be changed in the _main.py_ file if needed. If using D18, ensure that audio support on Pi is disabled by editing file in `/boot/firmware/cmdline.txt` and changing `dtparam=audio=on` to `dtparam=audio=off` and then rebooting.
If using different pixel size from default 16x16 matrix, edit corresponding definitions in the source code.
Adafruit library was chosen over alternative ones due to its use of DMA for a more stable LED control even when the main CPU is busy.

## Running
To run the application, execute the following with **sudo** (since Adafruit library requires privileged access to hardware):
```shell
sudo venv/bin/python main.py
```
To run as service, create service definition as follows:
```shell
sudo nano /lib/systemd/system/led-matrix.service
```
Edit the file and define service as follows:
```ini
[Unit]
Description=LED Matrix Display Service
After=network.target

[Service]
Type=idle
Restart=on-failure
User=root
ExecStart=/bin/bash -c 'cd  /<PATH_TO_led-matrix>/ && source venv/bin/activate && python main.py'

[Install]
WantedBy=multi-user.target
```
Adjust the service file to suit source location. Afterwards, enable service and start it:
```shell
sudo chmod 644 /lib/systemd/system/led-matrix.service
sudo systemctl daemon-reload
sudo systemctl enable led-matrix
sudo systemctl start led-matrix
```


## Control
You can use any RabbitMQ deployment or service to communicate to the device:
* Local deployments
* Container deployments
* SaaS cloud (such as CloudAMQP with its capable free tier)

Supply connection string to your RabbitMQ deployment either as part of .env file based on provided [.env.template](./.env.template) or by directly populating environment variable **RABBITMQ_URL**
The application will create and listen on queue called _led_command_queue_ and bind it to exchange called _led_commands_. Sending command to the exchange will cause the system to pick it up and process, displaying supplied frames and animating as needed. Example payload is supplied in [example_payload.json](./example_payload.json) file. 