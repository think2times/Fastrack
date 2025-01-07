package hbase.demo;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.Get;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Table;
/**
 * 查询表t1中的行键为row1的一行数据
 */
public class HBaseGetData{
	public static void main(String[] args) throws Exception {
		//创建HBase配置对象
		Configuration conf=HBaseConfiguration.create();
		//指定ZooKeeper集群地址
		conf.set("hbase.zookeeper.quorum", "192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181");
        //获得数据库连接
        Connection conn=ConnectionFactory.createConnection(conf);
	   //获取Table对象，指定查询表名，Table负责与记录相关的操作,如增删改查等
        Table table = conn.getTable(TableName.valueOf("t1"));  
        //创建Get对象，根据rowkey查询,rowkey=row1  
        Get get = new Get("row1".getBytes());
        //查询数据，取得结果集
        Result r = table.get(get); 
        //循环输出每个单元格的数据
        for (Cell cell : r.rawCells()) {  
        	//取得当前单元格所属的列族名称
        	String family=new String(CellUtil.cloneFamily(cell));
        	//取得当前单元格所属的列名称
        	String qualifier=new String(CellUtil.cloneQualifier(cell));
        	//取得当前单元格的列值
        	String value=new String(CellUtil.cloneValue(cell));
        	//输出结果
        	System.out.println("列：" + family+":"+qualifier + "—————值:" + value);  
        }  
	}
}
