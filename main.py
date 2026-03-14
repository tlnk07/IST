import customtkinter as ctk
import speedtest
import threading
import random
from tkinter import messagebox

# Cấu hình giao diện
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SpeedTestApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Internet Speed Test")
        self.window.geometry("600x650")
        self.window.resizable(False, False)

        # Biến lưu kết quả
        self.download_speed = ctk.StringVar(value="0.00 Mbps")
        self.upload_speed = ctk.StringVar(value="0.00 Mbps")
        self.ping = ctk.StringVar(value="0 ms")
        self.test_in_progress = False

        # Biến cho hiệu ứng chạy số
        self.download_anim_running = False
        self.upload_anim_running = False

        self.setup_ui()

    def setup_ui(self):
        # Khung chính
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tiêu đề
        title_label = ctk.CTkLabel(
            main_frame,
            text="🌐 Internet Speed Test",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        title_label.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            main_frame,
            text="Measure your download, upload speed and ping",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 20))

        # Khung hiển thị tốc độ
        display_frame = ctk.CTkFrame(main_frame)
        display_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # Download
        download_label = ctk.CTkLabel(
            display_frame,
            text="Download ⬇️",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        download_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.download_display = ctk.CTkLabel(
            display_frame,
            textvariable=self.download_speed,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#2ecc71"
        )
        self.download_display.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Upload
        upload_label = ctk.CTkLabel(
            display_frame,
            text="Upload ⬆️",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        upload_label.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="w")

        self.upload_display = ctk.CTkLabel(
            display_frame,
            textvariable=self.upload_speed,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#3498db"
        )
        self.upload_display.grid(row=1, column=1, padx=20, pady=(0, 15), sticky="w")

        # Ping
        ping_label = ctk.CTkLabel(
            display_frame,
            text="Ping ❓",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        ping_label.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="w")

        self.ping_display = ctk.CTkLabel(
            display_frame,
            textvariable=self.ping,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#e67e22"
        )
        self.ping_display.grid(row=3, column=0, padx=20, pady=(0, 15), sticky="w")

        # Thanh tiến trình và trạng thái
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=5)

        # Nút bắt đầu
        self.start_button = ctk.CTkButton(
            main_frame,
            text="▶ Start Speed Test",
            command=self.start_test,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2ecc71",
            hover_color="#27ae60"
        )
        self.start_button.pack(pady=15)

    def start_test(self):
        if self.test_in_progress:
            return

        # Reset hiển thị
        self.download_speed.set("0.00 Mbps")
        self.upload_speed.set("0.00 Mbps")
        self.ping.set("0 ms")
        self.progress_bar.set(0)
        self.status_label.configure(text="Initializing...")

        # Vô hiệu hóa nút
        self.start_button.configure(state="disabled", text="Testing...")

        # Chạy kiểm tra trong luồng riêng
        self.test_in_progress = True
        thread = threading.Thread(target=self.run_speed_test)
        thread.daemon = True
        thread.start()

    def run_speed_test(self):
        try:
            # Tạo đối tượng Speedtest
            st = speedtest.Speedtest(secure=True)

            # Tìm server tốt nhất
            self.update_status("Finding best server...")
            st.get_best_server()

            # Kiểm tra download với hiệu ứng số chạy
            self.update_status("Testing download speed...")
            self.update_progress(0.3)
            # Bắt đầu animation cho download
            self.start_download_animation()
            # Thực hiện đo thật
            download_speed = st.download() / 1_000_000  # Mbps
            # Dừng animation và cập nhật kết quả thật
            self.stop_download_animation(download_speed)

            # Kiểm tra upload với hiệu ứng số chạy
            self.update_status("Testing upload speed...")
            self.update_progress(0.6)
            self.start_upload_animation()
            upload_speed = st.upload() / 1_000_000
            self.stop_upload_animation(upload_speed)

            # Lấy ping
            ping = st.results.ping
            self.update_ping(f"{ping:.0f} ms")

            self.update_progress(1.0)
            self.update_status("Test completed!")

        except Exception as e:
            self.update_status("Error occurred!")
            messagebox.showerror("Speed Test Error", f"An error occurred:\n{str(e)}")
        finally:
            self.test_in_progress = False
            self.start_button.after(0, lambda: self.start_button.configure(state="normal", text="▶ Start Speed Test"))

    def start_download_animation(self):
        """Bắt đầu hiệu ứng chạy số cho download"""
        self.download_anim_running = True
        self.current_download = 0
        self.update_download_animation()

    def update_download_animation(self):
        if not self.download_anim_running:
            return
        # Tăng dần giá trị hiện tại (mô phỏng)
        self.current_download += random.uniform(1.0, 5.0)
        # Giới hạn để không quá lớn
        if self.current_download > 200:
            self.current_download = random.uniform(50, 150)
        self.download_speed.set(f"{self.current_download:.2f} Mbps")
        self.window.after(150, self.update_download_animation)  # Cập nhật mỗi 150ms

    def stop_download_animation(self, final_value):
        """Dừng animation và hiển thị kết quả thật"""
        self.download_anim_running = False
        self.download_speed.set(f"{final_value:.2f} Mbps")

    def start_upload_animation(self):
        """Bắt đầu hiệu ứng chạy số cho upload"""
        self.upload_anim_running = True
        self.current_upload = 0
        self.update_upload_animation()

    def update_upload_animation(self):
        if not self.upload_anim_running:
            return
        self.current_upload += random.uniform(0.5, 3.0)
        if self.current_upload > 100:
            self.current_upload = random.uniform(20, 80)
        self.upload_speed.set(f"{self.current_upload:.2f} Mbps")
        self.window.after(150, self.update_upload_animation)

    def stop_upload_animation(self, final_value):
        self.upload_anim_running = False
        self.upload_speed.set(f"{final_value:.2f} Mbps")

    def update_progress(self, value):
        self.window.after(0, lambda: self.progress_bar.set(value))

    def update_ping(self, value):
        self.window.after(0, lambda: self.ping.set(value))

    def update_status(self, message):
        self.window.after(0, lambda: self.status_label.configure(text=message))

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = SpeedTestApp()
    app.run()