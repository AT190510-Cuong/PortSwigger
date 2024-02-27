# Client-side template injection (CSTI)

### Khái niệm & Khai thác & Phòng tránh

- Các framework phía máy khách hiện đại như Vue, React hoặc Angular cho phép sử dụng các Template để in giá trị của các biến hoặc đánh giá biểu thức
- Client-side template injection vulnerabilities phát sinh khi các ứng dụng sử dụng Template phía máy khách tự động nhúng dữ liệu nhập của người dùng vào trang web. Khi một trang web được hiển thị, khung sẽ quét trang để tìm các biểu thức mẫu và thực thi bất kỳ biểu thức nào nó gặp phải. Kẻ tấn công có thể khai thác điều này bằng cách cung cấp một biểu thức mẫu độc hại để khởi động một cuộc tấn công tập lệnh cross-site scripting (XSS). Giống như cross-site scripting thông thường, mã do kẻ tấn công cung cấp có thể thực hiện nhiều hành động khác nhau, chẳng hạn như đánh cắp mã thông báo phiên hoặc thông tin xác thực đăng nhập của nạn nhân, thực hiện các hành động tùy ý thay mặt nạn nhân và ghi lại các lần gõ phím của họ.

- khác nhau giữa SSTI và CSTI:

  - SSTI cho phép thực thi mã trên máy chủ từ xa, trong khi CSTI cho phép thực thi mã JavaScript tùy ý ở phía nạn nhân.

- **𝗦𝗲𝗿𝘃𝗲𝗿-𝘀𝗶𝗱𝗲 𝘁𝗲𝗺𝗽𝗹𝗮𝘁𝗲 𝗶𝗻𝗷𝗲𝗰𝘁𝗶𝗼𝗻** đề cập đến một lỗ hổng hoặc vấn đề bảo mật có thể xảy ra trên web các ứng dụng sử dụng công cụ tạo khuôn mẫu phía máy chủ. Nó liên quan đến một cuộc tấn công tiêm mã trong đó kẻ tấn công có thể tiêm và thực thi mã độc trong mẫu phía máy chủ.
  VD:

```!
template = “Your comment is: {{ comment }}”
rendered = template.render(comment=comment_input)
```

Nếu bạn gửi `{{7*7}}` làm nhận xét, kết quả sẽ là:
kết quả là `Your comment is: 49`

Lỗ hổng này có thể dẫn đến việc thực thi mã, như được minh họa bằng payload sau:

```!
{{ user .__class__ .__mro__ [1] .__subclasses__ () [407] (“cat /etc/passwd”, shell=True, stdout=- 1 ) .communicate () }}
```

Tải trọng cố gắng thực thi lệnh cat /etc/passwd trên máy chủ. Nếu môi trường máy chủ cho phép thực thi lệnh như vậy và công cụ tạo mẫu dễ bị SSTI tấn công thì nội dung của tệp /etc/passwd có thể được hiển thị dưới dạng kết quả của tải trọng.

- **𝗖𝗹𝗶𝗲𝗻𝘁 𝗦𝗶𝗱𝗲 𝗧𝗲𝗺𝗽𝗹𝗮𝘁𝗲 𝗜𝗻𝗷𝗲𝗰𝘁𝗶𝗼𝗻** là một vấn đề bảo mật trong đó đầu vào của kẻ tấn công được đưa vào vào một trang và được xử lý bởi thư viện JavaScript phía máy khách.

VD:

```htmlembedded!
<h1>Hello, {{name}}</h1>
```

test lỗ hổng như SSTI với payload `{{7*7}}` cho kết quả

`Hello, 49.`

Trước khi cố gắng thực thi mã, hãy kiểm tra xem biến này có được thư viện JS trong trình duyệt của bạn xử lý hay không.

```!
{{constructor.constructor(‘alert(1)’)()}}
```

