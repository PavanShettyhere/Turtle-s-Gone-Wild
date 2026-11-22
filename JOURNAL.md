# Turtle’s Gone Wild — Build journal


By Pavan Shetty · Living notebook


> Evidence note: Day 1 milestones were reported by the author. Detailed commands are reference instructions, not recovered history. Day 2’s Pi setup is an explicit assumption awaiting confirmation. Expected output is never a claim of a completed test.


## Day 01 — The foundation

Milestones reported · commands reconstructed

You reported installing ROS 2 Jazzy on your laptop and preparing a Raspberry Pi SD card on Day 1. Your confirmed hardware is a Raspberry Pi 4B, a TurtleBot Burger, and a 32 GB SanDisk microSD card. Later terminal evidence confirms that the Pi currently runs Ubuntu 24.04.5 LTS (Noble Numbat), arm64. The exact original image filename and flashing sequence have not been supplied. Detailed installation commands below are reference instructions, not recovered terminal history.

### 1. Check the operating system

**Run on:** Laptop / Pi

Reference procedure, not a recovered terminal history. These apt instructions assume Ubuntu 24.04 (Noble). Do not apply them unchanged to Raspberry Pi OS or Ubuntu 22.04.

```bash
cat /etc/os-release
```

Prints the Linux distribution and version. Look for Ubuntu and VERSION_ID="24.04".

```bash
dpkg --print-architecture
```

Prints the package architecture: typically amd64 on a laptop or arm64 on a 64-bit Pi installation.

**Checkpoint:** Record the actual OS and architecture before continuing.



### 2. Prepare a UTF-8 locale

**Run on:** Laptop / Pi

A locale defines language and text encoding. An existing UTF-8 locale is fine; the following is an example configuration.

```bash
locale
```

Shows the current language and encoding settings.

```bash
sudo apt update
sudo apt install locales
```

Refreshes the package index, then installs locale management tools. sudo runs with administrator privileges.

```bash
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Generates locale data, saves defaults, and sets the language in this shell.

**Checkpoint:** Run locale again and check for UTF-8.



### 3. Connect Ubuntu to the ROS package repository

**Run on:** Laptop / Pi

Ubuntu needs the ROS package source before apt can find Jazzy. This uses the official ros2-apt-source package. Run each block in the same terminal and stop if a download fails.

```bash
sudo apt install software-properties-common curl
sudo add-apt-repository universe
```

Installs repository tools and curl, then enables Ubuntu’s Universe software collection.

```bash
sudo apt update
export ROS_APT_SOURCE_VERSION=$(curl -fsSL https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F '"tag_name"' | cut -d '"' -f 4)
printf "%s\n" "$ROS_APT_SOURCE_VERSION"
```

Refreshes apt. The pipeline fetches the latest release metadata, selects tag_name, and extracts its value. $(...) captures output; export makes the variable available to child processes. Check that a version was printed.

```bash
curl -fL -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

Downloads the package for this Ubuntu codename. -f fails on HTTP errors, -L follows redirects, and -o selects the output file. dpkg installs the repository configuration package.

**Checkpoint:** The download and dpkg command must both succeed.



### 4. Install Jazzy on the laptop

**Run on:** Laptop

Use the desktop package for a development laptop. Review proposed upgrades before accepting them.

```bash
sudo apt update
sudo apt upgrade
sudo apt install ros-jazzy-desktop
```

Refreshes packages, upgrades installed software, and installs Jazzy with desktop tools.

```bash
source /opt/ros/jazzy/setup.bash
printenv ROS_DISTRO
```

Loads ROS into the current Bash terminal, then prints the selected ROS distribution.

```bash
grep -qxF 'source /opt/ros/jazzy/setup.bash' ~/.bashrc || echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
```

Optional: adds the setup line to future interactive Bash sessions only if absent. || runs the second command when the first does not find a match. >> appends.

**Checkpoint:** ROS_DISTRO should print jazzy. This is an expected result, not an observed result from your laptop.



