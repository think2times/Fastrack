package zookeeper.demo;

import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.ZooDefs.Ids;

/**
 * 创建ZooKeeper节点，并设置元数据
 */
public class CreatePath {

  public static void main(String[] args) throws Exception {
    String connectStr = "centos01:2181,centos02:2181,centos03:2181";
    // 参数1：服务器连接字符串
    // 参数2：连接超时时间
    // 参数3：观察者对象（回调方法）
    ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);
    /*
     * CreateMode 取值如下：
     * PERSISTENT：持久节点 
     * PERSISTENT_SEQUENTIAL：持久顺序节点(自动编号)
     * EPHEMERAL：临时节点，客户端断开连接时，这种节点会被自动删除 
     * EPHEMERAL_SEQUENTIAL：临时顺序节点
     */
    String path = zk.create("/zk001", "zk001_data".getBytes(),
        Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
    System.out.println(path);
  }
}
