import os

import cv2
import numpy as np
from matplotlib import pyplot as plt

from action import Action
from constants import AGENT, WIRE, NO_WIRE, AGENT_ON_WIRE, AGENT_ON_NO_WIRE
from state import State


class Environment:
    def __init__(self, image: np.array, pixel_to_mm_ratio):
        cv2.namedWindow("display", cv2.WINDOW_NORMAL)
        self.position = (0, 256)  # TODO: Change to start position
        self.end_position = (512, 256)
        self.orientation = 0
        self.current_state = None
        self.pixel_to_mm_ratio = 1
        self.next_state = None
        self.image = image
        self.__first_action = True
        self.__do_four_steps()

    def __do_four_steps(self):
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)
        self.do_action(Action.RIGHT)

    def show_image(self):
        # Mark the current position of the agent in the image
        marked_image = self.image.copy()
        # Convert the image to 8-bit depth
        marked_image = cv2.normalize(marked_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # Convert the image to RGB
        marked_image = cv2.cvtColor(marked_image, cv2.COLOR_GRAY2RGB)
        marked_image = cv2.circle(marked_image, self.position, radius=0, color=(0, 0, 255), thickness=2)
        # Show the image
        cv2.imshow('display', marked_image)
        # Update the window
        cv2.waitKey(1)

    def do_action(self, action):
        # action is a tuple of (x, y, orientation)
        print("Action: ", action)
        if not self.__first_action:
            self.image[self.position[0], self.position[1]] = self.image[self.position[0], self.position[1]] - AGENT
        self.position = (self.position[0] + action.value[0], self.position[1] + action.value[1])
        self.orientation = (self.orientation + action.value[2]) % 360
        self.image[self.position[0], self.position[1]] = self.image[self.position[0], self.position[1]] + AGENT
        
        # ! placeholder. needs to be replaced with actual local goal
        local_goal = (512, 256)
        self.next_state = State(self.image, self.position, self.orientation, self.pixel_to_mm_ratio, local_goal)
        self.__first_action = False
        self.show_image()

    def reset_agent(self):
        self.position = (0, 256)  # TODO: Change to start position
        self.orientation = 0
        # self.image[self.position[0], self.position[1]] = AGENT
        # self.do_action(Action.RIGHT)
        # self.do_action(Action.RIGHT)
        self.__do_four_steps()

    def check_end_position(self):
        if self.position[0] == self.end_position[0] - 2 and self.position[1] == self.end_position[1]:
            self.__do_four_steps()
            return True
        else:
            return False

    def update_states(self):
        self.current_state = self.next_state