### 5. Test two ROS nodes

**Run on:** Laptop

Open two terminals. A node is a running ROS program; a topic carries typed messages between nodes.

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_cpp talker
```

Terminal A: ros2 run starts the talker executable from the demo_nodes_cpp package.

```bash
source /opt/ros/jazzy/setup.bash
ros2 run demo_nodes_py listener
```

Terminal B: starts the Python listener. Keep the talker running.

**Checkpoint:** The listener should receive the talker’s messages. Stop each with Ctrl+C; record your actual output.



### 6. Write the Raspberry Pi SD card

**Run on:** Laptop → microSD

You install an operating-system image onto the SD card; the Raspberry Pi is the computer that boots it. Your card is a 32 GB SanDisk, used with a Raspberry Pi 4B and TurtleBot Burger. Your terminal output confirms Ubuntu 24.04.5 LTS (Noble Numbat), arm64, on the Pi. This identifies the currently running OS; it does not establish the original image filename, original point release, or whether the image was Server or Desktop. The following flashing sequence is a reference reconstruction. For this Ubuntu/Jazzy reference path, choose a compatible Ubuntu Server 24.04 LTS 64-bit image for your exact Pi model.

1. Install and open Raspberry Pi Imager from the official Raspberry Pi website.
2. Select your exact Pi model and the intended OS image (or use a downloaded compatible image).
3. Select the microSD card by capacity/device name. Writing erases the selected device; check it carefully.
4. If that image supports customisation, set hostname, username, networking, and SSH; otherwise finish setup with a keyboard and display after boot. Do not publish passwords or SSH private keys.
5. Write, wait for verification, safely eject, insert into the powered-off Pi, then connect a suitable power supply.
6. Allow the first boot to finish. Record the image filename, Pi model, and first successful login.

**Checkpoint:** Verified from your supplied terminal output: the Pi runs Ubuntu 24.04.5 LTS, codename noble, architecture arm64. The original image filename and exact flashing procedure remain to be recorded; no reflash is needed to identify the current OS.



## Day 02 — Bring the Pi online

Hardware and Pi OS verified · Day 2 installation history pending

You mentioned installing ROS 2 on Day 2. This chapter assumes you meant installing ROS 2 Jazzy on the Raspberry Pi; the exact Day 2 installation commands and results remain to be supplied. Your hardware is Raspberry Pi 4B and TurtleBot Burger with a 32 GB SanDisk card. Your supplied terminal output now verifies Ubuntu 24.04.5 LTS (Noble Numbat), arm64, on the Pi. The OS check below is observed evidence; the remaining setup and communication steps are reference instructions. Jazzy is the ROS release, not the operating system.

### 1. Log in and verify the Pi operating system

**Run on:** Laptop → Pi

You supplied terminal output from the Pi confirming its operating system and architecture. This evidence was provided later while documenting the build; its execution on Day 2 is not established. If connecting remotely, use your configured username and address in place of PI_USER and PI_IP. The SSH command is a reference example, not a recovered command.

```bash
ssh PI_USER@PI_IP
```

Opens an encrypted terminal on the Pi. On first connection, verify the host fingerprint using a trusted local view of the Pi.

```bash
hostname
cat /etc/os-release
dpkg --print-architecture
```

Confirms which machine you are on, its OS version, and its package architecture.

**Observed output (relevant lines supplied by the author):**

```text
PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.5 LTS (Noble Numbat)"
VERSION_CODENAME=noble
UBUNTU_CODENAME=noble
arm64
```

**Checkpoint:** Observed: Ubuntu 24.04.5 LTS, Noble, arm64 (64-bit ARM). This confirms the Pi OS and architecture only; it does not prove ROS is installed or that laptop–Pi communication works.



### 2. Install ROS on the Pi

**Run on:** Pi

Repeat Day 1’s UTF-8 locale and ROS repository steps on the Pi itself. Installing ROS on the laptop does not install it on the Pi.

```bash
sudo apt update
sudo apt upgrade
sudo apt install ros-jazzy-ros-base ros-jazzy-demo-nodes-cpp
```

Installs the smaller ROS base and the demonstration executables used in the communication check.

```bash
source /opt/ros/jazzy/setup.bash
printenv ROS_DISTRO
```

Loads Jazzy into this terminal and checks the selected distribution.

**Checkpoint:** Expected: jazzy. Record any package error before moving on.



### 3. Put both machines in the same ROS domain

**Run on:** Laptop + Pi

Use the same local network, avoiding guest/client isolation. The domain number is an example; use the same number on both devices. This shell configuration must be repeated in each ROS terminal. This reference assumes DDS middleware; these discovery variables do not configure rmw_zenoh.

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=30
export ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
```

