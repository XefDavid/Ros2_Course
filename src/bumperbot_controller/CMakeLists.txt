cmake_minimum_required(VERSION 3.5)
project(bumperbot_controller)

# Encuentra las dependencias necesarias
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2 REQUIRED)


# Instala el paquete Python
ament_python_install_package(${PROJECT_NAME})

# Instala el script Python como ejecutable
install(PROGRAMS
  ${PROJECT_NAME}/simple_controller.py
  DESTINATION lib/${PROJECT_NAME}
)

# Instala los directorios launch y config
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()