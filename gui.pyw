from tkinter import Tk
from tkinter import Frame, Label, Menu, Button, Entry, Scrollbar, Listbox
from tkinter import filedialog as fd
from tkinter import N, E, S, W, END, LEFT, RIGHT, BOTH, BOTTOM, Y, HORIZONTAL
from tkinter import messagebox, Toplevel, Message, StringVar, TclError
from tkinter.ttk import Progressbar

from PIL import Image, ImageTk
import cv2

import graph
import particle_simulation as ps
import ride
import pdf
import settings

settings_file = settings.Settings()

trip = None
trials = settings_file.get_sim_settings().trials
attractive_force = settings_file.get_sim_settings().attractive_force
repulsive_force = settings_file.get_sim_settings().repulsive_force
orphan_penalty = settings_file.get_sim_settings().orphan_penalty

boat_img = None
boat_init_graph_function = None
result_img_name = "result.png"


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        # Config menu
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Export", command=self._export)
        file_menu.add_command(label="Settings", command=display_settings)
        file_menu.add_command(label="Exit", command=self._exit_program)
        menu.add_cascade(label="File", menu=file_menu)

        sim_menu = Menu(menu, tearoff=0)
        sim_menu.add_command(label="Load Trip", command=self._get_csv_file)
        sim_menu.add_command(label="Run Simulation", command=self._run_simulation)
        menu.add_cascade(label="Simulation", menu=sim_menu)

        boat_menu = Menu(sim_menu, tearoff=0)
        boat_menu.add_command(label="Rogue Wave", command=self._update_boat_rw)
        boat_menu.add_command(label="Gale Force", command=self._update_boat_gf)
        boat_menu.add_command(label="Island Girl", command=self._update_boat_ig)

        sim_menu.add_cascade(label="Boat", menu=boat_menu)

        # config results frame
        self.result_frame = Frame(self)

        self.result_frame.pack(side=LEFT, pady=10, fill=BOTH, expand=True)

        self.result_frame_scroll = Scrollbar(self.result_frame)
        self.result_frame_scroll.pack(side=RIGHT, fill=Y)

        self.result_list = Listbox(self.result_frame, yscrollcommand=self.result_frame_scroll.set)
        self.result_list.insert(END, "Load CSV file to view results")
        self.result_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.result_frame_scroll.config(command=self.result_list.yview)

        # config image
        self.img = Label(self)
        self.img.pack(side=RIGHT, padx=10, pady=10, expand=False)
        self._update_boat_rw()


    @staticmethod
    def _exit_program():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()

    def _update_boat_rw(self):
        global settings_file
        boats = settings_file.get_available_boats()

        boat = None
        for vessel in boats:
            if vessel.id == 1:
                boat = vessel
                break

        set_boat(boat)
        self._load_img(boat.image_file)

    def _update_boat_gf(self):
        global settings_file
        boats = settings_file.get_available_boats()

        boat = None
        for vessel in boats:
            if vessel.id == 2:
                boat = vessel
                break
        set_boat(boat)
        self._load_img(boat.image_file)

    def _update_boat_ig(self):
        global settings_file
        boats = settings_file.get_available_boats()

        boat = None
        for vessel in boats:
            if vessel.id == 3:
                boat = vessel
                break
        set_boat(boat)
        self._load_img(boat.image_file)

    def _export(self):
        global trip

        if trip is None:
            messagebox.showerror('Error', 'No trip manifest csv file loaded')
            return

        file_name = fd.asksaveasfilename(filetypes=(("pdf", ".pdf"),))

        if len(file_name.strip()) == 0:
            messagebox.showerror('Error', 'No save name given')
            return

        try:
            pdf.generate_pdf(file_name, trip, result_img_name)

        except Exception as e:
            messagebox.showerror('Error', 'Unable to generate PDF! Make sure you ran the simulation and a valid CSV file was selected')

    def _load_img(self, filepath):
        load = Image.open(filepath)
        render = ImageTk.PhotoImage(load)
        self.img.configure(image=render)
        self.img.image = render

    def _update_results(self):
        global trip
        self.result_list.destroy()

        self.result_list = Listbox(self.result_frame, yscrollcommand=self.result_frame_scroll.set)

        results = trip.to_string(monolithic_string=False)

        for entry in results:
            self.result_list.insert(END, entry)

        self.result_list.pack(side=LEFT, fill=BOTH, expand=True)
        self.result_frame_scroll.config(command=self.result_list.yview)

    def _get_csv_file(self):
        global trip

        file_name = fd.askopenfilename(filetypes=(("csv", ".csv"),))
        trip = ride.Trip(file_name)
        self._update_results()

    def _destroy_sim_progress(self):
        result = messagebox.askyesno('Warning', 'Are you sure you want to halt the simulation?')
        if result:
            self._progress_window.destroy()

    def _run_simulation(self):
        global trip

        if trip is None:
            messagebox.showerror('Error', 'No trip manifest csv file loaded')
            return

        self._progress_window = Toplevel()
        self._progress_window.title("Simulation Progress")
        self._progress_window.geometry("320x100")
        self._progress_window.protocol("WM_DELETE_WINDOW", self._destroy_sim_progress)
        self._progress_window.grab_set()

        progress_window_msg = Message(self._progress_window, text="0%%", width=100)
        progress_window_msg.pack()

        progress_bar = Progressbar(self._progress_window, orient=HORIZONTAL, length=300, mode='determinate')
        progress_bar['maximum'] = trials
        progress_bar.pack(pady=10)
        progress_val = 0
        progress_bar['value'] = progress_val
        progress_bar.update_idletasks()

        self._progress_window.update()
        self._progress_window.update_idletasks()

        passengers = trip.get_passengers()

        boat_graph = boat_init_graph_function(boat_img)

        try:
            sim = ps.Simulation(boat_graph, passengers, repulsive_force, attractive_force, orphan_penalty)
        except IndexError as e:
            messagebox.showerror('Error', 'There are more passengers than seats!')
            self._progress_window.destroy()
            return

        min_energy = 0xFFFFFFFF
        result_img = None

        for progress_val in range(trials):
            sim.init_particles()
            energy = sim.run_sim(show_result=False, max_iterations=50, debug=False)
            img = boat_graph.get_graph_image()

            if energy < min_energy:
                energy = min_energy
                result_img = img

            try:
                progress_bar['value'] = progress_val + 1
                progress_window_msg.configure(text="%.2f%%" % (float(progress_val)/float(trials) * 100.0))
                progress_bar.update_idletasks()
                self._progress_window.update()
                self._progress_window.update_idletasks()

            except TclError as e:
                # The window was destroyed
                # Halt the simulation
                return

        self._progress_window.destroy()
        cv2.imwrite(result_img_name, result_img)
        self._load_img(result_img_name)
        self._update_results()




