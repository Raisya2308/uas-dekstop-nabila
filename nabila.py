import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Fungsi untuk membuat koneksi ke database
def get_db_connection():
    return sqlite3.connect('petshop.db')

# Fungsi untuk membuat tabel hewan jika belum ada
def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS hewan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama TEXT NOT NULL,
        jenis TEXT NOT NULL,
        harga REAL NOT NULL,
        usia INTEGER NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

# Fungsi untuk menambah data hewan
def tambah_data():
    nama = entry_nama.get()
    jenis = entry_jenis.get()
    harga = entry_harga.get()
    usia = entry_usia.get()

    # Validasi input
    if nama and jenis and harga and usia:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO hewan (nama, jenis, harga, usia) VALUES (?, ?, ?, ?)', 
                           (nama, jenis, float(harga), int(usia)))
            conn.commit()
            conn.close()
            messagebox.showinfo("Info", "Data hewan berhasil ditambahkan!")
            clear_entries()
            tampilkan_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah data: {str(e)}")
    else:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")

# Fungsi untuk menampilkan data hewan di Treeview
def tampilkan_data():
    # Clear existing rows in Treeview
    for row in tree.get_children():
        tree.delete(row)

    # Fetch data from the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hewan")
    rows = cursor.fetchall()
    
    # Insert each row into the Treeview
    for row in rows:
        tree.insert('', 'end', values=row)  # This ensures all columns are inserted

    conn.close()

# Fungsi untuk mencari data hewan berdasarkan nama atau jenis
def cari_data():
    search = entry_search.get()
    for row in tree.get_children():
        tree.delete(row)

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hewan WHERE nama LIKE ? OR jenis LIKE ?", 
                   ('%' + search + '%', '%' + search + '%'))
    rows = cursor.fetchall()

    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close()

# Fungsi untuk mengubah data hewan yang dipilih
def ubah_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin diubah!")
        return

    item_id = tree.item(selected_item[0])['values'][0]
    nama = entry_nama.get()
    jenis = entry_jenis.get()
    harga = entry_harga.get()
    usia = entry_usia.get()

    # Validasi input
    if nama and jenis and harga and usia:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE hewan SET nama=?, jenis=?, harga=?, usia=? WHERE id=?", 
                           (nama, jenis, float(harga), int(usia), item_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Info", "Data hewan berhasil diubah!")
            clear_entries()
            tampilkan_data()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengubah data: {str(e)}")
    else:
        messagebox.showwarning("Peringatan", "Semua field harus diisi!")

# Fungsi untuk menghapus data hewan yang dipilih
def hapus_data():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Peringatan", "Pilih data yang ingin dihapus!")
        return

    item_id = tree.item(selected_item[0])['values'][0]
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hewan WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Info", "Data hewan berhasil dihapus!")
        tampilkan_data()
    except Exception as e:
        messagebox.showerror("Error", f"Gagal menghapus data: {str(e)}")

# Fungsi untuk membersihkan entry fields
def clear_entries():
    entry_nama.delete(0, 'end')
    entry_jenis.delete(0, 'end')
    entry_harga.delete(0, 'end')
    entry_usia.delete(0, 'end')

# Membuat window utama aplikasi
root = tk.Tk()
root.title("Aplikasi Pet Shop")
root.geometry("700x600")
root.config(bg="#85A98F")  # Lighter brown color (#8174A0)

# Frame untuk input data
frame_input = tk.Frame(root, bg="#E5E3D4", padx=10, pady=10)  # Lighter frame to contrast with brown background
frame_input.pack(pady=20)

# Label dan entry fields
label_nama = tk.Label(frame_input, text="Nama Hewan", font=("Arial", 10), bg="#E5E3D4")
label_nama.grid(row=0, column=0, pady=5, sticky="w")
entry_nama = tk.Entry(frame_input, font=("Arial", 10), width=30)
entry_nama.grid(row=0, column=1, pady=5)

label_jenis = tk.Label(frame_input, text="Jenis Hewan", font=("Arial", 10), bg="#E5E3D4")
label_jenis.grid(row=1, column=0, pady=5, sticky="w")
entry_jenis = tk.Entry(frame_input, font=("Arial", 10), width=30)
entry_jenis.grid(row=1, column=1, pady=5)

label_harga = tk.Label(frame_input, text="Harga Hewan (Rp)", font=("Arial", 10), bg="#E5E3D4")
label_harga.grid(row=2, column=0, pady=5, sticky="w")
entry_harga = tk.Entry(frame_input, font=("Arial", 10), width=30)
entry_harga.grid(row=2, column=1, pady=5)

label_usia = tk.Label(frame_input, text="Usia Hewan (Tahun)", font=("Arial", 10), bg="#E5E3D4")
label_usia.grid(row=3, column=0, pady=5, sticky="w")
entry_usia = tk.Entry(frame_input, font=("Arial", 10), width=30)
entry_usia.grid(row=3, column=1, pady=5)

# Tombol untuk tambah, ubah, hapus
btn_tambah = tk.Button(frame_input, text="Tambah Hewan", font=("Arial", 10), bg="#A59D84", fg="white", command=tambah_data)
btn_tambah.grid(row=4, column=0, pady=10)

btn_ubah = tk.Button(frame_input, text="Ubah Hewan", font=("Arial", 10), bg="#A59D84", fg="white", command=ubah_data)
btn_ubah.grid(row=4, column=1, pady=10)

btn_hapus = tk.Button(frame_input, text="Hapus Hewan", font=("Arial", 10), bg="#A59D84", fg="white", command=hapus_data)
btn_hapus.grid(row=4, column=2, pady=10)

# Entry untuk pencarian
label_search = tk.Label(root, text="Cari Hewan", font=("Arial", 10), bg="#B6A28E", fg="white")
label_search.pack(pady=10)
entry_search = tk.Entry(root, font=("Arial", 10), width=50)
entry_search.pack(pady=5)
btn_search = tk.Button(root, text="Cari", font=("Arial", 10), bg="#B59F78", fg="white", command=cari_data)
btn_search.pack(pady=5)

# Treeview untuk menampilkan data hewan
tree = ttk.Treeview(root, columns=("ID", "Nama", "Jenis", "Harga", "Usia"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama Hewan")
tree.heading("Jenis", text="Jenis Hewan")
tree.heading("Harga", text="Harga Hewan (Rp)")
tree.heading("Usia", text="Usia Hewan (Tahun)")
tree.pack(fill=tk.BOTH, expand=True)

# Jalankan fungsi create_table untuk memastikan tabel ada
create_table()

# Menampilkan data awal
tampilkan_data()

root.mainloop()