Loads ROS, chooses a shared discovery domain, and allows discovery on the local subnet. These exports affect this shell and its child processes.

**Checkpoint:** Matching domain IDs alone do not guarantee discovery: network, firewall, and middleware settings also matter.



### 4. Prove laptop ↔ Pi messaging

**Run on:** Laptop + Pi

This is a suggested verification, not a confirmed Day 2 result.

```bash
ros2 run demo_nodes_cpp talker
```

On the Pi, starts a publisher. Leave it running.

```bash
ros2 run demo_nodes_py listener
```

On the laptop, starts the listener after the environment block above.

```bash
ros2 topic list
ros2 node list
```

In another configured terminal, lists discovered topics and nodes.

**Checkpoint:** Look for received messages on the laptop. Save a short output sample, then stop the demos with Ctrl+C.



### 5. Separate ROS setup from robot bringup

**Run on:** TurtleBot hardware

ROS installation is only the foundation. You confirmed TurtleBot Burger and Raspberry Pi 4B. The exact robot revision, motor-controller firmware, LiDAR model, USB permissions, robot packages, and launch configuration still need identifying before writing exact bringup commands. TurtleBot3 instructions should only be used if this is a TurtleBot3.

Still to record: exact robot revision, original OS image filename, package branches, any workspace build, firmware steps, errors and fixes, launch command, and actual test result. No motor or firmware commands are presented as completed.

**Checkpoint:** Next milestone: add the actual ROS installation commands, ROS_DISTRO output, and Day 2 test results.



## Day 03 — First drive

First drive reported · LiDAR scans unresolved

Two days of staring at a terminal. One keypress. It finally moved. 🤖⌨️ Day 3 of my 15-day TurtleBot series. The replacement battery was still two weeks away, so I borrowed a 3S LiPo from a friend. Then I got home and realized the plugs didn’t match. These milestones are from my Day 3 note; exact commands and terminal logs have not been recorded here.

### 1. Connect the borrowed battery

**Run on:** TurtleBot3 Burger / battery

Built an adapter to connect the XT60 and T-connectors so I could use the borrowed 3S LiPo while waiting for the replacement battery.

**Checkpoint:** Adapter built; the borrowed battery powered the first-drive session.



### 2. Test movement with the OpenCR buttons

**Run on:** TurtleBot3 Burger / OpenCR

Tested forward motion and turning with the OpenCR’s built-in buttons.

**Checkpoint:** Forward motion and turning reported working.



### 3. Drive from the laptop keyboard

**Run on:** Laptop → TurtleBot3 Burger

Drove the TurtleBot from my laptop keyboard using ROS 2 teleop. After two days at the terminal, the robot finally moved with a keypress.

**Checkpoint:** First drive ✅ Keyboard teleoperation reported working.



### 4. Try mapping a mini maze

**Run on:** TurtleBot3 Burger / LiDAR

Set up a mini maze for mapping. The LiDAR was spinning, but every scan came back as zeros. The cause is still unresolved.

**Checkpoint:** Next up: get the LiDAR working and map the maze. A successful map has not yet been reported.



### 5. Resources from the Day 3 note

**Run on:** Reference notes

