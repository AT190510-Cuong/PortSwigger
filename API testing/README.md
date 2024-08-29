# API testing

- https://hackmd.io/@W8hH7NRgT8-m1aWaJJjIoA/H1mdfzTOT?utm_source=preview-mode&utm_medium=rec#Truncating-query-strings

## Khái niệm & Khai thác &

### Khái niệm

### Khai thác

### Phòng tránh

## 1. Lab: Exploiting an API endpoint using documentation

### Đề bài

![image](https://hackmd.io/_uploads/rJ6SRITjA.png)

### Phân tích

Hãy thử một số điểm cuối có thể tham khảo tài liệu API như `/api`

![image](https://hackmd.io/_uploads/r18JlPTsR.png)

Tôi thấy rằng có một api DELETE sẽ giúp chúng ta xóa một tài khoản bằng cách gửi tên người dùng của tài khoản đó

![image](https://hackmd.io/_uploads/S1ENlD6sR.png)

![image](https://hackmd.io/_uploads/HJ3VewpoR.png)

Có vẻ như chúng ta cần phải đăng nhập sử dụng api này

### Khai thác

Đăng nhập bằng thông tin xác thực của wiener

![image](https://hackmd.io/_uploads/SkUwxvpi0.png)

Sau đó thử sử dụng api DELETE thêm một lần nữa

![image](https://hackmd.io/_uploads/SJiteD6sR.png)

Thành công. Phòng thí nghiệm đã được giải quyết

## 2. Lab: Finding and exploiting an unused API endpoint

### Đề bài

![image](https://hackmd.io/_uploads/B1MN8PTsC.png)

### Khai thác

![image](https://hackmd.io/_uploads/Sk4i8wToR.png)

![image](https://hackmd.io/_uploads/H1zbwwaiA.png)

![image](https://hackmd.io/_uploads/r1oGvDajC.png)

![image](https://hackmd.io/_uploads/Sy1qwvTiR.png)

![image](https://hackmd.io/_uploads/By5pDPasA.png)

![image](https://hackmd.io/_uploads/SJwluvpiA.png)

![image](https://hackmd.io/_uploads/Bk-Zuw6j0.png)

## 3. Lab: Exploiting a mass assignment vulnerability

### Đề bài

![image](https://hackmd.io/_uploads/BJUC3w6o0.png)

### Khai thác

![image](https://hackmd.io/_uploads/r1E1RD6sA.png)

![image](https://hackmd.io/_uploads/r1j1RPTsR.png)

![image](https://hackmd.io/_uploads/BkzbCPajC.png)

![image](https://hackmd.io/_uploads/HyxSAD6o0.png)

![image](https://hackmd.io/_uploads/rkqq0vpjC.png)

![image](https://hackmd.io/_uploads/SyHMkdaj0.png)

![image](https://hackmd.io/_uploads/BkeGyupsR.png)

![image](https://hackmd.io/_uploads/Bym0JOaiR.png)

![image](https://hackmd.io/_uploads/Sk3LWupoR.png)

![image](https://hackmd.io/_uploads/BkvHZOTi0.png)

## 4. Lab: Exploiting server-side parameter pollution in a query string

### Đề bài

![image](https://hackmd.io/_uploads/rJ8lVdaiC.png)

### Khai thác

![image](https://hackmd.io/_uploads/SJEQL_psC.png)

![image](https://hackmd.io/_uploads/BkFuLupsA.png)

![image](https://hackmd.io/_uploads/BJaCU_6o0.png)

![image](https://hackmd.io/_uploads/SkMAUdTj0.png)

![image](https://hackmd.io/_uploads/BJ8b_dpi0.png)

![image](https://hackmd.io/_uploads/HJBEudaiR.png)

![image](https://hackmd.io/_uploads/SJ1rdOpjC.png)

![image](https://hackmd.io/_uploads/S1eI_dpiR.png)

![image](https://hackmd.io/_uploads/H1ljduTo0.png)

![image](https://hackmd.io/_uploads/B1w3ddpiR.png)

![image](https://hackmd.io/_uploads/Hy0COdpjA.png)

![image](https://hackmd.io/_uploads/BkjyFupsA.png)

## 5. Lab: Exploiting server-side parameter pollution in a REST URL

### Đề bài

![image](https://hackmd.io/_uploads/BkpmsuTiC.png)

### khai thác

![image](https://hackmd.io/_uploads/SJgtq_6sA.png)

![image](https://hackmd.io/_uploads/rkBh5u6i0.png)

![image](https://hackmd.io/_uploads/S15ysuaoC.png)

![image](https://hackmd.io/_uploads/HJalsOpjR.png)

![image](https://hackmd.io/_uploads/r1Ibju6jA.png)
