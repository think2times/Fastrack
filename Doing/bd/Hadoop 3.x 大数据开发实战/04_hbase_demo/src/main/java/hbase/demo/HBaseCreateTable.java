package hbase.demo;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.client.Admin;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptor;
import org.apache.hadoop.hbase.client.ColumnFamilyDescriptorBuilder;
import org.apache.hadoop.hbase.client.Connection;
import org.apache.hadoop.hbase.client.ConnectionFactory;
import org.apache.hadoop.hbase.client.TableDescriptor;
import org.apache.hadoop.hbase.client.TableDescriptorBuilder;
import org.apache.hadoop.hbase.util.Bytes;

/**
 * 在HBase中创建一张表
 */
public class HBaseCreateTable {
    public static void main(String[] args) throws Exception {
        //1.集群配置信息
        //创建HBase配置对象
        Configuration conf = HBaseConfiguration.create();
        //指定ZooKeeper集群地址
        conf.set("hbase.zookeeper.quorum",
                "192.168.170.133:2181,192.168.170.134:2181,192.168.170.135:2181");
        //创建连接对象Connection
        Connection conn = ConnectionFactory.createConnection(conf);
        //得到数据库管理员对象
        Admin admin = conn.getAdmin();

        //2.表描述信息
        //指定表名为“t1”。TableName为表示表名的不可变POJO类
        TableName tableName = TableName.valueOf("t1");
        //创建表描述构造器
        TableDescriptorBuilder tableDescriptorBuilder = TableDescriptorBuilder.newBuilder(tableName);
        //创建列族描述器，指定列族名称为“f1”
        ColumnFamilyDescriptor columnFamilyDescriptor = ColumnFamilyDescriptorBuilder.newBuilder(Bytes.toBytes("f1")).build();
        //向表描述构造器中添加列族
        tableDescriptorBuilder.setColumnFamily(columnFamilyDescriptor);
        //创建表描述器
        TableDescriptor tableDescriptor = tableDescriptorBuilder.build();
        
        //3.请求HBase，执行创建表命令
        admin.createTable(tableDescriptor);
        System.out.println("create table success!!");
    }
}
