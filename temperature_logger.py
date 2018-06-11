from kafka import KafkaProducer
from kafka.errors import KafkaError
import paho.mqtt.client as mqtt
import paho.mqtt
import socket
from config import *
import sqlite3
import time
from datetime import datetime
import logging
from logging.config import fileConfig



def getSensorDetails():
    '''
    :returns dict consisting temperature sensor information from the sqlite
    '''
    db=sqlite3.connect('sensor_details.sql')
    cursor=db.cursor()
    sql = "select * from sensors where  class=%d" % ( class_)
    cursor.execute(sql)
    temp_sensor_list = cursor.fetchall()
    if len(temp_sensor_list) == 0:
        print "Error reading from the SQLite DB"

    temp_sensor={}
    for elem in temp_sensor_list:
        val={'zone':elem[1], 'lane':elem[2],'classroom':elem[3] }
        temp_sensor[elem[0]]=val

    return temp_sensor



def get_ip():
    """
    :returns the ip address of the rpi
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    my_ip=s.getsockname()[0]
    s.close()
    return (my_ip)



def kafka_publish(data):
    """
    :publishes temperature to MQTT and Kafka
    """
    try:
        sensor_id=data.split(" ")[0]
        tempC=float(data.split(" ")[1])
        timestamp=time.time()
        temp_string = "%f,%d,%d,%d,%f"%(timestamp,temp_sensor[sensor_id]['zone'], temp_sensor[sensor_id]['lane'], temp_sensor[sensor_id]['classroom'], tempC)
        kafka_producer.send(KAFKA_TOPIC,"temp_string")
    except Exception as e:
        logger.exception(str(e.message)+" "+str(data))


def get_temperature():
    """
    gets and process temperature data from nodemcu
    """
    def on_connect(client, userdata, flags, rc):
        logger.debug("Receving data from MQTT " )
        client.subscribe(MQTT_Recv_topic)

    def on_message(client, userdata, msg):
      kafka_publish(msg.payload)

    my_ip=get_ip()
    mqttc = mqtt.Client("I2C_temp_"+str(class_))  #remove if mqtt is not needed
    client = mqtt.Client(protocol=mqtt.MQTTv31)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(my_ip, 1883, 60)
        logger.debug("Connected to Local MQTT : " +str(my_ip))
    except Exception as e:
        logger.exception("Error connecting to  Local MQTT : " +str(my_ip))

    client.loop_forever()



if __name__ == '__main__':
    fileConfig('config.ini')
    logger=logging.getLogger()

    logger.debug('Connecting to Kafka Brokers')
    kafka_producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
    logger.debug("Connected to Kafka Brokers :"+str(KAFKA_BROKER))

    temp_sensor=getSensorDetails()
    get_temperature()
