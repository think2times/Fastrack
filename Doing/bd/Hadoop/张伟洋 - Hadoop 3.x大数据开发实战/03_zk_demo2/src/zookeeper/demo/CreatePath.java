package zookeeper.demo;
import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.ZooDefs.Ids;

/**
 * 创建ZooKeeper节点，并设置元数据
 */
public class CreatePath {

	public static void main(String[] args) throws Exception {
		String connectStr="192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
		//参数1：服务器连接字符串
		//参数2：连接超时时间
		//参数3：观察者对象（回调函数）
		ZooKeeper zk = new ZooKeeper(connectStr, 3000, null);		
		/* 1.CreateMode 取值   
	     *  PERSISTENT：持久化节点
	     *  PERSISTENT_SEQUENTIAL：顺序自动编号的目录节点
	     *  EPHEMERAL：临时目录节点，客户端断开连接时，这种节点会被自动删除 
	     *  EPHEMERAL_SEQUENTIAL：临时自动编号节点 
	     *  */
		String path=zk.create("/zk001", "zk001_data".getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.PERSISTENT);
		System.out.println(path);
	}
}