các biểu thức Angular được đánh giá dựa trên đối tượng Phạm vi. Về cơ bản, điều này có nghĩa là nếu bạn cố gắng đánh giá “alert(1)” thì nó sẽ thất bại vì phạm vi không có chức năng “alert” (trừ khi bạn xác định một chức năng). Phạm vi chỉ là một đối tượng và bạn có thể định nghĩa các biến và hàm trong đó

- Lỗ hổng này chủ yếu được sử dụng để kích hoạt payload XSS và thường có thể bỏ qua các biện pháp ngăn chặn XSS truyền thống như mã hóa dữ liệu đầu vào của người dùng

### Khai thác

- Người dùng có thể bị xúi giục đưa ra yêu cầu do kẻ tấn công tạo ra theo nhiều cách khác nhau. Ví dụ: kẻ tấn công có thể gửi cho nạn nhân một liên kết chứa URL độc hại trong email hoặc tin nhắn tức thời. Họ có thể gửi liên kết tới các trang web phổ biến cho phép biên soạn nội dung, chẳng hạn như trong các bình luận trên blog. Và họ có thể tạo một trang web trông vô hại khiến bất kỳ ai xem nó đều thực hiện các yêu cầu tên miền chéo tùy ý tới ứng dụng dễ bị tấn công (sử dụng phương thức GET hoặc POST).

- Tác động bảo mật của các lỗ hổng chèn mẫu phía máy khách phụ thuộc vào bản chất của ứng dụng dễ bị tấn công, loại dữ liệu và chức năng chứa trong đó cũng như các ứng dụng khác thuộc cùng một miền và tổ chức. Nếu ứng dụng chỉ được sử dụng để hiển thị nội dung công khai không nhạy cảm, không có chức năng xác thực hoặc kiểm soát quyền truy cập thì lỗ hổng chèn mẫu phía máy khách có thể được coi là có rủi ro thấp. Tuy nhiên, nếu cùng một ứng dụng nằm trên một miền có thể truy cập cookie cho các ứng dụng quan trọng hơn về bảo mật thì lỗ hổng bảo mật có thể được sử dụng để tấn công các ứng dụng khác đó và do đó có thể được coi là có rủi ro cao. Tương tự, nếu tổ chức sở hữu ứng dụng có khả năng là mục tiêu của các cuộc tấn công lừa đảo thì lỗ hổng này có thể bị lợi dụng để tăng độ tin cậy cho các cuộc tấn công đó bằng cách đưa chức năng Trojan vào ứng dụng dễ bị tấn công và khai thác lòng tin của người dùng đối với tổ chức để chiếm đoạt. thông tin xác thực cho các ứng dụng khác mà nó sở hữu. Trong nhiều loại ứng dụng, chẳng hạn như những ứng dụng cung cấp chức năng ngân hàng trực tuyến, việc chèn mẫu phía khách hàng luôn được coi là có rủi ro cao.

- có thể tìm dấu hiệu bằng {{7*7}}
  VD:

```!
<center> <p style="font-size:2em;"> {{CSTI}} </p></center>
```

Vì Angular sử dụng trình phân tích cú pháp để đánh giá mọi biểu thức trong dấu ngoặc nhọn, loại bỏ các giá trị HTML (thông qua thuộc tính ng-bind-html, nếu rõ ràng) và sử dụng hộp cát để tránh mã JavaScript gọi các hàm bên ngoài đối tượng phạm vi Angular, nên chúng ta cần phải thực hiện các bước sau để khai thác thành công:

- thoát khỏi sanitizer
- thoát khỏi sandbox (Nó được cho là lọc các lệnh của người dùng và không thực thi các lệnh độc hại.)
- cuối cùng là chèn payload

nếu server encode đầu vào của chúng ta bằng `htmlspecialchars` như sau

```php!
<?php
    // GET parameter ?q= mit sicherem escaping
    $q = $_GET['q'];
    echo htmlspecialchars($q,ENT_QUOTES);
?>
```

