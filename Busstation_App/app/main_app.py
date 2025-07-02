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
            password=os.getenv("DB_PASSWORD", "your_strong_password"), 
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
            tree.column(col, anchor="center", width=widths[i])
        else:
            tree.column(col, anchor="center")
    
    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.config(yscrollcommand=scrollbar.set)
    return tree

# --- Helper function to fetch IDs for Comboboxes ---
def fetch_ids(table_name, id_column):
    conn = create_db_connection()
    ids = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(f"SELECT {id_column} FROM {table_name}")
            ids = [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as e:
            print(f"Error fetching {id_column}s from {table_name}: {e}")
        finally:
            cursor.close()
            conn.close()
    return ids

# --- Driver Management Tab Content ---
def create_driver_management_tab(notebook_parent):
    driver_frame = ttk.Frame(notebook_parent)

    # Input fields
    input_frame = ttk.LabelFrame(driver_frame, text="Driver Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    driver_id_entry = ttk.Entry(input_frame)
    full_name_entry = ttk.Entry(input_frame)
    gender_var = tk.StringVar()
    gender_combobox = ttk.Combobox(input_frame, textvariable=gender_var, values=["Nam", "Nữ", "Khác"])
    birth_date_entry = ttk.Entry(input_frame)
    phone_entry = ttk.Entry(input_frame)

    ttk.Label(input_frame, text="Driver ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    driver_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Full Name:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    full_name_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Gender:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    gender_combobox.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Birth Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    birth_date_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Phone Number:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
    phone_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

    input_frame.grid_columnconfigure(1, weight=1)

    # Treeview for displaying data
    columns = ("DriverID", "FullName", "Gender", "BirthDate", "PhoneNumber")
    column_widths = [80, 150, 70, 120, 120]
    tree = setup_treeview(driver_frame, columns, column_widths)
    
    def view_drivers():
        for item in tree.get_children():
            tree.delete(item)
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DriverID, FullName, Gender, BirthDate, PhoneNumber FROM driver")
            for row in cursor:
                tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def add_driver():
        driver_id = driver_id_entry.get()
        full_name = full_name_entry.get()
        gender = gender_var.get()
        birth_date = birth_date_entry.get()
        phone = phone_entry.get()

        if not all([driver_id, full_name, gender, birth_date, phone]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Input Error", "Birth Date must be in YYYY-MM-DD format.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "INSERT INTO driver (DriverID, FullName, Gender, BirthDate, PhoneNumber) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (driver_id, full_name, gender, birth_date, phone))
                conn.commit()
                messagebox.showinfo("Success", "Driver added successfully!")
                view_drivers()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add driver: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_driver():
        driver_id = driver_id_entry.get()
        full_name = full_name_entry.get()
        gender = gender_var.get()
        birth_date = birth_date_entry.get()
        phone = phone_entry.get()

        if not all([driver_id, full_name, gender, birth_date, phone]):
            messagebox.showwarning("Input Error", "All fields are required for update.")
            return
        
        try:
            datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            messagebox.showwarning("Input Error", "Birth Date must be in YYYY-MM-DD format.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "UPDATE driver SET FullName = %s, Gender = %s, BirthDate = %s, PhoneNumber = %s WHERE DriverID = %s"
                cursor.execute(sql, (full_name, gender, birth_date, phone, driver_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Driver updated successfully!")
                else:
                    messagebox.showwarning("No Change", "No driver found with that ID or no changes made.")
                view_drivers()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update driver: {e}")
            finally:
                cursor.close()
                conn.close()

    def delete_driver():
        driver_id = driver_id_entry.get()
        if not driver_id:
            messagebox.showwarning("Selection Error", "Please enter Driver ID or select a driver to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete driver {driver_id}?"):
            return
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "DELETE FROM driver WHERE DriverID = %s"
                cursor.execute(sql, (driver_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Driver deleted successfully!")
                    driver_id_entry.delete(0, tk.END)
                    full_name_entry.delete(0, tk.END)
                    gender_var.set("")
                    birth_date_entry.delete(0, tk.END)
                    phone_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Not Found", "No driver found with that ID.")
                view_drivers()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete driver: {e}")
            finally:
                cursor.close()
                conn.close()

    def on_tree_select_driver(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            driver_id_entry.delete(0, tk.END)
            driver_id_entry.insert(0, values[0])
            full_name_entry.delete(0, tk.END)
            full_name_entry.insert(0, values[1])
            gender_var.set(values[2])
            birth_date_entry.delete(0, tk.END)
            birth_date_entry.insert(0, values[3])
            phone_entry.delete(0, tk.END)
            phone_entry.insert(0, values[4])

    tree.bind("<<TreeviewSelect>>", on_tree_select_driver)

    # Buttons
    button_frame = ttk.Frame(driver_frame)
    button_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(button_frame, text="Add Driver", command=add_driver).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Driver", command=update_driver).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Driver", command=delete_driver).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_drivers).grid(row=0, column=3, padx=5, pady=5)

    view_drivers() # Initial load of data
    return driver_frame

# --- Bus Management Tab Content ---
def create_bus_management_tab(notebook_parent):
    bus_frame = ttk.Frame(notebook_parent)

    # Input fields
    input_frame = ttk.LabelFrame(bus_frame, text="Bus Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    bus_id_entry = ttk.Entry(input_frame)
    plate_number_entry = ttk.Entry(input_frame)
    capacity_entry = ttk.Entry(input_frame)
    bus_type_entry = ttk.Entry(input_frame)

    ttk.Label(input_frame, text="Bus ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    bus_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Plate Number:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    plate_number_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Capacity:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    capacity_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Bus Type:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    bus_type_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

    input_frame.grid_columnconfigure(1, weight=1)

    # Treeview for displaying data
    columns = ("BusID", "PlateNumber", "Capacity", "BusType")
    tree = setup_treeview(bus_frame, columns) # Using common setup_treeview

    def view_buses():
        for item in tree.get_children():
            tree.delete(item)
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM bus")
            for row in cursor:
                tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def add_bus():
        bus_id = bus_id_entry.get()
        plate_number = plate_number_entry.get()
        capacity = capacity_entry.get()
        bus_type = bus_type_entry.get()

        if not all([bus_id, plate_number, capacity, bus_type]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        try:
            capacity = int(capacity)
            if capacity <= 0:
                messagebox.showwarning("Input Error", "Capacity must be a positive integer.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Capacity must be an integer.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "INSERT INTO bus (BusID, PlateNumber, Capacity, BusType) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (bus_id, plate_number, capacity, bus_type))
                conn.commit()
                messagebox.showinfo("Success", "Bus added successfully!")
                view_buses()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add bus: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_bus():
        bus_id = bus_id_entry.get()
        plate_number = plate_number_entry.get()
        capacity = capacity_entry.get()
        bus_type = bus_type_entry.get()

        if not all([bus_id, plate_number, capacity, bus_type]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        try:
            capacity = int(capacity)
            if capacity <= 0:
                messagebox.showwarning("Input Error", "Capacity must be a positive integer.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Capacity must be an integer.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "UPDATE bus SET PlateNumber = %s, Capacity = %s, BusType = %s WHERE BusID = %s"
                cursor.execute(sql, (plate_number, capacity, bus_type, bus_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Bus updated successfully!")
                else:
                    messagebox.showwarning("No Change", "No bus found with that ID or no changes made.")
                view_buses()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update bus: {e}")
            finally:
                cursor.close()
                conn.close()

    def delete_bus():
        bus_id = bus_id_entry.get()
        if not bus_id:
            messagebox.showwarning("Selection Error", "Please enter Bus ID or select a bus to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete bus {bus_id}?"):
            return
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "DELETE FROM bus WHERE BusID = %s"
                cursor.execute(sql, (bus_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Bus deleted successfully!")
                    bus_id_entry.delete(0, tk.END)
                    plate_number_entry.delete(0, tk.END)
                    capacity_entry.delete(0, tk.END)
                    bus_type_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Not Found", "No bus found with that ID.")
                view_buses()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete bus: {e}")
            finally:
                cursor.close()
                conn.close()

    def on_tree_select_bus(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            bus_id_entry.delete(0, tk.END)
            bus_id_entry.insert(0, values[0])
            plate_number_entry.delete(0, tk.END)
            plate_number_entry.insert(0, values[1])
            capacity_entry.delete(0, tk.END)
            capacity_entry.insert(0, values[2])
            bus_type_entry.delete(0, tk.END)
            bus_type_entry.insert(0, values[3])

    tree.bind("<<TreeviewSelect>>", on_tree_select_bus)

    # Buttons
    button_frame = ttk.Frame(bus_frame)
    button_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(button_frame, text="Add Bus", command=add_bus).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Bus", command=update_bus).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Bus", command=delete_bus).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_buses).grid(row=0, column=3, padx=5, pady=5)

    view_buses() # Initial load of data
    return bus_frame

# --- Bus Stop Management Tab Content ---
def create_bus_stop_management_tab(notebook_parent):
    bus_stop_frame = ttk.Frame(notebook_parent)

    # Input fields
    input_frame = ttk.LabelFrame(bus_stop_frame, text="Bus Stop Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    stop_id_entry = ttk.Entry(input_frame)
    stop_name_entry = ttk.Entry(input_frame)
    location_entry = ttk.Entry(input_frame)

    ttk.Label(input_frame, text="Stop ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    stop_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Stop Name:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    stop_name_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Location:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    location_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

    input_frame.grid_columnconfigure(1, weight=1)

    # Treeview for displaying data
    columns = ("StopID", "StopName", "Location")
    tree = setup_treeview(bus_stop_frame, columns)

    def view_bus_stops():
        for item in tree.get_children():
            tree.delete(item)
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM busstop")
            for row in cursor:
                tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def add_bus_stop():
        stop_id = stop_id_entry.get()
        stop_name = stop_name_entry.get()
        location = location_entry.get()

        if not all([stop_id, stop_name, location]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "INSERT INTO busstop (StopID, StopName, Location) VALUES (%s, %s, %s)"
                cursor.execute(sql, (stop_id, stop_name, location))
                conn.commit()
                messagebox.showinfo("Success", "Bus Stop added successfully!")
                view_bus_stops()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add bus stop: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_bus_stop():
        stop_id = stop_id_entry.get()
        stop_name = stop_name_entry.get()
        location = location_entry.get()

        if not all([stop_id, stop_name, location]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "UPDATE busstop SET StopName = %s, Location = %s WHERE StopID = %s"
                cursor.execute(sql, (stop_name, location, stop_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Bus Stop updated successfully!")
                else:
                    messagebox.showwarning("No Change", "No bus stop found with that ID or no changes made.")
                view_bus_stops()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update bus stop: {e}")
            finally:
                cursor.close()
                conn.close()

    def delete_bus_stop():
        stop_id = stop_id_entry.get()
        if not stop_id:
            messagebox.showwarning("Selection Error", "Please enter Stop ID or select a bus stop to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete bus stop {stop_id}?"):
            return
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "DELETE FROM busstop WHERE StopID = %s"
                cursor.execute(sql, (stop_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Bus Stop deleted successfully!")
                    stop_id_entry.delete(0, tk.END)
                    stop_name_entry.delete(0, tk.END)
                    location_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Not Found", "No bus stop found with that ID.")
                view_bus_stops()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete bus stop: {e}")
            finally:
                cursor.close()
                conn.close()

    def on_tree_select_bus_stop(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            stop_id_entry.delete(0, tk.END)
            stop_id_entry.insert(0, values[0])
            stop_name_entry.delete(0, tk.END)
            stop_name_entry.insert(0, values[1])
            location_entry.delete(0, tk.END)
            location_entry.insert(0, values[2])

    tree.bind("<<TreeviewSelect>>", on_tree_select_bus_stop)

    # Buttons
    button_frame = ttk.Frame(bus_stop_frame)
    button_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(button_frame, text="Add Stop", command=add_bus_stop).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Stop", command=update_bus_stop).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Stop", command=delete_bus_stop).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_bus_stops).grid(row=0, column=3, padx=5, pady=5)

    view_bus_stops()
    return bus_stop_frame

# --- Route Management Tab Content ---
def create_route_management_tab(notebook_parent):
    route_frame = ttk.Frame(notebook_parent)

    # Input fields
    input_frame = ttk.LabelFrame(route_frame, text="Route Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    route_id_entry = ttk.Entry(input_frame)
    route_name_entry = ttk.Entry(input_frame)
    start_location_entry = ttk.Entry(input_frame)
    end_location_entry = ttk.Entry(input_frame)
    distance_entry = ttk.Entry(input_frame)

    ttk.Label(input_frame, text="Route ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    route_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Route Name:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    route_name_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Start Location:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    start_location_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="End Location:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    end_location_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Distance (km):").grid(row=4, column=0, padx=5, pady=2, sticky="w")
    distance_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

    input_frame.grid_columnconfigure(1, weight=1)

    # Treeview for displaying data
    columns = ("RouteID", "RouteName", "StartLocation", "EndLocation", "Distance")
    tree = setup_treeview(route_frame, columns)

    def view_routes():
        for item in tree.get_children():
            tree.delete(item)
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM route")
            for row in cursor:
                tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def add_route():
        route_id = route_id_entry.get()
        route_name = route_name_entry.get()
        start_location = start_location_entry.get()
        end_location = end_location_entry.get()
        distance_str = distance_entry.get()

        if not all([route_id, route_name, start_location, end_location, distance_str]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        try:
            distance = float(distance_str)
            if distance <= 0:
                messagebox.showwarning("Input Error", "Distance must be a positive number.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Distance must be a number.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "INSERT INTO route (RouteID, RouteName, StartLocation, EndLocation, Distance) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (route_id, route_name, start_location, end_location, distance))
                conn.commit()
                messagebox.showinfo("Success", "Route added successfully!")
                view_routes()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add route: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_route():
        route_id = route_id_entry.get()
        route_name = route_name_entry.get()
        start_location = start_location_entry.get()
        end_location = end_location_entry.get()
        distance_str = distance_entry.get()

        if not all([route_id, route_name, start_location, end_location, distance_str]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        try:
            distance = float(distance_str)
            if distance <= 0:
                messagebox.showwarning("Input Error", "Distance must be a positive number.")
                return
        except ValueError:
            messagebox.showwarning("Input Error", "Distance must be a number.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "UPDATE route SET RouteName = %s, StartLocation = %s, EndLocation = %s, Distance = %s WHERE RouteID = %s"
                cursor.execute(sql, (route_name, start_location, end_location, distance, route_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Route updated successfully!")
                else:
                    messagebox.showwarning("No Change", "No route found with that ID or no changes made.")
                view_routes()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update route: {e}")
            finally:
                cursor.close()
                conn.close()

    def delete_route():
        route_id = route_id_entry.get()
        if not route_id:
            messagebox.showwarning("Selection Error", "Please enter Route ID or select a route to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete route {route_id}?"):
            return
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "DELETE FROM route WHERE RouteID = %s"
                cursor.execute(sql, (route_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Route deleted successfully!")
                    route_id_entry.delete(0, tk.END)
                    route_name_entry.delete(0, tk.END)
                    start_location_entry.delete(0, tk.END)
                    end_location_entry.delete(0, tk.END)
                    distance_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Not Found", "No route found with that ID.")
                view_routes()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete route: {e}")
            finally:
                cursor.close()
                conn.close()

    def on_tree_select_route(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            route_id_entry.delete(0, tk.END)
            route_id_entry.insert(0, values[0])
            route_name_entry.delete(0, tk.END)
            route_name_entry.insert(0, values[1])
            start_location_entry.delete(0, tk.END)
            start_location_entry.insert(0, values[2])
            end_location_entry.delete(0, tk.END)
            end_location_entry.insert(0, values[3])
            distance_entry.delete(0, tk.END)
            distance_entry.insert(0, values[4])

    tree.bind("<<TreeviewSelect>>", on_tree_select_route)

    # Buttons
    button_frame = ttk.Frame(route_frame)
    button_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(button_frame, text="Add Route", command=add_route).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Route", command=update_route).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Route", command=delete_route).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_routes).grid(row=0, column=3, padx=5, pady=5)

    view_routes()
    return route_frame

# --- Schedule Management Tab Content ---
def create_schedule_management_tab(notebook_parent):
    schedule_frame = ttk.Frame(notebook_parent)

    # Input fields
    input_frame = ttk.LabelFrame(schedule_frame, text="Schedule Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    schedule_id_entry = ttk.Entry(input_frame)
    
    route_id_var = tk.StringVar()
    route_ids = fetch_ids('route', 'RouteID')
    route_id_combobox = ttk.Combobox(input_frame, textvariable=route_id_var, values=route_ids, state="readonly")

    departure_time_entry = ttk.Entry(input_frame) # Format HH:MM:SS
    arrival_time_entry = ttk.Entry(input_frame)   # Format HH:MM:SS
    
    day_of_week_var = tk.StringVar()
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_of_week_combobox = ttk.Combobox(input_frame, textvariable=day_of_week_var, values=days_of_week, state="readonly")

    ttk.Label(input_frame, text="Schedule ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    schedule_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Route ID:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    route_id_combobox.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Departure Time (HH:MM:SS):").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    departure_time_entry.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Arrival Time (HH:MM:SS):").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    arrival_time_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Day of Week:").grid(row=4, column=0, padx=5, pady=2, sticky="w")
    day_of_week_combobox.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

    input_frame.grid_columnconfigure(1, weight=1)

    # Treeview for displaying data
    columns = ("ScheduleID", "RouteID", "DepartureTime", "ArrivalTime", "DayOfWeek")
    tree = setup_treeview(schedule_frame, columns)

    def view_schedules():
        for item in tree.get_children():
            tree.delete(item)
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM schedule")
            for row in cursor:
                tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def add_schedule():
        schedule_id = schedule_id_entry.get()
        route_id = route_id_var.get()
        departure_time = departure_time_entry.get()
        arrival_time = arrival_time_entry.get()
        day_of_week = day_of_week_var.get()

        if not all([schedule_id, route_id, departure_time, arrival_time, day_of_week]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        try:
            datetime.strptime(departure_time, '%H:%M:%S')
            datetime.strptime(arrival_time, '%H:%M:%S')
        except ValueError:
            messagebox.showwarning("Input Error", "Time must be in HH:MM:SS format.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "INSERT INTO schedule (ScheduleID, RouteID, DepartureTime, ArrivalTime, DayOfWeek) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (schedule_id, route_id, departure_time, arrival_time, day_of_week))
                conn.commit()
                messagebox.showinfo("Success", "Schedule added successfully!")
                view_schedules()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add schedule: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_schedule():
        schedule_id = schedule_id_entry.get()
        route_id = route_id_var.get()
        departure_time = departure_time_entry.get()
        arrival_time = arrival_time_entry.get()
        day_of_week = day_of_week_var.get()

        if not all([schedule_id, route_id, departure_time, arrival_time, day_of_week]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        try:
            datetime.strptime(departure_time, '%H:%M:%S')
            datetime.strptime(arrival_time, '%H:%M:%S')
        except ValueError:
            messagebox.showwarning("Input Error", "Time must be in HH:MM:SS format.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "UPDATE schedule SET RouteID = %s, DepartureTime = %s, ArrivalTime = %s, DayOfWeek = %s WHERE ScheduleID = %s"
                cursor.execute(sql, (route_id, departure_time, arrival_time, day_of_week, schedule_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Schedule updated successfully!")
                else:
                    messagebox.showwarning("No Change", "No schedule found with that ID or no changes made.")
                view_schedules()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update schedule: {e}")
            finally:
                cursor.close()
                conn.close()

    def delete_schedule():
        schedule_id = schedule_id_entry.get()
        if not schedule_id:
            messagebox.showwarning("Selection Error", "Please enter Schedule ID or select a schedule to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete schedule {schedule_id}?"):
            return
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "DELETE FROM schedule WHERE ScheduleID = %s"
                cursor.execute(sql, (schedule_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Schedule deleted successfully!")
                    schedule_id_entry.delete(0, tk.END)
                    route_id_var.set("")
                    departure_time_entry.delete(0, tk.END)
                    arrival_time_entry.delete(0, tk.END)
                    day_of_week_var.set("")
                else:
                    messagebox.showwarning("Not Found", "No schedule found with that ID.")
                view_schedules()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete schedule: {e}")
            finally:
                cursor.close()
                conn.close()

    def on_tree_select_schedule(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            schedule_id_entry.delete(0, tk.END)
            schedule_id_entry.insert(0, values[0])
            route_id_var.set(values[1])
            departure_time_entry.delete(0, tk.END)
            departure_time_entry.insert(0, values[2])
            arrival_time_entry.delete(0, tk.END)
            arrival_time_entry.insert(0, values[3])
            day_of_week_var.set(values[4])

    tree.bind("<<TreeviewSelect>>", on_tree_select_schedule)

    # Buttons
    button_frame = ttk.Frame(schedule_frame)
    button_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(button_frame, text="Add Schedule", command=add_schedule).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Schedule", command=update_schedule).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Schedule", command=delete_schedule).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_schedules).grid(row=0, column=3, padx=5, pady=5)

    view_schedules()
    return schedule_frame

# --- Assignment Management Tab Content (Full CRUD) ---
def create_assignment_management_tab(notebook_parent):
    assignment_frame = ttk.Frame(notebook_parent)

    # Input fields
    input_frame = ttk.LabelFrame(assignment_frame, text="Assignment Information")
    input_frame.pack(padx=10, pady=10, fill="x")

    assignment_id_entry = ttk.Entry(input_frame)
    
    bus_id_var = tk.StringVar()
    bus_ids = fetch_ids('bus', 'BusID')
    bus_id_combobox = ttk.Combobox(input_frame, textvariable=bus_id_var, values=bus_ids, state="readonly")

    driver_id_var = tk.StringVar()
    driver_ids = fetch_ids('driver', 'DriverID')
    driver_id_combobox = ttk.Combobox(input_frame, textvariable=driver_id_var, values=driver_ids, state="readonly")

    route_id_var = tk.StringVar()
    route_ids = fetch_ids('route', 'RouteID')
    route_id_combobox = ttk.Combobox(input_frame, textvariable=route_id_var, values=route_ids, state="readonly")

    assignment_date_entry = ttk.Entry(input_frame) # Format YYYY-MM-DD
    departure_time_entry = ttk.Entry(input_frame)  # Format HH:MM:SS
    arrival_time_entry = ttk.Entry(input_frame)    # Format HH:MM:SS

    ttk.Label(input_frame, text="Assignment ID:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
    assignment_id_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Bus ID:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
    bus_id_combobox.grid(row=1, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Driver ID:").grid(row=2, column=0, padx=5, pady=2, sticky="w")
    driver_id_combobox.grid(row=2, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Route ID:").grid(row=3, column=0, padx=5, pady=2, sticky="w")
    route_id_combobox.grid(row=3, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Assignment Date (YYYY-MM-DD):").grid(row=4, column=0, padx=5, pady=2, sticky="w")
    assignment_date_entry.grid(row=4, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Departure Time (HH:MM:SS):").grid(row=5, column=0, padx=5, pady=2, sticky="w")
    departure_time_entry.grid(row=5, column=1, padx=5, pady=2, sticky="ew")
    ttk.Label(input_frame, text="Arrival Time (HH:MM:SS):").grid(row=6, column=0, padx=5, pady=2, sticky="w")
    arrival_time_entry.grid(row=6, column=1, padx=5, pady=2, sticky="ew")

    input_frame.grid_columnconfigure(1, weight=1)

    # Treeview for displaying data
    columns = ("AssignmentID", "BusID", "DriverID", "RouteID", "AssignmentDate", "DepartureTime", "ArrivalTime")
    tree = setup_treeview(assignment_frame, columns)

    def view_assignments():
        for item in tree.get_children():
            tree.delete(item)
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM assignment ORDER BY AssignmentDate DESC") # Show recent assignments first
            for row in cursor:
                tree.insert("", "end", values=row)
            cursor.close()
            conn.close()

    def add_assignment():
        assignment_id = assignment_id_entry.get()
        bus_id = bus_id_var.get()
        driver_id = driver_id_var.get()
        route_id = route_id_var.get()
        assignment_date = assignment_date_entry.get()
        departure_time = departure_time_entry.get()
        arrival_time = arrival_time_entry.get()

        if not all([assignment_id, bus_id, driver_id, route_id, assignment_date, departure_time, arrival_time]):
            messagebox.showwarning("Input Error", "All fields are required.")
            return
        
        try:
            datetime.strptime(assignment_date, '%Y-%m-%d')
            datetime.strptime(departure_time, '%H:%M:%S')
            datetime.strptime(arrival_time, '%H:%M:%S')
        except ValueError:
            messagebox.showwarning("Input Error", "Date must be YYYY-MM-DD, Time must be HH:MM:SS.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "INSERT INTO assignment (AssignmentID, BusID, DriverID, RouteID, AssignmentDate, DepartureTime, ArrivalTime) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (assignment_id, bus_id, driver_id, route_id, assignment_date, departure_time, arrival_time))
                conn.commit()
                messagebox.showinfo("Success", "Assignment added successfully!")
                view_assignments()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to add assignment: {e}")
            finally:
                cursor.close()
                conn.close()

    def update_assignment():
        assignment_id = assignment_id_entry.get()
        bus_id = bus_id_var.get()
        driver_id = driver_id_var.get()
        route_id = route_id_var.get()
        assignment_date = assignment_date_entry.get()
        departure_time = departure_time_entry.get()
        arrival_time = arrival_time_entry.get()

        if not all([assignment_id, bus_id, driver_id, route_id, assignment_date, departure_time, arrival_time]):
            messagebox.showwarning("Input Error", "All fields are required for update.")
            return
        
        try:
            datetime.strptime(assignment_date, '%Y-%m-%d')
            datetime.strptime(departure_time, '%H:%M:%S')
            datetime.strptime(arrival_time, '%H:%M:%S')
        except ValueError:
            messagebox.showwarning("Input Error", "Date must be YYYY-MM-DD, Time must be HH:MM:SS.")
            return

        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "UPDATE assignment SET BusID = %s, DriverID = %s, RouteID = %s, AssignmentDate = %s, DepartureTime = %s, ArrivalTime = %s WHERE AssignmentID = %s"
                cursor.execute(sql, (bus_id, driver_id, route_id, assignment_date, departure_time, arrival_time, assignment_id))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Assignment updated successfully!")
                else:
                    messagebox.showwarning("No Change", "No assignment found with that ID or no changes made.")
                view_assignments()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to update assignment: {e}")
            finally:
                cursor.close()
                conn.close()

    def delete_assignment():
        assignment_id = assignment_id_entry.get()
        if not assignment_id:
            messagebox.showwarning("Selection Error", "Please enter Assignment ID or select an assignment to delete.")
            return
        if not messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete assignment {assignment_id}?"):
            return
        conn = create_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                sql = "DELETE FROM assignment WHERE AssignmentID = %s"
                cursor.execute(sql, (assignment_id,))
                conn.commit()
                if cursor.rowcount > 0:
                    messagebox.showinfo("Success", "Assignment deleted successfully!")
                    assignment_id_entry.delete(0, tk.END)
                    bus_id_var.set("")
                    driver_id_var.set("")
                    route_id_var.set("")
                    assignment_date_entry.delete(0, tk.END)
                    departure_time_entry.delete(0, tk.END)
                    arrival_time_entry.delete(0, tk.END)
                else:
                    messagebox.showwarning("Not Found", "No assignment found with that ID.")
                view_assignments()
            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Failed to delete assignment: {e}")
            finally:
                cursor.close()
                conn.close()

    def on_tree_select_assignment(event):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item, "values")
            assignment_id_entry.delete(0, tk.END)
            assignment_id_entry.insert(0, values[0])
            bus_id_var.set(values[1])
            driver_id_var.set(values[2])
            route_id_var.set(values[3])
            assignment_date_entry.delete(0, tk.END)
            assignment_date_entry.insert(0, values[4])
            departure_time_entry.delete(0, tk.END)
            departure_time_entry.insert(0, values[5])
            arrival_time_entry.delete(0, tk.END)
            arrival_time_entry.insert(0, values[6])

    tree.bind("<<TreeviewSelect>>", on_tree_select_assignment)

    # Buttons
    button_frame = ttk.Frame(assignment_frame)
    button_frame.pack(padx=10, pady=10, fill="x")

    ttk.Button(button_frame, text="Add Assignment", command=add_assignment).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(button_frame, text="Update Assignment", command=update_assignment).grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(button_frame, text="Delete Assignment", command=delete_assignment).grid(row=0, column=2, padx=5, pady=5)
    ttk.Button(button_frame, text="Refresh", command=view_assignments).grid(row=0, column=3, padx=5, pady=5)

    view_assignments()
    return assignment_frame


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

    schedule_tab = create_schedule_management_tab(notebook)
    notebook.add(schedule_tab, text="Manage Schedules")

    assignment_tab = create_assignment_management_tab(notebook)
    notebook.add(assignment_tab, text="Manage Assignments")


    root.mainloop()

if __name__ == "__main__":
    main_app()