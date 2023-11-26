import rclpy
from std_msgs.msg import String
import socket

global g_node, arduino_

def callback_msg(msg):
    global g_node, arduino_
    g_node.get_logger().info("Mensaje recibido desde ROS: %s" % msg.data)
    # Send message to Serial
    arduino_.send(msg.data.encode("utf-8"))

def main():
    global g_node, arduino_
    rclpy.init()

    g_node = rclpy.create_node('simple_socket_transmitter')
    g_node.declare_parameter("port", 8144)
    g_node.declare_parameter("ip_add", "192.168.59.210")
    port = g_node.get_parameter("port").value
    ip = g_node.get_parameter("ip_add").value
    arduino_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    arduino_.connect((ip,port))
    print("Conexión establecida con el Arduino. Envíe comandos desde ROS: ")
    
    subscription = g_node.create_subscription(String, '/socket_transmitter', callback_msg, 10)
    
    rclpy.spin(g_node)
    g_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()