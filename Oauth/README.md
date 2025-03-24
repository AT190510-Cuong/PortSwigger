# OAuth

## Khái niệm && Phâ tích && phòng tránh

Vậy tại sao lại sử dụng cái này?

Ví dụ:

Bạn có hai ứng dụng, tạm gọi là app1 và app2. App1 chứa danh sách bạn bè của end-user, App2 có chức năng tự động gửi lời chúc sinh nhật. Bạn muốn App2 có thể tự động gửi lời chúc sinh nhật cho danh sách bạn bè của end-user ở App1, làm cách nào để App2 lấy được danh sách bạn bè ở App1?

End-user tự nhập lại danh sách bạn bè ở App1 vào App2. Nếu số lượng bạn bè lớn lên tới vài trăm người thì phải làm sao? Liệu end-user có bỏ app của bạn mà đi sang app khác không?
Bạn cho phép App2 export danh sách bạn bè, sau đó import vào App1. Nếu sau thời điểm import, số lượng bạn bè tăng lên thì end-user phải import lại? Nếu App2 không có chức năng export danh sách bạn bè, App1 không có chức năng import danh sách bạn bè thì sao? Liệu end-user có bỏ app của bạn mà đi?
App2 lưu lại username/password khi end-user đăng nhập và sử dụng nó để đăng nhập vào App1 mỗi khi cần cần truy cập tới danh sách bạn bè. Cách này chỉ hoạt động được khi end-user dùng chung username/password ở cả App1 và App2. Tuy nhiên:
Cách này sẽ không bảo mật. Ngoài ra mỗi lần end-user thay đổi mật khẩu ở App1 thì họ phải qua App2 để thay đổi mật khẩu cho đồng nhất.
Vì App2 có mật khẩu và tài khoản của App1 nên App2 có thể truy cập được nhiều thông tin hơn ngoài danh sách bạn bè. Giả sử có những thông tin trong App1 như hình ảnh nhạy cảm cũng bị App2 truy cập. Như vậy sẽ dẫn tới nhiều hệ lụy phiền toái sau này.
Ba cách này dường như không khả thi. Trên thực tế người ta sẽ giải quyết vấn đề này bằng cách để App2 lấy danh sách bạn bè từ App1 chỉ cần người end-user xác nhận cho phép App2 truy cập vào danh sách bạn bè của App1. Lúc đó App2 chỉ được phép lấy danh sách bạn bè, những thông tin khác hoàn toàn không có quyền truy cập. Nó cũng giống với việc khi bạn tạo file trong Draw.io và chọn vùng lưu trữ là google drive, popup yêu cầu xác nhận quyền truy cập vào google drive sẽ hiện lên. Đây là một ví dụ điển hình về OAuth 2.0

Lý do đơn giản là-> trang web của chúng ta sử dụng cách đăng nhập nhanh này trước tiên chắc chắn là thuận tiện, sau đó trang web của bên thứ 3 và trang web hiện tại không được tin tưởng lẫn nhau và không thể chuyển thông tin người dùng cho bên thứ 3 .

Vì vậy nhìn chung OAuth cho phép người dùng cấp quyền truy cập mà không để lộ thông tin xác thực đăng nhập của họ cho ứng dụng yêu cầu. Điều này có nghĩa là người dùng có thể chọn dữ liệu mà họ muốn chia sẻ mà không cần phải giao mật khẩu tài khoản của mình cho bên thứ 3.

### Khái niệm

- Theo đó, OAuth 2.0 là một cơ chế cho phép các dịch vụ bên thứ 3 có quyền truy cập tới một số tài nguyên nhất định của chủ sở hữu tài nguyên. Ban đầu OAuth 2.0 được thiết kế nhằm mục địch xác thực quyền truy cập tới một số tài nguyên nhất định của người dùng. Tuy nhiên, với sự tiện lợi của mình, các trang web dần nhận ra có thể sử dụng framework này đối với việc định danh người dùng dịch vụ thông qua các thông tin được xác thực bởi bên cung cấp dịch vụ OAuth

#### OAuth Roles

Theo định nghĩa của IETF, trong OAuth có tất cả 4 roles:

- `Resource owner`: là người dùng sở hữu tài nguyên, thường được hiểu là `end-user`.
- `Resource server`: là nơi mà các tài nguyên lưu trữ. Được truy cập và phản hồi lại thông qua các cơ chế xác thực như `access token`.
- `Client`: Là dịch vụ gửi yêu cầu truy cập tới tài nguyên đại diện cho `resource owner` và các xác thực của nó.
- `Authorization server`: Dịch vụ cung cấp access token cho `client` sau khi đã xác minh thành công người dùng và đạt được xác thực quyền truy cập vào tài nguyên.