def display_settings():
    global settings_file, settings_window, settings_max_itr_var, \
        settings_trials_var, settings_rep_f_var, settings_attr_f_var, \
        settings_orphan_f_var

    settings_window = Toplevel()
    settings_window.title("Settings")
    settings_window.grab_set()

    frame = Frame(settings_window)
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    settings_window.columnconfigure(0, weight=1)
    settings_window.rowconfigure(0, weight=1)

    sim_settings = settings_file.get_sim_settings()

    settings_max_itr_var.set(str(sim_settings.max_iterations))
    settings_trials_var.set(str(sim_settings.trials))
    settings_attr_f_var.set(str(sim_settings.attractive_force))
    settings_rep_f_var.set(str(sim_settings.repulsive_force))
    settings_orphan_f_var.set(str(sim_settings.orphan_penalty))

    trials_entry = Entry(frame, width=7, textvariable=settings_trials_var)
    trials_entry.grid(column=2, row=1, sticky=E)

    max_iterations_entry = Entry(frame, width=7, textvariable=settings_max_itr_var)
    max_iterations_entry.grid(column=2, row=2, sticky=E)

    attractive_force_entry = Entry(frame, width=7, textvariable=settings_attr_f_var)
    attractive_force_entry.grid(column=2, row=3, sticky=E)

    repulsive_force_entry = Entry(frame, width=7, textvariable=settings_rep_f_var)
    repulsive_force_entry.grid(column=2, row=4, sticky=E)

    orphan_penalty_entry = Entry(frame, width=7, textvariable=settings_orphan_f_var)
    orphan_penalty_entry.grid(column=2, row=5, sticky=E)

    Label(frame, text="Trials:").grid(column=1, row=1, sticky=W)
    Label(frame, text="Max Iterations:").grid(column=1, row=2, sticky=W)
    Label(frame, text="Attractive Force:").grid(column=1, row=3, sticky=W)
    Label(frame, text="Repulsive Force:").grid(column=1, row=4, sticky=W)
    Label(frame, text="Orphan Penalty:").grid(column=1, row=5, sticky=W)

    Button(frame, text="Save", command=save_settings).grid(column=1, row=6, sticky=W)
    Button(frame, text="Cancel", command=settings_window.destroy).grid(column=2, row=6, sticky=E)

    for child in frame.winfo_children(): child.grid_configure(padx=5, pady=5)


def save_settings(*args):
    global settings_file, settings_window, settings_max_itr_var, \
        settings_trials_var, settings_rep_f_var, settings_attr_f_var, \
        settings_orphan_f_var

    sim_settings = settings_file.get_sim_settings()

    try:
        tmp_max_iterations = int(settings_max_itr_var.get())
        tmp_trials = int(settings_trials_var.get())
        tmp_repulsive_force = float(settings_rep_f_var.get())
        tmp_attractive_force = float(settings_attr_f_var.get())
        tmp_orphan_penalty = float(settings_orphan_f_var.get())

        assert tmp_max_iterations > 0
        assert tmp_trials > 0

        sim_settings.max_iterations = tmp_max_iterations
        sim_settings.trials = tmp_trials
        sim_settings.repulsive_force = tmp_repulsive_force
        sim_settings.attractive_force = tmp_attractive_force
        sim_settings.orphan_penalty = tmp_orphan_penalty

    except ValueError as e:
        messagebox.showerror(title="ERROR", message="One or more values are not numbers!"
                                                            " Double check all entries before saving")
        return

    except AssertionError as e:
        messagebox.showerror(title="ERROR", message="Max Iterations and Trials must be positive numbers")
        return

    settings_file.update_sim_settings(sim_settings)
    settings_file.save()
    settings_window.destroy()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()


def set_boat(boat):
    global trip, boat_img, boat_init_graph_function
    boat_img = boat.image_file

    if boat.id == 1:
        boat_init_graph_function = graph.init_rouge_wave_graph
    if boat.id == 2:
        boat_init_graph_function = graph.init_gale_force_graph
    if boat.id == 3:
        boat_init_graph_function = graph.init_island_girl_graph


if __name__ == '__main__':
    root = Tk()
    app = Window(root)

    settings_max_itr_var = StringVar()
    settings_trials_var = StringVar()
    settings_rep_f_var = StringVar()
    settings_attr_f_var = StringVar()
    settings_orphan_f_var = StringVar()

    settings_window = None

    # Window Attributes
    root.wm_title("Seating Chart")
    root.geometry("1200x600")

    set_boat(settings_file.get_available_boats()[0])

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
