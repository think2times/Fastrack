package zookeeper.demo;

import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;
import org.junit.Test;


/**
 * 对ZooKeeper节点数据的查询、删除和修改
 */
public class NodeTestDemo {

  /**
   * 修改节点数据
   */
  @Test
  public void setNodeData() throws Exception {
    String connectStr = "centos01:2181,centos02:2181,centos03:2181";
    ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);
    Stat stat = zk.setData("/zk001", "zk001_data_new".getBytes(), -1);
    //输出节点版本号
    System.out.println(stat.getVersion());
  }


  /**
   * 获取节点元数据
   */
  @Test
  public void getNodeData() throws Exception {
    //ZooKeeper连接字符串
    String connectStr = "centos01:2181,centos02:2181,centos03:2181";
    ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);
    Stat stat = new Stat();
    //返回指定路径上的节点数据和节点状态，节点的状态会放入stat对象中
    byte[] bytes = zk.getData("/zk002", null, stat);
    //输出节点元数据
    System.out.println(new String(bytes));
  }


  /**
   * 获取节点数据，并加入观察者对象Watcher（一次监听）
   */
  @Test
  public void getNodeDataWatch() throws Exception {
    String connectStr = "centos01:2181,centos02:2181,centos03:2181";
    ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);
    Stat stat = new Stat();
    
    //返回指定路径上的节点数据和节点状态，节点的状态会放入stat对象中
    byte[] bytes = zk.getData("/zk002", new Watcher() {
      //实现process()方法
      public void process(WatchedEvent event) {
        System.out.println(event.getType());
      }
    }, stat);
    
    System.out.println(new String(bytes));
    //改变节点数据，触发watch
    zk.setData("/zk002", "zk002_data_testwatch".getBytes(), -1);
    //为了验证是否触发了watch，不让程序结束
    while (true) {
      Thread.sleep(3000);
    }
  }


  /**
   * 获取节点数据，并加入观察者对象Watcher，实现持续监听
   */
  @Test
  public void getNodeDataWatch2() throws Exception {
    String connectStr = "centos01:2181,centos02:2181,centos03:2181";
    final ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);
    final Stat stat = new Stat();
    //定义Watcher对象
    Watcher watcher = new Watcher() {
      //实现process()方法
      public void process(WatchedEvent event) {
        //输出事件类型
        System.out.println(event.getType());
        //重新设置监听，参数this代表当前Watcher对象
        try {
          zk.getData("/zk001", this, stat);
        } catch (Exception e) {
          e.printStackTrace();
        }
      }
    };

    //返回指定路径上的节点数据和节点状态，并设置Watcher监听，节点的状态会放入stat对象中
    byte[] bytes = zk.getData("/zk001", watcher, stat);
    System.out.println(new String(bytes));
    //改变节点数据，触发watch
    //为了验证是否触发了watch，不让程序结束
    while (true) {
      Thread.sleep(3000);
    }
  }

  /**
   * 删除节点
   */
  @Test
  public void deletePath() throws Exception {
    String connectStr = "centos01:2181,centos02:2181,centos03:2181";
    ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);
    //删除节点
    zk.delete("/zk002", -1);
  }


  @Test
  public void existsPath() throws Exception {
    String connectStr = "192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
    ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);
    // 删除节点
    Stat stat = zk.exists("/zk001", null);
    System.out.println(stat.toString());
  }

}
