# class where this lane is present
class_=205

MQTT_Recv_topic='nodemcu/SCC/TEMP'

#kafka
KAFKA_BROKER = ['10.129.149.18:9092','10.129.149.19:9092','10.129.149.20:9092']
# KAFKA_BROKER = ['10.129.149.50:9092']
# KAFKA_TOPIC = "data/kresit/temp/" + str(class_)
KAFKA_TOPIC = str("temp_")+ str(class_)
