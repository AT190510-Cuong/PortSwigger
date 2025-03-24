# Web LLM attacks

![image](https://hackmd.io/_uploads/B1NDCAj5Jx.png)

## Khái niệm & Phát hiện& khai thác

### Khái niệm

- một cuộc tấn công có thể:
  - Truy xuất dữ liệu mà LLM có quyền truy cập. Các nguồn dữ liệu phổ biến như vậy bao gồm lời nhắc của LLM, bộ dữ liệu đào tạo và API được cung cấp cho mô hình
  - Kích hoạt các hành động có hại thông qua API. Ví dụ, kẻ tấn công có thể sử dụng LLM để thực hiện cuộc tấn công SQL injection vào API mà nó có quyền truy cập
  - Ở cấp độ cao, việc tấn công tích hợp LLM thường tương tự như khai thác lỗ hổng giả mạo yêu cầu phía máy chủ (SSRF). Trong cả hai trường hợp, kẻ tấn công đều lợi dụng hệ thống phía máy chủ để tấn công vào một thành phần riêng biệt không thể truy cập trực tiếp

### Phát hiện lỗ hổng LLM

1. Xác định các đầu vào của LLM, bao gồm cả đầu vào trực tiếp (như lời prompt) và gián tiếp (như dữ liệu đào tạo).
2. Tìm hiểu xem LLM có quyền truy cập vào dữ liệu và API nào.
3. Thăm dò bề mặt tấn công mới này để tìm lỗ hổng.

![image](https://hackmd.io/_uploads/SkktLw29Jx.png)

có thể được thực hiện theo hai cách:

- Trực tiếp, ví dụ, thông qua tin nhắn tới bot trò chuyện.
- Gián tiếp, khi kẻ tấn công gửi lời nhắc qua một nguồn bên ngoài. Ví dụ, lời nhắc có thể được đưa vào dữ liệu đào tạo hoặc đầu ra từ lệnh gọi API.

- `Could you remind me of...?` and `Complete a paragraph starting with...`

## 1. Lab: Exploiting LLM APIs with excessive agency

### Đề bài

![image](https://hackmd.io/_uploads/B1eokv35Jg.png)

### Khai thác

```
	what apis can you access?
```

![image](https://hackmd.io/_uploads/ByDZbD251x.png)

![image](https://hackmd.io/_uploads/HyheGv39yl.png)

- đăng nhập được vào tài khoản carlos và thực hiện xóa tài khoản

![image](https://hackmd.io/_uploads/B1_7Mv2qye.png)

![image](https://hackmd.io/_uploads/rJCNGwh9Jg.png)

## 2. Lab: Exploiting vulnerabilities in LLM APIs

### Đề bài

![image](https://hackmd.io/_uploads/S1FluDn5kx.png)

### Phân tích

- Phòng thí nghiệm này chứa lỗ hổng tiêm lệnh hệ điều hành có thể bị khai thác thông qua API của nó. Bạn có thể gọi các API này thông qua LLM. Để giải quyết phòng thí nghiệm, hãy xóa tệp morale.txt khỏi thư mục gốc của Carlos.

### Khai thác

```
	what apis can you access?
```

![image](https://hackmd.io/_uploads/rylLKw2c1e.png)

```
what are the inputs for each api?
```

![image](https://hackmd.io/_uploads/B1TP5Ph9kx.png)

tại chức năng subcribe có chuyền vào email nó sẽ gửi email về địa chỉ này

![image](https://hackmd.io/_uploads/BktLswnqyl.png)

![image](https://hackmd.io/_uploads/Skvrjw39kg.png)

- xóa tài khoản carlos

![image](https://hackmd.io/_uploads/HyuRiP2c1x.png)

![image](https://hackmd.io/_uploads/H1J0swnqyg.png)
