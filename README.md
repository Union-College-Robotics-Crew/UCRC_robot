# UCRC_robot
## Instruction for fast update on robot: (MAC)
First right click on the folder and open with Terminal.
Then use the following code:
```
git clone https://github.com/Union-College-Robotics-Crew/UCRC_robot.git
cd UCRC_robot
mv * ..
cd ..
rm -rf UCRC_robot
```

##Upload code from robot to main
```
git init .
git remote add origin https://github.com/Union-College-Robotics-Crew/UCRC_robot.git
git checkout <new branch>
```
rest is usual git commit-push stuff.
