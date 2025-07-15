import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import os 
from datetime import datetime

# --- Database Connection ---
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "db"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "123zzz"), 
            database=os.getenv("DB_NAME", "busstationmanagement")
        )
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to MySQL: {e}\n"
                                                           f"Host: {os.getenv('DB_HOST', 'db')}\n"
                                                           f"User: {os.getenv('DB_USER', 'root')}\n"
                                                           f"DB: {os.getenv('DB_NAME', 'busstationmanagement')}")
        return None

# --- Common function to setup Treeview ---
def setup_treeview(parent_frame, columns, widths=None):
    tree_frame = ttk.Frame(parent_frame)
    tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        if widths and i < len(widths):
            tree.column(col, width=widths[i], anchor="center")
        else:
            tree.column(col, anchor="center")

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)
    return tree

# --- Driver Management ---
def create_driver_management_tab(notebook):
    driver_frame = ttk.Frame(notebook)

    # Input fields
    input_frame = ttk.LabelFrame(driver_frame, text="Driver Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(input_frame, text="Full Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    fullname_entry = ttk.Entry(input_frame, width=30)
    fullname_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Gender:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    gender_entry = ttk.Entry(input_frame, width=30)
    gender_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Birth Date:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    birthdate_entry = ttk.Entry(input_frame, width=30)
    birthdate_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Treeview for displaying drivers
    driver_tree = setup_treeview(driver_frame, ["DriverID", "FullName", "Gender", "BirthDate"],
                                 widths=[70, 150, 120, 200])

    def clear_driver_entries():
        fullname_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)
        birthdate_entry.delete(0, tk.END)

    def add_driver():
        fullname = fullname_entry.get()
        gender = gender_entry.get()
        birthdate = birthdate_entry.get()

        if not all([fullname, gender]):
            messagebox.showerror("Error", "Full Name and Gender are required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO driver (FullName, Gender, BirthDate) VALUES (%s, %s, %s)"
                cursor.execute(sql, (fullname, gender, birthdate))
                conn.commit()
                messagebox.showinfo("Success", "Driver added successfully.")
                view_drivers()
                clear_driver_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def update_driver():
        selected_item = driver_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a driver to update.")
            return

        driver_id = driver_tree.item(selected_item)['values'][0]
        fullname = fullname_entry.get()
        gender = gender_entry.get()
        birthdate = birthdate_entry.get()

        if not all([fullname, gender]):
            messagebox.showerror("Error", "Full Name and Gender are required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE driver SET FullName = %s, Gender = %s, BirthDate = %s WHERE DriverID = %s"
                cursor.execute(sql, (fullname, gender, birthdate, driver_id))
                conn.commit()
                messagebox.showinfo("Success", "Driver updated successfully.")
                view_drivers()
                clear_driver_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def delete_driver():
        selected_item = driver_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a driver to delete.")
            return

        driver_id = driver_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Driver ID: {driver_id}?"):
            conn = create_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    sql = "DELETE FROM driver WHERE DriverID = %s"
                    cursor.execute(sql, (driver_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Driver deleted successfully.")
                    view_drivers()
                    clear_driver_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()

    def view_drivers():
        for row in driver_tree.get_children():
            driver_tree.delete(row)
        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM driver")
                for row in cursor.fetchall():
                    driver_tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def on_driver_select(event):
        selected_item = driver_tree.focus()
        if selected_item:
            values = driver_tree.item(selected_item)['values']
            clear_driver_entries()
            fullname_entry.insert(0, values[1])
            gender_entry.insert(0, values[2])
            birthdate_entry.insert(0, values[3])

    driver_tree.bind("<<TreeviewSelect>>", on_driver_select)

    # Buttons
    button_frame = ttk.Frame(driver_frame)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Add Driver", command=add_driver).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Driver", command=update_driver).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Driver", command=delete_driver).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_drivers).grid(row=0, column=3, padx=5, pady=5)

    view_drivers()
    return driver_frame

# --- Bus Management ---
def create_bus_management_tab(notebook):
    bus_frame = ttk.Frame(notebook)

    # Input fields
    input_frame = ttk.LabelFrame(bus_frame, text="Bus Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(input_frame, text="Plate Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    plate_number_entry = ttk.Entry(input_frame, width=30)
    plate_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Capacity:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    capacity_entry = ttk.Entry(input_frame, width=30)
    capacity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="BusType:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    bus_type_entry = ttk.Entry(input_frame, width=30)
    bus_type_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    # Treeview for displaying buses
    bus_tree = setup_treeview(bus_frame, ["BusID", "PlateNumber", "Capacity", "BusType"],
                              widths=[70, 120, 80, 150])

    def clear_bus_entries():
        plate_number_entry.delete(0, tk.END)
        capacity_entry.delete(0, tk.END)
        bus_type_entry.delete(0, tk.END)

    def add_bus():
        plate_number = plate_number_entry.get()
        capacity = capacity_entry.get()
        bus_type = bus_type_entry.get()

        if not all([plate_number, capacity]):
            messagebox.showerror("Error", "Plate Number and Capacity are required.")
            return
        try:
            capacity = int(capacity)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a number.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO bus (PlateNumber, Capacity, BusType) VALUES (%s, %s, %s)"
                cursor.execute(sql, (plate_number, capacity, bus_type))
                conn.commit()
                messagebox.showinfo("Success", "Bus added successfully.")
                view_buses()
                clear_bus_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def update_bus():
        selected_item = bus_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bus to update.")
            return

        bus_id = bus_tree.item(selected_item)['values'][0]
        plate_number = plate_number_entry.get()
        capacity = capacity_entry.get()
        bus_type = bus_type_entry.get()

        if not all([plate_number, capacity]):
            messagebox.showerror("Error", "Plate Number and Capacity are required.")
            return
        try:
            capacity = int(capacity)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a number.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE bus SET PlateNumber = %s, Capacity = %s, BusType = %s WHERE BusID = %s"
                cursor.execute(sql, (plate_number, capacity, bus_type, bus_id))
                conn.commit()
                messagebox.showinfo("Success", "Bus updated successfully.")
                view_buses()
                clear_bus_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def delete_bus():
        selected_item = bus_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bus to delete.")
            return

        bus_id = bus_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Bus ID: {bus_id}?"):
            conn = create_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    sql = "DELETE FROM bus WHERE BusID = %s"
                    cursor.execute(sql, (bus_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Bus deleted successfully.")
                    view_buses()
                    clear_bus_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()

    def view_buses():
        for row in bus_tree.get_children():
            bus_tree.delete(row)
        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM bus")
                for row in cursor.fetchall():
                    bus_tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def on_bus_select(event):
        selected_item = bus_tree.focus()
        if selected_item:
            values = bus_tree.item(selected_item)['values']
            clear_bus_entries()
            plate_number_entry.insert(0, values[1])
            capacity_entry.insert(0, values[2])
            bus_type_entry.insert(0, values[3])

    bus_tree.bind("<<TreeviewSelect>>", on_bus_select)

    # Buttons
    button_frame = ttk.Frame(bus_frame)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Add Bus", command=add_bus).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Bus", command=update_bus).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Bus", command=delete_bus).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_buses).grid(row=0, column=3, padx=5, pady=5)

    view_buses()
    return bus_frame

# --- Bus Stop Management ---
def create_bus_stop_management_tab(notebook):
    bus_stop_frame = ttk.Frame(notebook)

    # Input fields
    input_frame = ttk.LabelFrame(bus_stop_frame, text="Bus Stop Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(input_frame, text="Stop Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    stop_name_entry = ttk.Entry(input_frame, width=30)
    stop_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Location:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    location_entry = ttk.Entry(input_frame, width=30)
    location_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    # Treeview for displaying bus stops
    bus_stop_tree = setup_treeview(bus_stop_frame, ["StopID", "StopName", "Location"],
                                   widths=[70, 150, 200])

    def clear_bus_stop_entries():
        stop_name_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)

    def add_bus_stop():
        stop_name = stop_name_entry.get()
        location = location_entry.get()

        if not stop_name:
            messagebox.showerror("Error", "Stop Name is required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO busstop (StopName, Location) VALUES (%s, %s)"
                cursor.execute(sql, (stop_name, location))
                conn.commit()
                messagebox.showinfo("Success", "Bus Stop added successfully.")
                view_bus_stops()
                clear_bus_stop_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def update_bus_stop():
        selected_item = bus_stop_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bus stop to update.")
            return

        stop_id = bus_stop_tree.item(selected_item)['values'][0]
        stop_name = stop_name_entry.get()
        location = location_entry.get()

        if not stop_name:
            messagebox.showerror("Error", "Stop Name is required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE busstop SET StopName = %s, Location = %s WHERE StopID = %s"
                cursor.execute(sql, (stop_name, location, stop_id))
                conn.commit()
                messagebox.showinfo("Success", "Bus Stop updated successfully.")
                view_bus_stops()
                clear_bus_stop_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def delete_bus_stop():
        selected_item = bus_stop_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a bus stop to delete.")
            return

        stop_id = bus_stop_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Stop ID: {stop_id}?"):
            conn = create_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    sql = "DELETE FROM busstop WHERE StopID = %s"
                    cursor.execute(sql, (stop_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Bus Stop deleted successfully.")
                    view_bus_stops()
                    clear_bus_stop_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()

    def view_bus_stops():
        for row in bus_stop_tree.get_children():
            bus_stop_tree.delete(row)
        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM busstop")
                for row in cursor.fetchall():
                    bus_stop_tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def on_bus_stop_select(event):
        selected_item = bus_stop_tree.focus()
        if selected_item:
            values = bus_stop_tree.item(selected_item)['values']
            clear_bus_stop_entries()
            stop_name_entry.insert(0, values[1])
            location_entry.insert(0, values[2])

    bus_stop_tree.bind("<<TreeviewSelect>>", on_bus_stop_select)

    # Buttons
    button_frame = ttk.Frame(bus_stop_frame)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Add Bus Stop", command=add_bus_stop).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Bus Stop", command=update_bus_stop).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Bus Stop", command=delete_bus_stop).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_bus_stops).grid(row=0, column=3, padx=5, pady=5)

    view_bus_stops()
    return bus_stop_frame

# --- Route Management ---
def create_route_management_tab(notebook):
    route_frame = ttk.Frame(notebook)

    # Input fields
    input_frame = ttk.LabelFrame(route_frame, text="Route Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(input_frame, text="Route Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    route_name_entry = ttk.Entry(input_frame, width=30)
    route_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="StartPoint:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    start_point_entry = ttk.Entry(input_frame, width=30)
    start_point_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="EndPoint:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    end_point_entry = ttk.Entry(input_frame, width=30)
    end_point_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Distance (km):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    distance_entry = ttk.Entry(input_frame, width=30)
    distance_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # Treeview for displaying routes
    route_tree = setup_treeview(route_frame, ["RouteID", "RouteName", "StartPoint", "EndPoint", "Distance"],
                                widths=[70, 100, 150, 150, 100])

    def clear_route_entries():
        route_name_entry.delete(0, tk.END)
        start_point_entry.delete(0, tk.END)
        end_point_entry.delete(0, tk.END)
        distance_entry.delete(0, tk.END)

    def add_route():
        route_name = route_name_entry.get()
        start_point = start_point_entry.get()
        end_point = end_point_entry.get()
        distance = distance_entry.get()

        if not all([route_name, start_point, end_point, distance]):
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            distance = float(distance)
        except ValueError:
            messagebox.showerror("Error", "Distance must be a number.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO route (RouteName, StartPoint, EndPoint, Distance) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (route_name, start_point, end_point, distance))
                conn.commit()
                messagebox.showinfo("Success", "Route added successfully.")
                view_routes()
                clear_route_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def update_route():
        selected_item = route_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a route to update.")
            return

        route_id = route_tree.item(selected_item)['values'][0]
        route_name = route_name_entry.get()
        start_point = start_point_entry.get()
        end_point = end_point_entry.get()
        distance = distance_entry.get()

        if not all([route_name, start_point, end_point, distance]):
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            distance = float(distance)
        except ValueError:
            messagebox.showerror("Error", "Distance must be a number.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE route SET RouteName = %s, StartPoint = %s, EndPoint = %s, Distance = %s WHERE RouteID = %s"
                cursor.execute(sql, (route_name, start_point, end_point, distance, route_id))
                conn.commit()
                messagebox.showinfo("Success", "Route updated successfully.")
                view_routes()
                clear_route_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def delete_route():
        selected_item = route_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a route to delete.")
            return

        route_id = route_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Route ID: {route_id}?"):
            conn = create_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    sql = "DELETE FROM route WHERE RouteID = %s"
                    cursor.execute(sql, (route_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Route deleted successfully.")
                    view_routes()
                    clear_route_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()

    def view_routes():
        for row in route_tree.get_children():
            route_tree.delete(row)
        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM route")
                for row in cursor.fetchall():
                    route_tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def on_route_select(event):
        selected_item = route_tree.focus()
        if selected_item:
            values = route_tree.item(selected_item)['values']
            clear_route_entries()
            route_name_entry.insert(0, values[1])
            start_point_entry.insert(0, values[2])
            end_point_entry.insert(0, values[3])
            distance_entry.insert(0, values[4])

    route_tree.bind("<<TreeviewSelect>>", on_route_select)

    # Buttons
    button_frame = ttk.Frame(route_frame)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Add Route", command=add_route).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Route", command=update_route).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Route", command=delete_route).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_routes).grid(row=0, column=3, padx=5, pady=5)

    view_routes()
    return route_frame

# --- Assignment Management (Updated to exclude DepartureTime/ArrivalTime) ---
def create_assignment_management_tab(notebook):
    assignment_frame = ttk.Frame(notebook)

    # Input fields
    input_frame = ttk.LabelFrame(assignment_frame, text="Assignment Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(input_frame, text="Bus ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    bus_id_entry = ttk.Entry(input_frame, width=30)
    bus_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Driver ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    driver_id_entry = ttk.Entry(input_frame, width=30)
    driver_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Route ID:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    route_id_entry = ttk.Entry(input_frame, width=30)
    route_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Assignment Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    assignment_date_entry = ttk.Entry(input_frame, width=30)
    assignment_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # Treeview for displaying assignments
    assignment_tree = setup_treeview(assignment_frame, ["AssignmentID", "BusID", "DriverID", "RouteID", "AssignmentDate"],
                                     widths=[90, 70, 70, 70, 150])

    def clear_assignment_entries():
        bus_id_entry.delete(0, tk.END)
        driver_id_entry.delete(0, tk.END)
        route_id_entry.delete(0, tk.END)
        assignment_date_entry.delete(0, tk.END)

    def add_assignment():
        bus_id = bus_id_entry.get()
        driver_id = driver_id_entry.get()
        route_id = route_id_entry.get()
        assignment_date = assignment_date_entry.get()

        if not all([bus_id, driver_id, route_id, assignment_date]):
            messagebox.showerror("Error", "All assignment fields are required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO assignment (BusID, DriverID, RouteID, AssignmentDate) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (bus_id, driver_id, route_id, assignment_date))
                conn.commit()
                messagebox.showinfo("Success", "Assignment added successfully.")
                view_assignments()
                clear_assignment_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def update_assignment():
        selected_item = assignment_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an assignment to update.")
            return

        assignment_id = assignment_tree.item(selected_item)['values'][0]
        bus_id = bus_id_entry.get()
        driver_id = driver_id_entry.get()
        route_id = route_id_entry.get()
        assignment_date = assignment_date_entry.get()

        if not all([bus_id, driver_id, route_id, assignment_date]):
            messagebox.showerror("Error", "All assignment fields are required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE assignment SET BusID = %s, DriverID = %s, RouteID = %s, AssignmentDate = %s WHERE AssignmentID = %s"
                cursor.execute(sql, (bus_id, driver_id, route_id, assignment_date, assignment_id))
                conn.commit()
                messagebox.showinfo("Success", "Assignment updated successfully.")
                view_assignments()
                clear_assignment_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def delete_assignment():
        selected_item = assignment_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an assignment to delete.")
            return

        assignment_id = assignment_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Assignment ID: {assignment_id}?"):
            conn = create_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    sql = "DELETE FROM assignment WHERE AssignmentID = %s"
                    cursor.execute(sql, (assignment_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Assignment deleted successfully.")
                    view_assignments()
                    clear_assignment_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()

    def view_assignments():
        for row in assignment_tree.get_children():
            assignment_tree.delete(row)
        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Select only columns present in the assignment table as per init.sql
                cursor.execute("SELECT AssignmentID, BusID, DriverID, RouteID, AssignmentDate FROM assignment")
                for row in cursor.fetchall():
                    assignment_tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def on_assignment_select(event):
        selected_item = assignment_tree.focus()
        if selected_item:
            values = assignment_tree.item(selected_item)['values']
            clear_assignment_entries()
            bus_id_entry.insert(0, values[1])
            driver_id_entry.insert(0, values[2])
            route_id_entry.insert(0, values[3])
            assignment_date_entry.insert(0, values[4])

    assignment_tree.bind("<<TreeviewSelect>>", on_assignment_select)

    # Buttons
    button_frame = ttk.Frame(assignment_frame)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Add Assignment", command=add_assignment).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Assignment", command=update_assignment).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Assignment", command=delete_assignment).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_assignments).grid(row=0, column=3, padx=5, pady=5)

    view_assignments()
    return assignment_frame


# --- Schedule Management ---
def create_schedule_management_tab(notebook):
    schedule_frame = ttk.Frame(notebook)

    # Input fields
    input_frame = ttk.LabelFrame(schedule_frame, text="Schedule Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    ttk.Label(input_frame, text="Route ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    route_id_schedule_entry = ttk.Entry(input_frame, width=30)
    route_id_schedule_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Departure Time (HH:MM:SS):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    departure_time_entry = ttk.Entry(input_frame, width=30)
    departure_time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Arrival Time (HH:MM:SS):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    arrival_time_entry = ttk.Entry(input_frame, width=30)
    arrival_time_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

    ttk.Label(input_frame, text="Day of Week:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    day_of_week_entry = ttk.Entry(input_frame, width=30)
    day_of_week_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

    # Treeview for displaying schedules
    schedule_tree = setup_treeview(schedule_frame, ["ScheduleID", "RouteID", "DepartureTime", "ArrivalTime", "DayOfWeek"],
                                   widths=[90, 70, 120, 120, 100])

    def clear_schedule_entries():
        route_id_schedule_entry.delete(0, tk.END)
        departure_time_entry.delete(0, tk.END)
        arrival_time_entry.delete(0, tk.END)
        day_of_week_entry.delete(0, tk.END)

    def add_schedule():
        route_id = route_id_schedule_entry.get()
        departure_time = departure_time_entry.get()
        arrival_time = arrival_time_entry.get()
        day_of_week = day_of_week_entry.get()

        if not all([route_id, departure_time, arrival_time, day_of_week]):
            messagebox.showerror("Error", "All schedule fields are required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "INSERT INTO schedule (RouteID, DepartureTime, ArrivalTime, DayOfWeek) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (route_id, departure_time, arrival_time, day_of_week))
                conn.commit()
                messagebox.showinfo("Success", "Schedule added successfully.")
                view_schedules()
                clear_schedule_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def update_schedule():
        selected_item = schedule_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a schedule to update.")
            return

        schedule_id = schedule_tree.item(selected_item)['values'][0]
        route_id = route_id_schedule_entry.get()
        departure_time = departure_time_entry.get()
        arrival_time = arrival_time_entry.get()
        day_of_week = day_of_week_entry.get()

        if not all([route_id, departure_time, arrival_time, day_of_week]):
            messagebox.showerror("Error", "All schedule fields are required.")
            return

        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                sql = "UPDATE schedule SET RouteID = %s, DepartureTime = %s, ArrivalTime = %s, DayOfWeek = %s WHERE ScheduleID = %s"
                cursor.execute(sql, (route_id, departure_time, arrival_time, day_of_week, schedule_id))
                conn.commit()
                messagebox.showinfo("Success", "Schedule updated successfully.")
                view_schedules()
                clear_schedule_entries()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def delete_schedule():
        selected_item = schedule_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a schedule to delete.")
            return

        schedule_id = schedule_tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Schedule ID: {schedule_id}?"):
            conn = create_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    sql = "DELETE FROM schedule WHERE ScheduleID = %s"
                    cursor.execute(sql, (schedule_id,))
                    conn.commit()
                    messagebox.showinfo("Success", "Schedule deleted successfully.")
                    view_schedules()
                    clear_schedule_entries()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error: {err}")
                finally:
                    cursor.close()
                    conn.close()

    def view_schedules():
        for row in schedule_tree.get_children():
            schedule_tree.delete(row)
        conn = create_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM schedule")
                for row in cursor.fetchall():
                    schedule_tree.insert("", tk.END, values=row)
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

    def on_schedule_select(event):
        selected_item = schedule_tree.focus()
        if selected_item:
            values = schedule_tree.item(selected_item)['values']
            clear_schedule_entries()
            route_id_schedule_entry.insert(0, values[1])
            departure_time_entry.insert(0, values[2])
            arrival_time_entry.insert(0, values[3])
            day_of_week_entry.insert(0, values[4])

    schedule_tree.bind("<<TreeviewSelect>>", on_schedule_select)

    # Buttons
    button_frame = ttk.Frame(schedule_frame)
    button_frame.pack(pady=10)
    ttk.Button(button_frame, text="Add Schedule", command=add_schedule).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Schedule", command=update_schedule).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Schedule", command=delete_schedule).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_schedules).grid(row=0, column=3, padx=5, pady=5)

    view_schedules()
    return schedule_frame

# --- Main Application Window ---
def main_app():
    root = tk.Tk()
    root.title("Bus Station Management System")
    root.geometry("1050x650") # Increased size to accommodate more content and tabs

    # Create a Notebook widget (for tabs)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Create and add all management tabs
    driver_tab = create_driver_management_tab(notebook)
    notebook.add(driver_tab, text="Manage Drivers")

    bus_tab = create_bus_management_tab(notebook)
    notebook.add(bus_tab, text="Manage Buses")
    
    bus_stop_tab = create_bus_stop_management_tab(notebook)
    notebook.add(bus_stop_tab, text="Manage Bus Stops")

    route_tab = create_route_management_tab(notebook)
    notebook.add(route_tab, text="Manage Routes")

    # Add the modified assignment tab
    assignment_tab = create_assignment_management_tab(notebook)
    notebook.add(assignment_tab, text="Manage Assignments")

    # Add the schedule tab (existing, unchanged)
    schedule_tab = create_schedule_management_tab(notebook)
    notebook.add(schedule_tab, text="Manage Schedules")

    root.mainloop()

if __name__ == "__main__":
    main_app()