Where to buy: MYBOTSHOP or Génération Robots. Search for “TurtleBot3 Burger.”

Docs: ROBOTIS e-Manual and ROS 2 Jazzy Documentation.

#TurtleBot3 #ROS2 #Robotics #LiDAR #MobileRobotics

**Checkpoint:** Continue the 15-day series with LiDAR troubleshooting and mapping.



## Day 04 — Build the first maze map

Map saved · scan quality still limited

Day 4 moved from keyboard driving to mapping the maze with Cartographer. The project records include a saved map image and YAML file, live scan and odometry checks, and the first saved-map localization experiments. Recovering usable LiDAR points enabled an experimental map; it did not establish a hardware repair.

### 1. Recover usable scan data

**Run on:** TurtleBot3 Burger / Pi

Used the experimental packet-resynchronizing LiDAR reader with robot bringup. It rejects checksum failures and leaves missing measurements as NaN instead of filling gaps or reusing old points. Corruption had also been reproduced during direct sensor testing.

**Checkpoint:** Live scans were available, but coverage remained incomplete and the physical cause was unresolved.



### 2. Map the maze with Cartographer

**Run on:** Laptop + TurtleBot3 Burger

Ran Cartographer and its occupancy-grid publisher while exploring with keyboard teleoperation. The mapping session verified live scans near 5 Hz, odometry near 20 Hz, and the map-to-sensor transform. Saved the map as slam_trial_20261114_143646.pgm with its YAML metadata.

**Checkpoint:** First map saved. This was an experimental map made with degraded scan data.



### 3. Inspect the map and localization in RViz

**Run on:** Laptop

Started working with the saved map and AMCL. Investigated invisible scans and pose displays: the LaserScan display needed Best Effort reliability, and the estimated pose needed its own display. Created a dedicated Nav2 RViz configuration.

**Checkpoint:** The recorded live check found AMCL publishing a pose and a map-to-base_scan transform.



### 4. Carry the timing problems forward

**Run on:** Laptop + Pi

Early navigation attempts exposed inactive lifecycle nodes, stale transforms and uneven scan delivery. One comparison showed roughly 5.2 Hz scans on the Pi, while laptop reception included a 5.213-second gap. Clock synchronization was active, but that alone did not identify the delivery problem.

**Checkpoint:** Next: repeat Nav2 tests using the saved map and investigate scan and transform reliability.



## Day 05 — First Nav2 tests

Navigation tested · repeatable autonomy unresolved

Day 5 focused on Nav2 after the Cartographer mapping session. I made a fresh map, set the starting pose, tried navigation goals, and adjusted speed during testing. The day’s recap describes autonomous movement; the troubleshooting record also contains aborted goals and intermittent transform failures, so reliable navigation remained unfinished.

### 1. Save a fresh map

**Run on:** Laptop / Cartographer

Recorded and saved a new Cartographer map as day5_20261116_222203.pgm and day5_20261116_222203.yaml for the navigation tests.

**Checkpoint:** Fresh map image and metadata are present in the project maps folder.



### 2. Localize and send navigation goals

**Run on:** Laptop / RViz + AMCL + Nav2

Launched saved-map localization, set the robot’s position and heading using 2D Pose Estimate, and started Nav2. Tested sending goals in RViz and learned how obstacle inflation and goal tolerances affect the robot’s behavior.

**Checkpoint:** Map saving, AMCL pose publishing and Nav2 startup worked; goal execution was not consistently reliable.



### 3. Adjust the speed for testing

**Run on:** Laptop / Nav2

Reduced forward speed to 0.10 m/s, then increased it slightly to 0.15 m/s. The session recorded successful live changes to the velocity smoother and controller limits. These were runtime settings rather than evidence of a permanent configuration change.

**Checkpoint:** The final reported forward limit for that session was 0.15 m/s.



### 4. Investigate navigation stops

**Run on:** Laptop + Pi

