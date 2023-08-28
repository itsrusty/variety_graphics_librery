import turtle
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader

# ? initialization to ursina
app = Ursina()

# TODO: figure alternative
def figure_alternative():

    # Configuración de la ventana
    screen = turtle.Screen()
    screen.bgcolor("white")
    screen.title("Cubo con Turtle")

    # Configuración de la pluma
    pen = turtle.Turtle()
    pen.speed(1)
    pen.pensize(2)

    # Función para dibujar un cuadrado
    def draw_square(size):
        for _ in range(4):
            pen.forward(size)
            pen.left(90)

    # Función para dibujar un cubo
    def draw_cube(side_length):
        for _ in range(4):
            pen.forward(side_length)
            pen.left(45)
        pen.goto(pen.xcor() - side_length / 2, pen.ycor() + side_length / 2)
        for _ in range(4):
            pen.forward(side_length)
            pen.left(45)
        pen.goto(pen.xcor() - side_length / 2, pen.ycor() - side_length / 2)
        pen.setheading(0)
        pen.forward(side_length)
        pen.goto(pen.xcor() + side_length / 2, pen.ycor() + side_length / 2)
        pen.setheading(0)
        pen.forward(side_length)
        pen.goto(pen.xcor(), pen.ycor() - side_length)

    # Dibujar el cubo
    cube_side_length = 100
    pen.penup()
    pen.goto(-cube_side_length / 2, cube_side_length / 2)
    pen.pendown()
    draw_cube(cube_side_length)

    # Ocultar la pluma y mostrar la ventana
    pen.hideturtle()
    turtle.done()
    
    
# TODO: draw a cube
def draw_cube():
    # Crear una entidad cubo
    cube = Entity(model='cube', texture='white_cube', color=color.red)

    # Configurar la cámara
    camera.position = (0, 0, -5)
    camera.rotation_x = 0

    def update():
        # Rotar el cubo
        cube.rotation_x += 1
        cube.rotation_y += 1
        cube.rotation_z += 1

    # Ejecutar la aplicación
    app.run()

# TODO: draw a smile person
def draw_face():
    random.seed(0)
    Entity.default_shader = lit_with_shadows_shader

    ground = Entity(model='plane', collider='box', scale=64, texture='grass', texture_scale=(4,4))

    editor_camera = EditorCamera(enabled=False, ignore_paused=True)
    player = FirstPersonController(model='cube', z=-10, color=color.orange, origin_y=-.5, speed=8, collider='box')
    player.collider = BoxCollider(player, Vec3(0,1,0), Vec3(1,2,1))

    gun = Entity(model='cube', parent=camera, position=(.5,-.25,.25), scale=(.3,.2,1), origin_z=-.5, color=color.red, on_cooldown=False)
    gun.muzzle_flash = Entity(parent=gun, z=1, world_scale=.5, model='quad', color=color.yellow, enabled=False)

    shootables_parent = Entity()
    mouse.traverse_target = shootables_parent


    for i in range(16):
        Entity(model='cube', origin_y=-.5, scale=2, texture='brick', texture_scale=(1,2),
            x=random.uniform(-8,8),
            z=random.uniform(-8,8) + 8,
            collider='box',
            scale_y = random.uniform(2,3),
            color=color.hsv(0, 0, random.uniform(.9, 1))
            )

    def update():
        if held_keys['left mouse']:
            shoot()

    def shoot():
        if not gun.on_cooldown:
            # print('shoot')
            gun.on_cooldown = True
            gun.muzzle_flash.enabled=True
            from ursina.prefabs.ursfx import ursfx
            ursfx([(0.0, 0.0), (0.1, 0.9), (0.15, 0.75), (0.3, 0.14), (0.6, 0.0)], volume=0.5, wave='noise', pitch=random.uniform(-13,-12), pitch_change=-12, speed=3.0)
            invoke(gun.muzzle_flash.disable, delay=.05)
            invoke(setattr, gun, 'on_cooldown', False, delay=.15)
            if mouse.hovered_entity and hasattr(mouse.hovered_entity, 'hp'):
                mouse.hovered_entity.hp -= 10
                mouse.hovered_entity.blink(color.red)


    from ursina.prefabs.health_bar import HealthBar

    class Enemy(Entity):
        def __init__(self, **kwargs):
            super().__init__(parent=shootables_parent, model='cube', scale_y=2, origin_y=-.5, color=color.light_gray, collider='box', **kwargs)
            self.health_bar = Entity(parent=self, y=1.2, model='cube', color=color.red, world_scale=(1.5,.1,.1))
            self.max_hp = 100
            self.hp = self.max_hp

        def update(self):
            dist = distance_xz(player.position, self.position)
            if dist > 40:
                return

            self.health_bar.alpha = max(0, self.health_bar.alpha - time.dt)


            self.look_at_2d(player.position, 'y')
            hit_info = raycast(self.world_position + Vec3(0,1,0), self.forward, 30, ignore=(self,))
            # print(hit_info.entity)
            if hit_info.entity == player:
                if dist > 2:
                    self.position += self.forward * time.dt * 5

        @property
        def hp(self):
            return self._hp

        @hp.setter
        def hp(self, value):
            self._hp = value
            if value <= 0:
                destroy(self)
                return

            self.health_bar.world_scale_x = self.hp / self.max_hp * 1.5
            self.health_bar.alpha = 1

    # Enemy()
    enemies = [Enemy(x=x*4) for x in range(4)]


    def pause_input(key):
        if key == 'tab':    # press tab to toggle edit/play mode
            editor_camera.enabled = not editor_camera.enabled

            player.visible_self = editor_camera.enabled
            player.cursor.enabled = not editor_camera.enabled
            gun.enabled = not editor_camera.enabled
            mouse.locked = not editor_camera.enabled
            editor_camera.position = player.position

            application.paused = editor_camera.enabled

    pause_handler = Entity(ignore_paused=True, input=pause_input)


    sun = DirectionalLight()
    sun.look_at(Vec3(1,-1,-1))
    Sky()

    app.run()
    

# TODO: triangle
from ursina import *

def draw_triangle():
    # Crear vértices del triángulo
    vertices = [
        Vec3(0, 0.5, 0),   # Vértice superior
        Vec3(-0.5, -0.5, 0),  # Vértice inferior izquierdo
        Vec3(0.5, -0.5, 0),   # Vértice inferior derecho
    ]

    # Crear triángulo
    triangle_entity = Entity(model=Mesh(vertices=vertices, mode='triangle'), color=color.blue)

    # Ejecutar la aplicación
    app.run()
    
# TODO: balls
def draw_ball():
 ball = Entity(model='sphere', color=color.random_color(), scale=1.0)

 # Función para actualizar el movimiento de la pelota
 def update():
     speed = 0.1  # Velocidad de movimiento de la pelota 

     if held_keys['w']:
         ball.y += speed
     if held_keys['s']:
         ball.y -= speed
     if held_keys['a']:
         ball.x -= speed
     if held_keys['d']:
         ball.x += speed 

 # Ejecutar la aplicación
 app.run()