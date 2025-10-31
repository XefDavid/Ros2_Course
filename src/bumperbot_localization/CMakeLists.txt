cmake_minimum_required(VERSION 3.8)
project(bumperbot_localization)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# === DEPENDENCIAS ===
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# === INSTALA PAQUETE PYTHON ===
ament_python_install_package(${PROJECT_NAME})

# === INSTALA ARCHIVOS PYTHON COMO EJECUTABLES ===
# install(PROGRAMS
#   ${PROJECT_NAME}/imu_republisher.py
#   # Si tienes kalman_filter.py, añádelo aquí también
#   # ${PROJECT_NAME}/kalman_filter.py
#   DESTINATION lib/${PROJECT_NAME}
# )

# === INSTALA CARPETAS ===
install(
  DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()