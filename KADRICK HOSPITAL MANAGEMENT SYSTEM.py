#Creating a Hospital Management System
#Created by ID:20254329
# UCC: 2025


import random

def generate_id(prefix):  # to generate random and unique ID numbers
    return f"{prefix}{random.randint(1000, 9999)}"

def is_time_available(schedule, date, time):# if date and time is available
    return (date, time) not in schedule

class Person: # Super class
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def display_info(self): # displays bio data of persons
        print(f"Name: {self.name}, Age: {self.age}, Gender: {self.gender}")

class Patient(Person): #class for patient
    def __init__(self, name, age, gender):
        super().__init__(name, age, gender)
        self.patient_id = generate_id("PA")
        self.appointment_list = []

    def book_appointment(self, appointment):# to add an appointment
        self.appointment_list.append(appointment)
#to display patient profile appointment
    def view_profile(self):
        print("\nPatient BIO DATA")
        self.display_info()
        print(f"Patient ID: {self.patient_id}")
        print("Appointments:")
        if self.appointment_list:
            for appointment in self.appointment_list:
                print(f"Assigned to Dr. {appointment.doctor.name} on {appointment.date} at {appointment.time}")
        else:
            print("No appointments yet. Please set an appointment.")

class Doctor(Person): # Class for Doctor
    def __init__(self, name, age, gender, specialty):
        super().__init__(name, age, gender)
        self.doctor_id = generate_id("DOC")
        self.specialty = specialty
        self.schedule = []

    def is_available(self, date, time):
        return is_time_available(self.schedule, date, time)

    def view_schedule(self):
        print(f"Schedule for Dr. {self.name}:")
        if self.schedule:
            for date, time in self.schedule:
                print(f"{date} at {time}")
        else:
            print("No scheduled appointments.")



class Appointment:#class for appointment
    def __init__(self, patient, doctor, date, time):
        self.appointment_id = generate_id("AP")
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.status = " This Appointment is confirmed "

    def confirm(self):# to confirm an appointment
        print(f"\nAppointment Confirmed! Appointment ID: {self.appointment_id}")

    def cancel(self): #to cancel an appointment
        self.status = "This Appointment is Cancelled, Do You Wish to make another appointment "
        #print(f"\nAppointment {self.appointment_id} has been cancelled.")

class HospitalSystem: #dictionary for class information
    def __init__(self):
        self.patient = {}
        self.doctor = {}
        self.appointment ={}

    def add_patient(self, name, age, gender): #patient registry
        try:
            age = int(age)
            if age <= 0:
                raise ValueError("Age must be positive.")
        except ValueError:
            print("Please enter a valid age!")
            return

        patient = Patient(name, age, gender)
        self.patient[patient.patient_id] = patient
        print("\nRegistration Complete")
        print("***************************************************")
        print(f"Patient Registration ID is: {patient.patient_id}\n")

    def add_doctor(self, name, age, gender, specialty):           #doctor registry
        doctor = Doctor(name, age, gender, specialty)
        self.doctor[doctor.doctor_id] = doctor
        print(f"\nDoctor successfully Added. DOC ID Number is: {doctor.doctor_id}")

    def book_appointment(self, patient_id, doctor_id, date, time):    # booking an appointment
        patient = self.patient.get(patient_id)
        doctor = self.doctor.get(doctor_id)

        if not patient or not doctor:
            print("Invalid ID Information")
            return

        if not doctor.is_available(date, time):
            print("Doctor is unavailable for this time. Please schedule another time.")
            return

        appointment = Appointment(patient, doctor, date, time)
        self.appointment[appointment.appointment_id] = appointment
        patient.book_appointment(appointment)
        doctor.schedule.append((date, time))
        appointment.confirm()


        pass

#cancelling an appointment
    def cancel_appointment(self, appointment_id):
        appointment = self.appointment.get(appointment_id)
        if appointment:
            appointment.cancel()
        else:
            print("Appointment not found. Please make another appointment.")


    def generate_bill(self, appointment_id, extra_services):
        appointment = self.appointment.get(appointment_id)
        if not appointment:
            print("Appointment not found.")
            return

        base_fee = 3000  # Consultation Fee #set baser fee for bill
        total_extra = sum(extra_services) #adding ant additional charges
        total = base_fee + total_extra #total bill
