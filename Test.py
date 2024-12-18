from panda3d.core import Point3
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.showbase.DirectObject import DirectObject

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        
        # Load the ball model
        self.ball = self.loader.loadModel("models/balls.glb")
        self.ball.reparentTo(self.render)

        
        # Set the initial position of the ball
        self.update_ball_position()
        
        # Update the ball's position every frame
        self.taskMgr.add(self.update_task, "updateTask")
        
        # Set up key controls
        self.accept("arrow_up", self.move_camera, [0, 1])
        self.accept("arrow_down", self.move_camera, [0, -1])
        self.accept("arrow_left", self.move_camera, [-1, 0])
        self.accept("arrow_right", self.move_camera, [1, 0])
    
    def update_ball_position(self):
        # Get the camera's position and direction
        cam_pos = self.camera.getPos()
        cam_dir = self.camera.getQuat().getForward()
        
        # Calculate the new position 10 feet away from the camera
        new_pos = cam_pos + cam_dir * 10
        
        # Set the ball's position
        self.ball.setPos(new_pos)
    
    def update_task(self, task):
        return Task.cont
    
    def move_camera(self, x, y):
        # Move the camera based on the input
        self.camera.setPos(self.camera.getPos() + Point3(x, y, 0))
        self.update_ball_position()

app = MyApp()
app.run()
