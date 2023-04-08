from math import sqrt
import tkinter as tk
from tkinter import simpledialog, ttk
import re, csv
import csv
from collections import defaultdict
import tkinter.font as tkFont
import heapq

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        
    def add_edge(self, u, v, w):
        if self.edge_exists(u, v):
            print(f"Edge ({u}, {v}) already exists in the graph.")
            return
        self.graph[u].append((v, w))
        
    def edge_exists(self, u, v):
        for vertex, weight in self.graph[u]:
            if vertex == v:
                return True
        return False
    def check_vertex(self,v):
        if v in self.graph:
            return False
        return True
    def add_vertex(self, v):
        self.graph[v] = []

    def delete_vertex(self,v):
        del self.graph[v]
    
    def build_from_csv(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                u, v, w = row['Origin'], row['Dest'], float(row['Distance'])
                if (self.edge_exists(u,v)):
                    continue
                self.add_edge(u, v, w)
    
    def print_graph(self):
        for u in self.graph:
            for v, w in self.graph[u]:
                print(f"({u} -> {v}, distance = {w:.2f})")
    def get_vertices(self):
        return list(self.graph.keys())
    def dijkstra_path(graph, start, end):
        """
        Find the shortest path between start and end vertices using Dijkstra's algorithm.
        """
        distances = {vertex: float('inf') for vertex in graph.get_vertices()}
        distances[start] = 0
        previous_vertices = {vertex: None for vertex in graph.get_vertices()}
        pq = [(0, start)]
        while len(pq) > 0:
            current_distance, current_vertex = heapq.heappop(pq)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, weight in graph.graph[current_vertex]:
                distance = current_distance + weight
                if neighbor in distances and distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(pq, (distance, neighbor))
        if previous_vertices[end] is None:
            return -1
        path = []
        current_vertex = end
        while current_vertex is not None:
            path.insert(0, current_vertex)
            current_vertex = previous_vertices[current_vertex]
        return path

class WorldMap:
    def __init__(self, master):
        self.graph = Graph()  # Composition relationship
        self.root = master
        self.root.title("World Map")
        self.root.configure(bg="#F5F5F5")
        self.canvas_width = 750
        self.canvas_height = 750
        # self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="#FFFFFF")
        self.canvas.grid(row=0, column=0, rowspan=4, padx=10, pady=10)
        self.world_map_img = tk.PhotoImage(file="Image.png")
        self.world_map_img = self.world_map_img.subsample(2)
        self.canvas.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.world_map_img)
        self.airport_markers = []
        self.airport_names = self.graph.get_vertices()
        self.create_widgets()
    
    def create_widgets(self):
        button_style = ttk.Style()
        button_style.configure("W.TButton", font=("Arial", 12), background="#87CEFA", foreground="black", width=15, padding=5)
        label_style = ttk.Style()
        label_style.configure("W.TLabel", font=("Arial", 12), background="#F5F5F5", foreground="#333333", padding=5)
        combobox_style = ttk.Style()
        combobox_style.configure("W.TCombobox", font=("Arial", 12), background="#FFFFFF", foreground="#333333", width=17, padding=5)
        dialog_style = ttk.Style()
        dialog_style.configure("W.TDialog", background="#F5F5F5")

        self.add_route_button = ttk.Button(self.root, text="Add Route", style="W.TButton", command=self.add_route)
        self.add_route_button.grid(row=0, column=1, padx=10, pady=10)

        self.route_label = ttk.Label(self.root, text="", style="W.TLabel")
        self.route_label.grid(row=0, column=2, padx=10, pady=10)

        self.delete_airport_button = ttk.Button(self.root, text="Delete Airport", style="W.TButton", command=self.delete_airport)
        self.delete_airport_button.grid(row=1, column=1, padx=10, pady=10)

        self.delete_label = ttk.Label(self.root, text="", style="W.TLabel")
        self.delete_label.grid(row=1, column=2, padx=10, pady=10)

        self.minimum_distance_ab = ttk.Button(self.root, text="Minimum Distance", style="W.TButton", command=self.minimum_cost_ab)
        self.minimum_distance_ab.grid(row=2, column=1, padx=10, pady=10)

        self.canvas.bind("<Button-1>", self.add_airport_marker)
    
    def open_label_in_new_window(self, label_text):
        new_window = tk.Toplevel()
        new_window.title('Label Window')
        new_window.geometry('300x150')
        new_window.configure(bg='#F5F5F5')

        # Set label font and size
        label_font = ('Arial', 14)

        # Add padding to the label
        pad_x = 20
        pad_y = 10

        # Create and pack label with desired text and styling
        label = tk.Label(new_window, text=label_text, font=label_font, bg='#F5F5F5', padx=pad_x, pady=pad_y)
        label.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)


    def is_valid_iata_code(self,code):
        """
        Check if the given code is a valid IATA code
        """
        pattern = re.compile(r'^[A-Z]{3}$')
        return pattern.match(code) is not None

    def check_existance(self, airport_name):
        if airport_name not in self.airport_names:
            self.airport_names.append(airport_name)
            return True
        else:
            return False
    def delete_text(self, text_id):
        self.canvas.after(3000, self.canvas.delete, text_id)
    def add_airport_marker(self, event):
        x, y = event.x, event.y
        airport_name = None
        while airport_name is None or airport_name not in self.airport_names:
            airport_name = simpledialog.askstring("Airport Name", "Enter name for airport:")
            if airport_name is None:
                return
            if airport_name in self.airport_names:
                text_id=self.canvas.create_text(x, y+15, text="airport already exists", fill="black")
                self.delete_text(text_id)
            elif not self.is_valid_iata_code(airport_name):
                text_id=self.canvas.create_text(x, y+15, text="Invalid IATA code", fill="red")
                self.delete_text(text_id)
            else:
                self.airport_names.append(airport_name)
                for airport in self.airport_markers:
                    dist = sqrt((airport[0]-x)**2 + (airport[1]-y)**2)
                    if dist < 15:
                        self.canvas.create_text(x, y+15, text="Too close to existing airport", fill="red")
                        return
                if self.graph.check_vertex(airport_name):
                    print("Adding marker at:", x, y)
                    airport_marker = self.canvas.create_rectangle(x-5, y-5, x+5, y+5, fill="red")
                    self.canvas.tag_raise(airport_marker)
                    self.airport_markers.append((x, y, airport_name))
                    self.graph.add_vertex(airport_name)
                else:
                    text_id=self.canvas.create_text(x, y+15, text="Vertex already exists in the graph.", fill="red")
                    self.delete_text(text_id)
    def delete_airport(self):
        vertex_names = self.graph.get_vertices()
        dialog = tk.Toplevel()
        dialog.title("Delete Airport")
        dialog.geometry("250x150")
        source_label = tk.Label(dialog, text="Choose Airport:")
        source_label.grid()
        source_var = tk.StringVar()
        source_cb = ttk.Combobox(dialog, textvariable=source_var, values=vertex_names)
        source_cb.grid()

        def delete_airport_callback():
            source = source_var.get()
            self.graph.delete_vertex(source)
            dialog.destroy()

        delete_button = tk.Button(dialog, text="Delete", command=delete_airport_callback)
        delete_button.grid(row=2, column=0, pady=10)  # add button using the grid method




    def add_route(self):
        vertex_names = self.graph.get_vertices()
        if len(vertex_names) < 2:
            self.open_label_in_new_window("There must be at least two airports to add a route.")
            # self.route_label.config(text="There must be at least two airports to add a route.")
            return

        # Create the dialog window for selecting the source and destination airports
        dialog = tk.Toplevel()
        dialog.title("Add Route")
        dialog.geometry("250x150")

        source_var = tk.StringVar()
        dest_var = tk.StringVar()

        source_label = tk.Label(dialog, text="Source airport:")
        source_label.pack()

        source_cb = ttk.Combobox(dialog, textvariable=source_var, values=vertex_names)
        source_cb.pack()

        dest_label = tk.Label(dialog, text="Destination airport:")
        dest_label.pack()

        dest_cb = ttk.Combobox(dialog, textvariable=dest_var, values=vertex_names)
        dest_cb.pack()

        def add_route():
            source = source_var.get()
            dest = dest_var.get()

            if source == dest:
                self.open_label_in_new_window("Source and destination airports cannot be the same.")
                return
            if source==None or dest==None:
                self.open_label_in_new_window("There must be at least two airports to add a route.")


            # Check if a route between the two airports already exists
            if self.graph.edge_exists(source, dest):
                self.open_label_in_new_window("Route already exists.")
                return

            # Create a dialog window for entering the distance between the two airports
            distance_dialog = tk.Toplevel()
            distance_dialog.title("Distance")
            distance_dialog.geometry("250x150")

            distance_var = tk.StringVar()

            distance_label = tk.Label(distance_dialog, text="Distance between airports (km):")
            distance_label.pack()

            distance_entry = tk.Entry(distance_dialog, textvariable=distance_var)
            distance_entry.pack()

            def add_route_with_distance():
                distance_str = distance_var.get()
                try:
                    distance = float(distance_str)
                except ValueError:
                    self.open_label_in_new_window("Invalid distance")
                    return

                self.graph.add_edge(source, dest, distance)
                self.open_label_in_new_window(f"route between {source} and {dest} with distance {distance} km.")
                dialog.destroy()
                distance_dialog.destroy()

            add_distance_button = tk.Button(distance_dialog, text="Add", command=add_route_with_distance)
            add_distance_button.pack()

        add_route_button = tk.Button(dialog, text="Add", command=add_route)
        add_route_button.pack()

    def minimum_cost_ab(self):
        vertex_names = self.graph.get_vertices()
        if len(vertex_names) < 2:
            self.open_label_in_new_window("There must be at least two airports to verify a path.")
            return

        # Create the dialog window for selecting the source and destination airports
        dialog = tk.Toplevel()
        dialog.title("Shortest path")
        dialog.geometry("250x150")

        source_var = tk.StringVar()
        dest_var = tk.StringVar()

        source_label = tk.Label(dialog, text="Source airport:")
        source_label.pack()

        source_cb = ttk.Combobox(dialog, textvariable=source_var, values=vertex_names)
        source_cb.pack()

        dest_label = tk.Label(dialog, text="Destination airport:")
        dest_label.pack()

        dest_cb = ttk.Combobox(dialog, textvariable=dest_var, values=vertex_names)
        dest_cb.pack()

        def find_path():
            source = source_var.get()
            dest = dest_var.get()

            if source == dest:
                self.open_label_in_new_window("Source and destination airports cannot be the same.")
                return
            if source== None or dest==None:
                self.open_label_in_new_window("There must be at least two airports to verify a path.")


            path = self.graph.dijkstra_path(source, dest)

            if path == -1:
                print(-1)
                self.open_label_in_new_window("There is no path")
            else:
                self.open_label_in_new_window(f"Path between {source}, {dest} = {path}.")
            dialog.destroy()

        add_route_button = tk.Button(dialog, text="Add", command=find_path)
        add_route_button.pack()
        
    def run(self):
        self.graph.build_from_csv("Lab2_datos2\Routes.csv")
        self.root.mainloop()
class Intro:
    def __init__(self, master):
        self.root = master
        self.root.title("My Application")
        self.root.geometry("400x300")
        self.root.configure(bg='#F7F7F7') # set the background color

        font_style = tkFont.Font(family="Arial", size=16) # define a font style
        self.button = tk.Button(self.root, text="Continue", command=self.open_window_b, font=font_style)
        self.button.configure(bg='#0072C6', fg='#FFFFFF') # set the button background color and font color
        self.button.place(relx=0.5, rely=0.5, anchor=tk.CENTER) # center the button
        
        # Add label with welcome text
        welcome_text = "Welcome to the airport algorithm"
        welcome_label = tk.Label(self.root, text=welcome_text, font=font_style, bg='#F7F7F7')
        welcome_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER) # center the label

    def open_window_b(self):
        self.new_window = tk.Toplevel(self.root)
        self.window_b = WorldMap(self.new_window)
        self.window_b.run()



        
root = tk.Tk()
introw = Intro(root)
introw.root.mainloop()