![image](https://hackmd.io/_uploads/SyvTM3FnT.png)

sẽ chống được XSS vì encode các ký tự đặc biệt nhưng trong Angular, chúng ta có thể sử dụng các biểu thức không nhất thiết phải sử dụng các ký tự đặc biệt được mã hóa bởi hàm PHP “htmlspecialchars” như dưới đây:

![image](https://hackmd.io/_uploads/ryKzXht36.png)

Việc buộc một ứng dụng cộng hai số lại với nhau không phải là điều thú vị lắm, nhưng điều gì sẽ xảy ra nếu chúng ta có thể chèn mã javascript vào, nhưng không thể chỉ chèn một hàm “alert(1)” vì hàm đó không được xác định trong đối tượng phạm vi

- heo mặc định, đối tượng phạm vi chứa một đối tượng khác gọi là **“constructor”** chứa một hàm còn được gọi là **“ constructor ”**. Chức năng này có thể được sử dụng để tạo và thực thi mã động. Đây chính xác là những gì chúng ta cần để thực thi tải trọng XSS của mình như dưới đây:

```javascript!
{{constructor.constructor('alert(1)')()}}
```

- payload trên không chứa bất kỳ ký tự đặc biệt nào. Điều này có nghĩa là mọi nỗ lực mã hóa tải trọng của bằng hàm `htmlspecialchars` sẽ không ngăn được XSS

![image](https://hackmd.io/_uploads/SkOVB2Kha.png)

biểu thức Angular độc hại đã được đưa vào trang khiến ứng dụng tự động tạo và thực thi payload.

- Để giúp ngăn chặn kiểu tấn công này, Angular 1.2 – 1.5 chứa một hộp cát. Điều này sau đó đã bị xóa trong phiên bản 1.6 trở lên vì nó không cung cấp bảo mật thực sự vì có rất nhiều đường vòng sandbox. Nếu ứng dụng mà bạn đang thử nghiệm nằm giữa các phiên bản 1.2 – 1.5, bạn sẽ cần tra cứu đường vòng sandbox cho phiên bản đó để tải trọng XSS của bạn thực thi

các bạn có thể tìm hiểu sự khác nhau giữa cách tấn công CSTI với SSTI tại https://www.paloaltonetworks.com/blog/prisma-cloud/template-injection-vulnerabilities/

### Phòng tránh

Các khung mẫu phía máy khách thường triển khai hộp cát nhằm mục đích cản trở việc thực thi trực tiếp JavaScript tùy ý từ bên trong biểu thức mẫu. Tuy nhiên, những hộp cát này không nhằm mục đích kiểm soát bảo mật và thường có thể bị bỏ qua.

Các bộ lọc tập lệnh cross-site scripting của trình duyệt thường không thể phát hiện hoặc ngăn chặn các cuộc tấn công chèn mẫu phía máy khách.

- Nếu có thể, hãy tránh sử dụng mã phía máy chủ để tự động nhúng thông tin đầu vào của người dùng vào các mẫu phía máy khách. Nếu điều này không thực tế, hãy cân nhắc việc lọc cú pháp biểu thức mẫu khỏi dữ liệu đầu vào của người dùng trước khi nhúng nó vào các mẫu phía máy khách.

Lưu ý rằng mã hóa HTML không đủ để ngăn chặn các cuộc tấn công tiêm mẫu phía máy khách, vì các khung thực hiện giải mã HTML nội dung có liên quan trước khi định vị và thực thi các biểu thức mẫu.

## Tham khảo

- https://skf.gitbook.io/asvs-write-ups/client-side-template-injection-csti/client-side-template-injection
- https://www.paloaltonetworks.com/blog/prisma-cloud/template-injection-vulnerabilities/
- https://bergee.it/blog/xss-via-angular-template-injection/
- https://book.hacktricks.xyz/pentesting-web/client-side-template-injection-csti
