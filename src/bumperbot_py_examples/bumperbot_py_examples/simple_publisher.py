#importamos la libreria, info en => https://docs.ros.org/en/iron/p/rclpy/

import  rclpy
from rclpy.node import Node 
from std_msgs.msg import String
import random #esto es para hacer pruebas no es necesario en el codigo

class SimplePublisher(Node):
    def  __init__(self):
        super().__init__("simple_spublisher")

        self.publi_disparos = self.create_publisher(String, "Disparos", 5)# el 5 es el numero de mensajes maximo que hay en cola
        self.publi_reaccion = self.create_publisher(String, "Onomatopellas",5)
        self.publi_sonido=self.create_publisher(String, "Sonidos", 5)#importante no repetir el nombre del t

        self.counter = 0
        self.frequency = 1.0 #elegimo la frecuencia de publicacion de mensajes dentro del canal , ahora es cada segundo

        self.get_logger().info("Publicando a %d Hz" % self.frequency)

        self.timer = self.create_timer(self.frequency , self.timerCallback)     
        self.soundOfWar()
        self.onomatopeya()

      

    
    def timerCallback(self):
        colors = ["rojo", "verde", "azul", "negro", "muy negro", "mas que negro"]
        bulletColor = random.choice(colors)


        msg = String()
        msg.data = f"Hola, contador de disparos: {self.counter}, color de la bala es: {bulletColor}"

        self.publi_disparos.publish(msg)

        self.soundOfWar()
        self.onomatopeya()
        self.counter += 1   

        

    def soundOfWar(self):
        sounds= ["bim", "pum", "pamPam", "cataPum", "Chimpumpam", "alalalalala!!"]
        bulletSound= random.choice(sounds)

        msg =String()
        msg.data =f"el sonido de la bala es {bulletSound}!!!"
        self.publi_sonido.publish(msg)

    def onomatopeya(self):
         onomatopeyas= ["UY!", "AY", "ostia", "aiba", "la leche ", "OMG!, corre!"]
         onomatopeya= random.choice(onomatopeyas)

         msg= String()
         msg.data= f"EL publico dice: {onomatopeya}"
         self.publi_reaccion.publish(msg) 

def main():
        rclpy.init()
        Simple_Publisher =  SimplePublisher()
        rclpy.spin(Simple_Publisher)
        Simple_Publisher.destroy_node() #Limpia el nodo
        rclpy.shutdown() #cierra el bucle

if __name__ == '__main__':
        main()