package zookeeper.demo.watcher;
import org.apache.zookeeper.CreateMode;
import org.apache.zookeeper.ZooDefs.Ids;
import org.apache.zookeeper.ZooKeeper;

/**
 * 服务端类
 * 服务器启动时连接ZooKeeper，并向指定节点创建临时子节点，若临时子节点状态发生变化将通知客户端
 */
public class PCServer {
	//ZooKeeper连接字符串
    private static final String CONNETC_STR = "192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
    //连接超时时间（两秒）
    private static final int SESSION_TIME_OUT = 2000;
    //指定ZooKeeper中的一个节点，服务器需要在该节点下创建子节点
    private static final String PARENT_NODE = "/serverGroup";
    /**
     * 连接到ZooKeeper服务器
     */
    public void connectZookeeper(String hostname) throws Exception {
    	ZooKeeper zk = new ZooKeeper(CONNETC_STR, SESSION_TIME_OUT,null);
        //当服务断掉时ZooKeeper将此临时节点删除，这样client就不会得到服务的信息了
        String path = zk.create(PARENT_NODE + "/server", hostname.getBytes(), Ids.OPEN_ACL_UNSAFE, CreateMode.EPHEMERAL_SEQUENTIAL);
        System.out.println("主机"+hostname+"在ZooKeeper中的临时节点为"+path);
    }
    /**
     * 服务器业务逻辑在此处编写
     */
    public void handle(String hostname) throws InterruptedException {
        System.out.println("主机"+hostname+"正在处理业务逻辑...");
        //线程睡眠，防止线程退出
        Thread.sleep(Long.MAX_VALUE);
    }
    public static void main(String[] args) throws Exception {
    	//声明当前服务器主机名，不同服务器修改此主机名即可
    	String hostname="serverHostName02";
        //连接ZooKeeper
        PCServer server = new PCServer();
        server.connectZookeeper(hostname);
        //业务逻辑处理
        server.handle(hostname);
    }
}