import rclpy
import socket
from std_msgs.msg import String

global g_node, arduino_, publisher

def timer_callback():
    global g_node, arduino_, publisher
    if rclpy.ok():
        data = arduino_.recv(1)
        data_to_publish = ""
        while(data.decode("utf-8") != "\n"):
            data_to_publish += data.decode("utf-8")
            data = arduino_.recv(1)
        msg = String()
        msg.data = str(data_to_publish)
        publisher.publish(msg)

def main():
    global g_node, arduino_, publisher
    rclpy.init()

    g_node = rclpy.create_node('simple_socket_receiver')
    g_node.declare_parameter("port", 8144)
    g_node.declare_parameter("ip_add", "192.168.59.210")
    port = g_node.get_parameter("port").value
    ip = g_node.get_parameter("ip_add").value
    arduino_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    arduino_.connect((ip, port))
    publisher = g_node.create_publisher(String, '/socket_receiver', 10)

    # Timers
    timer = g_node.create_timer(1, timer_callback)
    print("Esperando mensajes desde el Arduino...")

    rclpy.spin(g_node)
    g_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
