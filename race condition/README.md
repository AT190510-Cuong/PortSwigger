# race condition

## Khái niệm & Phòng Tránh

### Khái niệm

Tấn công race condition còn được gọi là time-of-check, time-of-use (TOCTOU) xảy ra khi 2 hoặc nhiều threads cố gắng truy cập hoặc sử dùng cùng một tài nguyên chung trong cùng một thời điểm dẫn tới việc kết quả bị sai so với quy trình thông thường.

![image](https://hackmd.io/_uploads/ryJN8FLF0.png)

### Phòng tránh

Sử dụng threading’s lock để khoá thread đó lại đến khi xử lý xong.

## 1. Lab: Limit overrun race conditions

### Đề bài

![image](https://hackmd.io/_uploads/H1NClN8tA.png)

### Phân tích

- chúng ta cần mua Lightweight L33t Leather Jacket.
- Nhưng tín dụng cửa hàng wiener chỉ có 50,00 đô la
- mình đăng nhập và chọn sản phẩm Lightweight L33t Leather Jacket. vào giỏ hàng

![image](https://hackmd.io/_uploads/HkDNVNLt0.png)

khi chúng ta nhập mã giảm giá

1. Đó là một yêu cầu POST tới/cart/coupon
2. Máy chủ sẽ kiểm tra xem coupon=PROMO20đã được sử dụng hay chưa
3. Nếu không áp dụng thì áp dụng, tính toán và chiết khấu giá, sau đó lưu ở đâu đó trong cơ sở dữ liệu mà phiếu giảm giá này được áp dụng và trả về "Coupon applied"

Đây là nơi có thể phát sinh tình trạng chạy đua. Chúng ta sẽ kiểm tra bằng cách sử dụng Burp Repeater để gửi nhiều yêu cầu song song

### Khai thác

tạo 1 group request áp dụng mã giảm giá

![image](https://hackmd.io/_uploads/ByxLvEIYA.png)

- chọn opttion gửi các gói tin sonng song

![image](https://hackmd.io/_uploads/Hkjow4IFA.png)

- chúng ta gửi và thấy mã giảm giá đã được áp dụng nhiều lần

![image](https://hackmd.io/_uploads/Hyt1Y4Lt0.png)

- và bây giờ chúng ta đã có đủ tiền mua

![image](https://hackmd.io/_uploads/Skj-tELKR.png)

## 2. Lab: Bypassing rate limits via race conditions

### Đề bài

![image](https://hackmd.io/_uploads/SkIFjNUtC.png)

### Phân tích

- Cơ chế đăng nhập của phòng thí nghiệm này sử dụng giới hạn tốc độ để chống lại các cuộc tấn công brute-force. Tuy nhiên, điều này có thể bị bỏ qua do tình trạng chạy đua.
- mình cần tìm cách khai thác tình trạng chạy đua để vượt qua giới hạn tốc độ.
  Tấn công bằng cách brute force để tìm ra mật khẩu của người dùng carlos.
  Đăng nhập và truy cập bảng quản trị.
  Xóa người dùng carlos.
  Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: wiener:peter.

luồng hoạt động của chương trình có thể như sau

![image](https://hackmd.io/_uploads/HkwuSr8FA.png)

khi nhập sai mật khẩu quá 5 lần chúng ta sẽ bị chặn 1 khoảng thời gian:

- chúng ta có thể tận dụng race condition để guwir nhiều gói tin trước khi faill_attempt ++ vượt quá 5

### Khai thác

- Nhấp chuột phải vào yêu cầu đó > Tiện ích mở rộng > Turbo Intruder > Gửi đến turbo invader

![image](https://hackmd.io/_uploads/S1yRZr8K0.png)

![image](https://hackmd.io/_uploads/HkzlzBIYA.png)

- Trong yêu cầu, hãy đổi tên người dùng thành carlos và mật khẩu thành %s như thế này

![image](https://hackmd.io/_uploads/ryQd4HIFA.png)

- Click Attack và chờ kết quả. Ta sẽ thấy có 1 request trả về với trạng thái 302

![image](https://hackmd.io/_uploads/ryjr4BIYR.png)

- Sử dụng mật khẩu đó để đăng nhập vào tài khoản carlos và chúng ta có thể giải quyết phòng thí nghiệm

![image](https://hackmd.io/_uploads/ryQW4SLFC.png)

![image](https://hackmd.io/_uploads/B1VGNB8tA.png)

![image](https://hackmd.io/_uploads/HkfmESLK0.png)

## 3. Lab: Multi-endpoint race conditions

### Đề bài

![image](https://hackmd.io/_uploads/HkLhvHUYC.png)

### Phân tích

- chúng ta cần mua Lightweight L33t Leather Jacket.

Trong Repeater, hãy thử gửi GET /cartyêu cầu có và không có cookie phiên của bạn.

Với cookie phiên:

![image](https://hackmd.io/_uploads/HJuJB88FR.png)

Không có cookie phiên:

![image](https://hackmd.io/_uploads/SywfHLIt0.png)

Xác nhận rằng nếu không có cookie phiên, bạn chỉ có thể truy cập vào một giỏ hàng trống. Từ đó, bạn có thể suy ra rằng:

Trạng thái của giỏ hàng được lưu trữ trên máy chủ trong phiên của bạn.
Bất kỳ hoạt động nào trên giỏ hàng đều được mã hóa theo ID phiên của bạn hoặc ID người dùng được liên kết.
Điều này cho biết có khả năng xảy ra va chạm
Lưu ý rằng việc gửi và nhận xác nhận đơn hàng thành công diễn ra trong một chu kỳ yêu cầu/phản hồi duy nhất

Hãy cân nhắc rằng có thể có một khoảng thời gian chờ giữa thời điểm đơn hàng của bạn được xác thực và thời điểm đơn hàng được xác nhận. Điều này có thể cho phép bạn thêm nhiều mặt hàng hơn vào đơn hàng sau khi máy chủ kiểm tra xem bạn có đủ tín dụng trong cửa hàng hay không

![image](https://hackmd.io/_uploads/S1THE88KA.png)

### Khai thác

- mình thêm vào giỏ hàng gift card

![image](https://hackmd.io/_uploads/SyQuS8UY0.png)

- tạo 1 group trong đó có thanh toán giỏ hàng và mình add thêm 2 request thêm vào giỏ hàng Lightweight "l33t" Leather Jacket

![image](https://hackmd.io/_uploads/S1q-kUIKR.png)

![image](https://hackmd.io/_uploads/BkNu4IItC.png)

- gửi group request sonng song và thấy rằng kết quả trả về khi add Lightweight "l33t" Leather Jacket vào giỏ hàng nhanh hơn sso với checkout và mình đã thanh toán thành công Lightweight "l33t" Leather Jacket chỉ với 10 $ của gift card

![image](https://hackmd.io/_uploads/Syp20H8FC.png)

## 4. Lab: Single-endpoint race conditions

link: https://portswigger.net/web-security/race-conditions/lab-race-conditions-single-endpoint

### Đề bài

![image](https://hackmd.io/_uploads/Bk2t2PUFR.png)

### Phân tích

Tính năng thay đổi email của phòng thí nghiệm này chứa một điều kiện chạy đua cho phép bạn liên kết một địa chỉ email tùy ý với tài khoản của mình.

Người có địa chỉ này carlos@ginandjuice.shopcó lời mời đang chờ để trở thành quản trị viên cho trang web, nhưng họ vẫn chưa tạo tài khoản. Do đó, bất kỳ người dùng nào xác nhận thành công địa chỉ này sẽ tự động được thừa hưởng quyền quản trị viên.

chúng ta cần

1. Xác định tình trạng chạy đua cho phép bạn yêu cầu một địa chỉ email tùy ý.
2. Đổi địa chỉ email của bạn thành carlos@ginandjuice.shop.
3. Truy cập bảng quản trị.
4. Xóa người dùngcarlos

vậy chúng ta đang có 1 email và cần liết kết nó với tài khoản của attacker vì victim chưa liên kết nó với tài khoản của mình

![image](https://hackmd.io/_uploads/r19gX_LFA.png)

### Khai thác

- mình tạo 1 group 2 requesst trong đó có đổi email thành carlos@ginandjuice.shop

![image](https://hackmd.io/_uploads/H1kQm_LYR.png)

- xác nhận tronng email và đã nhận được thông báo update thành công

![image](https://hackmd.io/_uploads/rk-a7O8K0.png)

![image](https://hackmd.io/_uploads/rko0bOLFR.png)

![image](https://hackmd.io/_uploads/S1bgGdUYR.png)

## 5. Lab: Exploiting time-sensitive vulnerabilities

Link: https://portswigger.net/web-security/race-conditions/lab-race-conditions-exploiting-time-sensitive-vulnerabilities

### Đề bài

![image](https://hackmd.io/_uploads/HygwEOItA.png)

### Phân tích

### Khai thác

![image](https://hackmd.io/_uploads/SJVmetUtA.png)

![image](https://hackmd.io/_uploads/B1cmgtLYA.png)

![image](https://hackmd.io/_uploads/SJkNgFIYA.png)

![image](https://hackmd.io/_uploads/HJfq1KIYA.png)

![image](https://hackmd.io/_uploads/ByEjJFIFC.png)

![image](https://hackmd.io/_uploads/Hk6qyFLYR.png)

![image](https://hackmd.io/_uploads/HkPcytLtA.png)

## 6. Lab: Partial construction race conditions

Link: https://portswigger.net/web-security/race-conditions/lab-race-conditions-partial-construction

### Đề bài

![image](https://hackmd.io/_uploads/r11ieF8tA.png)

### Phân tích

### Khai thác
