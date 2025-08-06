# Copyright (c) 2025, preciholesports and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_url
from datetime import datetime, time


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

    #     # Step 5: Check for overlapping reservations in the same room

    def validate(self):
        def parse_time(t):
            if isinstance(t, time):
                return t
            try:
                return datetime.strptime(t, "%H:%M:%S").time()
            except ValueError:
                try:
                    return datetime.strptime(t, "%H:%M").time()
                except ValueError:
                    frappe.throw(_("Invalid time format: {0}").format(t))

        # Parse and log date
        if isinstance(self.date, str):
            self.date = datetime.strptime(self.date, "%Y-%m-%d").date()

        # Parse and log times
        self.from_time = parse_time(self.from_time)
        self.to_time = parse_time(self.to_time)

        # Log parsed values
        frappe.logger().info(f"[VALIDATE] Room: {self.room}")
        frappe.logger().info(f"[VALIDATE] Date: {self.date}")
        frappe.logger().info(f"[VALIDATE] From Time: {self.from_time}")
        frappe.logger().info(f"[VALIDATE] To Time: {self.to_time}")

        if self.from_time >= self.to_time:
            frappe.throw(_("From Time must be before To Time."))

        from_datetime = datetime.combine(self.date, self.from_time)
        to_datetime = datetime.combine(self.date, self.to_time)

        # Log datetime ranges
        frappe.logger().info(f"[VALIDATE] From Datetime: {from_datetime}")
        frappe.logger().info(f"[VALIDATE] To Datetime: {to_datetime}")
        frappe.logger().info(f"[VALIDATE] Doc Name: {self.name}")

        # Execute overlap query
        overlapping = frappe.db.sql("""
            SELECT name FROM `tabRoom Reservation`
            WHERE
                room = %(room)s AND
                date = %(date)s AND
                name != %(name)s AND NOT (
                    %(to_datetime)s <= TIMESTAMP(date, from_time)
                    OR %(from_datetime)s >= TIMESTAMP(date, to_time)
                )
        """, {
            "room": self.room,
            "date": self.date,
            "name": self.name,
            "from_datetime": from_datetime,
            "to_datetime": to_datetime
        })

        # Log SQL and result
        frappe.logger().info(f"[VALIDATE] Overlapping query result: {overlapping}")

        if overlapping:
            frappe.throw(_("This room is already booked for the selected time slot."))


        # Log SQL and result
        frappe.logger().info(f"[VALIDATE] Overlapping query result: {overlapping}")

        if overlapping:
            frappe.throw(_("This room is already booked for the selected time slot."))

        def after_insert(self):
            if self.docstatus == 0:
                self.booked_by = frappe.session.user
                # frappe.print("Booking by: ", self.booked_by)
                self.submit()

        def before_cancel(self):
            # Send cancellation email to attendees
            self.send_cancellation_email()

        # email on update
        def on_update_after_submit(self):
                frappe.logger().info(f"on_update_after_submit triggered for {self.name}")
                self.send_reschedule_email()
                

        def send_reschedule_email(self):
            try:
                attendee_emails = []

                # Only collect attendee emails if attendees are added
                for attendee_name in self.attendees_emails:
                    attendee = frappe.get_doc("PreciAttendees", attendee_name)
                    if attendee.email_ids:
                        email = frappe.db.get_value("User", attendee.email_ids, "email")
                        if email:
                            attendee_emails.append(email)


                # Collect invitee emails from invitees field
                invitee_emails = []
                if self.invitees_emails:
                    invitee_emails = [email.strip() for email in self.invitees_emails.split(',') if email.strip()]
                all_recipients = attendee_emails + invitee_emails

                subject = f"Meeting is reshedule: {self.subject}"
                message = f"""
                <p>Hello,</p>
                <p>You meeting has been reschedule as follows.</p>
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
                    frappe.msgprint("Meeting reschedule email sent successfully!")
                else:
                    frappe.msgprint("No recipients found to send email.")

            except Exception as e:
                frappe.log_error(frappe.get_traceback(), "Room Booking: Email Sending Error")
                frappe.msgprint(f"Failed to send email notification: {str(e)}")



        def send_cancellation_email(self):  
            try:
                attendee_emails = []

                # Only collect attendee emails if attendees are added
                for attendee_name in self.attendees_emails:
                    attendee = frappe.get_doc("PreciAttendees", attendee_name)
                    if attendee.email_ids:
                        email = frappe.db.get_value("User", attendee.email_ids, "email")
                        if email:
                            attendee_emails.append(email)

                # Collect invitee emails from invitees field
                invitee_emails = []
                if self.invitees_emails:
                    invitee_emails = [email.strip() for email in self.invitees_emails.split(',') if email.strip()]

                all_recipients = attendee_emails + invitee_emails

                subject = f"Meeting Cancelled: {self.subject}"
                message = f"""
                <p>Dear Sir/Madam,</p>
                <p>The meeting scheduled on {self.date} regarding {self.description} has been cancelled.</p>
                <p>For any update we will inform you soon.</p>
                """

                if all_recipients:
                    frappe.sendmail(
                        recipients=list(set(all_recipients)), 
                        subject=subject,
                        message=message
                    )
                    frappe.msgprint("Cancellation email sent successfully!")
                else:
                    frappe.msgprint("No recipients found to send cancellation email.")

            except Exception as e:
                frappe.log_error(frappe.get_traceback(), "Room Booking: Email Sending Error")
                frappe.msgprint(f"Failed to send cancellation email notification: {str(e)}")


        def before_submit(self):
            self.send_attendees_email()

        def send_attendees_email(self):
            try:
                attendee_emails = []

                # Only collect attendee emails if attendees are added
                for attendee_name in self.attendees_emails:
                    attendee = frappe.get_doc("PreciAttendees", attendee_name)
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

