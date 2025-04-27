import tkinter as tk
from tkinter import PhotoImage, ttk
from PIL import Image, ImageTk
import tkinter.messagebox as messagebox

class HospitalAppointmentSystem:
    def __init__(self):
        self.scheduled_patients = set()  # Set of patients who have appointments
        self.appointment = {}  # Dictionary mapping patients to appointment times

    def book_appointment(self, patient, time):
        """Book an appointment for a patient at the specified time."""
        if patient in self.scheduled_patients:
            return f"Error: Patient {patient} already has an appointment."
        
        if time in self.appointment.values():
            return f"Error: Time slot {time} is already taken."
        
        # Book the appointment
        self.appointment[patient] = time
        self.scheduled_patients.add(patient)
        return f"Appointment successfully booked for {patient} at {time}."

    def cancel_appointment(self, patient):
        """Cancel the appointment for a patient."""
        if patient not in self.scheduled_patients:
            return f"Error: Patient {patient} does not have an appointment."
        
        # Remove the patient's appointment
        del self.appointment[patient]
        self.scheduled_patients.remove(patient)
        return f"Appointment for {patient} has been canceled."

    def view_appointments(self):
        """View all scheduled appointments."""
        if not self.appointment:
            return "No appointments scheduled."
        
        appointments = "\n".join([f"{patient} - {time}" for patient, time in self.appointment.items()])
        return f"Scheduled Appointments:\n{appointments}"

    def find_appointment(self, patient):
        """Find the appointment for a specific patient."""
        if patient in self.appointment:
            return f"Appointment for {patient}: {self.appointment[patient]}"
        return f"Error: No appointment found for patient {patient}."

    def update_appointment(self, patient, new_time):
        """Update the appointment time for a specific patient."""
        if patient not in self.appointment:
            return f"Error: Patient {patient} does not have an appointment."
        
        # Update the appointment time
        old_time = self.appointment[patient]
        self.appointment[patient] = new_time
        return f"Appointment for {patient} updated from {old_time} to {new_time}."


class AppointmentGUI:
    def __init__(self, root, system):
        self.root = root
        self.root.title("Hospital Appointment System")
        self.system = system

        # Configure the background color for the window
        self.root.configure(bg="#d0e9f7")

        # Header frame (Bluish)
        self.header_frame = tk.Frame(self.root, bg="#4fa3f7", pady=10)
        self.header_frame.pack(fill="x")

        # Load and resize the logo image
        original_logo = Image.open("logo.png")  # Make sure logo.png is in the same directory
        resized_logo = original_logo.resize((100, 100), Image.Resampling.LANCZOS)  # Resize the image using LANCZOS
        self.logo = ImageTk.PhotoImage(resized_logo)

        # Display the resized logo
        self.logo_label = tk.Label(self.header_frame, image=self.logo, bg="#4fa3f7")
        self.logo_label.pack(side="left", padx=10)  # Logo on the left side

        # Title in header
        self.title_label = tk.Label(self.header_frame, text="Hospital Appointment System", font=("Arial", 24, "bold"), bg="#4fa3f7", fg="white")
        self.title_label.pack(side="left", padx=20)  # Title on the right side of the logo

        # Input Frame for patient name and time
        self.input_frame = tk.Frame(self.root, bg="#d0e9f7", pady=20)
        self.input_frame.pack(padx=20, pady=10)

        # Patient Name Label with emoji
        self.patient_label = tk.Label(self.input_frame, text="📝Enter Patient Name: ", font=("Arial", 14), bg="#d0e9f7")
        self.patient_label.grid(row=0, column=0, padx=10)

        self.patient_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=30)
        self.patient_entry.grid(row=0, column=1)

        # Appointment Time Label with emoji
        self.time_label = tk.Label(self.input_frame, text="⏰Enter Appointment Time:", font=("Arial", 14), bg="#d0e9f7")
        self.time_label.grid(row=1, column=0, padx=10, pady=10)

        self.time_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=30)
        self.time_entry.grid(row=1, column=1)

        # Buttons with emojis
        self.button_frame = tk.Frame(self.root, bg="#d0e9f7")
        self.button_frame.pack(pady=20)

        self.book_button = tk.Button(self.button_frame, text="📅 Book Appointment", font=("Arial", 14), bg="#4fa3f7", fg="white", command=self.book_appointment, width=20)
        self.book_button.grid(row=0, column=0, padx=10, pady=10)

        self.cancel_button = tk.Button(self.button_frame, text="❌ Cancel Appointment", font=("Arial", 14), bg="#f44336", fg="white", command=self.cancel_appointment, width=20)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10)

        self.view_button = tk.Button(self.button_frame, text="📋 View Appointments", font=("Arial", 14), bg="#8bc34a", fg="white", command=self.view_appointments, width=20)
        self.view_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.update_button = tk.Button(self.button_frame, text="✏️ Update Appointment", font=("Arial", 14), bg="#ff9800", fg="white", command=self.update_appointment, width=20)
        self.update_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.find_button = tk.Button(self.button_frame, text="🔍 Find Appointment", font=("Arial", 14), bg="#2196f3", fg="white", command=self.find_appointment, width=20)
        self.find_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Result Label to show system output
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#d0e9f7", justify="left", anchor="w")
        self.result_label.pack(padx=20, pady=10, fill="x")

        # Table to display appointments
        self.tree = ttk.Treeview(self.root, columns=("Patient", "Time"), show="headings", height=10)
        self.tree.pack(padx=20, pady=10, fill="both")

        self.tree.heading("Patient", text="Patient Name")
        self.tree.heading("Time", text="Appointment Time")

    def book_appointment(self):
        patient = self.patient_entry.get()
        time = self.time_entry.get()
        if not patient or not time:
            messagebox.showerror("Input Error", "Please fill both fields.")
            return

        result = self.system.book_appointment(patient, time)
        self.result_label.config(text=result)
        self.patient_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.update_table()

    def cancel_appointment(self):
        patient = self.patient_entry.get()
        if not patient:
            messagebox.showerror("Input Error", "Please enter the patient's name.")
            return

        result = self.system.cancel_appointment(patient)
        self.result_label.config(text=result)
        self.patient_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.update_table()

    def view_appointments(self):
        appointments = self.system.view_appointments()
        self.result_label.config(text=appointments)
        self.update_table()

    def find_appointment(self):
        patient = self.patient_entry.get()
        if not patient:
            messagebox.showerror("Input Error", "Please enter the patient's name.")
            return

        result = self.system.find_appointment(patient)
        self.result_label.config(text=result)

    def update_appointment(self):
        patient = self.patient_entry.get()
        new_time = self.time_entry.get()
        if not patient or not new_time:
            messagebox.showerror("Input Error", "Please fill both fields.")
            return

        result = self.system.update_appointment(patient, new_time)
        self.result_label.config(text=result)
        self.patient_entry.delete(0, tk.END)
        self.time_entry.delete(0, tk.END)
        self.update_table()

    def update_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for patient, time in self.system.appointment.items():
            self.tree.insert("", "end", values=(patient, time))

# Main code to run the GUI
if __name__ == "__main__":
    system = HospitalAppointmentSystem()
    root = tk.Tk()
    gui = AppointmentGUI(root, system)
    root.mainloop()