Checked clock synchronization, scan and odometry rates, transforms, CPU load, and network connectivity. Increased the scan timeout from 0.2 to 0.5 seconds to address a timing mismatch. A laptop-to-Pi ping test had no packet loss in 30 packets, but intermittent TF failures and corrupted scans remained.

**Checkpoint:** Next: resolve the odom-to-base_link connection and LiDAR reliability, then repeat short goals. A short successful ping test does not establish healthy ROS delivery.



## Day 06 — Distance on display

Distance bridge and status display working

Day 6 added a front-distance sensor and a small status screen to the TurtleBot. I connected a VL53L0X and a 128 × 64 OLED to the ESP32, then bridged the ESP32 to the Raspberry Pi and ROS 2 over USB. The goal was to see distance and robot status without constantly checking the laptop, and prepare for later obstacle-aware driving.

### 1. Wire the sensor and display

**Run on:** ESP32 / VL53L0X / OLED

Connected the distance sensor and OLED on the same I²C bus. The ESP32 sketch reads distance and displays it locally.

**Checkpoint:** The OLED showed distance measurements from the sensor.



### 2. Publish distance into ROS 2

**Run on:** ESP32 → USB → Raspberry Pi

Sent newline-delimited JSON from the ESP32 over USB serial at 115200 baud. The Pi bridge converts millimetres into metres and publishes sensor_msgs/Range on /front_distance at about 10 readings per second, using front_distance_link as the frame name.

**Checkpoint:** ROS received distance readings. Naming a frame does not by itself establish the physical mounting transform.



### 3. Show motion and connection status

**Run on:** ROS odometry → ESP32 OLED

Used robot odometry to send IDLE or DRIVING status back to the ESP32. Stopped status updates deliberately and verified the OLED switched to NO LINK after three seconds.

**Checkpoint:** The status display and timeout behavior were verified in the Day 6 session.



### 4. Debug serial data and invalid ranges

**Run on:** ESP32 + Pi

Initially received garbled serial data. Switching the connection from 9600 back to 115200 baud restored readable messages in that session. Invalid or out-of-limits sensor readings became NaN in ROS. Increasing max_range to 6.0 did not recover missing measurements or increase the sensor’s physical reach.

**Checkpoint:** Learned serial bridging, unit conversion and invalid-data handling. Distance reporting worked; automatic obstacle response remained a future task.



## Day 07 — Understand drift and plan sensor fusion

Concepts and experiment plan · implementation scheduled for Day 8

Day 7 was about understanding how the TurtleBot knows which way it is facing. I prepared an explanation of gyroscope drift and the complementary roles of wheel encoders, an IMU and LiDAR. The Day 7 script explicitly left hardware implementation for the following day; the later working session was corrected to Day 8.

### 1. Explain gyroscope drift

**Run on:** Learning notes / video script

Explored how angular-rate measurements accumulate into a heading estimate, and how a small stationary offset can accumulate into angle error. Distinguished the gyroscope from the full IMU.

**Checkpoint:** The Day 7 milestone was understanding and explaining drift, not a completed calibration.



### 2. Compare the sensor roles

**Run on:** TurtleBot motion-estimation plan

Outlined wheel odometry for motion estimates, IMU measurements for rotation, and LiDAR localization against the map. Planned to investigate the motion estimate because navigation had been inconsistent.

**Checkpoint:** Gyroscope drift was not established as the cause of the earlier Nav2 failures; the scan and transform issues still needed attention.



### 3. Plan an additional IMU experiment

**Run on:** ESP32 → Raspberry Pi → ROS 2 (planned)

Proposed testing an additional module described at the time as an MPU-9250, reading it through the ESP32, calibrating it, and publishing measurements into ROS 2. Planned wheel-odometry and IMU fusion with an Extended Kalman Filter, with LiDAR localization supplying the map reference. The module identity still needed a hardware check.

**Checkpoint:** Hardware identification, calibration and filter implementation belong to the subsequent Day 8 work.



### 4. Define how to judge improvement

**Run on:** Experiment plan / series visuals

