import json
import copy


class BoatSettings:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.image_file = data['image_file']

    def get_data(self):
        return {'id': self.id,
                'name': self.name,
                'image_file': self.image_file}


class SimSettings:

    def __init__(self, data):
        self.max_iterations = data['max_iterations']
        self.trials = data['trials']
        self.attractive_force = data['attractive_force']
        self.repulsive_force = data['repulsive_force']
        self.orphan_penalty = data['orphan_penalty']

    def get_data(self):
        return {'max_iterations': self.max_iterations,
                'trials': self.trials,
                'attractive_force': self.attractive_force,
                'repulsive_force': self.repulsive_force,
                'orphan_penalty': self.orphan_penalty}


class Settings:

    def __init__(self):
        self._file_name = 'settings.json'
        self._boats = list()
        self._sim_settings = None

        with open(self._file_name, 'r') as file:
            data = file.read()

        settings_data = json.loads(data)

        boat_data = settings_data["boats"]
        for boat in boat_data:
            self._boats.append(BoatSettings(boat))

        self._sim_settings = SimSettings(settings_data['simulation'])

    def get_available_boats(self):
        return copy.copy(self._boats.copy())

    def update_boat(self, new_boat):

        for i in range(len(self._boats)):
            if self._boats[i].id == new_boat.id:
                self._boats[i] = new_boat
                break

    def get_sim_settings(self):
        return copy.copy(self._sim_settings)

    def update_sim_settings(self, sim_settings):
        self._sim_settings = sim_settings

    def save(self):
        data = dict()

        boat_data = list()
        for boat in self._boats:
            boat_data.append(boat.get_data())

        data["boats"] = boat_data
        data["simulation"] = self._sim_settings.get_data()

        with open(self._file_name, 'w') as file:
            json.dump(data, file)
