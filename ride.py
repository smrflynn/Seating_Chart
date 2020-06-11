import csv

import particle_simulation as ps


class Group:
    def __init__(self, first_name, last_name, confirmation_number):
        self.first_name = first_name
        self.last_name = last_name
        self.confirmation_number= confirmation_number
        self.passengers = set()
        self.adults = 0
        self.children = 0

    def __hash__(self):
        return hash(repr(self))

    def add_passenger(self, position=None, is_child=False):
        new_passenger = ps.Particle(self.confirmation_number, is_child=is_child, position=position)
        self.passengers.add(new_passenger)

        if is_child:
            self.children += 1
        else:
            self.adults += 1


class Trip:
    def __init__(self, manifest_file):
        self.ride_date = ""
        self.groups = set()
        self._load_manifest_file(manifest_file)

    def _load_manifest_file(self, manifest_file):

        with open(manifest_file) as csvfile:
            read_csv = csv.reader(csvfile)

            found_data_start = False
            for row in read_csv:

                if not found_data_start and len(row) > 1:
                    # Found the table header -- data begins after this
                    found_data_start = True
                    continue

                if found_data_start:

                    try:
                        ride_date = row[0]
                        first_name = row[1]
                        last_name = row[2]
                        group_name = row[3]
                        confirm_num = row[4]
                        adults = int(row[5])
                        children = int(row[6])
                        comps = int(row[7])
                        total = int(row[8])
                        payment = row[9]
                        reservation_date = row[10]
                        private_notes = row[11]
                        comments = row[12]
                        referal = row[13]
                        add_ons = row[14]

                        self.ride_date=ride_date

                        new_group = Group(first_name, last_name, confirm_num)

                        for adult in range(adults):
                            new_group.add_passenger(is_child=False)

                        for child in range(children):
                            new_group.add_passenger(is_child=True)

                        self.groups.add(new_group)

                    except:
                        # Extra row added by excel
                        pass

    def get_passengers(self):

        result = set()
        for group in self.groups:
            result = set.union(result, group.passengers)
        return result

    def print(self):
        print(self.to_string())

    def to_string(self, monolithic_string=True):
        result = list()

        result.append("Trip:")
        result.append("    Departure: %s" % self.ride_date)

        for group in self.groups:
            adults = 0
            children = 0
            seats = set()

            for passenger in group.passengers:
                if passenger.is_child:
                    children += 1
                else:
                    adults += 1
                seats.add(passenger.position)

            seats = list(seats)
            seats.sort()

            result.append("    Group:")
            result.append("        #: %s" % group.confirmation_number)
            result.append("        Name: %s, %s" % (group.last_name, group.first_name))
            result.append("        Adults: %d" % adults)
            result.append("        Children: %d" % children)


            if seats[0] is None:
                seats = "N/A"
            else:
                seats = " ,".join(seats)
            result.append("        Seats: %s" % seats)

        if monolithic_string:
            result = "\n".join(result)
        return result


if __name__ == '__main__':
    trip = Trip('2020-6-6_13_00_manifest.csv')
    trip.print()
    print(trip.get_passengers())
