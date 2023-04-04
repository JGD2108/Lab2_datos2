import tkinter as tk
from math import sqrt
from tkinter import simpledialog
import re, csv
import csv
import pandas as pd
from collections import defaultdict
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
    
    def build_from_csv(self, file_path):
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                numero_de_fila = reader.line_num
                print(numero_de_fila)
                u, v, w = row['Origin_airport'], row['Destination_airport'], float(row['Distance'])
                if (self.edge_exists(u,v)):
                    continue
                self.add_edge(u, v, w)
    
    def print_graph(self):
        for u in self.graph:
            for v, w in self.graph[u]:
                print(f"({u} -> {v}, cost = {w:.2f})")

class WorldMap():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("World Map")
        self.canvas_width = 750
        self.canvas_height = 500
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.root.resizable(False,False)
        self.canvas.pack()
        self.world_map_img = tk.PhotoImage(file="Lab2_datos2\Image.png")
        self.world_map_img = self.world_map_img.subsample(2)
        self.canvas.create_image(self.canvas_width/2, self.canvas_height/2, image=self.world_map_img)
        self.airport_markers = []
        self.airport_names = []
        self.create_widgets()

    def create_widgets(self):
        self.add_route_button = tk.Button(self.root, text="Add Route", command=self.add_route)
        self.add_route_button.pack()
        self.route_label = tk.Label(self.root, text="")
        self.route_label.pack()
        self.canvas.bind("<Button-1>", self.add_airport_marker)
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

    def add_airport_marker(self, event):
        x, y = event.x, event.y
        airport_name = None
        while airport_name is None or airport_name not in self.airport_names:
            airport_name = simpledialog.askstring("Airport Name", "Enter name for airport:")
            if airport_name is None:
                return
            if airport_name in self.airport_names:
                text_id=self.canvas.create_text(x, y+15, text="airport already exists", fill="black")
                def delete_text():
                    self.canvas.after(3000, self.canvas.delete, text_id)
                delete_text()
            elif not self.is_valid_iata_code(airport_name):
                text_id=self.canvas.create_text(x, y+15, text="Invalid IATA code", fill="red")
                def delete_text():
                    self.canvas.after(3000, self.canvas.delete, text_id)
                delete_text()
            else:
                self.airport_names.append(airport_name)
                for airport in self.airport_markers:
                    dist = sqrt((airport[0]-x)**2 + (airport[1]-y)**2)
                    if dist < 15:
                        print("Too close to existing airport")
                        self.canvas.create_text(x, y+15, text="Too close to existing airport", fill="red")
                        return
                print("Adding marker at:", x, y)
                airport_marker = self.canvas.create_rectangle(x-5, y-5, x+5, y+5, fill="red")
                self.canvas.tag_raise(airport_marker)
                self.airport_markers.append((x, y, airport_name))
    def add_route(self):
        airports = []
        print(self.airport_markers)
        airport1 = None
        while airport1 is None:
            airport1_name = simpledialog.askstring("Airport Selection", "Enter name of origin airport:")
            for airport in self.airport_markers:
                if airport1_name == airport[2]:
                    airport1 = airport
                    airports.append(airport1)
                    break
            if airport1 is None:
                text_id = self.canvas.create_text(self.canvas_width/2, 20, text="Airport not found", fill="red")
                def delete_text():
                    self.canvas.after(3000, self.canvas.delete, text_id)
                delete_text()
        airport2 = None
        while airport2 is None:
            airport2_name = simpledialog.askstring("Airport Selection", "Enter name of destination airport:")
            for airport in self.airport_markers:
                if airport2_name == airport[2]:
                    airport2 = airport
                    airports.append(airport2)
                    break
            if airport2 is None:
                text_id = self.canvas.create_text(self.canvas_width/2, 20, text="Airport not found", fill="red")
                def delete_text():
                    self.canvas.after(3000, self.canvas.delete, text_id)
                delete_text()
            distance = tk.simpledialog.askfloat("Distance", "Enter distance between airports:")
            if distance is None:
                return
            
            # display route information in text label
            origin = airports[0][2]
            destiny = airports[1][2]
            route_info = f"Route from {origin} to {destiny}\nDistance: {distance:.2f}"
            self.route_label.configure(text=route_info)
if __name__=="__main__":
    # g = Graph()
    # g.build_from_csv("Lab2_datos2\FlightsDatabase.csv")
    world_map = WorldMap()
    world_map.root.mainloop()
    
