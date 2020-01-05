# 掼蛋-AI
本项目是一个基于启发式规则的掼蛋AI。采用C/S架构。

## 客户端
`/client`目录下是客户端代码，里面包含了四种客户端：
- `BaseClient`：其它三个客户端的基类客户端。
- `RandomClient`：随机出牌的客户端。
- `MinClient`： 出当前可出的最小牌的客户端。
- `HumanClient`：从命令行读取人类输入出牌的客户端。
- `AIClient`：基于启发式规则的AI客户端。

### BaseClient
`BaseClient`是其它三个客户端的基类客户端。它的作用是
- 报文处理：读取、解析、回应服务端的通讯报文。
- 记忆：记录当前已经出的牌、记录当前牌桌上的牌。
- 事件派发：在合适的时机调用三个分别定义为`my_play`、`others_play`、`finish`的事件接口，
交由继承`BaseClient`的客户端处理。子类客户端至少需要实现`my_play`方法。

## 服务端
服务端见另一个项目。

## 使用方法
首先启动服务端，然后从命令行使用下面的指令启动客户端：

    python gd.py <client_type> <name>
