package hbase.demo;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Delete;
import org.apache.hadoop.hbase.client.Table;
import org.apache.hadoop.hbase.util.Bytes;
/**
 * 删除表t1中行键为row1的一整条数据
 */
public class HBaseDeleteData{
	public static void main(String[] args) throws Exception {
		//创建HBase配置对象
		Configuration conf=HBaseConfiguration.create();
		//指定ZooKeeper集群地址
		conf.set("hbase.zookeeper.quorum", "192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181");
		//获得数据库连接
        Connection conn=ConnectionFactory.createConnection(conf);
	    //获取Table对象，指定表名，Table负责与记录相关的操作,如增删改查等
	    TableName tableName=TableName.valueOf("t1");
	    Table table=conn.getTable(tableName);
	    //创建删除对象Delete，根据rowkey删除一整条
	    Delete delete=new Delete(Bytes.toBytes("row1"));
	    table.delete(delete);
        //释放资源
        table.close();
        System.out.println("delete data success!!");
	}
}
