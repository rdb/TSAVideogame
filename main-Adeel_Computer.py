from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.showbase.DirectObject import DirectObject
from direct.controls.InputState import InputState
from panda3d.core import CollisionTraverser, BitMask32, CollisionHandlerEvent, CollisionNode, CollisionHandlerPusher, CollisionBox, Point3, CollisionSphere, LVector3, CollisionPolygon, WindowProperties
from panda3d.physics import *
from panda3d.ai import AIWorld, AICharacter, Flock
import direct.gui.DirectGuiGlobals as DGG
from direct.actor.Actor import Actor
from direct.gui.DirectGui import *
class CameraControllerBehaviour(DirectObject):
    _instances = 0
    def __init__(self, camera, velocity=9, mouse_sensitivity=0.2, initial_pos=(-0.5, -12, 7.7), showbase=None):
        self._camera = camera
        self._velocity = velocity
        self._mouse_sensitivity = mouse_sensitivity
        self._keys = None
        self._input_state = InputState()
        self._heading = 0.0
        self._pitch = 0.0
        self._yaw = 0.0
        self._roll = 0.0
        self._showbase = base if showbase is None else showbase
        self._gravity = LVector3(0, 0, -3.8)  # Set gravity vector pointing downward
        self._instance = CameraControllerBehaviour._instances
        CameraControllerBehaviour._instances += 1
        self._camera.setPos(*initial_pos)
        # Set the initial position of the camera

    def setup(self, keys={
        'w':"forward", 
        's':"backward",
        'a':"left",
        'd':"right",
        'space':"up",
        'e':"down"
    }):
        self._keys = keys
        for key in self._keys:
            self._input_state.watchWithModifiers(self._keys[key], key)

        self._showbase.disableMouse()

        props = WindowProperties()
        props.setCursorHidden(True)

        self._showbase.win.requestProperties(props)

        self._showbase.taskMgr.add(self.update, "UpdateCameraTask" + str(self._instance))
    
    def destroy(self):
        self.disable()
        self._input_state.delete()

        del self

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        self._velocity = velocity
    
    @property
    def mouse_sensitivity(self):
        return self._mouse_sensitivity

    @mouse_sensitivity.setter
    def mouse_sensitivity(self, sensitivity):
        self._mouse_sensitivity = sensitivity

    def disable(self):
        self._showbase.taskMgr.remove("UpdateCameraTask" + str(self._instance))

        props = WindowProperties()
        props.setCursorHidden(False)

        self._showbase.win.requestProperties(props)            

    def update(self, task):
        dt = globalClock.getDt()
        
        # Get mouse movement for rotation
        md = self._showbase.win.getPointer(0)
        x = md.getX()
        y = md.getY()
        center_x = self._showbase.win.getXSize() // 2
        center_y = self._showbase.win.getYSize() // 2

        if self._showbase.win.movePointer(0, center_x, center_y):
            self._yaw = self._yaw - (x - center_x) * self._mouse_sensitivity
            self._pitch = self._pitch - (y - center_y) * self._mouse_sensitivity

        # Clamp the pitch to prevent camera flipping over
        self._pitch = max(-89, min(89, self._pitch))
        
        # Set the camera's orientation
        self._showbase.camera.setHpr(self._yaw, self._pitch, self._roll)
        
        # Access the camera's lens and set the focal length
        lens = self._showbase.cam.node().getLens()
        lens.setFocalLength(0.25)
        
        # Get the camera's position
        
        # Calculate the position increment
        pos_increment = self._velocity * dt
        
        # Handle keyboard input for movement
        if  self._input_state.isSet('forward'):
            self._showbase.camera.setY(self._showbase.camera, pos_increment)

        if  self._input_state.isSet('backward'):
            self._showbase.camera.setY(self._showbase.camera, -pos_increment)

        if  self._input_state.isSet('left'):
            self._showbase.camera.setX(self._showbase.camera, -pos_increment)

        if  self._input_state.isSet('right'):
            self._showbase.camera.setX(self._showbase.camera, pos_increment)

        if  self._input_state.isSet('up'):
            self._showbase.camera.setZ(self._showbase.camera, pos_increment)

        if  self._input_state.isSet('down'):
            self._showbase.camera.setZ(self._showbase.camera, -pos_increment)
        
        self.cam_pos = self._showbase.camera.getPos(self._showbase.render)
        # Apply gravity to the camera's position
        (self.cam_pos) += self._gravity * dt
        
        # Update the camera's position
        self._showbase.camera.setPos(self.cam_pos)
        return Task.cont
        
