#!/usr/bin/env python3

import rclpy
from rclpy.node import Node #importamos node para poder crear los nodos
from std_msgs.msg import Float64MultiArray #asi el mensaje se puede mandar en un array de multiples numeros en 64bits
from geometry_msgs.msg import TwistStamped #con esta importacion cada mensaje publicado tiene un time stamp
import numpy as np #importamos numpy para que se pueda realizar operaciones aritmeticas  como las matriz

class SimpleController(Node):# creamos la clase del nodo
    def __init__(self): #constructor
        super().__init__("simple_controller") #con esto creamos el constructor y le damos el nombre al nodo en el que vamos a crear los topic

        #declaramos los parametros por defecto , pero pueden estar escritos o sobre escritos en un archivo, esta distancia en le mundo real es en metros
        self.declare_parameter("wheel_radius", 0.033)
        self.declare_parameter("wheel_separation", 0.17)
        
        #aqui guardamos en variables los parametros obtenidos  utilizando un double para estandarizar el valos y tiparlo 
        self.wheel_radius = self.get_parameter("wheel_radius").get_parameter_value().double_value
        self.wheel_separation = self.get_parameter("wheel_separation").get_parameter_value().double_value

        #escribimos unos log para ver que va funcionando el flujo
        self.get_logger().info("Using wheel radius %f" % self.wheel_radius) #forma antigua de escribir un logger
        self.get_logger().info(f"using wheel separation {self.wheel_separation}")#forma moderna 

        #creamo una subscripcion al nodo con este topico  en que vamos a escribir un array de decimales, en que va ahaber en cola no mas de diez mensajes
        self.wheel_cmd_pub = self.create_publisher(Float64MultiArray,"simple_velocity_controller/commands", 10)
        #creamos una subscripcion a un topic en el que  se llama a la funcion callback, cada mensaje tiene un timestamp
        self.vel_sub = self.create_subscription(TwistStamped,"bumperbot_controller/cmd_vel",self.velCallback, 10) 

        #creamos una matriz de 2x2 para cinematica
        self.speed_conversion = np.array([[self.wheel_radius/2, self.wheel_radius/2],# calcula la velocidad lineal riueda derecha e izquierda de forma respectiva
                                          [self.wheel_radius/self.wheel_separation, -self.wheel_radius/self.wheel_separation] #calcula la rotacion(velocidad angular)
                                          ])
        self.get_logger().info(f"the conversion matrix is {self.speed_conversion}")
    
    def velCallback(self, msg):
        robot_speed = np.array([[msg.twist.linear.x], #velocidad hacia adelante si es positiva..
                                [msg.twist.angular.z]]) #velocidad de rotacion o angular
        wheel_speed = np.matmul(np.linalg.inv(self.speed_conversion), robot_speed) #se invierte la matriz de conversion

        #creamos el mensaje tipado en float y seguido le añadimos la velocidad de la rueda derecha y de la izquierda
        wheel_speed_msg = Float64MultiArray()
        wheel_speed_msg.data = [wheel_speed[0,0],wheel_speed[1,0]]

        self.wheel_cmd_pub.publish(wheel_speed_msg)#publica en el topic wheel_cmd_pub la velocidad 

def main():
    rclpy. init()
    simple_controller = SimpleController()
    rclpy.spin(simple_controller)
    simple_controller.destroy_node()
    rclpy.shutdown()

if __name__== "__main__":
    main()
