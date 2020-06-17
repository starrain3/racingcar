import random
import numpy as np
class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)                        # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        pass

    def update(self, scene_info):
        """
        9 grid relative position
        |    |    |    |
        |  1 |  2 |  3 |
        |    |  5 |    |
        |  4 |  c |  6 |
        |    |    |    |
        |  7 |  8 |  9 |
        |    |    |    |       
        """
        # print(self.car_pos)
        def check_grid():
            grid = set()
            speed_ahead = [100,100,100]
            if self.car_pos[0] <= 45: # left bound
                grid.add(1)
                grid.add(4)
                grid.add(7)
            elif self.car_pos[0] >= 545: # right bound
                grid.add(3)
                grid.add(6)
                grid.add(9)

            for car in scene_info["cars_info"]:
                if car["id"] != self.player_no:
                    x = self.car_pos[0] - car["pos"][0] # x relative position
                    y = self.car_pos[1] - car["pos"][1] # y relative position
                    if x <= 40 and x >= -40 :      
                        if y > 0 and y < 300:
                            grid.add(2)
                            if y < 200:
                                if speed_ahead[1]>car["velocity"]:
                                    speed_ahead[1]=car["velocity"]
                                grid.add(5) 
                        elif y < 0 and y > -200:
                            grid.add(8)
                    if x > -100 and x < -40 :
                        if y > 80 and y < 250:
                            grid.add(3)
                            if speed_ahead[2]>car["velocity"]:
                                speed_ahead[2]=car["velocity"]
                        elif y < -80 and y > -200:
                            grid.add(9)
                        elif y < 80 and y > -80:
                            grid.add(6)
                    if x < 100 and x > 40:
                        if y > 80 and y < 250:
                            grid.add(1)
                            if speed_ahead[0]>car["velocity"]:
                                speed_ahead[0]=car["velocity"]
                        elif y < -80 and y > -200:
                            grid.add(7)
                        elif y < 80 and y > -80:
                            grid.add(4)
            return move(grid= grid, speed_ahead = speed_ahead)
            
        def move(grid, speed_ahead): 
            # if self.player_no == 0:
            # print(speed_ahead)
            print(grid)
            if len(grid) == 0:
                if self.car_pos[0]>315:
                    return ["SPEED","MOVE_LEFT"]
                else: 
                    return ["SPEED","MOVE_RIGHT"]    
            else:
                if(1 not in grid) and (2 not in grid) and (3 not in grid) and (5 not in grid):
                    if self.car_pos[0] > self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_LEFT"]
                    elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                        return ["SPEED", "MOVE_RIGHT"]
                    else :return ["SPEED"]
                else:
                    if(5 in grid)or (2 in grid): #前面有車
                        if(1 in grid)and (3 in grid): #左前右前都有
                            if(4 not in grid) and(6 not in grid):
                                if self.car_pos[0]>315:
                                    if(speed_ahead[1]>self.car_vel) and (speed_ahead[0]>self.car_vel):
                                        return ["SPEED","MOVE_LEFT"]
                                    else:
                                        return ["BRAKE","MOVE_LEFT"]
                                else:    
                                    if(speed_ahead[1]>self.car_vel) and (speed_ahead[2]>self.car_vel):
                                        return ["SPEED","MOVE_RIGHT"]
                                    else:
                                        return ["BRAKE","MOVE_RIGHT"]
                            elif(4 not in grid):
                                if(speed_ahead[1]>self.car_vel) and (speed_ahead[0]>self.car_vel):
                                    return ["SPEED","MOVE_LEFT"]
                                else:
                                    return ["BRAKE","MOVE_LEFT"]
                            elif(6 not in grid):
                                if(speed_ahead[1]>self.car_vel) and (speed_ahead[2]>self.car_vel):
                                    return ["SPEED","MOVE_RIGHT"]
                                else:
                                    return ["BRAKE","MOVE_RIGHT"]
                            else:
                                return["BRAKE"]               
                        if(1 not in grid) and (4 not in grid) and (3 not in grid) and (6 not in grid) :
                            a=(speed_ahead[1]+random.random())%2
                            print(a)
                            if a>=0.5:
                                if self.car_pos[0]>65:
                                    if(speed_ahead[1]>self.car_vel) and (speed_ahead[0]>self.car_vel):
                                        return ["SPEED","MOVE_LEFT"]
                                    else:
                                        return ["BRAKE","MOVE_LEFT"]
                                else:
                                    if(speed_ahead[1]>self.car_vel) and (speed_ahead[2]>self.car_vel):
                                        return ["SPEED","MOVE_RIGHT"]
                                    else:
                                        return ["BRAKE","MOVE_RIGHT"]

                            else:
                                if self.car_pos[0]<545:    
                                    if(speed_ahead[1]>self.car_vel) and (speed_ahead[2]>self.car_vel):
                                        return ["SPEED","MOVE_RIGHT"]
                                    else:
                                        return ["BRAKE","MOVE_RIGHT"]
                                else:
                                    if(speed_ahead[1]>self.car_vel) and (speed_ahead[0]>self.car_vel):
                                        return ["SPEED","MOVE_LEFT"]
                                    else:
                                        return ["BRAKE","MOVE_LEFT"]
                        if(1 not in grid) :
                            if(4 not in grid):
                                if(5 in grid):
                                    if(speed_ahead[1]>self.car_vel):
                                        return ["SPEED","MOVE_LEFT"]
                                    else:
                                        return ["BRAKE","MOVE_LEFT"]
                                else:
                                    return ["SPEED","MOVE_LEFT"]
                            if(6 not in grid):
                                if(5 in grid):
                                    if(speed_ahead[1]>self.car_vel):
                                        return ["SPEED","MOVE_RIGHT"]
                                    else:
                                        return ["BRAKE","MOVE_RIGHT"]
                                else:
                                    return ["SPEED","MOVE_RIGHT"]

                        if(3 not in grid):
                            if(6 not in grid):
                                if(5 in grid):
                                    if(speed_ahead[1]>self.car_vel):
                                        return ["SPEED","MOVE_RIGHT"]
                                    else:
                                        return ["BRAKE","MOVE_RIGHT"]
                                else:
                                    return ["SPEED","MOVE_RIGHT"]
                            if(4 not in grid):
                                if(5 in grid):
                                    if(speed_ahead[1]>self.car_vel):
                                        return ["SPEED","MOVE_LEFT"]
                                    else:
                                        return ["BRAKE","MOVE_LEFT"]
                                else:
                                    return ["SPEED","MOVE_LEFT"]    
                        else:
                            return ["BRAKE"]            
                    else:
                        if self.car_pos[0] > self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_LEFT"]
                        elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                            return ["SPEED", "MOVE_RIGHT"]
                        else :return ["SPEED"]              

                        


                                
                    
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]

        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]

        if scene_info["status"] != "ALIVE":
            return "RESET"
        self.car_lane = self.car_pos[0] // 70
        return check_grid()

    def reset(self):
        """
        Reset the status
        """
        pass