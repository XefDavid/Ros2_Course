# /home/david/bumperbot_ws/src/bumperbot_localization/setup.py

from setuptools import setup

package_name = 'bumperbot_localization'
# Define la ruta relativa al script
scripts_path = 'bumperbot_localization/imu_republisher.py' 

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    # AÑADE ESTA LÍNEA (con la ruta relativa correcta)
    scripts=[scripts_path], 
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='david',
# ... (resto de las líneas) ...
    entry_points={
        'console_scripts': [
            'imu_republisher = bumperbot_localization.imu_republisher:main',
            'kalman_filter = bumperbot_localization.kalman_filter:main',
        ],
    },
)