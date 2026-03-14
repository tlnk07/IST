# 🌐 Internet Speed Test (IST)
A high-performance, dark-themed network diagnostic tool built with Python. Measure your connection quality with precision and style.

## ✨ Features

### Network Performance Analytics
- **Real-Time Speed Testing** – Accurately measure Download and Upload speeds using integrated speedtest-cli engines.
- **Latency (Ping) Measurement** – Get instant feedback on your network response time for gaming and streaming stability.
- **Dynamic Progress Visualization** – Track the testing process with smooth, real-time progress bars and status updates.
- **Unit Conversion** – Automatic calculation and display of results in Mbps for industry-standard benchmarking.
### Modern User Experience
- **Sleek GUI** – A modern, responsive dark-themed interface crafted with CustomTkinter for a professional desktop experience.
- **Asynchronous Execution** – Multi-threaded architecture ensures the UI remains fluid and responsive while heavy network tests run in the background.
- **Minimalist Design** – High-contrast dashboard focusing on the most critical network metrics.

## 📦 Requirements
- Python 3.8+
- CustomTkinter (v5.2.2) – For the modern UI components.
- speedtest-cli (v2.1.3) – Core engine for bandwidth measurement.
- pyspeedtest (v1.2.7) – Reliable fallback for latency and speed verification.

## 🔧 Installation
- Clone or download this repository.
- Install the required packages using pip:
```bash
pip install -r requirements.txt
```
- Run the application:
```bash
python main.py
```