class MyApp(ShowBase):
    def Dmgbynpc(self, task):
        print('damage')
        self.healthpoints-=1
        print(self.healthpoints)
        
    def createwalls(self):
        self.wall_collision_node = CollisionNode('wall')
        self.wall_collision_node.addSolid(CollisionBox(Point3(22, -6.5, 32), 19, .5, 27))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-23.5, -6.5, 32), 19, .5, 27))
        self.wall_collision_node.addSolid(CollisionBox(Point3(0, -6.5, 35), 10, .5, 25))
        self.wall_collision_node.addSolid(CollisionBox(Point3(0, -63, 30), 48, .5, 27))
        self.wall_collision_node.addSolid(CollisionBox(Point3(41, -35, 32), .5, 28, 27))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-43, -35, 32), .5, 28, 27))
        self.wall_collision_node.addSolid(CollisionBox(Point3(0, -35, 2), 43, 28, 4.5))
        self.wall_collision_node.addSolid(CollisionBox(Point3(0, 0, 0), 15, 7, 2))
        self.wall_collision_node.addSolid(CollisionBox(Point3(14, -32, 9), .3, 15, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-17.5, -15, 9), 1.5, .3, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-25, -15, 9), 1.7, .3, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-15.75, -12.5, 9), .3, 6, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-15.75, -34, 9), .3, 11.5, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-15.75, -57.5, 9), .3, 5, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(14, -56.5, 9), .3, 6, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(13, -35, 9), 10, .3, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-23, -35, 9), 19, .3, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-25, -10, 9), .3, 5, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-33,-41, 9), .3, 5.5, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-33,-52.5, 9), .3, 2, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-38,-55, 9), 5, .3, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(23, -20.5, 9), .3, 14.5, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(27, -25, 9), 3.5, .3, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(37.5, -25, 9), 3.5, .3, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-13, -9, 7), 1, 1, 1))
        self.wall_collision_node.addSolid(CollisionBox(Point3(8.5, -33, 6), 4.5, 1, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-10, -33, 6), 4.5, 1, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-17.5, -30, 6), 1, 4, 4))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-36, -34.25, 6), 6, 3.25, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-38.75, -25.5 , 6), 4, 1.25, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-40, -12 , 6), 2, 4, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-28, -11 , 6), 1, 1, 1))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-18, -11 , 6), 1, 1, 1))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-34.5, -41.4 , 6), 1, 3.6, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-42, -54 , 6), 1.5, 1.5, 1))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-25.75, -40, 6), .75, .5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-22.5, -40, 6), .75, .5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-25.75, -46, 6), .75, .5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-22.5, -46, 6), .75, .5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-24.25, -42.75, 6), 3.5, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-18, -58, 6), 1, 5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-42, -59, 6), 1, 3, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-11, -37, 6), 5, 1, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(12, -37, 6), 1, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(11.25, -61.5, 6), 3.25, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-13.5, -61, 6), 1, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-1, -55, 6), 4.75, 2, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(6, -49, 6), 2, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-7, -49, 6), 2, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-.8, -49.25, 6), 2, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-.75, -43, 6), 4.5, 1.75, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(15.8, -59.5, 6), .8, 2.95, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(23, -58.7, 6), 2.3, 4, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(39, -58.5, 6), 1.6, 4.2, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(39, -40.4, 6), 1.6, 13.155, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(17.75, -36, 6), 2.95, 1.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(25, -29.5, 6), 1.3, 2.95, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(24.5, -21, 6), .7, 1, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(26.1, -12.75, 6), 2.8, 1.4, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(24.5, -21, 6), .7, 1, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(39.5, -10, 6), 1, 1, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(39.5, -20.4, 6), 1, 2.5, .75))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(14.7, -15, 5), Point3(14.7, -32, 19.2), Point3(22.9, -32, 19.2), Point3(22.9, -15, 5)))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-16, -35, 14), 31, 28, 4.95))
        self.wall_collision_node.addSolid(CollisionBox(Point3(28, -47.5, 14), 13.5, 15.5, 4.95))
        self.wall_collision_node.addSolid(CollisionBox(Point3(32, -18.51, 14), 10, 13.5, 5))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(22, -29, 19.2), Point3(22, -33, 19.2), (50, -33, 19.2),Point3(50, -29, 19.2)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(13.7, -32, 19.2), Point3(13.7, -67, 19.2), Point3(22.9, -67, 19.2), Point3(22.9, -32, 19.2)))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-10.8, -35, 21), 15.2, 5.9, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(6, -35, 21), 2, 4.5, .75))
        self.wall_collision_node.addSolid(CollisionBox(Point3(-28, -35, 21), 2, 4.5, .75))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(14.7, -32, 19.2), Point3(14.7, -36, 26), Point3(19, -36, 26), Point3(19, -32, 19.2)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(10, -36, 34), Point3(10, -40, 34), Point3(17, -40, 26), Point3(14, -36, 26)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(10, -29, 40), Point3(10, -39, 34), Point3(13.5, -36, 29), Point3(13.5, -29, 42)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(12, -27, 39), Point3(12, -32, 37), Point3(19, -34, 46), Point3(19, -28, 46)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(14, -31, 42), Point3(17, -37, 49), Point3(19, -37, 49), Point3(19, -31, 46)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(19, -32, 19.2), Point3(19, -36, 26), Point3(20.5, -36, 26), Point3(20.5, -32, 19.2)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(14, -36, 26), Point3(17, -40, 28), Point3(20.5, -36, 26)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(9, -37, 33), Point3(13, -40, 31), Point3(14, -36, 26)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(12.2, -28, 39), Point3(13.5, -36, 29), Point3(16, -33, 41.5)))
        self.wall_collision_node.addSolid(CollisionBox(Point3(19, -37.75, 20), 2, 3, 3))
        self.wall_collision_node.addSolid(CollisionBox(Point3(16, -38.5, 20), 3, 3.5, 3))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(20.5, -32, 19.2), Point3(20.5, -36, 26), Point3(20.5, -36, 29.2), Point3(20.5, -32, 26)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(10, -40, 34), Point3(10, -40, 39), Point3(17, -40, 29.2), Point3(17, -40, 26)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(17, -40, 26), Point3(17, -40, 29.2), Point3(20.5, -36, 29.2), Point3(20.5, -36, 26)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(8.75, -37, 32), Point3(8.75, -37, 39), Point3(10, -40, 39), Point3(10, -40, 34)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(10, -29, 40), Point3(10, -29, 46), Point3(8.75, -37, 39), Point3(8.75, -37, 32)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(12, -27, 40), Point3(12, -27, 46), Point3(10, -29, 46), Point3(10, -29, 40)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(19, -28, 46), Point3(19, -28, 52), Point3(12, -27, 46), Point3(12, -27, 40)))
        self.wall_collision_node.addSolid(CollisionPolygon(Point3(19, -28, 46), Point3(19, -34, 46), Point3(19, -34, 52), Point3(19, -28, 52)))
        self.wall_collision_node.addSolid(CollisionBox(Point3(14.6, -33.75, 17), .7, .7, 25))

        self.wall_collision_node_path = self.render.attachNewNode(self.wall_collision_node)
