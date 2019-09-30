# 실시간 채팅 구현
- 실시간으로 데이터를 송수신하는 시스템을 구축하려면 관계형 데이터베이스와 Ajax호출로는 불가능하다고 한다.
- 검색해본 결과, 대부분의 멀티 채팅 시스템은 웹소켓이란 것을 활용한다.
- 많은 자료가 있는데 거의 대부분은 socket.io랑 node.js를 사용하는 것 같다.

- 웹소켓은 다음의 특징을 가진다.
- 1) http통신의 단점을 개선
- 2) 영구적 양방향 통신
- 3) client와 server가 실시간으로 메시지를 자유롭게 주고 받을 수 있음.
- 따라서 멀티 채팅에는 웹소켓이 활용되어야 한다.

- node.js는 서버를 위한 프로그램이고, socket.io는 소켓통신을 위해 필요하다.
- 프로그램은 모두 javascript를 기반으로 한다.

- /* Server Source */
- var io = require('socket.io').listen(80);

- io.sockets.on('connection', function (socket) {
-  socket.emit('news', { hello: 'world' });
-  socket.on('my other event', function (data) {
-    console.log(data);
-  });
- });

- /* Client Source */
- <script src="/socket.io/socket.io.js"></script>
- <script>
-  var socket = io.connect('http://localhost');
-  socket.on('news', function (data) {
-    console.log(data);
-    socket.emit('my other event', { my: 'data' });
-  });
- </script>

- node.js+socket.io를 활용한 서버와 클라이언트의 기본적인 소스는 위와 같다.

- 위 방법의 경우 천 여명 이상이 접속할 경우 과부화의 위험도 있다.
- 포스텍 대상의 채팅앱이기 때문에 걱정해야할지는 모르겠지만, 그럴 경우 redis를 활용하거나 pinus라는 게임 서버 프레임워크를 활용하면 해결할 수 있을 것 같다.