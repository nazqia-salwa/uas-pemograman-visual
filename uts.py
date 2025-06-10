import tkinter as tk
from tkinter import messagebox, StringVar

def bayar():
    # Mengambil data dari input
    universitas = universitas_var.get()
    invoice = invoice_entry.get()
    nim = nim_entry.get()
    nama_mahasiswa = nama_entry.get()
    jumlah_ukt = jumlah_entry.get()
    metode_pembayaran = metode_var.get()

    # Validasi input
    if not invoice or not nim or not nama_mahasiswa or not jumlah_ukt:
        messagebox.showerror("Error", "Semua data harus diisi terlebih dahulu!")
        return

    # Jika lolos validasi, tampilkan info pembayaran
    messagebox.showinfo("Info Pembayaran", f"Pembayaran untuk {nama_mahasiswa} ({nim})\n" +
                        f"Universitas: {universitas}\nNomor Invoice: {invoice}\n" +
                        f"Jumlah UKT: Rp {jumlah_ukt}\n" +
                        f"Metode Pembayaran: {metode_pembayaran}\n\nPembayaran berhasil!")

# Membuat jendela utama
root = tk.Tk()
root.title("Pembayaran UKT")
root.geometry("400x500")

# Variabel
universitas_var = StringVar(value="Universitas Uin Ar-raniry")
metode_var = StringVar(value="Saldo Rekening")

# Label dan Entry
tk.Label(root, text="Pembayaran UKT", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Pilih Universitas").pack()
universitas_menu = tk.OptionMenu(root, universitas_var, "Universitas Uin Ar-raniry", "Universitas Lain")
universitas_menu.pack()

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
jumlah_entry.insert(0, "7500000")
jumlah_entry.pack()

tk.Label(root, text="Metode Pembayaran").pack()
tk.Radiobutton(root, text="Saldo Rekening", variable=metode_var, value="Saldo Rekening").pack()
tk.Radiobutton(root, text="Virtual Account Bank", variable=metode_var, value="Virtual Account Bank").pack()
tk.Radiobutton(root, text="Kartu Debit/Kredit", variable=metode_var, value="Kartu Debit/Kredit").pack()

# Tombol untuk bayar
pay_button = tk.Button(root, text="Bayar Sekarang", command=bayar, bg="blue", fg="white")
pay_button.pack(pady=20)

# Menjalankan aplikasi
root.mainloop()
