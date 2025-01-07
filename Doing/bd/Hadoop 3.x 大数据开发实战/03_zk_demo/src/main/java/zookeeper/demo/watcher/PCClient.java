package zookeeper.demo.watcher;
import java.util.ArrayList;
import java.util.List;
import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
/**
 * 客户端类
 * 监听ZooKeeper中的指定节点，若子节点状态发生变化，则获取子节点列表
 */
public class PCClient {
	//ZooKeeper连接字符串
	private static final String CONNETC_STR = "192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
	//连接超时时间（两秒）
    private static final int SESSION_TIME_OUT = 2000;
    //指定需要监控的ZooKeeper中的节点，该节点需要提前在ZooKeeper中创建
    private static final String PARENT_NODE = "/serverGroup";
    ZooKeeper zk = null;
    //客户端连接ZooKeeper
    private void connectZookeeper() throws Exception {
        zk = new ZooKeeper(CONNETC_STR, SESSION_TIME_OUT, new Watcher(){
        	//监听事件的回调函数
            public void process(WatchedEvent event) {
            	System.out.println(event.getType()+"============"+event.getPath());
            	//如果节点"/serverGroup"下的子节点状态发生变化，重新获取服务器列表，并重新注册监听
                if(event.getType() == Event.EventType.NodeChildrenChanged && (PARENT_NODE).equals(event.getPath())){
                    try {
                    	//获取服务器列表
                    	getServerList();
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        });
        //获取在线服务器列表
        getServerList();
    }
    //获取在线服务器列表
    private void getServerList() throws Exception {
        //获取服务器子节点列表，并重新对父节点进行监听。参数true代表设置监听
        List<String> subNodeList = zk.getChildren(PARENT_NODE, true);
        //先创建一个List集合存储服务器信息
        List<String> newServerList = new ArrayList<String>();
        //循环服务器子节点列表，并将每个子节点的元数据字符串添加到newServerList集合
        for (String subNodeName : subNodeList) {
            byte[] data = zk.getData(PARENT_NODE+"/"+subNodeName, false, null);
            //输出节点元数据字符串
            newServerList.add(new String(data));
        }
        //输出当前在线服务器列表
        if(newServerList==null||newServerList.size()==0)
        	System.out.println("暂无服务器在线");
        else
        	System.out.println("服务器列表被更新："+newServerList);
    }
    /**
     * 客户端的业务逻辑写在该函数中，此处不做处理
     */
    private void handle() throws Exception {
        System.out.println("客户端正在处理业务逻辑...");
        //线程睡眠，防止退出
        Thread.sleep(Long.MAX_VALUE);
    }
    public static void main(String[] args) throws Exception {
        PCClient client = new PCClient();
        //连接ZooKeeper
        client.connectZookeeper();
        //客户端业务逻辑处理
        client.handle();
    }
}