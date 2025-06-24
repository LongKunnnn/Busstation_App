# Sử dụng một image Python cơ sở
FROM python:3.9-slim-buster

# Đặt thư mục làm việc trong container
WORKDIR /app

# Cài đặt các gói cần thiết cho GUI (Tkinter) và kết nối MySQL
# Đã xóa 'libtcl-img' vì không tìm thấy gói này
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tk \
    tcl \
    libtk-img \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Cài đặt mysql-connector-python
RUN pip install mysql-connector-python --break-system-packages

# Sao chép mã nguồn ứng dụng vào container
COPY app/ .

# Lệnh mặc định để chạy ứng dụng khi container khởi động
CMD ["python", "main_app.py"]