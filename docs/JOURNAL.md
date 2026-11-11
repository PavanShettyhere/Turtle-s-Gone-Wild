# Turtle’s Gone Wild — Build journal


By Pavan Shetty · Living notebook


> Evidence note: Day 1 milestones were reported by the author. Detailed commands are reference instructions, not recovered history. Day 2’s Pi setup is an explicit assumption awaiting confirmation. Expected output is never a claim of a completed test.


## Day 01 — The foundation

Milestones reported · commands reconstructed

You reported installing ROS 2 Jazzy on your laptop and preparing a Raspberry Pi SD card on Day 1. The steps below explain a reference workflow; your original commands, dates, screenshots, and errors have not been supplied. Your confirmed hardware is a Raspberry Pi 4B, a TurtleBot Burger, and a 32 GB SanDisk microSD card. You described the card image as “Raspberry Pi”; the exact OS name, version, and 32-bit/64-bit architecture still need confirmation.

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

You install an operating-system image onto the SD card; the Raspberry Pi is the computer that boots it. Your card is a 32 GB SanDisk, used with a Raspberry Pi 4B and TurtleBot Burger. You described the installed image as “Raspberry Pi”; whether this means Raspberry Pi OS, and its release and architecture, remain unconfirmed. The Ubuntu image below is an alternative reference path, not a claim about the card you flashed. For this Ubuntu/Jazzy reference path, choose a compatible Ubuntu Server 24.04 LTS 64-bit image for your exact Pi model.

1. Install and open Raspberry Pi Imager from the official Raspberry Pi website.
2. Select your exact Pi model and the intended OS image (or use a downloaded compatible image).
3. Select the microSD card by capacity/device name. Writing erases the selected device; check it carefully.
4. If that image supports customisation, set hostname, username, networking, and SSH; otherwise finish setup with a keyboard and display after boot. Do not publish passwords or SSH private keys.
5. Write, wait for verification, safely eject, insert into the powered-off Pi, then connect a suitable power supply.
6. Allow the first boot to finish. Record the image filename, Pi model, and first successful login.

**Checkpoint:** Record the image filename and the output of cat /etc/os-release and dpkg --print-architecture from the Pi. Do not reflash the card just to match this reference.



## Day 02 — Bring the Pi online

Hardware confirmed · OS and Day 2 actions awaiting confirmation

You mentioned installing ROS 2 on Day 2. This chapter assumes you meant installing ROS 2 Jazzy on the Raspberry Pi. That assumption and every result below need your confirmation. Jazzy is the ROS release, not a separate operating system. Your hardware is now confirmed as Raspberry Pi 4B and TurtleBot Burger with a 32 GB SanDisk card. Since the image was described as “Raspberry Pi,” the Ubuntu apt installation steps below are conditional reference instructions only; first identify the installed OS. Do not run the Ubuntu repository setup on Raspberry Pi OS.

### 1. Log in and identify the Pi

**Run on:** Laptop → Pi

Your Pi is a Raspberry Pi 4B. Identify the existing installation before changing it. Use the username and address you configured; replace PI_USER and PI_IP with real values. If SSH is not available, run the identification commands directly with a keyboard and display.

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

**Checkpoint:** Continue with this reference only for Ubuntu 24.04 arm64 on a compatible Pi.



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

ROS installation is only the foundation. You confirmed TurtleBot Burger and Raspberry Pi 4B. The exact robot revision, installed OS, motor-controller firmware, LiDAR model, USB permissions, robot packages, and launch configuration still need identifying before writing exact bringup commands. TurtleBot3 instructions should only be used if this is a TurtleBot3.

Still to record: exact robot revision, OS image, package branches, any workspace build, firmware steps, errors and fixes, launch command, and actual test result. No motor or firmware commands are presented as completed.

**Checkpoint:** Next milestone: identify the installed OS and add the commands you actually ran on Day 2.



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
