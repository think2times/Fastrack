package hbase.demo.filter;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.Cell;
import org.apache.hadoop.hbase.CellUtil;
import org.apache.hadoop.hbase.CompareOperator;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.TableName;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.hbase.filter.*;
import org.apache.hadoop.hbase.client.*;

/**
 * 使用单列值过滤器组合筛选出年龄在18到30岁之间的所有数据
 */
public class HBaseMultiFilterDemo {
  static Configuration conf = null;
  static {
    // 创建HBase配置对象
    conf = HBaseConfiguration.create();
    // 配置ZooKeeper连接地址
    conf.set("hbase.zookeeper.quorum",
        "centos01:2181,centos02:2181,centos03:2181");
  }

  public static void main(String[] args) throws Exception {
    filterTest();
  }

  /**
   * 创建表t1 ,列族f1
   * 
   * @throws Exception
   */
  public static void filterTest() throws Exception {
    // 得到数据库连接
    Connection conn = ConnectionFactory.createConnection(conf);
    // 指定要查询的表t1
    Table table = conn.getTable(TableName.valueOf("t1"));
    Scan scan = new Scan();
    // 创建过滤器1，查询年龄小于等于30岁的所有数据
    Filter filter1 = new SingleColumnValueFilter(Bytes.toBytes("f1"),
        Bytes.toBytes("age"), CompareOperator.LESS_OR_EQUAL,
        Bytes.toBytes("30"));
    // 创建过滤器2，查询年龄大于等于18岁的所有数据
    Filter filter2 = new SingleColumnValueFilter(Bytes.toBytes("f1"),
        Bytes.toBytes("age"), CompareOperator.GREATER_OR_EQUAL,
        Bytes.toBytes("18"));
    // 创建过滤器集合对象
    FilterList filterList = new FilterList();
    // 添加过滤器1
    filterList.addFilter(filter1);
    // 添加过滤器2
    filterList.addFilter(filter2);
    // 设置过滤器
    scan.setFilter(filterList);
    // 执行查询，得到结果集
    ResultScanner rs = table.getScanner(scan);
    // 输出结果，每个res代表一行数据
    for (Result res : rs) {
      printResult(res);
      System.out.println("--------------------------------");

    }

    rs.close();
  }

  /**
   * 输出一行中所有单元格的信息
   */
  public static void printResult(Result res) {
    if (!res.toString().equals("keyvalues=NONE")) {
      // 循环输出每个单元格的数据
      for (Cell cell : res.rawCells()) {
        // 取得当前单元格所属的行键
        String rowkey = new String(CellUtil.cloneRow(cell));
        // 取得当前单元格所属的列族名称
        String family = new String(CellUtil.cloneFamily(cell));
        // 取得当前单元格所属的列名称
        String qualifier = new String(CellUtil.cloneQualifier(cell));
        // 取得当前单元格的列值
        String value = new String(CellUtil.cloneValue(cell));
        // 输出结果
        System.out.println("行键：" + rowkey + "—————列：" + family + ":"
            + qualifier + "—————值:" + value);
      }

    }
  }

}
