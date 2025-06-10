import tkinter as tk
from tkinter import messagebox, StringVar, Toplevel, Text, Scrollbar
import sqlite3

# ================== KONEKSI DAN SETUP DATABASE ==================
conn = sqlite3.connect("ukt.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS histori_pembayaran (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        universitas TEXT,
        invoice TEXT,
        nim TEXT,
        nama_mahasiswa TEXT,
        jumlah_ukt INTEGER,
        metode TEXT
    )
""")
conn.commit()

# ================== FUNGSI APLIKASI ==================

def bayar():
    universitas = universitas_var.get()
    invoice = invoice_entry.get().strip()
    nim = nim_entry.get().strip()
    nama = nama_entry.get().strip()
    jumlah = jumlah_entry.get().strip()
    metode = metode_var.get()

    if not invoice or not nim or not nama or not jumlah:
        messagebox.showerror("Error", "Semua data harus diisi!")
        return

    if not jumlah.isdigit():
        messagebox.showerror("Error", "Jumlah UKT harus berupa angka!")
        return

    cursor.execute("""
        INSERT INTO histori_pembayaran (universitas, invoice, nim, nama_mahasiswa, jumlah_ukt, metode)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (universitas, invoice, nim, nama, int(jumlah), metode))
    conn.commit()

    messagebox.showinfo("Sukses", f"Pembayaran untuk {nama} berhasil disimpan.")
    bersihkan_input()

def tampilkan_histori():
    cursor.execute("SELECT * FROM histori_pembayaran")
    data = cursor.fetchall()

    histori_window = Toplevel(root)
    histori_window.title("Histori Pembayaran")
    histori_window.geometry("500x400")

    scrollbar = Scrollbar(histori_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_area = Text(histori_window, wrap=tk.WORD, yscrollcommand=scrollbar.set)
    text_area.pack(expand=True, fill="both")

    if not data:
        text_area.insert(tk.END, "Belum ada histori pembayaran.")
    else:
        for row in data:
            text_area.insert(tk.END, f"ID: {row[0]}\n"
                                     f"Nama: {row[4]}\n"
                                     f"NIM: {row[3]}\n"
                                     f"Universitas: {row[1]}\n"
                                     f"Invoice: {row[2]}\n"
                                     f"Jumlah UKT: Rp {row[5]}\n"
                                     f"Metode: {row[6]}\n\n")

    scrollbar.config(command=text_area.yview)

def reset_data():
    konfirmasi = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus semua histori pembayaran?")
    if konfirmasi:
        try:
            cursor.execute("DELETE FROM histori_pembayaran")
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='histori_pembayaran'")
            conn.commit()
            messagebox.showinfo("Sukses", "Data berhasil direset. ID mulai dari 1 lagi.")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

def bersihkan_input():
    invoice_entry.delete(0, tk.END)
    nim_entry.delete(0, tk.END)
    nama_entry.delete(0, tk.END)
    jumlah_entry.delete(0, tk.END)
    jumlah_entry.insert(0, "2500000")

# ================== ANTARMUKA TKINTER ==================
root = tk.Tk()
root.title("Pembayaran UKT")
root.geometry("400x600")

universitas_var = StringVar(value="Universitas Uin Ar-raniry")
metode_var = StringVar(value="Saldo Rekening")

tk.Label(root, text="Pembayaran UKT", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Pilih Universitas").pack()
tk.OptionMenu(root, universitas_var, "Universitas Uin Ar-raniry", "Universitas Lain").pack()

tk.Label(root, text="Nomor Invoice").pack()
invoice_entry = tk.Entry(root)
invoice_entry.pack()

tk.Label(root, text="Nomor Induk Mahasiswa (NIM)").pack()
nim_entry = tk.Entry(root)
nim_entry.pack()

tk.Label(root, text="Nama Mahasiswa").pack()
nama_entry = tk.Entry(root)
nama_entry.pack()

tk.Label(root, text="Semester Genap 2024/2025", font=("Arial", 10, "italic")).pack(pady=5)

tk.Label(root, text="Jumlah UKT").pack()
jumlah_entry = tk.Entry(root)
jumlah_entry.insert(0, "2500000")
jumlah_entry.pack()

tk.Label(root, text="Metode Pembayaran").pack()
tk.Radiobutton(root, text="Saldo Rekening", variable=metode_var, value="Saldo Rekening").pack()
tk.Radiobutton(root, text="Virtual Account Bank", variable=metode_var, value="Virtual Account Bank").pack()
tk.Radiobutton(root, text="Kartu Debit/Kredit", variable=metode_var, value="Kartu Debit/Kredit").pack()

tk.Button(root, text="Bayar Sekarang", command=bayar, bg="blue", fg="white").pack(pady=10)
tk.Button(root, text="Lihat Histori Pembayaran", command=tampilkan_histori, bg="green", fg="white").pack(pady=5)
tk.Button(root, text="Reset Data", command=reset_data, bg="red", fg="white").pack(pady=5)

# Saat ditutup
def keluar():
    conn.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", keluar)
root.mainloop()