#        self.wall_collision_node_path.show()
    def setAI(self):
        self.npcs = {}
        self.aidotdict = {}
        self.Aichardict = {}
        self.Aicharbehaviorsdict = {}
        self.colliderdict = {}
        self.Aiworld = AIWorld(self.render)
        for i in range(4):
            npc_name = f"npc{i}"
            aidotname = f"aidot{i}"
            aicharname = f"aichar{i}"
            aicharbehaviorname = f"aibehavior{i}"
            collidername = f"collider{i}"
            self.npcs[npc_name] = self.loader.loadModel(r"models/newghost.glb")
            self.aidotdict[aidotname] = self.loader.loadModel(r'models/aidotupdater.glb')
            self.aidotdict[aidotname].reparentTo(self.render)
            self.npcs[npc_name].reparentTo(self.render)
            self.npcs[npc_name].setPos(i*10, i*5, 10)
            self.aidotdict[aidotname].setPos(i*10, 0, 10)
            self.npcs[npc_name].lookAt(self.camera)
            self.npcs[npc_name].setHpr(0,90,0)
            self.npcs[npc_name].setScale(2,2,2)
            self.colliderdict[collidername] = CollisionNode(npc_name)
            self.colliderdict[collidername].addSolid(CollisionSphere(0, 0, 0, 1))
            self.Aichardict[aicharname] = AICharacter(f"npc{i}", self.aidotdict[aidotname], 100, 0.05, 5)
            self.Aiworld.addAiChar(self.Aichardict[aicharname])
            self.Aicharbehaviorsdict[aicharbehaviorname] = self.Aichardict[aicharname].getAiBehaviors()
            self.Aicharbehaviorsdict[aicharbehaviorname].pursue(self.camera)
            self.Aicharbehaviorsdict[aicharbehaviorname].arrival(10) #arrival
        #AI World update
        taskMgr.add(self.Update,"Update")

    #to update the AIWorld
    def Update(self,task):
        for npc, aidot in zip(self.npcs.values(), self.aidotdict.values()):
            npc.setH(aidot.getH())
            aidot.setZ(8)
            npc.setPos(aidot.getPos())
        # Separation logic to prevent NPC overlap
        separation_threshold = 7  # Minimum distance between NPCs
        repelling_force = 2  # Strength of the repelling force

        npc_positions = {name: npc.getPos(self.render) for name, npc in self.npcs.items()}
        for name_a, pos_a in npc_positions.items():
            for name_b, pos_b in npc_positions.items():
                if name_a != name_b:
                    distance = (pos_a - pos_b).length()
                    if distance < separation_threshold:
                    # Calculate repelling direction
                        direction = pos_a - pos_b
                        direction.normalize()
                    # Apply the repelling force
                        new_pos = pos_a + direction * repelling_force
                        self.npcs[name_a].setPos(new_pos)
        self.bar['value'] = self.healthpoints
        self.Aiworld.update()
        return Task.cont
    def __init__(self):
        super().__init__()
        self.healthpoints=100
        self.bar = DirectWaitBar(text="HP", value=100, pos=(-.5, -15, -.8))
        self.bar['barColor'] = (0, 2, 0, 2)
        self.bar['text_scale'] = .05
        self.bar['frameSize'] = (-.5, .5, -.035, .02)
        self.bar['barRelief']= DGG.RAISED        
        self.Manor = self.loader.loadModel(r"models/HauntedMansion.glb")
        self.Manor.reparentTo(self.render)
        self.Manor.setHpr(90, 90, 90)
        self.cameramodel = self.loader.loadModel(r'models/aidotupdater.glb')
        self.cameramodel.reparentTo(self.camera)

        self.miniboss = self.loader.loadModel(r'models/monster_with_glowing_eyes.glb')
        self.miniboss.setScale(15,15,15)
        self.miniboss.setHpr(0,90,0)
        self.miniboss.setPos(0, 10, 10)
        self.miniboss.reparentTo(self.render)
        cam_controller = CameraControllerBehaviour(self.camera, velocity=9, mouse_sensitivity=.2)
        cam_controller.setup(keys={'w':"forward",
            's':"backward",
            'a':"left",
            'd':"right",
            'space':"up",
            'e':"down"})
        # Create a collision traverser
        self.cTrav = CollisionTraverser()
        # Create a collision handler
        self.pusher = CollisionHandlerPusher()
        self.pusher.addInPattern("%fn-into-wall")
        self.setAI()
        for npc, collidername in zip(self.npcs.values(), self.colliderdict.values()):
            self.npcColliderpath = npc.attachNewNode(collidername)
        self.npcintocam = CollisionHandlerEvent()
        self.npcintocam.addInPattern('into-camera')
        self.cTrav.removeCollider(self.npcColliderpath)
        self.cTrav.addCollider(self.npcColliderpath, self.npcintocam)
        # Create a collision node for the camera
        camera_collision_node = CollisionNode('camera')
        camera_collision_node.addSolid(CollisionSphere(0, 0, 0, 1.25))
        camera_collision_node_path = self.camera.attachNewNode(camera_collision_node)
        self.cTrav.addCollider(camera_collision_node_path, self.pusher) 
        self.pusher.addCollider(camera_collision_node_path, self.camera)

        self.accept('into-camera', self.Dmgbynpc)
        # Create a collision node for a wall
        MyApp.createwalls(self)

w = MyApp()
base.run()