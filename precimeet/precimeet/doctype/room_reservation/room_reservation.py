# Copyright (c) 2025, preciholesports and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_url
from datetime import datetime, timedelta


class RoomReservation(Document):
    # def validate(self):
    #     # Step 1: Ensure 'date' is a datetime.date object
    #     if isinstance(self.date, str):
    #         try:
    #             booking_date = datetime.strptime(self.date, "%Y-%m-%d").date()
    #         except ValueError:
    #             frappe.throw("Invalid booking date format. Expected YYYY-MM-DD.")
    #     else:
    #         booking_date = self.date

    #         # Step 2: Ensure 'from_time' and 'to_time' are datetime.time objects
    #     def to_time_obj(t):
    #         if isinstance(t, str):
    #             try:
    #                 return datetime.strptime(t, "%H:%M:%S").time()
    #             except ValueError:
    #                 frappe.throw("Time format must be HH:MM:SS")
    #         return t
    #     from_time = to_time_obj(self.from_time)
    #     to_time = to_time_obj(self.to_time)

    #     # Step 3: Combine date and time into datetime objects for comparison
    #     start_datetime = datetime.combine(booking_date, from_time)
    #     end_datetime = datetime.combine(booking_date, to_time)

    #     # Step 4: Ensure 'from_time' is before 'to_time'
    #     if start_datetime >= end_datetime:
    #         frappe.throw("Start time must be before end time.")

    #     # Step 5: Check for overlapping reservations in the same room
    #     overlapping = frappe.db.sql("""
    #         SELECT name FROM `tabRoom Reservation`
    #         WHERE room = %s AND date = %s AND name != %s
    #         AND (
    #             (%s BETWEEN from_time AND to_time)
    #             OR (%s BETWEEN from_time AND to_time)
    #             OR (from_time BETWEEN %s AND %s)
    #             OR (to_time BETWEEN %s AND %s)
    #             )
    #         """, (
    #         self.room, booking_date, self.name or "New Room Reservation",
    #         from_time, to_time,
    #         from_time, to_time,
    #         from_time, to_time
    #         ))

    #     if overlapping:
    #         frappe.throw("This room is already booked during the selected time.")

    #     # Step 6: Optionally, log for debugging (you can remove this in production)
    #     frappe.logger().info(f"Room validated: {self.room} from {start_datetime} to {end_datetime}")
    # @frappe.whitelist()
    # def get_my_bookings():
    #     user = frappe.session.user
    #     frappe.logger().info(f"Fetching bookings for user: {user}")
    #     return frappe.get_all(
    #     'Room Reservation',
    #     filters={'user': user},
    #     fields=['subject', 'room', 'date', 'from_time', 'to_time', 'description'],
    #     order_by='date asc',
    # )
    def after_insert(self):
        if self.docstatus == 0:
            self.booked_by = frappe.session.user
            # frappe.print("Booking by: ", self.booked_by)
            self.submit()


    def before_submit(self):
        self.send_attendees_email()

    def send_attendees_email(self):
        try:
            attendee_emails = []

            # Only collect attendee emails if attendees are added
            for attendee in self.attendees_emails:
                if attendee.email_ids:               
                    email = frappe.db.get_value("User", attendee.email_ids, "email")
                    if email:
                        attendee_emails.append(email)

            # Collect invitee emails from invitees field
            invitee_emails = []
            if self.invitees_emails:
                invitee_emails = [email.strip() for email in self.invitees_emails.split(',') if email.strip()]

            all_recipients = attendee_emails + invitee_emails

            subject = f"Meeting Scheduled: {self.subject}"
            message = f"""
            <p>Hello,</p>
            <p>You have been invited to a meeting.</p>
            <p><strong>Subject:</strong> {self.subject}</p>
            <p><strong>Room:</strong> {self.room}</p>
            <p><strong>Date:</strong> {self.date}</p>
            <p><strong>From Time:</strong> {self.from_time} <strong>To:</strong> {self.to_time}</p>
            <p><strong>Booked By:</strong> {frappe.session.user}</p>
            <p><strong>Description:</strong> {self.description}</p>
            """

            if all_recipients:
                frappe.sendmail(
                    recipients=list(set(all_recipients)), 
                    subject=subject,
                    message=message
                )
                frappe.msgprint("Meeting invitation email sent successfully!")
            else:
                frappe.msgprint("No recipients found to send email.")

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), "Room Booking: Email Sending Error")
            frappe.msgprint(f"Failed to send email notification: {str(e)}")

