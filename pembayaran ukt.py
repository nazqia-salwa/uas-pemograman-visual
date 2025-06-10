import tkinter as tk
from tkinter import messagebox, StringVar, Toplevel, Text, Scrollbar
import sqlite3

# Koneksi dan setup awal database
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

def bayar():
    universitas = universitas_var.get()
    invoice = invoice_entry.get()
    nim = nim_entry.get()
    nama_mahasiswa = nama_entry.get()
    jumlah_ukt = jumlah_entry.get()
    metode_pembayaran = metode_var.get()

    if not invoice or not nim or not nama_mahasiswa or not jumlah_ukt:
        messagebox.showerror("Error", "Semua data harus diisi terlebih dahulu!")
        return

    # Simpan ke database
    cursor.execute("""
        INSERT INTO histori_pembayaran (universitas, invoice, nim, nama_mahasiswa, jumlah_ukt, metode)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (universitas, invoice, nim, nama_mahasiswa, jumlah_ukt, metode_pembayaran))
    conn.commit()

    messagebox.showinfo("Info Pembayaran", f"Pembayaran untuk {nama_mahasiswa} ({nim})\n" +
                        f"Universitas: {universitas}\nNomor Invoice: {invoice}\n" +
                        f"Jumlah UKT: Rp {jumlah_ukt}\n" +
                        f"Metode Pembayaran: {metode_pembayaran}\n\nPembayaran berhasil!")

def tampilkan_histori():
    cursor.execute("SELECT * FROM histori_pembayaran")
    data = cursor.fetchall()

    # Buat jendela baru untuk histori
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
            text_area.insert(tk.END, f"ID: {row[0]}\nNama: {row[4]}\nNIM: {row[3]}\n"
                                     f"Universitas: {row[1]}\nInvoice: {row[2]}\n"
                                     f"Jumlah UKT: Rp {row[5]}\nMetode: {row[6]}\n\n")

    scrollbar.config(command=text_area.yview)

# GUI Tkinter
root = tk.Tk()
root.title("Pembayaran UKT")
root.geometry("400x550")

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

tk.Label(root, text="Semester Genap 2024/2025").pack()

tk.Label(root, text="Jumlah UKT").pack()
jumlah_entry = tk.Entry(root)
jumlah_entry.insert(0, "2.000.000")
jumlah_entry.pack()

tk.Label(root, text="Metode Pembayaran").pack()
tk.Radiobutton(root, text="Saldo Rekening", variable=metode_var, value="Saldo Rekening").pack()
tk.Radiobutton(root, text="Virtual Account Bank", variable=metode_var, value="Virtual Account Bank").pack()
tk.Radiobutton(root, text="Kartu Debit/Kredit", variable=metode_var, value="Kartu Debit/Kredit").pack()

tk.Button(root, text="Bayar Sekarang", command=bayar, bg="blue", fg="white").pack(pady=10)
tk.Button(root, text="Lihat Histori Pembayaran", command=tampilkan_histori, bg="green", fg="white").pack()

root.mainloop()
conn.close()
