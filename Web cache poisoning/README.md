# Web cache poisoning

## Khái niệm & Khai thác & Phòng tránh

### Khái niệm

- Việc caching được áp dụng rộng khắp ở mọi mặt trận trong ngành IT, ngay chiếc smartphone hay PC bạn đang dùng, việc Caching cũng diễn ra liên tục. Mục đích là tốc độ xử lý các tác vụ được nhanh hơn nhờ vào việc nó được lưu vào một vùng nhớ đệm, để mỗi khi tác vụ được request đến, nó response trực tiếp từ đây.

![image](https://hackmd.io/_uploads/HkRYF7n66.png)

![image](https://hackmd.io/_uploads/SkMfeqh6p.png)

- Ở đây các bạn có thể nhìn thấy 4 layer chính khi nói tới 1 application phổ biến là: Client side, proxy, application và database. Tại mỗi layer này thì đều có những hệ thống cache tương ứng và chúng ta có thể có các mức độ kiểm soát khác nhau.

![image](https://hackmd.io/_uploads/ryLdcKhp6.png)

- Loại bộ đệm

  - **Bộ nhớ đệm của trình duyệt** (bộ nhớ đệm riêng tư trên thiết bị của người dùng.) ![image](https://hackmd.io/_uploads/Hk-emjn66.png)
  - **Bộ đệm máy chủ proxy** ( được duy trì bởi ISP hoặc nhà cung cấp Mạng phân phối nội dung (CDN)) ![image](https://hackmd.io/_uploads/B1tVQsnT6.png) ![image](https://hackmd.io/_uploads/By-cms3pp.png)

- **Web caching**: Bên cạnh các phương pháp cải thiện băng thông, đường truyền, để giảm thiểu về thời gian tải trang, các nhà phát triển hướng đến ý tưởng lưu trữ bản sao của các trang web trên máy tính của người dùng hoặc trên các máy chủ CDN (Content Delivery Network)

![image](https://hackmd.io/_uploads/r1MiEm2ap.png)

- Web caching lưu trữ bản sao của các tài nguyên trên trang web, chúng thường bao gồm hình ảnh, tệp CSS và JavaScript trên máy chủ quản lý cache CDN (Content Delivery Network) hoặc trên các máy tính của người dùng. Khi người dùng truy cập trang web lần đầu tiên, trình duyệt sẽ tải toàn bộ tài nguyên từ máy chủ gốc, lần tiếp theo người dùng truy cập lại trang web, các tài nguyên đã được lưu trữ trước đó sẽ được sử dụng thay vì tải lại toàn bộ. Điều này làm cho trang web được tải nhanh hơn và cải thiện trải nghiệm người dùng.

![image](https://hackmd.io/_uploads/HJqeM92a6.png)

- **Cache keys và Unkeyed inputs**

      - Khi người dùng gửi request tới server, server cần quyết định response trả về cho họ sẽ được lấy từ CDN hay sẽ xử lý qua hệ thống backend rồi trả về nội dung từ server gốc. Nếu thực hiện kiểm tra, so sánh từng ký tự trong request sẽ rất tốn kém do các request thường chứa nhiều thông tin và số lượng request cũng vô cùng lớn. Bởi vậy, cần có các yếu tố giúp server xác nhận điều đó, chúng được gọi là các cache keys. Nếu mà so sánh từng byte 1 thì hoàn toàn không hiệu quả, do đó sinh ra 1 khái niệm gọi là “Cache keys” – là một số thành phần cụ thể của HTTP request dùng để xác định resource đang được yêu cầu.

      - Quá trình xác nhận được thực hiện đơn giản như sau: Server so sánh các giá trị cache keys trong request gửi đến có trùng khớp với tập giá trị cache keys được quy định từ trước, nếu giống nhau sẽ trả về kết quả từ CDN, ngược lại có nghĩa request nhận được là "mới", cần thực hiện xử lý qua backend và trả về kết quả từ server gốc.
      - Ví dụ:
      - ![image](https://hackmd.io/_uploads/BJ6qs52aa.png)
      - cache keys ở đây là phần bôi cam cam ở trên, nếu request nào match 2 cái đó thì resource cache sẽ được trả về, như vậy nếu ta request:
      - ![image](https://hackmd.io/_uploads/BkWCjc3Tp.png)

      - Thì content trả về vẫn là english, vì cache key vẫn đúng, và… poisoned >_<, Lưu ý là cache keys tuỳ thuộc từng trường hợp, không cố định (hoặc có thể được xác định bằng trường Vary)





      - Các thành phần còn lại trong request không phải cache keys sẽ được gọi là các giá trị unkeyed.

  ![image](https://hackmd.io/_uploads/H1umi53aa.png)

- **Web cache poisoning vulnerability**: Dựa vào phương thức hoạt động đặc biệt của web caching, những kẻ tấn công đã lựa chọn các tài nguyên được lưu trữ tạm thời trong máy chủ caching CDN làm mục tiêu. Sau khi nắm được quy trình caching của trang web, họ thực hiện đầu độc (poisoning) bộ nhớ đệm (cache), khiến server lưu trữ các tài nguyên chứa payload tấn công vào bộ nhớ cache, khi người dùng truy cập vào trang web, chính server sẽ "giúp" kẻ tấn công trả về các phản hồi nguy hiểm tới người dùng. Trong hình thức tấn công Web cache poisoning, kẻ tấn công đóng vai trò một thợ săn đặt sẵn các bẫy (các tài nguyên cache nguy hiểm), đợi chờ những con mồi "cắn câu" (truy cập trang web và nhận được phản hồi cache nguy hiểm).
- Mục tiêu của việc này là gửi một request có thể tạo ra một response có hại, nó được lưu lại tại vùng Cache và được sử dụng để phục vụ tiếp cho những user (victim) phía sau:

![image](https://hackmd.io/_uploads/SkdKS72aT.png)

### Khai thác

- Dấu hiệu caching:

  - Chúng ta có thể nhận biết một trang web thực hiện caching tài nguyên hay không thông qua một số header trong response như X-Cache, Age, Cache-Control.
  - Cache-Control`với từ khóa`max-age```
  - `X-cache` với từ khóa `miss` hoặc `hit`
    - Header X-Cache với giá trị hit nghĩa là nội dung response hiện tại nhận được đến từ máy chủ CDN.
    - Khi giá trị Age đạt tối đa thời gian lưu trữ được quy định trong max-age, máy chủ CDN sẽ lưu trữ một phiên tài nguyên mới. Khi đó header X-cache cũng được chuyển sang giá trị miss, cho thấy nội dung response nhận được đang tới từ máy chủ gốc.

- Bây giờ hãy tìm hiểu kĩ hơn về kĩ thuật tấn công Cache Poisoning.

Mục tiêu của tấn công này là hacker phải gửi một request tới server mà response của nó trở nên độc hại, đồng thời phải làm cho response này lưu được trên cache để nó được gửi đến nhiều người khác. Có một vài cách để làm cho response sau khi gửi request trở nên độc hại như là : ghi chèn vào HTTP headers, phương pháp HTTP Response Splitting, HTTP Request Smuggling.

- poison shared cache: Qua 3 bước:
  1. Tìm những chỗ input không phải cache key
  2. Xem những chỗ input đó có thành lỗi được không
  3. Nếu có thì bắt đầu poison shared cache
- Sơ đồ sau cho ta cái nhìn tổng quan hơn:
  ![image](https://hackmd.io/_uploads/HJgmlon66.png)

Ví dụ: sử dụng Param Miner tìm ra được unkeyed input `X-Forwarded-Host`

![image](https://hackmd.io/_uploads/SkpCejnpp.png)

Và tấn công, nếu ressponse được lưu trên cache thành công, thì ai truy cập vào `www.redhat.com/en?cb=1` cũng sẽ bị alert(1).

![image](https://hackmd.io/_uploads/SJWzbi2pa.png)

### Phòng tránh

- Cách dứt khoát để ngăn chặn việc đầu độc bộ nhớ đệm web rõ ràng là vô hiệu hóa hoàn toàn bộ nhớ đệm. Mặc dù đối với nhiều trang web, đây có thể không phải là một lựa chọn thực tế nhưng trong những trường hợp khác, nó có thể khả thi
- Vá các lỗ hổng phía máy khách ngay cả khi chúng có vẻ không thể khai thác được. Một số lỗ hổng này thực sự có thể bị khai thác do những điều kỳ lạ không thể đoán trước trong hoạt động của bộ nhớ đệm
- Sử dụng chuẩn HTTP và hạn chế sử dụng phần body cho GET request.
- Sử dụng một số công cụ chặn thư rác (spam) như CAPTCHA hoặc Google reCAPTCHA để giảm thiểu các request tấn công từ bot.
- Ngoài ra, có thể sử dụng các giải pháp bảo mật như Web Application Firewall (WAF) để chặn các request độc hại. Với WAF, có thể tùy chỉnh các quy tắc để chặn các request không hợp lệ hoặc có chứa các chuỗi độc hại.

## 1. Lab: Web cache poisoning with an unkeyed header

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header

### Đề bài

![image](https://hackmd.io/_uploads/r1VOLV6Ta.png)

### Phân tích

- Lab này dễ bị nhiễm độc bộ đệm web vì nó xử lý đầu vào từ tiêu đề không có khóa theo cách không an toàn. Một người dùng không nghi ngờ thường xuyên truy cập trang chủ của trang web. Để giải quyết bài thí nghiệm này, hãy đầu độc bộ nhớ đệm bằng một phản hồi thực thi alert(document.cookie)trong trình duyệt của khách truy cập.

- Quan sát response, chú ý rằng ứng dụng có thể tồn tại lỗ hổng web cache poisoning do tồn tại cơ chế caching:

![image](https://hackmd.io/_uploads/rkY5wNaaa.png)

Click chuột phải trong request, chọn đến extension Param Miner, sử dụng lựa chọn Guess everything!

![image](https://hackmd.io/_uploads/SkpJONTT6.png)

extension Param Miner phát hiện trường `X-Forwarded-Host` có chèn và chứa unkeyed

![image](https://hackmd.io/_uploads/HkxkcV6p6.png)

![image](https://hackmd.io/_uploads/rkMN5VTap.png)

### Khai thác

- Thay đổi một giá trị khác cho header `X-Forwarded-Host`, response không đổi. Chứng tỏ header này không phải một cache key, hay nói cách khác nó là một giá trị unkeyed. Đồng thời được lưu trữ trong tài nguyên cache với thời gian 30 giây.

![image](https://hackmd.io/_uploads/SyBcs4TTa.png)

Ngoài ra value của header X-Forwarded-Host được thêm vào src của tag script.

- Dựa vào đó, gửi request với X-Forwarded-Host có giá trị như sau:

```javascript!
cuong.com"></script><script>alert(document.cookie);</script>
```

![image](https://hackmd.io/_uploads/S1FV2Naa6.png)

Khi victim truy cập trang chủ cũng sẽ bị alert do nhận response từ cache. Ta solve thành công challenge.

![image](https://hackmd.io/_uploads/Bka6DHT6T.png)

![image](https://hackmd.io/_uploads/HJ-wnETT6.png)

### Burp scan

- mình đã quét lại lab với burp scan

![image](https://hackmd.io/_uploads/SkSvu4pTT.png)

burp scan đã thêp 3 http header

```http!
X-Forwarded-Host: p3tby47uvcp30xhw3z93leyoifo8cy0r1fr2hq6.oastify.com X-Host: p3tby47uvcp30xhw3z93leyoifo8cy0r1fr2hq6.oastify.com X-Forwarded-Server: p3tby47uvcp30xhw3z93leyoifo8cy0r1fr2hq6.oastify.com
```

và vẫn nhận cùng 1 response nên cho rằng nó đã cache

![image](https://hackmd.io/_uploads/B1Av_ETpp.png)

và burp phát hiện thông tin đưa vào 3 header trên được trả về trong html của response

![image](https://hackmd.io/_uploads/SkmAd4a6a.png)

và khi đóng giả nạn nhân truy cập vào với request thứ 2 burp thấy response trả về từ cache server với payload đã được chèn vào từ request 1

![image](https://hackmd.io/_uploads/ByyYuNT6p.png)

![image](https://hackmd.io/_uploads/B1nt_4ppa.png)

với lỗi tìm thứ 2 burp thấy trong trường Host

![image](https://hackmd.io/_uploads/HygsdN6TT.png)

Burp chèn thêm port vào phần domain trên http header Host thì thấy được trả về trong response

![image](https://hackmd.io/_uploads/BJKiOEpTp.png)

![image](https://hackmd.io/_uploads/HkhyFNpaT.png)

và với request thứ 2 đóng giả victim khi truy cập vào trang web sẽ được trả response từ cache

![image](https://hackmd.io/_uploads/HJIetVap6.png)

![image](https://hackmd.io/_uploads/SkqgKN6Tp.png)

và chúng ta có thể tận dụng để chèn payload vào 2 unkeyed mà burp đã tìm ra

## 2. Lab: Web cache poisoning with an unkeyed cookie

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-cookie

### Đề bài

![image](https://hackmd.io/_uploads/Bye5OBTTT.png)

### Phân tích

- Phòng thí nghiệm này dễ bị nhiễm độc bộ đệm web vì cookie không có trong khóa bộ đệm. Một người dùng không nghi ngờ thường xuyên truy cập trang chủ của trang web. Để giải quyết bài thí nghiệm này, mình đầu độc bộ nhớ đệm bằng một phản hồi thực thi alert(1)trong trình duyệt của khách truy cập.

![image](https://hackmd.io/_uploads/BJ-atrpaT.png)

Ứng dụng này không include cookie vào cache keys. Trong đó có cookie fehost được chèn trực tiếp giá trị vào script.

Thực hiện gửi request với cookie fehost=cuong ta thấy chuỗi cuong đã được thêm vào script.

![image](https://hackmd.io/_uploads/Hki1orapT.png)

### Khai thác

- gửi request với `fehost=abc"-alert(1)-"abc` để inject XSS.

![image](https://hackmd.io/_uploads/HJCsjB6aa.png)

Khi victim truy cập trang chủ cũng sẽ bị alert do nhận response từ cache. Ta solve thành công challenge.

![image](https://hackmd.io/_uploads/B1fynHT6p.png)

Ta solve thành công challenge.

![image](https://hackmd.io/_uploads/B1ansHaTT.png)

## 3. Lab: Web cache poisoning with multiple headers

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-multiple-headers

### Đề bài

![image](https://hackmd.io/_uploads/rJB22ST6a.png)

### Phân tích

- Phòng thí nghiệm này chứa một lỗ hổng đầu độc bộ đệm web chỉ có thể khai thác được khi bạn sử dụng nhiều tiêu đề để tạo một yêu cầu độc hại. Một người dùng truy cập trang chủ khoảng một lần một phút. Để giải quyết bài thí nghiệm này, hãy đầu độc bộ nhớ đệm bằng một phản hồi thực thi alert(document.cookie)trong trình duyệt của khách truy cập.

Sử dụng Param Miner ta thấy cache unkey header X-Forwared-Scheme.

![image](https://hackmd.io/_uploads/r1kc6rT6T.png)

extension đã thử chèn vào url `/h70mqmag5.jpg` và thêm trường `Xyzx-Forwarded-Schemez: zwrtxqvaxpucs7y8wn`

![image](https://hackmd.io/_uploads/SJg3TBpa6.png)

và thấy trong response chuyển hướng đến /h70mqmag5.jpg

![image](https://hackmd.io/_uploads/Hko36rp6p.png)

web vẫn trả về response như thường

![image](https://hackmd.io/_uploads/HyY1CH6p6.png)

Sử dụng cache buster ?abcd=1 và test thử với `X-Forwared-Scheme: https` thì thấy vẫn nhận response bình thường.

![image](https://hackmd.io/_uploads/B17zx8aT6.png)

Tuy nhiên khi gửi X-Forwared-Scheme khác https thì sẽ được trả về 302 và redirect về https.

Tận dụng thêm 1 unkeyed header X-Forwarded-Host kết hợp với X-Forwared-Scheme khác https, ta có thể redirect user về đường dẫn `https://<X-Forwarded-Host>/?abc=1`.

### Khai thác

![image](https://hackmd.io/_uploads/rkN1mI6aa.png)

## 4. Lab: Targeted web cache poisoning using an unknown header

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-targeted-using-an-unknown-header

### Đề bài

![image](https://hackmd.io/_uploads/B1JGNL6TT.png)

### Phân tích

- Phòng thí nghiệm này dễ bị nhiễm độc bộ đệm web. Người dùng nạn nhân sẽ xem bất kỳ bình luận nào bạn đăng. Để giải quyết bài thí nghiệm này, mình cần đầu độc bộ đệm bằng một phản hồi thực thi alert(document.cookie)trong trình duyệt của khách truy cập. Tuy nhiên, bạn cũng cần đảm bảo rằng phản hồi được cung cấp cho tập hợp con người dùng cụ thể mà nạn nhân dự định thuộc về.

### Khai thác

- Param Miner chỉ ra cache của ứng dụng ignore X-Host header.

![image](https://hackmd.io/_uploads/Hybo4uA66.png)

![image](https://hackmd.io/_uploads/SybMHuAT6.png)

![image](https://hackmd.io/_uploads/rkymB_RTp.png)

- Như vậy ta đã xác định được unkeyed header và ta có thể chèn XSS payload ở đó.

![image](https://hackmd.io/_uploads/HkjvOOC6T.png)

- Lưu ý rằng Varytiêu đề được sử dụng để chỉ định rằng đó User-Agentlà một phần của khóa bộ đệm. Để nhắm mục tiêu vào nạn nhân, bạn cần tìm hiểu tên miền User-Agent.

Ta thấy các bài post có chức năng comment với comment có thể là HTML code.

![image](https://hackmd.io/_uploads/BkXbtdAaa.png)

- Bây giờ ta chỉ cần chèn payload sau để khi victim xem comment thì sẽ request đến exploit-server: `<img src="https://<EXPLOIT-SERVER>">`.

![image](https://hackmd.io/_uploads/ByXUYuC6p.png)

Lấy `User-Agent` đó kèm theo `X-Host` là XSS payload, ta đã có thể poison cache thành công với victim đã xác định.

![image](https://hackmd.io/_uploads/By5Y9OAp6.png)

khai thác như vậy không thành công vậy mình sẽ dùng domain của server lab cung cấp

- tạo nội dung cho file `/resources/js/tracking.js`

![image](https://hackmd.io/_uploads/r1Y9suCp6.png)

![image](https://hackmd.io/_uploads/ByBjhORp6.png)

thấy file js đã chứa script

![image](https://hackmd.io/_uploads/r1LanuR6a.png)

thay đổi user-agent thành của victim và gửi

![image](https://hackmd.io/_uploads/Sk-aTOR66.png)

khi user truy cập trang web đoạn mã js trong file `/resources/js/tracking.js` sẽ được kích hoạt và chúng ta solve được lab này

![image](https://hackmd.io/_uploads/B1LIkYApT.png)

### Burp scan

- mình đã quét lại lab với burp scan

![image](https://hackmd.io/_uploads/rkWoLOAaa.png)

![image](https://hackmd.io/_uploads/BylR8_Cpa.png)

![image](https://hackmd.io/_uploads/Bkw0Id0ap.png)

## 5. Web cache poisoning via an unkeyed query string

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-unkeyed-query

### Đề bài

![image](https://hackmd.io/_uploads/rJAjetApa.png)

### Phân tích

- Lab này dễ bị nhiễm độc bộ đệm web vì chuỗi truy vấn không được khóa. Người dùng thường xuyên truy cập trang chủ của trang web này bằng Chrome.

- Để giải quyết vấn đề, mình cần đầu độc trang chủ bằng một phản hồi thực thi `alert(1)`trong trình duyệt của nạn nhân.

![image](https://hackmd.io/_uploads/rkZDVYCpp.png)

![image](https://hackmd.io/_uploads/ByaDNF06p.png)

![image](https://hackmd.io/_uploads/Byau4FRpa.png)

![image](https://hackmd.io/_uploads/HkLFNtRpa.png)

![image](https://hackmd.io/_uploads/H1nt4tRa6.png)

mình dùng burp scan thấy

- Gửi request đến / với query string `pu94x064vu=1` thì thấy cả URL chứa query string được gán vào href của link canonical → có thể XSS. Ngoài ra, khi ta thay đổi query string thì X-Cache: hit chứng tỏ query string không thuộc cache keys.

### Khai thác

gửi request với param `cuong='/><script>alert(1)</script>`

![image](https://hackmd.io/_uploads/B1V1Lt0Tp.png)

và mình trigger thành công

![image](https://hackmd.io/_uploads/BygpSKA6a.png)

![image](https://hackmd.io/_uploads/r1iyItRaa.png)

## 6. Lab: Web cache poisoning via an unkeyed query parameter

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-unkeyed-param

### Đề bài

![image](https://hackmd.io/_uploads/SkQ_LFR6T.png)

### Phân tích

- Lab này dễ bị nhiễm độc bộ đệm web vì nó loại trừ một tham số nhất định khỏi khóa bộ đệm. Người dùng thường xuyên truy cập trang chủ của trang web này bằng Chrome.

- Để giải quyết vấn đề, hãy đầu độc bộ đệm bằng một phản hồi thực thi alert(1)trong trình duyệt của nạn nhân.

- mình dùng burp scan

![image](https://hackmd.io/_uploads/H18IDYA6T.png)

![image](https://hackmd.io/_uploads/ByePwt0Ta.png)

![image](https://hackmd.io/_uploads/SkauDtATT.png)

### Khai thác

- Tương tự bài trên, thử gửi request với `utm_content='/><script>alert(1)</script>` cho đến khi X-Cache:hit. Để ý ta có thể XSS tại canonical link.

![image](https://hackmd.io/_uploads/r1HTuK06p.png)

và mình solve được lab này

![image](https://hackmd.io/_uploads/r1LnuFRaa.png)

## 7. Lab: Parameter cloaking

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-param-cloaking

### Đề bài

![image](https://hackmd.io/_uploads/ry_4KFR6a.png)

### Phân tích

- Lab này dễ bị nhiễm độc bộ đệm web vì nó loại trừ một tham số nhất định khỏi khóa bộ đệm. Ngoài ra còn có sự phân tích tham số không nhất quán giữa bộ đệm và back-end. Người dùng thường xuyên truy cập trang chủ của trang web này bằng Chrome.

- Để giải quyết bài lab, mình cần sử dụng kỹ thuật che giấu tham số để đầu độc bộ đệm bằng phản hồi thực thi alert(1)trong trình duyệt của nạn nhân.
- mình dùng burp scan

![image](https://hackmd.io/_uploads/Hyw0FF0pT.png)

![image](https://hackmd.io/_uploads/Hkyk9Y0pT.png)

![image](https://hackmd.io/_uploads/rJF15K0T6.png)

- Mỗi khi load trang chủ thì một hàm setCountryCookie() được thực thi từ file /js/geolocate.js bằng tham số callback.

![image](https://hackmd.io/_uploads/BkChqFRTT.png)

### Khai thác

- ta thấy UTM params bị unkeyed bởi cache.
- Sử dụng kĩ thuật parameter cloaking với tham số callback với requesst với params `?callback=setCountryCookie&utm_content=test;callback=alert(1)`

![image](https://hackmd.io/_uploads/HyX83t0aa.png)

- ta thấy alert(1) được gọi.
  và mình solve được lab này

![image](https://hackmd.io/_uploads/B1iGnFR6T.png)

## 8. Lab: Web cache poisoning via a fat GET request

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-fat-get

### Đề bài

![image](https://hackmd.io/_uploads/B11qaYATp.png)

### Phân tích

- Phòng thí nghiệm này dễ bị nhiễm độc bộ đệm web. Nó chấp nhận GETcác yêu cầu có phần thân nhưng không bao gồm phần thân trong khóa bộ đệm. Người dùng thường xuyên truy cập trang chủ của trang web này bằng Chrome.

- Để giải quyết vấn đề, mình cần đầu độc bộ đệm bằng một phản hồi thực thi alert(1)trong trình duyệt của nạn nhân.

- mình dùng burp scan

![image](https://hackmd.io/_uploads/ry4MX9ATT.png)

![image](https://hackmd.io/_uploads/r1vQmqAaT.png)

![image](https://hackmd.io/_uploads/S1WVXcRpp.png)

### Khai thác

và mình thêm parameter trong requset body `callback=alert(1)&_method=POST`

![image](https://hackmd.io/_uploads/H1gxN90T6.png)

trgger thành công và mình solve được challenge

![image](https://hackmd.io/_uploads/BJxp79Ap6.png)

![image](https://hackmd.io/_uploads/BkykEqApp.png)

## 9. Lab: URL normalization

link: https://portswigger.net/web-security/web-cache-poisoning/exploiting-implementation-flaws/lab-web-cache-poisoning-normalization

### Đề bài

![image](https://hackmd.io/_uploads/ryPnV5Aaa.png)

### Phân tích

- Phòng thí nghiệm này chứa lỗ hổng XSS không thể khai thác trực tiếp do mã hóa URL của trình duyệt.

- Để giải quyết bài lab, mình tận dụng quá trình chuẩn hóa của bộ đệm để khai thác lỗ hổng này. Tìm lỗ hổng XSS và chèn một tải trọng sẽ thực thi alert(1)trong trình duyệt của nạn nhân. Sau đó, gửi URL độc hại cho nạn nhân.

- Khi truy cập 1 đường dẫn không tồn tại, trang web reflect lại đường dẫn đó ra output → nhìn có vẻ reflected XSS.

![image](https://hackmd.io/_uploads/HkPU8q0pT.png)

- Escape tag `<p>` và thêm XSS payload vào đường dẫn như hình dưới, ta thấy alert(1) đã được thực thi.

![image](https://hackmd.io/_uploads/Sk_28cA6p.png)

hiển thị response trên browser

![image](https://hackmd.io/_uploads/r1yfvq06p.png)

![image](https://hackmd.io/_uploads/HySCLcRaT.png)

Tuy nhiên có 1 điều, khi mình truy cập đường dẫn này trên URL thì bị fail do browser đã url-encode payload trên rồi mới gửi server. Do đó, mình cần kết hợp lỗi của cache trong việc nomarlize URL để có thể khiến nạn nhân truy cập đường dẫn trên URL mà vẫn bị dính XSS.

![image](https://hackmd.io/_uploads/rk6LPc0Ta.png)

### Khai thác

- Cách làm như sau:

Gửi lại request tấn công giống lúc nãy cho đến khi X-Cache:hit, tức là response đã được cached chứa unencoded XSS payload.

Lập tức truy cập lại đường dẫn trên URL, ta XSS thành công.

![image](https://hackmd.io/_uploads/SJs5vqRT6.png)

Giải thích:

- Khi attacker gửi XSS payload qua Repeater thì không bị URL-encoded bởi proxy → server xử lí bình thường và lưu vào cache.

- Khi nạn nhân truy cập malicious URL trên browser, browser sẽ URL-encode nó, nhưng khi qua bước URL normalization của cache, cache hiểu là cùng cache keys → trả về response giống như response chứa unencoded payload của attacker → bị XSS.

submit gửi co victim và mình solve được lab

![image](https://hackmd.io/_uploads/S1BUKqATa.png)

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">

## Tham khảo

- https://viblo.asia/p/web-cache-poisoning-reborn-by-james-kettle-yMnKMMXEK7P
- https://www.youtube.com/watch?v=iSDoUGjfW3Q
- https://viblo.asia/p/caching-dai-phap-1-nac-thang-len-level-cua-developer-V3m5WdO8KO7
- https://cystack.net/research/web-cache-poisoning
- https://viblo.asia/p/web-cache-poisoning-lo-hong-dau-doc-bo-nho-cache-phan-2-EvbLb5koJnk
