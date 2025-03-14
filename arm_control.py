import pybullet as p
import numpy as np

class RoboticArm:
    def __init__(self):
        # Initialize PyBullet
        self.physicsClient = p.connect(p.GUI)
        p.setGravity(0, 0, -9.81)
        
        # Load URDF model
        self.arm = p.loadURDF('robot_arm.urdf', [0, 0, 0])
        
        # Get joint information
        self.num_joints = p.getNumJoints(self.arm)
        self.joint_indices = range(self.num_joints)

    def move_to(self, target_position):
        # Convert 2D target to 3D
        target_3d = (target_position[0], target_position[1], 0.5)
        
        # Calculate inverse kinematics
        joint_angles = p.calculateInverseKinematics(
            self.arm,
            endEffectorLinkIndex=self.num_joints - 1,
            targetPosition=target_3d
        )
        
        # Move joints to target angles
        for i in self.joint_indices:
            p.setJointMotorControl2(
                bodyIndex=self.arm,
                jointIndex=i,
                controlMode=p.POSITION_CONTROL,
                targetPosition=joint_angles[i]
            )
        
        # Step simulation
        p.stepSimulation()

    def cleanup(self):
        p.disconnect()