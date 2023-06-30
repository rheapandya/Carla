
# initialize traffic manager (tm) and create traffic randomly distributed around the city
import carla
import random

# connect to the client and retrieve the world object
client = carla.Client('localhost', 2000)
world = client.get_world()

# set up simulator in synchronous mode
settings = world.get_settings()
# enables synchronous mode
settings.synchronous_mode = True 
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# set up traffic manager in synchronus mode
traffic_manager = client.get_trafficmanager()
traffic_manager.set_synchronous_mode(True)

# set a seed so behaviour can be repeated if necessary
traffic_manager.set_random_device_seed(0)
random.seed(0)

# see what we do
spectator = world.get_spectator()


# getting predefined spawn points
spawn_points = world.get_map().get_spawn_points()

# # visually seeing the spawn points with numbers
# # drawing the spawn point locations as numbers in the map
# for i, spawn_point in enumerate(spawn_points):
#     world.debug.draw_string(spawn_point.location, str(i), life_time = 10)

# # run simulator to fly spectator in synchronus mode
# while True: 
#     world.tick()


# select models from blueprint library
models = ['dodge', 'audi', 'model3', 'mini', 'mustang', 'lincoln', 'prius', 'nissan', 'crown', 'impala']
blueprints = []
# getting vehicles that correspond to model names from blueprint (getting the actual object not just the name)
for vehicle in world.get_blueprint_library().filter('*vehicle*'):
    if any(model in vehicle.id for model in models):
        blueprints.append(vehicle)

# set max number of vehicles + list to put vehicles spawned
max_vehicles = 50
max_vehicles = min([max_vehicles, len(spawn_points)])
vehicles = []

# take a random sample of the spawn spoints and spawn some vehicles
for i, spawn_point in enumerate(random.sample(spawn_points, max_vehicles)):
    temp = world.try_spawn_actor(random.choice(blueprints), spawn_point)
    if temp is not None:
        vehicles.append(temp)



# go through list of vehicle and give control to tm
for vehicle in vehicles:
    vehicle.set_autopilot(True)
    # randomly set probability that vehicle will ignore traffic lights
    traffic_manager.ignore_lights_percentage(vehicle, random.randint(0,50))


# create two coverging streams of traffic within town creating congestion
spawn_points = world.get_map().get_spawn_points()

#route 1
spawn_point_1 = spawn_points[32]
#create route 1 from the chosen spawn points
route_1_indices = [129, 28, 124, 33, 97, 119, 58, 154, 147]
route_1 = []
for ind in route_1_indices:
    route_1.append(spawn_points[ind].location)

#route 2
spawn_point_2 = spawn_points[149]
#create route 2 from the chosen spawn points
route_2_indices = [21, 76, 38, 34, 90, 3]
route_2 = []
for ind in route_2_indices:
    route_2.append(spawn_points[ind].location)

# print in map to see routes
world.debug.draw_string(spawn_point_1.location, 'Spawn point 1', life_time=30, color=carla.Color(255,0,0))
world.debug.draw_string(spawn_point_2.location, 'Spawn point 2', life_time=30, color=carla.Color(0,0,255))

for ind in route_1_indices:
    spawn_points[ind].location
    world.debug.draw_string(spawn_points[ind].location, str(ind), life_time=60, color=carla.Color(255,0,0))

for ind in route_2_indices:
    spawn_points[ind].location
    world.debug.draw_string(spawn_points[ind].location, str(ind), life_time=60, color=carla.Color(0,0,255))


# set delay between spawn times
spawn_delay = 20
counter = spawn_delay

# set max vehicles
max_vehicles = 200
# alternate between spawn points
alt = False

spawn_points = world.get_map().get_spawn_points()
while True:
    world.tick()
    n_vehicles = len(world.get_actors().filter('*vehicles*'))
    vehicle_bp = random.choice(blueprints)

    # spawn vehicle only after delay
    if counter == spawn_delay and n_vehicles < max_vehicles:
        #alternate spawn points
        if alt:
            vehicle = world.try_spawn_actor(vehicle_bp, spawn_point_1)
        else:
            vehicle = world.try_spawn_actor(vehicle_bp, spawn_point_2)

        if vehicle:
            vehicle.set_autopilot(True)

            # set parameters of TM vehicle control, no lane changes
            traffic_manager.update_vehicle_lights(vehicle, True)
            traffic_manager.random_left_lanechange_percentage(vehicle, 0)
            traffic_manager.random_right_lanechange_percentage(vehicle, 0)
            traffic_manager.auto_lane_change(vehicle, False)

            # Alternate between routes
            if alt:
                traffic_manager.set_path(vehicle, route_1)
                alt = False
            else:
                traffic_manager.set_path(vehicle, route_2)
                alt = True

            vehicle = None

        counter -= 1
    elif counter > 0:
        counter -= 1
    elif counter == 0:
        counter = spawn_delay
        








# # run simulation to inspect result
# while True: 
#     world.tick()