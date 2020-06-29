import random
import copy
import numpy as np
from uuid import uuid4


def triangle_wave(x, p, max, min):
    offset = min
    a = max - min
    return ((2.0*a)/p) * abs( (x % p) - (p/2.0) ) - ((2.0*a)/4.0) + offset


def get_n_distinct_group_colors(n):
    hues = np.arange(0, 255, (255//n))

    colors = []
    for i in range(len(hues)):
        hue = int(hues[i])
        sat = int(triangle_wave(i, 5, 255, 150))
        val = int(triangle_wave(i, 7, 255, 150))
        colors.append( (hue, sat, val ))

    fills = list(colors)
    strokes = list(colors)

    random.shuffle(fills)
    random.shuffle(strokes)

    result = []
    for i in range(len(fills)):
        result.append((fills[i], strokes[i]))
    return result


class Particle:
    def __init__(self, group, is_child=False, position=None):
        self.group = group
        self.position = position
        self.is_child = is_child
        self._id = uuid4()

    def __eq__(self, other):
        result = False

        if isinstance(other, Particle):
            result = other._id == self._id
        return result

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self._id)


class Simulation:

    def __init__(self, graph, particles, repulsion_factor, attraction_factor, orphan_penalty):
        self._graph = graph
        self._particles = particles
        self._repulsion_factor = repulsion_factor
        self._attraction_factor = attraction_factor
        self._orphan_penalty = orphan_penalty

        distances = set()
        for node_a in self._graph.get_nodes():
            for node_b in self._graph.get_nodes():

                if node_a == node_b:
                    continue

                distances.add(graph.get_weight(node_a, node_b))

        distances = list(distances)
        distances.sort()
        self._min_node_distances = [distances[0], distances[1]]

        self._groups = dict()
        for particle in self._particles:

            if particle.group not in self._groups:
                self._groups[particle.group] = (list(), list())

            if particle.is_child:
                self._groups[particle.group][1].append(particle)
            else:
                self._groups[particle.group][0].append(particle)

        self._occupation_map = dict()
        for node in self._graph.get_nodes():
            self._occupation_map[node] = False

    def init_particles(self):
        """
        Set random positions for all the particles
        :return:
        """
        nodes = list(self._graph.get_nodes())
        random.shuffle(nodes)

        if len(nodes) < len(self._particles):
            raise IndexError("More Passengers Than Seats")

        for particle in self._particles:
            node = nodes.pop()
            particle.position = node
            self._occupation_map[node] = True
        self._update_image()

    def _get_group_names(self):
        return self._groups.keys()

    def _update_image(self):
        """
        Update and display the image produced by the graph to show the current system
        :return: None
        """

        particles = self._particles.copy()
        group_colors = {}

        groups = self._get_group_names()
        available_colors = get_n_distinct_group_colors(len(groups))
        for group in groups:
            group_colors[group] = available_colors.pop()

        for node in self._graph.get_nodes():
            self._graph.set_color(node, None, None)

            for particle in particles:

                if node == particle.position:
                    self._graph.set_color(node,
                                          group_colors[particle.group][0],
                                          group_colors[particle.group][1],
                                          accent=particle.is_child)
                    particles.remove(particle)
                    break

    def _get_group_orphan_penalty(self, group, test_particle=None, test_particle_position=None):
        penalty = 0

        group_children = set(self._groups[group][1])
        group_adults = set(self._groups[group][0])

        # for particle in self._particles:
        #
        #     if group == particle.group:
        #
        #         if (particle == test_particle) and (test_particle_position is not None):
        #             sample = Particle( particle.group, particle.is_child)
        #             sample.position = test_particle_position
        #         else:
        #             sample = particle
        #
        #         if sample.is_child:
        #             group_children.add(sample)
        #         else:
        #             group_adults.add(sample)

        for child in group_children:
            distance_from_adult = 9999999
            vector = (0, 0)

            for adult in group_adults:
                dist = self._graph.get_weight(child.position, adult.position)
                if dist < distance_from_adult:
                    distance_from_adult = dist
                    vector = self._graph.get_direction_vector(child.position, adult.position)

            # Adult and child are seated adjacent (no penalty)
            if distance_from_adult <= self._min_node_distances[0]:
                pass
            elif distance_from_adult <= self._min_node_distances[1]:

                if vector[0] < 0:
                    # Child is behind adult
                    penalty += self._orphan_penalty * 0.5
                else:
                    # Child is in front of adult
                    penalty += self._orphan_penalty * 0.25

            # Child is Orphaned Apply Penalty
            else:
                penalty += self._orphan_penalty

        return penalty

    def _get_force(self, p1, p2):
        """
        Get the force (Culomb's law) between two particle
        [An attractive force has a negative magnitude]
        :param p1: the first particle
        :param p2: the second particle
        :return: The singed force between the two particles
        """

        if p1.position == p2.position:
            # Don't let particles overlap
            return 10000

        if p1.group == p2.group:
            f = self._attraction_factor * 1.0 / ((self._graph.get_weight(p1.position, p2.position)) ** 2)
        else:
            f = self._repulsion_factor * 1.0 / ((self._graph.get_weight(p1.position, p2.position)) ** 2)
        return f

    def _get_energy(self, particle, position=None):
        """
        Get the energy of a particle at a given position
        Energy is defined as the sum of all forces acting on a particle
        :param particle: the particle to evaluate
        :param position: [Optional] Provide a new position for the particle
        :return: The energy of the particle at the position
        """

        if position is None:
            position = particle.position

        p_new = Particle(particle.group)
        p_new.position = position

        energy = 0

        # Get sum of all forces
        for p_test in self._particles:

            if p_test == particle:
                # Don't test against the original particle
                continue

            energy += self._get_force(p_new, p_test)

        # Add group orphan penalty
        energy += self._get_group_orphan_penalty(particle.group, test_particle=particle, test_particle_position=position)

        return energy

    def _get_system_energy(self):
        """
        Get the total energy of the system
        :return: the system's total energy
        """
        system_energy = 0
        for particle in self._particles:
            system_energy += self._get_energy(particle)

        return system_energy

    def _get_particles_by_energy(self, particles):
        """
        Get a dictionary of particles keyed by their energy
        :param particles: a set of particles
        :return: a dictionary
        """
        particle_energies = dict()

        for particle in particles:
            energy = self._get_energy(particle)
            particle_energies[energy] = particle

        return particle_energies

    def _get_free_positions(self):
        """
        Get a set of free positions in the graph
        :return: a set of positions
        """
        nodes = self._graph.get_nodes()
        particles = self._particles.copy()
        positions = set()

        for node in self._occupation_map:
            if not self._occupation_map[node]:
                positions.add(node)

        # for node in nodes:
        #     particle_found = False
        #
        #     for p in particles:
        #         if node == p.position:
        #             particles.remove(p)
        #             particle_found = True
        #             break
        #
        #     if not particle_found:
        #         positions.add(node)
        return positions

    def run_iteration(self, show_result=False):
        """
        Run a single iteration of the simulation
            1. Retrive the particle with the highest energy
            2. Move it the position that minimizes system energy
            3. Update the system to reflect the new position
            4. Repeat for all particles in the system
        :param show_result: [Optional] If true display n image fo the graph after the iteration
        :return: None
        """
        import time

        todo = set(self._particles.copy())

        while len(todo) > 0:

            # Find the particle with the highest energy
            particle_energies = self._get_particles_by_energy(todo)
            keys = sorted(particle_energies)
            test_particle = particle_energies[keys[0]]
            todo.remove(test_particle)

            # Find the best position to lower the energy of the particle
            min_energy = self._get_energy(test_particle)
            best_position = test_particle.position

            # Force children out of the front seats (they can sometimes initialize there)
            if best_position in self._graph.front_seats and test_particle.is_child:
                min_energy = 99999

            for position in self._get_free_positions():

                # Test if this is a valid seat for a child
                if position in self._graph.front_seats and test_particle.is_child:
                    continue

                energy = self._get_energy(test_particle, position=position)
                if energy < min_energy:
                    min_energy = energy
                    best_position = position

            # Update the particle's position in the master set
            for particle in self._particles:
                if particle == test_particle:
                    self._occupation_map[particle.position] = False
                    self._occupation_map[best_position] = True
                    particle.position = best_position
                    break

        # Update the graph image and display it (if applicable)
        self._update_image()

        if show_result:
            self._graph.show_graph()

    def run_sim(self, show_result=False, max_iterations=50, debug=False):

        if debug:
            print("===================================")

        for i in range(max_iterations):

            if debug:
                print("Running iteration: %i" % i)

            old_particles = copy.deepcopy(self._particles)  # Copy of particles to test for convergence
            self.run_iteration(show_result=False)

            if debug:
                print("\tSystem Energy: %f" % self._get_system_energy())

            if show_result:
                self._graph.show_graph()

            # Test for convergence
            new_particles = self._particles
            converged = True
            for new_p in new_particles:

                changed_position = True

                # Has the particle stayed in the same position?
                for old_p in old_particles:

                    if new_p == old_p and new_p.position == old_p.position:
                        # Yes: Keep testing for convergence
                        #      No need to keep searching for the particle
                        old_particles.remove(old_p)
                        changed_position = False
                        break

                # No: Stop testing for convergence (we have not converged)
                if changed_position:
                    converged = False
                    break

            # If the system has converged (found a local minimum solution) stop the simulation
            if converged:
                if debug:
                    print("Converged!")
                break

        if debug:
            print("Simulation Complete")
        return self._get_system_energy(), self._particles











