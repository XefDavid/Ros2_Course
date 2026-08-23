# Ros2_Course

Personal learning workspace for a ROS 2 course: differential-drive robot simulation
("bumperbot") covering description/URDF, Gazebo simulation, `ros2_control`, TF2,
kinematics, joystick teleoperation, and sensor fusion / localization with an
Extended Kalman Filter.

Several packages (`bumperbot_description`, `bumperbot_controller`,
`bumperbot_localization`) are based on course-provided starter code; the
`bumperbot_msgs`, `bumperbot_py_examples`, `bumperbot_utils` and
`bumperbot_cpp_examples` packages are exercises built while following along.

## Requirements

- ROS 2 (Humble or newer — some packages use `ROS_DISTRO`-conditional
  dependencies for Iron/Jazzy, e.g. `gz_ros2_control` vs `ign_ros2_control`)
- Gazebo via `ros_gz_sim` / `ros_gz_bridge`
- `robot_localization` (for the EKF)
- Python 3 with `rclpy`, `numpy`, `tf_transformations`

Install ROS dependencies from the workspace root with `rosdep`:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

## Building

```bash
colcon build --symlink-install
source install/setup.bash
```

## Package overview

| Package | Purpose |
|---|---|
| `bumperbot_description` | Robot URDF/xacro, meshes, RViz config, Gazebo spawn launch |
| `bumperbot_controller` | `ros2_control` controllers, simple/noisy differential-drive controller, joystick teleop |
| `bumperbot_localization` | EKF sensor fusion (`robot_localization`), custom Kalman filter, IMU republisher |
| `bumperbot_msgs` | Custom service definitions (`AddTwoInts`, `GetTransform`) |
| `bumperbot_py_examples` | Standalone rclpy examples: pub/sub, services, parameters, TF2, turtlesim kinematics |
| `bumperbot_utils` | Odometry subscriber / trajectory publisher utilities |
| `bumperbot_cpp_examples` | Placeholder package for C++ examples (work in progress, no sources yet) |

## Running the simulation

Visualize the robot in RViz only:

```bash
ros2 launch bumperbot_description display.launch.py
```

Spawn the robot in Gazebo (bridges `/clock` and `/imu`):

```bash
ros2 launch bumperbot_description gazebo.launch.py
```

Load the `ros2_control` controllers and the simple/noisy velocity controller
(add `use_python:=True` to run the Python nodes instead of the C++ ones):

```bash
ros2 launch bumperbot_controller controller.launch.py
```

Joystick teleoperation:

```bash
ros2 launch bumperbot_controller joystick_teleop.launch.py
```

Run the EKF localization stack (`robot_localization` + IMU republisher):

```bash
ros2 launch bumperbot_localization local_localization.launch.py
```

## Notes

- `build/`, `install/`, `log/`, and any local Python `venv/` are git-ignored —
  they are not meant to be committed and should be regenerated locally.
- Commit history is organized progressively by topic (kinematics → ROS 2
  control → TF2 → joystick → Kalman filter → sensor fusion), so it can be
  followed lesson by lesson.
