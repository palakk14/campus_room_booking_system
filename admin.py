from flask import render_template, request, redirect, session, flash
from app import app
from db import get_db_connection


@app.route('/admin')
def admin():
    if 'user_id' not in session:
        return redirect('/login')

    if session.get('role') != 'admin':
        return redirect('/dashboard')

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    # Stats
    cur.execute("SELECT COUNT(*) AS total_users FROM users WHERE role != 'admin'")
    total_users = cur.fetchone()['total_users']

    cur.execute("SELECT COUNT(*) AS total_rooms FROM rooms")
    total_rooms = cur.fetchone()['total_rooms']

    cur.execute("SELECT COUNT(*) AS total_bookings FROM bookings")
    total_bookings = cur.fetchone()['total_bookings']

    # Rooms
    cur.execute("SELECT * FROM rooms")
    rooms = cur.fetchall()

    # Bookings
    cur.execute("""
        SELECT bookings.*, users.name, rooms.room_name
        FROM bookings
        JOIN users ON bookings.user_id = users.user_id
        JOIN rooms ON bookings.room_id = rooms.room_id
        ORDER BY booking_id DESC
    """)
    bookings = cur.fetchall()

    # Users
    cur.execute("SELECT user_id, name, email, role FROM users WHERE role != 'admin'")
    users = cur.fetchall()

    cur.close()
    conn.close()

    return render_template(
        "admin.html",
        total_users=total_users,
        total_rooms=total_rooms,
        total_bookings=total_bookings,
        rooms=rooms,
        bookings=bookings,
        users=users
    )


@app.route('/addroom', methods=['GET', 'POST'])
def add_room():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    if request.method == 'POST':
        room_name = request.form['room_name']
        capacity = request.form['capacity']
        room_type = request.form['type']
        status = request.form['status']

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO rooms(room_name, capacity, type, status)
            VALUES(%s,%s,%s,%s)
        """, (room_name, capacity, room_type, status))

        conn.commit()
        cur.close()
        conn.close()

        flash("Room added successfully", "success")
        return redirect('/admin')

    return render_template("add_room.html")


@app.route('/deleteroom/<int:room_id>')
def delete_room(room_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM rooms WHERE room_id=%s", (room_id,))
    conn.commit()

    cur.close()
    conn.close()

    flash("Room deleted successfully", "success")
    return redirect('/admin')


@app.route('/toggle_room/<int:room_id>')
def toggle_room(room_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE rooms
        SET status =
        CASE
            WHEN status='Available' THEN 'Unavailable'
            ELSE 'Available'
        END
        WHERE room_id=%s
    """, (room_id,))

    conn.commit()

    cur.close()
    conn.close()

    flash("Room status updated", "warning")
    return redirect('/admin')


@app.route('/admin_cancel/<int:booking_id>')
def admin_cancel_booking(booking_id):
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM bookings WHERE booking_id=%s", (booking_id,))
    conn.commit()

    cur.close()
    conn.close()

    flash("Booking cancelled by admin", "danger")
    return redirect('/admin')