Trên thực tế, authorization có thể nằm trên cùng một server với resource server hoặc không. Một `authorization server` có thể cung cấp access token cho nhiều `resource server`.

#### OAuth Grant Types

##### Authorization code grant type

- Trong kiểu grant type này, client sẽ trao đổi authorization code để lấy được access token. Quá trình này có thể được mô tả trong mô hình dưới đây:

![image](https://hackmd.io/_uploads/Hk3-Ocahye.png)

1. Client gửi một request tới server authentication:

```http!
GET /authorization?client_id=12345&redirect_uri=https://client-app.com/callback&response_type=code&scope=openid%20profile&state=ae13d489bd00e3c24 HTTP/1.1
Host: oauth-authorization-server.com
```

- `clientid`: 1 đoạn mã định danh duy nhất của client, được tạo khi client đăng kí với dịch vụ authorization
- `redirecturi`: là uri mà browser sử dụng để redirect tới sau khi nhận được authorization code. Thường gọi là callback URI
  responsetype: là kiểu trả về mà client muốn. Ở đây là code.
- `scope`: các nhóm dữ liệu, tài nguyên mà client muốn truy cập tới. Tùy theo từng dịch vụ OAuth mà có thể khác nhau.
- `state (optional)`: Là một giá trị duy nhất và không đoán được. Sẽ được gửi lại trong các response và request khác như callback request giống như 1 csrf token.

2. Người dùng đăng nhập và cho phép quyền truy cập

- Sau khi nhận được request khởi tạo trên, browser sẽ redirect người dùng tới 1 trang đăng nhập vào hệ thống cung cấp OAuth:
- Sau khi xác minh người dùng thành công, authorization server sẽ hỏi người dùng về có cung cấp các quyền cụ thể cho ứng dụng client hay không:
- Nếu người dùng đồng ý thì quá trình sẽ tiếp tục sang bước tiếp theo

3. Authorization server gửi authorization code tới cho client

- Sau khi có được sự đồng ý của người dùng cho phép truy cập các tài nguyên, authorization server sẽ gửi lại client 1 đoạn authorization code

4. Request access token

- Khi đã có được `authorization code`, client sẽ thực hiện request lấy `access token` từ authorization server. Request này sẽ được tạo trong một kênh riêng không đi qua browser. Client_secret cũng sẽ được truyền qua kênh này.

5. Client nhận access token

- Khi `authorization server` nhận được request của client, nó sẽ phản hồi lại 1 `access token` tương ứng với `authorization code` được gửi lên

6. Thực hiện API call

- Sau khi đã có được access token, giờ client có thể request tới tài nguyên cần thiết để lấy được tài nguyên.

7. Nhận dữ liệu cần thiết

- Lúc này `resource server` dựa vào `access token` của client mà trả về các dữ liệu tương ứng.

|            | Đặc điểm                                                                                                                                                                                                                                                                                                                                                                            |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ưu điểm    | Dựa theo mô hình của authorization code grant type, tất cả các dữ liệu quan trọng (ví dụ như access token) đều không đi qua browser mà thông qua một kênh riêng giữa client và authorization server. Điều này giúp tăng tính bảo mật trong quá trình xác thực OAuth. Ngoài ra, client secret cũng sử dụng kênh này để truyền và gửi nên có thể đảm bảo tính an toàn của secret này. |
| Nhược điểm | Nhược điểm duy nhất ở đây là việc triển khai có chút phức tạp hơn so với 1 số kiểu khác.                                                                                                                                                                                                                                                                                            |

#### Implicit grant type

- Implicit grant type đơn giản hơn khá nhiều so với authorization code grant type. Lí do là nó bỏ qua việc request authorization code mà trực tiếp request lấy access token từ phía authorization server. Mô hình của implicit grant type có thể hiểu đơn giản như sau:

![image](https://hackmd.io/_uploads/BkYqpcThJe.png)

|            | Đặc điểm                                                                                                                                                                                                                                                   |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ưu điểm    | Đơn giản, dễ triển khai                                                                                                                                                                                                                                    |
| Nhược điểm | Tất cả các request được gửi qua browser thay vì 1 kênh riêng giữa client và authorization server. Điều này dẫn tới việc các dữ liệu của người dùng và access token có thể bị tấn công, đánh cắp. Ngoài ra việc bảo vệ client secret cũng không hề dễ dàng. |

### Phân tích

### Phòng tránh

1. Xác minh người dùng

- Các thông tin xác thực người dùng PHẢI LUÔN LUÔN được bảo mật
- Khuyến khích sử dụng xác thực đa yếu tố
- KHÔNG ĐƯỢC lưu mật khẩu hay các thông tin định danh khác ở ứng dụng native hay user-agent-based với mục đích xác thực
- Hạn chế tối đa việc để lộ bất cứ thông tin định danh nào của người dùng (code, refresh token...)
- ...

2. Giả mạo người dùng

- Authorization server phải xác thực người dùng bất cứ khi nào có thể.
- Authorization server nên cho người dùng biết về ứng dụng client, scope và thời gian ủy quyền với client.
- Authorization server không nên tự động xử lí các yêu cầu ủy quyền lặp lại.
- ...

3. Access tokens

- Access token phải được và luôn được bảo mật trong lưu trữ và truyền tải
- Access token chỉ được phép truy cập bởi authorization server, resource server với access token hợp lệ và người dùng sở hữu access token.
  Access token phải được truyền tải trên giao thức TLS.
- Access token phải không được tạo mới, sửa hay đoán được giá trị
  Access token nên được ủy quyền ở mức tối thiểu
- ...

4. Refresh tokens

- Refresh token phải được và luôn được bảo mật trong lưu trữ và truyền tải
- Refresh token chỉ được phép truy cập bởi authorization server và người dùng sở hữu access token.
- Refresh token phải được truyền tải trên giao thức TLS.
- Authorization server phải đảm bảo refresh token tương ứng với định danh của người dùng khi người dùng đã xác thực
- Nếu người dùng không thể xác thực, authorization server phải có các cơ chế khác để đảm bảo refresh token khoong bị lợi dụng
- Refresh token phải không được tạo mới, sửa hay đoán được giá trị
- ...

5. Authorization codes

- Việc truyền tải authorization code phải trên một kênh bảo mật
- Client phải đảm bảo redirect uri phải xác thực qua TLS
- Nếu client sử dụng authorization code để làm phương thức xác thực tài nguyên của mình, phải đảm bảo mọi thức truyền tải trên giao thức TLS.
  Authorization code phải có tuổi đời ngắn và dùng một lần
- Nếu có thể xác thực người dùng, client phải xác thực chính xác người dùng và authorization code là tương ứng với nhau.

6. Việc xử lí redirect URI trong Authorization codes

- Redirect URI là một điểm nhạy cảm mà hacker rất dễ lợi dụng để tấn công cơ chế OAuth
- Authorization server phải yêu cầu public client
  Authorization server nên yêu cầu client đăng kí redirect URI
- Redirect URI phải được kiểm tra, đối chiều với redirect URI client đã đăng kí

7. Mật khẩu của resource owner

- Hạn chế tối đa việc sử dụng resource owner password credentials grant type
- Sử dụng các kiểu grant type khác nếu có thể

8. Tính bảo mật của request

- Access tokens, refresh tokens, resource owner passwords, and client credentials không được truyển tải dưới dạng cleartext
- Authorization code không nên được truyền đi dưới dạng cleartext
- Các tham số có thể truyền tải hoặc lưu trữ không an toàn như state hay scope không nên chứa các thông tin nhạy cảm của client hay resource owner dưới dạng cleartext

9. Xác thực endpoint

- Tất cả request giữa các endpoints phải truyền tải trên giao thức TLS
- Client phải xác nhận đúng chứng chỉ TLS của authorization server

10. Tấn công "đoán" thông tin xác thực

- Authorization server phải đảm bảo hacker không thể đoán được giá trị của access tokens, authorization codes, refresh tokens, resource owner passwords, and client credentials
  Xác suất kẻ tấn công đoán được access token phải nhỏ
- Authorization server phải có các cơ chế bổ sung nhằm đảm bảo xác thực của end-user.

11. Tấn công lừa đảo (phishing)

- Nhà cung cấp dịch vụ nên có các cơ chế để người dùng hiểu biết hơn về các tấn công lừa đảo
  Nên có các cơ chế xác thực đa yếu tố
- Để hạn chế phishing attack, authorization server phải sử dụng giao thức TLS cho tất cả các endpoint có tương tác với end-user.

12. Cross-site request forgery (CSRF)

- Authorization server phải có các cơ chế bảo vệ khỏi các tấn công CSRF cho redirect_uri
  Nên sử dụng tham số state như một csrf token cho các request
- Giá trị của csrf token phải đảm bảo là không thể đoán được
- Trạng thái xác thực của user-agent chỉ có thể được truy cập bởi client và user-agent (được bảo vệ bới Same-Origin Policy)

13. Click-jacking

- Ứng dụng native nên sử dụng một browser ngoài thay vì browser nhúng để thực hiện xác thực
- Đối với các browser đời mới, sử dụng header x-frame-options để ngăn việc sử dụng iframe
- Đối với các browser phiên bản thấp hơn, có thể sử dụng kĩ thuật JavaScript frame-busting (tuy nhiên không đảm bảo với tất cả browser)

14. Code injection và Input validation

- Authorization server phải có các cơ chế kiểm tra, xử lí, xác thực các giá trị được gửi lên từ phía client, đặc biệt với các tham số state và redirect_uri

15. Open redirect

- Authorization server phải có các cơ chế kiểm tra, xử lí, xác thực các giá trị được gửi lên từ phía client, đặc biệt với các tham số state và redirect_uri

16. Sử dụng access token sai mục đích trong implicit flow

- Access token của người dùng có thể bị đánh cắp bằng nhiều cách như phishing, CSRF attack ...
- Trong implicit flow, authorization rất khó xác định thực sự ai đang sử dụng access token
- Kẻ tấn công với access token đánh cắp từ người dùng có thể lấy được các thông tin của người dùng từ phía resource server

#### Phía Service

Yêu cầu ứng dụng khách đăng ký whitelist gồm redirect_uri hợp lệ. Điều này ngăn chặn kẻ tấn công truy cập vào các trang khác.
Thực thi việc sử dụng tham số trạng thái. giá trị của nó phải được ràng buộc với phiên của người dùng. giúp bảo vệ khỏi các cuộc tấn công CSRF.
trên máy chủ tài nguyên, đảm bảo xác minh access token đã được cấp cùng client_id thực hiện yêu cầu.

#### Phía client

đảm bảo hiểu chi tiết hoạt động của OAuth trước khi triển khai.
Sử dụng tham số state để đảm bảo an toàn
Gửi tham số redirect_uri không chỉ đến điểm cuối /authorization mà còn đến điểm cuối /token
áp dụng một số tiêu chuẩn có sẵn để đảm bảo an toan như RFC 7636 (chặn và chống rò rỉ token)

Dành cho nhà cung cấp dịch vụ OAuth

- Yêu cầu các ứng dụng khách hàng đăng ký danh sách trắng hợp lệ redirect_uris. Bất cứ khi nào có thể, hãy sử dụng so sánh byte-cho-byte nghiêm ngặt để xác thực URI trong bất kỳ yêu cầu nào đến. Chỉ cho phép khớp hoàn toàn và chính xác thay vì sử dụng khớp mẫu. Điều này ngăn chặn kẻ tấn công truy cập vào các trang khác trên các miền được liệt kê trắng.
- Thực thi việc sử dụng statetham số. Giá trị của tham số cũng phải được liên kết với phiên của người dùng bằng cách bao gồm một số dữ liệu không thể đoán trước, cụ thể cho phiên, chẳng hạn như hàm băm chứa cookie phiên. Điều này giúp bảo vệ người dùng khỏi các cuộc tấn công giống như CSRF. Nó cũng khiến kẻ tấn công khó sử dụng bất kỳ mã ủy quyền nào bị đánh cắp hơn nhiều.
- Trên máy chủ tài nguyên, hãy đảm bảo bạn xác minh rằng mã thông báo truy cập đã được cấp cho cùng một client_idngười đang thực hiện yêu cầu. - Bạn cũng nên kiểm tra phạm vi được yêu cầu để đảm bảo rằng phạm vi này khớp với phạm vi mà mã thông báo ban đầu được cấp.
  Đối với các ứng dụng khách hàng OAuth
- Hãy đảm bảo bạn hiểu đầy đủ chi tiết về cách OAuth hoạt động trước khi triển khai. Nhiều lỗ hổng là do thiếu hiểu biết đơn giản về những gì đang diễn ra ở từng giai đoạn và cách thức khai thác tiềm ẩn.
- Sử dụng statetham số ngay cả khi nó không bắt buộc.
- Gửi redirect_uritham số không chỉ đến /authorizationđiểm cuối mà còn đến /tokenđiểm cuối khác.
- Khi phát triển ứng dụng máy khách OAuth trên thiết bị di động hoặc máy tính để bàn gốc, thường không thể giữ được tính client_secret riêng tư. Trong những tình huống này, cơ chế PKCE( RFC 7636) có thể được sử dụng để cung cấp thêm khả năng bảo vệ chống lại việc chặn hoặc rò rỉ mã truy cập.
- Nếu bạn sử dụng OpenID Connect id_token, hãy đảm bảo rằng nó được xác thực đúng theo các thông số kỹ thuật của JSON Web Signature, JSON Web Encryption và OpenID.
- Hãy cẩn thận với mã ủy quyền - chúng có thể bị rò rỉ qua Referertiêu đề khi hình ảnh bên ngoài, tập lệnh hoặc nội dung CSS được tải. Điều quan trọng nữa là không đưa chúng vào các tệp JavaScript được tạo động vì chúng có thể được thực thi từ các miền bên ngoài thông qua `<script>`.

## 1. Lab: Authentication bypass via OAuth implicit flow

### Đề bài

![image](https://hackmd.io/_uploads/rJz0PjT3kl.png)

### Phân tích

Trong bài này, chúng ta sẽ lợi dụng lỗ hổng trong cơ chế xác thực OAuth của ứng dụng web để có thể đăng nhập vào tài khoản của Carlos, với điều kiện là chúng ta biết email của người dùng này.

Ở đây, có thể thấy response_type của request là token, nên có thể đoán rằng trang web sử dụng implicit grant type. Ngoài ra, tham số state cũng không nằm trong request, đồng nghĩa với các tấn công CSRF có thể thực hiện được.

Sau khi đang nhập và cấp quyền cho ứng dụng, ứng dụng sẽ gửi 1 request call back và browser sẽ lấy được access token trả về

Sau đó sử dụng access token này để truy cập tới /me để lấy dữ liệu với token truyền trong Authorizattion header

Tới đây mọi thứ vẫn ổn. Tuy nhiên sau đó là một request để xác minh người dùng của ứng dụng web

Ở đây, ứng dựng web gửi các thông tin đăng nhập của người dùng lên backend để xác minh người dùng nhằm mục đích đăng nhập. Tuy nhiên, backend lại chỉ sử dụng email để thực hiện xác minh thay vì cặp key-pair giữa email và token. Lợi dụng điểm này, ta có thể thay email của mình thành email của người khác (cụ thể ở bài này là Carlos) để có được quyền truy cập vào tài khoản của họ.

### Khai thác

![image](https://hackmd.io/_uploads/SJZoDJ0_Jx.png)

![image](https://hackmd.io/_uploads/SkfaDyRd1l.png)

![image](https://hackmd.io/_uploads/BJ90DkAdJe.png)

## 2. Lab: Forced OAuth profile linking

![image](https://hackmd.io/_uploads/SyVCmgRdyl.png)

![image](https://hackmd.io/_uploads/B1FlExCOJl.png)

![image](https://hackmd.io/_uploads/S10hQx0_Jg.png)

![image](https://hackmd.io/_uploads/BJ1G4xAdJg.png)

## 3. Lab: OAuth account hijacking via redirect_uri

### Đề bài

![image](https://hackmd.io/_uploads/SJE5J7R2ye.png)

### Phân tích

![image](https://hackmd.io/_uploads/rJNPWXAnyg.png)

![image](https://hackmd.io/_uploads/BJY_ZX03kx.png)

Mình có thể chỉnh redirect_uri tùy ý tại authorization request.

![image](https://hackmd.io/_uploads/rJxolXR21x.png)

Authorization code được gửi về đúng redirect_uri đã gửi.

![image](https://hackmd.io/_uploads/BkYogXCnye.png)

### Khai thác

Bây giờ chỉ việc gửi cho admin authorization request chứa redirect_uri là exploit-server.

![image](https://hackmd.io/_uploads/rJBXmQR3Jl.png)

![image](https://hackmd.io/_uploads/By8VQQR21g.png)

Ta sẽ nhận được authorization code của admin.

![image](https://hackmd.io/_uploads/Bk_FXXR3ke.png)

![image](https://hackmd.io/_uploads/B1M_4Q0nJx.png)

## 4. Lab: Stealing OAuth access tokens via an open redirect

### Đề bài

![image](https://hackmd.io/_uploads/r16zSQCn1e.png)

### Phân tích

Tại Authorization request, thử thay thế redirect_uri thành 1 URI khác thì bị báo không khớp trong whitelist.

![image](https://hackmd.io/_uploads/HyOBHQ03Je.png)

![image](https://hackmd.io/_uploads/HyOOS70hJe.png)

Như vậy redirect_uri phải chứa `https://<LAB-ID>.web-security-academy.net/oauth-callback.` Thử path traversal thì lại thấy thành công. Như vậy mình có thể lợi dụng để redirect về 1 URL mà tại đó có chức năng open redirect về domain attacker.

![image](https://hackmd.io/_uploads/HJ2qSmA31g.png)

Ta tìm được endpoint có chức năng open redirect đó là chức năng load next post có tham số path là URL nó sẽ redirect đến.

![image](https://hackmd.io/_uploads/r1V5SmAnyx.png)

Như vậy ta sẽ chỉnh redirect_uri thành như sau với path là exploit-server.

![image](https://hackmd.io/_uploads/r1bTBXC3yl.png)

Lúc này, oauth server sẽ request đến exploit-server để trả về access_token.

![image](https://hackmd.io/_uploads/Bk0sP70hkl.png)

### Khai thác

Bây giờ chỉ việc tạo payload. Đoạn script có chức năng khiến nạn nhân load authorization request → access_token trả ngược về exploit-server qua query string (vì URL fragment không xem được trong log).

![image](https://hackmd.io/_uploads/SkvEuQRhke.png)

Deliver exploit to victim, ta thấy nạn nhân đã thực hiện oauth thành công và ta lấy được access_token log.

## 5. Lab: SSRF via OpenID dynamic client registration

### Đề bài

![image](https://hackmd.io/_uploads/Sk5Yq7C3ke.png)

### Phân tích

Ta xem được openid config tại `<OAuth-server>/.well_known/openid-configuration`.

![image](https://hackmd.io/_uploads/HyU6cXCh1l.png)

![image](https://hackmd.io/_uploads/ByvOhQC3Jl.png)

Để ý thấy endpoint client app registration tại /reg. Thực hiện đăng kí client application thử với redirect_uris bất kì, ta thấy server trả về tạo thành công và có client_id.

![image](https://hackmd.io/_uploads/rkT62X03ye.png)

![image](https://hackmd.io/_uploads/SkG3aXC2ye.png)

Sử dụng client_id tương ứng và load logo, ta thấy đã có request đến collaborator → có thể SSRF.

![image](https://hackmd.io/_uploads/H19a0XCnkl.png)

Mặt khác quan sát ta thấy, bước confirm về thông tin có thể truy cập có xuất hiện request đến /client/<CLIENT_ID>/logo để hiển thị logo.

![image](https://hackmd.io/_uploads/Byd5R7Rn1x.png)

Và theo docs, thì nó lấy logo từ đường dẫn được định nghĩa tại logo_uri tương ứng với client_id. Ta kiểm tra out bound request đến collaborator không khi đăng kí new client app với logo_uri là collaborator URL

![image](https://hackmd.io/_uploads/H13FAQ03ye.png)

Làm lại các bước tương tự với logo_uri chính là đường dẫn đã cho http://169.254.169.254/latest/meta-data/iam/security-credentials/admin/.

![image](https://hackmd.io/_uploads/BJ8K0XC2Jx.png)

## 6. Lab: Stealing OAuth access tokens via a proxy page

### Đề bài

![image](https://hackmd.io/_uploads/HyUTkEAhke.png)

### Phân tích

Tương tự bài 4, ta có thể path traversal tại redirect_uri.

![image](https://hackmd.io/_uploads/HJ0yeN03Jg.png)

Tại mỗi post của blog, form comment được load bằng frame từ /post/comment/comment-form

![image](https://hackmd.io/_uploads/HyQSgN03Jg.png)

Tại đó, xuất hiện một postMessage() đến parent có origin bất kì \*, tức là trang đang dùng frame của comment form này, với message là window.location.href. Như vậy nếu trang exploit-server frame chứa comment-form này thì nó sẽ nhận được message chứa window.location.href. Và nếu redirect_uri của oauth là /post/comment/comment-form thì window.location.href sẽ chứa access_token.

### Khai thác

![image](https://hackmd.io/_uploads/S12c-4R2kl.png)

![image](https://hackmd.io/_uploads/rJZ3b4Rhke.png)

![image](https://hackmd.io/_uploads/ByLWz4R31x.png)

![image](https://hackmd.io/_uploads/BkilMVRh1e.png)

![image](https://hackmd.io/_uploads/r1xmzVR31g.png)

## Tham khảo thêm

- https://nhattruong.blog/2023/12/06/oauth-2-va-mot-so-tan-cong/