#formating the bill view
        print("\n ********** RECEIPT ***********")
        print("Hospital: KADRICK HOSPITAL")
        print("Tel: 876-972-2258  Email: kadrick.hospital@moh.gov.jm")
        print(f"Appointment ID: {appointment_id}")
        print(f"Patient Name: {appointment.patient.name}")
        print(f"Doctor: Dr. {appointment.doctor.name}")
        print(f"Consultation Fee: JMD$ {base_fee:.2f}")
        print(f"Other Services Fee: JMD$ {total_extra:.2f}")
        print(f"TOTAL: JMD$ {total:.2f}")
        print("*********************************\n")
#Main menu to input data from user
def main():
    system = HospitalSystem()

    while True:
        print("\n^^^^^^^^ KADRICK HOSPITAL MANAGEMENT SYSTEM MENU ^^^^^^^^^^")
        print("1. New Patient Register")
        print("2. New Doctor Register")
        print("3. Book Appointment")
        print("4. Cancel Appointment")
        print("5. View All Appointments")
        print("6. Display Bill")
        print("7.Doctor's Schedule")
        print("8.View  Patient Profile")
        print("9. Exit")

        option = input("What would you like to do?  Select an Option (1-9): ")

        if option == '1':
            name = input("Patient name: ")
            age = input("Age: ")
            gender = input("Gender (M/F): ")
            system.add_patient(name, age, gender)

        elif option == '2':
            name = input("Doctor name: ")
            age = input("Age: ")
            gender = input("Gender (M/F): ")
            specialty = input("Specialty: ")
            print("Enter available time slots (format YYYY-MM-DD HH:MM). Type 'done' to stop.")
            schedule = []
            while True:
                entry = input("> ")
                if entry.lower() == 'done':
                    break
                parts = entry.split()
                if len(parts) == 2:
                    schedule.append((parts[0], parts[1]))
                else:
                    print("Invalid format. Please try again.")
            system.add_doctor(name, age, gender, specialty)
            # add schedule manually to the last added doctor
            for doctor in system.doctor.values():
                if doctor.name == name:
                    doctor.schedule = schedule

        elif option == '3':
            patient_id = input("Enter patient ID: ")
            doctor_id = input("Enter doctor ID: ")
            date = input("Enter appointment date (YYYY-MM-DD): ")
            time = input("Enter appointment time (HH:MM): ")
            system.book_appointment(patient_id, doctor_id, date, time)

        elif option == '4':
            appt_id = input("Enter appointment ID to cancel: ")
            (system.cancel_appointment(appt_id))

        elif option == '5': #view all appointments
            for appt in system.appointment.values():
                print(f"ID: {appt.appointment_id} | Patient: {appt.patient.name} | Doctor: {appt.doctor.name} | Date: {appt.date} {appt.time} | Status: {appt.status}")



        elif option == '6': #display total bill
            appt_id = input("Enter appointment ID: ")
            extra_services = []
            print("Enter additional service fees (type 'done' to finish):")
            while True:
                fee = input("Fee amount: ")
                if fee.lower() == 'done':
                    break
                try:
                    extra_services.append(float(fee))
                except ValueError:
                    print("Invalid input. Please enter a number.")
            system.generate_bill(appt_id, extra_services)


        elif option == "7": #view doctors schedule
            for doctor in system.doctor.values():
             doctor.view_schedule()

        elif option == "8":#view patient profile
            patient_id = input("Enter patient ID to view profile: ")
            patient = system.patient.get(patient_id)
            if patient:
                patient.view_profile()
            else:
                print("Patient not found.")



        elif option == '9': #terminate interaction
            print("Exiting the program. Thank you have a productive day!")
            break

        else:
            print("Invalid option. Please enter a number from 1 to 7.")

#start the program
if __name__ == "__main__":
    main()


