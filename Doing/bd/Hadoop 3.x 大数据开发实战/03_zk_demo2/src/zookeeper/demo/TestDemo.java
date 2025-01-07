package zookeeper.demo;

import org.apache.zookeeper.WatchedEvent;
import org.apache.zookeeper.Watcher;
import org.apache.zookeeper.ZooKeeper;
import org.apache.zookeeper.data.Stat;

public class TestDemo {
	
	/**
	 * 修改节点数据
	 */
	public void setNodeData() throws Exception {  
    	String connectStr="192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
    	ZooKeeper zk  = new ZooKeeper(connectStr, 3000, null);  
        Stat stat = zk.setData("/zk002", "zk002_data2".getBytes(), -1);  
        System.out.println(stat.getVersion());
	}
	/**
	 * 获取节点数据
	 */
	public void getNodeData() throws Exception {  
    	String connectStr="192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
    	ZooKeeper zk  = new ZooKeeper(connectStr, 3000, null);  
    	Stat stat=new Stat();
		//返回指定路径上的节点数据和节点状态，节点的状态会放入stat对象中
		byte[] bytes=zk.getData("/zk002", null, stat);
		System.out.println(new String(bytes));
	}
	/**
	 * 获取节点数据，并加入观察者对象Watcher
	 */
	public void getNodeDataWatch() throws Exception {  
    	String connectStr="192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
    	ZooKeeper zk  = new ZooKeeper(connectStr, 3000, null);  
    	Stat stat=new Stat();
		//返回指定路径上的节点数据和节点状态，节点的状态会放入stat对象中
		byte[] bytes=zk.getData("/zk002", new Watcher(){
			public void process(WatchedEvent event) {
				System.out.println(event.getType());
			}
		}, stat);
		System.out.println(new String(bytes));
		//改变节点数据，触发watch
		zk.setData("/zk002", "zk002_data_testwatch".getBytes(), -1); 
		//为了验证是否触发了watch，不让程序结束
		while(true){
			Thread.sleep(3000);
		}	
	}

	
	public void deletePath() throws Exception{
		String connectStr="192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
		ZooKeeper zk  = new ZooKeeper(connectStr, 3000, null);  
		//删除节点 
		zk.delete("/zk002", -1);
	}

	
	public static void main(String[] args) throws Exception {
		String connectStr="192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181";
    	ZooKeeper zk  = new ZooKeeper(connectStr, 3000, null);  
        Stat stat = zk.setData("/zk002", "zk002_data2".getBytes(), -1);  
        System.out.println(stat.getVersion());
	}

}