Planned to repeat the same route and compare the estimated final heading rather than assume fusion would improve it. Prepared the Day 7 voiceover and explanatory animations covering rotation, drift, sensor roles, EKF estimation and the proposed repeat-route test.

**Checkpoint:** Day 7 ended with a testable plan. No completed fusion integration or measured navigation improvement is claimed.



## Git & GitHub — Give the journey a home

Commands supplied by you · execution not evidenced

These are the initial repository commands you pasted. They belong in a project folder on your development computer, not in an arbitrary system directory. Keep this setup chapter separate from your day numbering until you decide when it happened.

### 1. Create the first commit

**Run on:** Laptop / project folder

These bootstrap commands are for a new repository. Do not repeat them as your daily update routine.

```bash
echo "# Turtle-s-Gone-Wild" >> README.md
```

echo prints the Markdown title. >> appends it to README.md, creating the file if needed. Repeating this adds duplicate titles.

```bash
git init
```

Creates local Git metadata so this folder can track file revisions.

```bash
git add README.md
```

Stages only README.md for the next commit. Other files are not included.

```bash
git commit -m "first commit"
```

Records the staged snapshot with a message. Git needs your configured author name and email.

```bash
git branch -M main
```

Renames the current branch to main. -M permits replacing an existing branch name; use carefully in an established repository.

```bash
git remote add origin https://github.com/PavanShettyhere/Turtle-s-Gone-Wild.git
```

Registers this GitHub URL as the remote named origin. It does not create the GitHub repository.

```bash
git push -u origin main
```

Uploads main and remembers origin/main as its upstream. Requires repository access and working GitHub authentication.

**Checkpoint:** Expected: the committed README appears on GitHub.



### 2. Publish later journal updates

**Run on:** Project folder

Use this routine after editing docs/journal.json. The build regenerates both the readable Markdown document and the interactive website from the same content.

```bash
python3 scripts/build.py
```

Regenerates JOURNAL.md and docs/index.html. No third-party Python packages are needed.

```bash
git add docs/journal.json docs/index.html docs/JOURNAL.md JOURNAL.md
git diff --cached
git commit -m "Document the next TurtleBot day"
git push
```

Stages the journal changes, lets you review them, saves a commit, and uploads it. The Pages workflow publishes the docs folder.

**Checkpoint:** Check the Pages workflow in the repository’s Actions tab.



## Troubleshooting

- `ros2: command not found`: source the Jazzy setup file in this terminal and verify installation.

- Package not found: check Ubuntu version, successful ROS apt-source installation, network access, and apt update errors.

- SSH refused: confirm the Pi has booted, its address is correct, and SSH is enabled.

- Listener receives nothing: test on one machine first; then check domain, subnet discovery, network isolation, and firewall rules. Do not disable the firewall blindly.

- Git origin already exists: inspect `git remote -v` before changing any URL.

- Push rejected: fetch and inspect remote changes; do not force-push over someone else’s work.


## Future days

Copy DAY-TEMPLATE.md to collect new notes; then append a chapter in docs/journal.json and regenerate with python3 scripts/build.py. Capture date, machine, goal, exact commands, explanation, actual output, errors/fixes, evidence, and next steps.


## References

- [ROS 2 Jazzy installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html)

- [Official installation source](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/Ubuntu-Install-Debs.rst)

- [ROS apt repository setup](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/_Apt-Repositories.rst)

- [ROS locale setup](https://github.com/ros2/ros2_documentation/blob/jazzy/source/Installation/_Ubuntu-Set-Locale.rst)

- [Raspberry Pi getting started](https://www.raspberrypi.com/documentation/computers/getting-started.html)

- [TurtleBot3 SBC setup (model-specific)](https://emanual.robotis.com/docs/en/platform/turtlebot3/sbc_setup/)

- [ROS discovery configuration](https://docs.ros.org/en/jazzy/Tutorials/Advanced/Improved-Dynamic-Discovery.html)

- [GitHub Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
